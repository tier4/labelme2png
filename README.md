# LabelMe Instance Segmentation Visualizer

This tool visualizes instance segmentation masks from LabelMe JSON format. It supports overlaying the segmentation masks on original images and grouping instances by their `group_id`. The tool also supports parallel processing for improved performance.

## Features
- Visualizes LabelMe instance segmentation masks with color-coded instances.
- Supports blending segmentation masks with original images if specified.
- Groups instances by `group_id` and outlines their contours in **white**.
- Displays instance labels within each segmented area.
- Utilizes multiprocessing for faster processing of large datasets.

## Requirements
- Python 3.6 or higher
- Required Libraries:
  - `numpy`
  - `opencv-python`
  - `tqdm`

You can install dependencies using the following command:

```bash
pip install numpy opencv-python tqdm
```

## Usage
### Command Syntax
```bash
python visualize_labelme.py <input_dir> <output_dir> [--src <src_dir>] [--workers <num_workers>]
```

### Arguments
- **`input_dir`** (required): Directory containing LabelMe JSON files.
- **`output_dir`** (required): Directory where the generated segmentation mask images will be saved.
- **`--src`** (optional): Directory containing original images for blending with segmentation masks.
- **`--workers`** (optional): Number of parallel workers to use (default is the number of available CPU cores).

### Example Commands
**Visualize segmentation masks only**
```bash
python visualize_labelme.py input_dir output_dir
```

**Visualize segmentation masks overlaid on original images**
```bash
python visualize_labelme.py input_dir output_dir --src path/to/images --workers 4
```

## Output
- The generated segmentation masks are saved in `.png` format with the same filename as the original `.json` file.
- Each instance is displayed in a unique color, grouped by `group_id`.
- Segmentation contours are displayed in **white**.
- Labels are displayed at the center of each segmented area.

## Example Output
- Example Input JSON:
```json
{
    "shapes": [
        {
            "label": "marking_arrow",
            "points": [
                [1471, 991], [1474, 991], [1474, 993], [1475, 993],
                [1475, 996], [1473, 996], [1473, 995], [1471, 995]
            ],
            "group_id": 54,
            "shape_type": "polygon",
            "flags": {}
        }
    ],
    "imagePath": "example_image.jpg",
    "imageHeight": 1080,
    "imageWidth": 1920
}
```

## Notes
- Ensure that `imagePath` in your JSON files corresponds correctly to the image files in your `--src` directory.
- For optimal performance, set `--workers` based on the number of available CPU cores.

## License
This project is licensed under the MIT License.

## Contact
If you have any questions or suggestions, please feel free to reach out!


