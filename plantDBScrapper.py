import requests
import urllib3
import os
from PIL import Image
from lxml import html
from bs4 import BeautifulSoup
from matplotlib.pyplot import imshow
from io import BytesIO
from tqdm import tqdm
import cv2
import numpy as np
import csv

#saving folder path
path = "C:/Users/Qnouro/Desktop/Programming/Scrapper/leavesDatabase/"
csv_path = "C:/Users/Qnouro/Desktop/Programming/Scrapper/leavesDatabase/leaf.csv"


#database url
database_page = 'http://clearedleavesdb.org/?q=node%2F1337%2F79&sort_by=totalcount&sort_order=DESC&items_per_page=100&page=0'


#getting the html code
r = requests.get(database_page)
soup = BeautifulSoup(r.content, "html.parser")


#img index for name
img_counter = 0


#last : 47
for k in tqdm(range(100)):
    database_page = 'http://clearedleavesdb.org/?q=node%2F1337%2F79&sort_by=totalcount&sort_order=DESC&items_per_page=100&page=' + str(k)

    for j in tqdm(range(1, 21)):
        #row scraping
        row = soup.find('tr', {'class': "row-"+str(j)})

        for i in range(1, 6):
            #getting the img address
            addr = row.find('td', {'class':"col-" + str(i)}).find('a')


            #creating + printing the info page url
            photo_page = 'http://clearedleavesdb.org' + addr['href']


            #scraping the img url
            r2 = requests.get(photo_page)
            soup2 = BeautifulSoup(r2.content, "html.parser")
            real_img_addr = soup2.find('div', {'class' : 'field-item even'}).find('img')


            #scraping the leaf type
            try:
                first_type_name = soup2.find('div', {'class' : 'field field-name-field-leaf-image-family field-type-text field-label-inline clearfix'}).find('div', {'class' : 'field-item even'}).getText()
            except:
                first_type_name = ""

            try:
                second_type_name = soup2.find('div', {'class' : 'panel-pane pane-entity-field pane-node-field-leaf-image-genus'}).find('div', {'class' : 'field-item even'}).getText()
            except:
                second_type_name = ""


            #downloading the img
            http = urllib3.PoolManager()
            dll = http.request('GET', real_img_addr['src'])
            resized_image = Image.open(BytesIO(dll.data))


            ##showing the img for debugging purposes
            #cv2.imshow('image', cv2.cvtColor(np.array(resized_image), cv2.COLOR_RGB2BGR))
            #cv2.waitKey(0)


            #Creating the database
            data = [np.asarray(resized_image), first_type_name.lower(), second_type_name.lower()]


            #writing in csv file
            with open(csv_path, mode='a') as leaf:
                leaf = csv.writer(leaf, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                leaf.writerow(data)


            #saving the img
            resized_image.save(path + str(img_counter) + ".jpg", 'JPEG')
            img_counter+= 1














#
# payload = {'key1': 'value1', 'key2': 'value2'}
#
# r = requests.get('https://httpbin.org/get', params=payload)
# the resulting url is: https://httpbin.org/get?key2=value2&key1=value1






# - too much whitespace
# - pep8 violation with imports
# - blanket except statements
# - global variables
# - string concatenation
# - pep8 violation with line lengths
# - code duplication with first/second type names
# - mixing quotes for strings
# - mixing urllib and requests, why not use one?
# - ambiguous variables i, j and k
