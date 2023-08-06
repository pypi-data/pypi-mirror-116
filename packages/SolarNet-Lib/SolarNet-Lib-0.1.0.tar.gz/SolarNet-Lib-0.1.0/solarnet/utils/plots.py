import math
from pathlib import Path
from typing import List, Optional, Union

import matplotlib.pyplot as plt

colors = {
    "black": "#000000",
    "green": "#34a853",
    "red": "#af001e",
}


def plot_image_grid(
    images: list,
    y: List[Union[int, float]] = None,
    y_pred: Optional[List[Union[int, float]]] = None,
    y_proba: Optional[List[List[float]]] = None,
    labels: List[str] = None,
    columns: int = 5,
    width: int = 22,
    max_images: int = 10,
    label_font_size: int = 14,
    save_path: Optional[Path] = None,
):
    """
    Display a grid of images with labels. Compares true labels and predictions if predictions are given.
    The true values and predictions can be regression values (float).

    :param images: list of image (format supported by plt.imshow())
    :param y: list of labels (int) or values (float for regression)
    :param y_pred: list of predictions (int) or values (float for regression)
    :param y_proba: list of probabilities (float) for predictions
    :param labels: list of string labels
    :param columns: number of images to show in a row
    :param width: width of the figure
    :param max_images: Number max of image to show from the given list
    :param label_font_size: Size of the labels
    :param save_path: optional path where the figure will be saved
    """

    def pretty_label(label: int) -> str:
        return label if labels is None else labels[label]

    if len(images) > max_images:
        images = images[0:max_images]

    is_regression = y is not None and not isinstance(y[0], int) and not isinstance(y[0], str)
    if is_regression:
        pretty_label = lambda x: f'{x:.1e}'

    height = width * math.ceil(len(images) / columns) / columns * 1.33

    plt.figure(figsize=(width, height))
    # plt.subplots_adjust(wspace=0.05)
    # plt.subplots_adjust(hspace=0.2)

    if y_proba is not None and not is_regression:
        # Take probability of y_pred
        y_proba = [p[y_pred[i]] for i, p in enumerate(y_proba)]

    for i, image in enumerate(images):
        plt.subplot(int(len(images) / columns + 1), columns, i + 1)
        plt.imshow(image)
        plt.axis("off")

        if y is not None:
            if y_pred is None:
                title = pretty_label(y[i])
                color = colors["black"]
            elif is_regression:
                title = f"y_true: {pretty_label(y[i])}\ny_pred: {pretty_label(y_pred[i])}"
                color = colors["black"]
            else:
                is_correct = y[i] == y_pred[i]
                if is_correct:
                    title = f"y_true & y_pred: {pretty_label(y[i])}"
                    color = colors["green"]
                else:
                    title = f"y_true: {pretty_label(y[i])} / y_pred: {pretty_label(y_pred[i])}"
                    color = colors["red"]
                if y_proba is not None:
                    title += f" ({y_proba[i]:.2f})"
            plt.title(title, fontsize=label_font_size, color=color, wrap=True)

    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path, bbox_inches="tight")
