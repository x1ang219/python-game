#!/usr/bin/env python3
""" () — tkinter 版
================================================
4x4 = 16 張牌，玩家點擊兩張：
    -> 若圖案相同，就保持翻開並加分
    -> 不同則 1 秒後自動蓋回
完成全部配對即可通關，顯示總配對次數。

執行：
    python memory_match.py

可延伸：
    1. 改成 6×6 難度、加計時器
    2. 用 PNG 圖片 (PhotoImage) 取代 emoji
    3. 記錄排行榜或多關卡
"""

import random
import tkinter as tk
from functools import partial

EMOJIS = ["🍎", "🍇", "🍋", "🍓", "🍑", "🍍", "🥝", "🥑"]  # 8 種 * 2 = 16
CARD_BACK = "點我"
GRID_SIZE = 4  # 4×4 格
DELAY_MS = 1000  # 延遲


class MemoryMatch(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("翻牌配對小遊戲（Memory Match）")
        self.resizable(False, False)

        self.attempts = 0
        self.first_btn = None
        self.locked = False

        self._build_board()

    # ---------------- 建立棋盤 ----------------
    def _build_board(self):
        # 隨機排 16 張牌
        cards = EMOJIS * 2
        random.shuffle(cards)

        self.buttons: list[tk.Button] = []
        for idx, emoji in enumerate(cards):
            btn = tk.Button(
                self,
                text=CARD_BACK,
                font=("Helvetica", 28),
                width=4,
                height=2,
                command=partial(self.flip_card, idx),
            )
            btn.emoji = emoji  # 該位置的圖案（動態）
            row, col = divmod(idx, GRID_SIZE)
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)

        # 狀態 & 重置按鈕
        self.status_lbl = tk.Label(self, text="嘗試次數: 0", font=("Helvetica", 14))
        self.status_lbl.grid(row=GRID_SIZE, column=0, columnspan=GRID_SIZE, pady=(10, 0))

        tk.Button(self, text="重新開始", command=self.reset).grid(
            row=GRID_SIZE + 1, column=0, columnspan=GRID_SIZE, pady=(0, 10)
        )

    # ---------------- 牌面邏輯 ----------------
    def flip_card(self, idx: int) -> None:
        if self.locked:
            return  # 防止在等待蓋牌時再點

        btn = self.buttons[idx]
        if btn["text"] != CARD_BACK:  # 已翻開牌
            return

        btn.config(text=btn.emoji, state="disabled")

        if self.first_btn is None:
            self.first_btn = btn
        else:
            self.attempts += 1
            self.status_lbl.config(text=f"嘗試次數: {self.attempts}")
            self._check_match(btn)

    def _check_match(self, second_btn: tk.Button) -> None:
        assert self.first_btn is not None
        if self.first_btn.emoji == second_btn.emoji:
            # 配對成功
            self.first_btn = None
            if all(b["text"] != CARD_BACK for b in self.buttons):
                self._game_clear()
        else:
            # 配對失敗，1 秒後蓋回
            self.locked = True
            self.after(DELAY_MS, self._hide_cards, self.first_btn, second_btn)

    def _hide_cards(self, btn1: tk.Button, btn2: tk.Button) -> None:
        btn1.config(text=CARD_BACK, state="normal")
        btn2.config(text=CARD_BACK, state="normal")
        self.first_btn = None
        self.locked = False

    # ---------------- 通關 & 重置 ----------------
    def _game_clear(self) -> None:
        tk.messagebox.showinfo("完成！", f"全部配對成功！\n總嘗試次數：{self.attempts}")

    def reset(self) -> None:
        self.destroy()
        self.__init__()


if __name__ == "__main__":
    # 提前匯入 messagebox
    import tkinter.messagebox

    game = MemoryMatch()
    game.mainloop()