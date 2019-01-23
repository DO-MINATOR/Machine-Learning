from app.web import web


@web.route('/ss')
def index():
    return "dasd"

@web.route('/')
def pending():
    pass