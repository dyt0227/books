#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Netflix Culture Handbook H5 pages - v7"""

import json, re, html as html_mod

with open("../chapters.json", "r", encoding="utf-8") as f:
    chapters = json.load(f)

CHAPTERS_NAV = [
    {"id": "preface", "title": "推荐序", "subtitle": "毛大庆 / 龚宇"},
    {"id": "intro", "title": "前言", "subtitle": "自由与责任，奈飞文化的核心"},
    {"id": "c1", "title": "文化准则1", "subtitle": "我们只招成年人"},
    {"id": "c2", "title": "文化准则2", "subtitle": "要让每个人都理解公司业务"},
    {"id": "c3", "title": "文化准则3", "subtitle": "绝对坦诚，才能获得真正高效的反馈"},
    {"id": "c4", "title": "文化准则4", "subtitle": "只有事实才能捍卫观点"},
    {"id": "c5", "title": "文化准则5", "subtitle": "现在就开始组建你未来需要的团队"},
    {"id": "c6", "title": "文化准则6", "subtitle": "员工与岗位的关系，不是匹配而是高度匹配"},
    {"id": "c7", "title": "文化准则7", "subtitle": "按照员工带来的价值付薪"},
    {"id": "c8", "title": "文化准则8", "subtitle": "离开时要好好说再见"},
    {"id": "epilogue", "title": "结语", "subtitle": "文化即战略，创造你自己的管理新算法"},
]

ID_TO_IDX = {c["id"]: i for i, c in enumerate(CHAPTERS_NAV)}

def esc(s):
    return html_mod.escape(s)

ICON_BACK = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>'
ICON_MENU = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg>'
ICON_SETTINGS = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path stroke-linecap="round" stroke-linejoin="round" d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'
ICON_CHEVRON_R = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>'
ICON_CHEVRON_L = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>'
ICON_HOME = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>'
ICON_LIST = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg>'
ICON_TEXT = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h8m-8 6h16"/></svg>'
ICON_CLOSE = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>'
ICON_SHARE = '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>'

def make_head(title):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>'''

# ===== CONTENT PROCESSING v7 =====

KNOWN_HEADINGS = {
    "c1": ["成年人最渴望的奖励，就是成功", "每个人都渴望与高绩效者合作", "不要让规章与制度限制了高绩效者"],
    "c2": ["培养基层员工的高层视角", "保持沟通的强节奏", "双向沟通，注入好奇文化", "员工的无知，是管理者的失职", "让员工学习冲突管理，不如让他们学习业务运作", "情况在不断变化，沟通必须持续进行"],
    "c3": ["人前人后言行一致", "公开批评的价值", "学会给出受欢迎的批评", "自上而下树立坦诚的榜样", "为反馈提供多种机制", "坦承成绩，更要坦承问题", "领导者能够坦承错误，员工就能畅所欲言", "透明文化，让错误无处遁形"],
    "c4": ["坚持你的观点，用事实为它辩护", "数据并不带有观点", "小心看起来很好实际上没用的数据", "用数据对观点进行检验", "基于事实≠真实，对观点进行不断审视", "要解决观点分歧，就将辩论公开化"],
    "c5": ["不要让招聘成为一场数字游戏", "不要期望你今天的团队能成为你明天的团队", "站在6个月后的未来，审视你现在的团队", "你建立的是团队，不是家庭", "员工的成长，只能由自己负责", "企业在不同的阶段，需要不同的员工", "你不必在一家公司待一辈子"],
    "c6": ["人才保留不是团队建设的目标", "伟大的工作与福利无关", "不与面试者谈薪酬", "用超高的人才密度吸引人才", "不是每个岗位都需要爱因斯坦", "简历之外，更能看出匹配度", "永远在招聘", "当人力资源部门成为业务部门"],
    "c7": ["薪酬与绩效评估流程无关，只与绩效有关", "不要让员工在不得不离开时才获得应得的薪水", "保证每个人都获得市场最高水平的薪水", "告别密薪制，薪酬透明有助于市场定价"],
    "c8": ["每10场比赛就做一次评估", "取消绩效评估流程", "废除绩效提升计划", "理想的公司就是那种离开之后仍然觉得它很伟大的公司", "高敬业度不代表高绩效", "员工评估的一个算法", "主动让员工离开", "终身雇用制的消失"],
}

GENERIC_HEADINGS = [
    "21世纪的企业VS.20世纪的管理方法", "像管理创新那样管理员工", "打造以自由与责任为核心的企业文化",
    "文化即战略，创造你自己的管理新算法",
]

def is_heading(text, chapter_id):
    text = text.strip()
    if not text:
        return False
    all_headings = KNOWN_HEADINGS.get(chapter_id, []) + GENERIC_HEADINGS
    for h in all_headings:
        if h == text or text in h or h in text:
            return True
    return False

def clean_raw_text(text):
    text = re.sub(r'^\d+/79\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
    # Only fix spaces (not newlines) between CJK chars
    text = re.sub(r'([\u4e00-\u9fff]) +([\u4e00-\u9fff])', r'\1\2', text)
    text = re.sub(r'([\u4e00-\u9fff]) +([，。、；：！？「」『』""''（）【】])', r'\1\2', text)
    text = re.sub(r'([，。、；：！？「」『』""''（）【】]) +([\u4e00-\u9fff])', r'\1\2', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def strip_quiz_and_prefix(text, chapter_id):
    quiz_start = text.find("你拥有奈飞思维吗")
    if quiz_start >= 0:
        rest = text[quiz_start:]
        d_positions = [m.start() for m in re.finditer(r'\nD\.', rest)]
        if len(d_positions) >= 5:
            after_5d = d_positions[4] + 2
            line_end = rest.find('\n', after_5d)
            if line_end < 0:
                line_end = len(rest)
            prefix = text[:quiz_start].rstrip()
            last_nl = prefix.rfind('\n')
            if last_nl >= 0:
                line_before = prefix[last_nl+1:].strip()
                if any(p in line_before for p in ['文化准则', '推荐序', '前言', '结语']):
                    prefix = prefix[:last_nl+1]
            text = prefix + rest[line_end:]
    
    text = re.sub(r'你拥有奈飞思维吗', '', text)
    text = re.sub(r'^\d+\.[\s\S]*?(?=\n\d+\.|\n[A-Z]\.|\n[^\dA-Z\s]|$)', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[A-D]\..*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+.*$', '', text, flags=re.MULTILINE)
    
    title_patterns = [
        r'^\d{1,2}\s*文化准则\d.*$',
        r'^文化准则\d.*$',
        r'^推荐序[一二].*$',
        r'^前言.*$',
        r'^结语.*$',
    ]
    for pat in title_patterns:
        text = re.sub(pat, '', text, flags=re.MULTILINE)
    return text

def merge_soft_breaks(text, chapter_id):
    """Merge soft line breaks, but preserve headings as separate blocks"""
    lines = text.split('\n')
    result = []
    current = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            if current:
                result.append(current)
                current = ""
            continue
        
        # If this line is a known heading, flush current and output heading separately
        if is_heading(line, chapter_id):
            if current:
                result.append(current)
                current = ""
            result.append(f"__HEADING__{line}")
            continue
        
        # If current is empty, start new paragraph
        if not current:
            current = line
            continue
        
        # If current ends with sentence-ending punctuation, start new paragraph
        if current.endswith(('。', '！', '？', '」', '”', '.', '…', '）', '：')):
            result.append(current)
            current = line
        else:
            # Soft break: merge with current (remove the newline)
            current += line
    
    if current:
        result.append(current)
    
    return result

def is_quote(text):
    # Only mark as quote if text is relatively short and primarily quoted
    if len(text) > 200:
        return False
    if '「' in text and '」' in text:
        return True
    if '“' in text and '”' in text:
        return True
    return False

def process_content(text, chapter_id):
    text = clean_raw_text(text)
    text = strip_quiz_and_prefix(text, chapter_id)
    text = clean_raw_text(text)
    blocks = merge_soft_breaks(text, chapter_id)
    
    html_parts = []
    for block in blocks:
        if not block.strip():
            continue
        
        if block.startswith('__HEADING__'):
            title = block[11:]
            html_parts.append(f'<h3>{esc(title)}</h3>')
            continue
        
        if is_quote(block):
            html_parts.append(f'<div class="quote"><p>{format_inline(esc(block))}</p></div>')
            continue
        
        highlight_labels = ['关键洞察', '核心启示', '行动建议', '帕蒂的回应', '关键准则']
        is_highlight = False
        for label in highlight_labels:
            if block.startswith(label):
                html_parts.append(render_highlight_block(block, label))
                is_highlight = True
                break
        if is_highlight:
            continue
        
        if len(block) < 120 and ('永远不要' in block or '最重要' in block or '必须' in block[:50]):
            html_parts.append(f'<div class="takeaway"><div class="takeaway-title">核心启示</div><p>{format_inline(esc(block))}</p></div>')
            continue
        
        html_parts.append(f'<p>{format_inline(esc(block))}</p>')
    
    return '\n'.join(html_parts)

def render_highlight_block(text, label):
    text = re.sub(r'^' + re.escape(label) + r'\s*', '', text)
    paras = [p.strip() for p in text.split('\n') if p.strip()]
    inner = '\n'.join(f'<p class="no-indent">{format_inline(esc(p))}</p>' for p in paras)
    return f'<div class="highlight-box"><div class="highlight-label">{esc(label)}</div>{inner}</div>'

def format_inline(text):
    text = re.sub(r'(《[^》]+》)', r'<em>\1</em>', text)
    return text

# ===== GENERATE INDEX =====
def generate_index():
    toc_items = []
    for idx, ch in enumerate(CHAPTERS_NAV, 1):
        num_cls = "toc-num preface" if ch["id"] == "preface" else "toc-num"
        num_text = "序" if ch["id"] == "preface" else ("结" if ch["id"] == "epilogue" else ("引" if ch["id"] == "intro" else str(idx - 1)))
        toc_items.append(f'''
        <a href="chapter-{ch["id"]}.html" class="toc-item animate-in delay-{min(idx, 3)}">
          <span class="{num_cls}">{num_text}</span>
          <div class="toc-content">
            <div class="toc-item-title">{esc(ch["title"])}</div>
            <div class="toc-item-sub">{esc(ch["subtitle"])}</div>
          </div>
          <span class="toc-arrow">{ICON_CHEVRON_R}</span>
          <div class="toc-progress-bg"><div class="toc-progress-fill" id="prog-{ch["id"]}"></div></div>
        </a>''')
    
    return make_head("奈飞文化手册") + f'''
<body>
<div class="cover-page">
  <div class="cover-hero animate-in">
    <div class="cover-badge">Netflix Culture</div>
    <h1 class="cover-title">奈飞文化手册</h1>
    <p class="cover-subtitle">支撑 827 亿 IP 整合的底层逻辑</p>
    <p class="cover-author">帕蒂·麦考德 著 · 范珂 译</p>
    <div class="cover-meta">
      <div class="cover-meta-item">
        <div class="cover-meta-num">{len(CHAPTERS_NAV)}</div>
        <div class="cover-meta-label">章节</div>
      </div>
      <div class="cover-meta-item">
        <div class="cover-meta-num">79</div>
        <div class="cover-meta-label">页数</div>
      </div>
    </div>
    <a href="chapter-preface.html" class="cover-start-btn">开始阅读</a>
  </div>

  <div class="toc-section">
    <div class="toc-title">目录</div>
    <div class="toc-list">
      {''.join(toc_items)}
    </div>
  </div>
</div>

<script>
const CHAPTERS_NAV = {json.dumps([{"id":c["id"]} for c in CHAPTERS_NAV], ensure_ascii=False)};
function updateTOCProgress() {{
  CHAPTERS_NAV.forEach(ch => {{
    const prog = localStorage.getItem('prog_' + ch.id);
    if (prog) {{
      const el = document.getElementById('prog-' + ch.id);
      if (el) el.style.width = prog + '%';
    }}
  }});
}}
updateTOCProgress();
</script>
</body>
</html>'''

# ===== GENERATE CHAPTER =====
def generate_chapter(ch_data):
    cid = ch_data["id"]
    idx = ID_TO_IDX[cid]
    
    prev_ch = CHAPTERS_NAV[idx - 1] if idx > 0 else None
    next_ch = CHAPTERS_NAV[idx + 1] if idx < len(CHAPTERS_NAV) - 1 else None
    
    article_html = process_content(ch_data["content"], cid)
    
    pages = ch_data.get("pages", (0, 0))
    page_range = f"P{pages[0]}-{pages[1]}" if pages != (0, 0) else ""
    
    prev_btn = ''
    if prev_ch:
        prev_btn = f'''<a href="chapter-{prev_ch["id"]}.html" class="chapter-nav-btn">
          {ICON_CHEVRON_L}
          <div>
            <div class="chapter-nav-label">上一章</div>
            <div class="chapter-nav-title">{esc(prev_ch["title"])}</div>
          </div>
        </a>'''
    else:
        prev_btn = f'''<a href="index.html" class="chapter-nav-btn">
          {ICON_CHEVRON_L}
          <div>
            <div class="chapter-nav-label">返回</div>
            <div class="chapter-nav-title">目录</div>
          </div>
        </a>'''
    
    next_btn = ''
    if next_ch:
        next_btn = f'''<a href="chapter-{next_ch["id"]}.html" class="chapter-nav-btn next">
          <div>
            <div class="chapter-nav-label">下一章</div>
            <div class="chapter-nav-title">{esc(next_ch["title"])}</div>
          </div>
          {ICON_CHEVRON_R}
        </a>'''
    else:
        next_btn = f'''<a href="index.html" class="chapter-nav-btn next">
          <div>
            <div class="chapter-nav-label">完成</div>
            <div class="chapter-nav-title">返回目录</div>
          </div>
          {ICON_CHEVRON_R}
        </a>'''
    
    toc_drawer_items = []
    for c in CHAPTERS_NAV:
        active = ' active' if c["id"] == cid else ''
        toc_drawer_items.append(f'''<a href="chapter-{c["id"]}.html" class="toc-drawer-item{active}">
          <div class="toc-drawer-item-title">{esc(c["title"])}</div>
          <div class="toc-drawer-item-sub">{esc(c["subtitle"])}</div>
        </a>''')
    
    return make_head(f"{ch_data['title']} - 奈飞文化手册") + f'''
<body>
<header class="header">
  <div class="header-left">
    <a href="index.html" class="header-btn" aria-label="返回">{ICON_BACK}</a>
  </div>
  <div class="header-title">{esc(ch_data["subtitle"] if ch_data["subtitle"] else ch_data["title"])}</div>
  <div class="header-right">
    <button class="header-btn" onclick="toggleTOC()" aria-label="目录">{ICON_MENU}</button>
    <button class="header-btn" onclick="toggleSettings()" aria-label="设置">{ICON_SETTINGS}</button>
  </div>
</header>

<div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>

<main class="chapter-main" id="chapterMain">
  <div class="chapter-container">
    <div class="chapter-hero animate-in">
      <div class="chapter-label">{esc(ch_data["title"])}</div>
      <h1 class="chapter-title">{esc(ch_data["subtitle"])}</h1>
      <div class="chapter-pages">{page_range}</div>
    </div>
    
    <article class="article animate-in delay-1" id="article">
      {article_html}
    </article>
    
    <div class="chapter-nav">
      {prev_btn}
      {next_btn}
    </div>
  </div>
</main>

<div class="settings-overlay" id="tocOverlay" onclick="toggleTOC()"></div>
<aside class="toc-drawer" id="tocDrawer">
  <div class="toc-drawer-header">
    <div class="toc-drawer-title">目录</div>
    <button class="toc-drawer-close" onclick="toggleTOC()">{ICON_CLOSE}</button>
  </div>
  <div class="toc-drawer-list">
    <a href="index.html" class="toc-drawer-item">
      <div class="toc-drawer-item-title">封面</div>
      <div class="toc-drawer-item-sub">奈飞文化手册</div>
    </a>
    {''.join(toc_drawer_items)}
  </div>
</aside>

<div class="settings-overlay" id="settingsOverlay" onclick="toggleSettings()"></div>
<div class="settings-panel" id="settingsPanel">
  <button class="settings-close" onclick="toggleSettings()">{ICON_CLOSE}</button>
  <div class="settings-title">阅读设置</div>
  <div class="settings-row">
    <span class="settings-label">字体大小</span>
    <div class="settings-options">
      <button class="settings-opt" onclick="setFontSize(14)">小</button>
      <button class="settings-opt active" onclick="setFontSize(16)">中</button>
      <button class="settings-opt" onclick="setFontSize(18)">大</button>
    </div>
  </div>
  <div class="settings-row">
    <span class="settings-label">行间距</span>
    <div class="settings-options">
      <button class="settings-opt" onclick="setLineHeight(1.6)">紧凑</button>
      <button class="settings-opt active" onclick="setLineHeight(2)">标准</button>
      <button class="settings-opt" onclick="setLineHeight(2.4)">宽松</button>
    </div>
  </div>
</div>

<nav class="bottom-bar">
  <button class="bottom-btn" onclick="location.href='index.html'">{ICON_HOME}<span>目录</span></button>
  <button class="bottom-btn" onclick="toggleTOC()">{ICON_LIST}<span>章节</span></button>
  <button class="bottom-btn" onclick="toggleSettings()">{ICON_TEXT}<span>设置</span></button>
  <button class="bottom-btn" onclick="sharePage()">{ICON_SHARE}<span>分享</span></button>
</nav>

<script>
const chapterId = '{cid}';

function updateProgress() {{
  const main = document.getElementById('chapterMain');
  const scrollTop = window.scrollY;
  const scrollHeight = main.scrollHeight + main.offsetTop - window.innerHeight;
  const progress = scrollHeight > 0 ? Math.min(100, (scrollTop / scrollHeight) * 100) : 0;
  document.getElementById('progressFill').style.width = progress + '%';
  localStorage.setItem('prog_' + chapterId, Math.round(progress));
}}
window.addEventListener('scroll', updateProgress, {{ passive: true }});
updateProgress();

function toggleSettings() {{
  document.getElementById('settingsPanel').classList.toggle('open');
  document.getElementById('settingsOverlay').classList.toggle('open');
}}

function toggleTOC() {{
  document.getElementById('tocDrawer').classList.toggle('open');
  document.getElementById('tocOverlay').classList.toggle('open');
}}

function setFontSize(size) {{
  document.getElementById('article').style.fontSize = size + 'px';
  const btns = document.querySelectorAll('#settingsPanel .settings-opt');
  btns.forEach((btn, idx) => {{
    if (idx < 3) btn.classList.toggle('active', 
      (size === 14 && idx === 0) || (size === 16 && idx === 1) || (size === 18 && idx === 2));
  }});
  localStorage.setItem('fontSize', size);
}}

function setLineHeight(lh) {{
  document.getElementById('article').style.lineHeight = lh;
  const btns = document.querySelectorAll('#settingsPanel .settings-opt');
  btns.forEach((btn, idx) => {{
    if (idx >= 3) btn.classList.toggle('active',
      (lh === 1.6 && idx === 3) || (lh === 2 && idx === 4) || (lh === 2.4 && idx === 5));
  }});
  localStorage.setItem('lineHeight', lh);
}}

const savedFont = localStorage.getItem('fontSize');
const savedLH = localStorage.getItem('lineHeight');
if (savedFont) setFontSize(parseInt(savedFont));
if (savedLH) setLineHeight(parseFloat(savedLH));

function sharePage() {{
  const url = window.location.href;
  const title = document.title;
  if (navigator.share) {{
    navigator.share({{ title: title, url: url }}).catch(() => {{}});
  }} else {{
    navigator.clipboard.writeText(url).then(() => alert('链接已复制'));
  }}
}}
</script>
</body>
</html>'''

if __name__ == '__main__':
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generate_index())
    print("Generated: index.html")
    
    for ch in chapters:
        html = generate_chapter(ch)
        fname = f"chapter-{ch['id']}.html"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Generated: {fname}")
    
    print("\nDone!")
