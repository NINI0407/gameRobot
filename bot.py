import pyautogui
import time
import os

# 設置
pyautogui.FAILSAFE = True
CONFIDENCE = 0.7  # 辨識信心值

# 圖片路徑配置
IMG_DIR = 'images/'
RICE = os.path.join(IMG_DIR, 'rice_button.png')
SEAWEED = os.path.join(IMG_DIR, 'seaweed_button.png')
ROE = os.path.join(IMG_DIR, 'roe_button.png')
MAT = os.path.join(IMG_DIR, 'clear_mat.png')

# 壽司食譜配置 (格式: 食材圖片路徑, 數量)
RECIPES = {
    'onigiri': {
        'order_img': os.path.join(IMG_DIR, 'onigiri_order.png'),
        'ingredients': [(RICE, 2), (SEAWEED, 1)]
    },
    'california_roll': {
        'order_img': os.path.join(IMG_DIR, 'california_roll_order.png'),
        'ingredients': [(RICE, 1), (SEAWEED, 1), (ROE, 1)]
    },
    'gunkan_maki': {
        'order_img': os.path.join(IMG_DIR, 'gunkan_order.png'),
        'ingredients': [(RICE, 1), (SEAWEED, 1), (ROE, 2)]
    }
}

def click_element(img_path, name, clicks=1):
    """通用點擊函數"""
    try:
        location = pyautogui.locateCenterOnScreen(img_path, confidence=CONFIDENCE)
        if location:
            for _ in range(clicks):
                pyautogui.click(location)
                time.sleep(0.1)  # 點擊間隔，防止遊戲沒反應
            return True
        else:
            print(f"  [警告] 找不到 {name} 圖標")
            return False
    except Exception as e:
        print(f"  [錯誤] 辨識 {name} 異常: {e}")
        return False

def make_sushi(sushi_name):
    """根據壽司名稱與食譜製作壽司"""
    print(f">>> 正在製作: {sushi_name}")
    recipe = RECIPES[sushi_name]['ingredients']
    
    # 1. 依序點擊食材
    for img, count in recipe:
        if not click_element(img, f"食材({img})", clicks=count):
            print(f"  [中斷] 製作 {sushi_name} 失敗，缺少食材。")
            return
    
    # 2. 點擊竹簾完成製作
    click_element(MAT, "竹簾")
    print(f"--- {sushi_name} 完成 ---")

def check_orders():
    """掃描所有已定義的壽司訂單"""
    for name, data in RECIPES.items():
        try:
            # 偵測訂單
            order = pyautogui.locateOnScreen(data['order_img'], confidence=CONFIDENCE)
            if order:
                make_sushi(name)
                return  # 每次只處理一個訂單，避免邏輯混亂
        except pyautogui.ImageNotFoundException:
            continue

def clear_tables():
    """收盤子 (建議改為影像辨識空盤，以下維持你提供的座標法)"""
    table_coords = [(100, 200), (200, 200), (300, 200)] 
    for coord in table_coords:
        pyautogui.click(coord)

def main():
    print("腳本已啟動，請切換至遊戲視窗...")
    time.sleep(5)
    
    try:
        while True:
            check_orders()
            clear_tables()
            time.sleep(1) 
    except KeyboardInterrupt:
        print("腳本手動停止。")

if __name__ == "__main__":
    main()