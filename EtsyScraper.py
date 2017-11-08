from bs4 import BeautifulSoup
import urllib.request
import csv

fieldsWritten = False

def productScrape(url):
    global fieldsWritten
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")
    quantity = 1

    # Field values
    title = soup.find("span", {"itemprop":"name"} ).text
    desc = soup.find("div", {"class":"max-height-text-container ui-toolkit"})
    description = desc.find("div")
    price = soup.find(itemprop="price").get("content")
    #currencyCode = soup.find(itemprop="currency").get("content")
    #materials = soup.find("span", {"id":"overview-materials"} ).text
    print(description)
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

    # Image fields/values
    fieldImages = ""
    fieldVariationCategories = ""
    fieldVariationValues = ""
    fields = [["TITLE", "DESCRIPTION", "PRICE", "QUANTITY", "TAGS"]]
    values = [[title, description, price, quantity, tags]]
    # Add image fields
    for i in range(1, len(images) + 1):
        fields[0].append("IMAGE" + str(i))
        values[0].append(images[i - 1])

    # Variation fields/values
    for i in range(1, len(variationCategories) + 1):
        #fields[0].append("VARIATION " + str(i) + " TYPE")
        fields[0].append("VARIATION " + str(i) + " NAME")
        fields[0].append("VARIATION " + str(i) + " VALUES")
        #values[0].append("Color")
        values[0].append(variationCategories[i - 1])
        values[0].append(variationValues[i - 1])

    with open('sample.csv', 'a', newline='', encoding="utf8") as csvfile:
        writer = csv.writer(csvfile)
        if fieldsWritten is False:
            writer.writerows(fields)
            fieldsWritten = True
        writer.writerows(values)

    csvfile.close()

with open('links','r', encoding="utf8") as links:
    for url in links:
        productScrape(url)