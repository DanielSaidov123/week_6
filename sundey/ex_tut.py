from datetime import datetime
from typing import Optional, Iterable

from sqlmodel import SQLModel, Field, Session, create_engine, select, func

# ---------------------------------------------------------
# הגדרת חיבור ל-MySQL
# שים לב: אתה חייב ליצור קודם DB בשם bookstore_db ב-MySQL:
#   CREATE DATABASE bookstore_db;
# ---------------------------------------------------------

DB_URL = "mysql+pymysql://root@localhost:3306/bookstore_db"
# אם יש לך סיסמה ל-root:
# DB_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/bookstore_db"

engine = create_engine(DB_URL, echo=True)


# ---------------------------------------------------------
# חלק 1 + חלק 3 – מודל Book עם כל השדות וההגבלות
# ---------------------------------------------------------

class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: Optional[int] = Field(default=None, primary_key=True)

    # title - כותרת הספר, מינימום 2 תווים, מקסימום 200
    title: str = Field(min_length=2, max_length=200, nullable=False)

    # author - שם המחבר, מינימום 2 תווים, מקסימום 100
    author: str = Field(min_length=2, max_length=100, nullable=False)

    # pages - מספר עמודים בין 1 ל-5000
    pages: int = Field(ge=1, le=5000, nullable=False)

    # price - מחיר בין 0.01 ל-999.99
    price: float = Field(ge=0.01, le=999.99, nullable=False)

    # isbn - מחרוזת עד 20 תווים, אופציונלי, ייחודי
    isbn: Optional[str] = Field(
        default=None,
        max_length=20,
        unique=True,
        index=True
    )

    # publication_year - שנה בין 1000 ל-2030 (אופציונלי)
    publication_year: Optional[int] = Field(default=None, ge=1000, le=2030)

    # in_stock - האם במלאי, ברירת מחדל True
    in_stock: bool = Field(default=True)

    # created_at - תאריך יצירה אוטומטי
    created_at: datetime = Field(default_factory=datetime.now)


# יצירת הטבלה ב-DB אם לא קיימת
SQLModel.metadata.create_all(engine)


# ---------------------------------------------------------
# חלק 1 – פונקציות CRUD בסיסיות
# ---------------------------------------------------------

def add_book(title: str, author: str, pages: int, price: float) -> Book:
    """
    ליגרת 1.3 – הוספת ספר ראשון
    """
    with Session(engine) as session:
        book = Book(
            title=title,
            author=author,
            pages=pages,
            price=price
        )
        session.add(book)
        session.commit()
        session.refresh(book)
        print(f"נוסף ספר חדש עם id={book.id}")
        return book


def show_all_books() -> None:
    """
    ליגרת 1.4 – הצגת כל הספרים
    פורמט:
    ID: X | כותרת: Y | מחבר: Z | עמודים: W | מחיר: V
    """
    with Session(engine) as session:
        books = session.exec(select(Book)).all()

    if not books:
        print("אין ספרים במערכת.")
        return

    for b in books:
        print(
            f"ID: {b.id} | כותרת: {b.title} | מחבר: {b.author} | "
            f"עמודים: {b.pages} | מחיר: {b.price}"
        )


def get_book_by_id(book_id: int) -> Optional[Book]:
    """
    ליגרת 1.5 – חיפוש ספר לפי ID
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)

    if book is None:
        print(f"ספר עם ID {book_id} לא נמצא.")
        return None

    print(
        f"ID: {book.id} | כותרת: {book.title} | מחבר: {book.author} | "
        f"עמודים: {book.pages} | מחיר: {book.price}"
    )
    return book


def update_book_price(book_id: int, new_price: float) -> bool:
    """
    ליגרת 1.6 – עדכון מחיר ספר
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            print(f"ספר עם ID {book_id} לא נמצא.")
            return False

        book.price = new_price
        session.add(book)
        session.commit()
        session.refresh(book)
        print(f"עודכן מחיר הספר ID={book.id} ל-{book.price}")
        return True


def delete_book(book_id: int) -> bool:
    """
    ליגרת 1.7 – מחיקת ספר
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            print(f"ספר עם ID {book_id} לא נמצא, לא נמחק.")
            return False

        session.delete(book)
        session.commit()
        print(f"ספר עם ID={book_id} נמחק בהצלחה.")
        return True


def count_books() -> int:
    """
    ליגרת 1.8 – ספירת ספרים
    (לפי ההנחיה – להשתמש ב-len על רשימת ספרים)
    """
    with Session(engine) as session:
        books = session.exec(select(Book)).all()
        count = len(books)

    print(f"יש {count} ספרים במערכת.")
    return count


def add_books_from_list(books_list: Iterable[tuple[str, str, int, float]]) -> int:
    """
    ליגרת 1.9 – הוספת רשימת ספרים
    books_list – Iterable של טאפלים:
    (title, author, pages, price)
    """
    added = 0
    with Session(engine) as session:
        for title, author, pages, price in books_list:
            book = Book(
                title=title,
                author=author,
                pages=pages,
                price=price
            )
            session.add(book)
            added += 1
        session.commit()

    print(f"הוספו {added} ספרים חדשים.")
    return added


def book_exists(title: str) -> bool:
    """
    ליגרת 1.10 – בדיקת קיום ספר לפי כותרת
    """
    with Session(engine) as session:
        stmt = select(Book).where(Book.title == title)
        result = session.exec(stmt).first()

    exists = result is not None
    print(f"האם הספר '{title}' קיים? {exists}")
    return exists


# ---------------------------------------------------------
# חלק 2 – חיפושים ומיונים
# ---------------------------------------------------------

def find_books_by_author(author_name: str):
    """
    ליגרת 2.1 – חיפוש ספרים לפי מחבר
    """
    with Session(engine) as session:
        stmt = (
            select(Book)
            .where(Book.author == author_name)
            .order_by(Book.title)
        )
        books = session.exec(stmt).all()

    if not books:
        print(f"לא נמצאו ספרים של המחבר: {author_name}")
        return []

    for b in books:
        print(f"{b.id}: {b.title} ({b.price})")
    return books


def get_cheap_books(max_price: float):
    """
    ליגרת 2.2 – ספרים מתחת למחיר מסוים
    """
    with Session(engine) as session:
        stmt = (
            select(Book)
            .where(Book.price < max_price)
            .order_by(Book.price)  # מהזול ליקר
        )
        books = session.exec(stmt).all()

    if not books:
        print(f"לא נמצאו ספרים מתחת למחיר {max_price}.")
        return []

    for b in books:
        print(f"{b.id}: {b.title} - {b.price}")
    return books


def get_long_books(min_pages: int):
    """
    ליגרת 2.3 – ספרים ארוכים (יותר מ-min_pages)
    """
    with Session(engine) as session:
        stmt = (
            select(Book)
            .where(Book.pages >= min_pages)
            .order_by(Book.pages.desc())  # מהארוך לקצר
        )
        books = session.exec(stmt).all()

    if not books:
        print(f"לא נמצאו ספרים עם יותר מ-{min_pages} עמודים.")
        return []

    for b in books:
        print(f"{b.id}: {b.title} - {b.pages} עמודים")
    return books


def search_books(keyword: str):
    """
    ליגרת 2.4 – חיפוש חלקי בכותרת
    Book.title.contains(keyword)
    """
    with Session(engine) as session:
        stmt = select(Book).where(Book.title.contains(keyword))
        books = session.exec(stmt).all()

    if not books:
        print(f"לא נמצאו ספרים שהכותרת שלהם מכילה את: {keyword}")
        return []

    for b in books:
        print(f"{b.id}: {b.title}")
    return books


def books_in_price_range(min_price: float, max_price: float):
    """
    ליגרת 2.5 – ספרים בטווח מחירים
    price >= min_price AND price <= max_price
    """
    with Session(engine) as session:
        stmt = select(Book).where(
            (Book.price >= min_price) & (Book.price <= max_price)
        ).order_by(Book.price)
        books = session.exec(stmt).all()

    if not books:
        print(f"לא נמצאו ספרים בטווח מחירים {min_price} - {max_price}.")
        return []

    for b in books:
        print(f"{b.id}: {b.title} - {b.price}")
    return books


def get_most_expensive_book() -> Optional[Book]:
    """
    ליגרת 2.6 – הספר היקר ביותר
    """
    with Session(engine) as session:
        stmt = select(Book).order_by(Book.price.desc())
        book = session.exec(stmt).first()

    if book is None:
        print("אין ספרים במערכת.")
        return None

    print(f"הספר היקר ביותר: {book.title} - {book.price}")
    return book


def get_cheapest_book() -> Optional[Book]:
    """
    ליגרת 2.7 – הספר הזול ביותר
    """
    with Session(engine) as session:
        stmt = select(Book).order_by(Book.price)
        book = session.exec(stmt).first()

    if book is None:
        print("אין ספרים במערכת.")
        return None

    print(f"הספר הזול ביותר: {book.title} - {book.price}")
    return book


def calculate_average_price() -> Optional[float]:
    """
    ליגרת 2.8 – חישוב מחיר ממוצע של כל הספרים
    """
    with Session(engine) as session:
        avg_price = session.exec(select(func.avg(Book.price))).one_or_none()

    if avg_price is None or avg_price[0] is None:
        print("אין ספרים, אי אפשר לחשב ממוצע.")
        return None

    avg_value = float(avg_price[0])
    print(f"המחיר הממוצע של כל הספרים הוא: {avg_value}")
    return avg_value


def get_books_sorted_by_length(ascending: bool = True):
    """
    ליגרת 2.9 – מיון ספרים לפי אורך (מספר עמודים)
    ascending=True  -> מהקצר לארוך
    ascending=False -> מהארוך לקצר
    """
    order = Book.pages if ascending else Book.pages.desc()

    with Session(engine) as session:
        stmt = select(Book).order_by(order)
        books = session.exec(stmt).all()

    for b in books:
        print(f"{b.id}: {b.title} - {b.pages} עמודים")
    return books


def get_books_page(page_number: int, page_size: int = 10):
    """
    ליגרת 2.10 – Pagination
    page_number: מספר דף (1 מבוסס)
    page_size: כמה ספרים בכל דף
    """
    if page_number < 1:
        raise ValueError("page_number חייב להיות >= 1")

    offset_value = (page_number - 1) * page_size

    with Session(engine) as session:
        stmt = select(Book).offset(offset_value).limit(page_size)
        books = session.exec(stmt).all()

    print(f"דף {page_number} (גודל דף {page_size}):")
    for b in books:
        print(f"{b.id}: {b.title}")
    return books


# ---------------------------------------------------------
# חלק 3 – הרחבות ל-Book (ISBN, מלאי וכו')
# ---------------------------------------------------------

def add_book_with_isbn(title: str, author: str, pages: int,
                       price: float, isbn: str) -> Optional[Book]:
    """
    ליגרת 3.4 – הוספת ספר עם בדיקת ISBN ייחודי
    """
    with Session(engine) as session:
        # בדיקה אם כבר קיים ספר עם אותו ISBN
        existing = session.exec(
            select(Book).where(Book.isbn == isbn)
        ).first()

        if existing:
            print(f"ISBN {isbn} כבר קיים עבור הספר: {existing.title}")
            return None

        book = Book(
            title=title,
            author=author,
            pages=pages,
            price=price,
            isbn=isbn,
        )
        session.add(book)
        session.commit()
        session.refresh(book)
        print(f"נוסף ספר חדש עם ISBN {isbn} ו-id={book.id}")
        return book


def mark_out_of_stock(book_id: int) -> bool:
    """
    ליגרת 3.5 – סימון ספר כלא במלאי
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            print(f"ספר עם ID {book_id} לא נמצא.")
            return False

        book.in_stock = False
        session.add(book)
        session.commit()
        print(f"ספר ID={book_id} סומן כלא במלאי.")
        return True


def mark_in_stock(book_id: int) -> bool:
    """
    ליגרת 3.5 – סימון ספר כבמלאי
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            print(f"ספר עם ID {book_id} לא נמצא.")
            return False

        book.in_stock = True
        session.add(book)
        session.commit()
        print(f"ספר ID={book_id} סומן כבמלאי.")
        return True


def get_available_books():
    """
    3.6 – רשימת ספרים זמינים (in_stock=True)
    """
    with Session(engine) as session:
        stmt = select(Book).where(Book.in_stock == True)  # noqa: E712
        books = session.exec(stmt).all()

    if not books:
        print("אין ספרים זמינים במלאי.")
        return []

    for b in books:
        print(f"{b.id}: {b.title} (במלאי)")
    return books


# ---------------------------------------------------------
# אזור בדיקות מהיר – תריץ רק כשאתה רוצה לבדוק
# ---------------------------------------------------------

if __name__ == "__main__":
    # דוגמת רשימת ספרים (ליגרת 1.9)
    example_books = [
        ("הארי פוטר", "ג'יי קיי רולינג", 400, 79.90),
        ("שר הטבעות", "טולקין", 600, 89.90),
        ("1984", "ג'ורג' אורוול", 350, 59.90),
    ]

    # הוספת ספר אחד
    add_book("ספר בדיקה", "מחבר בדיקה", 123, 49.90)

    # הוספת כמה ספרים
    add_books_from_list(example_books)

    # הצגת כל הספרים
    show_all_books()

    # כמה ספרים יש
    count_books()

    # חיפוש לפי ID
    get_book_by_id(1)

    # בדיקת ספר זול/יקר
    get_cheapest_book()
    get_most_expensive_book()

    # ספרים מתחת למחיר
    get_cheap_books(80)

    # ספרים ארוכים
    get_long_books(300)

    # חיפוש לפי מילת מפתח
    search_books("ה")

    # ממוצע מחיר
    calculate_average_price()

    # ספרים בדף 1
    get_books_page(page_number=1, page_size=2)
