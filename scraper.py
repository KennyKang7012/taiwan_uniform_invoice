import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

BASE_URL = "https://www.etax.nat.gov.tw"
# 中獎號碼詳細頁面 URL 格式: ETW183W2_YYMM (民國年+起始月)
DETAIL_URL_TEMPLATE = f"{BASE_URL}/etw-main/ETW183W2_{{yymm}}"

# 統一發票每兩個月一期，起始月份
PERIOD_START_MONTHS = [1, 3, 5, 7, 9, 11]


def get_winning_numbers(detail_url):
    """抓取詳細頁面的中獎號碼（適配新版財政部網站結構）"""
    try:
        response = requests.get(detail_url, timeout=15)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        results = {}
        
        # 新版網站的表格 id 為 "tenMillionsTable"
        table = soup.find('table', id='tenMillionsTable')
        if not table:
            # 向後相容：嘗試舊的 class 匹配
            table = soup.find('table', class_='table')
        if not table:
            return results

        rows = table.find_all('tr')
        for row in rows:
            th = row.find('th', scope='row')
            td = row.find('td')
            if not th or not td:
                continue

            title = th.get_text(strip=True)
            if title in ["序號", "年月份", "獎別", "領獎注意事項"]:
                continue

            # 標準化獎項名稱
            if "特別獎" in title:
                title = "特別獎"
            elif "特獎" in title:
                title = "特獎"
            elif "增開六獎" in title:
                title = "增開六獎"
            elif "頭獎" in title:
                title = "頭獎"
            elif "二獎" in title:
                continue  # 二獎~六獎由頭獎號碼推導，不需抓取
            elif "三獎" in title:
                continue
            elif "四獎" in title:
                continue
            elif "五獎" in title:
                continue
            elif "六獎" in title:
                continue

            # 從 td 中提取號碼
            # 新版結構: td > div.row > div.col-12.mb-3 內含號碼
            number_divs = td.select('div.col-12')
            if number_divs:
                numbers = []
                for div in number_divs:
                    text = div.get_text(strip=True)
                    # 提取 3~8 位數字
                    found = re.findall(r'\b\d{3,8}\b', text)
                    numbers.extend(found)
            else:
                # 備案：直接從 td 文字中提取
                text_content = td.get_text(" ", strip=True)
                numbers = re.findall(r'\b\d{8}\b', text_content)
                if not numbers:
                    potential = re.findall(r'\d+', text_content)
                    numbers = [p for p in potential if 3 <= len(p) <= 8]

            if title and numbers:
                # 去重
                unique_nums = list(dict.fromkeys(numbers))
                results[title] = unique_nums

        # 額外檢查：增開六獎可能在獨立的表格中
        all_tables = soup.find_all('table', class_=re.compile(r'table'))
        for t in all_tables:
            if t == table:
                continue
            for row in t.find_all('tr'):
                th = row.find('th')
                td = row.find('td')
                if th and td and "增開六獎" in th.get_text(strip=True):
                    number_divs = td.select('div.col-12')
                    if number_divs:
                        nums = []
                        for div in number_divs:
                            text = div.get_text(strip=True)
                            found = re.findall(r'\b\d{3,8}\b', text)
                            nums.extend(found)
                    else:
                        text_content = td.get_text(" ", strip=True)
                        nums = re.findall(r'\d{3}', text_content)
                    if nums:
                        results["增開六獎"] = list(dict.fromkeys(nums))

        return results
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {}  # 該期別尚未公告
        print(f"  HTTP 錯誤 {e.response.status_code}: {detail_url}")
        return {}
    except Exception as e:
        print(f"  抓取錯誤 {detail_url}: {e}")
        return {}


def build_period_label(roc_year, month):
    """產生期別標籤，例如 '114年 09 ~ 10 月'"""
    end_month = month + 1
    return f"{roc_year}年 {month:02d} ~ {end_month:02d} 月"


def main():
    print("開始爬取統一發票中獎號碼...")
    all_data = []

    # 動態計算民國年份
    current_year_ad = datetime.now().year
    current_month = datetime.now().month
    current_roc_year = current_year_ad - 1911

    # 產生近兩年的期別 URL（從最新到最舊）
    target_periods = []
    for roc_year in [current_roc_year, current_roc_year - 1]:
        for month in reversed(PERIOD_START_MONTHS):
            yymm = f"{roc_year}{month:02d}"
            url = DETAIL_URL_TEMPLATE.format(yymm=yymm)
            label = build_period_label(roc_year, month)
            target_periods.append({
                "yymm": yymm,
                "url": url,
                "label": label,
                "roc_year": roc_year,
                "month": month
            })

    # 排序：最新的在前
    target_periods.sort(key=lambda x: int(x["yymm"]), reverse=True)

    print(f"  將爬取 {len(target_periods)} 個期別 (民國 {current_roc_year - 1}~{current_roc_year} 年)")

    for period in target_periods:
        print(f"  正在處理: {period['label']}...")
        numbers = get_winning_numbers(period["url"])

        if numbers:
            item = {
                "period": period["label"],
                "numbers": numbers,
                "url": period["url"]
            }
            all_data.append(item)
            prize_names = ", ".join(numbers.keys())
            print(f"    ✓ 成功擷取 {len(numbers)} 個獎項 ({prize_names})")
        else:
            print(f"    ✗ 無資料 (可能尚未公告)")

        time.sleep(0.5)  # 避免過度請求

    # 排序：最新的在前
    all_data.sort(
        key=lambda x: int(re.search(r'(\d+)年\s*(\d+)', x['period']).group(1)) * 100
                       + int(re.search(r'(\d+)年\s*(\d+)', x['period']).group(2))
        if re.search(r'(\d+)年\s*(\d+)', x['period']) else 0,
        reverse=True
    )

    # 儲存資料
    print(f"\n正在將 {len(all_data)} 筆期別資料寫入 data.json...")
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"爬取完成！最終共收集 {len(all_data)} 筆有效資料")


if __name__ == "__main__":
    main()
