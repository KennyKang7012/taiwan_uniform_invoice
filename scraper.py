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
            
            # 標準化獎項名稱
            if "特別獎" in title: title = "特別獎"
            elif "特獎" in title: title = "特獎"
            elif "頭獎" in title: title = "頭獎"
            elif "二獎" in title: title = "二獎"
            elif "三獎" in title: title = "三獎"
            elif "四獎" in title: title = "四獎"
            elif "五獎" in title: title = "五獎"
            elif "六獎" in title: title = "六獎"
            elif "增開六獎" in title: title = "增開六獎"

            # 抓取包含號碼的文字
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
    
    # 動態計算年份 (民國年)
    from datetime import datetime
    current_year = datetime.now().year - 1911
    recent_years = [str(current_year), str(current_year - 1)]
    print(f"  目標年份: {recent_years}")
    
    # 爬取前幾頁以涵蓋兩年
    for page in range(1, 6):
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
                    
                # 規則：只擷取序號為偶數的內容 (一般中獎號碼)
                if seq % 2 == 0:
                    a_tag = td_content.find('a')
                    if not a_tag:
                        continue
                        
                    period_title = a_tag.get_text(strip=True)
                    if period_title in seen_periods:
                        continue
                        
                    # 檢查是否為近兩年內
                    is_recent = any(y in period_title for y in recent_years)
                    if not is_recent:
                        # 額外檢查跨年期別 (如 113年 12 ~ 114年 01)
                        # 但通常清冊會標註 114年 01-02月，所以 is_recent 應該夠
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

    # 排序：年份與月份降序 (最新在前)
    # period 格式通常為 "114年09-10月"
    def sort_key(item):
        import re
        match = re.search(r'(\d+)年\s*(\d+)', item['period'])
        if match:
            return int(match.group(1)) * 100 + int(match.group(2))
        return 0
    
    all_data.sort(key=sort_key, reverse=True)

    # 儲存資料
    print(f"正在將 {len(all_data)} 筆期別資料寫入 data.json...")
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"爬取完成！最終共收集 {len(all_data)} 筆有效資料")

if __name__ == "__main__":
    main()
