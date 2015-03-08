$('.pieces-wap')
    .on('click', 'a', function (event) {
        event.stopPropagation();
    }).on('click', '.piece', function () {
        var pieceId = parseInt($(this).attr('data-piece-id'));
        var pieceModal = $('.piece-modal').first();
        var pieceIdOfModal = parseInt(pieceModal.attr('data-piece-id'));

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
                pieceModal.attr('data-piece-id', pieceId);
                $.ajax({
                    url: urlFor('piece.modal', {uid: pieceId}),
                    success: function (modal) {
                        $('.piece-modal').html(modal);
                    }
                });
            });
        }
    });
