# -*- coding: utf-8 -*-
"""
This module provides functions for image augmentation.

It includes a function to transform an image by flipping or rotating it,
and a main function that applies these transformations to all images in a directory.
"""

import os
import sys
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# pylint: disable=wrong-import-position
import config.constants as const
import packages.utils.get_path as getpath


def transform_image(image_path, save_path, transformation, suffix):
    """
    Transforms an image and saves it to disk.

    This function opens an image, applies a transformation to it, converts it to RGB,
    and saves it to disk with a new filename.

    Args:
        image_path: The path to the image file.
        save_path: The path where the transformed image will be saved.
        transformation: The PIL.Image.Transpose method to apply to the image.
        suffix: The suffix to append to the filename of the transformed image.

    Returns:
        None. The function saves the transformed image to disk and does not return anything.
    """
    img = Image.open(image_path)
    # Transform the image
    transformed_img = img.transpose(transformation)
    # Convert the image to RGB
    transformed_img = transformed_img.convert(const.IMAGE_RBG)
    flip_image_path = (
        save_path
        + "/"
        + image_path.split("/")[-1].split(".")[0]
        + suffix
        + const.IMAGE_JPG_EXTENTION
    )
    transformed_img.save(flip_image_path)


def main():
    """
    Main function to apply image transformations to all images in a directory.

    This function retrieves the paths of the images and labels directories,
    creates a list of all image files in these directories,
    and applies image transformations to each image.
    The transformed images are saved to disk with new filenames.

    Returns:
        None. The function saves the transformed images to disk and does not return anything.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(script_dir)

    image_rgb_path = getpath.make_path(
        parent_dir, const.DATA_DIR, const.RAW_DIR, const.IMAGES_DIR
    )
    images_label_path = getpath.make_path(
        parent_dir, const.DATA_DIR, const.RAW_DIR, const.LABELS_DIR
    )

    images_item_list = getpath.make_item_list(
        image_rgb_path, file_ext=const.IMAGE_JPG_EXTENTION
    ) + getpath.make_item_list(images_label_path, file_ext=const.IMAGE_JPG_EXTENTION)
    folder_to_save = getpath.make_path(
        parent_dir, const.DATA_DIR, const.RAW_DIR, const.AUGMENTATION_DIR
    )

    image_to_be_augment = list(images_item_list)
    if len(image_to_be_augment) > 0:
        for path in image_to_be_augment:
            transform_image(
                path,
                folder_to_save,
                const.IMAGE_ROTATE_180,
                f"_R{const.IMAGE_ROTATE_180}"
            )
            print(f"Image {path} was augmented")


if __name__ == "__main__":
    main()
