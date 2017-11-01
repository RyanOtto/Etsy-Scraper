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
variationCategories = []
for category in variantRawCategories:
    if 'inventory-variation-select' in str((category.get('for'))):
        variationCategories.append(category.text)

# Variant choices (or values)
variationValuesRaw = soup.find_all("select", {"class": "variation-select"})
variationValues = []
currentList = []
for value in variationValuesRaw:
    valueList = value.text
    valueList = valueList.split('\n')
    newValueList = [x for x in valueList if str(x) != 'Select an option']
    variationValues.append(newValueList[1:len(valueList) - 2])
for i in range(0, len(variationValues)):
    variationValues[i] = str.join(",", variationValues[i])

# finalthing=[]
# i =0
# for x in variationValues:
#     x = str.join(',', variationValues[i])
#     i+=1
#     finalthing.append(x)
# print(finalthing)



# print(title)
# print(description)
# print(price)
# print(currencyCode)
# print(quantity)
# print(tags)
# print(materials)
# print(images)
# print(variationCategories)
# print(variationValues)

# Image fields/values
with open('sample.csv','w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    fieldImages = ""
    fieldVariationCategories = ""
    fieldVariationValues = ""
    fields = [["TITLE", "DESCRIPTION", "PRICE", "CURRENCY CODE", "QUANTITY", "TAGS", "MATERIALS"]]
    values = [[ title, description, price, currencyCode, quantity, tags, materials ]]
    # Add image fields
    for i in range(1, len(images)):
        fields[0].append("IMAGE" + str(i))
        values[0].append(images[i])

    # Variation fields/values
    for i in range(1, len(variationCategories)+1):
        fields[0].append("VARIATION " + str(i) + " TYPE")
        fields[0].append("VARIATION " + str(i) + " NAME")
        fields[0].append("VARIATION " + str(i) + " VALUES")
        values[0].append("Color")
        values[0].append(variationCategories[i-1])
        values[0].append(variationValues[i-1])


    writer.writerows(fields)
    writer.writerows(values)
csvfile.close()