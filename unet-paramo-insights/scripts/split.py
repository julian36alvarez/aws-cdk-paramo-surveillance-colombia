# -*- coding: utf-8 -*-
"""
This module provides functions for splitting images into smaller images.

It includes a function to divide an image into smaller images of a specified size,
and a main function that applies this operation to all images in a directory.
"""

import os
import sys
import argparse
from PIL import Image

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# pylint: disable=wrong-import-position
import config.constants as const
import packages.utils.get_path as get_path_module


def divide_image(image, save_path):
    """
    Divide a larger image into smaller images of a fixed size.
    Parameters:
    image (str): The path to the image to divide.
    save_path (str): The path where the smaller images will be saved.
    Returns:
    None
    """
    img_size = const.IMAGE_SIZE
    print(f"{const.IMAGE_NAME}: {image}")
    image_name = image.split("/")[-1].split(".")[0]
    with Image.open(image) as img:
        rows, cols = img.size[1] // img_size, img.size[0] // img_size
        # Loop over the smaller images and save them to disk
        for row in range(rows):
            for col in range(cols):
                # Crop the input image to the current smaller image
                cropped_img = img.crop((col * img_size, row * img_size,
                                        (col + 1) * img_size,
                                        (row + 1) * img_size))
                cropped_img = cropped_img.convert(const.IMAGE_RBG)  # Convert to RGB mode
                dir_path = f"{save_path}/{image_name}"
                if not os.path.exists(dir_path):
                    print(f"Creating directory: {dir_path}")
                    os.makedirs(dir_path, exist_ok=True)
                cropped_img.save(f"{dir_path}/{image_name}_{row}_{col}{const.IMAGE_JPG_EXTENTION}")


def main(flag):
    """
    Main function to divide all images in a directory into smaller images.

    This function retrieves the paths of the images and labels directories,
    creates a list of all image files in these directories,
    and divides each image into smaller images.
    The smaller images are saved to disk with new filenames.

    Args:
        flag (bool): If True, the function also divides the augmented images.

    Returns:
        None. The function saves the smaller images to disk and does not return anything.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(script_dir)

    image_rgb_path = get_path_module.make_path(
        parent_dir, const.DATA_DIR, const.RAW_DIR, const.NORMALIZATION_DIR_IMAGES
    )
    images_label_path = get_path_module.make_path(
        parent_dir, const.DATA_DIR, const.RAW_DIR, const.LABELS_DIR
    )
    image_augmentation_path = get_path_module.make_path(
        parent_dir, const.DATA_DIR, const.RAW_DIR, const.AUGMENTATION_DIR
    )
    images_item_list = get_path_module.make_item_list(
        image_rgb_path, file_ext=const.IMAGE_JPG_EXTENTION
    ) + get_path_module.make_item_list(images_label_path, file_ext=const.IMAGE_JPG_EXTENTION)

    if flag:
        images_item_list += get_path_module.make_item_list(
            image_augmentation_path, file_ext=const.IMAGE_JPG_EXTENTION
        )

    folder_to_save = get_path_module.make_path(parent_dir, const.DATA_DIR, const.INTERMEDIATE_DIR)

    for i in images_item_list:
        divide_image(i, folder_to_save)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--augment_data", type=str, default="False")
    args = parser.parse_args()
    augment_data_flag = args.augment_data.lower() in ["true", "1", "t", "y", "yes"]
    main(augment_data_flag)
