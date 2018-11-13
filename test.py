import re
html = '<dd class="txt">12℃ ~ <b>17</b>℃</dd>'
dr = re.compile(r'<[^>]+>', re.S)
dd = dr.sub('', html)
print(dd)