from bs4 import BeautifulSoup
import urllib.request
import csv

url = 'https://www.etsy.com/se-en/listing/483597760/christian-t-shirt-choose-joy-tshirt?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery_22'
# url='https://www.etsy.com/se-en/listing/559679743/extra-detailed-paw-patrol-logo-multi?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sc_gallery_1&plkey=1fa7bdf685bee3bba74bd3f5ac773da0cf96ffa8:559679743'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page.read(), "html.parser")

# Field values
title = soup.find("span", {"itemprop":"name"} ).text
description = soup.find("meta", {"name":"description"} ).get("content")
price = soup.find(itemprop="price").get("content")
currencyCode = soup.find(itemprop="currency").get("content")
materials = soup.find("span", {"id":"overview-materials"} ).text

# Quantity
for selector in soup.find_all( "select", {"id":'inventory-select-quantity'} ):
   for child in selector.find_all('option'):
    quantity = child.string

# Tags
tags = []
for selector in soup.find_all( "ul", {"id":'listing-tag-list'} ):
   for child in selector.find_all('li'):
    tags.append( child.text.replace("\n", "") )
tags = str.join(', ', tags)

# Images
images=[]
carouseEntries = soup.select("#image-carousel > li")
for image in carouseEntries: images.append(image.get('data-full-image-href'))

# Variant categories
variantRawCategories = soup.find_all("label")
variantFinalCategories = []
for category in variantRawCategories:
    if 'inventory-variation-select' in str((category.get('for'))):
        variantFinalCategories.append(category.text)

# Variant choices (or values)
variationValuesRaw = soup.find_all("select", {"class": "variation-select"})
variationValues = []
currentList = []
for value in variationValuesRaw:
    valueList = value.text
    valueList = valueList.split('\n')
    new_array = [x for x in valueList if str(x) != 'Select an option']
    variationValues.append(new_array[1:len(valueList)-2])

# finalthing=[]
# i =0
# for x in variationValues:
#     x = str.join(',', variationValues[i])
#     i+=1
#     finalthing.append(x)
# print(finalthing)



# print(title)
print(description)
# print(price)
# print(currencyCode)
# print(quantity)
# print(tags)
# print(materials)
# print(images)
# print(variantFinalCategories)
# print(variationValues)

# Fields to be written
# writeImages = ""
# writeVariantFinalCategories = ""
# write variationValues = ""

# For every image, add "image N" to fields

with open('sample.csv','a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows([[ title, description, price, currencyCode, quantity, tags, materials ]])