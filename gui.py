import tkinter as tk


def show_borrow():
    print("Showing borrow function")


def show_return():
    print("Saying hello")


def show_review():
    print("Saying hello")


def show_manage():
    print("Saying hello")


app = tk.Tk()
app.title("Book Inventory")

btn_borrow = tk.Button(app, text="Borrow a book",
                       command=show_borrow, width=20)
btn_return = tk.Button(app, text="Return a book",
                       command=show_return, width=20)
btn_review = tk.Button(app, text="Review borrowed books",
                       command=show_review, width=20)
btn_manage = tk.Button(app, text="Manage Inventory",
                       command=show_manage, width=20)

btn_borrow.pack(side=tk.TOP, padx=5, pady=5)
btn_return.pack(side=tk.TOP, padx=5, pady=5)
btn_review.pack(side=tk.TOP, padx=5, pady=5)
btn_manage.pack(side=tk.TOP, padx=5, pady=5)

app.mainloop()
