# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for
from ..utils.permissions import AdminPermission
from ..models import db, CollectionEditLogReport, PieceEditLogReport, Feedback

bp = Blueprint('admin', __name__)


@bp.route('/admin/report_piece_logs', methods=['GET', 'POST'])
@AdminPermission()
def report_piece_logs():
    reports = PieceEditLogReport.query
    return render_template('admin/report_piece_logs.html', reports=reports)


@bp.route('/admin/report_collection_logs', methods=['GET', 'POST'])
@AdminPermission()
def report_collection_logs():
    reports = CollectionEditLogReport.query
    return render_template('admin/report_collection_logs.html', reports=reports)


@bp.route('/admin/feedback', methods=['GET', 'POST'])
@AdminPermission()
def feedback():
    feedbacks = Feedback.query
    return render_template('admin/feedback.html', feedbacks=feedbacks)


@bp.route('/admin/feedback/<int:uid>/process')
@AdminPermission()
def process_feedback(uid):
    feedback = Feedback.query.get_or_404(uid)
    feedback.processed = True
    db.session.add(feedback)
    db.session.commit()
    return redirect(request.referrer or url_for('.feedback'))
