import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import csv
from datetime import datetime

# -----------------------------
# BMI Calculation
# -----------------------------
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# -----------------------------
# BMI Category
# -----------------------------
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# -----------------------------
# Save to CSV
# -----------------------------
def save_to_csv(weight, height, bmi, category):
    with open("bmi_results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), weight, height, round(bmi,2), category])

# -----------------------------
# Modern Pie Chart with Refresh Button
# -----------------------------
def show_pie_chart(bmi):

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    categories = ["Underweight", "Normal", "Overweight", "Obese"]
    colors = ["#3498db", "#2ecc71", "#f39c12", "#e74c3c"]

    # Determine index
    if bmi < 18.5:
        index = 0
    elif bmi < 25:
        index = 1
    elif bmi < 30:
        index = 2
    else:
        index = 3

    sizes = [0.1, 0.1, 0.1, 0.1]
    sizes[index] = 1

    wedges, texts = ax.pie(
        sizes,
        labels=categories,
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.5)
    )

    ax.set_title(f"Your BMI: {bmi:.2f}", fontsize=14, fontweight="bold")

    # -------------------------
    # Refresh Button inside graph
    # -------------------------
    ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
    button = Button(ax_button, 'Refresh')

    def refresh(event):
        plt.close(fig)

    button.on_clicked(refresh)

    plt.show()

# -----------------------------
# Main Calculate Function
# -----------------------------
def calculate():

    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Values must be positive numbers.")
            return

        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)

        result_label.config(
            text=f"Your BMI: {bmi:.2f}\nCategory: {category}"
        )

        save_to_csv(weight, height, bmi, category)
        show_pie_chart(bmi)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# -----------------------------
# Reset Fields
# -----------------------------
def reset_fields():
    entry_weight.delete(0, tk.END)
    entry_height.delete(0, tk.END)
    result_label.config(text="")

# -----------------------------
# Modern GUI Design
# -----------------------------
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x420")
root.configure(bg="#1e272e")
root.resizable(False, False)

title = tk.Label(
    root,
    text="BMI Calculator",
    font=("Helvetica", 18, "bold"),
    bg="#1e272e",
    fg="white"
)
title.pack(pady=20)

tk.Label(root, text="Weight (kg)", bg="#1e272e", fg="white").pack()
entry_weight = tk.Entry(root, font=("Helvetica", 12), justify="center")
entry_weight.pack(pady=5)

tk.Label(root, text="Height (m)", bg="#1e272e", fg="white").pack()
entry_height = tk.Entry(root, font=("Helvetica", 12), justify="center")
entry_height.pack(pady=5)

tk.Button(
    root,
    text="Calculate",
    command=calculate,
    bg="#00cec9",
    fg="black",
    width=15,
    font=("Helvetica", 11, "bold")
).pack(pady=15)

tk.Button(
    root,
    text="Reset",
    command=reset_fields,
    bg="#636e72",
    fg="white",
    width=15
).pack()

result_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 13),
    bg="#1e272e",
    fg="#f1c40f"
)
result_label.pack(pady=20)

footer = tk.Label(
    root,
    text="Results are saved to bmi_results.csv",
    bg="#1e272e",
    fg="gray",
    font=("Helvetica", 8)
)
footer.pack(side="bottom", pady=10)

root.mainloop()
