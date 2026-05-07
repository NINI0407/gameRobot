import pyautogui
import keyboard
import time
import os

# 設定儲存路徑
FILE_PATH = "coordinates.txt"

def record_on_demand():
    print("=== 精確座標紀錄工具 ===")
    print(f"紀錄檔案: {os.path.abspath(FILE_PATH)}")
    print("使用說明：")
    print("1. 將滑鼠移到目標位置。")
    print("2. 按下 [Shift] 鍵紀錄座標。")
    print("3. 按下 [Esc] 鍵結束程式並存檔。")
    print("-" * 30)

    # 確保以追加模式開啟
    with open(FILE_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n--- 新紀錄時段: {time.ctime()} ---\n")
        
        try:
            while True:
                # 偵測 Esc 鍵退出
                if keyboard.is_pressed('esc'):
                    break

                # 偵測 Shift 鍵
                if keyboard.is_pressed('shift'):
                    x, y = pyautogui.position()
                    
                    # 取得該點顏色（用於判斷食材是否用完或盤子是否清空）
                    pixel_color = pyautogui.pixel(x, y)
                    
                    record_str = f"位置: X={x:>4}, Y={y:>4} | 顏色 RGB={pixel_color}"
                    
                    # 輸出到螢幕
                    print(f"[已紀錄] {record_str}")
                    
                    # 寫入檔案
                    f.write(record_str + "\n")
                    f.flush() # 立即存入硬碟
                    
                    # 防止按一下 Shift 紀錄太多次，加入短暫延遲
                    while keyboard.is_pressed('shift'):
                        time.sleep(0.1)

                time.sleep(0.01) # 降低 CPU 負擔

        except Exception as e:
            print(f"\n發生錯誤: {e}")
        finally:
            print("\n=== 紀錄結束，檔案已關閉 ===")

if __name__ == "__main__":
    # 提醒：必須以系統管理員權限執行，鍵盤監聽才能在所有視窗生效
    record_on_demand()