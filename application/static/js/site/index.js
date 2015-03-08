$('.pieces-wap').on('click', '.piece', function (event) {
    // 链接和vote不触发此事件
    if (event.target.tagName.toLowerCase() === 'a'
        || $(event.target).hasClass('vote')
        || $(event.target).parents('.vote').length) {
        return true;
    }

    var pieceId = parseInt($(this).attr('data-piece-id')),
        pieceModal = $('.piece-modal').first(),
        pieceIdOfModal = parseInt(pieceModal.attr('data-piece-id'));

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

$(document).on('click', '.vote', function () {
    var pieceId = parseInt($(this).attr('data-piece-id')),
        url = "",
        votesCount = $(this).find('.votes-count').first(),
        vote = $(this),
        voted = $(this).hasClass('voted');

    if (voted) {
        url = urlFor('piece.unvote', {uid: pieceId});
    } else {
        url = urlFor('piece.vote', {uid: pieceId});
    }

    $.ajax({
        url: url,
        method: 'post',
        dataType: 'json',
        success: function (response) {
            var currentVotesCount = parseInt(votesCount.text()),
                targetVotesCount;
            if (response.result) {
                if (voted) {
                    targetVotesCount = (currentVotesCount > 0) ? currentVotesCount - 1 : 0;
                    $(".vote[data-piece-id=" + pieceId + "]")
                        .removeClass('voted')
                        .find('.votes-count').text(targetVotesCount);
                } else {
                    targetVotesCount = currentVotesCount + 1;
                    $(".vote[data-piece-id=" + pieceId + "]")
                        .addClass('voted')
                        .find('.votes-count').text(targetVotesCount);
                }
            }
        }
    });
});
