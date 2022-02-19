from sqlalchemy import Column, Integer, String
from ..storages.base import Base
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class Reader(Base, UserMixin):
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False, nullable=False)
    surname = Column(String, unique=False, nullable=False)
    year = Column(Integer, unique=False, nullable=False)
    email = Column(String, unique=True, nullable=False)
    psw_hash = Column(String, unique=True, nullable=False)

    def __init__(self, name: str, surname: str, year: int, email: str, psw: str):
        self.name = name
        self.surname = surname
        self.year = year
        self.email = email
        self.psw_hash = generate_password_hash(psw)
        # self.id = _id if _id is not None else int(id(self))

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_year(self):
        return self.year

    def check_psw(self, psw: str):
        '''принимает введенньій пользователем пароль и сравнивает его с хеш-паролем, результат - bool'''
        return check_password_hash(self.psw_hash, psw)

    def __str__(self):
        return f'reader № {self.id}: {self.surname} {self.name}, {self.year}'

    def repr(self):
        cls_name = __class__.__name__

        return ' '.join(
            [
                f'{attr.replace(f"_{cls_name}", "")}={getattr(self, attr)}'
                for attr in dir(self) if attr.startswith(f'_{cls_name}')
            ]
        )