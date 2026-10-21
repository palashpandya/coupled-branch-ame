"""Run every verifier module, capture logs, and record the environment."""
from ._paths import ROOT, RESULTS
import os
import platform
import subprocess
import sys
import time
for variable in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]:
    os.environ[variable] = "1"
import numpy
import sympy
import mpmath
(RESULTS/'environment.txt').write_text(
    f'Python {platform.python_version()}\nPlatform {platform.system()} {platform.machine()}\n'
    f'numpy {numpy.__version__}\nsympy {sympy.__version__}\nmpmath {mpmath.__version__}\n'
    'Numerical scope: three deterministic binary cuts per cell for N<=15.\n'
    'All required cuts are checked exactly by two independent implementations.\n')
start=time.perf_counter(); records=[]
for name in ['o3_verify','sym1_verify','independent','rank_and_c15','farkas_symbolic','permutation_cycles','parent13','reconstruct','inventory']:
    then=time.perf_counter()
    with (RESULTS/(name+'.log')).open('w') as out:
        result=subprocess.run([sys.executable,'-m','coupled_ame.'+name],cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
        elapsed=time.perf_counter()-then
        out.write(f'\n[runner] exit={result.returncode} elapsed_seconds={elapsed:.3f}\n')
    records.append(f'{name}: exit={result.returncode}, seconds={elapsed:.3f}')
    print(records[-1],flush=True)
records.append(f'total_seconds={time.perf_counter()-start:.3f}')
(RESULTS/'timings.txt').write_text('\n'.join(records)+'\n')
if any('exit=0,' not in s for s in records[:-1]):sys.exit(1)
print('[PASS] all verifier modules')
