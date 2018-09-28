from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

scrape_url = "https://www.newegg.com/global/in/Store/SubCategory.aspx?SubCategory=343&Page="


def scrape(product, n):
    scrape_url = "https://www.newegg.com/global/in/Product/ProductList.aspx?Submit=ENE&IsNodeId=1&Description="
    l = []
    for i in range(1, n):

        webpage = urlopen(scrape_url + str(product) + "&Page=" + str(i))
        html_data = BeautifulSoup(webpage.read(), "html.parser")
        webpage.close()
        containers = html_data.findAll("div", {"class": "item-container"})
        if len(containers) <= 0:
            break
        print("Page: " + str(i))
        print("Products: " + str(len(containers)))
        for container in containers:
            try:
                loc_dict = {}
                brand = container.div.div.a.img["title"]
                img_src = container.findAll("a", {"class": "item-img"})[0].img["src"]
                title = container.findAll("a", {"class": "item-title"})[0].text
                price = container.findAll("li", {"class": "price-current"})[0].text.strip()
                if price != "":
                    price_num = "".join(price.split()[1].split(',')[:])
                else:
                    price = "OUT OF STOCK"
                    price_num = 0
                price = " ".join(price.split()[:2])
                loc_dict["Brand"] = brand
                loc_dict["Img_Src"] = img_src
                loc_dict["Title"] = title
                loc_dict["Price"] = price
                l.append(loc_dict)
                print(title + " " + price)
            except:
                print("Thrown")
        print()
    with open('./Parts/'+product+'.json', 'w') as file:
        json.dump(l, file)
