import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = r'C:\Users\14724\Desktop\C1_翻译项目\source'
t = r'C:\Users\14724\Desktop\C1_翻译项目\translated'
rows = []
for f in sorted(os.listdir(s)):
    tp = os.path.join(t, f)
    if not os.path.exists(tp):
        continue
    src = open(os.path.join(s, f), encoding='utf-8', errors='replace').read()
    tr = open(tp, encoding='utf-8', errors='replace').read()
    hd = len(re.findall(r'^#{1,4} ', src, re.M))
    lnk = src.count('](http')
    ratio = round(len(tr) / len(src) * 100) if src else 0
    rows.append((f, len(src), len(tr), ratio, hd, lnk))
print('file | src_chars | tr_chars | ratio% | src_hd | src_links')
for f, a, b, r, h, l in sorted(rows, key=lambda x: -x[3]):
    print(f'{f} | {a} | {b} | {r}% | {h} | {l}')
