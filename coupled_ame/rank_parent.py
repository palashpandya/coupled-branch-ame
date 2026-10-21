#!/usr/bin/env python3
"""Exact CPU verifier for o4_binary_coupling_v1 JSON.
Default: N=13, p=13, <=13 positive-weight branches. --control permits p=17
and <=17 branches, solely to replay the AME(13,34) positive control.
Tableau rows are {x: bitmask,z: bitmask,sign: +/-1}, denoting
sign*i^popcount(x&z) X^x Z^z; bit i is party i. Thirteen independent,
commuting rows specify a pure stabilizer state.
Alternatively {kind:'amplitudes',amplitudes:{index:[real,imag]}} specifies a
nonzero exact Q(i) direction, normalized internally. Rational scalars are
JSON integers or fraction strings (floats are rejected). Missing indices=0.
This also allows rational amplitudes by setting imag=0. No cyclotomic input
is claimed. Parent: symmetric zero-diagonal 14x14 graph over F_p.
Distinct branch label a conditions vertex 0. State sum sqrt(weight)*u_a*v_a;
local digit p*b+y. No dense composite state is allocated.
"""
import argparse,json,itertools,math,sys
from collections import defaultdict,Counter
from fractions import Fraction as F
from pathlib import Path

def require(c,msg):
 if not c:raise ValueError(msg)
def rat(v):
 require(type(v) in (str,int),'rational must be an integer or fraction string')
 return F(v)
def rank2(rows):
 p={}
 for w in rows:
  while w:
   i=w.bit_length()-1
   if i in p:w^=p[i]
   else:p[i]=w;break
 return len(p)
def mul(a,b):
 x,z,e=a;u,v,f=b
 return x^u,z^v,(e+f+2*((z&u).bit_count()%2))%4

def tableau_terms(state,n):
 rows=state['generators'];require(len(rows)==n,'pure tableau needs N generators')
 gs=[]
 for r in rows:
  x,z,s=r['x'],r['z'],r['sign']
  require(type(x)==type(z)==int and 0<=x<1<<n and 0<=z<1<<n,'bad Pauli mask')
  require(type(s)==int and s in [-1,1],'bad Pauli sign')
  gs.append((x,z,((x&z).bit_count()+(0 if s==1 else 2))%4))
 require(rank2([x|(z<<n) for x,z,e in gs])==n,'dependent tableau')
 require(all(((x&v).bit_count()+(z&u).bit_count())%2==0 for x,z,e in gs for u,v,f in gs),'noncommuting tableau')
 elems=[(0,0,0)]
 for g in gs:elems += [mul(a,g) for a in elems]
 for x,z,e in elems:
  if 1<=(x|z).bit_count()<=n//2:
   phase=(e-(x&z).bit_count())%4;require(phase in [0,2],'non-Hermitian product')
   yield x|(z<<n),1 if phase==0 else -1

def amplitude_data(state,n):
 a={};den=1
 for key,pair in state['amplitudes'].items():
  b=int(key);require(str(b)==str(key) and 0<=b<1<<n,'bad amplitude index')
  require(len(pair)==2,'amplitude needs [real,imag]')
  re,im=map(rat,pair);a[b]=(re,im);den=math.lcm(den,re.denominator,im.denominator)
 a={b:(int(re*den),int(im*den)) for b,(re,im) in a.items() if re or im}
 norm=sum(re*re+im*im for re,im in a.values());require(norm>0,'zero amplitude vector')
 return a,norm

def fwht(a):
 h=1
 while h<len(a):
  for i in range(0,len(a),2*h):
   for j in range(i,i+h):
    u,v=a[j],a[j+h];a[j],a[j+h]=u+v,u-v
  h*=2

def amplitude_terms(a,n):
 # Each x has <=6 nonzero bits. All z with wt(x|z)<=6 are examined.
 # Coefficients are Gaussian-integer autocorrelation Walsh transforms.
 size=1<<n;zero=(0,0)
 for x in range(size):
  if x.bit_count()>n//2:continue
  re=[0]*size;im=[0]*size
  for b,(r,s) in a.items():
   t,u=a.get(b^x,zero);re[b]=t*r+u*s;im[b]=t*s-u*r
  if not any(re) and not any(im):continue
  fwht(re);fwht(im)
  for z in range(size):
   if not 1<=(x|z).bit_count()<=n//2:continue
   phase=(x&z).bit_count()%4
   val=[re[z],-im[z],-re[z],im[z]][phase]
   imaginary=[im[z],re[z],-im[z],-re[z]][phase]
   require(imaginary==0,'Hermitian expectation unexpectedly complex')
   if val:yield x|(z<<n),val

def modrank(A,p):
 a=[row[:] for row in A];r=0
 for col in range(len(a[0])):
  pivot=next((j for j in range(r,len(a)) if a[j][col]%p),None)
  if pivot is None:continue
  a[r],a[pivot]=a[pivot],a[r];inv=pow(a[r][col]%p,-1,p)
  a[r]=[(t*inv)%p for t in a[r]]
  for j in range(r+1,len(a)):
   v=a[j][col]%p;a[j]=[(x-v*y)%p for x,y in zip(a[j],a[r])]
  r+=1
 return r

def verify_parent(A,p):
 require(type(p)==int and p>=2 and all(p%d for d in range(2,math.isqrt(p)+1)),'parent field must be prime')
 require(len(A)==14 and all(len(row)==14 for row in A),'parent must be 14x14')
 require(all(type(x)==int and 0<=x<p for row in A for x in row),'parent entries not canonical field elements')
 require(all(A[i][i]==0 for i in range(14)) and all(A[i][j]==A[j][i] for i in range(14) for j in range(14)),'invalid parent graph')
 hist=Counter()
 for S in itertools.combinations(range(14),7):
  T=[j for j in range(14) if j not in S];r=modrank([[A[i][j] for j in T] for i in S],p);hist[r]+=1
  require(r==7,'parent balanced cut is singular: '+str(S))
 return {'classification':'exact','balanced_cut_orientations':sum(hist.values()),'rank_histogram':dict(hist)}

def verify(spec,control=False):
 require(spec['schema']=='o4_binary_coupling_v1','unknown schema')
 require(spec['N']==13,'N must be 13');n=13;p=spec['p']
 require(p==(17 if control else 13),'p must be 13 (or 17 with explicit --control)')
 bs=spec['branches'];require(0<len(bs)<=(17 if control else 13),'too many branches')
 ws=[rat(b['weight']) for b in bs]
 require(all(w>=0 for w in ws) and sum(ws)==1,'weights must be nonnegative and sum to one')
 labels=[b['parent_label'] for b in bs]
 require(all(type(x)==int and 0<=x<p for x in labels) and len(set(labels))==len(labels),'parent labels must be distinct field elements')
 coeff=defaultdict(F);counts=[]
 for b,w in zip(bs,ws):
  state=b['state'];kind=state['kind']
  if kind=='tableau':terms=tableau_terms(state,n);scale=w
  elif kind=='amplitudes':
   a,norm=amplitude_data(state,n);terms=amplitude_terms(a,n);scale=w/norm
  else:raise ValueError('unsupported state kind: '+str(kind))
  c=0
  for P,val in terms:coeff[P]+=scale*val;c+=1
  counts.append(c)
 bad=[(P,str(v)) for P,v in coeff.items() if v]
 require(not bad,'nonzero low-weight Pauli coefficients: '+str(bad[:8]))
 parent=verify_parent(spec['parent_graph'],p)
 return {'classification':'exact','valid':True,'AME':[13,2*p],'branches':len(bs),'binary_low_Paulis_total':sum(math.comb(13,j)*3**j for j in range(1,7)), 'branch_nonzero_low_Paulis':counts,'union_nonzero_branch_Paulis':len(coeff),'all_weight_1_to_6_coefficients_zero':True,'parent':parent,'coupling':'parent reference+6 reductions are I/p^7; conditioning gives delta_ab I/p^6; binary mixture gives I/2^6'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('spec');p.add_argument('--control',action='store_true');args=p.parse_args()
 try:out=verify(json.loads(Path(args.spec).read_text()),args.control)
 except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:print(json.dumps({'valid':False,'error':str(e)}));sys.exit(1)
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
