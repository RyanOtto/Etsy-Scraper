from bs4 import BeautifulSoup
import urllib.request
import csv

linkWord="word"
# url = 'https://www.etsy.com/listing/275754976/vintage-forest-green-red-silk-traveler'
url = 'https://www.etsy.com/se-en/listing/483597760/christian-t-shirt-choose-joy-tshirt?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sr_gallery_22'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page.read(), "html.parser")

# Field values
title = soup.find("span", {"itemprop":"name"} ).text
description = soup.find("div", {"id":"item-description"} ).text
price = soup.find(itemprop="price").get("content")
currencyCode = soup.find(itemprop="currency").get("content")

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


materials = soup.find("span", {"id":"overview-materials"} ).text


# Images
images=[]
for selector in soup.find_all("ul", {"id":"image-carousel"} ):
    for child in selector.find_all('li'):
        for childchild in selector.find_all('img'):
            images.append(childchild.get("src"))
images = str.join(", ", images)

# Variant categories
variantRawCategories = soup.find_all("label")
variantFinalCategories = []
for category in variantRawCategories:
    if 'inventory-variation-select' in str((category.get('for'))):
        variantFinalCategories.append(category.text)
variantFinalCategories = str.join(", ", variantFinalCategories)
print(variantFinalCategories)



variationValues = soup.find_all("select", {"class": "variation-select"})

# print(variantCategories)
# for value in variationValues:
#     print(value)



# print(title)
# print(description)
# print(price)
# print(currencyCode)
# print(quantity)
# print(tags)
# print(materials)
# print(images)


# with open('sample.csv','w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Field 1", "Field 2", "Field 3", "Field 4", "Field 5", "Field 6", "Field 7"])
#     writer.writerows([["a","b","c"],["a","b","c"],["a","b","c"],["a","b","c"],["a","b","c"],["a","b","c"],
#                     ["a", "b", "c"],["a","b","c"],["a","b","c"],["a","b","c"],["a","b","c"]])