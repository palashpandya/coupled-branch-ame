"""Mechanical factor certificates; the unbounded classification uses the text proof."""
import json
from math import prod
from fractions import Fraction
from ._paths import DATA, RESULTS
def factor(n):
 out=[];p=2
 while p*p<=n:
  a=1
  while n%p==0:n//=p;a*=p
  if a>1:out.append((p,a))
  p+=1
 if n>1:out.append((n,n))
 return out
def odd(n):return [q for p,q in factor(n)]
def split(d):
 m=d;e=0
 while m%2==0:m//=2;e+=1
 if e==0:return odd(m)
 if e>=2:return [2**e]+odd(m)
 if m%3==0:return [6]+odd(m//3)
 p=factor(m)[0][0];assert p>=5
 return [2*p]+odd(m//p)
def main():
 rows=[]
 for d in range(3,2001):
  xs=split(d);assert prod(xs)==d and all(x>=3 for x in xs)
  rows.append(dict(d=d,factors=xs))
 old=json.loads((DATA/'prime_powers/product_coverage.json').read_text())
 for r in old['cases']:assert [x['d'] for x in r['factors']]==split(r['d'])
 expectation=sum((-1)**((m&255).bit_count())*Fraction(1,2**min(m.bit_count(),9-m.bit_count())) for m in range(512))
 assert expectation==Fraction(-1,4)
 out=dict(status='PASS',range=[3,2000],cases=rows,binary9_shadow=str(expectation),scope='Conditional product deduction from certified/cited inputs; finite sweep is not the infinite proof; external9,6 verification is separate')
 (RESULTS/'product_classification.json').write_text(json.dumps(out,indent=2)+'\n');print('[PASS] product factors3..2000 and binary9 shadow')
if __name__=='__main__':main()
