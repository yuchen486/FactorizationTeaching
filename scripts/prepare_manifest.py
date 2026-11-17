"""Record the exact adopted bytes after visual review; prepare official packager input."""
import datetime,hashlib,json,pathlib
from PIL import Image
R=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pages=json.loads((R/'slides/pages.json').read_text(encoding='utf-8'))
native=json.loads((R/'assets/native-generation.json').read_text(encoding='utf-8'))
manifest={'schema_version':1,'project':{'id':'L01','title':'因式分解——提公因式法入门','target_seconds':600,'timing_tolerance_seconds':0,'generation_policy':{'mode':'single_requested','required_lanes':['configured_api','native_imagegen'],'single_lane_reason':'Approved API main with automatic native fallback. API candidates rejected after formula/text inspection.'}},'pages':[]}
for n,p in enumerate(pages,1):
 pid=p['page_id'];source=R/f'assets/slides/{pid}.png';im=Image.open(source);im.verify();im=Image.open(source)
 assert abs(im.width/im.height-16/9)/(16/9)<.002,(pid,im.size)
 prompt=f'slides/prompts/{pid}-native-v1.md';(R/prompt).write_text(native[pid]['prompt'],encoding='utf-8',newline='\n')
 notes=f"{p['title']}｜预算{p['seconds']}秒。\n{p['script']}\n本画面文字："+'；'.join(p['text'])+'\n教材依据：沪科版七下8.4，第80—82页，国家中小学智慧教育平台。'
 c={'id':pid+'-native','project_id':'L01','status':'adopted','path':source.relative_to(R).as_posix(),'sha256':sha(source),'source':{'kind':'native_imagegen','reference':native[pid]['path']},'prompt':{'path':prompt,'version':'native-v1','sha256':sha(R/prompt)},'quality':{'rating':'accept','reason':'逐字目视检查中文、公式、符号、画幅与清晰度'},'dimensions':{'width_px':im.width,'height_px':im.height}}
 manifest['pages'].append({'page_number':n,'page_id':pid,'project_id':'L01','status':'adopted','topic':p['title'],'visible_text':[p['title']]+p['text'],'evidence':[{'reference':'exercises/L01-exercises.md','supports':'原创题目、答案及数学检验'}],'candidates':[c],'adopted_candidate_id':c['id'],'qa':{'facts':'passed','text':'passed','visual':'passed'},'speaker':{'seconds':p['seconds'],'keywords':[p['title']],'idea':p['script'],'transition':'进入本环节反馈' if n%2 else '进入下一教学环节' if n<14 else '课堂结束','notes_text':notes}})
(R/'slides/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
cards=['# L01 讲者提示卡\n\n14个状态共600秒，同一环节完整逐字稿只讲一次，按画面内容推进。\n']
for p in pages:cards.append(f"## {p['page_id']} {p['title']} · {p['seconds']}秒\n\n画面："+'；'.join(p['text'])+'\n\n讲述：'+p['script']+'\n')
(R/'outputs/L01-提示卡.md').write_text('\n'.join(cards),encoding='utf-8',newline='\n')
print('Manifest prepared:',sum(p['speaker']['seconds'] for p in manifest['pages']))
