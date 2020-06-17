import sys
from typing import Tuple

import cv2
import matplotlib.pyplot as plt
import numpy as np
from keras_retinanet.models import load_model
from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.image import read_image_bgr
from keras_retinanet.utils.visualization import draw_box, draw_caption
from skimage.io import imread

_labels_to_names = {
    0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane',
    5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light',
    10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench',
    14: 'bird', 15: 'cat', 16: 'piesel', 17: 'horse', 18: 'sheep', 19: 'cow',
    20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack',
    25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee',
    30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite',
    34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard',
    37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass',
    41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
    46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli',
    51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake',
    56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed',
    60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse',
    65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave',
    69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book',
    74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
    78: 'hair drier', 79: 'toothbrush'}


def _predict(model, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    image = image.astype("float32")
    image = np.expand_dims(image, 0)
    boxes, scores, labels = model.predict_on_batch(image)
    return boxes[0], scores[0], labels[0]


def _get_marked_image(image, boxes: np.ndarray, scores: np.ndarray, labels: np.ndarray) -> np.ndarray:
    image = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for box, score, label in zip(boxes, scores, labels):
        if score < 0.5:
            break
        box = box.astype(int)
        draw_box(image, box, color=label_color(label))
        caption = f"{_labels_to_names[label].capitalize()}: {score * 100:.1f}%"
        draw_caption(image, box, caption)
    return image


def _display(image) -> None:
    plt.figure(figsize=(image.shape[1] // 100, image.shape[0] // 100))
    plt.axis("off")
    plt.imshow(image)
    plt.show()


def _grab_camera_snapshot(camera_id=0) -> np.ndarray:
    camera = cv2.VideoCapture(camera_id)
    try:
        for i in range(15):
            snapshot_ok, image = camera.read()
        if not snapshot_ok:
            print("Could not access camera")
    finally:
        camera.release()
    return image


def evaluate_image_from_file(model, file_name: str) -> None:
    _display(_get_marked_image(read_image_bgr(file_name), *_predict(model, imread(file_name))))


def evaluate_taken_photo(model) -> None:
    image = _grab_camera_snapshot()
    _display(_get_marked_image(image, *_predict(model, image)))


def evaluate_camera_stream(model, camera_id=0) -> None:
    camera = cv2.VideoCapture(camera_id)
    plt.ion()
    fig, ax = plt.subplots()
    fig.canvas.draw_idle()
    fig.set_size_inches(14, 9)
    plt.axis("off")
    screen = ax.imshow(np.ndarray(shape=(9, 14), dtype=np.int))
    while True:
        snapshot_ok, image = camera.read()
        if not snapshot_ok:
            print("Could not access camera", file=sys.stderr)
            exit(2)
        screen.set_data(_get_marked_image(image, *_predict(model, image)))
        plt.draw()
        plt.pause(0.00001)


def _error():
    print('You need to specify argument: "--image", "--photo" or "--stream"', file=sys.stderr)
    exit(1)


def _get_model():
    model = None
    try:
        model = load_model("resnet50_coco_best_v2.1.0.h5", backbone_name="resnet50")
    except OSError:
        print("Not found file resnet50_coco_best_v2.1.0.h5 with trained model. "
              "You can download it here: "
              "https://github.com/fizyr/keras-retinanet/releases/download/0.5.1/resnet50_coco_best_v2.1.0.h5",
              file=sys.stderr)
        exit(3)
    return model


if __name__ == "__main__":
    if len(sys.argv) < 2:
        _error()
    mode = sys.argv[1]
    if mode == "--image":
        if len(sys.argv) < 3:
            print('You need to specify file name.', file=sys.stderr)
            exit(1)
        evaluate_image_from_file(_get_model(), sys.argv[2])
    elif mode == "--photo":
        evaluate_taken_photo(_get_model())
    elif mode == "--stream":
        evaluate_camera_stream(_get_model())
    else:
        _error()
