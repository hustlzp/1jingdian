// Flash message
setTimeout(showFlash, 200);
setTimeout(hideFlash, 2000);

$(document).popover({
    content: function () {
        return $(this).nextAll('.popover-content-wap').first().html()
    },
    html: true,
    container: 'body',
    trigger: 'hover',
    placement: 'bottom',
    selector: '.user-avatar'
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
