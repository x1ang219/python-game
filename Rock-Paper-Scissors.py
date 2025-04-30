#!/usr/bin/env python3
"""Rock-Paper-Scissors GUI小遊戲
================================
使用 tkinter 製作的石頭剪刀布小遊戲。

執行方式：
    python Rock-Paper-Scissors.py

遊戲特色：
    • 石頭✊／剪刀✌️／布🖐 按鈕點擊即玩
    • 即時顯示電腦出拳與結果
    • 自動計分，按「重置」可歸零重玩
"""

import tkinter as tk
from random import choice

# 名稱對應的emoji
CHOICES = [
    ("石頭", "✊"),
    ("剪刀", "✌️"),
    ("布",   "🖐"),
]

class RPSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("石頭剪刀布 GUI 版")
        self.geometry("400x300")
        self.resizable(False, False)

        # 分數
        self.player_score = 0
        self.comp_score = 0

        # 版面配置
        self._build_widgets()

    # ---------------- 架設 UI ----------------
    def _build_widgets(self):
        self.header = tk.Label(self, text="誰會贏？", font=("Helvetica", 16, "bold"))
        self.header.pack(pady=10)

        self.result_lbl = tk.Label(self, text="", font=("Helvetica", 14))
        self.result_lbl.pack()

        self.score_lbl = tk.Label(self, text=self._score_text(), font=("Helvetica", 12))
        self.score_lbl.pack(pady=5)

        # 按鈕列
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        for name, emoji in CHOICES:
            btn = tk.Button(
                btn_frame,
                text=f"{name}\n{emoji}",
                font=("Helvetica", 14),
                width=6,
                height=3,
                command=lambda n=name: self.play(n),
            )
            btn.pack(side=tk.LEFT, padx=5)

        # 重置按鈕
        tk.Button(self, text="重置", command=self.reset).pack(pady=10)

    # ---------------- 遊戲邏輯 ----------------
    def _score_text(self) -> str:
        return f"玩家 {self.player_score} : {self.comp_score} 電腦"

    def play(self, player_choice: str) -> None:
        comp_choice = choice([name for name, _ in CHOICES])
        outcome = self._judge(player_choice, comp_choice)

        if outcome == "win":
            self.player_score += 1
            msg = "你贏了！"
        elif outcome == "lose":
            self.comp_score += 1
            msg = "你輸了！"
        else:
            msg = "平手！"

        self.result_lbl.config(text=f"你出 {player_choice}，電腦出 {comp_choice} → {msg}")
        self.score_lbl.config(text=self._score_text())

    @staticmethod
    def _judge(p: str, c: str) -> str:
        # 判定勝負
        if p == c:
            return "tie"
        win_map = {"石頭": "剪刀", "剪刀": "布", "布": "石頭"}
        return "win" if win_map[p] == c else "lose"

    # ---------------- 其餘功能 ----------------
    def reset(self) -> None:
        self.player_score = self.comp_score = 0
        self.result_lbl.config(text="")
        self.score_lbl.config(text=self._score_text())

if __name__ == "__main__":
    app = RPSApp()
    app.mainloop()
