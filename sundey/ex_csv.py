import csv
from pathlib import Path

CSV_FILE = Path("books.csv")
FIELDNAMES = ["id", "title", "author", "pages", "price"]


def load_books():
    """
    קורא את כל הספרים מה-CSV ומחזיר רשימה של מילונים
    """
    if not CSV_FILE.exists():
        return []

    with CSV_FILE.open(mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        books = list(reader)

    # להמיר סוגים (id, pages, price)
    for b in books:
        b["id"] = int(b["id"])
        b["pages"] = int(b["pages"])
        b["price"] = float(b["price"])

    return books


def save_books(books):
    """
    שומר רשימת ספרים (מילונים) חזרה ל-CSV
    מוחק תוכן קודם וכותב מחדש
    """
    with CSV_FILE.open(mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for b in books:
            writer.writerow(
                {
                    "id": b["id"],
                    "title": b["title"],
                    "author": b["author"],
                    "pages": b["pages"],
                    "price": b["price"],
                }
            )


def get_next_id(books):
    """
    מחשב ID הבא (max+1)
    """
    if not books:
        return 1
    return max(b["id"] for b in books) + 1


def add_book(title: str, author: str, pages: int, price: float):
    """
    הוספת ספר חדש ל-CSV
    """
    books = load_books()
    new_id = get_next_id(books)

    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "pages": pages,
        "price": price,
    }

    books.append(new_book)
    save_books(books)
    print(f"נוסף ספר חדש עם id={new_id}")
    return new_book


def get_book_by_id(book_id: int):
    """
    החזרת ספר לפי ID
    """
    books = load_books()
    for b in books:
        if b["id"] == book_id:
            return b
    return None


def show_all_books():
    """
    הדפסת כל הספרים
    """
    books = load_books()
    if not books:
        print("אין ספרים בקובץ.")
        return

    for b in books:
        print(
            f"ID: {b['id']} | כותרת: {b['title']} | מחבר: {b['author']} | "
            f"עמודים: {b['pages']} | מחיר: {b['price']}"
        )


def update_book_price(book_id: int, new_price: float):
    """
    עדכון מחיר ספר לפי ID
    """
    books = load_books()
    found = False
    for b in books:
        if b["id"] == book_id:
            b["price"] = new_price
            found = True
            break

    if not found:
        print(f"ספר עם ID {book_id} לא נמצא.")
        return False

    save_books(books)
    print(f"עודכן מחיר הספר ID={book_id} ל-{new_price}")
    return True


def delete_book(book_id: int):
    """
    מחיקת ספר לפי ID
    """
    books = load_books()
    new_books = [b for b in books if b["id"] != book_id]

    if len(new_books) == len(books):
        print(f"ספר עם ID {book_id} לא נמצא, לא נמחק.")
        return False

    save_books(new_books)
    print(f"ספר עם ID={book_id} נמחק.")
    return True


def book_exists(title: str) -> bool:
    """
    בדיקה אם קיים ספר עם כותרת מסוימת
    """
    books = load_books()
    for b in books:
        if b["title"] == title:
            return True
    return False


if __name__ == "__main__":
    # דוגמאות שימוש

    add_book("Harry Potter", "J.K. Rowling", 400, 79.9)
    add_book("1984", "George Orwell", 350, 59.9)

    show_all_books()

    print("קיים Harry Potter?", book_exists("Harry Potter"))
    print("קיים Blabla?", book_exists("Blabla"))

    update_book_price(1, 99.9)
    delete_book(2)

    show_all_books()
