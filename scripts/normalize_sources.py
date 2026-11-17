"""Keep source hashes stable across Git's LF checkout policy."""
import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
for file in (R/'slides/prompts').glob('*.md'):
 file.write_bytes(file.read_bytes().replace(b'\r\n',b'\n'))
for name in ['manifest.json','manifest.delivered.json']:
 p=R/'slides'/name;m=json.loads(p.read_text(encoding='utf-8'))
 for page in m['pages']:
  for c in page['candidates']:
   c['prompt']['sha256']=hashlib.sha256((R/c['prompt']['path']).read_bytes()).hexdigest()
 p.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
for file in (R/'scripts').glob('*.py'):
 if file.name=='normalize_sources.py':continue
 s=file.read_text(encoding='utf-8');s=s.replace(",encoding='utf-8')",",encoding='utf-8',newline='\\n')")
 file.write_text(s,encoding='utf-8',newline='\n')
print('Prompt hashes normalized for LF checkouts')
