#!/usr/bin/env python3
"""最终版：萘环生物等排替换设计——两个原型 + 12个设计分子，结构图+性质表+JSON"""
import json
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors, QED, inchi
from rdkit.Chem import Draw

# ===== 原型（PubChem权威SMILES，2026-09-22核验）=====
PROTO = {
    'naproxen': {
        'label': 'Naproxen 萘普生\nNSAID · C14H14O3 · MW 230.26\n(FDA处方药1976年起，OTC 1994)',
        'smiles': 'C[C@@H](C1=CC2=C(C=C1)C=C(C=C2)OC)C(=O)O',
    },
    'agomelatine': {
        'label': 'Agomelatine 阿戈美拉汀\nMT1/MT2激动剂 · C15H17NO2 · MW 243.30\n(EMA 2009)',
        'smiles': 'CC(=O)NCCC1=CC=CC2=C1C=C(C=C2)OC',
    },
}

NPX = [
    ('NPX-01 吲哚', 'COc1ccc2[nH]cc(C(C)C(=O)O)c2c1', '萘→吲哚',
     '引入NH氢键给体；同系先例：依托度酸（吲哚乙酸类NSAID，FDA 1991）证明吲哚骨架在NSAID中成药'),
    ('NPX-02 苯并噻吩', 'COc1ccc2sc(C(C)C(=O)O)cc2c1', '萘→苯并噻吩',
     'S增强π极化、改变代谢软点；先例：雷洛昔芬（苯并噻吩核心，FDA 1997）'),
    ('NPX-03 苯并呋喃', 'COc1ccc2oc(C(C)C(=O)O)cc2c1', '萘→苯并呋喃',
     'O降低logP约0.4；先例：胺碘酮/达沙替尼（苯并呋喃核心）'),
    ('NPX-04 喹啉', 'COc1ccc2ncccc2c1C(C)C(=O)O', '萘→喹啉',
     '环内N使logP降0.6、改善水溶性；先例：众多喹啉类抗炎/激酶药物'),
    ('NPX-05 吲唑', 'COc1ccc2[nH]nc(C(C)C(=O)O)c2c1', '萘→吲唑',
     '双N杂环偶极强、logP降1.3最多；文献报道吲唑替换萘常提升代谢稳定性'),
    ('NPX-06 联苯', 'COc1ccc(-c2ccccc2)cc1C(C)C(=O)O', '萘→联苯',
     '骨架简化；二面角可旋转，选择性可通过邻位取代微调（沙坦类联苯先例）'),
    ('NPX-07 二氢苯并呋喃', 'COc1ccc2OCC(C(C)C(=O)O)c2c1', '萘→2,3-二氢苯并呋喃',
     'sp3引入打破平面性（Fsp3 0.21→0.42），降低平面芳烃的CYP抑制/hERG风险'),
]

AGO = [
    ('AGO-01 吲哚', 'CC(=O)NCCC1=CNC2=C1C=C(OC)C=C2', '萘→吲哚',
     '褪黑素本身是吲哚胺（5-甲氧基吲哚骨架）！此替换让药物回到内源配体拓扑，MT受体识别口袋天然适配（需实验验证）'),
    ('AGO-02 苯并呋喃', 'CC(=O)NCCC1=COC2=C1C=C(OC)C=C2', '萘→苯并呋喃',
     '与吲哚等构但无NH；若AGO-01的NH引起脱靶（如α2受体）可用此替代'),
    ('AGO-03 苯并噻吩', 'CC(=O)NCCC1=CSC2=C1C=C(OC)C=C2', '萘→苯并噻吩',
     'logP略升（+0.06），探索脂溶性对脑穿透的影响；苯并噻吩在CNS药物中常见（如齐拉西酮）'),
    ('AGO-04 喹啉', 'CC(=O)NCCC1=NC2=CC=C(OC)C=C2C=C1', '萘→喹啉',
     '环内N改变pKa分布与水溶性；喹啉氮可作为hinge binder，探索MT口袋外相互作用'),
    ('AGO-05 二氢苯并呋喃', 'CC(=O)NCCC1=CC(OC)=CC=C2OCCC12', '萘→2,3-二氢苯并呋喃',
     '打破平面性探索亚型选择性；Fsp3升到0.53，降低平面芳烃毒性风险'),
]


def calc(mol):
    return {'MW': Descriptors.MolWt(mol), 'cLogP': Crippen.MolLogP(mol),
            'TPSA': rdMolDescriptors.CalcTPSA(mol), 'HBD': Lipinski.NumHDonors(mol),
            'HBA': Lipinski.NumHAcceptors(mol), 'RotB': Lipinski.NumRotatableBonds(mol),
            'QED': round(QED.qed(mol), 3),
            'InChIKey': inchi.MolToInchiKey(mol)}


results = {}
print('=' * 105)
print('【原型A】萘普生萘环替换（7个设计）')
print('=' * 105)
mnap = Chem.MolFromSmiles(PROTO['naproxen']['smiles'])
b = calc(mnap)
results['naproxen_proto'] = {'smiles': PROTO['naproxen']['smiles'], **b}
print('%-22s MW=%-6.1f logP=%-5.2f TPSA=%-5.1f HBD=%d HBA=%d QED=%.3f' % ('Naproxen(原型)', b['MW'], b['cLogP'], b['TPSA'], b['HBD'], b['HBA'], b['QED']))
np_mols, np_names = [mnap], ['Naproxen\n(原型)']
for name, smi, strat, basis in NPX:
    mm = Chem.MolFromSmiles(smi)
    if mm is None:
        print(name, 'INVALID!')
        continue
    d = calc(mm)
    results[name] = {'smiles': smi, 'strategy': strat, 'basis': basis, **d}
    print('%-22s MW=%-6.1f logP=%-5.2f TPSA=%-5.1f HBD=%d HBA=%d QED=%.3f ΔlogP=%+.2f' % (
        name, d['MW'], d['cLogP'], d['TPSA'], d['HBD'], d['HBA'], d['QED'], d['cLogP'] - b['cLogP']))
    np_mols.append(mm)
    np_names.append(name.split(' ')[0] + '\n' + name.split(' ', 1)[1].replace('→', '→'))

print()
print('=' * 105)
print('【原型B】阿戈美拉汀萘环替换（5个设计）')
print('=' * 105)
mago = Chem.MolFromSmiles(PROTO['agomelatine']['smiles'])
b2 = calc(mago)
results['agomelatine_proto'] = {'smiles': PROTO['agomelatine']['smiles'], **b2}
print('%-22s MW=%-6.1f logP=%-5.2f TPSA=%-5.1f HBD=%d HBA=%d QED=%.3f' % ('Agomelatine(原型)', b2['MW'], b2['cLogP'], b2['TPSA'], b2['HBD'], b2['HBA'], b2['QED']))
ag_mols, ag_names = [mago], ['Agomelatine\n(原型)']
for name, smi, strat, basis in AGO:
    mm = Chem.MolFromSmiles(smi)
    if mm is None:
        print(name, 'INVALID!')
        continue
    d = calc(mm)
    results[name] = {'smiles': smi, 'strategy': strat, 'basis': basis, **d}
    print('%-22s MW=%-6.1f logP=%-5.2f TPSA=%-5.1f HBD=%d HBA=%d QED=%.3f ΔlogP=%+.2f' % (
        name, d['MW'], d['cLogP'], d['TPSA'], d['HBD'], d['HBA'], d['QED'], d['cLogP'] - b2['cLogP']))
    ag_mols.append(mm)
    ag_names.append(name.split(' ')[0] + '\n' + name.split(' ', 1)[1])

# ===== 渲染最终图 =====
print()
print('渲染最终结构图...')
img1 = Draw.MolsToGridImage(np_mols, molsPerRow=4, subImgSize=(400, 340), legends=np_names, returnPNG=False)
img1.save('/Users/pilot/萘环替换设计_萘普生系列.png') if hasattr(img1, 'save') else open('/Users/pilot/萘环替换设计_萘普生系列.png', 'wb').write(img1)
img2 = Draw.MolsToGridImage(ag_mols, molsPerRow=3, subImgSize=(430, 350), legends=ag_names, returnPNG=False)
img2.save('/Users/pilot/萘环替换设计_阿戈美拉汀系列.png') if hasattr(img2, 'save') else open('/Users/pilot/萘环替换设计_阿戈美拉汀系列.png', 'wb').write(img2)
print('  ~/萘环替换设计_萘普生系列.png (8个结构)')
print('  ~/萘环替换设计_阿戈美拉汀系列.png (6个结构)')

with open('/tmp/final_designs.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print('数据 /tmp/final_designs.json')
