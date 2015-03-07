$('.pieces-wap').on('click', '.piece', function () {
    var pieceModal = $('.piece-modal').first();
    var pieceId = parseInt($(this).data('piece-id'));
    var pieceIdOfModal = parseInt(pieceModal.data('piece-id'));

    if (pieceId === pieceIdOfModal) {
        if (pieceModal.hasClass('open')) {
            pieceModal.animate({'right': '-503px'}, function () {
                pieceModal.removeClass('open');
            });
        } else {
            pieceModal.animate({'right': '0'}, function () {
                pieceModal.addClass('open');
            });
        }
    } else {
        pieceModal.animate({'right': '0'}, function () {
            pieceModal.addClass('open');
        });
    }
});
