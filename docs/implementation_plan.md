# 統一發票爬蟲與靜態網頁生成計畫

本計畫將實作一個 Python 腳本，用於爬取財政部中獎號碼，並生成一個包含所有數據的現代化靜態網頁。

## 使用者評論與確認事項
> [!IMPORTANT]
> - 本計畫將使用 `uv` 作為環境管理工具。
> - 網頁將使用純 HTML/CSS/JS 實作，確保可靜態部署。
> - 爬蟲將嚴格遵守「序號為偶數」的過濾規則。

## 擬議變動

### [爬蟲與資料結構]
實作 Python 爬蟲邏輯。

#### [NEW] `scraper.py`(file:///Users/kennykang/Desktop/VibeProj/Anti/taiwan_uniform_invoice/scraper.py)
- 使用 `requests` 與 `BeautifulSoup4` 爬取列表頁。
- 實作分頁爬取（預計爬取前 2 頁即可涵蓋兩年數據）。
- 爬取詳細頁中所有 `.etw-color-red` 標籤的文字。
- 將結果儲存為 `data.json`。

### [網頁生成與模板]
實作靜態網頁生成邏輯。

#### [NEW] `generator.py`(file:///Users/kennykang/Desktop/VibeProj/Anti/taiwan_uniform_invoice/generator.py)
- 讀取 `data.json`。
- 使用 Python 字串模板或 Jinja2 生成 `index.html`。

#### [NEW] `template/`(file:///Users/kennykang/Desktop/VibeProj/Anti/taiwan_uniform_invoice/template/)
- 包含 `index.css` 與 `main.js` 的基礎模板。
- CSS 將使用現代化漸層與深色模式選項。

### [環境配置]
#### [NEW] `pyproject.toml`(file:///Users/kennykang/Desktop/VibeProj/Anti/taiwan_uniform_invoice/pyproject.toml)
- 使用 `uv init` 生成。

---

## 驗證計畫

### 自動化測試
1. **執行爬蟲**：`uv run python scraper.py`
   - 預期結果：成功生成 `data.json`，且包含 113-114 年的偶數序號項目。
2. **生成網頁**：`uv run python generator.py`
   - 預期結果：生成 `index.html`。

### 手動驗證
1. **開啟 index.html**：使用 `open index.html` (Mac) 查看。
2. **驗證 UI**：
   - 檢查是否有期別切換功能。
   - 檢查中獎號碼是否顯示正確（對比官網）。
   - 驗證 RWD 響應式效果。
