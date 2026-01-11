import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.etax.nat.gov.tw"
LIST_URL = f"{BASE_URL}/etw-main/ETW183W1/"

def get_winning_numbers(detail_url):
    """抓取詳細頁面的中獎號碼"""
    try:
        response = requests.get(detail_url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = {}
        table = soup.find('table', class_='table')
        if not table:
            return results
            
        rows = table.find_all('tr')
        for row in rows:
            th = row.find('th')
            td = row.find('td')
            if not th or not td:
                continue
                
            title = th.get_text(strip=True)
            if title in ["序號", "年月份", "獎別", "領獎注意事項"]:
                continue

            # 抓取包含號碼的文字
            # 我們尋找 td 內所有內容，並提取看起來像中獎號碼的字串 (通常是 8 位數字)
            # 有些期別可能有多組號碼
            import re
            text_content = td.get_text(" ", strip=True)
            # 尋找所有 8 位數字，或者至少 3 位數字 (領獎金額說明外的數字)
            # 這裡我們主要針對官網呈現紅色部分的數字
            # 但保險起見，我們尋找 td 內所有 8 位連續數字
            numbers = re.findall(r'\b\d{8}\b', text_content)
            
            # 如果是頭獎，可能有多組 8 位數
            # 如果是其他獎，可能是末幾位，但在詳細頁面中，通常特別獎、特獎、頭獎都是 8 位
            if not numbers:
                # 備案：尋找所有數字，排除掉太長的描述
                potential = re.findall(r'\d+', text_content)
                numbers = [p for p in potential if len(p) >= 3 and len(p) <= 8]

            if title and numbers:
                # 排除重複
                unique_nums = []
                for n in numbers:
                    if n not in unique_nums:
                        unique_nums.append(n)
                results[title] = unique_nums
                
        return results
    except Exception as e:
        print(f"Error crawling detail page {detail_url}: {e}")
        return {}

def main():
    print("開始爬取統一發票中獎號碼...")
    all_data = []
    seen_periods = set()
    
    # 爬取前幾頁以涵蓋兩年
    for page in range(1, 5):
        print(f"正在爬取列表第 {page} 頁...")
        url = f"{LIST_URL}?page={page}" if page > 1 else LIST_URL
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', class_='table')
            if not table:
                continue
                
            rows = table.find_all('tr')
            for row in rows:
                th_seq = row.find('th', scope='row')
                td_content = row.find('td')
                if not th_seq or not td_content:
                    continue
                    
                seq_text = th_seq.get_text(strip=True)
                try:
                    seq = int(seq_text)
                except ValueError:
                    continue
                    
                # 規則：只擷取序號為偶數的內容
                if seq % 2 == 0:
                    a_tag = td_content.find('a')
                    if not a_tag:
                        continue
                        
                    period_title = a_tag.get_text(strip=True)
                    if period_title in seen_periods:
                        continue
                        
                    # 限制兩年 (114, 113, 112年11-12月等)
                    # 包含 "114", "113", 或 "112年 11 ~ 12"
                    is_recent = any(y in period_title for y in ["114", "113"]) or "112年 11" in period_title
                    if not is_recent:
                        continue

                    href = a_tag['href'].replace('/etwmain/../', '/')
                    detail_link = BASE_URL + href if not href.startswith('http') else href
                    
                    print(f"  正在處理: {period_title}")
                    numbers = get_winning_numbers(detail_link)
                    
                    if numbers:
                        item = {
                            "period": period_title,
                            "numbers": numbers,
                            "url": detail_link
                        }
                        all_data.append(item)
                        seen_periods.add(period_title)
                        print(f"    成功擷取 {len(numbers)} 個獎項")
                    else:
                        print(f"    警告: 無法在 {period_title} 抓取到號碼")
                    
                    time.sleep(1)
                    
        except Exception as e:
            print(f"爬取錯誤: {e}")

    # 儲存資料
    print(f"正在將 {len(all_data)} 筆期別資料寫入 data.json...")
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"爬取完成！最終共收集 {len(all_data)} 筆有效資料")

if __name__ == "__main__":
    main()
