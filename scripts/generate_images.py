"""Approved local gateway adapter. Secrets stay in memory; never enter arguments/logs."""
import base64, concurrent.futures, datetime, hashlib, json, os, pathlib, sqlite3, time, urllib.request, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
def run(page):
    out=ROOT/'assets/slides'/f"{page['page_id']}.png"
    if out.exists(): return
    dbpath=pathlib.Path(os.environ['USERPROFILE'])/'new-api/one-api.db'
    db=sqlite3.connect(f'file:{dbpath.as_posix()}?mode=ro',uri=True)
    row=db.execute("SELECT base_url,key FROM channels WHERE name=?",('openai-next-image',)).fetchone(); db.close()
    if not row: raise RuntimeError('Configured image channel unavailable')
    endpoint,key=row
    prompt=(ROOT/page['prompt_path']).read_text(encoding='utf-8')
    for attempt in range(3):
        start=time.time()
        payload={'model':'gpt-image-2.5','prompt':prompt,'size':'2048x1152','quality':'medium','n':1,'response_format':'b64_json'}
        try:
            config='url = '+json.dumps(endpoint.rstrip('/')+'/v1/images/generations')+'\nheader = '+json.dumps('Authorization: Bearer '+key)+'\nheader = "Content-Type: application/json"\ndata = '+json.dumps(json.dumps(payload,ensure_ascii=False))+'\nsilent\nshow-error\nmax-time = 240\n'
            result=subprocess.run(['curl.exe','--config','-'],input=config.encode(),capture_output=True,timeout=250)
            data=json.loads(result.stdout)
            if 'data' not in data: raise RuntimeError('Upstream returned no image data')
            item=data['data'][0]
            if item.get('b64_json'): raw=base64.b64decode(item['b64_json'])
            else:
                with urllib.request.urlopen(item['url'],timeout=120) as response: raw=response.read()
            out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
            log={'page_id':page['page_id'],'attempt':attempt+1,'seconds':round(time.time()-start,2),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'completed_at':datetime.datetime.now().astimezone().isoformat(),'source':'configured_upstream_api','model_label':'gpt-image-2.5'}
            (ROOT/'assets/records'/f"{page['page_id']}.json").write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
            print(json.dumps(log),flush=True);return
        except Exception as exc:
            print(json.dumps({'page_id':page['page_id'],'attempt':attempt+1,'error_type':type(exc).__name__,'http_status':getattr(exc,'code',None)}),flush=True)
            time.sleep(3*(attempt+1))
    raise RuntimeError('Generation attempts exhausted for '+page['page_id'])
if __name__=='__main__':
    pages=json.loads((ROOT/'slides/pages.json').read_text(encoding='utf-8'))
    (ROOT/'assets/records').mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(run,pages))
