from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, DateField, FloatField
#from wtforms.fields import SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class IdeaForm(FlaskForm):
    ideaType = StringField('고객사명', validators=[DataRequired('아이디어 유형을 선택하세요.')])
    ideaStatus = StringField('계열사품목코드', validators=[DataRequired('현재 아이디어 진행현황을 선택하세요.')]) 
    effectBegin = DateField('적용시작월', format='%Y-%m')
    effectEnd = DateField('적용종료월', format='%Y-%m')
    ideaTitle = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    companyID = StringField('고객사명', validators=[DataRequired('고객사명은 필수입력 항목입니다.')])
    prodID = StringField('계열사품목코드', validators=[DataRequired('계열사품목코드는 필수입력 항목입니다.')])
    priceBefore = FloatField('기존단가')
    priceAfter = FloatField('변경단가')
    estSavings = FloatField('예상절감액')
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class FeedbackForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class UserCreateForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired(), Length(min=3, max=25)])
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('password1', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('password2', validators=[DataRequired()])
    userteam = StringField('userteam', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('email', [DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])


class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])
