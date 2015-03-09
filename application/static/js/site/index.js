// 弹出侧边栏
$('.pieces-wap').on('click', '.piece', function (event) {
    // 链接和vote不触发此事件
    if (event.target.tagName.toLowerCase() === 'a'
        || $(event.target).hasClass('vote')
        || $(event.target).hasClass('user-avatar')
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
        if (pieceModal.hasClass('open')) {
            pieceModal.attr('data-piece-id', pieceId);
            $.ajax({
                url: urlFor('piece.modal', {uid: pieceId}),
                success: function (modal) {
                    $('.piece-modal').html(modal);
                }
            });
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

    }
});

// 投票
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

// 下拉加载往期文字
$.extend(g, {
    // 是否正在加载
    loading: false,
    // 下一次加载的起始日期
    startDate: moment(g.startDate),
    // 每次加载多少天的数据
    DAYS: 2
});

$(window).scroll(function () {
    if ($(window).scrollTop() == $(document).height() - $(window).height()) {
        if (!g.loading) {
            g.loading = true;
            $('.loading-flag').fadeIn();

            setTimeout(function () {
                console.log(g.startDate);
                $.ajax({
                    url: urlFor('piece.pieces_by_date'),
                    method: 'post',
                    data: {
                        'start': g.startDate.format('YYYY-MM-DD'),
                        'days': g.DAYS
                    }
                }).done(function (html) {
                    $('.pieces-container').append(html);
                    g.startDate = g.startDate.subtract(g.DAYS, 'days');
                }).always(function () {
                    g.loading = false;
                    $('.loading-flag').fadeOut();
                });
            }, 800);
        }
    }
});
