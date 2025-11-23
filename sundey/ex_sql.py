from typing import Optional
from sqlmodel import SQLModel, Session, create_engine, select, Field

DB_URL = "mysql+pymysql://root@localhost:3306/test"
engine = create_engine(DB_URL, echo=True)


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    author: str = Field(max_length=100, nullable=False)
    pages: Optional[int] = Field(default=None)
    price: Optional[float] = Field(default=None)


SQLModel.metadata.create_all(engine)


def add_book(title: str, author: str, pages: int, price: float):
    with Session(engine) as session:
        book = Book(title=title, author=author, pages=pages, price=price)
        session.add(book)
        session.commit()
        session.refresh(book)
        print(book)


def show_all_books():
    with Session(engine) as session:
        books = session.exec(select(Book)).all()
        print(books)

    if not books:
        print("אין ספרים במערכת.")
        return

    for b in books:
        print(
            f"ID: {b.id} | titel: {b.title} | author: {b.author} | "
            f"pages: {b.pages} | price: {b.price}"
        )

def get_book_by_id(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
    if book is None:
        print("error: book not found")
    else:
        print(book)


def update_book_price(book_id, new_price):
    with Session(engine) as session:
        book = session.get(Book, book_id)
    if book is None:
        print("error: book not found")
    else:
        book.price=new_price
        session.add(book)
        session.commit()
        session.refresh(book)
        print(book)


def delete_book(book_id):
    with Session(engine) as session:
        book = session.get(Book, book_id)
    if book is None:
        print("error: book not found")
    else:
        session.delete(book)
        session.commit()
        print(book)

def count_books():
     with Session(engine) as session:
        books = session.exec(select(Book)).all()
        return len(books)


def add_books_from_list(books):
    addd = 0
    
    for title, author, pages , price in books:
        add_book(title,author,pages,price)
        addd+=1
    return addd



def book_exists(title: str) -> bool:
    
    with Session(engine) as session:
        stmt = select(Book).where(Book.title == title)
        result = session.exec(stmt).first()

    if result==None:
        return False
    else:
        return True















# add_book("daniel", "ddd", 300, 500.5)
# delete_book(1)
books=[("ssss","aaaaa",400 , 79.90 ) ,("gek","flask",322,3213.80)]
print(add_books_from_list(books))
