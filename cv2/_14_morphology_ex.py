import cv2
import numpy as np
def show_wait_destroy(winname, img):
    cv2.imshow(winname, img)
    cv2.moveWindow(winname, 500, 0)
    cv2.waitKey(0)
    cv2.destroyWindow(winname)
def main():
    src = cv2.imread('images/music.png', cv2.IMREAD_COLOR)
    cv2.imshow("src", src)
    if len(src.shape) != 2:
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    else:
        gray = src

    show_wait_destroy("gray", gray)
    gray = cv2.bitwise_not(gray)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 15, -2)

    show_wait_destroy("binary", bw)
    horizontal = np.copy(bw)
    vertical = np.copy(bw)
    cols = horizontal.shape[1]
    horizontal_size = cols // 30
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    # Show extracted horizontal lines
    show_wait_destroy("horizontal", horizontal)

    rows = vertical.shape[0]
    verticalsize = rows // 30
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)
    # Show extracted vertical lines
    show_wait_destroy("vertical", vertical)
    vertical = cv2.bitwise_not(vertical)
    show_wait_destroy("vertical_bit", vertical)
    edges = cv2.adaptiveThreshold(vertical, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 3, -2)
    show_wait_destroy("edges", edges)
    # Step 2
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel)
    show_wait_destroy("dilate", edges)
    # Step 3
    smooth = np.copy(vertical)
    # Step 4
    smooth = cv2.blur(smooth, (2, 2))
    # Step 5
    (rows, cols) = np.where(edges != 0)
    vertical[rows, cols] = smooth[rows, cols]
    # Show final result
    show_wait_destroy("smooth - final", vertical)
    # [smooth]
    return 0
if __name__ == "__main__":
    main()