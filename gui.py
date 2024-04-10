import tkinter as tk
from tkinter import ttk, Frame
import book_inventory as bi

entries = []


def destroy():
    btn_borrow.pack_forget()
    btn_return.pack_forget()
    btn_review.pack_forget()
    btn_manage.pack_forget()
    for e in entries:
        e.pack_forget()


def show_borrow():
    destroy()
    print("Showing borrow function")
    frm = Frame(app)
    frm.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    tv = ttk.Treeview(frm, columns=(1, 2, 3, 4), show="headings", height=5)

    tv.heading(1, text="Title")
    tv.heading(2, text="Author")
    tv.heading(3, text="Available")
    tv.heading(4, text="Borrowed")

    books = bi.get_books()
    # books_reformatted = ""
    for b in books:
        # books_reformatted += f"{b['title']:20s}  {b['author']:20s} {b['in_stock']:15s} {b['borrowed']:15s}\n"
        tv.insert("", tk.END, values=(
                  b['title'], b['author'], b['in_stock'], b['borrowed']))

    tv.pack()
    # tk.Label(app, text=books_reformatted,).pack()

    username_input = tk.Entry(app)
    username_input_label = tk.Label(app, text="Your name:")
    username_input_label.pack()
    username_input.pack()
    entries.append(username_input)

    membership_input = tk.Entry(app)
    membership_input_label = tk.Label(app, text="Membership number:")
    membership_input_label.pack()
    membership_input.pack()
    entries.append(membership_input)

    book_input = tk.Entry(app)
    book_input_label = tk.Label(app, text="Book title:")
    book_input_label.pack()
    book_input.pack()
    entries.append(book_input)

    btn_submit = tk.Button(
        app, command=lambda: borrow_click(username_input.get(), membership_input.get(), book_input.get()), text="Borrow")
    btn_submit.pack()
    entries.append(btn_submit)


def borrow_click(user, membership, book_title):
    lbl_error.pack_forget()
    borrow_succes = bi.borrow_book(user, membership, book_title)

    if borrow_succes == 1:
        show_menu()
    if borrow_succes == 0:
        lbl_error.config(text=lbl_error.cget("text")+"\nEnter valid name.")
    if borrow_succes == 00:
        lbl_error.config(text=lbl_error.cget("text") +
                         "\nEnter valid membership number.")
    if borrow_succes == -1:
        lbl_error.config(text=lbl_error.cget("text") +
                         "\nWe do not have that book.")
    if borrow_succes == -2:
        lbl_error.config(text=lbl_error.cget("text") +
                         "\nSorry but we do not have that book in the inventory.")

    lbl_error.pack()


def show_return():
    print("Saying hello")


def show_review():
    print("Saying hello")


def show_manage():
    print("Saying hello")


def show_menu():
    destroy()
    print(app.winfo_width(), app.winfo_height())
    btn_borrow.pack(side=tk.TOP, padx=5)
    btn_return.pack(side=tk.TOP, padx=5)
    btn_review.pack(side=tk.TOP, padx=5)
    btn_manage.pack(side=tk.TOP, padx=5)


app = tk.Tk()
app.title("Book Inventory")
app.geometry("860x500")

btn_borrow = tk.Button(app, text="Borrow a book",
                       command=show_borrow, width=20)
btn_return = tk.Button(app, text="Return a book",
                       command=show_return, width=20)
btn_review = tk.Button(app, text="Review borrowed books",
                       command=show_review, width=20)
btn_manage = tk.Button(app, text="Manage Inventory",
                       command=show_manage, width=20)


lbl_error = tk.Label(app, text="", fg='#FF0000')

show_menu()

btn_back = tk.Button(app, text="Back", command=show_menu, width=20)
btn_back.pack(side=tk.BOTTOM)

app.mainloop()
