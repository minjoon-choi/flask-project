from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .auth_views import login_required
from .. import db
from ..forms import AnswerForm
from ..models import Idea, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:idea_id>', methods=('POST',))
@login_required
def create(idea_id):
    form = AnswerForm()
    idea = Idea.query.get_or_404(idea_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        idea.answer_set.append(answer)
        db.session.commit()
        return redirect('{}#answer_{}'.format(
            url_for('idea.detail', idea_id=idea_id), answer.id))
    return render_template('idea/idea_detail.html', idea=idea, form=form)


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=answer.idea.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#answer_{}'.format(
                url_for('idea.detail', idea_id=answer.idea.id), answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)


@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    idea_id = answer.idea.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('idea.detail', idea_id=idea_id))
