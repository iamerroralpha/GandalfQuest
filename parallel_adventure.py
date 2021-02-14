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


print('Process 1 out of 3: Getting the URLS of the first ' +str(n)+' listings in Metros Cuadrados')
urls = get_n_links(n)

print('Process 2 out of 3: scrapping each listing, this can take a while...')
cpus = multiprocessing.cpu_count()

i = 0
with Pool(cpus) as p:
         data=(p.map(scrap, urls))


print('Process 3 out of 3: saving the info to db and filesystem...')

if not os.path.exists('imgs'):
    os.makedirs('imgs')

con = sqlite3.connect('homes.db')
cur = con.cursor()
cur.execute(define_houses_table)

i = 1
for element in data:
    img_name = element[-2].replace('/','')+str(int(element[2]))
    img_location = './imgs/' + img_name +'.jpg'
    try:
     	element[-1].save(img_location)
    except:
     	print('couldnt save picture '+str(i))
    add_house_to_db(con,element[0],element[1],element[2],element[3],element[4],element[5],element[6],element[7],element[8],element[9],element[10],element[11],img_location)
    i = i+1
    
    
print('We are almost there, just let me commit the db')
con.commit()
t = time.time() - t0
print('This script took '+ str(t)+ 'seconds to run.')
print('We are good to go, check the images in the imgs folder, the db is saved in this same dir :)')

