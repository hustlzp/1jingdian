# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, g, json
from ..utils.permissions import UserPermission, CollectionEditPermission, AdminPermission
from ..models import db, Piece, Collection, CollectionPiece, CollectionLike, \
    CollectionEditLog, COLLECTION_EDIT_KIND, CollectionEditLogReport, CollectionKind
from ..forms import CollectionForm
from ..utils.uploadsets import collection_covers, crop_image, process_image_for_cropping
from ..utils.helpers import generate_lcs_html

bp = Blueprint('collection', __name__)


@bp.route('/collection/<int:uid>', defaults={'page': 1})
@bp.route('/collection/<int:uid>/page/<int:page>')
def view(uid, page):
    collection = Collection.query.get_or_404(uid)
    pieces = collection.pieces.paginate(page, 20)
    return render_template('collection/view.html', collection=collection, pieces=pieces)


@bp.route('/collection/<int:uid>/hot', defaults={'page': 1})
@bp.route('/collection/<int:uid>/hot/page/<int:page>')
def hot_view(uid, page):
    collection = Collection.query.get_or_404(uid)
    pieces = Piece.query.filter(Piece.collections.any(CollectionPiece.collection_id == uid)) \
        .order_by(Piece.votes_count.desc()).paginate(page, 20)
    return render_template('collection/hot_view.html', collection=collection, pieces=pieces)


@bp.route('/collection/<int:uid>/voted', defaults={'page': 1})
@bp.route('/collection/<int:uid>/voted/page/<int:page>')
@UserPermission()
def voted_view(uid, page):
    collection = Collection.query.get_or_404(uid)
    pieces = collection.voted_pieces_by_user.paginate(page, 20)
    return render_template('collection/voted_view.html', collection=collection, pieces=pieces)


@bp.route('/collection/<int:uid>/edit', methods=['GET', 'POST'])
def edit(uid):
    collection = Collection.query.get_or_404(uid)
    permission = CollectionEditPermission(collection)
    if not permission.check():
        return permission.deny()

    form = CollectionForm(obj=collection)
    form.kind_id.choices = [(kind.id, kind.name) for kind in
                            CollectionKind.query.order_by(CollectionKind.show_order.asc())]
    if form.validate_on_submit():
        # title变更
        if collection.title != form.title.data:
            title_log = CollectionEditLog(collection_id=uid, user_id=g.user.id,
                                          kind=COLLECTION_EDIT_KIND.UPDATE_TITLE,
                                          before=collection.title, after=form.title.data,
                                          compare=generate_lcs_html(collection.title,
                                                                    form.title.data))
            db.session.add(title_log)

        # desc变更
        if (collection.desc or "") != form.desc.data:
            desc_log = CollectionEditLog(collection_id=uid, user_id=g.user.id,
                                         before=collection.desc, after=form.desc.data,
                                         compare=generate_lcs_html(collection.desc, form.desc.data))
            if collection.desc == "":
                desc_log.kind = COLLECTION_EDIT_KIND.ADD_DESC
            elif form.desc.data == "":
                desc_log.kind = COLLECTION_EDIT_KIND.REMOVE_DESC
            else:
                desc_log.kind = COLLECTION_EDIT_KIND.UPDATE_DESC
            db.session.add(desc_log)

        form.populate_obj(collection)
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('collection.view', uid=uid))
    return render_template('collection/edit.html', form=form, collection=collection)


@bp.route('/collection/upload_cover', methods=['POST'])
@UserPermission()
def upload_cover():
    try:
        filename, (w, h) = process_image_for_cropping(request.files['file'], collection_covers)
    except Exception, e:
        return json.dumps({'result': False, 'error': e.__repr__()})
    else:
        return json.dumps({
            'result': True,
            'image_url': collection_covers.url(filename),
            'width': w,
            'height': h
        })


@bp.route('/collection/<int:uid>/crop_avatar', methods=['POST'])
@UserPermission()
def crop_cover(uid):
    collection = Collection.query.get_or_404(uid)
    filename = request.form.get('filename')
    top_left_x_ratio = request.form.get('top_left_x_ratio', type=float)
    top_left_y_ratio = request.form.get('top_left_y_ratio', type=float)
    bottom_right_x_ratio = request.form.get('bottom_right_x_ratio', type=float)
    bottom_right_y_ratio = request.form.get('bottom_right_y_ratio', type=float)

    try:
        new_cover_filename = crop_image(filename, collection_covers, top_left_x_ratio,
                                        top_left_y_ratio, bottom_right_x_ratio,
                                        bottom_right_y_ratio)
    except Exception, e:
        return json.dumps({'result': False, 'message': e.__repr__()})
    else:
        # cover变更记录
        cover_log = CollectionEditLog(collection_id=uid, user_id=g.user.id,
                                      before=collection.cover_url,
                                      after=collection_covers.url(new_cover_filename))
        if not collection.cover or collection.cover == 'default.png':
            cover_log.kind = COLLECTION_EDIT_KIND.ADD_COVER
        else:
            cover_log.kind = COLLECTION_EDIT_KIND.UPDATE_COVER
        db.session.add(cover_log)

        # 保存图标
        collection.cover = new_cover_filename
        db.session.add(collection)
        db.session.commit()
        return json.dumps({
            'result': True,
            'image_url': collection_covers.url(new_cover_filename)
        })


@bp.route('/collection/query', methods=['POST'])
@UserPermission()
def query():
    q = request.form.get('q')
    piece_id = request.form.get('piece_id')
    if q:
        collections = Collection.query.filter(Collection.title.like("%%%s%%" % q))
        if piece_id:
            collections = collections.filter(
                ~Collection.pieces.any(CollectionPiece.piece_id == piece_id))
        return json.dumps([{'value': collection.title,
                            'count': collection.pieces.count(),
                            'id': collection.id}
                           for collection in collections])
    else:
        return json.dumps({})


@bp.route('/collection/<int:uid>/like', methods=['POST'])
@UserPermission()
def like(uid):
    collection = Collection.query.get_or_404(uid)
    like = collection.likers.filter(CollectionLike.user_id == g.user.id).first()
    if not like:
        like = CollectionLike(collection_id=uid, user_id=g.user.id)
        db.session.add(like)
        g.user.liked_collections_count += 1
        db.session.add(g.user)
        db.session.commit()
    return json.dumps({'result': True})


@bp.route('/collection/<int:uid>/unlike', methods=['POST'])
@UserPermission()
def unlike(uid):
    collection = Collection.query.get_or_404(uid)
    likes = collection.likers.filter(CollectionLike.user_id == g.user.id)
    for like in likes:
        db.session.delete(like)
        if g.user.liked_collections_count > 0:
            g.user.liked_collections_count -= 1
    db.session.add(g.user)
    db.session.commit()
    return json.dumps({'result': True})


@bp.route('/collection/log/<int:uid>/report', methods=['POST'])
@UserPermission()
def report_log(uid):
    """举报恶意编辑"""
    log = CollectionEditLog.query.get_or_404(uid)
    report = log.reports.filter(CollectionEditLog.user_id == g.user.id).first()
    if not report:
        report = CollectionEditLogReport(log_id=uid, user_id=g.user.id)
        db.session.add(report)
        db.session.commit()
    return json.dumps({'result': True})


@bp.route('/collection/<int:uid>/lock')
@AdminPermission()
def lock(uid):
    collection = Collection.query.get_or_404(uid)
    collection.locked = True
    db.session.add(collection)
    db.session.commit()
    return redirect(request.referrer or url_for('.view', uid=uid))


@bp.route('/collection/<int:uid>/unlock')
@AdminPermission()
def unlock(uid):
    collection = Collection.query.get_or_404(uid)
    collection.locked = False
    db.session.add(collection)
    db.session.commit()
    return redirect(request.referrer or url_for('.view', uid=uid))
