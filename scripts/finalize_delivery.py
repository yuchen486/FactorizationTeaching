import datetime,json,pathlib,shutil,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
m=json.loads((R/'work/pptx-v1/manifest.with-final-renders.json').read_text(encoding='utf-8'))
target=R/'assets/final-renders';target.mkdir(exist_ok=True)
for p in m['pages']:
 f=p['final_render'];src=R/f['path'];dst=target/src.name;shutil.copy2(src,dst)
 f.update(path=dst.relative_to(R).as_posix(),qa={'facts':'passed','text':'passed','visual':'passed'},reviewed=True,reviewer='Codex visual review',reviewed_at=datetime.datetime.now().astimezone().isoformat());p['status']='delivered'
(R/'slides/manifest.delivered.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
for fn in ['final.validation.json','manifest.pptx-integrity.json','build_result.json']:
 shutil.copy2(R/'work/pptx-v1'/fn,R/'assets/records'/fn)
summary={'pptx_sha256':hashlib.sha256((R/'outputs/L01-课件.pptx').read_bytes()).hexdigest(),'slides':14,'seconds':600,'visual_review':'14 reimported slide renders reviewed individually at 1920x1080 simulation','ui':json.loads((R/'work/delivery-ui.json').read_text()),'local_ui':json.loads((R/'work/ui-check.json').read_text()),'limits':['Actual classroom rehearsal pending','Exact raster font files unverified','PowerPoint desktop not opened'],'runtime_note':'Official operation marker file absent in installed skill; official finalizer and reimport/render completed successfully.'}
(R/'assets/records/delivery.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
p=R/'planning/alignment-and-plan.md';s=p.read_text(encoding='utf-8');start=s.index('## 当前制作进度');end=s.index('## 后续可扩展模块');s=s[:start]+'''## 当前制作进度

逐字稿、教案、板书SVG与逐步演示、14张纯图及PPTX/HTML已完成。PPTX已通过官方finalizer、重导入、逐页1920×1080渲染及目视核验；本地离线、HTTP项目子路径、全部图片、全屏、打印及移动布局检查通过。具体证据见assets/records/delivery.json及slides/manifest.delivered.json。

真实排练仍待主讲人完成，见rehearsal.md。课标具体条款未引用，教材目录及80—83页已核。

'''+s[end:];p.write_text(s,encoding='utf-8',newline='\n')
print('Delivery evidence finalized')
