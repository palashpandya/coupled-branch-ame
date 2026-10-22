"""Replay all N04 graphs, Hermitian parents and assembled q9 cells."""
import copy, json
from ._paths import DATA, RESULTS
from .finite_field import field
from .field_parents import verify_parent
from .field_cells import check
D=DATA/'prime_powers'
def read(name):return json.loads((D/(name+'.json')).read_text())
def main():
 out={}
 for q in [3,4,5,7,8,9]:
  a=read(f'graph_9_{q}');out[f'graph_9_{q}']=field(q).cuts(a.get('matrix',a.get('graph')))
 for n in [10,12,16]:
  a=read(f'parent_{n}_9')
  if n>10:assert json.loads(json.dumps(verify_parent(a['B'])))==a
  out[f'parent_{n}_9']=field(9).cuts(a['graph'])
 f=field(81);s=read('parent_16_9_source')
 assert [[f.pow(3,e) for e in row] for row in s['exponents']]==read('parent_16_9')['B']
 for n in [9,11,15]:
  a=read(f'ame_{n}_18');assert a['q']==9 and a['field_polynomial']==[1,0,1]
  out[f'ame_{n}_18']=check(a)
  for label in ['binary_labels','field_labels']:
   b=copy.deepcopy(a);b[label][1]=b[label][0]
   try:check(b)
   except AssertionError:pass
   else:raise AssertionError('duplicate accepted')
 for q in [3,4,9]:
  try:field(q).cuts([[0]*9 for _ in range(9)])
  except AssertionError:pass
  else:raise AssertionError('zero graph accepted')
 out['negative_controls']='duplicate binary/field labels per cell and zero graphs rejected'
 (RESULTS/'prime_powers.json').write_text(json.dumps(out,indent=2)+'\n')
 print('[PASS] six graphs, three parents, three assembled cells; negative controls')
if __name__=='__main__':main()
