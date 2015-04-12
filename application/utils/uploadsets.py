# coding: utf-8
import os
import uuid
from PIL import Image
from flask.ext.uploads import UploadSet, IMAGES, extension

# UploadSets
avatars = UploadSet('avatars', IMAGES)
collection_covers = UploadSet('collectionCovers', IMAGES)
qrcodes = UploadSet('qrcodes', IMAGES)


def process_avatar(file_storage, upload_set, border):
    """Center clipping, resize and then save the avatar."""
    image = open_image(file_storage)
    image = center_crop(image)
    image = resize_square(image, border)
    ext = extension(file_storage.filename)
    return save_image(image, upload_set, ext)


def process_avatar_to_crop(file_storage, upload_set):
    """将图片处理为适合裁剪的大小，即长宽均不超过1000"""
    image = open_image(file_storage)
    image = resize_with_max(image, 1000)
    ext = extension(file_storage.filename)
    return save_image(image, upload_set, ext), image.size


def crop_avatar(filename, top_left_x_ratio, top_left_y_ratio, bottom_right_x_ratio,
                bottom_right_y_ratio):
    """裁剪用户头像"""
    file_path = avatars.path(filename)
    image = Image.open(file_path)
    image = crop_by_ratio(image, top_left_x_ratio, top_left_y_ratio, bottom_right_x_ratio,
                          bottom_right_y_ratio)
    image = center_crop(image)
    image = resize_square(image, 160)

    # 删除裁剪前的图片
    os.remove(file_path)

    # 保存裁剪后的图片
    ext = extension(filename)
    return save_image(image, avatars, ext)


def open_image(file_storage):
    """Open image from FileStorage."""
    image = Image.open(file_storage.stream)
    # See: https://github.com/smileychris/easy-thumbnails/issues/95
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image


def save_image(image, upload_set, ext):
    """Save image with random filename and original ext."""
    filename = '%s.%s' % (random_filename(), ext)
    dir_path = upload_set.config.destination

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    path = os.path.join(dir_path, filename)
    image.save(path)
    return filename


def center_crop(image):
    """居中裁剪"""
    w, h = image.size
    if w == h:
        return image

    if w > h:
        border = h
        avatar_crop_region = ((w - border) / 2, 0, (w + border) / 2, border)
    else:
        border = w
        avatar_crop_region = (0, (h - border) / 2, border, (h + border) / 2)
    return image.crop(avatar_crop_region)


def crop_by_ratio(image, top_left_x_ratio, top_left_y_ratio, bottom_right_x_ratio,
                  bottom_right_y_ratio):
    """通过左上角和右下角的坐标比例进行裁剪"""
    w, h = image.size
    crop_rect = (int(top_left_x_ratio * w), int(top_left_y_ratio * h),
                 int(bottom_right_x_ratio * w), int(bottom_right_y_ratio * h))
    return image.crop(crop_rect)


def resize_square(image, border):
    return image.resize((border, border), Image.ANTIALIAS)


def resize_with_max(image, max_value):
    w, h = image.size
    if w > h and w > max_value:
        target_w = max_value
        target_h = max_value * h / w
        return image.resize((target_w, target_h), Image.ANTIALIAS)
    elif h > w and h > max_value:
        target_h = max_value
        target_w = max_value * w / h
        return image.resize((target_w, target_h), Image.ANTIALIAS)
    else:
        return image


def random_filename():
    return str(uuid.uuid4())
