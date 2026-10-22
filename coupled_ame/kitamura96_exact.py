"""Optional dense all-cut check adapted from Claude's independently written verifier.
No tensors are saved. Integer sixth-root coefficients eliminate transcendental
rounding: w^e=(r[e]+i*sqrt(3)*s[e])/2. Float64 BLAS operates only on exactly
representable integer products and sums bounded by 4*6**5 << 2**53.
"""
import itertools, json, re, os, hashlib, time
from pathlib import Path
import numpy as np
from ._paths import DATA, RESULTS
def read_matrices(text):
    out = {}
    for name in 'GBHC':
        block = re.search(rf'def {name} : Matrix.*?:=(.*?)(?=\ndef |\ntheorem |\Z)', text, re.S).group(1)
        nums = [int(v) for v in re.findall(r'-?\d+', block)]
        assert len(nums) == 81, (name, len(nums))
        out[name] = np.array(nums).reshape(9, 9)
    return out


def exponents(m, drop_mixed=False):
    G, B, H, C = (m[k] for k in 'GBHC')
    X = ((np.arange(2 ** 9)[:, None] >> np.arange(8, -1, -1)) & 1)
    Y = (np.arange(3 ** 9)[:, None] // 3 ** np.arange(8, -1, -1)) % 3
    qC = np.einsum('bi,ij,bj->b', Y, np.triu(C, 1), Y) % 3
    e = np.empty((2,) * 9 + (3,) * 9, np.int8).reshape(2 ** 9, 3 ** 9)
    for xi, x in enumerate(X):
        qG = int(x @ np.triu(G, 1) @ x) % 2
        mixed = 0 if drop_mixed else (Y @ (x @ B) + int(x @ np.triu(H, 1) @ x))
        e[xi] = (3 * qG + 2 * ((qC + mixed) % 3)) % 6
    # axes: x_0..x_8, y_0..y_8 -> party i digit = 3 x_i + y_i ; reorder to (x_0,y_0,...,x_8,y_8)
    e = e.reshape((2,) * 9 + (3,) * 9).transpose([a for i in range(9) for a in (i, 9 + i)])
    return np.ascontiguousarray(e.reshape((6,) * 9))


def check(e,label):
    # R=(rr^T+3ss^T + i sqrt(3)(sr^T-rs^T))/4.
    # Dot products contain 7776 integer terms of magnitude <=4. Every
    # ordinary IEEE binary64 multiply/add (including FMA) is exact here.
    r=np.array([2,1,-1,-2,-1,1],dtype=np.float64)[e]
    s=np.array([0,1,1,0,-1,-1],dtype=np.float64)[e]
    bad=0;worst=0;records=[]
    for A in itertools.combinations(range(9),4):
        rest=[i for i in range(9) if i not in A]
        rr=r.transpose(list(A)+rest).reshape(6**4,6**5)
        ss=s.transpose(list(A)+rest).reshape(6**4,6**5)
        real=rr@rr.T+3*(ss@ss.T)
        cross=ss@rr.T;imag=cross-cross.T
        real.flat[::6**4+1]-=4*6**5
        assert np.all(real==np.rint(real)) and np.all(imag==np.rint(imag))
        err=int(max(np.max(np.abs(real)),np.max(np.abs(imag))))
        bad+=int(err!=0);worst=max(worst,err)
        records.append(dict(cut=list(A),max_integer_coefficient_error=err))
    return dict(label=label,cuts=126,cuts_failing=bad,max_integer_coefficient_error=worst,exact=bad==0,cut_records=records)
def main():
    pin=json.loads((DATA/'kitamura96-source.json').read_text());name=os.environ.get('KITAMURA96_DATA')
    if not name:
        out=dict(status='NOT_RUN',reason='Supply KITAMURA96_DATA; see docs/R11-audit.md')
    else:
        source=Path(name);assert hashlib.sha256(source.read_bytes()).hexdigest()==pin['sha256']
        m=read_matrices(source.read_text());start=time.perf_counter()
        positive=check(exponents(m),'Kitamura AME(9,6)');assert positive['exact']
        print('[PASS] positive126 cuts',flush=True)
        negative=check(exponents(m,drop_mixed=True),'B and H removed');assert negative['cuts_failing']==18
        out=dict(status='PASS',source_sha256=pin['sha256'],positive=positive,negative=negative,seconds=time.perf_counter()-start,
          arithmetic='IEEE binary64 exact integer dot products: inputs r in[-2,2],s in[-1,1],7776 terms; intermediate bound<2^53. No transcendental rounding or tolerance acceptance.',
          gap='Z[w],w=exp(i*pi/3): |a+b*w|^2=a*a+a*b+b*b; a nonzero element has modulus>=1. Integer coefficients prove exact zero directly.')
    (RESULTS/'kitamura96_exact.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
