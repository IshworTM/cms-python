import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv("../.env")

conn = psycopg2.connect(
    dbname=os.getenv("DBNAME"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT"),
)

cur = conn.cursor()


def add_contact():
    name = name_field.get()
    phone = phone_field.get()
    email = email_field.get()

    if name and phone and email:
        cur.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)",
            (name, phone, email),
        )
        conn.commit()
        messagebox.showinfo(
            "Success", f"{name} has been successfully added to your contacts."
        )
        clear_fields()
        load_contacts()
    else:
        messagebox.showerror("Error", "Please fill all the fields.")


def update_contacts():
    selected_item = contact_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No contact selected!!")
        return

    contact_id = contact_tree.item(selected_item[0], "values")[0]
    name = name_field.get()
    phone = phone_field.get()
    email = email_field.get()

    if name and phone and email:
        cur.execute(
            "UPDATE contacts SET name=%s, phone=%s, email=%s WHERE id=%s",
            (name, phone, email, contact_id),
        )
        conn.commit()
        messagebox.showinfo("Success", "Contact updated successfully!")
        clear_fields()
        load_contacts()
    else:
        messagebox.showerror("Error", "All fields are required!")


def delete_contacts():
    contact_to_delete = contact_tree.selection()
    if not contact_to_delete:
        messagebox.showerror("Error", "No contact selected.")
        return

    contact_id = contact_tree.item(contact_to_delete[0], "values")[0]
    name = name_field.get()
    cur.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
    conn.commit()
    messagebox.showinfo("Success", f"{name} was removed from your contacts.")
    load_contacts()


def load_contacts():
    for row in contact_tree.get_children():
        contact_tree.delete(row)

    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for row in rows:
        contact_tree.insert("", tk.END, values=row)


def clear_fields():
    name_field.delete(0, tk.END)
    phone_field.delete(0, tk.END)
    email_field.delete(0, tk.END)


def select_item(event):
    selected_item = contact_tree.selection()
    if selected_item:
        contact = contact_tree.item(selected_item[0], "values")
        name_field.delete(0, tk.END)
        name_field.insert(0, contact[1])
        phone_field.delete(0, tk.END)
        phone_field.insert(0, contact[2])
        email_field.delete(0, tk.END)
        email_field.insert(0, contact[3])


root = tk.Tk()
root.title("Contact Management System (CMS)")
root.geometry("750x300")

tk.Label(root, text="Name:").grid(row=0, column=0)
name_field = tk.Entry(root)
name_field.grid(row=0, column=1)

tk.Label(root, text="Phone:").grid(row=1, column=0)
phone_field = tk.Entry(root)
phone_field.grid(row=1, column=1)

tk.Label(root, text="Email:").grid(row=2, column=0)
email_field = tk.Entry(root)
email_field.grid(row=2, column=1)

tk.Button(root, text="Add Contact", command=add_contact).grid(
    row=3, column=0, columnspan=2
)
tk.Button(root, text="Update Contact", command=update_contacts).grid(
    row=4, column=0, columnspan=2
)
tk.Button(root, text="Delete Contact", command=delete_contacts).grid(
    row=5, column=0, columnspan=2
)

columns = ("ID", "Name", "Email", "Phone")
contact_tree = ttk.Treeview(root, columns=columns, show="headings")
contact_tree.heading("ID", text="ID")
contact_tree.heading("Name", text="Name")
contact_tree.heading("Phone", text="Phone")
contact_tree.heading("Email", text="Email")
contact_tree.grid(row=6, column=0, columnspan=2, sticky="nsew")
contact_tree.bind("<ButtonRelease-1>", select_item)

load_contacts()

root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

cur.close()
conn.close()
