import json,urllib.request,urllib.error,time
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

s,r=api('/repos/mekotools/wick-editor/actions/workflows/bau.yml/dispatches','POST',
        {"ref":"main","inputs":{"quelle_commit":"b24d0de01006e3ce14ebfd7c3a6155b26d3126c7","tag":"1.19.3"}})
print('Anstoss:', s, r if s>=400 else '')
if s>=400: raise SystemExit(1)
time.sleep(8)
rid=None
for i in range(40):
    s,runs=api('/repos/mekotools/wick-editor/actions/runs?per_page=3')
    if isinstance(runs,dict) and runs.get('workflow_runs'):
        w=runs['workflow_runs'][0]
        rid=w['id']
        st=w['status']; cc=w.get('conclusion')
        print('  Lauf %d: %s %s' % (i, st, cc or ''))
        if st=='completed':
            print('Ergebnis:', cc)
            break
    time.sleep(15)
else:
    print('noch nicht fertig')
if rid:
    s,j=api('/repos/mekotools/wick-editor/actions/runs/%d/jobs'%rid)
    if isinstance(j,dict):
        for job in j.get('jobs',[]):
            print('Auftrag:', job['name'], job['conclusion'])
            for st in job.get('steps',[]):
                print('   %-46s %s' % (st['name'], st['conclusion']))
    open('/tmp/wick/run_id.txt','w').write(str(rid))
