# -*- coding: utf-8 -*-
"""
Streamlit应用 - 综合诉讼维权中心周报生成器
"""
import streamlit as st
import streamlit.components.v1 as components
import json
import re
import os
import webbrowser
import tempfile
from datetime import datetime, timedelta
from config import AVATAR_URLS, OWNERS, SECTIONS, DEFAULT_AUTHOR, DEFAULT_NOTICE, STATUS_OPTIONS, NON_COMPETE_STATUS_OPTIONS

# 自动保存文件路径
AUTO_SAVE_FILE = 'weekly_report_autosave.json'

def load_autosave():
    """从文件加载自动保存的数据"""
    if os.path.exists(AUTO_SAVE_FILE):
        try:
            with open(AUTO_SAVE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"加载自动保存数据失败: {e}")
    return None

def save_autosave(data):
    """保存数据到文件"""
    try:
        with open(AUTO_SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"自动保存失败: {e}")
        return False

# 页面配置
st.set_page_config(
    page_title="周报生成器",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式 - 现代化UI设计
st.markdown("""
<style>
    /* 全局字体和颜色 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    }
    
    /* 主标题 - 渐变效果 */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    /* 区块标题 - 毛玻璃效果 */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding: 0.75rem 1rem;
        background: rgba(99, 102, 241, 0.08);
        border-radius: 12px;
        border-left: 4px solid #6366f1;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .section-header:hover {
        background: rgba(99, 102, 241, 0.12);
        transform: translateX(4px);
    }
    
    /* 案件容器 - 卡片效果 */
    .case-container {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .case-container:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    /* 主按钮 - 渐变背景 */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.625rem 1.25rem;
        border: none;
        box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* 次要按钮 */
    .stButton>button[kind="secondary"] {
        background: #f1f5f9;
        color: #64748b;
        box-shadow: none;
    }
    
    .stButton>button[kind="secondary"]:hover {
        background: #e2e8f0;
        color: #475569;
    }
    
    /* 下载按钮 */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.625rem 1.25rem;
        border: none;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
    }
    
    /* 输入框美化 */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        padding: 0.75rem 1rem;
        background: #fafafa;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #6366f1;
        background: #ffffff;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* 数字输入框 */
    .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        background: #fafafa;
    }
    
    /* 多选框美化 */
    .stMultiSelect>div>div {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        background: #fafafa;
    }
    
    /* 折叠面板美化 */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        font-weight: 500;
        color: #475569;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        color: #1e293b;
    }
    
    /* 标签页美化 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8fafc;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        color: #64748b;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }
    
    /* 侧边栏美化 */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* 信息框美化 */
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
    }
    
    /* 成功提示 */
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-radius: 12px;
        border-left: 4px solid #10b981;
    }
    
    /* 警告提示 */
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
    }
    
    /* 分割线美化 */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }
    
    /* 日期选择器 */
    .stDateInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        background: #fafafa;
    }
    
    /* 开关按钮 */
    .stCheckbox>div>div>div {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)


def get_week_range(start_date_str, end_date_str):
    """根据起始和截止日期获取周报日期范围显示"""
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        # 简写格式：03.17-03.23
        short_range = start_date.strftime("%m.%d") + "-" + end_date.strftime("%m.%d")
        # 完整格式：2026年03月17日 – 03月23日
        full_range = start_date.strftime("%Y年%m月%d日") + " – " + end_date.strftime("%m月%d日")
        return short_range, full_range
    except:
        return "", ""


def generate_avatar_html(owners_str):
    """生成负责人头像HTML"""
    if not owners_str:
        return ""
    
    owners = [o.strip() for o in owners_str.split('、') if o.strip()]
    html_parts = []
    
    for owner in owners:
        if owner in AVATAR_URLS:
            html_parts.append(
                f'<span class="owner-name"><img src="{AVATAR_URLS[owner]}" class="avatar" alt="{owner}">{owner}</span>'
            )
    
    return ''.join(html_parts)


def generate_case_card(case_data, section_id, case_index):
    """生成案件卡片HTML"""
    title = case_data.get('title', '')
    progress = case_data.get('progress', '')
    follow_up = case_data.get('follow_up', '')
    owners = case_data.get('owners', '')
    status = case_data.get('status', '')
    
    # 生成案件锚点ID
    case_id = f"case-{section_id}-{case_index+1}"
    
    # 判断第一个负责人是否是 mark
    owner_list = [o.strip().lower() for o in owners.split('、') if o.strip()]
    is_mark_first = len(owner_list) > 0 and owner_list[0] == 'mark'
    
    # 根据负责人设置小标题（只有第一个是mark时才应用）
    if is_mark_first:
        first_title = "基本背景"
        second_title = "案件进展"
    else:
        first_title = "案件进展"
        second_title = "后续安排"
    
    # 处理进展文本，将换行转换为<p>标签
    progress_html = ''
    if progress:
        lines = progress.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if line:
                # 检查是否是编号列表
                if re.match(r'^\d+\.', line):
                    progress_html += f'<p style="margin-bottom: 12px; padding-left: 16px;">{line}</p>'
                else:
                    progress_html += f'<p style="margin-bottom: 12px;">{line}</p>'
    
    avatar_html = generate_avatar_html(owners)
    
    # 处理多个状态标签
    status_badges = ''
    if status:
        # 支持多选，状态可能是列表或字符串
        if isinstance(status, list):
            status_list = status
        else:
            status_list = [s.strip() for s in status.split('、') if s.strip()]
        
        for s in status_list:
            if s:
                status_badges += f'<span class="badge badge-status" style="margin-right: 6px;">{s}</span>'
    
    return f'''
    <div class="case-card" id="{case_id}">
        <div class="case-header">
            <span class="case-title">⚖️ {title}</span>
            <span class="case-badges">
                {status_badges}
                <span class="badge badge-primary">
                    {avatar_html}
                </span>
            </span>
        </div>
        <div class="case-body">
            <div class="case-section">
                <div class="case-section-title">{first_title}</div>
                <div class="case-section-content">{progress_html}</div>
            </div>
            <div class="case-section">
                <div class="case-section-title">{second_title}</div>
                <div class="case-section-content">{follow_up}</div>
            </div>
        </div>
    </div>
'''


def generate_section_html(section_data, section_config):
    """生成板块HTML"""
    section_id = section_config['id']
    section_number = section_config['number']
    section_title = section_config['title']
    
    # 获取板块数据
    overview = section_data.get('overview', {})
    summary = section_data.get('summary', '')
    doc_links = section_data.get('doc_links', [])
    cases = section_data.get('cases', [])
    
    # 生成概览HTML
    overview_html = ''
    if overview:
        # 劳动纠纷板块：按指定顺序排列【在办案件】【活跃案件】【国内案件】【涉外案件】
        if section_id == 'labor':
            cells = []
            order = ['在办案件', '活跃案件', '国内案件', '涉外案件']
            for key in order:
                if key in overview:
                    value = overview[key]
                    cells.append(f'''
                        <td class="overview-cell">
                            <div class="overview-value">{value}</div>
                            <div class="overview-label">{key}</div>
                        </td>
                    ''')
            overview_html = f'''
            <div class="data-overview">
                <table class="overview-table">
                    <tr>{''.join(cells)}</tr>
                </table>
            </div>
            '''
        
        # 基建纠纷板块：主数据 + 案件类型分布
        elif section_id == 'infrastructure':
            # 主数据行
            main_keys = ['在办案件', '本周新增', '本周结案']
            main_cells = []
            for key in main_keys:
                if key in overview:
                    value = overview[key]
                    main_cells.append(f'''
                        <td class="overview-cell">
                            <div class="overview-value">{value}</div>
                            <div class="overview-label">{key}</div>
                        </td>
                    ''')
            
            # 案件类型分布
            type_keys = ['结算纠纷', '工伤案件', '劳务纠纷', '保险案件']
            type_cells = []
            for key in type_keys:
                if key in overview:
                    value = overview[key]
                    type_cells.append(f'''
                        <td class="breakdown-cell">
                            <div class="breakdown-value">{value}</div>
                            <div class="breakdown-label">{key}</div>
                        </td>
                    ''')
            
            overview_html = f'''
            <div class="data-overview">
                <table class="overview-table">
                    <tr>{''.join(main_cells)}</tr>
                </table>
                <div class="breakdown-box">
                    <div class="breakdown-header">案件类型分布</div>
                    <table class="breakdown-table">
                        <tr>{''.join(type_cells)}</tr>
                    </table>
                </div>
            </div>
            '''
        
        # 竞业限制板块：主指标 + 次要指标 + BG分布
        elif section_id == 'non_compete':
            # 主指标行
            main_keys = ['竞业期内人员', '在诉案件', '调查取证']
            main_cells = []
            for key in main_keys:
                if key in overview:
                    value = overview[key]
                    main_cells.append(f'''
                        <td class="overview-cell">
                            <div class="overview-value">{value}</div>
                            <div class="overview-label">{key}</div>
                        </td>
                    ''')
            
            # 次要指标行
            secondary_keys = ['新增主诉', '近期待诉', '被诉支持']
            secondary_cells = []
            for key in secondary_keys:
                if key in overview:
                    value = overview[key]
                    secondary_cells.append(f'''
                        <td class="nc-secondary-cell">
                            <div class="nc-secondary-value">{value}</div>
                            <div class="nc-secondary-label">{key}</div>
                        </td>
                    ''')
            
            # BG分布数据
            bg_list = ['TEG', 'CDG', 'IEG', 'CSIG', 'WXG', 'S1', 'PCG']
            
            # 在诉案件BG分布
            litigation_bg_cells = []
            for bg in bg_list:
                key = f'在诉_{bg}'
                if key in overview and overview[key] > 0:
                    litigation_bg_cells.append(f'''
                        <td class="bg-grid-cell"><span class="bg-grid-name">{bg}</span><span class="bg-grid-value">{overview[key]}</span></td>
                    ''')
            # 补齐表格（每行2个）
            litigation_bg_rows = []
            for i in range(0, len(litigation_bg_cells), 2):
                row_cells = litigation_bg_cells[i:i+2]
                while len(row_cells) < 2:
                    row_cells.append('<td class="bg-grid-cell"></td>')
                litigation_bg_rows.append(f'<tr>{"".join(row_cells)}</tr>')
            
            # 调查取证BG分布
            investigation_bg_cells = []
            for bg in bg_list:
                key = f'调查_{bg}'
                if key in overview and overview[key] > 0:
                    investigation_bg_cells.append(f'''
                        <td class="bg-grid-cell"><span class="bg-grid-name">{bg}</span><span class="bg-grid-value">{overview[key]}</span></td>
                    ''')
            investigation_bg_rows = []
            for i in range(0, len(investigation_bg_cells), 2):
                row_cells = investigation_bg_cells[i:i+2]
                while len(row_cells) < 2:
                    row_cells.append('<td class="bg-grid-cell"></td>')
                investigation_bg_rows.append(f'<tr>{"".join(row_cells)}</tr>')
            
            # 获取总数
            litigation_total = overview.get('在诉案件', 0)
            investigation_total = overview.get('调查取证', 0)
            
            overview_html = f'''
            <div class="data-overview">
                <table class="overview-table">
                    <tr>{''.join(main_cells)}</tr>
                </table>
                <table class="nc-secondary-table">
                    <tr>{''.join(secondary_cells)}</tr>
                </table>
            </div>
            <table class="bg-dist-table">
                <tr>
                    <td class="bg-dist-cell">
                        <div class="bg-dist-header">
                            <span class="bg-dist-title">在诉案件 BG 分布</span>
                            <span class="bg-dist-total">{litigation_total} 起</span>
                        </div>
                        <table class="bg-grid-table">
                            {''.join(litigation_bg_rows)}
                        </table>
                    </td>
                    <td class="bg-dist-cell">
                        <div class="bg-dist-header">
                            <span class="bg-dist-title">调查取证 BG 分布</span>
                            <span class="bg-dist-total">{investigation_total} 起</span>
                        </div>
                        <table class="bg-grid-table">
                            {''.join(investigation_bg_rows)}
                        </table>
                    </td>
                </tr>
            </table>
            '''
        
        else:
            # 其他板块保持原有顺序
            cells = []
            for key, value in overview.items():
                cells.append(f'''
                    <td class="overview-cell">
                        <div class="overview-value">{value}</div>
                        <div class="overview-label">{key}</div>
                    </td>
                ''')
            overview_html = f'''
            <div class="data-overview">
                <table class="overview-table">
                    <tr>{''.join(cells)}</tr>
                </table>
            </div>
            '''
    
    # 生成摘要HTML - 处理重点案件列表
    summary_html = ''
    highlight_cases = section_data.get('highlight_cases', [])
    
    if highlight_cases:
        formatted_lines = []
        for case in highlight_cases:
            case_name = case.get('name', '').strip()
            case_progress = case.get('progress', '').strip()
            
            if not case_name and not case_progress:
                continue
            
            # 对案件名称进行模糊匹配，添加跳转链接
            linked_name = case_name
            if case_name and cases:
                for i, c in enumerate(cases):
                    case_title = c.get('title', '')
                    if not case_title:
                        continue
                    
                    case_id = f"case-{section_id}-{i+1}"
                    if f'href="#{case_id}"' in linked_name:
                        continue
                    
                    # 1. 精确匹配
                    if case_title == case_name or case_title in case_name:
                        linked_name = linked_name.replace(
                            case_title,
                            f'<a href="#{case_id}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{case_title}</a>'
                        )
                        break
                    
                    # 2. 清理后的标题匹配
                    clean_title = re.sub(r'^[【\[]*.*?[】\]]*[\s]*[⚖️]*\s*', '', case_title)
                    if len(clean_title) > 5 and clean_title in case_name:
                        linked_name = linked_name.replace(
                            clean_title,
                            f'<a href="#{case_id}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{clean_title}</a>'
                        )
                        break
                    
                    # 3. 关键词匹配：提取核心关键词（去除无意义词汇后进行匹配）
                    # 清理输入的案件名称和案件列表中的名称
                    def extract_keywords(text):
                        # 去除标点、空格、常见无意义词汇
                        text = re.sub(r'[【\]()（）\[\]\s⚖️、，。！？,.!?]', '', text)
                        # 去除常见后缀
                        text = re.sub(r'(案|案件|纠纷|争议|诉讼|仲裁|一审|二审|再审|执行)$', '', text)
                        # 去除常见前缀
                        text = re.sub(r'^(关于|涉及|有关)', '', text)
                        return text
                    
                    input_keywords = extract_keywords(case_name)
                    title_keywords = extract_keywords(case_title)
                    
                    # 如果清理后的关键词长度大于4，进行相互包含检查
                    if len(input_keywords) >= 4 and len(title_keywords) >= 4:
                        # 检查输入是否包含标题的核心部分（至少4个连续字符）
                        match_found = False
                        min_match_len = min(8, len(title_keywords))
                        for length in range(len(title_keywords), min_match_len - 1, -1):
                            for start in range(0, len(title_keywords) - length + 1):
                                substr = title_keywords[start:start + length]
                                if len(substr) >= 4 and substr in input_keywords:
                                    # 找到匹配，在原始输入中替换
                                    # 尝试在原始case_name中找到对应的文本
                                    for original_len in range(len(substr), min(len(case_name), 20) + 1):
                                        for original_start in range(0, len(case_name) - original_len + 1):
                                            original_substr = case_name[original_start:original_start + original_len]
                                            if extract_keywords(original_substr) == substr:
                                                linked_name = linked_name.replace(
                                                    original_substr,
                                                    f'<a href="#{case_id}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{original_substr}</a>'
                                                )
                                                match_found = True
                                                break
                                        if match_found:
                                            break
                                    break
                            if match_found:
                                break
                        if match_found:
                            break
                    
                    # 4. 部分匹配（前N个字符）
                    core_title = re.sub(r'[【\]()（）\[\]\s⚖️]', '', case_title)
                    if len(core_title) > 8:
                        match_len = min(15, len(core_title))
                        for length in range(match_len, 7, -1):
                            partial = core_title[:length]
                            if partial in case_name and len(partial) >= 8:
                                linked_name = linked_name.replace(
                                    partial,
                                    f'<a href="#{case_id}" style="color: #2563eb; text-decoration: none; font-weight: 500;">{partial}</a>'
                                )
                                break
                        if f'href="#{case_id}"' in linked_name:
                            break
            
            # 组合成一段
            if linked_name and case_progress:
                formatted_lines.append(f'<p style="margin-bottom: 12px;">• <strong>{linked_name}</strong>：{case_progress}</p>')
            elif linked_name:
                formatted_lines.append(f'<p style="margin-bottom: 12px;">• <strong>{linked_name}</strong></p>')
            elif case_progress:
                formatted_lines.append(f'<p style="margin-bottom: 12px;">• {case_progress}</p>')
        
        if formatted_lines:
            summary_html = f'<div class="summary-text">{ "".join(formatted_lines) }</div>'
    
    # 生成文档链接HTML
    doc_links_html = ''
    if doc_links:
        links = []
        for link in doc_links:
            if link.get('name') and link.get('url'):
                links.append(f'<a href="{link["url"]}" class="doc-link" target="_blank">{link["name"]}</a>')
        if links:
            doc_links_html = f'<div class="doc-links">{ "".join(links) }</div>'
    
    # 生成案件列表HTML
    cases_html = ''
    if cases:
        case_cards = [generate_case_card(case, section_id, i) for i, case in enumerate(cases)]
        cases_html = f'<div class="case-list">{ "".join(case_cards) }</div>'
    
    return f'''
    <div class="section">
        <div class="section-header">
            <span class="section-number">{section_number}</span>
            <span class="section-title">{section_title}</span>
        </div>
        <div class="section-body">
            {overview_html}
            {summary_html}
            {doc_links_html}
            {cases_html}
        </div>
    </div>
'''


def generate_html(data):
    """生成完整HTML"""
    # 读取模板
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 基本信息
    start_date = data.get('start_date', '')
    end_date = data.get('end_date', '')
    week_range, week_date_full = get_week_range(start_date, end_date)
    
    # 替换基本变量
    template = template.replace('{{week_date}}', week_range)
    template = template.replace('{{week_date_full}}', week_date_full)
    template = template.replace('{{total_cases}}', str(data.get('total_cases', 0)))
    template = template.replace('{{new_cases}}', str(data.get('new_cases', 0)))
    template = template.replace('{{closed_cases}}', str(data.get('closed_cases', 0)))
    template = template.replace('{{foreign_cases}}', str(data.get('foreign_cases', 0)))
    
    # 生成板块HTML
    sections_html = ''
    for section_config in SECTIONS:
        section_id = section_config['id']
        if section_id in data.get('sections', {}):
            sections_html += generate_section_html(
                data['sections'][section_id],
                section_config
            )
    template = template.replace('{{sections}}', sections_html)
    
    # 文档链接
    doc_links_html = ''
    for link in data.get('global_doc_links', []):
        if link.get('name') and link.get('url'):
            doc_links_html += f'<a href="{link["url"]}" class="doc-link" target="_blank">{link["name"]}</a>'
    template = template.replace('{{doc_links}}', doc_links_html)
    
    # 作者信息
    author = data.get('author', DEFAULT_AUTHOR)
    template = template.replace('{{author_name}}', author.get('name', DEFAULT_AUTHOR['name']))
    template = template.replace('{{author_title}}', author.get('title', DEFAULT_AUTHOR['title']))
    template = template.replace('{{notice_text}}', data.get('notice', DEFAULT_NOTICE))
    
    return template


def main():
    """主函数"""
    st.markdown('<div class="main-header">📊 综合诉讼维权中心周报生成器</div>', unsafe_allow_html=True)
    
    # 初始化session state
    if 'data' not in st.session_state:
        # 尝试加载自动保存的数据
        autosave_data = load_autosave()
        
        if autosave_data:
            st.session_state.data = autosave_data
            st.toast("✅ 已恢复上次自动保存的数据", icon="💾")
        else:
            # 计算本周的起始和结束日期（周一到周日）
            today = datetime.now()
            monday = today - timedelta(days=today.weekday())
            sunday = monday + timedelta(days=6)
            
            st.session_state.data = {
                'start_date': monday.strftime('%Y-%m-%d'),
                'end_date': sunday.strftime('%Y-%m-%d'),
                'total_cases': 124,
                'new_cases': 1,
                'closed_cases': 0,
                'foreign_cases': 5,
                'sections': {},
                'global_doc_links': [
                    {
                        'name': '综合中心个人在办案件表格',
                        'url': 'https://doc.weixin.qq.com/sheet/e3_ALAA4QZ6ACcCNnER3CoZxTtOXzrog?scode=AJEAIQdfAAoc3m7F7LAIAAQgZcACo'
                    }
                ],
                'author': DEFAULT_AUTHOR.copy(),
                'notice': DEFAULT_NOTICE
            }
    
    # 自动保存开关（默认开启）
    if 'autosave_enabled' not in st.session_state:
        st.session_state.autosave_enabled = True
    
    # 初始化其他session_state变量
    if 'show_html_code_area' not in st.session_state:
        st.session_state.show_html_code_area = False
    if 'html_to_copy' not in st.session_state:
        st.session_state.html_to_copy = ""
    if 'show_preview' not in st.session_state:
        st.session_state.show_preview = False
    if 'preview_content' not in st.session_state:
        st.session_state.preview_content = ""
    
    # 侧边栏 - 基本信息
    with st.sidebar:
        st.header("📋 基本信息")
        
        st.subheader("📅 工作周期")
        # 起始日期
        start_date = st.date_input(
            "起始日期",
            datetime.strptime(st.session_state.data['start_date'], '%Y-%m-%d'),
            key='start_date_input'
        )
        st.session_state.data['start_date'] = start_date.strftime('%Y-%m-%d')
        
        # 截止日期
        end_date = st.date_input(
            "截止日期",
            datetime.strptime(st.session_state.data['end_date'], '%Y-%m-%d'),
            key='end_date_input'
        )
        st.session_state.data['end_date'] = end_date.strftime('%Y-%m-%d')
        
        # 显示当前选择的周期
        week_range, week_date_full = get_week_range(
            st.session_state.data['start_date'], 
            st.session_state.data['end_date']
        )
        st.info(f"**当前周期**: {week_date_full}")
        
        st.subheader("整体数据")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.data['total_cases'] = st.number_input(
                "在办案件", value=124, min_value=0, key='total_cases'
            )
            st.session_state.data['new_cases'] = st.number_input(
                "新增案件", value=1, min_value=0, key='new_cases'
            )
        with col2:
            st.session_state.data['closed_cases'] = st.number_input(
                "结案数量", value=0, min_value=0, key='closed_cases'
            )
            st.session_state.data['foreign_cases'] = st.number_input(
                "涉外纠纷", value=5, min_value=0, key='foreign_cases'
            )
        
        # 作者信息折叠区域
        with st.expander("👤 作者信息", expanded=False):
            st.session_state.data['author']['name'] = st.text_input(
                "姓名", value=st.session_state.data['author'].get('name', DEFAULT_AUTHOR['name']), key='author_name'
            )
            st.session_state.data['author']['title'] = st.text_input(
                "职位", value=st.session_state.data['author'].get('title', DEFAULT_AUTHOR['title']), key='author_title'
            )
        
        # 设置折叠区域
        with st.expander("⚙️ 设置", expanded=False):
            st.session_state.autosave_enabled = st.toggle(
                "自动保存", 
                value=st.session_state.autosave_enabled,
                help="开启后数据会自动保存到本地文件，刷新页面不会丢失"
            )
            
            # 手动保存和清除按钮
            col_save, col_clear = st.columns(2)
            with col_save:
                if st.button("💾 立即保存", use_container_width=True):
                    if save_autosave(st.session_state.data):
                        st.success("已保存")
            with col_clear:
                if st.button("🗑️ 清除缓存", use_container_width=True):
                    if os.path.exists(AUTO_SAVE_FILE):
                        os.remove(AUTO_SAVE_FILE)
                        st.success("已清除")
                        st.rerun()
            
            # 重置数据按钮
            if st.button("🔄 重置所有数据", use_container_width=True, type="secondary"):
                if os.path.exists(AUTO_SAVE_FILE):
                    os.remove(AUTO_SAVE_FILE)
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        st.subheader("📎 附件")
        # 初始化全局文档链接
        if 'global_doc_links' not in st.session_state.data:
            st.session_state.data['global_doc_links'] = [
                {
                    'name': '综合中心个人在办案件表格',
                    'url': 'https://doc.weixin.qq.com/sheet/e3_ALAA4QZ6ACcCNnER3CoZxTtOXzrog?scode=AJEAIQdfAAoc3m7F7LAIAAQgZcACo'
                }
            ]
        
        # 显示附件列表
        for i, link in enumerate(st.session_state.data['global_doc_links']):
            cols = st.columns([3, 0.5])
            with cols[0]:
                link['name'] = st.text_input(
                    f"文档名称 {i+1}",
                    value=link.get('name', ''),
                    key=f'global_doc_name_{i}'
                )
                link['url'] = st.text_input(
                    f"文档地址 {i+1}",
                    value=link.get('url', ''),
                    key=f'global_doc_url_{i}'
                )
            with cols[1]:
                if i > 0:
                    if st.button("🗑️", key=f'del_global_doc_{i}'):
                        st.session_state.data['global_doc_links'].pop(i)
                        st.rerun()
            st.divider()
        
        # 添加附件按钮
        if st.button("➕ 添加附件", key='add_global_doc'):
            st.session_state.data['global_doc_links'].append({'name': '', 'url': ''})
            st.rerun()
    
    # 主界面 - 板块编辑
    tabs = st.tabs([s['title'] for s in SECTIONS])
    
    for idx, (tab, section_config) in enumerate(zip(tabs, SECTIONS)):
        with tab:
            section_id = section_config['id']
            
            if section_id not in st.session_state.data['sections']:
                # 根据板块设置默认文档链接
                default_doc_links = {
                    'labor': [
                        {
                            'name': '海外劳动纠纷整体详情',
                            'url': 'https://doc.weixin.qq.com/doc/w3_AUEACAb8ADwCNkmv9OBoiTDewsoK0?scode=AJEAIQdfAAoRSMMVQIALAA4QZ6ACc'
                        }
                    ],
                    'infrastructure': [
                        {
                            'name': '综合诉讼-基建争议汇总表',
                            'url': 'https://doc.weixin.qq.com/sheet/e3_AIAAQgZcACojZU0AYcCQJu5FvGPbe?scode=AJEAIQdfAAoK2pdsV7AIAAQgZcACo'
                        },
                        {
                            'name': '基建重点案件情况梳理',
                            'url': 'https://doc.weixin.qq.com/doc/w3_AIAAQgZcACosOZ914YfTJWJ1iHHT0?scode=AJEAIQdfAAol57yC7xALAA4QZ6ACc'
                        }
                    ],
                    'non_compete': [
                        {
                            'name': '竞业限制案件整体情况',
                            'url': 'https://doc.weixin.qq.com/sheet/e3_AL4AgAaBACcdYDyiu5FQ3Gcy28GlW?scode=AJEAIQdfAAoHdoFEvUAMUA5waQACc&tab=BB08J2'
                        }
                    ],
                    'other': []
                }
                
                st.session_state.data['sections'][section_id] = {
                    'overview': {},
                    'summary': '',
                    'doc_links': default_doc_links.get(section_id, []),
                    'cases': []
                }
            
            section_data = st.session_state.data['sections'][section_id]
            
            # 概览数据
            st.markdown('<div class="section-header">📊 数据概览</div>', unsafe_allow_html=True)
            
            if section_id == 'labor':
                col1, col2, col3 = st.columns(3)
                with col1:
                    section_data['overview']['涉外案件'] = st.number_input(
                        "涉外案件", value=5, min_value=0, key=f'{section_id}_foreign'
                    )
                with col2:
                    section_data['overview']['国内案件'] = st.number_input(
                        "国内案件", value=80, min_value=0, key=f'{section_id}_domestic'
                    )
                with col3:
                    section_data['overview']['活跃案件'] = st.number_input(
                        "活跃案件", value=9, min_value=0, key=f'{section_id}_active'
                    )
                
                # 自动计算在办案件 = 涉外案件 + 国内案件
                foreign = section_data['overview'].get('涉外案件', 0)
                domestic = section_data['overview'].get('国内案件', 0)
                section_data['overview']['在办案件'] = foreign + domestic
                
                # 显示自动计算的在办案件
                st.markdown(f"**在办案件**: {section_data['overview']['在办案件']} (自动计算: 涉外 {foreign} + 国内 {domestic})")
            
            elif section_id == 'infrastructure':
                col1, col2, col3 = st.columns(3)
                with col1:
                    section_data['overview']['在办案件'] = st.number_input(
                        "在办案件", value=20, min_value=0, key=f'{section_id}_cases'
                    )
                with col2:
                    section_data['overview']['本周新增'] = st.number_input(
                        "本周新增", value=0, min_value=0, key=f'{section_id}_new'
                    )
                with col3:
                    section_data['overview']['本周结案'] = st.number_input(
                        "本周结案", value=0, min_value=0, key=f'{section_id}_closed'
                    )
                
                # 细分分布
                st.markdown("**案件类型分布**")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    section_data['overview']['结算纠纷'] = st.number_input(
                        "结算纠纷", value=4, min_value=0, key=f'{section_id}_type1'
                    )
                with col2:
                    section_data['overview']['工伤案件'] = st.number_input(
                        "工伤案件", value=4, min_value=0, key=f'{section_id}_type2'
                    )
                with col3:
                    section_data['overview']['劳务纠纷'] = st.number_input(
                        "劳务纠纷", value=9, min_value=0, key=f'{section_id}_type3'
                    )
                with col4:
                    section_data['overview']['保险案件'] = st.number_input(
                        "保险案件", value=3, min_value=0, key=f'{section_id}_type4'
                    )
            
            elif section_id == 'non_compete':
                st.markdown("**主指标**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    section_data['overview']['竞业期内人员'] = st.number_input(
                        "竞业期内人员", value=65, min_value=0, key=f'{section_id}_persons'
                    )
                with col2:
                    section_data['overview']['在诉案件'] = st.number_input(
                        "在诉案件", value=14, min_value=0, key=f'{section_id}_litigation'
                    )
                with col3:
                    section_data['overview']['调查取证'] = st.number_input(
                        "调查取证", value=40, min_value=0, key=f'{section_id}_investigation'
                    )
                
                st.markdown("**次要指标**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    section_data['overview']['新增主诉'] = st.number_input(
                        "新增主诉", value=1, min_value=0, key=f'{section_id}_new_main'
                    )
                with col2:
                    section_data['overview']['近期待诉'] = st.number_input(
                        "近期待诉", value=8, min_value=0, key=f'{section_id}_pending'
                    )
                with col3:
                    section_data['overview']['被诉支持'] = st.number_input(
                        "被诉支持", value=8, min_value=0, key=f'{section_id}_defense'
                    )
                
                # BG分布数据
                st.markdown("**在诉案件 BG 分布**")
                bg_list = ['TEG', 'CDG', 'IEG', 'CSIG', 'WXG', 'S1', 'PCG']
                # 在诉案件默认值：TEG=9, CDG=1, IEG=3, CSIG=1, WXG=0, S1=0, PCG=0
                lit_default_values = {'TEG': 9, 'CDG': 1, 'IEG': 3, 'CSIG': 1, 'WXG': 0, 'S1': 0, 'PCG': 0}
                col1, col2, col3 = st.columns(3)
                for i, bg in enumerate(bg_list):
                    with [col1, col2, col3][i % 3]:
                        section_data['overview'][f'在诉_{bg}'] = st.number_input(
                            f"在诉 {bg}", value=lit_default_values[bg], min_value=0, key=f'{section_id}_lit_{bg}'
                        )
                
                st.markdown("**调查取证 BG 分布**")
                # 调查取证默认值：TEG=18, CDG=8, CSIG=8, IEG=3, WXG=2, S1=1, PCG=0
                inv_default_values = {'TEG': 18, 'CDG': 8, 'CSIG': 8, 'IEG': 3, 'WXG': 2, 'S1': 1, 'PCG': 0}
                col1, col2, col3 = st.columns(3)
                for i, bg in enumerate(bg_list):
                    with [col1, col2, col3][i % 3]:
                        section_data['overview'][f'调查_{bg}'] = st.number_input(
                            f"调查 {bg}", value=inv_default_values[bg], min_value=0, key=f'{section_id}_inv_{bg}'
                        )
            
            # 摘要 - 重点案件列表
            st.markdown('<div class="section-header">📝 重点案件摘要</div>', unsafe_allow_html=True)
            
            # 初始化重点案件列表
            if 'highlight_cases' not in section_data:
                section_data['highlight_cases'] = [
                    {'name': '', 'progress': ''}
                ]
            
            # 显示重点案件输入表单
            for i, case in enumerate(section_data['highlight_cases']):
                cols = st.columns([1, 3, 0.3])
                with cols[0]:
                    case['name'] = st.text_input(
                        f"重点案件名称 {i+1}",
                        value=case.get('name', ''),
                        key=f'{section_id}_highlight_name_{i}'
                    )
                with cols[1]:
                    case['progress'] = st.text_input(
                        f"案件进展 {i+1}",
                        value=case.get('progress', ''),
                        key=f'{section_id}_highlight_progress_{i}'
                    )
                with cols[2]:
                    if i > 0:
                        st.write("")  # 添加空行对齐
                        if st.button("🗑️", key=f'{section_id}_del_highlight_{i}'):
                            section_data['highlight_cases'].pop(i)
                            st.rerun()
            
            # 添加新案件按钮
            if st.button("➕ 添加重点案件", key=f'{section_id}_add_highlight'):
                section_data['highlight_cases'].append({'name': '', 'progress': ''})
                st.rerun()
            
            # 保存为summary字段（兼容原有数据结构）
            summary_lines = []
            for case in section_data['highlight_cases']:
                if case.get('name') or case.get('progress'):
                    summary_lines.append(f"{case.get('name', '')}|{case.get('progress', '')}")
            section_data['summary'] = '\n'.join(summary_lines)
            
            # 文档链接
            st.markdown('<div class="section-header">🔗 文档链接</div>', unsafe_allow_html=True)
            doc_link_count = st.number_input(
                "文档链接数量", min_value=0, max_value=5, value=len(section_data.get('doc_links', [])), key=f'{section_id}_doc_count'
            )
            
            # 调整文档链接列表长度
            while len(section_data.get('doc_links', [])) < doc_link_count:
                section_data['doc_links'].append({'name': '', 'url': ''})
            while len(section_data.get('doc_links', [])) > doc_link_count:
                section_data['doc_links'].pop()
            
            for i in range(doc_link_count):
                col1, col2 = st.columns([1, 2])
                with col1:
                    section_data['doc_links'][i]['name'] = st.text_input(
                        f"链接名称 {i+1}",
                        value=section_data['doc_links'][i].get('name', ''),
                        key=f'{section_id}_doc_name_{i}'
                    )
                with col2:
                    section_data['doc_links'][i]['url'] = st.text_input(
                        f"链接地址 {i+1}",
                        value=section_data['doc_links'][i].get('url', ''),
                        key=f'{section_id}_doc_url_{i}'
                    )
            
            # 案件列表
            st.markdown('<div class="section-header">📁 案件列表</div>', unsafe_allow_html=True)
            
            # 初始化案件列表（默认1个）
            if 'cases' not in section_data or not section_data['cases']:
                section_data['cases'] = [{
                    'title': '',
                    'progress': '',
                    'follow_up': '',
                    'owners': '',
                    'status': ''
                }]
            
            # 显示案件表单
            for i, case in enumerate(section_data['cases']):
                case_title = case.get('title', '') or '未命名'
                case_count = len(section_data['cases'])
                
                # 构建标题栏，包含删除按钮
                if case_count > 1:
                    header_cols = st.columns([8, 1])
                    with header_cols[0]:
                        st.markdown(f"**案件 {i+1}**: {case_title}")
                    # 删除按钮
                    with header_cols[1]:
                        if st.button("🗑️", key=f'{section_id}_del_case_{i}', help="删除"):
                            section_data['cases'].pop(i)
                            st.rerun()
                
                with st.expander(f"编辑案件详情", expanded=True):
                    
                    case['title'] = st.text_input(
                        "案件标题",
                        value=case.get('title', ''),
                        key=f'{section_id}_case_title_{i}',
                        placeholder="请输入案件标题"
                    )
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        selected_owners = st.multiselect(
                            "负责人",
                            options=OWNERS,
                            default=[o for o in case.get('owners', '').split('、') if o in OWNERS],
                            key=f'{section_id}_case_owners_{i}'
                        )
                        # 将列表转换为字符串
                        case['owners'] = '、'.join(selected_owners)
                    with col2:
                        # 根据板块确定可选标签
                        if section_id == 'non_compete':
                            status_options = NON_COMPETE_STATUS_OPTIONS
                        else:
                            status_options = STATUS_OPTIONS
                        
                        # 处理默认值的解析
                        default_status = case.get('status', '')
                        if isinstance(default_status, str):
                            default_status_list = [s.strip() for s in default_status.split('、') if s.strip() and s.strip() in status_options]
                        elif isinstance(default_status, list):
                            default_status_list = [s for s in default_status if s in status_options]
                        else:
                            default_status_list = []
                        
                        selected_status = st.multiselect(
                            "状态标签（可多选）",
                            options=status_options,
                            default=default_status_list,
                            key=f'{section_id}_case_status_{i}'
                        )
                        # 将列表转换为字符串存储
                        case['status'] = '、'.join(selected_status)
                    
                    # 根据负责人动态设置标签（只有第一个负责人是mark时才应用）
                    current_owners = [o.strip().lower() for o in case['owners'].split('、') if o.strip()]
                    is_mark_first = len(current_owners) > 0 and current_owners[0] == 'mark'
                    first_label = "基本背景" if is_mark_first else "案件进展"
                    second_label = "案件进展" if is_mark_first else "后续安排"
                    
                    case['progress'] = st.text_area(
                        first_label,
                        value=case.get('progress', ''),
                        height=100,
                        key=f'{section_id}_case_progress_{i}'
                    )
                    
                    case['follow_up'] = st.text_area(
                        second_label,
                        value=case.get('follow_up', ''),
                        height=80,
                        key=f'{section_id}_case_follow_up_{i}'
                    )
            
            # 添加新案件按钮
            if st.button("➕ 添加案件", key=f'{section_id}_add_case'):
                section_data['cases'].append({
                    'title': '',
                    'progress': '',
                    'follow_up': '',
                    'owners': '',
                    'status': ''
                })
                st.rerun()
    
    # 底部操作按钮
    st.markdown("---")
    
    # 生成HTML内容（供后续使用）
    html_content = generate_html(st.session_state.data)
    file_date = st.session_state.data['end_date']
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        # 保存数据为JSON
        json_str = json.dumps(st.session_state.data, ensure_ascii=False, indent=2)
        st.download_button(
            label="💾 保存数据(JSON)",
            data=json_str,
            file_name=f"weekly_report_{file_date}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # 预览HTML - 使用Streamlit原生预览
        if st.button("👁️ 预览HTML", use_container_width=True, key="preview_html_btn"):
            st.session_state.show_preview = True
            st.session_state.preview_content = html_content
            st.rerun()
    
    with col3:
        # 直接下载HTML
        st.download_button(
            label="📥 下载HTML",
            data=html_content,
            file_name=f"weekly_report_{file_date}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col4:
        # 复制HTML源代码到剪贴板 - 使用Streamlit按钮
        if st.button("📋 复制HTML代码", use_container_width=True, key="copy_html_btn"):
            # 使用pyperclip或其他方式复制到剪贴板
            st.session_state.html_to_copy = html_content
            st.success("HTML代码已准备，请使用Ctrl+C复制下方显示的代码")
            st.session_state.show_html_code_area = True
        
        # 显示HTML代码区域
        if st.session_state.get('show_html_code_area', False):
            st.text_area("复制下方代码", st.session_state.get('html_to_copy', html_content), height=200, key="html_code_display")
    
    # 显示HTML预览
    if st.session_state.get('show_preview', False):
        st.markdown("---")
        st.subheader("👁️ HTML预览")
        
        # 使用iframe方式预览
        preview_html = st.session_state.get('preview_content', html_content)
        st.components.v1.html(preview_html, height=800, scrolling=True)
        
        # 关闭预览按钮
        if st.button("❌ 关闭预览", key="close_preview"):
            st.session_state.show_preview = False
            st.rerun()
    
    # 自动保存（在页面底部执行）
    if st.session_state.get('autosave_enabled', True):
        save_autosave(st.session_state.data)


if __name__ == '__main__':
    main()
