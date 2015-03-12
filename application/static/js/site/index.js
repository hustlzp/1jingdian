//// 下拉加载往期文字
//$.extend(g, {
//    // 是否正在加载
//    loading: false,
//    // 下一次加载的起始日期
//    startDate: moment(g.startDate),
//    // 每次加载多少天的数据
//    DAYS: 2
//});
//
//$(window).scroll(function () {
//    if ($(window).scrollTop() == $(document).height() - $(window).height()) {
//        if (!g.loading) {
//            g.loading = true;
//            $('.loading-flag').fadeIn();
//
//            setTimeout(function () {
//                console.log(g.startDate);
//                $.ajax({
//                    url: urlFor('piece.pieces_by_date'),
//                    method: 'post',
//                    data: {
//                        'start': g.startDate.format('YYYY-MM-DD'),
//                        'days': g.DAYS
//                    }
//                }).done(function (html) {
//                    $('.pieces-container').append(html);
//                    g.startDate = g.startDate.subtract(g.DAYS, 'days');
//                }).always(function () {
//                    g.loading = false;
//                    $('.loading-flag').fadeOut();
//                });
//            }, 800);
//        }
//    }
//});
