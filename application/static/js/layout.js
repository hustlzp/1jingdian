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

// 顶句子
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
    if (!g.signedIn) {
        window.location = urlFor('account.signin');
        return false;
    }
});

$(document).on('click', '.need-signed-in', function () {
    if (!g.signedIn) {
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
    clearTimeout(g.timerForBackdrop);

    $.ajax({
        url: urlFor('piece.random'),
        method: 'POST',
        dataType: 'json'
    }).done(function (piece) {
        var contentLength = piece.content_length;
        var seconds = calculateTimeByContentLength(contentLength);

        openBackdrop(true, '偶遇', piece.id, piece.content, piece.source);

        g.timerForBackdrop = setTimeout(function () {
            beginMeet();
        }, seconds * 1000);
    });
});

// 按下Esc，关闭backdrop
$(document).keydown(function (e) {
    if (e.keyCode == 27) {
        closeBackdrop();
    }

    if (e.keyCode == 32 && checkBackdropExist()) {
        e.preventDefault();
        e.stopPropagation();

        if (checkRandomBackdropExist()) {
            beginMeet();
        }
    }
});

// 切入tab时，继续偶遇
window.onfocus = function () {
    if (checkRandomBackdropExist()) {
        setTimeout(function () {
            beginMeet();
        }, 4000);
    }
};

// 切出tab时，停止偶遇
window.onblur = function () {
    if (checkRandomBackdropExist()) {
        clearTimeout(g.timerForBackdrop);
    }
};

// 按下关闭按钮，关闭backdrop
$(document).on('click', '.btn-close-backdrop', function () {
    closeBackdrop();
});

// 调整modal高度
$('.modal-need-adjust-height').on('show.bs.modal', function () {
    var _this = $(this);

    setTimeout(function () {
        var $dialog = _this.find(".modal-dialog");
        var offset;

        _this.css('display', 'block');
        offset = ($(window).height() - $dialog.height()) * 0.3;

        if (offset > 0) {
            $dialog.css('margin-top', offset);
        }
    }, 50);
});

/**
 * Open the backdrop.
 */
function openBackdrop(random, title, id, content, source) {
    var html = "<div class='full-screen-backdrop";

    if (random) {
        html += " random"
    }

    html += "'>";

    if (title !== "") {
        html += "<div class='title'>" + title + "</div>";
    }

    html += "<span class='btn-close-backdrop'>×</span>"
        + "<a target='_blank' class='piece-link' href='" + urlFor('piece.view', {uid: id}) + "'>"
        + "<span class='fa fa-external-link'></span>"
        + "</a>"
        + "<div class='wap'>"
        + "<div class='content'>" + content + "</div>";

    if (source !== "") {
        html += "<div class='source'>" + source + "</div>";
    }

    html += "</div></div>";

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
        verticalMargin;

    if (!$wap.length) {
        return;
    }

    // 若content为单行，则居中排版
    if ($content.height() < 100) {
        $content.addClass('text-center');
    } else {
        $content.removeClass('text-center');
    }

    console.log($wap.height());

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
 * Check if the backdrop with class 'random' is open.
 * @returns {boolean}
 */
function checkRandomBackdropExist() {
    return $('.full-screen-backdrop.random').length > 0;
}

/**
 * Check if the backdrop is open.
 * @returns {boolean}
 */
function checkBackdropExist() {
    return $('.full-screen-backdrop').length > 0;
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

/**
 * Begin meet random piece.
 */
function beginMeet() {
    clearTimeout(g.timerForBackdrop);

    $.ajax({
        url: urlFor('piece.random'),
        method: 'POST',
        dataType: 'json'
    }).done(function (piece) {
        var contentLength = piece.content_length;
        var seconds = calculateTimeByContentLength(contentLength);

        $('.full-screen-backdrop .content').hide().text(piece.content).fadeIn('slow');

        if (piece.source) {
            $('.full-screen-backdrop .source').hide().text(piece.source).fadeIn('slow');
        } else {
            $('.full-screen-backdrop .source').hide();
        }

        $('.full-screen-backdrop .piece-link').attr('href', urlFor('piece.view', {uid: piece.id}));

        adjustBackdropContent();

        g.timerForBackdrop = setTimeout(function () {
            beginMeet();
        }, seconds * 1000);
    });
}

/**
 * Calculate read time based on content length.
 * @param contentLength
 * @returns read time
 */
function calculateTimeByContentLength(contentLength) {
    var seconds;
    contentLength = parseInt(contentLength);

    if ($.isNumeric(contentLength)) {
        // 设定阅读速度为10字/s
        seconds = Math.ceil(contentLength / 10);
        if (seconds < 8) {
            seconds = 8;
        }
    } else {
        seconds = 8;
    }

    return seconds;
}

window.openBackdrop = openBackdrop;
