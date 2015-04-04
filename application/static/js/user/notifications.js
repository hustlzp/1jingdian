$('.notification').click(function () {
    var id = $(this).data('id')
    window.location = urlFor('user.check_notification', {uid: id});
});
