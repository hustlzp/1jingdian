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

// 输入source url时，加载favicon
g.timer = null;
$('#source_url').keyup(function () {
    var input = $(this);
    clearTimeout(g.timer);
    g.timer = setTimeout(function () {
        $('.source-favicon').attr('src', 'http://g.soz.im/' + input.val());
    }, 500);
});

// 图片加载失败时，隐藏
$('.source-favicon').load(function () {
    $(this).fadeIn('fast');
}).error(function () {
    $(this).hide();
});
