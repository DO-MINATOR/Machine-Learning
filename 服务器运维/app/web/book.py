from app.web import web
from flask import request, render_template, jsonify, flash
from app.form.searchform import Searchform
from app.form.isbn_or_key import is_isbn_or_key
from app.form.searchbook import *
from app.viewmodel.book import BookCollection, singlebook
import time


@web.route('/book/search/')
def search():
    form = Searchform(request.args)
    result = None
    if form.validate():
        q = form.q.data
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == 'isbn':
            result = search_by_isbn(q)
            if result:
                result = singlebook(result, q).get()
            else:
                flash("搜索结果为空")
                result = None
        else:
            result = search_by_keyword(q, page)
            result = BookCollection(result, q).getBook()
    else:
        flash("搜索格式不正确")
    return render_template('search_result.html', books=result)


@web.route('/book/search/<isbn>')
def book_detail(isbn):
    result = search_by_isbn(isbn)
    result = singlebook(result, isbn).get()
    return render_template('book_detail.html', book=result, wishes=[], gifts=[])
