$('.tips').hide().fadeIn('slow', function () {
    $.ajax({
        url: urlFor('piece.random'),
        method: 'POST',
        dataType: 'json'
    }).done(function (piece) {
        var contentLength = piece.content_length;
        var seconds = calculateTimeByContentLength(contentLength);

        setTimeout(function () {
            openBackdrop(true, '偶遇', piece.id, piece.content, piece.source);

            g.timerForBackdrop = setTimeout(function () {
                beginMeet();
            }, seconds * 1000);
        }, 800);
    });
});


// 切入tab时，继续偶遇
window.onfocus = function () {
    if (checkBackdropExist()) {
        g.timerForBackdrop = setTimeout(function () {
            beginMeet();
        }, 4000);
    }
};

// 切出tab时，停止偶遇
window.onblur = function () {
    if (checkBackdropExist()) {
        clearTimeout(g.timerForBackdrop);
    }
};

// 按下Esc，关闭backdrop
$(document).keydown(function (e) {
    if (e.keyCode == 32 && checkBackdropExist()) {
        beginMeet();
    }
});

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
        // 设定阅读速度为8字/s
        seconds = Math.ceil(contentLength / 8);
        if (seconds < 10) {
            seconds = 10;
        }
    } else {
        seconds = 10;
    }

    return seconds;
}
