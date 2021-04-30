import cv2
import numpy as np

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):

    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    # draw_lines(line_img, lines)
    line_img = slope_lines(line_img, lines)
    return line_img

def slope_lines(image, lines):
    img = image.copy()
    poly_vertices = []
    order = [0, 1, 3, 2]

    left_lines = []
    right_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:

            if x1 == x2:
                pass  # Vertical Lines
            else:
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1

                if m < 0:
                    left_lines.append((m, c))
                elif m >= 0:
                    right_lines.append((m, c))

    left_line = np.mean(left_lines, axis=0)
    right_line = np.mean(right_lines, axis=0)


    for slope, intercept in [left_line, right_line]:
        # getting complete height of image in y1
        rows, cols = image.shape[:2]
        y1 = int(rows)  # image.shape[0]

        # taking y2 upto 60% of actual height or 60% of y1
        y2 = int(rows * 0.6)  # int(0.6*y1)

        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
        poly_vertices.append((x1, y1))
        poly_vertices.append((x2, y2))
        draw_lines(img, np.array([[[x1, y1, x2, y2]]]))

    poly_vertices = [poly_vertices[i] for i in order]
    cv2.fillPoly(img, pts=np.array([poly_vertices], 'int32'), color=(0, 255, 0))
    return cv2.addWeighted(image, 0.7, img, 0.4, 0.)

    # cv2.polylines(img,np.array([poly_vertices],'int32'), True, (0,0,255), 10)
    # print(poly_vertices)


def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)



