from flask import Flask, render_template, request, redirect, url_for, get_flashed_messages
from Library.library import Library
from Library.storages.orm_storage import ORMStorage
import os
from dotenv import load_dotenv
from email_validator import validate_email
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

CURRENT_USER_ID = 1

load_dotenv('.env')

app = Flask(__name__,
            template_folder='../site/templates',
            static_folder='../site/static')

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

login_manager = LoginManager(app)
login_manager.login_view = 'api_login'

@login_manager.user_loader
def load_user(user_id):
    return lib.get_reader_by_id(user_id)

storage = ORMStorage(
    db_user=os.environ.get('DB_USER'),
    db_password=os.environ.get('DB_PASSWORD'),
    db_name=os.environ.get('DB_NAME'),
    db_address=os.environ.get('DB_ADDRESS'),
    db_port=os.environ.get('DB_PORT')
)

lib = Library(storage)
if not lib.get_all_books():
    lib.load_books_from_txt_file('books.txt', sep='$!$')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form.get('search')
        if not search:
            return render_template('index.html', message='Введены некорректные данные')
        return render_template('search_books.html', books=lib.search_book(search))

    return render_template('index.html')


@app.route('/search_books', methods=['GET', 'POST'])
def api_get_search_books():
    return render_template('search_books.html')


@app.route('/books', methods=['GET', 'POST'])
def api_get_all_books():
    return render_template('books.html', books=lib.get_all_books())


@app.route('/books_sorted_by_id', methods=['GET', 'POST'])
def api_sort_by_id():
    return render_template('books_sorted_by_id.html', books=lib.get_sorted_book('id'))


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def api_add_book():
    if request.method == 'POST':
        title_book = request.form.get('title')
        author_book = request.form.get('author')
        year_book = request.form.get('year')

        if not (title_book and author_book and year_book):
            flash('Введены некорректные данные', 'Error')
            return render_template('add_book.html')
        if not year_book.isnumeric():
            return render_template('add_book.html', message='Введен некорректный год издания')

        ret_code, ret_msg = lib.add_book(title_book, author_book, int(year_book))
        return render_template('add_book.html', message=ret_msg)

    return render_template('add_book.html')

    # # WTForm
    # from add_book_form import AddBookForm
    # add_book_form = AddBookForm()
    #
    # if request.method == 'POST':
    #     if add_book_form.validate_on_submit():
    #         print(add_book_form.title.data)
    #         print(add_book_form.author.data)
    #         print(add_book_form.year.data)
    #     else:
    #         print('Error')
    #
    # return render_template('add_book.html', form=add_book_form)


@app.route('/delete_book', methods=['GET', 'POST'])
@login_required
def api_delete_book():
    if request.method == 'POST':
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_books):
            ret_code, ret_msg = lib.remove_books(id_books)
            return render_template('delete_book.html',
                                   books=sorted(lib.get_all_books(), key=lambda book: book.id),
                                   message=ret_msg)

    return render_template('delete_book.html', books=sorted(lib.get_all_books(), key=lambda book: book.id))


@app.route('/take_book', methods=['GET', 'POST'])
@login_required
def api_take_book():
    if request.method == 'POST':
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_books):
            ret_code, message = lib.books_for_reader(id_books, current_user.get_id())
            # вместо reader_id = 1 вставить CURRENT_USER_ID
            return render_template('take_book.html',
                                   books=sorted(lib.get_available_books(), key=lambda book: book.id),
                                   message=message)

    return render_template('take_book.html', books=sorted(lib.get_available_books(), key=lambda book: book.id))


@app.route('/return_book', methods=['GET', 'POST'])
@login_required
def api_return_book():
    if request.method == 'POST':
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_books):
            ret_code, message = lib.return_books_to_library(id_books, current_user.get_id())
            return render_template('return_book.html',
                                   books=sorted(lib.get_all_book_from_reader(current_user.get_id()),
                                                key=lambda book: book.id),
                                   message=message)

    return render_template('return_book.html',
                           books=sorted(lib.get_all_book_from_reader(current_user.get_id()), key=lambda book: book.id))


@app.route('/registration', methods=['GET', 'POST'])
def api_registration():
    if current_user.is_authentificated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        psw = request.form.get('psw')
        name = request.form.get('name')
        surname = request.form.get('surname')
        year = request.form.get('year')


    try:
        validate_email(email)
    except:
        return render_template('registration.html')

    if lib.add_reader(name, surname, year, email, psw):
        # flash('fffff')
        return redirect(url_for('api_login'))
    else:
        return render_template('registration.html')
    # return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def api_login():
    if current_user.is_authentificated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        psw = request.form.get('psw')

        if not (email and psw):
            return  render_template('login.html', message = 'error')

        reader = lib.get_reader_by_email(email)
        if reader and reader.check_psw(psw):
            login_user(reader)

            if next_url:
                return redirect(next_url)

            return redirect(url_for('index'))
        else:
            return render_template('login.html', message = 'error')

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
@login_required
def api_logout():
    if request.method == 'POST':
        logout_user()


if __name__ == '__main__':
    app.run()
