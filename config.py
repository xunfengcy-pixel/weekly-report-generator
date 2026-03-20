# -*- coding: utf-8 -*-
"""
配置文件 - 负责人照片URL和其他常量
"""

# 负责人照片URL映射
AVATAR_URLS = {
    'bard': 'https://s41.ax1x.com/2026/03/20/pem5Du8.jpg',
    'chonya': 'https://s41.ax1x.com/2026/03/20/pem5rDS.jpg',
    'kevin': 'https://s41.ax1x.com/2026/03/20/pem5wgP.jpg',
    'mark': 'https://s41.ax1x.com/2026/03/20/pem50jf.jpg',
    'melanie': 'https://s41.ax1x.com/2026/03/20/pem5d3t.jpg',
    'qimeng': 'https://s41.ax1x.com/2026/03/20/pem5sHg.jpg',
    'spencer': 'https://s41.ax1x.com/2026/03/20/pem56EQ.jpg'
}

# 负责人列表（用于下拉选择）
OWNERS = ['bard', 'chonya', 'kevin', 'mark', 'melanie', 'qimeng', 'spencer']

# 板块配置
SECTIONS = [
    {'id': 'labor', 'number': '01', 'title': '劳动纠纷'},
    {'id': 'infrastructure', 'number': '02', 'title': '基建纠纷'},
    {'id': 'non_compete', 'number': '03', 'title': '竞业限制'},
    {'id': 'other', 'number': '04', 'title': '其他事项'}
]

# 默认作者信息
DEFAULT_AUTHOR = {
    'name': 'Dylan Bai (白杰)',
    'title': '腾讯公司 法务综合部 综合诉讼维权中心'
}

# 默认Notice文本
DEFAULT_NOTICE = '本邮件(包括附件及其批注)可能涉及公司秘密,未经相关人同意请勿直接对外转发、原文复制摘录对外传播或采取其他方式对外分享。感谢!'

# 状态标签选项
STATUS_OPTIONS = ['新收案件', '新结案件', '新收裁判', '本周开庭']
NON_COMPETE_STATUS_OPTIONS = ['新收案件', '新结案件', '新收裁判', '本周开庭', '主诉', '保护']

# 默认文档链接配置
DEFAULT_DOC_LINKS = {
    'labor': [
        {'name': '海外劳动纠纷整体详情', 'url': 'https://doc.weixin.qq.com/doc/w3_AUEACAb8ADwCNkmv9OBoiTDewsoK0?scode=AJEAIQdfAAoRSMMVQIALAA4QZ6ACc'}
    ],
    'infrastructure': [
        {'name': '综合诉讼-基建争议汇总表3月更新', 'url': 'https://doc.weixin.qq.com/sheet/e3_AIAAQgZcACojZU0AYcCQJu5FvGPbe?scode=AJEAIQdfAAoK2pdsV7AIAAQgZcACo'},
        {'name': '基建重点案件情况梳理', 'url': 'https://doc.weixin.qq.com/sheet/e3_AIAAQgZcACojZU0AYcCQJu5FvGPbe?scode=AJEAIQdfAAoK2pdsV7AIAAQgZcACo'}
    ],
    'non_compete': [
        {'name': '竞业主诉与调查概况', 'url': 'https://doc.weixin.qq.com/sheet/e3_AL4AgAaBACcdYDyiu5FQ3Gcy28GlW?scode=AJEAIQdfAAoHdoFEvUAMUA5waQACc&tab=BB08J2'}
    ],
    'other': []
}

# 竞业限制BG列表
BG_LIST = ['TEG', 'CDG', 'IEG', 'CSIG', 'WXG', 'S1']
