import json
from datetime import datetime

# 读取FireCrawl导出的JSON
with open('pelosi.json', 'r') as f:
    data = json.load(f)

# 创建Markdown文档的开头部分
markdown_content = f"""# Nancy Pelosi's Trading Activity

## Overview
- Data Source: CapitolTrades.com
- Politician: Nancy Pelosi (Former Speaker of the House)
- Collection Date: {datetime.now().strftime('%Y-%m-%d')}

## Recent Trades

"""

# 处理JSON中的每个元素
for item in data:
    # 从markdown字段获取内容
    trade_content = item.get('markdown', '')

    # 从metadata获取额外信息
    metadata = item.get('metadata', {})

    # 添加元数据信息（如果有）
    url = metadata.get('sourceURL', 'Unknown source')
    scrape_time = metadata.get('scrapeTime', datetime.now().strftime('%Y-%m-%d'))

    # 将提取的交易数据添加到markdown内容中
    markdown_content += trade_content + "\n\n"
    markdown_content += f"Source: {url}\n"
    markdown_content += f"Collected on: {scrape_time}\n\n"
    markdown_content += "---\n\n"  # 分隔符

# 添加背景信息
markdown_content += """
## Context on Congressional Trading

Members of Congress are required to disclose their financial trades under the STOCK Act. 
These disclosures provide insight into potential conflicts of interest and investment 
strategies of lawmakers who may have access to non-public information through their 
positions on congressional committees.

Nancy Pelosi's trades, particularly those made by her husband Paul Pelosi, have 
received significant attention from retail investors and media outlets due to their 
timing and performance.
"""

# 保存为Markdown文件
with open('pelosi_trades.md', 'w') as f:
    f.write(markdown_content)

print("成功创建Nancy Pelosi交易数据的Markdown文件")