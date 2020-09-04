from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Idea, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/idea/<int:idea_id>/')
@login_required
def idea(idea_id):
    _idea = Idea.query.get_or_404(idea_id)
    if g.user == _idea.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _idea.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('idea.detail', idea_id=idea_id))


@bp.route('/answer/<int:answer_id>/')
@login_required
def answer(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('idea.detail', idea_id=_answer.idea.id))
