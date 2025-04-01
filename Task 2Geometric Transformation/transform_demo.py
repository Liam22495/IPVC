import cv2
import numpy as np

# Load and resize image if needed
img = cv2.imread("Maltese Bread.png")
if img is None:
    print("Image not found.")
    exit()

max_dim = 1000
scale = 1.0
if max(img.shape[:2]) > max_dim:
    scale = max_dim / max(img.shape[0], img.shape[1])
    img = cv2.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)))

clone = img.copy()
points = []

corner_labels = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"]

def click_event(event, x, y, flags, param):
    global points, clone
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            label = corner_labels[len(points)]
            points.append((x, y))
            cv2.circle(clone, (x, y), 6, (0, 255, 0), -1)
            cv2.putText(clone, label, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.imshow(window_name, clone)

        if len(points) == 4:
            if validate_corner_order(points):
                apply_perspective_transform()
            else:
                print("❌ Invalid point order. Please follow: Top-Left → Top-Right → Bottom-Left → Bottom-Right")
                cv2.putText(clone, "Invalid point order! Press 'r' to reset.", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                cv2.imshow(window_name, clone)

def validate_corner_order(pts):
    # Simple logic: TL should be top-left-most, TR top-right, etc.
    tl, tr, bl, br = pts
    return tl[0] < tr[0] and tl[1] < bl[1] and br[0] > bl[0] and br[1] > tr[1]

def apply_perspective_transform():
    src_pts = np.float32(points)

    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    width = int(max_x - min_x)
    height = int(max_y - min_y)
    output_size = (width + 100, height + 100)

    dst_views = {
        "Top Down": np.float32([
            [0, 0],
            [output_size[0], 0],
            [0, output_size[1]],
            [output_size[0], output_size[1]]
        ]),
        "Angled Left": np.float32([
            [100, 50],
            [output_size[0] - 10, 0],
            [120, output_size[1] - 50],
            [output_size[0], output_size[1]]
        ]),
        "Skewed Right": np.float32([
            [10, 0],
            [output_size[0] - 120, 80],
            [0, output_size[1] - 10],
            [output_size[0] - 100, output_size[1] - 80]
        ])
    }

    for label, dst in dst_views.items():
        matrix = cv2.getPerspectiveTransform(src_pts, dst)
        warped = cv2.warpPerspective(img, matrix, output_size)
        cv2.imshow(f"Warped View - {label}", warped)

def reset_points():
    global points, clone
    points = []
    clone = img.copy()
    show_instructions()

def show_instructions():
    cv2.imshow(window_name, clone)
    print("\n🟢 Please click the 4 corners of the object in order:")
    for i, label in enumerate(corner_labels, 1):
        print(f"  {i}. {label}")

# Setup
window_name = "Select 4 Points in Order (Top left, Top right, Botom left, Bottom right)"
show_instructions()
cv2.imshow(window_name, clone)
cv2.setMouseCallback(window_name, click_event)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        reset_points()
    elif key == 27:  # ESC
        break

cv2.destroyAllWindows()
