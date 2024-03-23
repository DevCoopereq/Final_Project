from datetime import date, datetime, timedelta


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
        membership_number = input("Enter nembership number: ")
        if len(membership_number) != 6 or membership_number.isnumeric() == False:
            print(
                "Invalid Membership number. [Number must be numeric and 6 digits long.]")
            continue
        else:
            return membership_number


def get_user_books(user_name="", user_id=""):
    user_book = []
    if len(user_name) > 0 or len(user_id) > 0:
        with open("borrowed_books.txt", "r") as file:
            for line in file:
                entry = line.strip()
                parts = entry.split("==")

                if len(parts) == 4:
                    users_name, user_membership, book_title, borrow_date = parts
                    if user_name == users_name or user_id == user_membership:
                        user_book.append(
                            {"user_name": parts[0], "user_id": parts[1], "book_title": parts[2], "borrow_date": parts[3]})
        return user_book
    return None


def get_book(title):
    with open("book_inventory.txt", "r") as file:
        for line in file:
            if title in line:
                parts = line.strip().split("==")
                if len(parts) < 4:
                    return None
                return {"title": parts[0], "author": parts[1], "in_stock": parts[2], "borrowed": parts[3]}


def add_new_book():
    # TODO Validation
    print("-Add new book to inventory-")
    title = input("Book title: ")
    author = input("Author: ")
    copies = input("Copies available: ")
    borrowed = input("Copies borrowed: ")

    with open("book_inventory.txt", "a") as file:
        file.write(f"\n{title}=={author}=={copies}=={borrowed}")


def get_books():
    with open("book_inventory.txt", "r") as file:
        for line in file:
            parts = line.strip().split("==")
            if len(parts) < 4:
                return
            book = {"title": parts[0], "author": parts[1],
                    "in_stock": parts[2], "borrowed": parts[3]}
            print(
                f"{book['title']} written by {book['author']}.[{book['in_stock']}] copies available.")


def get_borrowed_books():
    with open("borrowed_books.txt", "r") as file:
        for line in file:
            parts = line.strip().split("==")
            if len(parts) < 4:
                return
            book = {"user": parts[0], "user_id": parts[1],
                    "book_title": parts[2], "borrow_date": parts[3]}

            borrow_date_obj = datetime.strptime(
                book['borrow_date'], "%Y-%m-%d")
            due_date = (borrow_date_obj + timedelta(days=7)
                        ).strftime("%Y-%m-%d")
            book["due_date"] = due_date
            print(
                f"{book['book_title']} borrowed by {book['user']} from {book['borrow_date']} to {book['due_date']}")


def update_inventory(title, stock, borrowed):
    with open("book_inventory.txt", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if title in line:
            book_title, author, in_stock, out_stock = lines[i].strip().split(
                "==")
            lines[i] = f"{book_title}=={author}=={stock}=={borrowed}\n"
            break
    with open("book_inventory.txt", "w") as file:
        file.writelines(lines)


def update_borrowed_books(user, book, remove=False):
    with open("borrowed_books.txt", "r") as file:
        lines = file.readlines()

    with open("borrowed_books.txt", "w") as file:
        if remove == True:
            for line in lines:
                buf = line.strip("\n")
                if buf.find(user["name"]) == -1 and buf.find(book) == -1:
                    file.write(line)
        else:
            lines.append(
                f"{user['name']}=={user['memberID']}=={book}=={date.today()}\n")
            file.writelines(lines)


def borrow_book():

    # Get name
    user_name = get_user_name()
    # Get Membership Number
    membership_number = get_user_ID()
    # Get a Book title
    while True:
        get_books()
        book_title = input("Enter the book title you want to borrow: ")
        # Ensure the book title entered is valid.
        book = get_book(book_title)
        if book is None:
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
    user_name = get_user_name()
    user_ID = get_user_ID()
    user_books = get_user_books(user_name, user_ID)
    user_return_book = ""

    if len(user_books) <= 0:
        print("You did not borrow any book.")
        return

    for book in user_books:
        print(
            f"Title: {book['book_title']}\nDate of borrowing: {book['borrow_date']}\n\n")

    user_return_book = input("Which book you wish to return? : ")
    for book in user_books:
        if book["book_title"] is user_return_book:
            print("You did not borrowed that book.")
            return
        # Get book from inventor"y
        book_inv = get_book(book["book_title"])
        book["in_stock"] = book_inv["in_stock"]
        book["borrowed"] = book_inv["borrowed"]
        user_return_book = book
    date_diff = datetime.today() - \
        datetime.strptime(user_return_book['borrow_date'], "%Y-%m-%d")
    if date_diff.days > 7:
        print("The book is overdue its return date!\n"
              "You must pay penalty of 2 euros per each additional day,after its due date.\n"
              f"Which is - €{date_diff.days*2}"
              )
    update_borrowed_books(
        {"name": user_name, "memberID": user_ID}, user_return_book["book_title"], True)
    update_inventory(user_return_book["book_title"], int(
        user_return_book["in_stock"])+1, int(user_return_book["borrowed"])-1)


def review_borrowed_books():
    choice = input("1. Review all borrowed books\n"
                   "2. Review borrowed books by Membership Number\n"
                   ": "
                   )
    match choice:
        case "1":
            get_borrowed_books()
        case "2":
            user_books = get_user_books("None", get_user_ID())

            for book in user_books:
                borrow_date_obj = datetime.strptime(
                    book['borrow_date'], "%Y-%m-%d")
                due_date = (borrow_date_obj + timedelta(days=7)
                            ).strftime("%Y-%m-%d")
                book["due_date"] = due_date
                print(
                    f"{book['book_title']} borrowed by {book['user_name']} from {book['borrow_date']} to {book['due_date']}")


def manage_inventory():
    print("===Book Stock===\n")
    with open("book_inventory.txt", "r") as file:
        for line in file:
            print(line.strip().split("=="))
    print("\n===Book Stock===")

    print("===Admin Panel===\n")
    choice = input(" 1.Add a new book\n"
                   " 2.Remove a book from inventory\n"
                   " 3.Update the total copies available, and copies borrowed\n"
                   " 0.Return\n")
    match choice:
        case "1":
            add_new_book()
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


# borrow_book()0
# get_books()
# return_book()
# get_borrowed_books()
# review_borrowed_books()
# manage_inventory()
main()
