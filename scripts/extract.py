# -*- coding: utf-8 -*-
"""
C1 翻译管线 · 第 1 步：正文提取
作用：把离线缓存的 HTML 文章，抽成干净的纯文本/markdown，供下一步翻译。
可复跑：python extract.py 即可重复执行，同样输入永远同样输出。
"""
import os
import re
import html
from html.parser import HTMLParser

# 输入：离线缓存的 pages 目录
SRC_DIR = r"C:\Users\14724\Desktop\我的挑战\挑战_C1 课程资料获取与翻译_pxzwy0_完整资料\materials\CS146S_offline\CS146S_offline\pages"
# 输出：抽取后的纯文本目录
OUT_DIR = r"C:\Users\14724\Desktop\C1_翻译项目\source"

# 需要整块跳过的非正文标签
SKIP_TAGS = {"script", "style", "noscript", "nav", "header", "footer",
             "aside", "form", "button", "svg", "iframe"}
# 标题标签（保留为 markdown 标题）
HEADING = {"h1": "# ", "h2": "## ", "h3": "### ",
           "h4": "#### ", "h5": "##### ", "h6": "###### "}


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.out = []
        self.cur = []
        self.in_heading = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in HEADING:
            self.in_heading = HEADING[tag]
        if tag == "br":
            self.cur.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if tag in HEADING:
            self.flush(self.in_heading or "")
            self.in_heading = None
        elif tag in ("p", "div", "li", "blockquote", "tr", "section", "article"):
            self.flush("")

    def handle_data(self, data):
        if self.skip_depth:
            return
        self.cur.append(data)

    def flush(self, prefix):
        text = "".join(self.cur)
        self.cur = []
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            self.out.append(prefix + text)


def extract(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    ex = Extractor()
    ex.feed(raw)
    body = "\n\n".join(ex.out)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    report = []
    for name in sorted(os.listdir(SRC_DIR)):
        if not name.endswith(".html"):
            continue
        body = extract(os.path.join(SRC_DIR, name))
        stem = name[:-5]
        out_path = os.path.join(OUT_DIR, stem + ".md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(body)
        report.append((stem, len(body)))
    # 输出清单，按字数排序
    report.sort(key=lambda x: -x[1])
    print("已提取文件清单（按正文字数降序）：")
    for stem, n in report:
        flag = "  <-- 空壳/缺正文" if n < 500 else ""
        print(f"{stem:45} {n:6} 字{flag}")


if __name__ == "__main__":
    main()
