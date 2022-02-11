from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..storages.base import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, nullable = False, primary_key=True, unique=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable=True)

    reader = relationship('Reader', backref='books')

    def __init__(self, title: str, author: str, year: int, reader_id: int = None) -> None:
        self.title = title
        self.author = author
        self.year = year
        # self.id = _id if _id is not None else int(id(self))
        self.reader_id = reader_id

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_year(self):
        return self.year

    def get_reader_id(self):
        return self.reader_id

    def set_reader_id(self, _reader_id: int):
        self.reader_id = _reader_id

    def __str__(self):
        return f'book № {self.id}: "{self.title}". {self.author}, {self.year}'

    def repr(self):
        cls_name = __class__.__name__

        return ' '.join(
            [
                f'{attr.replace(f"_{cls_name}", "")}={getattr(self, attr)}'
                for attr in dir(self) if attr.startswith(f'_{cls_name}')
            ]
        )