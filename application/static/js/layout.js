// Flash message
setTimeout(showFlash, 200);
setTimeout(hideFlash, 2000);

// 弹出用户卡片
// TODO: Need to stay popover when hovered.
$(document).popover({
    content: function () {
        return $(this).parent().nextAll('.popover-content-wap').first().html()
    },
    html: true,
    container: 'body',
    trigger: 'hover',
    placement: 'bottom',
    selector: '.user-avatar.user-avatar-popover',
    delay: {
        'hide': 100
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

// 点击input或textare，隐藏placeholder
$("input, textarea").focus(function () {
    $(this).data('placeholder', $(this).attr('placeholder'))
    $(this).attr('placeholder', '');
}).blur(function () {
    $(this).attr('placeholder', $(this).data('placeholder'));
});

// 若某操作需要登陆，而用户尚未登陆，则跳转登陆页
$('.need-signed-in').click(function () {
    if (!$(document.body).hasClass('signed-in')) {
        window.location = urlFor('account.signin');
    }
});

/**
 * Show flash message.
 */
function showFlash() {
    $('.flash-message').slideDown('fast');
}

/**
 * Hide flash message.
 */
function hideFlash() {
    $('.flash-message').slideUp('fast');
}
