#!/usr/bin/env python3
"""
萘环生物等排替换设计 v2（RDKit 验证 + 理化性质 + 结构图输出）
两个原型：萘普生（NSAID）、阿戈美拉汀（褪黑素受体激动剂）
所有设计分子为本研究提出的 in-silico 设计，尚未经实验验证。
"""
import json
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors, QED
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import Draw

# ============ 原型药物 ============
PROTO = {
    'naproxen': {
        'label': '萘普生 Naproxen\n(NSAID, 处方药1976起)',
        'smiles': 'COc1ccc2cc(ccc2c1)C(C)C(=O)O',
        'note': '6-甲氧基-2-萘丙酸；萘环=疏水锚',
    },
    'agomelatine': {
        'label': '阿戈美拉汀 Agomelatine\n(EMA 2009)',
        'smiles': 'COc1ccc2cc(ccc2c1)CCNC(=O)CCCN(C)C',
        'note': '萘环直接嵌在侧链上；褪黑素MT1/MT2激动',
    },
}

# ============ 设计分子（全部为本研究提出，标注替换策略） ============
DESIGNS_NPX = [
    ('NPX-01 吲哚', 'COc1ccc2[nH]cc(C(C)C(=O)O)c2c1',
     '萘→吲哚', '引入NH氢键给体；同系先例：吲哚美辛/依托度酸（吲哚乙酸类NSAID）证明该骨架在NSAID中成药'),
    ('NPX-02 苯并噻吩', 'COc1ccc2sc(C(C)C(=O)O)cc2c1',
     '萘→苯并噻吩', 'S原子增强π极化、改变代谢软点；先例：雷洛昔芬以苯并噻吩为核心骨架成药'),
    ('NPX-03 苯并呋喃', 'COc1ccc2oc(C(C)C(=O)O)cc2c1',
     '萘→苯并呋喃', 'O原子降低logP；先例：胺碘酮含苯并呋喃核心'),
    ('NPX-04 喹啉', 'COc1ccc2ncccc2c1C(C)C(=O)O',
     '萘→喹啉', '环内N使logP降约0.5-1，改善水溶性'),
    ('NPX-05 吲唑', 'COc1ccc2[nH]nc(C(C)C(=O)O)c2c1',
     '萘→吲唑', '双N杂环，偶极强；文献常报道吲唑替换萘提升代谢稳定性'),
    ('NPX-06 联苯', 'COc1ccc(-c2ccccc2)cc1C(C)C(=O)O',
     '萘→联苯', '骨架简化，二面角可调优化选择性'),
    ('NPX-07 二氢苯并呋喃', 'COc1ccc2OCC(C(C)C(=O)O)c2c1',
     '萘→2,3-二氢苯并呋喃', 'sp3引入打破平面性，降低平面芳烃的CYP抑制/hERG风险（Fsp3↑）'),
]

DESIGNS_AGO = [
    ('AGO-01 吲哚', 'COc1ccc2[nH]cc(CCNC(=O)CCCN(C)C)c2c1',
     '萘→吲哚', '褪黑素本身是吲哚胺！吲哚替换萘让分子回到内源配体拓扑，理论上亲和谱更接近MT1/MT2'),
    ('AGO-02 苯并呋喃', 'COc1ccc2oc(CCNC(=O)CCCN(C)C)cc2c1',
     '萘→苯并呋喃', '与吲哚等构但无NH，若NH引起α2拮抗副作用可用此替代（需实验验证）'),
    ('AGO-03 2-萘基→2,3-二氢苯并呋喃', 'COc1ccc2OCC(CCNC(=O)CCCN(C)C)c2c1',
     '萘→2,3-二氢苯并呋喃', '打破平面性，探索对受体亚型选择性的影响'),
]


def calc(m):
    return {
        'MW': Descriptors.MolWt(m),
        'cLogP': Crippen.MolLogP(m),
        'TPSA': rdMolDescriptors.CalcTPSA(m),
        'HBD': Lipinski.NumHDonors(m),
        'HBA': Lipinski.NumHAcceptors(m),
        'RotB': Lipinski.NumRotatableBonds(m),
        'QED': round(QED.qed(m), 3),
        'AromRings': rdMolDescriptors.CalcNumAromaticRings(m),
        'Fsp3': round(rdMolDescriptors.CalcFractionCSP3(m), 3),
        'LipinskiViolations': sum([Descriptors.MolWt(m) > 500, Crippen.MolLogP(m) > 5,
                                   Lipinski.NumHDonors(m) > 5, Lipinski.NumHAcceptors(m) > 10]),
    }


def row(name, d, base=None):
    dl = ('ΔlogP=%+.2f' % (d['cLogP'] - base['cLogP'])) if base else ''
    print('%-26s MW=%-6.1f logP=%-5.2f TPSA=%-5.1f HBD=%d HBA=%d RotB=%d QED=%.3f Fsp3=%.2f %s' % (
        name, d['MW'], d['cLogP'], d['TPSA'], d['HBD'], d['HBA'], d['RotB'], d['QED'], d['Fsp3'], dl))


all_results = {'naproxen': {}, 'agomelatine': {}}
proto_mols = {}
for key, p in PROTO.items():
    m = Chem.MolFromSmiles(p['smiles'])
    assert m is not None, key
    proto_mols[key] = m
    all_results[key]['_proto'] = calc(m)

print('=' * 110)
print('【原型A】萘普生及其萘环替换设计（7个）')
print('=' * 110)
base = all_results['naproxen']['_proto']
row('萘普生(原型)', base)
for name, smi, strat, basis in DESIGNS_NPX:
    m = Chem.MolFromSmiles(smi)
    if m is None:
        print('%-26s INVALID!' % name)
        continue
    d = calc(m)
    all_results['naproxen'][name] = {'smiles': smi, 'strategy': strat, 'basis': basis, **d}
    row(name, d, base)

print()
print('=' * 110)
print('【原型B】阿戈美拉汀及其萘环替换设计（3个）')
print('=' * 110)
base_b = all_results['agomelatine']['_proto']
row('阿戈美拉汀(原型)', base_b)
for name, smi, strat, basis in DESIGNS_AGO:
    m = Chem.MolFromSmiles(smi)
    if m is None:
        print('%-26s INVALID!' % name)
        continue
    d = calc(m)
    all_results['agomelatine'][name] = {'smiles': smi, 'strategy': strat, 'basis': basis, **d}
    row(name, d, base_b)

# ============ 结构图：两个原型 + 全部设计，一行一原型 ============
print()
print('渲染结构图...')
rows_spec = []
for key, designs in [('naproxen', DESIGNS_NPX), ('agomelatine', DESIGNS_AGO)]:
    m0 = proto_mols[key]
    valid = [(n, s) for n, s, _, _ in designs if Chem.MolFromSmiles(s) is not None]
    mols = [m0] + [Chem.MolFromSmiles(s) for _, s in valid]
    legends = [PROTO[key]['label']] + ['%s\n%s' % (n.split(' ')[0], n.split(' ', 1)[1]) for n, _ in valid]
    ncol = max(len(mols), 8)
    img = Draw.MolsToGridImage(mols, molsPerRow=ncol, subImgSize=(360, 330), legends=legends, returnPNG=False)
    outp = '/tmp/designs_%s.png' % key
    img.save(outp) if hasattr(img, 'save') else open(outp, 'wb').write(img)
    print('  图:', outp, '(%d分子)' % len(mols))
    rows_spec.append(outp)

with open('/tmp/design_results.json', 'w') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=1)
print('数据: /tmp/design_results.json')
