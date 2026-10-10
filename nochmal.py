import json,urllib.request,urllib.error,subprocess,time
def envval(k):
    for line in open('/opt/data/.env',encoding='utf-8',errors='replace'):
        line=line.strip()
        if line.startswith(k+'='): return line.split('=',1)[1].strip().strip('"').strip("'")
K=envval('GITHUB_TOKEN') or envval('GITHUB_PAT')
H={'Authorization':'Bearer '+K,'Accept':'application/vnd.github+json','User-Agent':'hermes'}
def api(path, method='GET', body=None):
    r=urllib.request.Request('https://api.github.com'+path, method=method, headers=H,
        data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(r) as f:
            raw=f.read().decode(); return f.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:300]
def run(cmd, mask=()):
    p=subprocess.run(cmd, cwd='/opt/data/cache/scratch/wick', shell=isinstance(cmd,str), capture_output=True, text=True)
    out=(p.stdout+p.stderr)
    for m in mask: out=out.replace(m,'[SCHLUESSEL]')
    return p.returncode, out.strip()
run(['git','add','-A'])
c,s=run(['git','-c','user.name=Hermes','-c','user.email=hermes@n0ne.de','commit','-q','-m',
  'Fehler behoben: der Bau ist EINE Zeile — sed /muster/d loeschte die ganze Startseite; jetzt wird nur das Script-Element entfernt, mit Grossen- und Inhaltsschranken'])
print('commit rc=%d'%c, s[:200])
url='https://x-access-token:%s@github.com/mekotools/wick-editor.git'%K
c,s=run(['git','push','-q',url,'main'], mask=[K]); print('push rc=%d'%c, s[:200])
s,r=api('/repos/mekotools/wick-editor/actions/workflows/bau.yml/dispatches','POST',
        {"ref":"main","inputs":{"quelle_commit":"b24d0de01006e3ce14ebfd7c3a6155b26d3126c7","tag":"1.19.3"}})
print('Anstoss:', s)
for i in range(30):
    time.sleep(12)
    s,runs=api('/repos/mekotools/wick-editor/actions/runs?per_page=1')
    w=runs['workflow_runs'][0]
    if w['status']=='completed':
        print('Lauf', w['id'], w['conclusion'])
        s,j=api('/repos/mekotools/wick-editor/actions/runs/%d/jobs'%w['id'])
        for job in j.get('jobs',[]):
            for st in job.get('steps',[]): print('   %-48s %s'%(st['name'],st['conclusion']))
        open('/tmp/wick/run_id2.txt','w').write(str(w['id']))
        break
    print('  ', i, w['status'])
else: print('noch nicht fertig')
