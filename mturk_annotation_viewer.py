# import boto
# from boto.mturk.question import HTMLQuestion
# from boto.mturk.layoutparam import LayoutParameter
# from boto.mturk.layoutparam import LayoutParameters
import argparse
import csv
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show, ion
import matplotlib.patches as patches
# import requests
from io import BytesIO
from PIL import Image
import msvcrt as m


def display_images(access_key='', secret_key='', csv_file='', directory=''):

    # get chars from STDIN on command line
    def wait():
        return m.getch()

    # Create your connection to MTurk

    # mtc = MTurkConnection(aws_access_key_id=access_key,
    # aws_secret_access_key=secret_key,
    # host='mechanicalturk.amazonaws.com')

    # This is the value you received when you created the HIT
    # You can also retrieve HIT IDs by calling GetReviewableHITs
    # and SearchHITs. See the links to read more about these APIs.
    with open(csv_file) as csv_open:

        csv_data = csv.DictReader(csv_open)
        csv_data = [row for row in csv_data]

    # Yes, this can be infinitely neater. But it will do for now.
    str_W = 'W'
    str_w = 'w'
    str_S = 'S'
    str_s = 's'
    str_A = 'A'
    str_a = 'a'
    str_D = 'D'
    str_d = 'd'
    str_E = 'E'
    str_e = 'e'

    # Convert strings to byte literals, since that is what getch returns from STDIN.
    byte_W = str_W.encode()
    byte_S = str_S.encode()
    byte_w = str_w.encode()
    byte_s = str_s.encode()
    byte_E = str_E.encode()
    byte_e = str_e.encode()
    byte_A = str_A.encode()
    byte_a = str_a.encode()
    byte_D = str_D.encode()
    byte_d = str_d.encode()

    # initialize counter to 0
    i = 0

    while i < csv_data.__len__():

        # print out what iteration we are currently on, and the current img url
        print('At i = %i \n' % i)
        print('Img url is: %s \n' % os.path.join(directory, csv_data[i]["Input.image_url"].split("/")[-1]))

        # Load the image from the HIT
        worker_answer = json.loads(csv_data[i]["Answer.annotatedResult.boundingBoxes"])

        img = Image.open(os.path.join(directory, csv_data[i]["Input.image_url"].split("/")[-1]))
        im = np.array(img, dtype=np.uint8)

        # Create figure, axes, and display the image
        fig, ax = plt.subplots(1)
        ax.imshow(im)

        # Draw the bounding box
        for answer in worker_answer:
            rect = patches.Rectangle((answer['left'], answer['top']), answer['width'], answer['height'], linewidth=1,
                                     edgecolor='#32cd32', facecolor='none')
            ax.add_patch(rect)

        # Show the bounding box
        # Draw and pause needed to avoid matplotlibs shitty innate blocking feature
        plt.draw()
        plt.pause(0.001)

        # Give the user the option of approving or rejecting the image
        print("\nApprove or Reject: \n"
              "W: approve \n"
              "S: reject \n"
              "E: EXIT \n")

        if wait() == byte_W or byte_w:
            print('You approved this image')
            csv_data[i]["Approve"] = 'x'
            csv_data[i]["Reject"] = ''
        elif wait() == byte_S or byte_s:
            print('You have rejected this image')
            csv_data[i]["Approve"] = ''
            csv_data[i]["Reject"] = 'Inaccurate annotation, please read instructions'
        # if user enters 'E' to exit, break out of while loop and end program
        elif wait() == byte_E or byte_e:
            i = 99999
            return i

        # Give the user the option of advancing to the next image or going back to the previous image
        print("\nPrevious Image or Next Image: \n"
              "A: Previous image \n"
              "D: Next image \n"
              "E: EXIT \n")

        if wait() == byte_D or byte_d:
            print('Next Image.')
            i += 1
            plt.close(fig)
        elif wait() == byte_A or byte_a:
            print('Previous Image.')
            if i != 0:
                i -= 1
                plt.close(fig)
        # if user enters 'E' to exit, break out of while loop and end program but not currently working
        elif wait() == byte_E or byte_e:
            i = 99999
            return i

    # Tricky, but needed to avoid the blocking features of matplotlib
    plt.ion()
    plt.show()


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--csv', type=str, default='', help="enter path to mturk results csv")
    args.add_argument('--keycsv', type=str, default='rootkey.csv',
                      help="Enter path to your key csv downloaded from amazon")
    args.add_argument('--dir', type=str, default='', help="Path to the images in the CSV")
    options = args.parse_args()
    access_key = ''
    secret_key = ''
    keys = ['', '']
    if os.path.exists(options.keycsv):
        with open(options.keycsv) as keyfile:
            file_reader = csv.reader(keyfile)
            keys = [row[0].split('=')[1] for row in file_reader]

        keys[0] = keys[0]  # .split('=')[1]
        keys[1] = keys[1]  # .split('=')[1]

    display_images(keys[0], keys[1], options.csv, options.dir)
