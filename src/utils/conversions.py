
def convert_bbox(size, box):
    """Convert [x_min, y_min, x_max, y_max] → YOLO (x_center, y_center, w, h) normalized"""
    W, H = size
    x_min, y_min, x_max, y_max = box
    x_c = (x_min + x_max) / 2.0 / W
    y_c = (y_min + y_max) / 2.0 / H
    w = (x_max - x_min) / W
    h = (y_max - y_min) / H
    return (x_c, y_c, w, h)
