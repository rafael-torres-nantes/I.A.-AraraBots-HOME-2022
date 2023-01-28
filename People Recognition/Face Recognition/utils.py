from typing import List, Mapping, Optional, Tuple, Union

import math
import dataclasses

# Checks if the float value is between 0 and 1.
def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                  math.isclose(1, value))

def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
    """Converts normalized value pair to pixel coordinates."""
    if not (is_valid_normalized_value(normalized_x) and 
            is_valid_normalized_value(normalized_y)):
        # TODO: Draw coordinates even if it's outside of the image bounds.
        return None
    
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px

def get_bbox(image, detection):
    if not detection.location_data: return

    image_rows, image_cols, _ = image.shape
    location = detection.location_data

    if location.HasField('relative_bounding_box'):
        relative_bounding_box = location.relative_bounding_box
        rect_start_point = _normalized_to_pixel_coordinates(
             relative_bounding_box.xmin, relative_bounding_box.ymin, image_cols,
             image_rows)
        rect_end_point = _normalized_to_pixel_coordinates(
             relative_bounding_box.xmin + relative_bounding_box.width,
             relative_bounding_box.ymin + relative_bounding_box.height, image_cols,
             image_rows)

        return rect_start_point, rect_end_point

    return None
