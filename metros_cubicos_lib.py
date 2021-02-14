import requests
import re
import sqlite3
from bs4 import BeautifulSoup
from PIL import Image
def n_visits(n):
    """Determines the number of times the listings page must be loaded, making sure that a lisitng does not appear twice in a signle listing"""
    return(int(n%48))
def get_fixed_price(ugly_price):
    """returns a float from an array filled with new lines, tabs and text, the numbers of the price sould be the only ones in the string"""
    fixed_price = ''
    for element in ugly_price:
        fixed_price = fixed_price + element
    return(float(fixed_price))

def split_delegacion_estado(delegacion_estado):
    pattern = ","
    split = re.split(pattern,delegacion_estado)
    delegacion = split[0]
    estado = split[1][1:]
    if split[1][1:] == 'Distrito Federal':
        estado = 'Ciudad de México'
    return([delegacion, estado])


def get_fixed_amenities(amenities):
    pattern = "\n"
    split = re.split(pattern,amenities)
    fixed_ammenities = ''
    for element in split:    
        if bool(element):
            fixed_ammenities = fixed_ammenities + element + ', '
    return(fixed_ammenities)

def fix_description(description):
    a_list = description.split()
    fixed_string = " ".join(a_list)
    return(fixed_string)

def get_long(soup):
    card_section = soup.find_all("div", {"class": "card-section"})[0]
    entrega = card_section.find_all("span", {"class": "attribute-value"})[0].get_text()
    unidades = card_section.find_all("span", {"class": "attribute-value"})[1].get_text()
    card_section = soup.find_all("div", {"class": "card-section"})[1]
    terreno = card_section.find_all("span", {"class": "attribute-value"})[0].get_text()
    recamaras = card_section.find_all("span", {"class": "attribute-value"})[1].get_text()
    banos = card_section.find_all("span", {"class": "attribute-value"})[2].get_text()
    return([entrega, unidades, terreno, recamaras, banos])

def get_description(soup):
    description = soup.find("pre", {"class": "preformated-text"}).get_text()
    fixed_description = fix_description(description)
    return(fixed_description)

def get_amenities(soup):
    amenities = soup.find("ul", {"class": "boolean-attribute-list"}).get_text()
    fixed_amenities = get_fixed_amenities(amenities)
    return(fixed_amenities)

def get_delegacion_estado(soup):
    delegacion_estado = soup.find("span", {"class": "profile-info-location-value"}).get_text()
    delegacion, estado = split_delegacion_estado(delegacion_estado)
    return([delegacion,estado])

def get_address(soup):
    address = soup.find("h2", {"class": "map-location"}).get_text()
    return(address)

def get_price(soup):
    price = soup.find("div", {"class": "vip-product-aux-info__price"}).get_text()
    ugly_list_of_price = re.findall('[0-9]+', price)
    fixed_list_of_price = get_fixed_price(ugly_list_of_price)
    return(fixed_list_of_price)

def get_name(soup):
    name_housing = soup.find("h4", {"class": "vip-product-aux-info__name"}).get_text()
    return(name_housing)

def get_n_links(n):
    links_to_housing = []
    for element in range(n_visits(n)):
        page_name = base_url+str(element*48+1)
        print(page_name)
        page = requests.get(page_name)
        soup = BeautifulSoup(page.content, 'html.parser')
        individual_urls = soup.find_all("div", {"class": "images-viewer"})
        for element in individual_urls:
            links_to_housing.append(element.get('item-url'))
            if len(links_to_housing) >= n:
                return(links_to_housing)
            
def get_long_fixed(soup):
    attr_list = soup.find_all("span", {"class": "vip-product-info__attribute-value"})
    superficie = attr_list[0].get_text()
    recamaras = attr_list[1].get_text()
    banos = attr_list[2].get_text()
    return([superficie, recamaras, banos])

def get_image(soup):
    pic_url_container = soup.find("div", {"class": "short-description-gallery"})
    pic_url = pic_url_container.get('style')[22:-1]
    #print(pic_url)
    im = Image.open(requests.get(pic_url, stream=True).raw)
    return(im)


def add_house_to_db(con, property_type, property_name, price, address, town, state, country, description, amenities, terreno, recamaras, banos, image_location):

    #sql statement

    sql = """INSERT INTO houses (property_type, property_name, price, address, town, state, country, description, amenities, terreno, recamaras, banos, image) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""

    #sql statement execution

    cur = con.cursor()
    cur.execute(sql, (property_type, property_name,price, address, town, state, country, description, amenities, terreno, recamaras, banos, image_location))
    return cur.lastrowid

def add_picture_location(con, pic_location):
    sql = """INSERT INTO houses(image)VALUES(?)"""
    cur = con.cursor()
    cur.execute(sql, [pic_location])

def get_info(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        try:
            bundle_housing = get_name(soup)
        except:
            property_type = 'Unknown'
            property_name = 'Unnamed'
            print('name error in url')
        
        if 'Casa' in bundle_housing:
            property_type = 'Casas en venta'
            property_name = bundle_housing[18:]
        elif 'Desarrollo' in bundle_housing:
            property_type = 'Desarrollo'
            property_name = bundle_housing[11:]
        else:
            property_type = 'Unknown'
            property_name = 'Unnamed'
        
            
        try: 
            price = get_price(soup)
        except:
            price = -1
            print('price error in url')

        try:
            address = get_address(soup)
        except:
            address = 'Not_Found'
            print('address error in url')

        try:
            town,state = get_delegacion_estado(soup)
        except:
            town,state =['Not_Found', 'Not_Found']
            print('del_estado error in url')

            
        country = 'Mexico'
        
        try:
            amenities = get_amenities(soup)
        except:
            amenities = 'Not_Found'
            print('ammenities error in url')

        try:
            description = get_description(soup)
        except:
            description = 'Not_Found'
            print('description error in url')

        try: 
            terreno, recamaras, banos = get_long_fixed(soup)
        except:
            terreno, recamaras, banos = ['Not_Found', 'Not_Found', 'Not_Found' ]
            print('long error in url')
            
        try:
            image = get_image(soup)
            #print(image)
        except:
            image = 'nope'
            print('image error in url')
            
        return(property_type, property_name, price, address, town, state, country, description, amenities, terreno, recamaras, banos, image, bundle_housing)


def scrap(element):
    property_type, property_name, price, address, town, state, country, description, amenities, terreno, recamaras, banos, image, bundle_housing = get_info(element)
    return(property_type, property_name, price, address, town, state, country, description, amenities, terreno, recamaras, banos, bundle_housing, image)

# Good idea, but I would need to find a way to orchestrate the process of writing to db
def scrap_n_load(bundle):
    element, con = bundle
    property_type, property_name, price, address, town, state, country, description, amenities, terreno, recamaras, banos, image, bundle_housing = get_info(element)
    print(bundle_housing)
    print(bundle_housing.replace('.',''))
    image_location = './imgs/' + bundle_housing.replace('.','') +str(int(price)) +'.jpg'
    try:
        image.save(image_location)
    except:
        print('couldnt save the image')
    cur = con.cursor()
    lastrow = add_house(con, property_type, property_name, price, address, town, state, country, description, amenities, terreno, recamaras, banos, image_location)
    print('Scrapped and saved house number ' + str(lastrow))
    
base_url = "https://inmuebles.metroscubicos.com/casas/venta/_Desde_"
