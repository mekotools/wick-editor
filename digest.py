import json,urllib.request,urllib.error
def get(url, headers=None, method='GET'):
    r=urllib.request.Request(url, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(r) as f: return f.status, dict(f.headers), f.read()
    except urllib.error.HTTPError as e: return e.code, dict(e.headers), e.read()
ACC=('application/vnd.oci.image.index.v1+json,'
     'application/vnd.oci.image.manifest.v1+json,'
     'application/vnd.docker.distribution.manifest.list.v2+json,'
     'application/vnd.docker.distribution.manifest.v2+json')
s,h,b=get('https://ghcr.io/token?service=ghcr.io&scope=repository:mekotools/wick-editor:pull')
print('Marke holen:', s)
tok=json.loads(b)['token']
print('anonyme Marke erhalten:', bool(tok))
s,h,b=get('https://ghcr.io/v2/mekotools/wick-editor/manifests/latest',
          {'Authorization':'Bearer '+tok,'Accept':ACC})
print('Manifest anonym:', s, h.get('Content-Type'))
dig=h.get('Docker-Content-Digest')
print('Index-Verdauungswert:', dig)
man=json.loads(b)
print('Typ:', man.get('mediaType'))
if 'manifests' in man:
    for m in man['manifests']:
        print('  Plattform', m.get('platform'), '->', m['digest'])
        s2,h2,b2=get('https://ghcr.io/v2/mekotools/wick-editor/manifests/'+m['digest'],
                     {'Authorization':'Bearer '+tok,'Accept':ACC})
        im=json.loads(b2)
        schichten=im.get('layers',[])
        print('   Schichten:', len(schichten), '| Gesamt:', round(sum(x['size'] for x in schichten)/1048576,1),'MB')
        print('   config.digest:', im.get('config',{}).get('digest'))
        open('/tmp/wick/sha_linux_amd64.txt','w').write(m['digest'])
