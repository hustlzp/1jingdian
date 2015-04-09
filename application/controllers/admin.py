# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for
from ..utils.permissions import AdminPermission
from ..models import db, CollectionEditLogReport, PieceEditLogReport

bp = Blueprint('admin', __name__)


@bp.route('/report_piece_logs', methods=['GET', 'POST'])
@AdminPermission()
def report_piece_logs():
    reports = PieceEditLogReport.query
    return render_template('admin/report_piece_logs.html', reports=reports)


@bp.route('/report_collection_logs', methods=['GET', 'POST'])
@AdminPermission()
def report_collection_logs():
    reports = CollectionEditLogReport.query
    return render_template('admin/report_collection_logs.html', reports=reports)
