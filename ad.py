import tkinter as tk
from tkinter import messagebox

# ---------- Logic ----------
def calculate_price(price):
    price_table = {
        390: (440, 420),
        450: (500, 480),
        490: (540, 520),
        550: (580, 570),
    }
    # ถ้าไม่อยู่ใน table → ใช้ราคาเดิมทั้งคู่
    return price_table.get(price, (price, price))


def copy_text(text):
    root.clipboard_clear()
    root.clipboard_append(text)


def clear_all():
    for entry in entries.values():
        entry.delete(0, tk.END)

    order_type.set("จองล่วงหน้า")  # reset dropdown

    for widget in result_frame.winfo_children():
        widget.destroy()


def process():
    try:
        code = int(entries["Shirt ID"].get())
        name = entries["Name of shirt"].get()
        amount = int(entries["Amount"].get())
        price = int(entries["Price"].get())
    except ValueError:
        messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบและถูกต้อง")
        return

    delivery, transfer = calculate_price(price)

    # ---------- amount handling ----------
    amount_text = f"{amount}สี" if amount > 0 else ""

    texts = []
    mode = order_type.get()

    # ---------- text by dropdown ----------
    if mode == "จองล่วงหน้า":
        texts = [
            f"จองเสื้อ{name}{amount_text}รหัส {code} รวมส่งปลายทาง {delivery} บาท รอ 15 วัน คลิกที่นี่",
            f"จองเสื้อ{name}{amount_text}รหัส {code} รวมส่งโอน {transfer} บาท รอ 15 วัน คลิกที่นี่",
            f"รับส่วนลด 10% สำหรับซื้อ 3 ชิ้นรหัส {code} คลิกที่นี่ค่ะ",
        ]
    else:  # พร้อมส่ง
        texts = [
            f"สั่งเสื้อพร้อมส่ง{name}{amount_text}รหัส {code} รวมปลายทาง {delivery} บาท คลิกที่นี่ค่ะ",
            f"สั่งเสื้อพร้อมส่ง{name}{amount_text}รหัส {code} รวมโอน {transfer} บาท คลิกที่นี่ค่ะ",
            f"รับส่วนลด 10% สำหรับรหัสเสื้อ {code} คละแบบอื่นได้คลิกที่นี่ค่ะ",
        ]

    # clear old result
    for widget in result_frame.winfo_children():
        widget.destroy()

    # render result + copy button
    for text in texts:
        row = tk.Frame(result_frame)
        row.pack(fill="x", pady=2)

        label = tk.Label(row, text=text, anchor="w")
        label.pack(side="left", fill="x", expand=True)

        btn = tk.Button(row, text="Copy", command=lambda t=text: copy_text(t))
        btn.pack(side="right")


# ---------- UI ----------
root = tk.Tk()
root.title("Shirt Order Tool")

main = tk.Frame(root, padx=10, pady=10)
main.pack(fill="both", expand=True)

# ---------- Dropdown ----------
row = tk.Frame(main)
row.pack(fill="x", pady=5)

tk.Label(row, text="ประเภทคำสั่งซื้อ", width=15, anchor="w").pack(side="left")

order_type = tk.StringVar(value="จองล่วงหน้า")
tk.OptionMenu(row, order_type, "จองล่วงหน้า", "พร้อมส่ง").pack(side="left")

# ---------- Inputs ----------
entries = {}
fields = ["Shirt ID", "Name of shirt", "Amount", "Price"]

for field in fields:
    row = tk.Frame(main)
    row.pack(fill="x", pady=3)

    label = tk.Label(row, text=field, width=15, anchor="w")
    label.pack(side="left")

    entry = tk.Entry(row)
    entry.pack(side="right", fill="x", expand=True)

    entries[field] = entry

# ---------- Buttons ----------
btn_frame = tk.Frame(main, pady=10)
btn_frame.pack()

tk.Button(btn_frame, text="Process", width=12, command=process).pack(side="left", padx=5)
tk.Button(btn_frame, text="Clear", width=12, command=clear_all).pack(side="left", padx=5)

# ---------- Result ----------
result_frame = tk.LabelFrame(main, text="Result", padx=5, pady=5)
result_frame.pack(fill="both", expand=True)

root.mainloop()

