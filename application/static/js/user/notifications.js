$('.notification').click(function () {
    var id = $(this).data('id')
    window.location = urlFor('user.check_notification', {uid: id});
});

$('.btn-check-all').click(function () {
    $.ajax({
        url: urlFor('user.check_all_notifications'),
        method: 'post',
        dataType: 'json'
    }).done(function (response) {
        if (response.result) {
            $('.only-for-nonzero').hide();
            $('.notification').addClass('checked');
            $('.notifications-count').hide();
        }
    });
});
