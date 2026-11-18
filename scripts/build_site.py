import argparse,pathlib,json,html,re,shutil
R=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Build the offline teaching site.')
parser.add_argument('--staging', type=pathlib.Path, help='Directory containing pages.json, manifest.json, and deck.pptx.')
staging=parser.parse_args().staging
D=staging/'site' if staging else R/'docs'
(D/'assets/slides').mkdir(parents=True,exist_ok=True)
pages=json.loads(((staging/'pages.json') if staging else (R/'slides/pages.json')).read_text(encoding='utf-8'))
image_paths={}
if staging:
 manifest=json.loads((staging/'manifest.json').read_text(encoding='utf-8'))
 for item in manifest['pages']:
  selected=next(c for c in item['candidates'] if c['id']==item['adopted_candidate_id'])
  image_paths[item['page_id']]=R/selected['path']
def esc(s):return html.escape(s)
def put(p,s):(D/p).write_text(s,encoding='utf-8',newline='\n')
nav='<nav><a class="brand" href="index.html">因式分解<span>十分钟课堂</span></a><div><a href="script.html">逐字稿</a><a href="board.html">板书</a><a href="slides.html">演示文稿</a><a href="lesson.html">教学设计</a></div></nav>'
def page(title,body,js=''):
 description='七年级数学因式分解入门：提公因式法十分钟试讲、逐字稿、教学设计、分步板书、课件和练习。'
 metadata='<meta name="description" content="'+description+'"><link rel="alternate" type="text/plain" href="llms.txt" title="Agent 资料索引">'
 footer='<footer>沪科版七年级下册 8.4 · 概念与提公因式法基础 · <a href="llms.txt">Agent 资料索引</a></footer>'
 return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+metadata+'<title>'+title+' · 因式分解</title><link rel="stylesheet" href="assets/style.css"><body>'+nav+body+footer+('<script src="assets/'+js+'"></script>' if js else '')+'</body></html>'
put(pathlib.Path('assets/style.css'),'''*{box-sizing:border-box}body{margin:0;background:#fff;color:#17364b;font-family:"Microsoft YaHei",system-ui,sans-serif}nav{display:flex;justify-content:space-between;align-items:center;padding:24px 5vw;border-bottom:1px solid #dde8e6;gap:20px}a{color:inherit;text-decoration:none}nav div{display:flex;gap:28px}a:hover{color:#087a70}.brand{font-size:21px;font-weight:700}.brand span{display:block;font-size:12px;font-weight:400;color:#607a80;margin-top:4px}main{max-width:1160px;margin:auto;padding:64px 28px}h1{font-size:clamp(32px,4vw,60px);line-height:1.25;letter-spacing:-1px}h2{font-size:27px}p,li{line-height:1.95;font-size:18px}.lead{color:#597078;max-width:650px}.hero{display:grid;grid-template-columns:1.1fr 1fr;gap:60px;align-items:center;min-height:480px}.mathhero{font-family:Georgia,"SimSun",serif;background:#eaf5f2;padding:65px 28px;font-size:clamp(27px,3vw,40px);line-height:2.4;border-left:5px solid #168b7a}.mathhero strong{color:#087a70}.links{margin-top:60px}.entry{display:grid;grid-template-columns:70px 220px 1fr;align-items:center;border-top:1px solid #dce7e5;padding:24px 0;gap:15px}.entry:last-child{border-bottom:1px solid #dce7e5}.entry span{color:#168b7a}.entry h2{margin:0}.entry p{margin:0;color:#597078}button,.button{display:inline-block;background:#143f42;color:white;border:0;padding:12px 20px;font:inherit;cursor:pointer;border-radius:4px}button:hover,.button:hover{background:#087a70;color:#fff}button:disabled{opacity:.35;cursor:default}button:focus-visible,a:focus-visible{outline:3px solid #d29b20;outline-offset:4px}.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:20px 0}.tools label{display:flex;align-items:center;gap:8px}.reading{max-width:850px}.reading h2{margin-top:45px}.reading p{white-space:pre-line}.reading table{border-collapse:collapse;width:100%;line-height:1.8}.reading td,.reading th{border:1px solid #ccdcd8;padding:10px;text-align:left}.reading section{border-top:1px solid #e2eae7;padding-top:20px;margin:28px 0}.stage{background:#f1f5f4;position:relative;display:flex;align-items:center;justify-content:center;aspect-ratio:16/9}.stage img{width:100%;height:100%;object-fit:contain}.stage:fullscreen{background:white;width:100vw;height:100vh;aspect-ratio:auto}.stage:fullscreen img{object-fit:contain}.slide-main{max-width:1450px;padding-top:28px}.board{background:#123b32;aspect-ratio:16/9}.board svg{width:100%;height:100%}.board:fullscreen{width:100vw;height:100vh;aspect-ratio:auto;display:flex;align-items:center}.board:fullscreen svg{max-height:100vh}.muted{color:#597078;font-size:15px}details{margin:25px 0;line-height:1.8}footer{padding:28px 5vw;color:#647a7c;font-size:13px;border-top:1px solid #e1e9e8}.hide-controls nav,.hide-controls .tools,.hide-controls footer,.hide-controls h1{display:none}.hide-controls main{padding:0;max-width:none}.hide-controls .stage{height:100vh;aspect-ratio:auto}.hide-controls img{object-fit:contain}@media(max-width:700px){nav{align-items:flex-start;padding:18px;flex-direction:column}nav div{gap:20px;font-size:14px}main{padding:30px 18px}.hero{grid-template-columns:1fr;gap:22px;min-height:auto}.mathhero{padding:25px}.entry{grid-template-columns:35px 1fr}.entry p{grid-column:2}h1{letter-spacing:0}.tools button{padding:10px 13px;font-size:14px}.reading table{font-size:13px}}@media print{nav,footer,.tools,.muted,details{display:none!important}main{padding:0;max-width:none}.reading{font-size:11pt}.reading p,.reading li{font-size:11pt;line-height:1.6}.reading h1{font-size:24pt}.board{width:100%;print-color-adjust:exact;-webkit-print-color-adjust:exact}.board [data-step]{visibility:visible!important}h2,section{break-inside:avoid}body{color:#102e3b}.hero{min-height:0}}''')
put(pathlib.Path('index.html'),page('教学资料','''<main><div class="hero"><div><h1>因式分解<br>提公因式法入门</h1><p class="lead">把熟悉的乘法分配律反过来使用。用一道例题，理解公因式、括号里的每一项，以及展开检验。</p><p class="muted">七年级 · 10分钟无生试讲</p><a class="button" href="slides.html">开始课堂演示</a></div><div class="mathhero">6x²＋9x<br>＝<strong>3x</strong>(2x＋3)<div style="font-size:17px">提取共同部分，乘回确认结果</div></div></div><div class="links"><a class="entry" href="script.html"><span>01</span><h2>逐字稿</h2><p>600秒授课节奏，含停顿、提问与板书提示。</p></a><a class="entry" href="board.html"><span>02</span><h2>板书设计</h2><p>按课堂顺序逐步呈现，保留完整推导。</p></a><a class="entry" href="slides.html"><span>03</span><h2>演示文稿</h2><p>15个整图画面，含独立选做作业。</p></a><a class="entry" href="lesson.html"><span>04</span><h2>教学设计</h2><p>目标、活动与检测对应，附教学意图。</p></a></div></main>'''))
def markdown(s):
 lines=s.splitlines();out=[];table=False
 for l in lines:
  if l.startswith('|'):
   if re.match(r'^\|[\s:|\-]+$',l):continue
   if not table:out.append('<table>');table=True
   out.append('<tr>'+''.join('<td>'+esc(x.strip())+'</td>' for x in l.strip('|').split('|'))+'</tr>');continue
  if table:out.append('</table>');table=False
  if l.startswith('# '):out.append('<h1>'+esc(l[2:])+'</h1>')
  elif l.startswith('## '):out.append('<h2>'+esc(l[3:])+'</h2>')
  elif l.strip():out.append('<p>'+esc(l)+'</p>')
 if table:out.append('</table>')
 return ''.join(out)
for target,src in [('script','L01-script'),('lesson','L01-lesson-plan')]:
 source=staging/f'{src}.md' if staging and (staging/f'{src}.md').is_file() else R/f'lesson-plans/{src}.md'
 md=source.read_text(encoding='utf-8');shutil.copy2(source,D/f'{src}.md')
 put(pathlib.Path(target+'.html'),page('逐字稿' if target=='script' else '教学设计','<main class="reading"><div class="tools"><button onclick="window.print()">打印</button><a class="button" download href="'+src+'.md">下载Markdown</a></div>'+markdown(md)+'</main>'))
player_pages = [{key: p[key] for key in ('page_id', 'title', 'text', 'seconds', 'script')} for p in pages]
put(pathlib.Path('assets/lesson-data.js'),'window.LESSON='+json.dumps(player_pages,ensure_ascii=False)+';')
put(pathlib.Path('slides.html'),page('演示文稿','''<main class="slide-main"><h1 style="font-size:30px">课堂演示</h1><div class="stage" id="stage"><img id="slide" alt=""></div><div class="tools"><button id="prev">上一页</button><button id="next">下一页</button><span id="counter" aria-live="polite"></span><button id="full">全屏</button><button id="hide">隐藏控件（H恢复）</button><a class="button" href="L01-课件.pptx" download>下载PPTX</a></div><p class="muted">方向键翻页，Home/End跳转，F全屏，H切换控件。教师提示默认收起。</p><details><summary>教师提示</summary><p id="notes"></p></details></main><script src="assets/lesson-data.js"></script>''','slides.js'))
put(pathlib.Path('assets/slides.js'),'''let i=0;const $=s=>document.querySelector(s);function show(){const p=LESSON[i];$('#slide').src='assets/slides/'+p.page_id+'.png';$('#slide').alt=p.title+'：'+p.text.join('；');$('#notes').textContent=p.script;$('#counter').textContent=(i+1)+' / '+LESSON.length+' · '+p.seconds+'秒';$('#prev').disabled=i===0;$('#next').disabled=i===LESSON.length-1}function move(n){i=Math.max(0,Math.min(LESSON.length-1,i+n));show()}$('#prev').onclick=()=>move(-1);$('#next').onclick=()=>move(1);$('#full').onclick=()=>$('#stage').requestFullscreen?.();$('#hide').onclick=()=>document.body.classList.toggle('hide-controls');document.addEventListener('keydown',e=>{if(['ArrowRight',' ','ArrowLeft','Home','End'].includes(e.key))e.preventDefault();if(e.key==='ArrowRight'||e.key===' ')move(1);if(e.key==='ArrowLeft')move(-1);if(e.key==='Home'){i=0;show()}if(e.key==='End'){i=LESSON.length-1;show()}if(e.key.toLowerCase()==='h')document.body.classList.toggle('hide-controls');if(e.key.toLowerCase()==='f')$('#stage').requestFullscreen?.()});show();''')
items=[(65,175,'概念与依据',1,True),(65,240,'ab＋ac＝a(b＋c)',1,False),(65,300,'多项式 → 整式的积',1,False),(65,360,'依据：乘法分配律',1,False),(480,175,'例题 E03',2,True),(480,235,'6x²＋9x',2,False),(480,295,'公因式：3x',3,True),(480,355,'＝3x·2x＋3x·3',4,False),(480,415,'＝3x(2x＋3)',5,True),(480,485,'检验：展开还原原式',6,False),(1010,175,'辨析 E04',7,True),(1010,235,'3x²＋3x',7,False),(1010,295,'＝3x(x＋1)',8,True),(1010,355,'3x＝3x·1',8,False),(1010,435,'检测 E05',9,True),(1010,495,'8a²－12a',9,False),(1010,555,'＝4a(2a－3)',10,True),(65,680,'找公因式　→　逐项确定商式　→　乘回检验',11,True)]
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 800" role="img" aria-label="提公因式法板书"><rect width="1500" height="800" fill="#123b32"/><text x="65" y="85" fill="#fff8df" font-size="47" font-family="SimSun,serif">因式分解——提公因式法</text><path d="M65 115H1435M440 155V595M970 155V595M65 625H1435" fill="none" stroke="#8db9a3" stroke-width="2"/>'
for x,y,s,step,accent in items:svg+=f'<text data-step="{step}" x="{x}" y="{y}" fill="{"#f5d676" if accent else "#f2f7ef"}" font-size="{32 if y!=680 else 38}" font-family="Times New Roman,SimSun,serif">{esc(s)}</text>'
svg+='</svg>'
if not staging:
 (R/'board-design/L01-board.svg').write_text(svg,encoding='utf-8',newline='\n')
put(pathlib.Path('assets/L01-board.svg'),svg)
put(pathlib.Path('board.html'),page('板书设计','<main class="slide-main"><h1 style="font-size:30px">板书设计</h1><div class="board" id="board">'+svg+'</div><div class="tools"><button id="back">上一步</button><button id="forward">下一步</button><button id="reset">重置</button><button id="end">终局</button><span id="step" aria-live="polite"></span><button id="full">全屏</button><button onclick="window.print()">打印终局</button><a class="button" href="assets/L01-board.svg" download>下载SVG</a></div><p class="muted">方向键推进或回退；板书动作计入课堂600秒。打印自动显示终局。</p></main>','board.js'))
put(pathlib.Path('assets/board.js'),'''let n=0;const $=s=>document.querySelector(s);function show(){document.querySelectorAll('[data-step]').forEach(e=>e.style.visibility=+e.dataset.step<=n?'visible':'hidden');$('#step').textContent=n+' / 11';$('#back').disabled=n===0;$('#forward').disabled=n===11}function move(d){n=Math.min(11,Math.max(0,n+d));show()}$('#back').onclick=()=>move(-1);$('#forward').onclick=()=>move(1);$('#reset').onclick=()=>{n=0;show()};$('#end').onclick=()=>{n=11;show()};$('#full').onclick=()=>$('#board').requestFullscreen?.();document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();move(1)}if(e.key==='ArrowLeft'){e.preventDefault();move(-1)}});show();''')
for p in pages:
 src=image_paths.get(p['page_id'],R/f"assets/slides/{p['page_id']}.png")
 shutil.copy2(src,D/'assets/slides'/f"{p['page_id']}.png")
pptx=staging/'deck.pptx' if staging else R/'outputs/L01-课件.pptx'
if staging or pptx.exists():shutil.copy2(pptx,D/'L01-课件.pptx')
put(pathlib.Path('.nojekyll'),'')
shutil.copy2(R/'llms.txt',D/'llms.txt')
print('Static site built, local scripts and relative paths only')
