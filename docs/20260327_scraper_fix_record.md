# 統一發票爬蟲維護紀錄：財政部網站改版與 GitHub Actions 棄用警告

**日期：** 2026-03-27

## 1. GitHub Pages 渲染空白問題

### 症狀描述
專案部署至 GitHub Pages 後，畫面中央的期別選擇器與中獎號碼區塊完全空白，僅顯示網頁標題與頁尾。同時，GitHub Actions 的執行紀錄均顯示為綠色（Success），沒有拋出任何錯誤。

### 根本原因分析
1. **資料層缺失**：檢查發現產生的 `data.json` 為空陣列 `[]`，導致 `generator.py` 使用 Jinja2 渲染 HTML 時，產生內容的迴圈沒有執行，因此 DOM 元素為空。
2. **爬蟲邏輯失效**：
   - **列表頁改版**：財政部稅務入口網（`ETW183W1`）結構已變更，不再使用舊有的 `<table>` 配合序號的設計，改為純連結清單。
   - **舊邏輯不相容**：原來的 `scraper.py` 依賴「尋找表格中的偶數序號」來定位一般中獎號碼頁面，因為找不到符合條件的 HTML 元素，爬蟲默默結束並未報錯，導致抓回的資料為空。
   - **詳細頁面微調**：中獎號碼頁面（`ETW183W2_YYMM`）內的號碼被包裹在新的 `div.row > div.col-12` 結構中。

### 解決方案
對 `scraper.py` 進行了全面重寫：
- **棄用列表頁爬取**：觀察到中獎號碼頁面的 URL 具有高度規律性（格式為 `ETW183W2_YYMM`，例如 `ETW183W2_11501` 代表 115 年 1~2 月）。因此，直接透過當前年份動態構造近兩年共 12 期的 URL，大幅提升穩定性，不再受外層選單改版影響。
- **更新 DOM 解析選擇器**：在提取詳細號碼時，加入對 `div.col-12` 結構的支援，透過正則表達式安全地提取 8 位數或 3 位數的號碼。

---

## 2. GitHub Actions Node.js 20 棄用警告

### 症狀描述
在 GitHub Actions 的執行日誌中，出現黃色警告：
`Node.js 20 actions are deprecated. The following actions are running on Node.js 20 and may not work as expected: actions/checkout@v4, astral-sh/setup-uv@v5. Actions will be forced to run with Node.js 24 by default starting June 2nd, 2026.`

### 根本原因分析
這是 GitHub 官方的底層 runner 更新通知。您使用的第三方 actions（例如 `actions/checkout` 和 `astral-sh/setup-uv`）它們的執行環境依賴 Node.js 20，而 GitHub 即將強制升級到 Node.js 24。

### 解決方案
在 `.github/workflows/update_invoices.yml` 的 `update` job 區塊中，主動注入環境變數，指示 Runner 提前使用 Node.js 24，從而消除警告訊息：

```yaml
jobs:
  update:
    runs-on: ubuntu-latest
    env:
      FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
    steps:
      ...
```

---

## 3. GitHub "Workflow will be disabled soon" 信件通知

### 症狀/原因
使用者收到標題為 `[GitHub] The "Update Invoice Numbers" workflow ... will be disabled soon` 的 Email。
這是 GitHub 的防閒置機制：如果一個原始碼儲存庫（Repository）超過 **60 天** 沒有任何活動（例如 Push 程式碼），GitHub 為了節省運算資源，會自動停用該儲存庫裡面的所有排程（cron）任務。

### 解決方案
只要對 Repository 進行任何一次 Push（例如本次修復爬蟲的 commit），活動狀態就會自動重置，排程將恢復正常運作，無需額外設定。
