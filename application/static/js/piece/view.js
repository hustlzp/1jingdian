var hash = window.location.hash;

if (hash) {
    var commentId = parseInt(hash.split('_').pop());
    var $comment = $(".comment[data-comment-id='" + commentId + "']");

    $(window).scrollTo($comment, 100, {
        offset: {
            top: -105
        },
        onAfter: function () {
            $comment.css('backgroundColor', '#eff6fa');
            setTimeout(function () {
                $comment.animate({
                    'backgroundColor': '#ffffff'
                }, 800)
            }, 1000);
        }
    });
}
