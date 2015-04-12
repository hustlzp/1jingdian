var imageWidth, imageHeight, imageUrl;
var previewWidth = 80, previewHeight = 80;
var jcropAPI = null;
var topLeftX, topLeftY, bottomRightX, bottomRightY;

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

            imageWidth = response.width;
            imageHeight = response.height;
            imageUrl = response.avatar_url;

            up.disableBrowse(false);

            if (response.result) {
                $('.upload-error-info').fadeOut();
                $('#modal-crop-avatar').modal('show');
                $('.avatar-preview').attr('src', imageUrl);
                $('.avatar-to-crop')
                    .attr('src', imageUrl)
                    .attr({'width': imageWidth, 'height': imageHeight})
                    .removeAttr('style')
                    .onOnce('load', function () {
                        var selectRect = null;

                        if (imageWidth > imageHeight) {
                            selectRect = [(imageWidth - imageHeight) / 2.0, 0,
                                    (imageWidth + imageHeight) / 2.0, imageHeight];
                        } else {
                            selectRect = [0, (imageHeight - imageWidth) / 2.0,
                                imageWidth, (imageHeight + imageWidth) / 2.0];
                        }

                        $('.avatar-to-crop').Jcrop({
                            onChange: showPreview,
                            onSelect: showPreview,
                            aspectRatio: 1
                        }, function () {
                            jcropAPI = this;
                            this.setSelect(selectRect);
                        });
                    });
            } else {
                $('.upload-error-info').fadeOut();
                $('.avatar-loading-percent').hide();
            }
        },

        // 上传失败
        Error: function (up) {
            $('.upload-error-info').fadeOut();
            $('.avatar-loading-percent').hide();
            up.disableBrowse(false);
        }
    }
}));

uploader.init();

function showPreview(coords) {
    var rx = previewWidth / coords.w;
    var ry = previewHeight / coords.h;

    topLeftX = coords.x;
    topLeftY = coords.y;
    bottomRightX = coords.x2;
    bottomRightY = coords.y2;

    $('.jcrop-holder').css('backgroundColor', '#ffffff');
    $('.avatar-preview').css({
        width: Math.round(rx * imageWidth) + 'px',
        height: Math.round(ry * imageHeight) + 'px',
        marginLeft: '-' + Math.round(rx * coords.x) + 'px',
        marginTop: '-' + Math.round(ry * coords.y) + 'px'
    });
}

$('#modal-crop-avatar').on('hidden.bs.modal', function () {
    $('.avatar-loading-percent').hide();
    jcropAPI.destroy();
});

// 保存头像
$('.btn-save-avatar').click(function () {
    var imageFileName = imageUrl.split('/').pop();

    $.ajax({
        url: urlFor('user.crop_avatar'),
        method: 'post',
        dataType: 'json',
        data: {
            'filename': imageFileName,
            'top_left_x_ratio': parseFloat(topLeftX) / imageWidth,
            'top_left_y_ratio': parseFloat(topLeftY) / imageHeight,
            'bottom_right_x_ratio': parseFloat(bottomRightX) / imageWidth,
            'bottom_right_y_ratio': parseFloat(bottomRightY) / imageHeight
        }
    }).done(function (response) {
        $('#modal-crop-avatar').modal('hide');
        if (response.result) {
            $('.user-avatar').attr('src', response.avatar_url);
        }
    });
});
