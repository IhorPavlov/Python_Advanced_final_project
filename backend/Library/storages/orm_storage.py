from .base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .istorage import IStorage
from ..library_units.book import Book
from ..library_units.readers import Reader
from ..utils import logprint
import os


class ORMStorage(IStorage):
    def __init__(self, db_user, db_password, db_name, db_address='localhost', db_port=5432, dialect='postgresql'):
        self.__engine = create_engine(f'{dialect}://{db_user}:{db_password}@{db_address}:{db_port}/{db_name}')
        Base.metadata.create_all(self.__engine)
        self.__session = Session(self.__engine)

    ############# BOOKS

    def load_books(self) -> list:
        """get all books from storage"""
        return [book for book in self.__session.query(Book)]

    def add_books(self, books: list):
        """add all books to storage"""
        for book in books:
            self.add_book(book)

    def add_book(self, obj_book: Book) -> bool:
        """add a book to storage"""
        self.__session.add(obj_book)
        # print(obj_book)
        try:
            self.__session.commit()
            logprint.print_done(f'the book {obj_book.get_title()}, {obj_book.get_author()} added')
        except:
            logprint.print_fail('the book isn\'t added')
            return False
        return True

    def remove_book(self, book_id) -> bool:
        """delete book from storage"""
        deleted_book = self.__session.query(Book).filter(Book.id == book_id).one()
        print(deleted_book)
        self.__session.delete(deleted_book)
        if not self.__session.commit():
            print('Error')
            return False
        return True


    ############# READERS

    def load_readers(self) -> list:
        """get all readers from storage"""
        return [reader for reader in self.__session.query(Reader)]

    def add_readers(self, readers: list):
        """add all readers to storage"""
        for reader in readers:
            self.add_reader(reader)

    def add_reader(self, obj_reader: Reader) -> bool:
        """add a reader to storage"""
        self.__session.add(obj_reader)
        print(obj_reader)
        try:
            self.__session.commit()
            logprint.print_done(f'the reader {obj_reader.get_name()}, {obj_reader.get_surname()} is registered')
        except:
            logprint.print_fail('the reader isn\'t registered')
            return False
        return True

    def remove_reader(self, reader_id):
        """delete reader from storage"""
        deleted_reader = self.__session.query(Reader).filter(Reader.id == reader_id).one()
        print(deleted_reader)
        self.__session.delete(deleted_reader)
        if not self.__session.commit():
            print('Error')
            return False
        return True

    # def update_reader(self, obj_reader) -> bool:
    #     pass

    ############# GIVE - RETURN
    def update_book(self, book_id, reader_id) -> bool:
        gived_book = self.__session.query(Book).filter(Book.id == book_id).one()
        # print(gived_book)
        gived_book.reader_id = reader_id
        # print(self.__session.dirty)
        if not self.__session.commit():
            print('Error')
            return False
        return True

    def return_book(self, book_id, reader_id) -> bool:
        returned_book = self.__session.query(Book).filter(Book.id == book_id).one()
        # print(gived_book)
        returned_book.reader_id = None
        # print(self.__session.dirty)
        if not self.__session.commit():
            print('Error')
            return False
        return True

    # def load_reader_by_email(self, email: str) -> Reader:
    #     load_reader = self.__session.query(Reader).filter(Reader.email == str(email)).one()
    #     print(load_reader)
    #     return load_reader

    def load_readers_by_email(self, email: str) -> Reader:
        return self.__session.query(Reader).filter_by(email=email).first()

    def load_reader_by_id(self, id_: int) -> Reader:
        load_reader = self.__session.query(Reader).filter(Reader.id == id_).one()
        print(load_reader)
        return load_reader

    def load_several_books(self, page: int, page_size: int) -> list:
        return self.__session.query(Book).order_by(Book.id).limit(page_size).offset(page*page_size)

