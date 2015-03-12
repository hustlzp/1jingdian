$('.source-help').popover({
    trigger: 'hover',
    container: 'body',
    content: '如：书名、电影名、人名、文章标题等。'
});

$('#original').change(function () {
    if ($(this).is(":checked")) {
        $('.external').slideUp('fast');
    } else {
        $('.external').slideDown('fast');
    }
});
