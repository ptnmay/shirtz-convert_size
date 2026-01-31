import tkinter as tk
from decimal import Decimal

# ---------- Data ----------
convert_table = {
    str(i): v for i, v in zip(
        range(20, 153),
        [
            7.9,8.3,8.7,9.1,9.4,9.8,10.2,10.6,11.0,11.4,11.8,12.2,12.6,13.0,13.4,
            13.8,14.2,14.6,15.0,15.4,15.7,16.1,16.5,16.9,17.3,17.7,18.1,18.5,
            18.9,19.3,19.7,20.1,20.5,20.9,21.3,21.7,22.0,22.4,22.8,23.2,23.6,
            24.0,24.4,24.8,25.2,25.6,26.0,26.4,26.8,27.2,27.6,28.0,28.3,28.7,
            29.1,29.5,29.9,30.3,30.7,31.1,31.5,31.9,32.3,32.7,33.1,33.5,33.9,
            34.3,34.6,35.0,35.4,35.8,36.2,36.6,37.0,37.4,37.8,38.2,38.6,39.0,
            39.4,39.8,40.2,40.6,40.9,41.3,41.7,42.1,42.5,42.9,43.3,43.7,44.1,
            44.5,44.9,45.3,45.7,46.1,46.5,46.9,47.2,47.6,48.0,48.4,48.8,49.2,
            49.6,50.0,50.4,50.8,51.2,51.6,52.0,52.4,52.8,53.1,53.5,53.9,54.3,
            54.7,55.1,55.5,55.9,56.3,56.7,57.1,57.5,57.9,58.3,58.7,59.1,59.4,
            59.8
        ]
    )
}

# ---------- Logic ----------
def round_float(n):
    d = Decimal(str(n))
    i = int(d)
    dp = d - i
    if Decimal("0.1") <= dp <= Decimal("0.3"):
        return str(i)
    elif Decimal("0.4") <= dp <= Decimal("0.7"):
        return str(i + Decimal("0.5"))
    elif Decimal("0.8") <= dp:
        return str(i + 1)
    return str(i)

def convert_value(v):
    try:
        key = str(int(float(v)))
        return round_float(convert_table[key]) if key in convert_table else None
    except:
        return None

def convert_part(p):
    if "-" in p:
        a, b = p.split("-")
        r1, r2 = convert_value(a), convert_value(b)
        return f"{r1}-{r2}" if r1 and r2 else None
    return convert_value(p)

# ---------- UI Helpers ----------
def copy_text(t):
    root.clipboard_clear()
    root.clipboard_append(t)

def clear_all():
    text_input.delete("1.0", tk.END)
    code_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    for w in result_frame.winfo_children():
        w.destroy()

# ---------- Main Process ----------
def process():
    for w in result_frame.winfo_children():
        w.destroy()

    code = code_entry.get().strip()
    price = price_entry.get().strip()

    lines = text_input.get("1.0", tk.END).strip().split("\n")
    result_lines = []

    for line in lines:
        parts = line.replace(" - ", "-").split()
        text_size = ""
        nums = []

        for p in parts:
            if any(c.isdigit() for c in p):
                nums.append(p)
            else:
                text_size = p

        if len(nums) < 2:
            continue

        chest = convert_part(nums[0])
        length = convert_part(nums[-1])
        if not chest or not length:
            continue

        line_parts = [f"อก {chest}"]

        if len(nums) == 3:
            shoulder = convert_part(nums[1])
            if shoulder:
                line_parts.append(f"ไหล่ {shoulder}")

        line_parts.append(f"ยาว {length}")

        result_lines.append(
            (f"{text_size} " if text_size else "") + " ".join(line_parts)
        )

    if not result_lines:
        return

    size_block = "\n".join(result_lines)

    # Block 1
    b1 = tk.Frame(result_frame, bd=1, relief="solid", padx=8, pady=8)
    b1.pack(fill="x", pady=6)

    tk.Label(b1, text=size_block, justify="left", anchor="w", wraplength=420)\
        .pack(side="left", fill="x", expand=True)

    tk.Button(b1, text="Copy", command=lambda: copy_text(size_block))\
        .pack(side="right")

    # Block 2
    if code and price:
        sell_block = f"{code} : {price}.-\n{size_block}"

        b2 = tk.Frame(result_frame, bd=1, relief="solid", padx=8, pady=8)
        b2.pack(fill="x", pady=(0, 6))

        tk.Label(b2, text=sell_block, justify="left", anchor="w", wraplength=420)\
            .pack(side="left", fill="x", expand=True)

        tk.Button(b2, text="Copy", command=lambda: copy_text(sell_block))\
            .pack(side="right")

# ---------- UI ----------
root = tk.Tk()
root.title("Chinese Size Tool")
root.geometry("520x600")

main = tk.Frame(root, padx=15, pady=15)
main.pack(fill="both", expand=True)

tk.Label(main, text="รหัสเสื้อ").pack(anchor="w")
code_entry = tk.Entry(main)
code_entry.pack(fill="x")

tk.Label(main, text="ราคา").pack(anchor="w", pady=(5, 0))
price_entry = tk.Entry(main)
price_entry.pack(fill="x")

tk.Label(main, text="ใส่ไซส์ (ตัวเลขล้วน / รองรับช่วง)",
         font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(10, 0))

text_input = tk.Text(main, height=6)
text_input.pack(fill="x", pady=6)

btns = tk.Frame(main)
btns.pack(pady=5)

tk.Button(btns, text="แปลง", width=12, command=process).pack(side="left", padx=5)
tk.Button(btns, text="ล้าง", width=12, command=clear_all).pack(side="left", padx=5)

result_box = tk.LabelFrame(main, text="ผลลัพธ์", padx=8, pady=8)
result_box.pack(fill="both", expand=True, pady=10)

canvas = tk.Canvas(result_box)
scroll = tk.Scrollbar(result_box, orient="vertical", command=canvas.yview)
result_frame = tk.Frame(canvas)

result_frame.bind("<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=result_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

root.mainloop()
