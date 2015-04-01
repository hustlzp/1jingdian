var uploader = new plupload.Uploader($.extend(g.pluploadDefaults, {
    browse_button: 'btn-upload-avatar',
    url: urlFor('user.upload_avatar'),
    multipart_params: {
        'csrf_token': g.csrfToken
    }
}));

//var options = $.extend(g.pluploadDefaults, {
//    browse_button: 'btn-upload-avatar',
//    url: urlFor('user.upload_avatar'),
//    multipart_params: {
//        'csrf_token': g.csrfToken
//    }
//});
//
//alert(options);
//
//var uploader = new plupload.Uploader(options);

uploader.init();

// 文件添加后立即上传
uploader.bind('FilesAdded', function (up, files) {
    plupload.each(files, function (file) {
        uploader.start();
    });
});

// 上传头像
uploader.bind('FileUploaded', function (up, file, info) {
    var response = $.parseJSON(info.response);
    if (response.result) {
        $('.upload-error-info').fadeOut();
        $('.user-avatar').hide().attr('src', response.avatar_url).fadeIn('fast');
    } else {
        $('.upload-error-info').fadeIn();
    }
});
