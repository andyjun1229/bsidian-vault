#!/usr/bin/env python3
"""分析流程图 v2：修正文字溢出/重叠/裁切"""
import matplotlib
matplotlib.use('Agg')
from matplotlib import font_manager
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

zh = None
for f in ['Hiragino Sans GB', 'PingFang SC', 'STHeiti', 'Arial Unicode MS']:
    if any(f.lower() in x.name.lower() for x in font_manager.fontManager.ttflist):
        zh = f
        break
plt.rcParams['font.family'] = [zh or 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(19, 12.5), dpi=150)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

C_STEP = '#0F172A'
C_OUT = '#FFFFFF'
C_ACC = '#38BDF8'
C_WARN = '#FDE68A'
C_EDGE = '#334155'


def box(x, y, w, h, text, fc=C_STEP, tc='white', fs=11.5, bold=False):
    b = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.5,rounding_size=1.0',
                       fc=fc, ec=C_EDGE, lw=1.3)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs,
            color=tc, fontweight='bold' if bold else 'normal', linespacing=1.45)


def arrow(x, y1, y2, color=C_ACC, ls='-'):
    ax.add_patch(FancyArrowPatch((x, y1), (x, y2), arrowstyle='-|>',
                                 mutation_scale=24, color=color, lw=2.4, linestyle=ls))


ax.text(46, 97.2, '萘环骨架生物等排替换 —— 完整分析流程', ha='center',
        fontsize=22, fontweight='bold', color='#0F172A')
ax.text(46, 93.6, '近30年FDA批准药物 → 骨架识别 → 等排设计 → 计算验证 → 实验迭代    2026-09-22',
        ha='center', fontsize=12, color='#64748B')

steps = [
    ('① 数据采集', 'openFDA 检索近30年批准药物\n筛选含萘环骨架的药物家族'),
    ('② 结构核验', 'PubChem 权威SMILES\nRDKit解析+分子式比对'),
    ('③ 骨架分析', '识别萘环与连接位点\n药效团：疏水锚+极性头'),
    ('④ 等排设计', '6类生物等排体逐一替换\n生成12个设计分子SMILES'),
    ('⑤ 计算验证', 'RDKit合法性+理化性质\nMW/logP/TPSA/QED/Fsp3'),
    ('⑥ 定性推导', '活性·选择性·代谢·毒性\n四维评估+先例证据链'),
    ('⑦ 实验建议', '结合assay/微粒体稳定性\nCYP抑制/hERG湿验清单'),
    ('⑧ SAR迭代', '实验数据反馈\n进入第2轮替换周期'),
]
outs = [
    '候选原型药清单\n萘普生/阿戈美拉汀/西那卡塞\n贝沙罗汀/阿达帕林/他扎罗汀',
    '可信原型分子库\n核验12个全PASS\n纠错1例(阿戈美拉汀侧链)',
    '替换位点图谱\n萘环=疏水锚定基团\n侧链连接位固定不动',
    '12个设计分子\n每个附替换策略\n与先例药物证据',
    '性质对比表\n每分子vs原型ΔlogP\nInChIKey标准标识',
    '优先级排序\nAGO-01回吲哚胺拓扑\nNPX-05 logP降1.3',
    'wet-lab验证清单\n先结合assay+微粒体\n过关再进细胞动物',
    '第2轮设计\n缩小窗口聚焦优势骨架\n直至候选化合物',
]

y_top, box_h, gap = 89.5, 7.6, 1.9
ys = []
for i, (t, d) in enumerate(steps):
    y = y_top - i * (box_h + gap) - box_h
    ys.append(y)
    box(2.5, y, 27, box_h, '【%s】\n%s' % (t, d), fc=C_STEP, tc='white', fs=11.8)
    box(34.5, y, 27, box_h, outs[i], fc=C_OUT, tc='#0F172A', fs=11.2)
    ax.add_patch(FancyArrowPatch((29.9, y + box_h / 2), (34.1, y + box_h / 2),
                                 arrowstyle='-|>', mutation_scale=18, color=C_ACC, lw=2))
    if i < len(steps) - 1:
        arrow(16, y - 0.3, y - gap + 0.3)

# 右侧原则栏：留足内边距，文字缩小
box(66, 18, 31.5, 71, '', fc='#F1F5F9')
ax.text(81.75, 86.2, '执行原则与数据源', ha='center', fontsize=14, fontweight='bold', color='#0F172A')
principles = (
    '数据源（全部一手核验）\n'
    '  openFDA drugsfda API\n'
    '  PubChem REST 权威SMILES\n'
    '  RDKit 2025.09.3\n'
    '  Europe PMC / Crossref\n\n'
    '硬性规则\n'
    '  原型结构必须权威源核对\n'
    '  (本次纠错1例凭记忆写错)\n'
    '  设计分子必算InChIKey\n'
    '  每步输出可追溯可复核\n\n'
    '诚实声明\n'
    '  所有设计分子为in-silico提案\n'
    '  未经任何实验验证\n'
    '  「活性/选择性改善」为基于\n'
    '  先例的定性推导而非结论\n\n'
    '优先级建议(第一轮)\n'
    '  1. AGO-01 吲哚(内源拓扑)\n'
    '  2. NPX-05 吲唑(代谢稳定)\n'
    '  3. NPX-07 二氢苯并呋喃\n'
    '     (降平面毒性风险)'
)
ax.text(81.75, 50.5, principles, ha='center', va='center', fontsize=10.8,
        color='#334155', linespacing=1.55)

# 底部 SAR 循环箭头 ⑧ -> ④
ax.add_patch(FancyArrowPatch((31.5, ys[7] + box_h * 0.3), (31.5, ys[3] + box_h * 0.7),
                             arrowstyle='-|>', mutation_scale=22, color='#D97706',
                             lw=2.3, linestyle='--', connectionstyle='arc3,rad=-0.62'))
ax.text(36.5, 13.5, 'SAR 迭代循环：第⑧步实验数据回流至第④步', fontsize=11, color='#B45309', fontweight='bold')

out = '/Users/pilot/萘环替换分析流程图.png'
fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='#FAFAFA')
print('OK', out)
