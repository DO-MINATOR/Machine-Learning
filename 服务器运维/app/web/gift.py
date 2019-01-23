from app.web import web
from flask_login import login_required,current_user
from fisher import db
from app.db.gift import Gift


@web.route('/my/gifts')
@login_required
def my_gifts():
    return "dsa"


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    gift = Gift()
    gift.isbn = isbn
    gift.uid = current_user.id
    current_user.beans +=0.5
    db.session.add(gift)
    db.session.commit()
    pass


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
