import json
from jinja2 import Template
import os

def main():
    print("正在生成靜態網頁...")
    
    # 讀取爬取的資料
    if not os.path.exists('data.json'):
        print("錯誤: 找不到 data.json，請先執行 scraper.py")
        return
        
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # 獎項說明對照表
    PRIZE_INFO = {
        "特別獎": {"desc": "同期統一發票收執聯 8 位數號碼與中獎號碼完全相同者", "amount": "1,000 萬元"},
        "特獎": {"desc": "同期統一發票收執聯 8 位數號碼與中獎號碼完全相同者", "amount": "200 萬元"},
        "頭獎": {"desc": "同期統一發票收執聯 8 位數號碼與中獎號碼完全相同者", "amount": "20 萬元"},
        "二獎": {"desc": "同期統一發票收執聯末 7 位數號碼與頭獎中獎號碼末 7 位完全相同者", "amount": "4 萬元"},
        "三獎": {"desc": "同期統一發票收執聯末 6 位數號碼與頭獎中獎號碼末 6 位完全相同者", "amount": "1 萬元"},
        "四獎": {"desc": "同期統一發票收執聯末 5 位數號碼與頭獎中獎號碼末 5 位完全相同者", "amount": "4,000 元"},
        "五獎": {"desc": "同期統一發票收執聯末 4 位數號碼與頭獎中獎號碼末 4 位完全相同者", "amount": "1,000 元"},
        "六獎": {"desc": "同期統一發票收執聯末 3 位數號碼與頭獎中獎號碼末 3 位完全相同者", "amount": "200 元"},
        "增開六獎": {"desc": "同期統一發票收執聯末 3 位數號碼與增開六獎中獎號碼完全相同者", "amount": "200 元"}
    }
    
    # 讀取 CSS
    with open('index.css', 'r', encoding='utf-8') as f:
        css_content = f.read()

    # HTML 模板
    html_template = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>台灣統一發票中獎號碼查詢</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        {{ css }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>統一發票中獎號碼</h1>
            <p class="subtitle">自動爬取財政部最新開獎資訊 (依據法規精準顯示)</p>
        </header>

        <div class="period-selector" id="periodSelector">
            {% for item in data %}
            <button class="period-btn {% if loop.first %}active{% endif %}" onclick="showPeriod('{{ loop.index0 }}')">
                {{ item.period }}
            </button>
            {% endfor %}
        </div>

        <div id="winningContent">
            {% for item in data %}
            <div class="winning-card {% if not loop.first %}hidden{% endif %}" id="period-{{ loop.index0 }}">
                <div class="period-header">
                    <h2>{{ item.period }}</h2>
                    <a href="{{ item.url }}" target="_blank" class="official-link">查看官網原文 →</a>
                </div>
                
                <div class="prizes">
                    {% for prize, numbers in item.numbers.items() %}
                    <div class="prize-row {% if prize in ['特別獎', '特獎'] %}special{% endif %}">
                        <div class="prize-info-col">
                            <div class="prize-name">{{ prize }}</div>
                            <div class="prize-amount">{{ prize_info[prize].amount if prize in prize_info else '' }}</div>
                        </div>
                        <div class="number-list">
                            <div class="win-number-wrap">
                                {% for num in numbers %}
                                <div class="win-number">{{ num }}</div>
                                {% endfor %}
                            </div>
                            <div class="prize-desc">{{ prize_info[prize].desc if prize in prize_info else '' }}</div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>

        <footer>
            <p>© 2026 統一發票中獎號碼自動更新系統 | 資料來源：財政部稅務入口網</p>
            <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 5px;">最後更新：{{ last_updated }}</p>
        </footer>
    </div>

    <script>
        function showPeriod(index) {
            const btns = document.querySelectorAll('.period-btn');
            btns.forEach((btn, i) => {
                if (i == index) btn.classList.add('active');
                else btn.classList.remove('active');
            });

            const cards = document.querySelectorAll('.winning-card');
            cards.forEach((card, i) => {
                if (i == index) card.classList.remove('hidden');
                else card.classList.add('hidden');
            });
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>
    """

    # 渲染模板
    from datetime import datetime
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    template = Template(html_template)
    rendered_html = template.render(
        data=data, 
        css=css_content, 
        prize_info=PRIZE_INFO,
        last_updated=last_updated
    )

    # 儲存為 index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    print("生成完成！請開啟 index.html 查看結果。")

if __name__ == "__main__":
    main()
