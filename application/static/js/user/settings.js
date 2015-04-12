var uploader = new plupload.Uploader($.extend(g.pluploadDefaults, {
    browse_button: 'btn-upload-avatar',
    url: urlFor('user.upload_avatar'),
    multipart_params: {
        'csrf_token': g.csrfToken
    },
    max_file_size: '10mb',
    init: {
        // 文件添加后立即上传
        FilesAdded: function (up, files) {
            up.disableBrowse(true);
            $('.avatar-loading-percent').show();

            plupload.each(files, function () {
                uploader.start();
            });
        },

        // 上传进度
        UploadProgress: function (up, file) {
            $('.avatar-loading-percent').text(file.percent + "%");
        },

        // 上传完毕
        FileUploaded: function (up, file, info) {
            var response = $.parseJSON(info.response);

            up.disableBrowse(false);

            if (response.result) {
                $('.upload-error-info').fadeOut();
                $('.user-avatar')
                    .attr('src', response.avatar_url)
                    .onOnce('load', function () {
                        $('.avatar-loading-percent').hide();
                    });
            } else {
                $('.upload-error-info').fadeOut();
                $('.avatar-loading-percent').hide();
            }
        },

        // 上传失败
        Error: function () {
            $('.upload-error-info').fadeOut();
            $('.avatar-loading-percent').hide();
            up.disableBrowse(false);
        }
    }
}));

uploader.init();
