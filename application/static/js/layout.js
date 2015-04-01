// Flash message
setTimeout(showFlash, 200);
setTimeout(hideFlash, 2000);

// 弹出用户卡片
$(document).on('mouseenter', '.user-avatar.user-avatar-popover', function () {
    var _this = $(this);

    $(this).popover({
        content: function () {
            return $(this).parent().nextAll('.popover-content-wap').first().html()
        },
        html: true,
        container: 'body',
        trigger: 'manual',
        placement: 'bottom',
        animation: false,
        viewport: {
            selector: 'body',
            padding: 15
        },
        selector: '.user-avatar.user-avatar-popover'
    }).popover('show');

    $(".popover").one("mouseleave", function () {
        $(_this).popover('destroy');
    });
});

$(document).on('mouseleave', '.user-avatar.user-avatar-popover', function () {
    var _this = $(this);

    setTimeout(function () {
        if (!$(".popover:hover").length) {
            $(_this).popover("destroy");
        }
    }, 200);
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
//$("input, textarea").focus(function () {
//    $(this).data('placeholder', $(this).attr('placeholder'))
//    $(this).attr('placeholder', '');
//}).blur(function () {
//    $(this).attr('placeholder', $(this).data('placeholder'));
//});

// 若某操作需要登陆，而用户尚未登陆，则跳转登陆页
$(document).on('click', '.need-signed-in', function () {
    if (!$(document.body).hasClass('signed-in')) {
        window.location = urlFor('account.signin');
    }
});

// 激活tooltip
$('[data-toggle="tooltip"]').tooltip();

// 操作系统标签
if (navigator.platform.indexOf('Win') > -1) {
    $('body').addClass('windows');
}

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

// Set the default settings of plupload.
plupload.Uploader.settings.flash_swf_url
    = '/static/bower_components/plupload/js/Moxie.swf';
plupload.Uploader.settings.silverlight_xap_url
    = '/static/bower_components/plupload/js/Moxie.xap';
