import argparse
import csv
import os
import json
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
from PIL import Image




class Viewer:

    def __init__(self,csvfile,dir):
        self.csvfile=csvfile
        self.dir=dir
        self.current_count = 0
        self.fig, self.ax = plt.subplots(1)


    def show_image(self, current_count):
        with open(self.csvfile) as csv_open:
            csv_data = csv.DictReader(csv_open)
            csv_data = [row for row in csv_data]
        worker_answer = json.loads(csv_data[current_count]["Answer.annotatedResult.boundingBoxes"])
        # Load the image from the HIT

        img = Image.open(os.path.join(self.dir, csv_data[current_count]["Input.image_url"].split("/")[-1]))
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

    def key_press(self,event):
        n = event.key
        if n=='right':
            self.current_count+=1
            self.show_image(self.current_count)


# def left_key():
#     None
#
# def right_key():
#     None
#
# def up_key():
#     None
#
# def down_key():
#     None




if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--csvfile',type=str,default='',help="enter path to mturk results csv")
    args.add_argument('--dir', type=str, default='', help="Path to the images in the CSV")
    options = args.parse_args()

    viewer = Viewer(csvfile=options.csvfile,dir=options.dir)
    viewer.show_image(0)
