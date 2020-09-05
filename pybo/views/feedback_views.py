from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .auth_views import login_required
from .. import db
from ..forms import FeedbackForm
from ..models import Idea, Feedback

bp = Blueprint('feedback', __name__, url_prefix='/feedback')


@bp.route('/create/<int:idea_id>', methods=('POST',))
@login_required
def create(idea_id):
    form = FeedbackForm()
    idea = Idea.query.get_or_404(idea_id)
    if form.validate_on_submit():
        content = request.form['content']
        feedback = Feedback(content=content, regDate=datetime.now(), user=g.user)
        idea.feedback_set.append(feedback)
        db.session.commit()
        return redirect('{}#feedback_{}'.format(
            url_for('idea.detail', idea_id=idea_id), feedback.id))
    return render_template('idea/idea_detail.html', idea=idea, form=form)


@bp.route('/modify/<int:feedback_id>', methods=('GET', 'POST'))
@login_required
def modify(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if g.user != feedback.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=feedback.idea.id))
    if request.method == "POST":
        form = FeedbackForm()
        if form.validate_on_submit():
            form.populate_obj(feedback)
            feedback.editDate = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#feedback_{}'.format(
                url_for('idea.detail', idea_id=feedback.idea.id), feedback.id))
    else:
        form = FeedbackForm(obj=feedback)
    return render_template('feedback/feedback_form.html', feedback=feedback, form=form)


@bp.route('/delete/<int:feedback_id>')
@login_required
def delete(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    idea_id = feedback.idea.id
    if g.user != feedback.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(feedback)
        db.session.commit()
    return redirect(url_for('idea.detail', idea_id=idea_id))
