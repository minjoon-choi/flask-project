from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import CommentForm
from pybo.models import Idea, Comment, Feedback
from pybo.views.auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/idea/<int:idea_id>', methods=('GET', 'POST'))
@login_required
def create_idea(idea_id):
    form = CommentForm()
    idea = Idea.query.get_or_404(idea_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data, regDate=datetime.now(), idea=idea)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(
            url_for('idea.detail', idea_id=idea_id), comment.id))
    return render_template('comment/comment_form.html', form=form)


@bp.route('/modify/idea/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_idea(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=comment.idea.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.editDate = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#comment_{}'.format(
                url_for('idea.detail', idea_id=comment.idea.id), comment.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)


@bp.route('/delete/idea/<int:comment_id>')
@login_required
def delete_idea(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    idea_id = comment.idea.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=idea_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('idea.detail', idea_id=idea_id))


@bp.route('/create/feedback/<int:feedback_id>', methods=('GET', 'POST'))
@login_required
def create_feedback(feedback_id):
    form = CommentForm()
    feedback = Feedback.query.get_or_404(feedback_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data, regDate=datetime.now(), feedback=feedback)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(
            url_for('idea.detail', idea_id=feedback.idea.id), comment.id))
    return render_template('comment/comment_form.html', form=form)


@bp.route('/modify/feedback/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_feedback(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=comment.feedback.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.editDate = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#comment_{}'.format(
                url_for('idea.detail', idea_id=comment.feedback.idea.id), comment.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)


@bp.route('/delete/feedback/<int:comment_id>')
@login_required
def delete_feedback(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    idea_id = comment.feedback.idea.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=idea_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('idea.detail', idea_id=idea_id))
