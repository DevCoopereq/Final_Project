from datetime import date, datetime, timedelta


def validate_user_name(user_name):
    """
    Validates user name.

    Returns:
        string: valid user name
    """
    if len(user_name) > 0 and len(user_name) < 20:
        return True
    else:
        return False


def validate_user_ID(membership_number):
    """
    Validates user's membership number.

    Returns:
        string: valid membership number.
    """
    if len(membership_number) != 6 or membership_number.isnumeric() == False:
        print(
            "Invalid Membership number. [Number must be numeric and 6 digits long.]")
        return False
    else:
        return True


def validate_book_title(book_title):
    print("is tru", len(book_title) <= 0)
    # Ensure the book title entered is valid.
    if len(book_title) <= 0:
        return -1
    book = get_book(book_title)
    if book is None:
        print("We do not have that book.")
        return -1
    elif int(book["in_stock"]) == 0:
        print("Sorry but we do not have that book in the inventory.")
        return -2
    else:
        return True, 0


def get_user_books(user_name="", user_id=""):
    """
    Gets all books borrowed by user.

    Args:
        user_name (str, optional): User name.
        user_id (str, optional): User Membership number.

    Returns:
        list: Collection of borrowed books
    """
    user_book = []
    if len(user_name) > 0 or len(user_id) > 0:
        with open("borrowed_books.txt", "r", encoding="utf-8") as file:
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
    """
    Reads book data from book_inventory.txt

    Args:
        title (string): book title

    Returns:
        dictionary: data containing information about book.
    """
    with open("book_inventory.txt", "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("==")
            if len(parts) == 4 and parts[0] == title:
                return {"title": parts[0], "author": parts[1], "in_stock": parts[2], "borrowed": parts[3]}
    return None


def admin_add_new_book():
    """
    Adds new book to the book_inventory.txt file
    """
    # TODO Validation
    print("-Add new book to inventory-")
    title = input("Book title: ")
    author = input("Author: ")
    copies = input("Copies available: ")
    borrowed = input("Copies borrowed: ")

    with open("book_inventory.txt", "a", encoding="utf-8") as file:
        file.write(f"\n{title}=={author}=={copies}=={borrowed}")

    print(f"{title} has been added succesfully.")


def admin_remove_book():
    """
    Removes book from book_inventory.txt file
    """
    # TODO Validation
    print("-Remove from inventory-")
    title = input("Book title: ")
    with open("book_inventory.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open("book_inventory.txt", "w", encoding="utf-8") as file:
        for line in lines:
            if title in line:
                print(f"{title} has been removed succesfully.")
                return
            else:
                file.write(line)
    print("The book the book was not removed.")


def admin_update_inventory():
    """
    Updates available copies, and borrowed copies in book_inventory.txt
    """
    # Validation
    books = get_books()
    title = input("\nWhich book you wish to edit: ")
    for book in books:
        if book["title"] == title:
            print(f"####Editing {book['title']} by {book['author']}####")
            copies = input("Enter new number of available copies: ")
            borrowed = input("Enter new number of borrowed copies: ")
            update_inventory(book['title'], copies, borrowed)
            return

    print("We do not have that book.")


def get_books():
    """
    Prints information about books.
    Get books from book_inventory.txt

    Returns:
        dictionary: 'book_title', 'author','in_stock','borrowed'
    """
    with open("book_inventory.txt", "r", encoding="utf-8") as file:
        books = []
        for line in file:
            parts = line.strip().split("==")
            if len(parts) < 4:
                return
            book = {"title": parts[0], "author": parts[1],
                    "in_stock": parts[2], "borrowed": parts[3]}
            print(
                f"{book['title']} written by {book['author']}. Stock:[{book['in_stock']}] Borrowed:[{book['borrowed']}]")
            books.append(book)
        return books


def get_borrowed_books():
    """
    Reads books from borrowed_books.txt
    Prints information about books.
    """
    with open("borrowed_books.txt", "r", encoding="utf-8") as file:
        if len(file.readlines()) == 0:
            print("Nobody borrowed any book yet.")
            return
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
    """
    Updates inventory
    Args:
        title (string): Book title
        stock (string): Copies in inventory
        borrowed (string): Copies borrowed.
    """
    with open("book_inventory.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if title in line:
            parts = lines[i].strip().split(
                "==")

            if len(parts) >= 2:
                book_title, author, in_stock, out_stock = parts
                lines[i] = f"{book_title}=={author}=={stock}=={borrowed}\n"
                break
    with open("book_inventory.txt", "w", encoding="utf-8") as file:
        file.writelines(lines)


def update_borrowed_books(user, book, remove=False):
    """
    Adds/Removes entry in borrowed_books.txt

    Args:
        user (string): User name
        book (string): Book title
        remove (bool, optional): True if book must be removed. Defaults to False.
    """
    with open("borrowed_books.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open("borrowed_books.txt", "w", encoding="utf-8") as file:
        if remove is True:
            for line in lines:
                buf = line.strip("\n")
                if buf.find(user["name"]) == -1 and buf.find(book) == -1:
                    file.write(line)
        else:
            lines.append(
                f"{user['name']}=={user['memberID']}=={book}=={date.today()}\n")
            file.writelines(lines)


def borrow_book(user_name, membership_number, book_title):
    """
    Checks if user can borrow book,if so update inventory and borrowed book.

    Args:
        user_name (string): User name
        membership_number (string): Membership ID
        book_title (string): Book title 

    Returns:
        int 0: Invalid user name
        int 00: Invalid membership number
        int -1: If book was not found
        int -2: If there is not available copies
        int 1: If succesfully borrowed
    """

    if validate_user_name(user_name) is False:
        return 0
    if validate_user_ID(membership_number) is False:
        return 00

    is_book_valid = validate_book_title(book_title)
    if validate_book_title(book_title) is False:
        return 000
    if is_book_valid == -1:
        return -1
    elif is_book_valid == -2:
        return -2
    book = get_book(book_title)

    update_inventory(book["title"], int(
        book["in_stock"])-1, int(book["borrowed"])+1)
    print(
        f"You have borrowed {book['title']} written by {book['author']}, please return a book back in 7 days.")
    update_borrowed_books(
        {"name": user_name, "memberID": membership_number},
        book["title"])
    return 1


def return_book():
    """
    Let's user return book

    """
    user_name = validate_user_name()
    user_ID = validate_user_ID()
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
    """
    Let's user review all borrowed books or specific users borrowed books
    """
    choice = input("1. Review all borrowed books\n"
                   "2. Review borrowed books by Membership Number\n"
                   ": "
                   )
    match choice:
        case "1":
            get_borrowed_books()
        case "2":
            user_books = get_user_books("None", validate_user_ID())

            for book in user_books:
                borrow_date_obj = datetime.strptime(
                    book['borrow_date'], "%Y-%m-%d")
                due_date = (borrow_date_obj + timedelta(days=7)
                            ).strftime("%Y-%m-%d")
                book["due_date"] = due_date
                print(
                    f"{book['book_title']} borrowed by {book['user_name']} from {book['borrow_date']} to {book['due_date']}")


def manage_inventory():
    """
    Manage inventory menu
    """
    print("===Book Stock===\n")
    get_books()
    print("\n===Book Stock===")

    choice = input("===Admin Panel===\n"
                   " 1.Add a new book\n"
                   " 2.Remove a book from inventory\n"
                   " 3.Update the total copies available, and copies borrowed\n"
                   " 0.Return\n"
                   "===Admin Panel===\n")
    match choice:
        case "1":

            admin_add_new_book()
        case "2":
            admin_remove_book()
        case "3":
            admin_update_inventory()
        case "0":
            return


def main():
    """
    Main function
    """
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
# main()
