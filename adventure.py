#------------ Importing libraries
import requests
import re
from bs4 import BeautifulSoup
import sqlite3
from PIL import Image
import os
import sys
import multiprocessing
from multiprocessing import Pool
import time
from metros_cubicos_lib import *
    
#******* begin the actual script

t0= time.time()

define_houses_table= """ CREATE TABLE houses (id integer PRIMARY KEY, property_type text NOT NULL, property_name text NOT NULL, price real NOT NULL, address text DEFAULT "Undefined", town text DEFAULT "Undefined", state text DEFAULT "Undefined", country text DEFAULT "Mexico", description text DEFAULT "Undefined", amenities text DEFAULT "Undefined", terreno text DEFAULT "Undefined", recamaras text DEFAULT "Undefined", banos text DEFAULT "Undefined", image text DEFAULT "Undefined")"""

try:
	n = int(sys.argv[1])
	if n != 150:
		print('Scrapping '+str(n)+' as required')
	else:
		print('Scrapping '+str(n)+' elements by default')
except:
	n = 150
	print('Scrapping '+str(n)+' elements by default')


if not os.path.exists('imgs'):
    os.makedirs('imgs')        
        
        
con = sqlite3.connect('homes.db')
cur = con.cursor()
cur.execute(define_houses_table)
print('Process 1 out of 2: Getting the URLS of the first ' +str(n)+' listings in Metros Cuadrados')
urls = get_n_links(n)

print('Process 2 out of 2: scrapping each listing, this can take a while...')

# cpus = multiprocessing.cpu_count()

# with Pool(cpus) as p:
#         p.map(scrap_n_load, urls)

for element in urls:
    property_type, property_name, price, address, town, state, country, description, amenities, terreno, recamaras, banos, image, bundle_housing = get_info(element)
    #print(bundle_housing)
    #print(bundle_housing.replace('.',''))
    image_location = './imgs/' + bundle_housing.replace('/','') +str(int(price)) +'.jpg'
    #print(image_location)
    image.save(image_location)
    #try:
    #    image.save(image_location)
    #except:
    #    print('couldnt save the image')
    cur = con.cursor()
    lastrow = add_house_to_db(con, property_type, property_name, price, address, town, state, country, description, amenities, terreno, recamaras, banos, image_location)
    print('Scrapped and saved house number ' + str(lastrow))
    
    
    
print('We are almost there, just let me commit the db')
con.commit()
t = time.time() - t0
print('This script took '+ str(t)+ 'seconds to run.')
print('We are good to go, check the images in the imgs folder, the db is saved in this same dir :)')

