

def borrow_book():
    print("Borrow book")


def return_book():
    print("Return book")


def review_borrowed_books():
    print("Review borrowed books")


def manage_inventory():
    print("Manage inventory")


def main():
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


main()
