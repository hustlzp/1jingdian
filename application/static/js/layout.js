// plupload全局配置
registerContext({
    pluploadDefaults: {
        flash_swf_url: '/static/bower_components/plupload/js/Moxie.swf',
        silverlight_xap_url: '/static/bower_components/plupload/js/Moxie.xap'
    },
    timerForBackdrop: null
});

// Flash message
setTimeout(showFlash, 200);
setTimeout(hideFlash, 2000);

// 弹出用户卡片
$(document).on('mouseenter', '.user-avatar.user-avatar-popover', function () {
    var _this = $(this);

    // 隐藏其他的用户卡片
    $('.user-avatar.user-avatar-popover').popover('destroy');

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

// 隐藏用户卡片
$(document).on('mouseleave', '.user-avatar.user-avatar-popover', function () {
    var _this = $(this);

    setTimeout(function () {
        if (!$(".popover:hover").length) {
            $(_this).popover("destroy");
        }
    }, 200);
});

// 顶
$(document).on('click', '.vote', function () {
    var pieceId = parseInt($(this).attr('data-piece-id')),
        url = "",
        voted = $(this).hasClass('voted'),
        _this = $(this);

    if (voted) {
        url = urlFor('piece.unvote', {uid: pieceId});
    } else {
        url = urlFor('piece.vote', {uid: pieceId});
    }

    // 点击后立即出发效果
    toggleVoteEffect(_this);

    $.ajax({
        url: url,
        method: 'post',
        dataType: 'json'
    }).done(function (response) {
        if (!response.result) {
            toggleVoteEffect(_this);
        }
    }).fail(function () {
        toggleVoteEffect(_this);
    });
});

/**
 * 切换顶效果
 * @param $voteElement
 */
function toggleVoteEffect($voteElement) {
    var voted = $voteElement.hasClass('voted');
    var pieceId = parseInt($voteElement.attr('data-piece-id'));
    var currentVotesCount = parseInt($voteElement.find('.votes-count').text());
    var targetVotesCount = 0;

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

// 若某操作需要登陆，而用户尚未登陆，则跳转登陆页
$('.need-signed-in').click(function () {
    if (!$(document.body).hasClass('signed-in')) {
        window.location = urlFor('account.signin');
        return false;
    }
});

$(document).on('click', '.need-signed-in', function () {
    if (!$(document.body).hasClass('signed-in')) {
        window.location = urlFor('account.signin');
        return false;
    }
});

// 激活tooltip
$('[data-toggle="tooltip"]').tooltip();

// 操作系统class
if (navigator.platform.indexOf('Win') > -1) {
    $('body').addClass('windows');
}

// 偶遇
$('.btn-meet').click(function () {
    $.ajax({
        url: urlFor('piece.random'),
        method: 'POST',
        dataType: 'json'
    }).done(function (piece) {
        var html = "<div class='content'>" + piece.content + "</div>";

        if (piece.source) {
            html += "<div class='source'>" + piece.source + "</div>";
        }

        openBackdrop('偶遇', html);
    });

    if (g.timerForBackdrop) {
        clearInterval(g.timerForBackdrop);
    }

    g.timerForBackdrop = setInterval(function () {
        $.ajax({
            url: urlFor('piece.random'),
            method: 'POST',
            dataType: 'json'
        }).done(function (piece) {
            $('.full-screen-backdrop .content').hide().text(piece.content).fadeIn();
            if (piece.source) {
                $('.full-screen-backdrop .source').hide().text(piece.source).fadeIn();
            } else {
                $('.full-screen-backdrop .source').hide();
            }

            adjustBackdropContent();
        });
    }, 8000);
});

// 按下Esc，关闭backdrop
$(document).keyup(function (e) {
    if (e.keyCode == 27) {
        closeBackdrop();
    }
});

// 按下关闭按钮，关闭backdrop
$(document).on('click', '.btn-close-backdrop', function () {
    closeBackdrop();
});

// 调整modal高度
$('.modal-need-adjust-height').on('show.bs.modal', function () {
    $(this).css('display', 'block');
    var $dialog = $(this).find(".modal-dialog");
    var offset = ($(window).height() - $dialog.height()) * 0.3;
    if (offset > 0) {
        $dialog.css('margin-top', offset);
    }
});

/**
 * Open the backdrop.
 */
function openBackdrop(title, content_html) {
    var html = "<div class='full-screen-backdrop'>";

    if (title !== "") {
        html += "<div class='title'>" + title + "</div>";
    }

    html += "<span class='btn-close-backdrop'>×</span>"
        + "<div class='wap'>" + content_html + "</div>"
        + "</div>";

    $('body').append(html);
    adjustBackdropContent();

    setTimeout(function () {
        $('.full-screen-backdrop').css('opacity', '.8');
        $('.base-wap').addClass('blur');
    }, 100);
}

/**
 * Adjust content in the backdrop.
 */
function adjustBackdropContent() {
    var $wap = $('.full-screen-backdrop .wap'),
        $content = $('.full-screen-backdrop .wap .content'),
        verticalMargin = 0;

    if (!$wap.length) {
        return;
    }

    // 若content为单行，则居中排版
    if ($content.height() < 100) {
        $content.addClass('text-center');
    } else {
        $content.removeClass('text-center');
    }

    // 上边距最小为80px
    verticalMargin = ($(window).height() - $wap.height()) / 2;
    if (verticalMargin < 80) {
        verticalMargin = 80;
    }

    $wap.css({
        'marginTop': verticalMargin,
        'marginBottom': verticalMargin
    });
}

/**
 * Close the backdrop.
 */
function closeBackdrop() {
    $('.base-wap').removeClass('blur');
    $('.full-screen-backdrop').detach();
    clearInterval(g.timerForBackdrop);
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

window.openBackdrop = openBackdrop;
