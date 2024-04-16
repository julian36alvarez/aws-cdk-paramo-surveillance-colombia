import numpy as np
import rasterio
from rasterio.merge import merge
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# pylint: disable=wrong-import-position
import config.constants as const
import packages.utils.get_path as get_path_module


script_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(script_dir)

all_images_path = get_path_module.make_path(
    parent_dir, const.DATA_DIR, const.OUTPUT_DIR, const.LABELS_DIR
)

save_merged_path = get_path_module.make_path(
    parent_dir, const.DATA_DIR, const.OUTPUT_DIR, const.MERGED_DIR
)


def merge_images(folder_path, output_folder):
    filenames = os.listdir(folder_path)

    tiff_files = [f for f in filenames if f.endswith(const.TIF_EXTENTION)]
    tiff_paths = [os.path.join(folder_path, f) for f in tiff_files]

    datasets = [rasterio.open(fp) for fp in tiff_paths]
    # Merge the datasets into a single image
    mosaic, out_trans = merge(datasets)
    # Write the result to a new .tif file
    out_meta = datasets[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
    })
    output_filename = os.path.join(output_folder, "{}{}".format(os.path.basename(folder_path)[-36:], const.TIF_EXTENTION))
    with rasterio.open(output_filename, "w", **out_meta) as dest:
        dest.write(mosaic)
    # Close the datasets
    for ds in datasets:
        ds.close()

for folder_name in os.listdir(all_images_path):
    folder_path = os.path.join(all_images_path, folder_name)
    if os.path.isdir(folder_path):
       merge_images(folder_path, save_merged_path)

