#!/usr/bin/env python3
"""Build the standalone site: embeds data/data.json and data/report.json into src/app.template.html
and writes index.html (open it in a browser or host it on GitHub Pages)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda *p: open(os.path.join(ROOT, *p), encoding='utf-8').read()

def safe(s):
    return (json.dumps(json.loads(s), ensure_ascii=False, separators=(',', ':'))
            .replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029'))

body = rd('src', 'app.template.html').replace('__DATA__', safe(rd('data', 'data.json'))).replace('__REPORT__', safe(rd('data', 'report.json')))
head = ('<!doctype html>\n<html lang="bn">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>html{padding:env(safe-area-inset-top,0) 0 env(safe-area-inset-bottom,0);color-scheme:light}'
        'body{margin:0;font:14px system-ui,sans-serif}[hidden]{display:none!important}img{max-width:100%}</style>\n</head>\n<body>\n')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(head + body + '\n</body>\n</html>\n')
print('wrote index.html', len(head + body), 'bytes')
