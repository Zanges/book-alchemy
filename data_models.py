from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

db = SQLAlchemy()


class Base(DeclarativeBase):
    pass


class Author(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    birth_date: Mapped[str] = mapped_column(db.Date, nullable=True)
    date_of_death: Mapped[str] = mapped_column(db.Date, nullable=True)

    books = db.relationship("Book", back_populates="author", lazy=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Author {self.name}>"


class Book(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    isbn: Mapped[str] = mapped_column(db.String(13), nullable=True)
    author_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("author.id"), nullable=False
    )

    author = db.relationship("Author", back_populates="books")

    def __str__(self):
        return f"{self.title} by {self.author}"

    def __repr__(self):
        return f"<{self.__str__()}>"
