from bs4 import BeautifulSoup
import urllib.request
import csv

linkWord="word"
url = 'https://www.etsy.com/listing/275754976/vintage-forest-green-red-silk-traveler'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page.read(), "html.parser")

#Field values
title = soup.find("span", {"itemprop":"name"} ).text
description = soup.find("div", {"id":"item-description"} ).text
price = soup.find(itemprop="price").get("content")
currencyCode = soup.find(itemprop="currency").get("content")

quantity = soup.find("span", {"itemprop":"name"} ).text
tags = soup.find("span", {"itemprop":"name"} ).text
materials = soup.find("span", {"itemprop":"name"} ).text
image1 = soup.find("span", {"itemprop":"name"} ).text
image2 = soup.find("span", {"itemprop":"name"} ).text
image3 = soup.find("span", {"itemprop":"name"} ).text
image4 = soup.find("span", {"itemprop":"name"} ).text
image5 = soup.find("span", {"itemprop":"name"} ).text
variation1Type = soup.find("span", {"itemprop":"name"} ).text
variation1Name = soup.find("span", {"itemprop":"name"} ).text
variation1Values = soup.find("span", {"itemprop":"name"} ).text
variation2Type = soup.find("span", {"itemprop":"name"} ).text
variation2Name = soup.find("span", {"itemprop":"name"} ).text
variation2Values = soup.find("span", {"itemprop":"name"} ).text


print(title)
print(description)
print(price)
print(currencyCode)


# with open('sample.csv','w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["Field 1", "Field 2", "Field 3", "Field 4", "Field 5", "Field 6", "Field 7"])
#     writer.writerows([["a","b","c"],["a","b","c"],["a","b","c"],["a","b","c"],["a","b","c"],["a","b","c"],
#                     ["a", "b", "c"],["a","b","c"],["a","b","c"],["a","b","c"],["a","b","c"]])
