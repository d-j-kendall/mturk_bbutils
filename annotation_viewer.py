from PIL import Image
import argparse
import csv
import os
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

matplotlib.use("TkAgg")


class Viewer:
    def __init__(self, csvfile, image_dir, output_file):
        self.csvfile = csvfile
        self.dir = image_dir
        self.output_file = output_file
        self.current_count = 0
        self.fig, self.ax = plt.subplots(1)
        self.csv_data = None
        with open(self.csvfile) as csv_open:
            csv_data = csv.DictReader(csv_open)
            self.csv_data = [row for row in csv_data]

    def show_image(self, current_count):
        plt.cla()
        plt.title(current_count)
        worker_answer = json.loads(self.csv_data[current_count]["Answer.annotatedResult.boundingBoxes"])
        # Load the image from the HIT

        img = Image.open(os.path.join(self.dir, self.csv_data[current_count]["Input.image_url"].split("/")[-1]))
        im = np.array(img, dtype=np.uint8)
        # Create figure, axes, and display the image

        self.ax.imshow(im)
        self.fig.canvas.mpl_connect('key_press_event', self.key_press)
        # Draw the bounding box

        for answer in worker_answer:
            rect = patches.Rectangle((answer['left'], answer['top']), answer['width'], answer['height'],
                                     linewidth=1, edgecolor='#32cd32', facecolor='none')
        self.ax.add_patch(rect)
        # Show the bounding box
        plt.show()

    def key_press(self, event):
        n = event.key
        if n == 'right':
            if self.current_count + 1 < len(self.csv_data):
                self.current_count += 1
            else:
                self.current_count = 0

            self.show_image(self.current_count)

        elif n == 'left':
            if self.current_count <= 0:
                self.current_count = len(self.csv_data) - 1
            else:
                self.current_count -= 1
            self.show_image(self.current_count)
        elif n == 'up':
            self.csv_data[self.current_count]['Approve'] = 'X'
            self.csv_data[self.current_count]['Reject'] = ''

        elif n == 'down':
            self.csv_data[self.current_count]['Approve'] = ''
            self.csv_data[self.current_count]['Reject'] = \
                'One or more annotations are incorrect, please read instructions'


if __name__ == '__main__':

    #  Setup parser and positional argument parser
    args = argparse.ArgumentParser(prog='annotation_viewer.py',
                                   description='This program is used to view, approve and reject annotations\n'
                                               'from an MTurk Batch Results CSV')
    subparser = args.add_subparsers(title='positional arguments',
                                    description="\'view\'     "
                                                "- view, approve and reject annotations\n\n"
                                                "\n\'reject\'       "
                                                "- reject annotations and write a new csv\n",
                                    prog='annotation_viewer.py',
                                    dest='sub')

    #  View parser
    view_prog = subparser.add_parser('view')
    view_prog.add_argument('--csv-file',
                           '-i',
                           type=str,
                           default='',
                           help="enter path to mturk results csv")
    view_prog.add_argument('--dir',
                           type=str,
                           default='',
                           help="Path to the images in the CSV")
    view_prog.add_argument('--output-csv',
                           '-o',
                           type=str,
                           default='',
                           help="output csv path to write back to "
                                "defaults to open file otherwise")

    #  Reject parser
    reject_prog = subparser.add_parser('reject')
    reject_prog.add_argument('--csv-file',
                             '-i',
                             type=str,
                             default='',
                             help="enter path to mturk results "
                                  "csv from which to remove rows")
    reject_prog.add_argument('--output-csv',
                             '-o',
                             type=str,
                             default='',
                             help="removed all rows "
                                  "with non empty 'Reject' Col\n"
                                  "and write to path defined here")

    args = args.parse_args()
    print(args)

    if args.sub == 'view':
        viewer = Viewer(csvfile=args.csv_file,
                        image_dir=args.dir,
                        output_file=args.output_csv)
        viewer.show_image(0)

    elif args.sub == 'reject':
        use_new_class_here = None
        #  TODO write new reject class to remove rows and rewrite csv
