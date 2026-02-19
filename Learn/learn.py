# وارد کردن کتابخانه‌های مورد نیاز
import tkinter as tk              # برای ساخت رابط گرافیکی
from tkinter import messagebox    # برای نمایش پیام خطا
import matplotlib.pyplot as plt   # برای رسم نمودار
from matplotlib.widgets import Button  # برای ساخت دکمه داخل نمودار
import csv                        # برای ذخیره اطلاعات در فایل CSV
from datetime import datetime     # برای ثبت تاریخ و زمان

# -------------------------------------------------
# تابع محاسبه BMI
# ورودی: وزن و قد
# خروجی: مقدار BMI
# -------------------------------------------------
def calculate_bmi(weight, height):
    return weight / (height ** 2)   # فرمول اصلی BMI


# -------------------------------------------------
# تابع تعیین دسته‌بندی BMI
# ورودی: مقدار BMI
# خروجی: وضعیت فرد
# -------------------------------------------------
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"   # کمبود وزن
    elif bmi < 25:
        return "Normal"        # نرمال
    elif bmi < 30:
        return "Overweight"    # اضافه وزن
    else:
        return "Obese"         # چاقی


# -------------------------------------------------
# ذخیره اطلاعات در فایل CSV
# هر بار محاسبه انجام شود اطلاعات ذخیره می‌شود
# -------------------------------------------------
def save_to_csv(weight, height, bmi, category):
    with open("bmi_results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(),    # ثبت زمان
            weight,
            height,
            round(bmi, 2),     # گرد کردن تا 2 رقم اعشار
            category
        ])


# -------------------------------------------------
# رسم نمودار دایره‌ای رنگی (Donut Chart)
# -------------------------------------------------
def show_pie_chart(bmi):

    fig, ax = plt.subplots()          # ساخت شکل و محور
    plt.subplots_adjust(bottom=0.2)   # ایجاد فضا برای دکمه پایین نمودار

    categories = ["Underweight", "Normal", "Overweight", "Obese"]
    colors = ["#3498db", "#2ecc71", "#f39c12", "#e74c3c"]  # رنگ هر بخش

    # مشخص کردن اینکه BMI کاربر در کدام دسته است
    if bmi < 18.5:
        index = 0
    elif bmi < 25:
        index = 1
    elif bmi < 30:
        index = 2
    else:
        index = 3

    # فقط دسته مربوط به کاربر بزرگ‌تر نمایش داده می‌شود
    sizes = [0.1, 0.1, 0.1, 0.1]
    sizes[index] = 1

    # رسم نمودار دایره‌ای
    wedges, texts = ax.pie(
        sizes,
        labels=categories,
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.5)  # باعث می‌شود نمودار حالت دوناتی بگیرد
    )

    # عنوان نمودار
    ax.set_title(f"Your BMI: {bmi:.2f}", fontsize=14, fontweight="bold")

    # -------------------------
    # ساخت دکمه Refresh داخل نمودار
    # -------------------------
    ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
    button = Button(ax_button, 'Refresh')

    # عملکرد دکمه (بستن نمودار)
    def refresh(event):
        plt.close(fig)

    button.on_clicked(refresh)

    plt.show()  # نمایش نمودار


# -------------------------------------------------
# تابع اصلی محاسبه که با دکمه اجرا می‌شود
# -------------------------------------------------
def calculate():

    try:
        weight = float(entry_weight.get())  # دریافت وزن از کاربر
        height = float(entry_height.get())  # دریافت قد از کاربر

        # بررسی اینکه مقادیر منفی یا صفر نباشند
        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Values must be positive numbers.")
            return

        bmi = calculate_bmi(weight, height)   # محاسبه BMI
        category = bmi_category(bmi)          # تعیین وضعیت

        # نمایش نتیجه در برنامه
        result_label.config(
            text=f"Your BMI: {bmi:.2f}\nCategory: {category}"
        )

        save_to_csv(weight, height, bmi, category)  # ذخیره در فایل
        show_pie_chart(bmi)                         # نمایش نمودار

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")


# -------------------------------------------------
# تابع ریست کردن فیلدها
# -------------------------------------------------
def reset_fields():
    entry_weight.delete(0, tk.END)  # پاک کردن وزن
    entry_height.delete(0, tk.END)  # پاک کردن قد
    result_label.config(text="")    # پاک کردن نتیجه


# -------------------------------------------------
# ساخت پنجره اصلی برنامه (GUI)
# -------------------------------------------------
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x420")
root.configure(bg="#1e272e")
root.resizable(False, False)

# عنوان برنامه
title = tk.Label(
    root,
    text="BMI Calculator",
    font=("Helvetica", 18, "bold"),
    bg="#1e272e",
    fg="white"
)
title.pack(pady=20)

# فیلد وزن
tk.Label(root, text="Weight (kg)", bg="#1e272e", fg="white").pack()
entry_weight = tk.Entry(root, font=("Helvetica", 12), justify="center")
entry_weight.pack(pady=5)

# فیلد قد
tk.Label(root, text="Height (m)", bg="#1e272e", fg="white").pack()
entry_height = tk.Entry(root, font=("Helvetica", 12), justify="center")
entry_height.pack(pady=5)

# دکمه محاسبه
tk.Button(
    root,
    text="Calculate",
    command=calculate,
    bg="#00cec9",
    fg="black",
    width=15,
    font=("Helvetica", 11, "bold")
).pack(pady=15)

# دکمه ریست
tk.Button(
    root,
    text="Reset",
    command=reset_fields,
    bg="#636e72",
    fg="white",
    width=15
).pack()

# لیبل نمایش نتیجه
result_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 13),
    bg="#1e272e",
    fg="#f1c40f"
)
result_label.pack(pady=20)

# متن پایین برنامه
footer = tk.Label(
    root,
    text="Results are saved to bmi_results.csv",
    bg="#1e272e",
    fg="gray",
    font=("Helvetica", 8)
)
footer.pack(side="bottom", pady=10)

root.mainloop()  # اجرای برنامه
