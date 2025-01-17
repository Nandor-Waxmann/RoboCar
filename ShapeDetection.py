import time
import cv2
from collections import Counter
import socket
import numpy as np

host = "192.168.1.144"
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket made")
#s.connect((host, port))
print("Socket connected!!!")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

shape_dict = {
    (3, (60, 60, 60)): 'Equilateral Triangle',
    (3, (90, 130, 130)): 'Right Triangle',
    (4, (90, 90, 90, 90)): 'Rectangle',
    (4, (120, 120, 65, 65)): 'Trapezoid',
    (5, (108, 108, 108, 108, 108)): 'Regular Pentagon',
    (6, (120, 120, 120, 120, 120, 120)): 'Regular Hexagon',
    (7, (129, 129, 129, 129, 129, 129, 129)): 'Regular Heptagon',
    (8, (135, 135, 135, 135, 135, 135, 135, 135)): 'Regular Octagon',
    (12, (90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90)): 'Plus'
}

interval = 3
camera_delay = 0
similarity_threshold = 0.9
min_contour_area = 400
angle_tolerance = 15
epsilon_parameter = 0.012
wait_time = 5
new_shape_name = "Shape"
num_recording_intervals = 3
last_time = time.time()

frame_shapes = []
frame_count = 0


def calculate_angles(points):
    angles = []
    num_points = len(points)
    for i in range(num_points):
        # Get the current, previous, and next points
        p1 = points[i][0]
        p2 = points[(i + 1) % num_points][0]
        p0 = points[i - 1][0]

        v1 = p1 - p0
        v2 = p2 - p1

        # Normalize vectors
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)

        # Calculate the angle between vectors in degrees
        angle = np.degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)))
        angles.append(round(angle, 1))
    return tuple(angles)


def match_shape(num_vertices, angles, shape_dict, angle_tolerance):
    sorted_angles = tuple(sorted(angles))
    for (vertices, ref_angles), shape_name in shape_dict.items():
        if vertices == num_vertices:
            # Normalize reference and detected angles to have the same sum
            ref_sum = sum(ref_angles)
            detected_sum = sum(sorted_angles)
            normalized_ref_angles = [angle * (detected_sum / ref_sum) for angle in ref_angles]
            normalized_ref_angles = tuple(sorted(normalized_ref_angles))

            # Check if all angles match within the tolerance
            if len(normalized_ref_angles) == len(sorted_angles) and all(abs(a - b) <= angle_tolerance for a, b in zip(normalized_ref_angles, sorted_angles)):
                return shape_name
    return "Unknown Shape"


record_new_shape = False
recording_angles = []
recording_vertices = 0
recorded_shape_count = 0


while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame. Exiting ...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    _, threshold = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(threshold, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    frame_shapes_current = []
    frame_shapes_current_temp = []

    if len(contours) < 300:
        for contour in contours:
            if cv2.contourArea(contour) < min_contour_area:
                continue

            approx = cv2.approxPolyDP(contour, 0.012 * cv2.arcLength(contour, True), True)
            num_vertices = len(approx)
            angles = calculate_angles(approx)

            # Match the shape
            shape_name = match_shape(num_vertices, angles, shape_dict, angle_tolerance)
            frame_shapes_current.append((shape_name, num_vertices, angles))
            frame_shapes_current_temp.append(shape_name)

            # Draw and label the shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                cv2.putText(frame, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 255), 2)
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)

    frame_shapes.append(frame_shapes_current_temp)
    frame_count += 1

    current_time = time.time()

    if record_new_shape:
        for shape in frame_shapes_current:
            shape_name, vertices, angles = shape
            if shape_name == "Unknown Shape":
                recording_angles.append(angles)
                recording_vertices = vertices

        if current_time - last_time >= interval:
            last_time = current_time
            num_recording_intervals -= 1
            print(f"Recording interval remaining: {num_recording_intervals}")

            if num_recording_intervals <= 0:
                record_new_shape = False

                if recording_angles:
                    # Flatten angles and compute averages for each position
                    max_length = max(len(angles) for angles in recording_angles)
                    padded_angles = [np.pad(angles, (0, max_length - len(angles)), constant_values=np.nan) for angles in recording_angles]
                    averaged_angles = np.nanmean(padded_angles, axis=0).tolist()
                    averaged_angles = [round(angle, 1) for angle in averaged_angles if not np.isnan(angle)]
                    averaged_angles.sort()

                    # Add the new shape to the dictionary
                    recorded_shape_count += 1
                    new_shape_name = f"Shape {recorded_shape_count}"
                    shape_dict[(recording_vertices, tuple(averaged_angles))] = new_shape_name
                    print(f"New shape recorded as '{new_shape_name}' with vertices {recording_vertices} and angles {averaged_angles}")

                recording_angles.clear()
                recording_vertices = 0
                num_recording_intervals = 3
    elif current_time - last_time >= interval:
        all_shapes = [shape for frame in frame_shapes for shape in frame]

        # Count the occurrences of each shape
        shape_counts = Counter(all_shapes)
        threshold = similarity_threshold * frame_count
        consistent_shapes = [shape for shape, count in shape_counts.items() if count >= threshold]

        consistent_shapes.sort()

        if consistent_shapes:
            print(f"Detected Shapes in the last {interval} seconds: " + ", ".join(consistent_shapes))
        else:
            print(f"No significant shapes detected in the last {interval} seconds.")

        frame_shapes = []
        frame_count = 0
        last_time = current_time

        # Trigger new shape recording if a known shape is detected
        if len(consistent_shapes) == 1 and consistent_shapes[0] == "Rectangle" and not record_new_shape:
            print(f"Detected known shape: {consistent_shapes}")
            record_new_shape = True
            recording_angles.clear()
            recording_vertices = 0
            print(f"Prepare the new shape. Recording will start in {wait_time} seconds...")
            time.sleep(wait_time)

        # s.send(" ".join(consistent_shapes).encode())

    cv2.imshow('shapes', frame)

    time.sleep(camera_delay)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
