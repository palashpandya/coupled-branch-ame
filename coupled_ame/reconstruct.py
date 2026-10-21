"""Rebuild binary seeds and prime parents; compare all construction certificates."""
from ._paths import DATA, RESULTS
from coupled_ame import codes as c
from coupled_ame.construction import parent_graph, cuts, graph_form
from coupled_ame.circle13 import circle
import json

def read(name):return json.loads((DATA/name).read_text())
def canonical(obj):return json.loads(json.dumps(obj))
binary=read('o3_binary_certificates.json')
poly=binary['cyclic15_polynomial']
# Reconstruct six length-15 shifts of the published polynomial.
g15=[([0]*i+poly+[0]*15)[:15] for i in range(6)]
assert g15==binary['cyclic15_gf4_generator']
s15=c.gf4_binary(g15)
s13=c.basis(c.pack(c.unpack(w,15)[2:]) for w in c.span(s15)
            if c.unpack(w,15)[0]==0 and c.unpack(w,15)[1] in (0,1))
qc=[[2,0,0,1,0,1],[0,1,2,2,2,2],[3,3,1,1,1,1]]
g18=[sum((a[-s:]+a[:-s] if s else a for a in qc),[]) for s in range(6)]
assert g18==binary['quasicyclic18_gf4_generator']
s18=c.gf4_binary(g18)
s17=c.basis(c.pack(c.unpack(w,18)[:-1]) for w in c.span(s18) if c.unpack(w,18)[-1] in (0,1))
for key,s in [('13_16',s13),('15_8',s15),('17_64',s17)]:
    n=int(key.split('_')[0]); assert canonical(c.certify(s,n))==binary['ingredients'][key]
    print('[PASS] seed/restriction',key)
A,provenance=circle(); circle_cert=read('o3_circle13_certificate.json')
assert A==circle_cert['prime_parent_graph'] and canonical(provenance)==circle_cert['provenance']
spec=read('o3_external_spec.json')['constructions']; certs=read('o3_construction_certificates.json');out={}
for key,state in spec.items():
    n,p=state['N'],state['p']
    parent=A if key=='15_26' else parent_graph(n+1,p)
    assert parent==state['prime_parent_graph']
    cutcert=canonical(cuts(parent,p));assert cutcert==certs[key]['prime_parent']
    if key=='15_26': assert cutcert==circle_cert['cut_certificate']
    out[key]=cutcert
    print('[PASS] reconstructed parent and cut certificate',key,cutcert['all_balanced_cuts'])
(RESULTS/'reconstruction.json').write_text(json.dumps(out,indent=2)+'\n')
