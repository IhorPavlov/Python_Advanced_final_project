from sqlalchemy import Column, Integer, String, ForeignKey
from ..storages.base import Base
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class Reader(Base, UserMixin):
    __tablename__ = 'readers'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    surname = Column('surname', String, nullable=False)
    year = Column('year', Integer, nullable=False)
    email = Column('email', String, nullable=False)
    psw_hash = Column('email', String, nullable=False)

    def __init__(self, name: str, surname: str, year: int, email: str, psw_hash: str):
        self.name = name
        self.surname = surname
        self.year = year
        self.email = email
        self.psw_hash= psw_hash
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