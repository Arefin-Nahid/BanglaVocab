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
        '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%279%27 fill=%27%236fbf9d%27/%3E%3Cpath d=%27M7.5 10.5c2.7-1.1 5.3-.8 8.5 1.1 3.2-1.9 5.8-2.2 8.5-1.1v11.2c-2.7-1.1-5.3-.8-8.5 1.1-3.2-1.9-5.8-2.2-8.5-1.1zM16 11.6v11.2%27 fill=%27none%27 stroke=%27%23052d20%27 stroke-width=%271.9%27 stroke-linejoin=%27round%27/%3E%3C/svg%3E">\n'
        '<meta name="theme-color" media="(prefers-color-scheme: light)" content="#fafcfa">\n'
        '<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#161616">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
        '<meta name="mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-title" content="শব্দভাণ্ডার">\n'
        '<style>html{padding:env(safe-area-inset-top,0) 0 env(safe-area-inset-bottom,0);color-scheme:light}'
        'body{margin:0;font:14px system-ui,sans-serif}[hidden]{display:none!important}img{max-width:100%}</style>\n</head>\n<body>\n')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(head + body + '\n<script>if("serviceWorker" in navigator&&/^https?:/.test(location.protocol)){addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){});});}</script>\n</body>\n</html>\n')
print('wrote index.html', len(head + body), 'bytes')
