import boto
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import HTMLQuestion
from boto.mturk.layoutparam import LayoutParameter
from boto.mturk.layoutparam import LayoutParameters
import argparse
import csv
import msvcrt

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import requests
from io import BytesIO
from PIL import Image

def display_images(access_key='',
                   secret_key='',
                   csv_file = ''):
    # Create your connection to MTurk
    mtc = MTurkConnection(aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    host='mechanicalturk.amazonaws.com')
    # This is the value you received when you created the HIT
    # You can also retrieve HIT IDs by calling GetReviewableHITs
    # and SearchHITs. See the links to read more about these APIs.
    with open()
        csv_data = csv.DictReader
    hit_id = "386T3MLZLNVRU564VQVZSIKA8D580B"
    result = mtc.get_assignments(hit_id)
    assignment = result[0]
    worker_id = assignment.WorkerId
    for answer in assignment.answers[0]:
      if answer.qid == 'annotation_data':
        worker_answer = json.loads(answer.fields[0])
    # Load the image from the HIT
    response = requests.get('http://turk.s3.amazonaws.com/stop_sign_picture.jpg')
    img = Image.open(BytesIO(response.content))
    im = np.array(img, dtype=np.uint8)
    # Create figure, axes, and display the image
    fig,ax = plt.subplots(1)
    ax.imshow(im)
    # Draw the bounding box
    for answer in worker_answer:
        rect = patches.Rectangle((answer['left'],answer['top']),answer['width'],answer['height'],linewidth=1,edgecolor='#32cd32',facecolor='none')
        ax.add_patch(rect)
    # Show the bounding box
    plt.show()


if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--csv',type=str,default='',help="enter path to mturk results csv")
    args.add_argument('--keycsv',type=str,default='rootkey.csv',help="Enter path to your key csv downloaded from amazon")
    options = args.parse_args()
    access_key = ''
    secret_key = ''
    with open(options.keycsv) as keyfile:
        file_reader = csv.reader(keyfile)
        keys = [row for row in file_reader]

    keys[0] = keys[0].split('=')[1]
    keys[1] = keys[1].split('=')[1]





    display_images(keys[0],keys[1], options.csv)