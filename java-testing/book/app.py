# -*- coding: utf-8 -*-

from datetime import datetime

import bottle
from bottle import get, post, run
from bottle import request, template, redirect
from bottle import HTTPError

# sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, UnicodeText
from sqlalchemy.ext.declarative import declarative_base

# bottle-sqlalchemy
from bottle.ext import sqlalchemy

# wtforms
from wtforms.form import Form
from wtforms import validators
from wtforms import StringField, IntegerField, TextAreaField

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

plugin = sqlalchemy.Plugin(
    engine,
    Base.metadata,
    keyword='db',
    create=True,
    commit=True,
    use_kwargs=False
)

bottle.install(plugin)


# book class
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(100), nullable=False)
    price = Column(Integer, nullable=False)
    memo = Column(UnicodeText)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return "<Book('%s', '%s', '%s', '%s')>" % (self.title, self.price, self.memo, self.created_at)


class BookForm(Form):
    title = StringField(u'Title', [
        validators.required(message=u'入力してください'),
        validators.length(min=1, max=100, message=u'100文字以下で入力してください')
    ])

    price = IntegerField(u'Price', [
        validators.required(message=u'数値で入力してください')
    ])

    memo = TextAreaField(u'Memo', [
        validators.required(message=u'入力してください')
    ])


@get('/books')
def index(db):
    books = db.query(Book).all()
    tmpobj = template('index', books=books, request=request)
    return tmpobj


@get('/books/add')
def new(db):
    form = BookForm()
    tmpobj = template('edit', form=form, request=request)
    return tmpobj

@post('/books/add')
def create(db):
    form = BookForm(request.forms.decode())
    if form.validate():
        book = Book(
            title=form.title.data,
            price=form.price.data,
            memo=form.memo.data
        )
        db.add(book)

        redirect("/books")
    else:
        return template('edit', form=form, request=request)


@get('/books/<id:int>/edit')
def edit(db, id):
    book = db.query(Book).get(id)
    if not book:
        return HTTPError(404, "book isn't found.")

    form = BookForm(request.POST, book)
    return template('edit', book=book, form=form, request=request)


@post('/books/<id:int>/edit')
def update(db, id):
    book = db.query(Book).get(id)
    if not book:
        return HTTPError(404, "book isn't found.")

    form = BookForm(request.forms.decode())

    if form.validate():
        book.title = form.title.data
        book.price = form.price.data
        book.memo = form.memo.data

        redirect("/books")

    else:
        return template('edit', form=form, request=request)


@post('/books/<id:int>/delete')
def destroy(db, id):
    book = db.query(Book).get(id)
    if not book:
        return HTTPError(404, "book isn't found.")

    db.delete(book)
    redirect("/books")


@get('/books/delete')
def destroy_all(db):
    books = db.query(Book).all()
    for book in books:
        db.delete(book)

    redirect("/books")

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
