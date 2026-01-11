# 台灣統一發票中獎號碼爬取與靜態網頁系統

一個自動化工具，用於爬取財政部稅務入口網之「統一發票中獎號碼」，並生成一個美觀、互動性佳且支援響應式佈局 (RWD) 的靜態網頁。

![網頁介面預覽](./docs/screenshots/web_preview.png)

## 🌟 特色功能

- **自動化爬取**：自動獲取最近兩年（目前為 113 至 114 年）的所有已開獎期別。
- **智能過濾**：嚴格遵守規則，僅擷取「一般中獎號碼」（序號為偶數項目），排除中獎清冊。
- **高品質 UI**：使用現代化漸層設計、Google Fonts 與流暢的切換動畫。
- **響應式佈局**：完美適配手機、平板與桌上型電腦。
- **無後端依賴**：產出純靜態網頁，可直接開啟或託管於 GitHub Pages。

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

---
*資料來源：[財政部稅務入口網](https://www.etax.nat.gov.tw)*
