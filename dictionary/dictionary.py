import tkinter as tk
from tkinter import messagebox
import os

# --- 設定 ---
TEX_FILE_PATH = "wordlist.tex"  # 追記先のTeXファイルパス
# -----------------

# 直近で追記したTeXエントリを記憶するグローバル変数
last_tex_entry = "" 

def append_to_tex(word, part_of_speech, definition):
    """
    指定された単語、品詞、意味をTeXファイルの末尾に追記する関数。
    """
    global last_tex_entry
    
    # TeXの description 環境の書式で整形
    # 削除時に正確に検索・置換できるように、改行やインデントを含めて完全に保存する
    tex_entry = (
        f"\\item[{word}]\n"
        f"    {part_of_speech}\\\\\n"
        f"    {definition}\n"
    )
    
    try:
        # ファイルを追記モード ('a') で開く
        with open(TEX_FILE_PATH, 'a', encoding='utf-8') as f:
            f.write(tex_entry)
        
        # 成功したら、追記した内容を記憶する
        last_tex_entry = tex_entry 
        
        messagebox.showinfo("成功", f"'{word}' を {TEX_FILE_PATH} に追記しました。\n元に戻す機能が有効になりました。")
        
        # 削除ボタンを有効にする (GUI更新は後述)
        delete_button.config(state=tk.NORMAL)
        
    except Exception as e:
        messagebox.showerror("エラー", f"ファイル書き込み中にエラーが発生しました: {e}")
        last_tex_entry = "" # エラー時は記憶をクリア

def undo_last_entry():
    """
    直近で追記したエントリをTeXファイルから削除する関数。
    """
    global last_tex_entry
    
    if not last_tex_entry:
        messagebox.showwarning("警告", "直近で追記されたエントリがありません。")
        return

    try:
        # ファイル全体を読み込む
        with open(TEX_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 記憶しているエントリを探し、削除（空文字列に置換）する
        new_content = content.replace(last_tex_entry, "", 1) # 最初の1回だけ置換

        if content == new_content:
            messagebox.showwarning("警告", "ファイル内で記憶されたエントリが見つかりませんでした。ファイルが手動で編集された可能性があります。")
        else:
            # 修正した内容でファイルを上書きする
            with open(TEX_FILE_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            word_to_delete = last_tex_entry.split('\n')[0].split('[')[1].split(']')[0]
            messagebox.showinfo("成功", f"直前の追記項目 '{word_to_delete}' を {TEX_FILE_PATH} から削除しました。")
            
            # 削除完了後、記憶をクリアし、ボタンを無効化
            last_tex_entry = ""
            delete_button.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("エラー", f"ファイル削除中にエラーが発生しました: {e}")


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
root.geometry("400x230") # 高さ調整

# ラベルと入力フィールドの作成 (変更なし)
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
submit_button.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

# 新しい削除ボタン
delete_button = tk.Button(root, text="直前の追記を削除 (Undo)", command=undo_last_entry, state=tk.DISABLED)
delete_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

# 初期フォーカス設定
entry_word.focus_set()

# Enterキーで登録を実行
root.bind('<Return>', lambda event=None: submit_entry())

root.mainloop()