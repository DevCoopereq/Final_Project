from datetime import date


def get_user_name():
    # Get name
    while True:
        user_name = input("Enter your name: ")
        if len(user_name) <= 0 or len(user_name) > 20:
            print("Invalid Name.")
            continue
        else:
            return user_name


def get_user_ID():
    # Get Membership Number
    while True:
        membership_number = input("Enter your nembership number: ")
        if len(membership_number) != 6 or membership_number.isnumeric() == False:
            print(
                "Invalid Membership number. [Number must be numeric and 6 digits long.]")
            continue
        else:
            return membership_number


def get_book(title):
    with open("book_inventory.txt", "r") as file:
        for line in file:
            if title in line:
                parts = line.strip().split("-")
                return {"title": parts[0], "author": parts[1], "in_stock": parts[2], "borrowed": parts[3]}


def update_inventory(title, stock, borrowed):
    with open("book_inventory.txt", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if title in line:
            book_title, author, in_stock, out_stock = lines[i].strip().split(
                "-")
            lines[i] = f"{book_title}-{author}-{stock}-{borrowed}\n"
            break
    with open("book_inventory.txt", "w") as file:
        file.writelines(lines)


def update_borrowed_books(user, book):
    with open("borrowed_books.txt", "r") as file:
        lines = file.readlines()

    lines.append(f"{user['name']}-{user['memberID']}-{book}-{date.today()}\n")
    with open("borrowed_books.txt", "w") as file:
        file.writelines(lines)


def borrow_book():

    # Get name
    user_name = get_user_name()
    # Get Membership Number
    membership_number = get_user_ID()
    # Get a Book title
    while True:
        book_title = input("Enter the book title you want to borrow: ")
        # Ensure the book title entered is valid.
        book = get_book(book_title)
        if book == None:
            print("We do not have that book.")
            return
        if int(book["in_stock"]) == 0:
            print("Sorry but we do not have that book in the inventory.")
            return
        update_inventory(book["title"], int(
            book["in_stock"])-1, int(book["borrowed"])+1)
        print(
            f"You have borrowed {book['title']} written by {book['author']}, please return a book back in 7 days.")
        update_borrowed_books(
            {"name": user_name, "memberID": membership_number},
            book["title"])
        return


def return_book():
    print(":")


def review_borrowed_books():
    print("Review borrowed books")


def manage_inventory():
    print("===Book Stock===\n")
    with open("book_inventory.txt", "r") as file:
        for line in file:
            print(line.strip())
    print("\n===Book Stock===")

    print("===Admin Panel===\n")
    choice = input(" 1.Add a new book\n"
                   " 2.Remove a book from inventory\n"
                   " 3.Update the total copies available, and copies borrowed\n"
                   " 0.Return\n")
    match choice:
        case "1":
            borrow_book()
        case "2":
            return_book()
        case "3":
            review_borrowed_books()
        case "4":
            manage_inventory()
        case "0":
            return
    print("\n===Admin Panel===")


def main():
    while True:
        choice = input("|-Book Inventory-|\n"
                       " 1.Borrow book\n"
                       " 2.Return a book\n"
                       " 3.Review Borrowed Books\n"
                       " 4.Manage Inventory\n"
                       " 0.Exit\n")
        match choice:
            case "1":
                borrow_book()
            case "2":
                return_book()
            case "3":
                review_borrowed_books()
            case "4":
                manage_inventory()
            case "0":
                return


borrow_book()
