import pyautogui
import time
import os

# --- 設定區域 ---
pyautogui.FAILSAFE = True
CONFIDENCE = 0.7

# 效能優化：定義訂單掃描區域 (左, 上, 寬, 高)
# 請使用 pyautogui.displayMousePosition() 來找出你遊戲中訂單出現的大致範圍
ORDER_REGION = (372, 163, 868, 648)  
INGREDIENTSANDMAT_REGION = (355, 616, 439, 435)
# MAT_REGION = (498, 616, 302, 221)
PHONE_REGION = (1000, 580, 250, 200)
PLAT_REGION = (334, 398, 866, 139)
RESTOCK_LIST_REGION = (900, 450, 300, 250)
RICE_MENU_REGION = (992, 592, 162, 14)
# pyautogui.screenshot('check_view.png', region=(372, 163, 868, 648))

# 圖片路徑配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, 'images')

RICE = os.path.join(IMG_DIR, 'rice_button.png')
NORI = os.path.join(IMG_DIR, 'nori_button.png')
ROE = os.path.join(IMG_DIR, 'roe_button.png')
SHRIMP = os.path.join(IMG_DIR, 'shrimp_button.png')
SALMON = os.path.join(IMG_DIR, 'salmon_button.png')
UNAGI = os.path.join(IMG_DIR, 'unagi_button.png')
RICE_ZERO = os.path.join(IMG_DIR, 'rice_zero.png')
NORI_ZERO = os.path.join(IMG_DIR, 'nori_zero.png')
ROE_ZERO = os.path.join(IMG_DIR, 'roe_zero.png')
SHRIMP_ZERO = os.path.join(IMG_DIR, 'shrimp_zero.png')
SALMON_ZERO = os.path.join(IMG_DIR, 'salmon_zero.png')
UNAGI_ZERO = os.path.join(IMG_DIR, 'unagi_zero.png')
MAT = os.path.join(IMG_DIR, 'clear_mat.png')
PLAY_BUTTON = os.path.join(IMG_DIR, 'play_button.png')
CONTINUE_BUTTON = os.path.join(IMG_DIR, 'continue_button.png')
SKIP_BUTTON = os.path.join(IMG_DIR, 'skip_button.png')
PINK_PLATE = os.path.join(IMG_DIR, 'pink_plate.png')
BLUE_PLATE = os.path.join(IMG_DIR, 'blue_plate.png')
PHONE = os.path.join(IMG_DIR, 'phone.png')
PHONE_RICE = os.path.join(IMG_DIR, 'rice_order_menu.png')
PHONE_TOPPING = os.path.join(IMG_DIR, 'topping_order_menu.png')
RICE_ORDER = os.path.join(IMG_DIR, 'rice_order_button.png')
NORI_ORDER = os.path.join(IMG_DIR, 'nori_order_button.png')
ROE_ORDER = os.path.join(IMG_DIR, 'roe_order_button.png')
SHRIMP_ORDER = os.path.join(IMG_DIR, 'shrimp_order_button.png')
SALMON_ORDER = os.path.join(IMG_DIR, 'salmon_order_button.png')
UNAGI_ORDER = os.path.join(IMG_DIR, 'unagi_order_button.png')
NORMAL_DELIVERY = os.path.join(IMG_DIR, 'normal_delivery_button.png')
EXPRESS_DELIVERY = os.path.join(IMG_DIR, 'express_delivery_button.png')
PHONE_CLOSE  = os.path.join(IMG_DIR, 'phone_close.png')
YES_BUTTON  = os.path.join(IMG_DIR, 'yes.png')

# --- 庫存初始化 ---
# 初始數量
inventory = {
    'rice': 10,
    'nori': 10,
    'roe': 10,
    'shrimp': 5,
    'salmon': 5,
    'unagi': 5
}

# 每次補貨增加的數量
RESTOCK_AMOUNTS = {
    'rice': 10,
    'nori': 10,
    'roe': 10,
    'shrimp': 5,
    'salmon': 5,
    'unagi': 5
}

def click_coord(coords, name, sleep_time=0.2):
    """
    直接點擊指定座標，並加上小幅隨機偏移(防偵測)
    """
    import random
    left, top, width, height = coords
    target_x = left + (width // 2)
    target_y = top + (height // 2)
    
    pyautogui.click(target_x, target_y)
    print(f"  [動作] 座標點擊: {name} ({target_x}, {target_y})")
    time.sleep(sleep_time)

def start_game():
    """處理進入遊戲前的所有按鈕點擊：PLAY -> SKIP -> CONTINUE (順序依遊戲而定)"""
    print(">>> 正在檢查遊戲進入流程...")
    
    # 定義啟動階段可能出現的所有按鈕及其名稱
    start_buttons = [
        (PLAY_BUTTON, "PLAY"),
        (SKIP_BUTTON, "SKIP"),
        (CONTINUE_BUTTON, "CONTINUE")
    ]
    
    found_any = False
    
    for img_path, name in start_buttons:
        try:
            # 使用 try-except 避免新版 pyautogui 找不到圖時崩潰
            pos = pyautogui.locateCenterOnScreen(img_path, confidence=0.7)
            if pos:
                pyautogui.click(pos)
                print(f"  [動作] 已點擊 {name}")
                time.sleep(2) # 給予動畫反應時間
                found_any = True
                
                # 如果點擊的是 CONTINUE，通常代表進入遊戲了
                if name == "CONTINUE":
                    return True
        except pyautogui.ImageNotFoundException:
            continue # 沒看到這個按鈕就找下一個

    return False

# 壽司食譜配置
RECIPES = {
    'gunkan_maki': {
        'order_img': os.path.join(IMG_DIR, 'gunkan_maki_order.png'),
        'ingredients': [(RICE, 1), (NORI, 1), (ROE, 2)]
    },
    'salmon_roll': {
        'order_img': os.path.join(IMG_DIR, 'salmon_roll_order.png'),
        'ingredients': [(RICE, 1), (NORI, 1), (SALMON, 2)]
    },
    'california_roll': {
        'order_img': os.path.join(IMG_DIR, 'california_roll_order.png'),
        'ingredients': [(RICE, 1), (NORI, 1), (ROE, 1)]
    },
    'onigiri': {
        'order_img': os.path.join(IMG_DIR, 'onigiri_order.png'),
        'ingredients': [(RICE, 2), (NORI, 1)]
    }
}

def verify_files():
    """啟動前檢查所有圖片是否存在"""
    missing = []
    base_images = [RICE, NORI, ROE, MAT, DIRTY_PLATE]
    # 檢查基礎食材
    for f in base_images:
        if not os.path.exists(f):
            missing.append(os.path.basename(f))
    # 檢查訂單圖片
    for name, data in RECIPES.items():
        if not os.path.exists(data['order_img']):
            missing.append(os.path.basename(data['order_img']))
    
    if missing:
        print(f"錯誤：缺少以下圖片檔案，請補齊後再執行：\n{missing}")
        return False
    return True

def click_element(img_path, region, name, clicks=1):
    """通用點擊函數：現在加入了 region 限制以提升速度"""
    try:
        # 使用 INGREDIENTS_REGION 來限制掃描範圍
        location = pyautogui.locateCenterOnScreen(
            img_path, 
            region=region, 
            confidence=CONFIDENCE
        )
        if location:
            for _ in range(clicks):
                pyautogui.click(location)
                time.sleep(0.1)
            return True
        else:
            pass
    except Exception as e:
        print(f"  [錯誤] 辨識 {name} 異常: {e}")
    return False

def make_sushi(sushi_name):
    """製作壽司邏輯"""
    print(f">>> 正在製作: {sushi_name}")
    recipe = RECIPES[sushi_name]['ingredients']

    img_to_key = {
        RICE: 'rice', NORI: 'nori', ROE: 'roe',
        SHRIMP: 'shrimp', SALMON: 'salmon', UNAGI: 'unagi'
    }
    
    for img, count in recipe:
        key = img_to_key.get(img)
        # 檢查內部數值是否足夠
        if inventory[key] < count:
            print(f"  [中斷] 庫存預警：{key} 剩餘 {inventory[key]}，不足以製作。")
            return False

        if click_element(img, INGREDIENTSANDMAT_REGION, sushi_name, clicks=count):
            # 成功點擊後，扣除數量
            inventory[key] -= count
            print(f"  [庫存] {key} 消耗 {count}，剩餘: {inventory[key]}")
        else:
            return False
        # if not click_element(img,INGREDIENTSANDMAT_REGION, sushi_name, clicks=count):
        #     print(f"  [中斷] 找不到食材按鈕，可能庫存不足或被遮擋。")
        #     return False
    
    # 點擊竹簾
    if click_element(MAT, INGREDIENTSANDMAT_REGION, "竹簾"):
        print(f"--- {sushi_name} 製作完成，等待送出 ---")
        time.sleep(2) # 建議：等待 2 秒讓動畫跑完，防止重複偵測同一份訂單
        return True
    return False

def check_orders():
    """優化版：帶有區域掃描的訂單偵測"""
    for name, data in RECIPES.items():
        try:
            # 加入 region 參數大幅提升速度
            order = pyautogui.locateOnScreen(
                data['order_img'], 
                region=ORDER_REGION, 
                confidence=CONFIDENCE
            )
            if order:
                if make_sushi(name):
                    return # 製作成功後跳出，進入下一輪 check (包含收盤子)
        except Exception:
            continue

def restock(item_type):
    """自動補貨流程"""
    print(f">>> 偵測到食材短缺，啟動補貨流程: {item_type}")
    try:
        # 偵測清單是否開啟
        close_btn = pyautogui.locateCenterOnScreen(PHONE_CLOSE, region=RESTOCK_LIST_REGION, confidence=0.7)
        if close_btn:
            print("  [狀態] 偵測到選單已開啟，正在重置狀態...")
            pyautogui.click(close_btn)
            time.sleep(0.5) # 等待選單關閉動畫
    except:
        pass # 沒看到選單代表是關閉的，繼續執行
    
    # 1. 點擊電話
    if not click_element(PHONE, PHONE_REGION, "電話"): return

    # 2. 選擇分類
    time.sleep(0.5)
    if item_type == 'rice':
        # click_element(PHONE_RICE, RESTOCK_LIST_REGION, "選單-米")
        click_coord(RICE_MENU_REGION, "選單-米", 0.5)
        click_element(RICE_ORDER, RESTOCK_LIST_REGION, "配料-米")
    else:
        click_element(PHONE_TOPPING, RESTOCK_LIST_REGION, "選單-配料")
        time.sleep(0.3)
        # if item_type == 'nori': click_element(NORI_ORDER, RESTOCK_LIST_REGION, "配料-海苔")
        # elif item_type == 'roe': click_element(ROE_ORDER, RESTOCK_LIST_REGION, "配料-魚卵")
        # elif item_type == 'shrimp': click_element(SHRIMP_ORDER, RESTOCK_LIST_REGION, "配料-蝦")
        # elif item_type == 'salmon': click_element(SALMON_ORDER, RESTOCK_LIST_REGION, "配料-鮭魚")
        # elif item_type == 'unagi': click_element(UNAGI_ORDER, RESTOCK_LIST_REGION, "配料-海膽")
        mapping = {
            'nori': (NORI_ORDER, "海苔"),
            'roe': (ROE_ORDER, "魚卵"),
            'shrimp': (SHRIMP_ORDER, "蝦"),
            'salmon': (SALMON_ORDER, "鮭魚"),
            'unagi': (UNAGI_ORDER, "海膽")
        }
        img, name = mapping[item_type]
        click_element(img, RESTOCK_LIST_REGION, name)

    # 3. 選擇送貨方式 (假設餘額檢查，優先嘗試點擊右邊 Express)
    time.sleep(0.3)
    # # 這裡的邏輯：先試快遞，失敗點普通 (或直接根據你的金額判斷)
    # if not click_element(EXPRESS_DELIVERY, RESTOCK_LIST_REGION, "快遞($40)"):
    # 一律選普通送貨
    click_element(NORMAL_DELIVERY, RESTOCK_LIST_REGION, "普通送貨")
    
    print(f"--- 補貨指令已發送 ---")
    clear_tables()
    time.sleep(6)
    inventory[item_type] += RESTOCK_AMOUNTS[item_type]
    print(f"--- {item_type} 補貨已送達！目前庫存: {inventory[item_type]} ---")

def check_inventory():
    """偵測食材是否為 0"""
    try:
        # 檢查米
        if pyautogui.locateOnScreen(RICE_ZERO, region=INGREDIENTSANDMAT_REGION, confidence=0.9):
            restock('rice')
            print("[狀態] 米沒有了")
        else:
            print("[狀態] 米還有")
    except pyautogui.ImageNotFoundException:
        pass
    
    try:
        # 檢查海苔
        if pyautogui.locateOnScreen(NORI_ZERO, region=INGREDIENTSANDMAT_REGION, confidence=0.9):
            restock('nori')
            print("[狀態] 海苔沒有了")
        else:
            print("[狀態] 海苔還有")
    except pyautogui.ImageNotFoundException:
        pass
    
    try:
        # 檢查魚卵
        if pyautogui.locateOnScreen(ROE_ZERO, region=INGREDIENTSANDMAT_REGION, confidence=0.9):
            restock('roe')
            print("[狀態] 魚卵沒有了")
        else:
            print("[狀態] 魚卵還有")
    except pyautogui.ImageNotFoundException:
        pass
    
    try:
        # 檢查蝦
        if pyautogui.locateOnScreen(SHRIMP_ZERO, region=INGREDIENTSANDMAT_REGION, confidence=0.9):
            restock('shrimp')
            print("[狀態] 蝦沒有了")
        else:
            print("[狀態] 蝦還有")
    except pyautogui.ImageNotFoundException:
        pass
    
    try:
        # 檢查鮭魚
        if pyautogui.locateOnScreen(SALMON_ZERO, region=INGREDIENTSANDMAT_REGION, confidence=0.9):
            restock('salmon')
            print("[狀態] 鮭魚沒有了")
        else:
            print("[狀態] 鮭魚還有")
    except pyautogui.ImageNotFoundException:
        pass
    
    try:
        # 檢查海膽
        if pyautogui.locateOnScreen(UNAGI_ZERO, region=INGREDIENTSANDMAT_REGION, confidence=0.9):
            restock('unagi')
            print("[狀態] 海膽沒有了")
        else:
            print("[狀態] 海膽還有")
    except pyautogui.ImageNotFoundException:
        pass

def clear_tables():
    """清理盤子"""
    try:
        plates = list(pyautogui.locateAllOnScreen(PINK_PLATE, region=PLAT_REGION, confidence=0.6))
        if plates:
            for p in plates:
                pyautogui.click(pyautogui.center(p))
                print("  [動作] 清理盤子")
                time.sleep(0.1)
    except: pass
    try:
        plates = list(pyautogui.locateAllOnScreen(BLUE_PLATE, region=PLAT_REGION, confidence=0.6))
        if plates:
            for p in plates:
                pyautogui.click(pyautogui.center(p))
                print("  [動作] 清理盤子")
                time.sleep(0.1)
    except: pass

def check_inventory_values():
    """根據內部數值檢查是否需要補貨 (剩餘 <= 1 時)"""
    for item, count in inventory.items():
        if count <= 1:
            restock(item)

# def main():
#     print("腳本啟動中，10秒倒數...")
#     time.sleep(10)
#     start_game()
    
#     last_inv_check = 0
    
#     try:
#         while True:
#             current_time = time.time()
            
#             # 每10秒檢查一次盤子
#             if current_time - last_inv_check > 10.0:
#                 # check_inventory()
#                 clear_tables()
#                 last_inv_check = current_time

#             # 偵測訂單並製作
#             check_inventory()
#             check_orders()
#             clear_tables()
#             time.sleep(0.5) # 稍微喘息，降低 CPU 負擔
#     except KeyboardInterrupt:
#         print("\n使用者停止。")

def handle_game_flow():
    """
    自動處理所有過場按鈕，讓遊戲能自動進入下一關
    """
    try:
        # 這裡不限制 Region，因為過場按鈕通常在畫面中央
        pos = pyautogui.locateCenterOnScreen(CONTINUE_BUTTON, confidence=0.7)
        if pos:
            pyautogui.click(pos)
            print(f"  [流程] 偵測到continue，已點擊並繼續。")
            time.sleep(6) # 過場動畫通常較長
            pyautogui.click(pos)

        yes = pyautogui.locateCenterOnScreen(YES_BUTTON, confidence=0.7)
        if yes:
            pyautogui.click(yes)

    except pyautogui.ImageNotFoundException:
        pass

def main():
    print("腳本啟動中，請確保遊戲庫存為初始滿額狀態...")
    time.sleep(13)
    start_game()

    last_flow_check = 0
    
    try:
        while True:
            current_time = time.time()
            # --- 每 20 秒檢查一次是否需要「點擊繼續」進入下一關 ---
            if current_time - last_flow_check > 20.0:
                handle_game_flow()
                last_flow_check = current_time
            # 1. 檢查內部數值，決定是否補貨
            check_inventory_values()
            # 2. 處理訂單
            check_orders()
            if current_time - last_flow_check > 4.0:
                # 3. 清理盤子
                clear_tables()
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n使用者停止。最終庫存狀態: {inventory}")

if __name__ == "__main__":
    main()