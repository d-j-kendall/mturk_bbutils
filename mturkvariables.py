import os
import csv
import cv2
import argparse

def generate_csv(
        o_file='mturkvars.csv',
        i_directory=None,
        height=False,
        width=False,
        url=''
):
    varlist = ['image_url']
    if width:
        varlist.append('image_width')
    if height:
        varlist.append('image_height')

    o_file = open(o_file,'w',newline='')
    mywriter = csv.writer(o_file, delimiter=',')
    mywriter.writerow(varlist)
    for file in os.listdir(i_directory):
        image = cv2.imread(os.path.join(i_directory,file))
        if image is not None:
            img_height, img_width, img_channels = image.shape
        vallist = [url+file]
        if width:
            vallist.append(img_width)
        if height:
            vallist.append(img_height)
        mywriter.writerow(vallist)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output', type=str, default='mturkvars.csv', help='output filename of generated csv file')
    parser.add_argument('-i','--input', type=str, default=None,help='input directory for which the program will iterate through')
    parser.add_argument('--height',action='store_true', help='output column with height of images')
    parser.add_argument('--width',action='store_true', help='output column with width of images')
    parser.add_argument('-url',type=str, default='', help='url prefix to append to each file name.')

    opt = parser.parse_args()
    generate_csv(
        o_file=opt.output,
        i_directory=opt.input,
        height=opt.height,
        width=opt.width,
        url=opt.url
    )



