from html.parser import HTMLParser
from pathlib import Path


class PageCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = set()
        self.title = False
        self.inside_title = False

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        if tag == "title":
            self.inside_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.inside_title = False

    def handle_data(self, data):
        if self.inside_title and data.strip():
            self.title = True


page = Path("index.html").read_text(encoding="utf-8")
check = PageCheck()
check.feed(page)
missing = {"html", "head", "body", "main"} - check.tags
if missing or not check.title:
    raise SystemExit(f"网页检查失败：缺少标签 {missing} 或非空标题")
print("网页结构检查通过")
