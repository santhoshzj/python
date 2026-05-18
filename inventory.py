import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ================= DATABASE CONNECTION =================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Santhosh$1010",   # Replace with your MySQL password
    database="inventory_db"
)

cursor = db.cursor()

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("1250x720")
root.config(bg="#dbeafe")
root.resizable(False, False)

# ================= STYLE =================
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="black",
    rowheight=28,
    fieldbackground="white",
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 11, "bold"),
    background="#2563eb",
    foreground="white"
)

style.map("Treeview", background=[("selected", "#93c5fd")])

# ================= FUNCTIONS =================
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_supplier.delete(0, tk.END)

def add_product():
    name = entry_name.get()
    category = entry_category.get()
    price = entry_price.get()
    quantity = entry_quantity.get()
    supplier = entry_supplier.get()

    if name == "" or category == "" or price == "" or quantity == "":
        messagebox.showerror("Error", "Please fill all required fields")
        return

    try:
        sql = """
        INSERT INTO products (product_name, category, price, quantity, supplier)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (name, category, price, quantity, supplier)

        cursor.execute(sql, values)
        db.commit()

        messagebox.showinfo("Success", "Product Added Successfully")
        clear_fields()
        show_products()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def show_products():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

def delete_product():
    selected = tree.focus()

    if not selected:
        messagebox.showerror("Error", "Select a product first")
        return

    data = tree.item(selected)
    product_id = data["values"][0]

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure?")

    if confirm:
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        db.commit()

        messagebox.showinfo("Deleted", "Product Deleted Successfully")
        show_products()
        clear_fields()

def update_product():
    selected = tree.focus()

    if not selected:
        messagebox.showerror("Error", "Select a product first")
        return

    product_id = tree.item(selected)["values"][0]

    sql = """
    UPDATE products
    SET product_name=%s, category=%s, price=%s, quantity=%s, supplier=%s
    WHERE id=%s
    """

    values = (
        entry_name.get(),
        entry_category.get(),
        entry_price.get(),
        entry_quantity.get(),
        entry_supplier.get(),
        product_id
    )

    cursor.execute(sql, values)
    db.commit()

    messagebox.showinfo("Updated", "Product Updated Successfully")
    show_products()
    clear_fields()

def search_product():
    search_value = entry_search.get()

    for row in tree.get_children():
        tree.delete(row)

    sql = """
    SELECT * FROM products
    WHERE product_name LIKE %s
    OR category LIKE %s
    OR supplier LIKE %s
    """

    values = (
        "%" + search_value + "%",
        "%" + search_value + "%",
        "%" + search_value + "%"
    )

    cursor.execute(sql, values)
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

def select_product(event):
    selected = tree.focus()

    if not selected:
        return

    values = tree.item(selected, "values")

    if not values:
        return

    clear_fields()

    entry_name.insert(0, values[1])
    entry_category.insert(0, values[2])
    entry_price.insert(0, values[3])
    entry_quantity.insert(0, values[4])
    entry_supplier.insert(0, values[5])

# ================= TITLE =================
title = tk.Label(
    root,
    text="INVENTORY MANAGEMENT SYSTEM",
    font=("Segoe UI", 24, "bold"),
    bg="#1d4ed8",
    fg="white",
    pady=15
)
title.pack(fill="x")

# ================= FORM FRAME =================
form_frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
form_frame.place(x=20, y=90, width=1200, height=220)

# Labels + Entries
labels = ["Product Name", "Category", "Price", "Quantity", "Supplier"]
y_positions = [20, 60, 100, 140, 180]

entries = []

for i, label in enumerate(labels):
    tk.Label(
        form_frame,
        text=label,
        font=("Segoe UI", 11, "bold"),
        bg="white"
    ).place(x=20, y=y_positions[i])

# Entry Fields
entry_name = tk.Entry(form_frame, font=("Segoe UI", 11), width=30)
entry_name.place(x=160, y=20)

entry_category = tk.Entry(form_frame, font=("Segoe UI", 11), width=30)
entry_category.place(x=160, y=60)

entry_price = tk.Entry(form_frame, font=("Segoe UI", 11), width=30)
entry_price.place(x=160, y=100)

entry_quantity = tk.Entry(form_frame, font=("Segoe UI", 11), width=30)
entry_quantity.place(x=160, y=140)

entry_supplier = tk.Entry(form_frame, font=("Segoe UI", 11), width=30)
entry_supplier.place(x=160, y=180)

# Search
tk.Label(
    form_frame,
    text="Search Product",
    font=("Segoe UI", 11, "bold"),
    bg="white"
).place(x=700, y=30)

entry_search = tk.Entry(form_frame, font=("Segoe UI", 11), width=25)
entry_search.place(x=850, y=30)

tk.Button(
    form_frame,
    text="Search",
    font=("Segoe UI", 10, "bold"),
    bg="#f59e0b",
    fg="white",
    width=15,
    command=search_product
).place(x=850, y=70)

# Buttons
buttons = [
    ("Add Product", add_product, "#16a34a"),
    ("Update Product", update_product, "#2563eb"),
    ("Delete Product", delete_product, "#dc2626"),
    ("Show All", show_products, "#7c3aed"),
    ("Clear", clear_fields, "#374151")
]

x_pos = 520

for text, cmd, color in buttons:
    tk.Button(
        form_frame,
        text=text,
        command=cmd,
        font=("Segoe UI", 10, "bold"),
        bg=color,
        fg="white",
        width=15,
        relief="flat"
    ).place(x=x_pos, y=150)
    x_pos += 130

# ================= TABLE FRAME =================
table_frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
table_frame.place(x=20, y=330, width=1200, height=360)

# Vertical Scrollbar
scroll_y = tk.Scrollbar(table_frame, orient="vertical")

# Treeview Table
columns = ("ID", "Product Name", "Category", "Price", "Quantity", "Supplier", "Date Added")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=scroll_y.set
)

scroll_y.config(command=tree.yview)
scroll_y.pack(side="right", fill="y")

tree.pack(fill="both", expand=True)

# Headings
for col in columns:
    tree.heading(col, text=col)

# Column Widths
tree.column("ID", width=60, anchor="center")
tree.column("Product Name", width=220)
tree.column("Category", width=150)
tree.column("Price", width=100, anchor="center")
tree.column("Quantity", width=100, anchor="center")
tree.column("Supplier", width=220)
tree.column("Date Added", width=180)

# Bind click
tree.bind("<ButtonRelease-1>", select_product)

# ================= INITIAL LOAD =================
show_products()

# ================= RUN APP =================
root.mainloop()