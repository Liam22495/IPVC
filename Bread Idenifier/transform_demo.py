import cv2
import numpy as np

# Load the image
img = cv2.imread("Maltese Bread.png")  # Make sure this file exists in your folder

if img is None:
    print("Image not found.")
    exit()

# Make a copy for marking points
clone = img.copy()
points = []

# Mouse callback function
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        cv2.circle(clone, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Select 4 Points", clone)

        if len(points) == 4:
            apply_perspective_transform()

def apply_perspective_transform():
    src_pts = np.float32(points)

    # Dynamically compute bounding box of selected area
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])
    width = int(max_x - min_x)
    height = int(max_y - min_y)

    # Expand size slightly to avoid tight cropping
    output_size = (width + 100, height + 100)

    # View 1: basic top-down
    dst1 = np.float32([
        [0, 0], [output_size[0], 0],
        [0, output_size[1]], [output_size[0], output_size[1]]
    ])

    # View 2: angled from left
    dst2 = np.float32([
        [100, 50],
        [output_size[0] - 10, 0],
        [120, output_size[1] - 50],
        [output_size[0], output_size[1]]
    ])

    # View 3: angled from right with skew
    dst3 = np.float32([
        [10, 0],
        [output_size[0] - 120, 80],
        [0, output_size[1] - 10],
        [output_size[0] - 100, output_size[1] - 80] 
    ])

    # Apply transforms
    M1 = cv2.getPerspectiveTransform(src_pts, dst1)
    M2 = cv2.getPerspectiveTransform(src_pts, dst2)
    M3 = cv2.getPerspectiveTransform(src_pts, dst3)

    warped1 = cv2.warpPerspective(img, M1, output_size)
    warped2 = cv2.warpPerspective(img, M2, output_size)
    warped3 = cv2.warpPerspective(img, M3, output_size)

    # Display
    cv2.imshow("Warped View 1", warped1)
    cv2.imshow("Warped View 2", warped2)
    cv2.imshow("Warped View 3", warped3)

cv2.imshow("Select 4 Points", clone)
cv2.setMouseCallback("Select 4 Points", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
