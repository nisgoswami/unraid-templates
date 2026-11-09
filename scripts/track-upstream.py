"""Track the official published image without importing application configuration."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
IMAGE = 'maximhq/bifrost:latest'

def fetch(url, headers=None):
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=60) as response:
        return response.read(), response.headers

def main():
    token_data, _ = fetch('https://auth.docker.io/token?service=registry.docker.io&scope=repository:maximhq/bifrost:pull')
    token = json.loads(token_data)['token']
    body, headers = fetch('https://registry-1.docker.io/v2/maximhq/bifrost/manifests/latest', {
        'Authorization': 'Bearer ' + token,
        'Accept': ', '.join(['application/vnd.oci.image.index.v1+json', 'application/vnd.docker.distribution.manifest.list.v2+json', 'application/vnd.oci.image.manifest.v1+json', 'application/vnd.docker.distribution.manifest.v2+json']),
    })
    digest = headers.get('Docker-Content-Digest', '')
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', digest):
        raise ValueError('Registry returned an invalid image digest')
    if digest != 'sha256:' + hashlib.sha256(body).hexdigest():
        raise ValueError('Manifest does not match registry digest')
    manifest = json.loads(body)
    if manifest.get('schemaVersion') != 2:
        raise ValueError('Unsupported image manifest')
    template = ROOT / 'templates/bifrost-ai-gateway.xml'
    xml = template.read_text()
    root = ET.fromstring(xml)
    if root.findtext('Repository') != IMAGE:
        raise ValueError('Template no longer references the expected official image')
    state = ROOT / 'upstream-image.json'
    if state.exists() and json.loads(state.read_text()).get('digest') == digest:
        print('Official image unchanged:', digest)
        return
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    changes = '<Changes>Official upstream image last detected on ' + now[:10] + ' (UTC).\nImage: ' + IMAGE + '\nDigest: ' + digest + '\nSee https://github.com/maximhq/bifrost/releases for upstream release notes.</Changes>'
    if root.find('Changes') is not None:
        xml = re.sub(r'<Changes>.*?</Changes>', lambda _: changes, xml, count=1, flags=re.S)
    else:
        xml = xml.replace('</Container>', '  ' + changes + '\n</Container>')
    ET.fromstring(xml)
    template.write_text(xml)
    state.write_text(json.dumps({'image': IMAGE, 'digest': digest, 'detected_at': now, 'upstream': 'https://github.com/maximhq/bifrost'}, indent=2) + '\n')
    print('Recorded official published image:', digest)

if __name__ == '__main__':
    main()
