# -*- coding: utf-8 -*-
"""
测试脚本 - 验证HTML生成功能
"""
import json
from app import generate_html

# 加载示例数据
with open('example_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 生成HTML
html_content = generate_html(data)

# 保存HTML
output_file = 'test_output.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("[OK] HTML生成成功！")
print(f"输出文件: {output_file}")
print(f"文件大小: {len(html_content)} 字符")

# 验证关键内容
print("\n验证关键内容:")
checks = [
    ('标题', '综合诉讼维权中心周报' in html_content),
    ('负责人头像', 'pem5wgP.jpg' in html_content),  # kevin的头像
    ('案件进展', '案件进展' in html_content),
    ('后续安排', '后续安排' in html_content),
    ('CSS样式', '.header {' in html_content),
    ('数据卡片', 'metric-value' in html_content),
]

for name, result in checks:
    status = "[OK]" if result else "[FAIL]"
    print(f"  {status} {name}")

print("\n测试完成！")
