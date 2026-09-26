import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
s = r'C:\Users\14724\Desktop\C1_翻译项目\source'
t = r'C:\Users\14724\Desktop\C1_翻译项目\translated'
files = ['ai-code-review-best-practices.md','mcp-food-for-thought.md',
         'kubernetes-troubleshooting-ai.md','code-review-essentials.md']
for f in files:
    src = open(os.path.join(s, f), encoding='utf-8', errors='replace').read()
    tr = open(os.path.join(t, f), encoding='utf-8', errors='replace').read()
    sh = re.findall(r'^#{1,4} .*', src, re.M)
    th = re.findall(r'^#{1,4} .*', tr, re.M)
    print('=== ' + f + ' ===')
    print('SOURCE headings (%d):' % len(sh))
    for h in sh: print('   S| ' + h.strip())
    print('TRANS headings (%d):' % len(th))
    for h in th: print('   T| ' + h.strip())
    print()
