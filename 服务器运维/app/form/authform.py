from wtforms import Form, StringField, IntegerField, PasswordField, ValidationError
from wtforms.validators import Length, NumberRange, DataRequired, Email
from app.db.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="email not exist")])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称为2-10个字符')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("电子邮件已被注册")


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message="email not exist")])
    password = PasswordField(validators=[DataRequired(message='密码不能为空'), Length(6, 32)])
