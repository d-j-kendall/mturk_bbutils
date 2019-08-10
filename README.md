# MTurk Bounding Box Utils
Utilities for formatting csvs, viewing bounding box annotations, and approving annotations with mturk

Welcome to the MTurk Bounding Box Utils wiki!

This project was inspired out of necessity because I lacked the tools to successfully annotate images using MTurk. 

### MTurkVariables
mturkvariables.py's intention is to take all the files in a given directory and concatenate them to a **URL** prefix. This is then put in a CSV to upload to MTurk for a bounding box annotation project. 

*Height and Width parameters are deprecated and included in the csv returned from amazon*

#### Usage

`python3 mturkvariables.py -i director_with_images -url s3_bucket_folder_url -o output.csv`

[How to create a project on mturk]()


### MTurk Annotation Viewer

mturk_annotation_viewer.py's purpose is to view the 'not so user friendly' MTurk `batch_results.csv` file. 

You can approve and reject a workers HIT(Human intelligence Task) by:
1. Putting an 'X' in the approved cell which approves a workers work (You pay!)
2. Or putting a "Reason for rejection" in the unapproved cell which rejects a worker's work (You don't pay)

So the idea is to automate the viewing of the label annotations by reading the csv MTurk provides, then allow the user to hit a key and write back to the `approve` and `reject` cells with generic messages. 

Tkinter should be used in future phases. 

