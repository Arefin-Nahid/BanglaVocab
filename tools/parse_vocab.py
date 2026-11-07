#!/usr/bin/env python3
"""Extract every entry from bengali_bcs_vocabulary.md into data.json and verify the extraction
with a second, independent counting pass. Nothing is added, translated or corrected."""
import re, json, collections, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'bengali_bcs_vocabulary.md'
src = open(os.path.join(ROOT, 'source', SRC), encoding='utf-8').read()
lines = src.split('\n')

CATS = [
    dict(id='syn',      tok='১.',   bn='সমার্থক শব্দ',                 en='Synonyms',                      kind='bullet'),
    dict(id='syn2',     tok='১.২',  bn='সমার্থক সারণি (সমোচ্চারিত)',   en='Synonym / near-sound table',    kind='table'),
    dict(id='ant',      tok='২.',   bn='বিপরীতার্থক শব্দ',            en='Antonyms',                      kind='table'),
    dict(id='onew',     tok='৩.',   bn='এক কথায় প্রকাশ',             en='One-word substitution',         kind='table'),
    dict(id='sound',    tok='৩.২',  bn='ডাক ও ধ্বনি',                 en='Calls & sounds',                kind='table'),
    dict(id='idiom',    tok='৪.',   bn='বাগ্‌ধারা',                    en='Idioms & phrases',              kind='table'),
    dict(id='idiomgrp', tok='৪.২',  bn='সমজাতীয় বাগ্‌ধারা',           en='Idiom groups by meaning',       kind='table'),
    dict(id='proverb',  tok='৫.',   bn='প্রবাদ-প্রবচন',                en='Proverbs',                      kind='table'),
    dict(id='term',     tok='৬.',   bn='পারিভাষিক শব্দ',              en='Terminology (English→Bengali)', kind='table'),
]
BY_TOK = {c['tok']: c for c in CATS}

SEP = re.compile(r'^\|[\s:\-|]+\|\s*$')
NOTE = re.compile(r'\s*(?<!\*)\*\((.*?)\)\*(?!\*)')
BULLET = re.compile(r'^- \*\*(.+?)\*\*: (.*)$')

entries, problems = [], []
counters = collections.Counter()
cur, h3 = None, None

def take_notes(s, notes):
    for m in NOTE.finditer(s):
        notes.append(m.group(1))
    return NOTE.sub('', s).strip()

for i, raw in enumerate(lines):
    line = raw.rstrip('\r')
    if line.startswith('## '):
        tok = line[3:].split()[0] if line[3:].split() else ''
        cur = BY_TOK.get(tok)
        h3 = None
        continue
    if line.startswith('### '):
        h3 = line[4:].strip()
        continue
    if cur is None:
        continue
    if cur['kind'] == 'bullet':
        m = BULLET.match(line)
        if not m:
            continue
        notes = []
        word = take_notes(m.group(1), notes)
        rest = take_notes(m.group(2), notes)
        items = [x.strip() for x in rest.split(',') if x.strip()]
        counters[cur['id']] += 1
        e = dict(id=f"{cur['id']}-{counters[cur['id']]:04d}", cat=cur['id'], n=counters[cur['id']],
                 q=word, a=', '.join(items), items=items, group=h3, line=i + 1)
        if notes: e['notes'] = notes
        entries.append(e)
    else:
        if not line.startswith('|') or SEP.match(line):
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if SEP.match(nxt):      # header row
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != 2:
            problems.append(f'line {i+1}: expected 2 cells, got {len(cells)}: {line}')
            continue
        notes = []
        c0 = take_notes(cells[0], notes)
        c1 = take_notes(cells[1], notes)
        counters[cur['id']] += 1
        e = dict(id=f"{cur['id']}-{counters[cur['id']]:04d}", cat=cur['id'], n=counters[cur['id']],
                 group=h3, line=i + 1)
        if cur['id'] == 'idiomgrp':
            e['q'] = c1                       # meaning shown first (recall the idioms)
            e['a'] = c0
            e['items'] = [x.strip() for x in c0.split(',') if x.strip()]
            e['flip'] = True
        else:
            e['q'], e['a'] = c0, c1
        if notes: e['notes'] = notes
        entries.append(e)

# ---------------------------------------------------------------- source-doubt list (from the md's own appendix)
DOUBT = [('syn', '(ধন)'), ('ant', 'কুন্তলা'), ('ant', 'রাম'), ('ant', 'খেদ'), ('idiomgrp', 'ঘন্টা গরুড়'), ('onew', 'চিক্ষমিষা')]
appendix_ok = all(w in src.split('## পরিশিষ্ট')[1] or w == '(ধন)' for _, w in DOUBT[1:]) 
for e in entries:
    txt = e['q'] + ' ' + e['a']
    for cat, w in DOUBT:
        if e['cat'] == cat and (e['q'] == w if cat == 'ant' else w in txt):
            e['unc'] = True
    if e.get('notes'):
        e['unc'] = True

# ---------------------------------------------------------------- independent verification pass
# 1) independent source row counts (different code path: regex over each ## block)
blocks = re.split(r'(?m)^## ', src)
src_counts = collections.Counter()
for b in blocks[1:]:
    head, _, body = b.partition('\n')
    toks = head.split()
    cat = BY_TOK.get(toks[0]) if toks else None
    if not cat:
        continue
    if cat['kind'] == 'bullet':
        src_counts[cat['id']] += len(re.findall(r'(?m)^- \*\*', body))
    else:
        rows = re.findall(r'(?m)^\|.*\|[ \t]*$', body)
        seps = re.findall(r'(?m)^\|[\s:\-|]+\|[ \t]*$', body)
        # header rows = rows immediately before a separator row
        hdrs = len(re.findall(r'(?m)^\|.*\|[ \t]*\n\|[\s:\-|]+\|[ \t]*$', body))
        src_counts[cat['id']] += len(rows) - len(seps) - hdrs

# 2) verbatim / round-trip check against the exact source line
def strip_notes(s): return NOTE.sub('', s)
verified = collections.Counter(); failed = []
for e in entries:
    raw = strip_notes(lines[e['line'] - 1])
    ok = True
    if e['cat'] == 'syn':
        rem = raw.replace('- **', '', 1).replace(e['q'], '', 1).replace('**:', '', 1)
        for it in e['items']:
            if it not in rem: ok = False
            rem = rem.replace(it, '', 1)
        ok = ok and rem.replace(',', '').strip() == '' and e['q'] in raw
    else:
        left, right = (e['a'], e['q']) if e.get('flip') else (e['q'], e['a'])
        rem = raw.replace(left, '', 1).replace(right, '', 1)
        ok = (left in raw) and (right in raw) and rem.replace('|', '').strip() == ''
        if e.get('flip'):
            rem2 = e['a']
            for it in e['items']:
                rem2 = rem2.replace(it, '', 1)
            ok = ok and rem2.replace(',', '').strip() == ''
    if ok: verified[e['cat']] += 1
    else: failed.append(e['id'])

# ---------------------------------------------------------------- anomalies & duplicates (information only, nothing changed)
allcells = []
for e in entries:
    allcells += [(e['cat'], e['q']), (e['cat'], e['a'])]
odd = collections.Counter(); latin_in_bn = []
for cat, s in allcells:
    for ch in s:
        o = ord(ch)
        if 0x0980 <= o <= 0x09FF or ch == ' ' or ch.isdigit():
            continue
        odd[ch] += 1
    if cat != 'term' and re.search(r'[A-Za-z]', s):
        latin_in_bn.append(s)
zwnj = sum(s.count('\u200c') for _, s in allcells)
zwj = sum(s.count('\u200d') for _, s in allcells)
yy_pre = sum(s.count('\u09df') for _, s in allcells)
yy_dec = sum(s.count('\u09af\u09bc') for _, s in allcells)
other_precomp = {n: sum(s.count(ch) for _, s in allcells) for n, ch in [('ড়', '\u09dc'), ('ঢ়', '\u09dd')]}
for ch in list(odd):
    pass

dup_q = collections.defaultdict(list)
for e in entries:
    dup_q[(e['cat'], e['q'])].append(e)
dups = [dict(cat=k[0], q=k[1], ids=[x['id'] for x in v], answers=[x['a'] for x in v], same=len({x['a'] for x in v}) == 1)
        for k, v in dup_q.items() if len(v) > 1]

cat_rows = []
for c in CATS:
    cat_rows.append(dict(id=c['id'], bn=c['bn'], en=c['en'], source_rows=src_counts[c['id']],
                         extracted=counters[c['id']], verified=verified[c['id']],
                         ok=(src_counts[c['id']] == counters[c['id']] == verified[c['id']])))

report = dict(
    source_file=SRC, source_lines=len(lines), categories=cat_rows,
    total_source=sum(src_counts.values()), total_extracted=len(entries), total_verified=sum(verified.values()),
    parse_problems=problems, failed_ids=failed,
    flagged=[dict(id=e['id'], cat=e['cat'], q=e['q'], a=e['a'], line=e['line'], notes=e.get('notes', []))
             for e in entries if e.get('unc')],
    duplicates=dups,
    anomalies=dict(latin_in_bengali_sections=latin_in_bn, zwnj=zwnj, zwj=zwj,
                   precomposed_yy=yy_pre, decomposed_yy=yy_dec, other_precomposed=other_precomp,
                   non_bengali_chars={k: v for k, v in odd.most_common()}),
)

cats_out = [dict(id=c['id'], bn=c['bn'], en=c['en']) for c in CATS]
json.dump(dict(cats=cats_out, entries=entries), open(os.path.join(ROOT, 'data', 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(report, open(os.path.join(ROOT, 'data', 'report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('PROBLEMS:', problems)
print('FAILED:', failed)
for r in cat_rows:
    print(f"{r['id']:9} source={r['source_rows']:4} extracted={r['extracted']:4} verified={r['verified']:4} {'OK' if r['ok'] else 'MISMATCH'}")
print('TOTAL', report['total_source'], report['total_extracted'], report['total_verified'])
print('FLAGGED:', [(f['id'], f['q']) for f in report['flagged']])
print('DUPS:', len(dups), 'same-answer dups:', sum(d['same'] for d in dups))
print('zwnj', zwnj, 'zwj', zwj, 'yy precomposed', yy_pre, 'decomposed', yy_dec, other_precomp)
print('non-bengali chars:', dict(odd))
print('latin in bn sections:', latin_in_bn[:10])
print('appendix names found:', appendix_ok)
