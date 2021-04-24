#!/usr/bin/env python

import io
import numpy as np

from PIL import Image


base_classes = [
    "c_0",
    "c_1",
    "c_2",
    "c_3",
    "c_4",
    "c_5",
    "c_6",
    "c_7",
    "c_8",
    "c_9",
    "c_10",
    "c_11",
    "c_12",
    "c_13",
    "c_14",
    "c_15",
    "c_16",
    "c_17",
    "c_18",
    "c_19",
    "c_20",
    "c_21",
    "c_22",
    "c_23",
    "c_24",
    "c_25",
    "c_26",
    "c_27",
    "c_28",
    "c_29",
    "c_30",
    "c_31",
    "c_32",
    "c_33",
    "c_34",
    "c_35",
    "c_36",
    "c_37",
]

classes_and_models = {"model_1": {"classes": base_classes, "model_name": "model_1.pt"}}


def update_logger(
    image, model_used, pred_class, pred_conf, correct=False, user_label=None
):
    """
    Tracks feedback given in app, updates and returns logger dictionary.
    """

    logger = {
        "image": image,
        "model_used": model_used,
        "pred_class": pred_class,
        "correct": correct,
        "user_label": user_label,
    }
    return logger
