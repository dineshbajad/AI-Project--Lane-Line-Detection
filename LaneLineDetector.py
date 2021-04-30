import cv2
import numpy as np

from ProbablistichoughLinesTransform import hough_lines
from cannyEdgeDetector import cannyEdgeDetector
from gaussianBlur import gaussian_blur
from grayscale import grayscale
from regionOfInterest import region_of_interest


def weighted_img(img, initial_img, α=0.1, β=1., γ=0.):
    lines_edges = cv2.addWeighted(initial_img, α, img, β, γ)
    # lines_edges = cv2.polylines(lines_edges,get_vertices(img), True, (0,0,255), 10)
    return lines_edges


def get_vertices(image):
    rows, cols = image.shape[:2]
    bottom_left = [cols * 0.15, rows]
    top_left = [cols * 0.45, rows * 0.6]
    bottom_right = [cols * 0.95, rows]
    top_right = [cols * 0.55, rows * 0.6]

    ver = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    return ver


# Lane finding Pipeline
def lane_finding_pipeline(image):
    # Grayscale
    gray_img = grayscale(image)
    # Gaussian Smoothing
    smoothed_img = gaussian_blur(img=gray_img, kernel_size=5)
    # Canny Edge Detection

    canny_img = cannyEdgeDetector(img=smoothed_img, low_threshold=180, high_threshold=240)
    # Masked Image Within a Polygon

    masked_img = region_of_interest(img=canny_img, vertices=get_vertices(image))
    # Hough Transform Lines
    houghed_lines = hough_lines(img=masked_img, rho=1, theta=np.pi / 180, threshold=20, min_line_len=20,
                                max_line_gap=180)
    # Draw lines on edges
    output = weighted_img(img=houghed_lines, initial_img=image, α=0.8, β=1., γ=0.)

    return output
