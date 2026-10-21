"""Build vector figures from exact checked exports; run after run_all.sh."""
from pathlib import Path
import hashlib
import json
import sys
import os
import tempfile
os.environ.setdefault("MPLCONFIGDIR", tempfile.mkdtemp(prefix="ame-figures-"))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from coupled_ame.codes import span, weight
OUT = Path(__file__).resolve().parent

def read(path):
    return json.loads((ROOT/path).read_text())

plt.rcParams.update({'font.size':8, 'font.family':'STIXGeneral', 'mathtext.fontset':'stix',
                     'axes.linewidth':.6, 'pdf.fonttype':42})
support = read('results/support.json')
assert support['status']=='PASS'
assert support['input_sha256']==hashlib.sha256((ROOT/'data/o3_external_spec.json').read_bytes()).hexdigest()
c = support['cells']['15_26']; k,p = c['K'],c['p']
assert (k,p)==(8,13)
a = np.array(c['squared_S_canonical'], dtype=int)
assert a.shape==(k,p,p-1)
zero = np.all(a==0,axis=2)
expected = np.zeros((k,p),dtype=bool); expected[1:,0]=True
assert np.array_equal(zero,expected)
assert np.array_equal(np.sum(a,axis=(0,1)), [k*k*p]+[0]*(p-2))
assert len({tuple(v) for row in a for v in row})==c['distinct_intensities_including_zero']==50
assert c['number_zero_cells']==7 and c['support_fraction']=='97/104'
roots = np.exp(2j*np.pi*np.arange(p-1)/p)
values = a @ roots
assert np.max(np.abs(values.imag))<1e-10
r = values.real/k
assert np.all(r[~zero]>0) and abs(r.mean()-1)<1e-12
r[zero]=0
fig,ax=plt.subplots(figsize=(3.4,2.7))
im=ax.imshow(np.ma.array(r,mask=zero),cmap='cividis',norm=Normalize(0,k),
             interpolation='none',aspect='equal',origin='upper')
y,x=np.where(zero)
ax.scatter(x,y,marker='x',s=17,color='black',linewidths=.7,label='exact zero')
ax.set(xticks=range(p),yticks=range(k),yticklabels=[f'{i:03b}' for i in range(k)],
       xlabel=r'$t=h\cdot y\ \mathrm{(mod}\ 13)$',ylabel=r'$\sigma$ (binary syndrome)')
ax.tick_params(length=2,pad=2)
cb=fig.colorbar(im,ax=ax,fraction=.045,pad=.035,ticks=[0,2,4,6,8])
cb.set_label(r'$R=|S(\sigma,t)|^2/8$',labelpad=4)
ax.set_title('AME(15,26): 97 of 104 cells occupied',loc='left',fontsize=8)
fig.tight_layout(pad=.35)
fig.savefig(OUT/'support.pdf',metadata={'CreationDate':None});plt.close(fig)

certs=read('data/o3_binary_certificates.json')['ingredients']
verified=read('results/o3_verification.json')['constructions']
fig,axes=plt.subplots(1,3,figsize=(7,2.25),sharey=True)
for ax,n,k,key,cell in zip(axes,[13,15,17],[16,8,64],['13_16','15_8','17_64'],['13_34','15_34','17_134']):
    cert=certs[key]; counts={int(w):v for w,v in cert['weight_enumerator'].items()}
    actual={w:0 for w in counts}
    for v in span(cert['generators']):
        w=weight(v,n);actual[w]=actual.get(w,0)+1
    assert actual==counts=={int(w):v for w,v in verified[cell]['binary_weight_enumerator'].items()}
    assert verified[cell]['passed'] and sum(counts.values())==2**n//k
    assert counts[0]==1 and min(w for w in counts if w)==n//2+1
    weights=np.arange(1,n+1); heights=np.array([counts.get(int(w),0) for w in weights])
    assert int(heights.sum())==2**n//k-1
    ax.axvspan(.5,n//2+.5,color='.93',zorder=0)
    ax.axvline(n//2+.5,color='.45',lw=.6,ls='--')
    ax.bar(weights,heights,color='#476b7a',width=.75,zorder=3)
    ax.set(xlim=(.5,17.7),xticks=[1,4,7,10,13,16],xlabel=r'Pauli weight $w$')
    ax.set_title(rf'$N={n},\ K={k}$',loc='left',fontsize=8)
    ax.grid(axis='y',color='#d9d8d4',lw=.4,zorder=0)
    ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Number of nonidentity terms')
fig.tight_layout(pad=.4,w_pad=.6)
fig.savefig(OUT/'pauli_weights.pdf',metadata={'CreationDate':None});plt.close(fig)

# Exact checks for the data shown in the manuscript's two TikZ schematics.
rank=read('results/rank_and_c15.json'); assert rank['status']=='PASS'
assert rank['C15_binary']['multiplicities']==[4,2,2]
assert rank['C15_binary']['signed_column_images']==[[4,1],[1,1],[2,1],[7,-1],[5,1],[0,1],[3,-1],[6,1]]
f=read('data/sym1_external_spec.json')['family_witness']
assert f['symmetry_generators'][0]['perm']==list(range(1,15))+[0]
assert f['isometry']['prime_slope']==5 and pow(5,3,31)==1 and 5!=1
assert [(31+2)//3,(31-1)//3,(31-1)//3]==[11,10,10]
assert any(v['rank_upper_bound']==8 and v['contradiction']=='-3328/492545' for v in rank['general_rank_certificates'])
assert certs['13_16']['K']==16 and support['cells']['13_34']['p']==17
summary={'status':'PASS','matplotlib':matplotlib.__version__,
         'support':{'cells':104,'zero_cells':7,'distinct_intensities':50,'mean_R':float(r.mean())},
         'weight_totals':[511,4095,2047], 'C15_multiplicities':[[4,2,2],[11,10,10]],
         'rank_diagram':{'lower_bound':9,'known_stabilizer_rank':16,'capacities':[5,13,17]},
         'pdf_sha256':{name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in ['support.pdf','pauli_weights.pdf']}}
(OUT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
print('[PASS] exact plot values, zero mask, normalization, weight counts and TikZ diagram values')
