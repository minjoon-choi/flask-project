from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash, current_app
from sqlalchemy import func, nullslast
from werkzeug.utils import redirect

from .. import db
from ..forms import IdeaForm, AnswerForm
from ..models import Idea, Answer, User, idea_voter
from ..views.auth_views import login_required

bp = Blueprint('idea', __name__, url_prefix='/idea')


def _nullslast(obj):
    if current_app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        return obj
    else:
        return nullslast(obj)


@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend':
        sub_query = db.session.query(idea_voter.c.idea_id, func.count('*').label('num_voter')) \
            .group_by(idea_voter.c.idea_id).subquery()
        idea_list = Idea.query \
            .outerjoin(sub_query, Idea.id == sub_query.c.idea_id) \
            .order_by(_nullslast(sub_query.c.num_voter.desc()), Idea.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Answer.idea_id, func.count('*').label('num_answer')) \
            .group_by(Answer.idea_id).subquery()
        idea_list = Idea.query \
            .outerjoin(sub_query, Idea.id == sub_query.c.idea_id) \
            .order_by(_nullslast(sub_query.c.num_answer.desc()), Idea.create_date.desc())
    else:  # recent
        idea_list = Idea.query.order_by(Idea.create_date.desc())

    # 조회
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.idea_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        idea_list = idea_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.idea_id == Idea.id) \
            .filter(Idea.subject.ilike(search) |  # 질문제목
                    Idea.prod_id.ilike(search) | # 계열사품목코드
                    Idea.content.ilike(search) |  # 제안내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    idea_list = idea_list.paginate(page, per_page=10)
    return render_template('idea/idea_list.html', idea_list=idea_list, page=page, kw=kw, so=so)


@bp.route('/detail/<int:idea_id>/')
def detail(idea_id):
    form = AnswerForm()
    idea = Idea.query.get_or_404(idea_id)
    return render_template('idea/idea_detail.html', idea=idea, form=form)


@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = IdeaForm()
    if request.method == 'POST' and form.validate_on_submit():
        idea = Idea(company=form.company.data, prod_id=form.prod_id.data,
                            subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(idea)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('idea/idea_form.html', form=form)


@bp.route('/modify/<int:idea_id>', methods=('GET', 'POST'))
@login_required
def modify(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    if g.user != idea.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=idea_id))
    if request.method == 'POST':
        form = IdeaForm()
        if form.validate_on_submit():
            form.populate_obj(idea)
            idea.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('idea.detail', idea_id=idea_id))
    else:
        form = IdeaForm(obj=idea)
    return render_template('idea/idea_form.html', form=form)


@bp.route('/delete/<int:idea_id>')
@login_required
def delete(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    if g.user != idea.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=idea_id))
    db.session.delete(idea)
    db.session.commit()
    return redirect(url_for('idea._list'))