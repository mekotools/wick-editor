import json,urllib.request,hashlib
def get(url, headers=None):
    r=urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(r) as f: return dict(f.headers), f.read()
ACC=('application/vnd.oci.image.manifest.v1+json,'
     'application/vnd.docker.distribution.manifest.v2+json')
h,b=get('https://ghcr.io/token?service=ghcr.io&scope=repository:mekotools/wick-editor:pull')
tok=json.loads(b)['token']
h,b=get('https://ghcr.io/v2/mekotools/wick-editor/manifests/latest',{'Authorization':'Bearer '+tok,'Accept':ACC})
d='sha256:'+hashlib.sha256(b).hexdigest()
man=json.loads(b)
print('Verdauungswert (aus dem Manifest gerechnet):', d)
print('Inhaltstyp:', man.get('mediaType'))
print('Schichten:', len(man.get('layers',[])), '| Groesse:', round(sum(x['size'] for x in man['layers'])/1048576,1), 'MB')
print('config.digest:', man.get('config',{}).get('digest'))
print('config.size:', man.get('config',{}).get('size'))
open('/tmp/wick/digest.txt','w').write(d)
# Gegenprobe: laesst sich genau dieser Verdauungswert anonym abrufen?
h2,b2=get('https://ghcr.io/v2/mekotools/wick-editor/manifests/'+d,{'Authorization':'Bearer '+tok,'Accept':ACC})
print('Abruf ueber den Verdauungswert:', 'ok' if b2==b else 'ABWEICHUNG')
