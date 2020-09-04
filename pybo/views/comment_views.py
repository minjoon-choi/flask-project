from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import CommentForm
from pybo.models import Idea, Comment, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/idea/<int:idea_id>', methods=('GET', 'POST'))
@login_required
def create_idea(idea_id):
    form = CommentForm()
    idea = Idea.query.get_or_404(idea_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), idea=idea)
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
            comment.modify_date = datetime.now()  # 수정일시 저장
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


@bp.route('/create/answer/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def create_answer(answer_id):
    form = CommentForm()
    answer = Answer.query.get_or_404(answer_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), answer=answer)
        db.session.add(comment)
        db.session.commit()
        return redirect('{}#comment_{}'.format(
            url_for('idea.detail', idea_id=answer.idea.id), comment.id))
    return render_template('comment/comment_form.html', form=form)


@bp.route('/modify/answer/<int:comment_id>', methods=('GET', 'POST'))
@login_required
def modify_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if g.user != comment.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=comment.answer.id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect('{}#comment_{}'.format(
                url_for('idea.detail', idea_id=comment.answer.idea.id), comment.id))
    else:
        form = CommentForm(obj=comment)
    return render_template('comment/comment_form.html', form=form)


@bp.route('/delete/answer/<int:comment_id>')
@login_required
def delete_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    idea_id = comment.answer.idea.id
    if g.user != comment.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('idea.detail', idea_id=idea_id))
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('idea.detail', idea_id=idea_id))
