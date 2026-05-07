# sushigoroundbot.py Function Reference

這份文件簡介 `sushigoroundbot.py` 中每個 function 的用途。

## `main()`

程式入口。負責依序找出遊戲畫面、進入遊戲選單、設定座標，最後開始自動服務客人。

## `imPath(filename)`

產生圖片檔案路徑。會把傳入的檔名加上 `images/` 目錄，方便程式讀取辨識用圖片。

## `getGameRegion()`

找出 Sushi Go Round 遊戲視窗在螢幕上的位置，並設定全域變數 `GAME_REGION`。後續所有圖片辨識都會以這個區域為範圍。

## `setupCoordinates()`

根據 `GAME_REGION` 計算並設定各種遊戲物件的座標，例如食材、電話、訂購按鈕、配送按鈕與壽司竹簾。

## `navigateStartGameMenu()`

自動點擊遊戲開始前的選單，包括 `Play`、`Continue`、`Skip` 等按鈕，讓遊戲進入第一關。

## `startServing()`

主要遊戲迴圈。負責偵測客人訂單、製作壽司、處理缺料訂單、補貨、清盤子、重新製作逾時訂單，並檢查是否過關或失敗。

## `clickOnPlates()`

點擊六個固定盤子位置，用來清除客人吃完後的空盤。執行後會更新最後清盤時間。

## `getOrders()`

掃描遊戲畫面上的訂單圖示，判斷目前有哪些客人點了哪些壽司。回傳一個以訂單位置為 key、訂單種類為 value 的 dictionary。

## `getOrdersDifference(newOrders, oldOrders)`

比較目前訂單與上一輪訂單，找出新增訂單與已消失訂單。回傳 `(added, removed)` 兩個 dictionary。

## `makeOrder(orderType)`

根據指定的壽司種類製作餐點。會先檢查庫存是否足夠，足夠就點擊所需食材並捲壽司；不夠則回傳缺少的食材名稱。

## `findAndClickPlatesOnBelt()`

搜尋輸送帶上的多餘盤子並點擊清除，避免輸送帶被卡住，讓新做好的壽司能送出去。

## `orderIngredient(ingredient)`

透過遊戲內電話補充指定食材。會檢查是否已經在訂購中、是否買得起，成功後設定該食材的預計送達時間。

## `updateInventory()`

檢查已訂購食材是否送達。若送達，更新 `INVENTORY` 庫存數量，並清除該食材的訂購等待狀態。

## `checkForGameOver()`

檢查畫面是否出現過關或失敗訊息。過關時回傳 `LEVEL_WIN_MESSAGE`，失敗時結束程式。

