"""終極密碼（Number Guessing Game）

玩法：
    電腦隨機選擇一個 low~high 區間內的整數。
    玩家每次輸入一個猜測，程式會縮小範圍並給提示：
        -> 太小（guess < secret）：更新下限 → low = guess
        -> 太大（guess > secret）：更新上限 → high = guess
    當 guess == secret 時遊戲結束，顯示總猜測次數。
    並詢問是否需要再玩一次？

執行方法：
    python guess_number.py
"""

import random

def play_game(low: int = 1, high: int = 100):
    # 執行一場遊戲
    secret = random.randint(low, high)
    guess_low, guess_high = low, high
    attempts = 0
    print(f"\n=== 終極密碼 — 猜一個 {low} 到 {high} 之間的整數 ===")

    while True:
        # 取得數字並驗證使用者輸入是否使正確數值
        try:
            guess = int(input(f"請輸入猜測 ({guess_low}-{guess_high}): "))
        except ValueError:
            print("\033[31m請輸入有效的整數！\033[0m")
            continue

        # 檢查是否在目前有效範圍
        if guess <= guess_low or guess >= guess_high:
            print("請輸入『開區間』內的數字！")
            continue

        attempts += 1

        # 比對大小並更新範圍
        if guess < secret:
            guess_low = guess
            print("太小了！再試試…")
        elif guess > secret:
            guess_high = guess
            print("太大了！再試試…")
        else:
            print(f"恭喜答對！你用了 {attempts} 次機會。答案就是 {secret}。")
            break

def main() -> None:
    # 主迴圈，可重複遊戲。
    while True:
        play_game()
        again = input("\n再玩一次？(Y/N): ").strip().lower()
        if again != "y":
            print("感謝遊玩，再見！")
            break

if __name__ == "__main__":
    main()
