import os
import json
import argparse
import cv2
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

def visualize_instance_segmentation(input_path, output_path, src_dir=None):
    """Visualize instance segmentation from LabelMe JSON format."""
    with open(input_path, 'r') as f:
        labelme_data = json.load(f)

    # Load the original image if src_dir is provided
    image_path = os.path.join(src_dir, labelme_data.get("imagePath", "")) if src_dir else None
    if image_path and os.path.exists(image_path):
        canvas = cv2.imread(image_path)
        overlay = np.zeros_like(canvas, dtype=np.uint8)
    else:
        # Create a blank canvas if no valid src image is found
        image_height = labelme_data["imageHeight"]
        image_width = labelme_data["imageWidth"]
        canvas = np.zeros((image_height, image_width, 3), dtype=np.uint8)
        overlay = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    # Group instances by group_id
    instances = {}
    for shape in labelme_data["shapes"]:
        group_id = shape.get("group_id", None)
        if group_id is not None:
            if group_id not in instances:
                instances[group_id] = []
            instances[group_id].append(shape)
        else:
            instances[len(instances)] = [shape]

    # Draw each grouped instance with random colors
    for instance_shapes in instances.values():
        color = np.random.randint(0, 255, 3).tolist()  # Random color
        for shape in instance_shapes:
            points = np.array(shape["points"], dtype=np.int32)
            cv2.fillPoly(overlay, [points], color)
            cv2.polylines(canvas, [points], isClosed=True, color=(255, 255, 255), thickness=2)  # White contour

            # Draw label name
            label = shape.get("label", "Unknown")
            centroid = np.mean(points, axis=0).astype(int)
            cv2.putText(canvas, label, tuple(centroid), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Blend the overlay with the canvas if src image is found
    canvas = cv2.addWeighted(canvas, 0.7, overlay, 0.3, 0)

    # Save the visualization as an image
    cv2.imwrite(output_path, canvas)

def process_single_file(args):
    """Process a single JSON file for visualization."""
    input_path, output_path, src_dir = args
    visualize_instance_segmentation(input_path, output_path, src_dir)

def process_json_files(input_dir, output_dir, src_dir, num_workers=None):
    """Process all JSON files in a directory in parallel for visualization."""
    os.makedirs(output_dir, exist_ok=True)
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    task_args = [
        (os.path.join(input_dir, json_file), os.path.join(output_dir, json_file.replace('.json', '.png')), src_dir)
        for json_file in json_files
    ]

    # Use all available CPU cores unless specified
    num_workers = num_workers or cpu_count()

    with Pool(num_workers) as pool:
        list(tqdm(pool.imap_unordered(process_single_file, task_args), total=len(task_args), desc="Visualizing JSON files"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Comlops JSON to RGB segmentation masks in parallel.")
    parser.add_argument("input_dir", type=str, help="Directory containing Comlops JSON files")
    parser.add_argument("output_dir", type=str, help="Directory to save the output segmentation masks")
    parser.add_argument("--src", type=str, default=None, help="Directory containing original images for blending (optional)")
    parser.add_argument("--workers", type=int, default=None, help="Number of parallel workers (default: all available cores)")

    args = parser.parse_args()
    process_json_files(args.input_dir, args.output_dir, args.src, args.workers)
