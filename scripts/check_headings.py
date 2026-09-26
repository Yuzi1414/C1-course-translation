import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = r'C:\Users\14724\Desktop\C1_翻译项目\source'
t = r'C:\Users\14724\Desktop\C1_翻译项目\translated'
print('file | src_headings | tr_headings | src_chars | tr_chars')
rows = []
for f in sorted(os.listdir(s)):
    tp = os.path.join(t, f)
    if not os.path.exists(tp):
        continue
    src = open(os.path.join(s, f), encoding='utf-8', errors='replace').read()
    tr = open(tp, encoding='utf-8', errors='replace').read()
    sh = len(re.findall(r'^#{1,4} ', src, re.M))
    th = len(re.findall(r'^#{1,4} ', tr, re.M))
    rows.append((f, sh, th, len(src), len(tr)))
for f, sh, th, a, b in sorted(rows, key=lambda x: x[1] - x[2], reverse=True):
    flag = '  <-- 译文标题明显偏少，疑似漏译' if th < sh * 0.6 else ''
    print(f'{f} | {sh} | {th} | {a} | {b}{flag}')
