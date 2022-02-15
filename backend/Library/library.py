from .library_units.book import Book
from .library_units.readers import Reader
from .storages.istorage import IStorage
from .utils import logprint
from typing import Union
from threading import Lock


class Library:
    def __init__(self, storage: IStorage, books: list = None, readers: list = None) -> None:  #
        self.__storage = storage
        self.__lock = Lock()

        if books:
            self.__storage.add_books(books)
        if readers:
            self.__storage.add_readers(readers)

    ############# INIT

    def load_books_from_txt_file(self, filename: str,
                                 sep: str = '$!$',
                                 encoding: str = 'utf-8') -> bool:
        books = self.__storage.load_books_from_txt_file(filename, sep, encoding)
        if not len(books):
            logprint.print_fail(f'error load books from \'{filename}\'')
            return False

        self.__storage.add_books(books)
        return True

    def load_readers_from_txt_file(self, filename: str,
                                   sep: str = ',',
                                   encoding: str = 'utf-8') -> bool:
        readers = self.__storage.load_readers_from_txt_file(filename, sep, encoding)
        if not len(readers):
            logprint.print_fail(f'error load readers from {filename}')
            return False

        self.__storage.add_readers(readers)
        return True

    ############# GIVE - RETURN
    def search_book(self, book: str) -> list:
        search_res_list = []
        for i in self.get_all_books():
            if str(Book.get_title(i)) == book:
                search_res_list.append(i)
            elif str(Book.get_author(i)) == book:
                search_res_list.append(i)
            elif str(Book.get_year(i)) == book:
                search_res_list.append(i)
        print(search_res_list)
        return search_res_list



    def book_for_reader(self, book_id: int, reader_id: int) -> (bool, str):
        """gives a book"""
        return_msg = ''
        with self.__lock:
            book = self.__get_book_by_id(book_id)
            if not book:
                return_msg = f'Error: книга с номером {book_id} не в библиотеке'
                logprint.print_fail(return_msg)
                return False, return_msg
            reader = self.get_reader_by_id(reader_id)
            if not reader:
                return_msg = f'Error: Читателя с номером {reader_id} нет в библиотеке'
                logprint.print_fail(return_msg)
                return False, return_msg
            if Book.get_reader_id(book):
                return_msg = f'Error: Книги под номером {book_id} нету в библиотеке'
                logprint.print_fail(return_msg)
                return False, return_msg
            # book.set_reader_id(reader_id)
            self.__storage.update_book(book_id, reader_id)

        return_msg = f'Книга {book.get_title()} (c/н {book_id}) выдана читателю {reader.get_name()} (номер {reader_id})'
        logprint.print_done(return_msg)

        return True, return_msg

    def books_for_reader(self, book_id: list, reader_id: int) -> (bool,str):
        """gives several books"""
        return_msg = ''
        return_msg_error = ''
        book_titles_list = []
        for book in book_id:
            self.book_for_reader(book, reader_id)
            book_titles_list.append((self.__get_book_by_id(book)).get_title())
        if len(book_titles_list) >1:
            book_names = str(", ".join(book_titles_list))
            return_msg = f'Книга "{book_names}" выданы читателю № {reader_id}'
            return True, return_msg
        elif len(book_titles_list) == 1:
            return_msg = f'"Книга {book_titles_list[0]}" выданa читателю № {reader_id}'
            return True, return_msg
        else:
            return_msg_error = 'Error'
            return False, return_msg_error

    def return_to_library(self, book_id: int, reader_id: int) -> str:
        """return a book"""

        with self.__lock:
            book = self.__get_book_by_id(book_id)
            if not book:
                return_msg = f'Error: книги с номером {book_id} нет в библиотеке'
                logprint.print_fail(return_msg)
                return False, return_msg
            reader = self.get_reader_by_id(reader_id)
            if not reader:
                return_msg = f'Error: читателя с номером {reader_id} нет в библиотеке'
                logprint.print_fail(return_msg)
                return return_msg
            if book.get_reader_id() != reader.get_id():
                reader_2 = self.get_reader_by_id(book.get_reader_id())
                return_msg = f'Error: {reader.get_name()} не может вернуть книгу {book_id}, книга выдана {reader_2.get_name()} ({book.get_reader_id()})'
                logprint.print_fail(return_msg)
                return return_msg
            # book.set_reader_id(None)
            self.__storage.return_book(book_id, reader_id)

        return_msg = f'Читатель {reader.get_name()} вернул книгу "{book.get_title()}" в библиотеку'
        logprint.print_done(return_msg)

        return return_msg

    def return_books_to_library(self, book_list: list, reader_id: int) -> (bool, str):
        """returns several books"""
        return_msg = ''
        list_msg = []
        for book in book_list:
            list_msg.append(self.return_to_library(book, reader_id))
        if len(list_msg) > 1:
            return_msg = 'Выбранные книги сданы в библиотеку'
        else:
            return_msg = 'Книга сдана в библиотеку'
        return True, return_msg

    ############# BOOKS

    def add_book(self, title: str, author: str, year: int = None, book_id: int = None) -> (bool, str):
        """adds a book to storage"""
        return_msg = ''
        with self.__lock:
            book = Book(title, author, year)
            if self.__storage.add_book(book):
                return_msg = f'книга {title} успешно добавлена в библиотеку'
                logprint.print_done(return_msg)
                return True, return_msg
            else: #####
                return_msg = f'книга под под номером {book_id} уже существует'
                logprint.print_fail(return_msg)
                return False, return_msg

    def remove_book(self, book_id: int) -> str:
        """removes book from storage"""
        return_msg = ''
        with self.__lock:
            if book_id is not None:
                for book in self.get_all_books():
                    if int(book.get_id()) == book_id:
                        self.__storage.remove_book(book_id)
                        return_msg = f'Книга № {book.get_id()} ({book.get_title()}, {book.get_author()}) удалена из библиотеки'
                        logprint.print_done(return_msg)
                        return return_msg

            return_msg = f'Ошибка ввода или такой книги нет в библиотеке'
        logprint.print_fail(return_msg)
        return return_msg

    def remove_books(self, id_book_list: list) -> (bool,str):
        """removes several books from storage"""
        return_msg = ''
        list_msg = []
        for book in id_book_list:
            list_msg.append(self.__storage.remove_book(book))
        if len(list_msg) > 1:
            return_msg = 'Все книги успешно удалены'
        else:
            return_msg = 'Книга успешно удалена'
        return True, return_msg

    def __get_book_by_id(self, book_id: int) -> Union[Book, None]:
        """
        Функция получения книги по id из списка книг

        :param book_id: id книги, которую хотим получить
        :return: obj Book (если книга есть в библиотеке); None (если книги нет)
        """
        print('get_book_by_id')
        for book in self.get_all_books():
            if int(book.get_id()) == book_id:
                return book
        return None

    def get_all_books(self) -> Union[list, str]:
        if self.__storage.load_books():
            return [_book for _book in self.__storage.load_books()]
        else:
            return 'no books in Library'

    def get_available_books(self) -> list:
        return [_book for _book in self.__storage.load_books() if not _book.get_reader_id()]

    def get_unavailable_books(self) -> list:
        return [_book for _book in self.__storage.load_books() if _book.get_reader_id()]

    def get_all_book_from_reader(self, id_reader: int) -> list:
        return [_book for _book in self.__storage.load_books() if _book.get_reader_id() == id_reader]

    def get_sorted_book(self, sort: str = 'id', reverse: bool = False) -> list:
        if sort not in ['id', 'name', 'author', 'year']:
            print(f'Error: no sorting by {sort} field')
            return []

        def get_sort_field(book: Book):
            if sort == 'id':
                return book.get_id()
            elif sort == 'name':
                return book.get_name()
            elif sort == 'author':
                return book.get_author()
            elif sort == 'year':
                return book.get_year()

        list_sorted_book =[]
        for book in sorted(self.get_all_books(), key=get_sort_field, reverse=reverse):
            list_sorted_book.append(book)
        return list_sorted_book

    ############# READERS

    def add_reader(self, name: str, surname: str, year: int = None, reader_id: int = None) -> (bool, str):
        '''добавляет нового читателя в список читателей. '''
        reader = Reader(name, surname, year)
        if self.__storage.add_reader(reader):
            return_msg = f'читатель {name} {surname} успешно зарегистрирован в библиотеке'
            logprint.print_done(return_msg)
            return True, return_msg
        else:
            return_msg = f'читатель {name} c номером {reader_id} уже зарегистрирован в этой библиотеке'
            logprint.print_fail(return_msg)
        return True, return_msg

    def remove_reader(self, reader_id: int) -> (bool, str):
        with self.__lock:
            if reader_id is not None:
                for reader in self.get_all_readers():
                    if int(reader.get_id()) == reader_id:
                        # self.__list_People.remove(self.__get_reader_by_id(reader_id))
                        self.__storage.remove_reader(reader_id)
                        return_msg = f'Карточка читателя {reader.get_name()} {reader.get_surname()} (№{reader.get_id()}) удалена из библиотеки'
                        logprint.print_done(return_msg)
                        return True, return_msg
            return_msg = f'Ошибка ввода или такой читатель не зарегистрирован в библиотеке'
            logprint.print_done(return_msg)
        return True, return_msg

    def get_all_readers(self) -> Union[list, str]:
        if self.__storage.load_readers():
            return [_reader for _reader in self.__storage.load_readers()]
        else:
            return 'no books in Library'

    def get_reader_by_id(self, reader_id: int) -> Union[Reader, None]:
        """
        Функция получения читателя по id из списка читателей

        :param reader_id: id читателя, которого хотим получить
        :return: obj Reader (зарегистрирован ли читатель в библиотеке); None (если не зарегистрирован)
        """
        print('get_reader_by_id')
        for reader in self.get_all_readers():

            if int(reader.get_id()) == reader_id:
                return reader
        return None

    def get_reader_by_email(self, email: str) -> Union[Reader, None]:
        """
        Функция получения читателя по email из списка читателей

        :param email: email читателя, которого хотим получить
        :return: obj Reader (зарегистрирован ли читатель в библиотеке); None (если не зарегистрирован)
        """
        print('get_reader_by_email')
        for reader in self.get_all_readers():

            if int(reader.get_id()) == email:
                return reader
        return None

    ############# LOADING

    def load_books(self) -> bool:
        books = self.__storage.load_books()
        if books:
            return True
        return False

    def load_readers(self) -> bool:
        readers = self.__storage.load_readers()
        if readers:
            return True
        return False


############# ???????

    # def save_all_books(self):
    #     self.__storage.add_books(self.__list_Books)
    #
    # def save_all_readers(self):
    #     self.__storage.add_readers(self.__list_People)

    def __str__(self):
        return f'{self}'






