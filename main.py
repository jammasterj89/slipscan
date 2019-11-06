#!/usr/bin/env python3

import os
import sys
import subprocess
import re
import json
import datetime
import inspect
import cv2
from fractions import Fraction

def main():

    global filename
    filename = "out.txt"
    # welcome message, decide whether to start a new scan or rescan
    print("Slipscan v0.1 ")
    option = input('Enter function option: 1 to scan or 2 to rescan: ')

    if option == '':
        print('Enter what function you wish to perform e.g. to perform new scan enter: 1')
        exit()

    if option == "1":
        source = input('Enter source option: 1 for scanned image or 2 for phone image: ')

        if source == '':
            print('Enter what source your image is, either from a scanner or a phone e.g. for a scanned image enter: 1')
            exit()

        image = input('Enter input image location: ')

        if image == '':
            print('Enter image location e.g. image.png')
            exit()

        # check that tesseract is installed
        try:
            result = subprocess.run(['tesseract'], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        except:
            print('Tesseract is not installed, please install tesseract via "sudo apt install tesseract-ocr"')
            exit()

        if source == "1":
            print("Ensure scanned image is cropped and scanned as greyscale with DPI of 400. ")
            dpi = "400"

            # optional thresh of image to give solid white and black background
            thresh = input('Do you want to thresh the image? Enter y or n: ')

            if thresh == "y":
                img = cv2.imread(image)
                grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                th, threshed = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY)
                cv2.imwrite(image, threshed)

        elif source == "2":
            print("Ensure phone image is cropped and converted to greyscale using https://pinetools.com/grayscale-image. ")
            print("Then threshed using https://pinetools.com/threshold-image ~ 150. ")
            dpi = "300"

        # check image is valid
        if os.path.isfile(image) and option == "1":
            # run tesseract ocr conversion on user provided image
            result = subprocess.run(['tesseract', image, 'out','--dpi', dpi, '-c', 'preserve_interword_spaces=1'],
                                    stdout=subprocess.PIPE)
            result.stdout

            formatting()

            conversion()

        else:
            print('Please ensure image exists at path provided: ', image)
            exit()

    # convert without rescanning image
    elif option == "2":
        conversion()

    # help message if nothing entered
    else:
        print("Slipscan v0.1 ")
        print("Example usage to start a scan from the start: ")
        print("$ ./slipscan.py")
        print("$ 1")
        print("$ image.png")
        print("Example usage to rescan an image after manual correction: ")
        print("$ ./slipscan.py")
        print("$ 2")

def formatting():

    # remove empty lines
    original = open(filename).read()
    whitespace = re.sub(r'^\n', '', original, flags=re.MULTILINE)
    open(filename, 'w').write(whitespace)

    # remove double spaces
    original = open(filename).read()
    spaces = re.sub('\s\s+' , ' ', original)
    open(filename, 'w').write(spaces)

    # replace 25 with 2/5
    original = open(filename).read()
    frac = re.sub('25', '2/5', original)
    open(filename, 'w').write(frac)

    # replace 46 with 4/6
    original = open(filename).read()
    frac = re.sub('46', '4/6', original)
    open(filename, 'w').write(frac)

    # replace 52 with 5/2
    original = open(filename).read()
    frac = re.sub('52', '5/2', original)
    open(filename, 'w').write(frac)

    # replace 56 with 5/6
    original = open(filename).read()
    frac = re.sub('56', '5/6', original)
    open(filename, 'w').write(frac)

    # replace 64 with 6/4
    original = open(filename).read()
    frac = re.sub('64', '6/4', original)
    open(filename, 'w').write(frac)

    # replace 94 with 9/4
    original = open(filename).read()
    frac = re.sub('94', '9/4', original)
    open(filename, 'w').write(frac)

    # replace 125 with 12/5
    original = open(filename).read()
    frac = re.sub('125', '12/5', original)
    open(filename, 'w').write(frac)

    # remove special chars except / & -
    original = open(filename).read()
    special = re.sub('[^a-zA-Z0-9-/\n\s\.]', '', original)
    open(filename, 'w').write(special)

    # replace - with /
    original = open(filename).read()
    slash = re.sub('-', '/', original)
    open(filename, 'w').write(slash)

    # replace EVS with 2.0
    original = open(filename).read()
    evs = re.sub('EVS', '2.00', original, flags=re.IGNORECASE)
    open(filename, 'w').write(evs)

def conversion():

    original = open(filename).read()

    # convert fractional to decimal oddds
    def format_fraction(a, b):
        odd = '{:.3g}'.format(float(a) / float(b) + 1)
        if '.' not in odd:
            return odd + '.0'
        return odd

    try:
        odd = re.sub(r'\b(\d+)/(\d+)\b', lambda g: format_fraction(g.group(1), g.group(2)), original)

    except:
        print("Error converting:", odd)

    open(filename, 'w').write(odd)

    # for all matches less than 1.9 write into ap.txt
    original = open(filename, 'r')
    final = open('ap.txt', 'w')

    for line in original:
        odds = re.findall(r'\d+\.\d+', line)
        try:
            if (odds[0] is not None and float(odds[0]) < 1.9) or (odds[1] is not None and float(odds[1]) < 1.9) or (odds[2] is not None and float(odds[2]) < 1.9):
                final.write(line)

        except:
            print("Error on line:", line, "recommend to manually fix out.txt then rescan ")

    # put in some kind of if if runs through without error
    print('Please find converted odds in out.txt and all odds < 2.0 in ap.txt')
    exit()

if __name__ == '__main__':
    main()
