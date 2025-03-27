import cv2
import numpy as np

# Create a blank image
img = np.zeros((200, 400, 3), dtype=np.uint8)

# Display setup confirmation message
cv2.putText(img, "Project Ready", (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 255, 255), 2)

# Show the image
cv2.imshow("Bread Identifier Setup", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
