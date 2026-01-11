# 台灣統一發票中獎號碼爬取與靜態網頁系統

一個自動化工具，用於爬取財政部稅務入口網之「統一發票中獎號碼」，並生成一個美觀、互動性佳且支援響應式佈局 (RWD) 的靜態網頁。

![網頁介面預覽](./docs/screenshots/web_preview.png)

## 🌟 特色功能

- **自動化更新 (GitHub Actions)**：設定於每單月 25-27 日自動執行爬取與發布，免去手動更新煩惱。
- **動態年份偵測**：系統自動計算當前民國年份，確保數據永遠包含最新兩年的開獎紀錄。
- **法規集成 UI**：依據法規第 3 條精確呈現「獎金金額」與「中獎號碼位數規則」，查詢更直觀。
- **高品質 UI**：使用現代化漸層設計、Google Fonts 與流暢的切換動畫。
- **響應式佈局**：完美適配手機、平板與桌上型電腦。
- **無後端依賴**：產出純靜態網頁，支援自動化 CI/CD 推送至 GitHub Pages。

## 🛠️ 技術棧

- **語言**：Python 3.12+
- **環境管理**：[uv](https://github.com/astral-sh/uv)
- **爬蟲工具**：Requests, BeautifulSoup4
- **網頁生成**：Jinja2 (模板引擎)
- **前端技術**：Vanilla CSS (CSS Variables), Vanilla JS

## 🚀 快速開始

### 1. 安裝環境
本項目使用 `uv` 進行管理，請確保已安裝 `uv`。
```bash
# 安裝依賴
uv sync
```

### 2. 執行爬取與生成
執行以下指令，系統會自動爬取資料並生成 `index.html`：
```bash
uv run python scraper.py && uv run python generator.py
```

### 3. 查看結果
直接開啟生成的 `index.html` 即可：
```bash
open index.html
```

### 4. 自動化佈署 (GitHub Actions)
本專案已整合 CI/CD 流程，若將代碼推送到 GitHub，系統會：
1. **定時觸發**：每單月 25, 26, 27 號下午 4 點 (UTC+8) 自動更新。
2. **手動觸發**：在 GitHub Actions 頁面點擊 "Run workflow" 即可立即爬取。

## 📂 檔案結構

- `scraper.py`: 爬蟲核心邏輯，負責抓取並存儲資料為 `data.json`。
- `generator.py`: 網頁產生器，將資料注入 HTML 模板。
- `index.css`: 現代化網頁樣式表。
- `docs/`: 存放專案文件。
  - `SRS.md`: 需求規格書。
  - `implementation_plan.md`: 實作計畫。
  - `walkthrough.md`: 成果報告與疑難排解紀錄。

## 📝 開發筆記
詳細的開發挑戰（如編碼問題、DOM 結構處理）與解決方案，請參閱 [docs/walkthrough.md](./docs/walkthrough.md)。

## ⚠️ 免責聲明與授權事項

1. **僅供參考**：本專案僅供開發與練習使用，所抓取之中獎號碼資料均來自於財政部稅務入口網。實際中獎號碼請以「[財政部稅務入口網](https://www.etax.nat.gov.tw)」或「財政部公告之新聞紙」為準。
2. **法律合規**：使用者應遵守中華民國相關法律規範（如《加值型及非加值型營業稅法》及相關行政執行規範）。本專案不對因使用此工具所產生的任何錯誤、遺漏或金錢損失負責。
3. **授權建議**：若欲將此專案之程式碼用於商業用途或公開部署，請確保遵循開源授權規範（本專案建議使用 MIT License 或同等授權）。

---
*資料來源：[財政部稅務入口網](https://www.etax.nat.gov.tw)*
