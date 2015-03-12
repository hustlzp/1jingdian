$('.source-help').popover({
    trigger: 'hover',
    container: 'body',
    content: '如：书籍、电影、歌曲、文章标题等。'
});

$('#original').change(function () {
    if ($(this).is(":checked")) {
        $('.external').slideUp('fast');
    } else {
        $('.external').slideDown('fast');
    }
});

var timer = null,
    sourceFavicon = $('.source-favicon'),
    sourceUrlInput = $('#source_url');

if ($.trim(sourceUrlInput.val()) !== "") {
    sourceFavicon.attr('src', 'http://g.soz.im/' + sourceUrlInput.val());
}

// 输入source url时，加载favicon
g.timer = null;
sourceUrlInput.keyup(function () {
    var input = $(this);
    clearTimeout(g.timer);
    g.timer = setTimeout(function () {
        sourceFavicon.attr('src', 'http://g.soz.im/' + input.val());
    }, 500);
});

// 图片加载失败时，隐藏
sourceFavicon.load(function () {
    $(this).fadeIn('fast');
}).error(function () {
    $(this).hide();
});
