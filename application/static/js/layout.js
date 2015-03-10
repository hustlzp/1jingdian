// Flash message
setTimeout(showFlash, 200);
setTimeout(hideFlash, 2000);

// TODO: Need to stay popover when hovered.
$(document).popover({
    content: function () {
        return $(this).parent().nextAll('.popover-content-wap').first().html()
    },
    html: true,
    container: 'body',
    trigger: 'hover',
    placement: 'bottom',
    selector: '.user-avatar.user-avatar-popover',
    delay: {
        'hide': 100
    }
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
