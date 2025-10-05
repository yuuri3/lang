import tkinter as tk
from tkinter import messagebox

# --- 設定 ---
TEX_FILE_PATH = "wordlist.tex"  # 追記先のTeXファイルパス
# TEXファイルがまだ存在しない場合は、初めての書き込み時に作成されます。
# 実際には、TeXファイルの \begin{document} と \end{document} の間に挿入する必要があります。
# 以下のコードはファイルの末尾に追記します。
# -----------------

def append_to_tex(word, part_of_speech, definition):
    """
    指定された単語、品詞、意味をTeXファイルの末尾に追記する関数。
    """
    # TeXの description 環境の書式で整形
    tex_entry = (
        f"\\item[{word}]\n"
        f"    {part_of_speech}\\\\\n"
        f"    {definition}\n"
    )
    
    try:
        # ファイルを追記モード ('a') で開く
        with open(TEX_FILE_PATH, 'a', encoding='utf-8') as f:
            f.write(tex_entry)
        
        messagebox.showinfo("成功", f"'{word}' を {TEX_FILE_PATH} に追記しました。")
        
    except Exception as e:
        messagebox.showerror("エラー", f"ファイル書き込み中にエラーが発生しました: {e}")

def submit_entry():
    """
    入力フィールドから値を取得し、TeXファイルに追記する処理を実行する。
    """
    word = entry_word.get().strip()
    pos = entry_pos.get().strip()
    definition = entry_definition.get().strip()
    
    if not word or not definition:
        messagebox.showwarning("警告", "単語と意味は必須入力です。")
        return
    
    # 品詞が空の場合はプレースホルダーを設定
    if not pos:
        pos = "---"
        
    append_to_tex(word, pos, definition)
    
    # 追記後、入力フィールドをクリア
    entry_word.delete(0, tk.END)
    entry_pos.delete(0, tk.END)
    entry_definition.delete(0, tk.END)
    
    # 次の単語入力にフォーカスを移動
    entry_word.focus_set()


# --- Tkinter GUIの設定 ---
root = tk.Tk()
root.title("TeX用語追記ツール")
root.geometry("400x200")

# ラベルと入力フィールドの作成
tk.Label(root, text="単語:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_word = tk.Entry(root, width=40)
entry_word.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="品詞:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_pos = tk.Entry(root, width=40)
entry_pos.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="意味:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_definition = tk.Entry(root, width=40)
entry_definition.grid(row=2, column=1, padx=5, pady=5)

# 登録ボタン
submit_button = tk.Button(root, text="TeXに追記", command=submit_entry)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

# 初期フォーカス設定
entry_word.focus_set()

# Enterキーで登録を実行
root.bind('<Return>', lambda event=None: submit_entry())

root.mainloop()