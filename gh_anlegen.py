import json,urllib.request,urllib.error,subprocess,os,base64

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

s,r=api('/repos/mekotools/wick-editor')
print('vorhanden?', s)
if s==404:
    s,r=api('/orgs/mekotools/repos','POST',{"name":"wick-editor","private":False,
        "description":"MekoTools-Auslieferung von Wick Editor (Animationen und Spiele im Browser; amtlicher Bau, Fremdaufruf entfernt)",
        "has_issues":False,"has_wiki":False,"auto_init":False})
    print('anlegen:', s, r.get('full_name') if isinstance(r,dict) else r)
    if s!=201: raise SystemExit(1)
    import time; time.sleep(4)

# Push ueber git mit Token
url='https://x-access-token:%s@github.com/mekotools/wick-editor.git'%K
def run(cmd, mask=()):
    p=subprocess.run(cmd, cwd='/opt/data/cache/scratch/wick', shell=isinstance(cmd,str), capture_output=True, text=True)
    out=(p.stdout+p.stderr)
    for m in mask: out=out.replace(m,'[SCHLUESSEL]')
    return p.returncode, out.strip()
run(['git','init','-q'])
run(['git','checkout','-q','-b','main'])
run(['git','remote','remove','origin'])
run(['git','remote','add','origin','https://github.com/mekotools/wick-editor.git'])
run(['git','add','-A'])
run(['git','-c','user.name=Hermes','-c','user.email=hermes@n0ne.de','commit','-q','-m',
     'MekoTools-Auslieferung von Wick Editor: amtlicher Bau aus dem Zweig gh-pages, Analyse-Fremdaufruf entfernt'])
c,s=run(['git','push','-q',url,'main'])
print('push rc=%d'%c, s)
c,s=run(['git','remote','set-url','origin','https://github.com/mekotools/wick-editor.git'])
c,ls=run(['git','ls-remote','origin','main']); print('ls-remote:', ls)
