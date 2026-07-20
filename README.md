# mturk_bbutils

Command-line utilities for running bounding-box image-annotation projects on Amazon Mechanical Turk — generating the input CSV of image URLs, and reviewing the annotations workers submit.

_Status: utility scripts (2019) · Python 3_

## What's here

- **`mturkvariables.py`** — builds the MTurk input CSV. Takes a directory of images and an S3 URL
  prefix and writes one row per image for a bounding-box annotation project.

  ```bash
  python3 mturkvariables.py -i images_dir -url s3_bucket_folder_url -o output.csv
  ```

- **`mturk_annotation_viewer.py`** — reviews the `batch_results.csv` MTurk returns. Step through
  each worker's HIT and approve it (you pay) or reject it with a reason (you don't), writing the
  decisions back to the CSV.

## Requirements

Python 3; the annotation viewer uses OpenCV (`cv2`) to display images.

## Notes

Built out of necessity for a real annotation project — a working script collection, not a packaged
tool. A couple of the scripts are experimental and unfinished.

---
Built by **Dustin Kendall** — production readiness & rescue for AI-built apps.
[dustinkendall.com](https://dustinkendall.com) · [LinkedIn](https://www.linkedin.com/in/dustinjkendall)
