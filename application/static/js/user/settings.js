var uploader = new plupload.Uploader($.extend(g.pluploadDefaults, {
    browse_button: 'btn-upload-avatar',
    url: urlFor('user.upload_avatar'),
    multipart_params: {
        'csrf_token': g.csrfToken
    }
}));

uploader.init();

// 文件添加后立即上传
uploader.bind('FilesAdded', function (up, files) {
    $('.avatar-wap .loading-flag').show();
    plupload.each(files, function () {
        uploader.start();
    });
});

// 上传头像
uploader.bind('FileUploaded', function (up, file, info) {
    var response = $.parseJSON(info.response);

    if (response.result) {
        $('.upload-error-info').fadeOut();
        $('.user-avatar').attr('src', response.avatar_url);
    } else {
        $('.upload-error-info').fadeOut();
    }

    $('.avatar-wap .loading-flag').hide();
});
