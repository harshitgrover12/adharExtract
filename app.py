# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
import io
import json
import ftfy
import numpy as np
# creating a Flask app
app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.

@app.route('/', methods = ['GET'])
def home1():
    if(request.method == 'GET'):
        return jsonify({'data':'success'})

@app.route('/getAdhar', methods = ['GET', 'POST'])
def home():
    if(request.method == 'POST'):
        # read image file string data
        name1 = request.form['name']
        dob = request.form['dob']
        image1= request.files['image']
        npimg = np.fromfile(image1, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # from nostril import nonsense

    ################################################################################################################
    ############################# Section 1: Initiate the command line interface ###################################
    ################################################################################################################

    # construct the argument parse and parse the arguments
    #     ap = argparse.ArgumentParser()
    #     ap.add_argument("-i", "--image", required=True,
    #                     help="path to input image to be OCR'd")
    #     ap.add_argument("-p", "--preprocess", type=str, default="thresh",
    #                     help="type of preprocessing to be done, choose from blur, linear, cubic or bilateral")
    #     args = vars(ap.parse_args())
    #
    #     '''
    #         Our command line arguments are parsed. We have two command line arguments:
    #         --image : The path to the image we’re sending through the OCR system.
    #         --preprocess : The preprocessing method. This switch is optional and for this tutorial and can accept the following
    #                         parameters to be passed (refer sections to know more:
    #                         - blur
    #                         - adaptive
    #                         - linear
    #                         - cubic
    #                         - gauss
    #                         - bilateral
    #                         - thresh (meadian threshold - default)
    #
    #         ---------------------------  Use Blur when the image has noise/grain/incident light etc. --------------------------
    #         '''
    #
    #     ##############################################################################################################
    #     ###################### Section 2: Load the image -- Preprocess it -- Write it to disk ########################
    #     ##############################################################################################################
    #
    #     # load the example image and convert it to grayscale

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #
    #     # check to see if we should apply thresholding to preprocess the
    #     # image
    #     if args["preprocess"] == "thresh":
    #         gray = cv2.threshold(gray, 0, 255,
    #                              cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #
    #     elif args["preprocess"] == "adaptive":
    #         gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    #     '''
    #         What we would like to do is to add some additional preprocessing steps as in most cases, you may need to scale your
    #         image to a larger size to recognize small characters.
    #         In this case, INTER_CUBIC generally performs better than other alternatives, though it’s also slower than others.
    #         If you’d like to trade off some of your image quality for faster performance,
    #         you may want to try INTER_LINEAR for enlarging images.
    #         '''
    #     if args["preprocess"] == "linear":
    #         gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    #
    #     elif args["preprocess"] == "cubic":
    #         gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    #
    #     # make a check to see if blurring should be done to remove noise, first is default median blurring
    #
    #     '''
    #         1. Gaussian Blurring works in a similar fashion to Averaging, but it uses Gaussian kernel,
    #         instead of a normalized box filter, for convolution. Here, the dimensions of the kernel and standard deviations
    #         in both directions can be determined independently.
    #         Gaussian blurring is very useful for removing — guess what? — 
    #         gaussian noise from the image. On the contrary, gaussian blurring does not preserve the edges in the input.
    #         2. In Median Blurring the central element in the kernel area is replaced with the median of all the pixels under the
    #         kernel. Particularly, this outperforms other blurring methods in removing salt-and-pepper noise in the images.
    #         Median blurring is a non-linear filter. Unlike linear filters, median blurring replaces the pixel values
    #         with the median value available in the neighborhood values. So, median blurring preserves edges
    #         as the median value must be the value of one of neighboring pixels
    #         3. Speaking of keeping edges sharp, bilateral filtering is quite useful for removing the noise without
    #         smoothing the edges. Similar to gaussian blurring, bilateral filtering also uses a gaussian filter
    #         to find the gaussian weighted average in the neighborhood. However, it also takes pixel difference into
    #         account while blurring the nearby pixels.
    #         Thus, it ensures only those pixels with similar intensity to the central pixel are blurred,
    #         whereas the pixels with distinct pixel values are not blurred. In doing so, the edges that have larger
    #         intensity variation, so-called edges, are preserved.
    #         '''
    #
    #     if args["preprocess"] == "blur":
    #         gray = cv2.medianBlur(gray, 3)
    #
    #     elif args["preprocess"] == "bilateral":
    #         gray = cv2.bilateralFilter(gray, 9, 75, 75)
    #
    #     elif args["preprocess"] == "gauss":
    #         gray = cv2.GaussianBlur(gray, (5, 5), 0)
    #
        # write the grayscale image to disk as a temporary file so we can
        # apply OCR to it
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)

        '''
            A blurring method may be applied. We apply a median blur when the --preprocess flag is set to blur. 
            Applying a median blur can help reduce salt and pepper noise, again making it easier for Tesseract 
            to correctly OCR the image.
            After pre-processing the image, we use  os.getpid to derive a temporary image filename based on the process ID 
            of our Python script.
            The final step before using pytesseract for OCR is to write the pre-processed image, gray, 
            to disk saving it with the filename  from above
            '''

        ##############################################################################################################
        ######################################## Section 3: Running PyTesseract ######################################
        ##############################################################################################################


        # load the image as a PIL/Pillow image, apply OCR, and then delete
        # the temporary file
        pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
        text = pytesseract.image_to_string(Image.open(filename))
        # add +hin after eng within the same argument to extract hindi specific text - change encoding to utf-8 while writing
        # print(text)

        # show the output images
        cv2.imshow("Image", image)
        cv2.imshow("Output", gray)
        # cv2.waitKey(0)

        # writing extracted data into a text file
        text_output = open('outputbase.txt', 'w', encoding='utf-8')
        text_output.write(text)
        text_output.close()

        file = open('outputbase.txt', 'r', encoding='utf-8')
        text = file.read()
        # print(text)

        # Cleaning all the gibberish text
        text = ftfy.fix_text(text)
        text = ftfy.fix_encoding(text)
        '''for god_damn in text:
                if nonsense(god_damn):
                    text.remove(god_damn)
                else:
                    print(text)'''
        # print(text)

        ############################################################################################################
        ###################################### Section 4: Extract relevant information #############################
        ############################################################################################################

        # Initializing data variable
        name = None
        yob = None
        gender = None
        adhar = None
        nameline = []
        dobline = []
        panline = []
        text0 = []
        text1 = []
        text2 = []

        # Searching for PAN
        lines = text.split('\n')
        for lin in lines:
            s = lin.strip()
            s = lin.replace('\n', '')
            s = s.rstrip()
            s = s.lstrip()
            text1.append(s)

        text1 = list(filter(None, text1))
        # print(text1)

        '''
            Note: Hindi has the worst error rates in tesseract and creates noise in image. Tesseract doesn't work well with noisy
            data 
            Reference: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35248.pdf
            1. Income Tax Department Government of India (the text might be distorted due to quality of image or inherent problems
            with tesseractocr and its inability to distinguish seamlessly between languages not native to the module or not as 
            developed - such as Hindi.)
            2. Name of the PAN Card Holder
            3. Father's Name
            4. Date of Birth in MM/DD/YYYY format as listed in the PAN Card
            5. ----Permanent Account Number---- text that is a named entity in the PAN Card (not the actual PAN Card Number)
            6. Permanent Account Number in the format ABCDE1234F
            7. Signature as normal text - named entity in the PAN Card
            '''

        # to remove any text read from the image file which lies before the line 'Income Tax Department'

        lineno = 0  # to start from the first line of the text file.

        for wordline in text1:
            xx = wordline.split('\n')
            if ([w for w in xx if re.search(
                    '(INCOMETAXDEPARWENT @|mcommx|INCOME|TAX|GOW|GOVT|Government|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|India|NDIA)$',
                    w)]):
                text1 = list(text1)
                lineno = text1.index(wordline)
                break

        # text1 = list(text1)
        text0 = text1[lineno + 1:]
         # Contains all the relevant extracted text in form of a list - uncomment to check

        def findword(textlist, wordstring):
            lineno = -1
            for wordline in textlist:
                xx = wordline.split()
                if ([w for w in xx if re.search(wordstring, w)]):
                    lineno = textlist.index(wordline)
                    textlist = textlist[lineno + 1:]
                    return textlist
            return textlist

        ###############################################################################################################
        ######################################### Section 5: Dishwasher part ##########################################
        ###############################################################################################################
        nameFound = False
        dobFound = False
        try:
            print(text0)
            for i in text0:
                if (len(i) == 14 and i[4] == ' ' and i[9] == ' '):
                    adhar = i
            for i in text0:
                if(i.find(name1)!=-1):
                    nameFound= True
                    break
            for i in text0:
                if(i.find(dob)!=-1):
                    dobFound=True
                    break
            # Cleaning Name
            name = text0[2]
            name = name.rstrip()
            name = name.lstrip()
            name = re.sub('[^a-zA-Z] +', ' ', name)

            # Cleaning YOB
            yob = text0[3]
            yob = re.sub('[^0-9]+', '', yob)
            yob = yob.replace(" ", "")
            yob = yob[4:8]
            yob = yob.rstrip()
            yob = yob.lstrip()

            # Cleaning Gender
            gender = text0[4]
            gender = gender.replace('/', '')
            gender = gender.replace('(', '')
            gender = gender.rstrip()
            gender = gender.lstrip()

            # # Cleaning Aadhar Number
            # adhar = text0[8]
            # adhar = adhar.rstrip()
            # adhar = adhar.lstrip()

        except:
            pass

        # Making tuples of data
        data = {}
        data['Name'] = name
        data['Year of Birth'] = yob
        data['Gender'] = gender
        data['Number'] = adhar

        # print(data)

        ###############################################################################################################
        ######################################### Section 6: Write Data to JSONs ######################################
        ###############################################################################################################
        #
        # # Writing data into JSON
        # try:
        #     to_unicode = unicode
        # except NameError:
        #     to_unicode = str
        #
        # # Write JSON file
        # with io.open('data.json', 'w', encoding='utf-8') as outfile:
        #     str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        #     outfile.write(to_unicode(str_))
        #
        # # Read JSON file
        # with open('data.json', encoding='utf-8') as data_file:
        #     data_loaded = json.load(data_file)
        #
        # # print(data == data_loaded)
        #
        # # Reading data back JSON(give correct path where JSON is stored)
        # with open('data.json', 'r', encoding='utf-8') as f:
        #     ndata = json.load(f)
        if(dobFound and nameFound):
            return jsonify({'data': 1})
        else:
            return jsonify({'data': 0})



hello=0
# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)


# driver function
if __name__ == '__main__':
	app.run(debug = True)
