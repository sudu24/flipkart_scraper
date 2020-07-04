# load libraries
# pip install bs4
# pip install selenium
# pip install pandas

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


browser = webdriver.Chrome(ChromeDriverManager().install())

comment_list = []
au_list = []
comment_date = []
title_list = []
loc_list = []
star_list = []
helpful_list = []
not_helpful_list = []
i = 1

while(True):
    print(i)
    url0 = "https://www.flipkart.com/venus-anti-pollution-mask-men-women-n95-inbuilt-filter-air-masks-reusable-respirator/product-reviews/itm86ff468b03c9a?pid=MRPFPKZMZNZXBJPY&aid=overall&certifiedBuyer=false&sortOrder=MOST_RECENT"
    url = url0 + "&page=%s" % i
    i = i + 1
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    comment_container = soup.findAll("div", {"class": "qwjRop"})
    author = soup.findAll("p", {"class": "_3LYOAd _3sxSiS"})
    title = soup.findAll("p", {"class": "_2xg6Ul"})
    loc = soup.findAll("p", {"class": "_19inI8"})
    star = soup.findAll("div", {"class": "hGSR34"})
    helpful = soup.findAll("span", {"class": "_1_BQL8"})
    date = soup.findAll("p", {"class":"_3LYOAd"})

    if len(comment_container) == 0:
        break
    # if i > 4:
    #     break

    for d in range(len(date)):
        if d % 2 != 0:
            d_date = date[d].get_text()
            comment_date.append(d_date)

    for c in author:
        note_author = c.get_text().replace('>', '')
        au_list.append(note_author)

    for t in title:
        note_title = t.get_text().replace('>', '')
        title_list.append(note_title)

    for comment in comment_container:
        note_comment = comment.get_text().replace('>', '')
        comment_list.append(note_comment)

    for lo in loc:
        loc_l = lo.get_text().replace('>','')
        loc_list.append(loc_l)

    for s in star[1:]:
        star_s = s.get_text()
        star_list.append(star_s)

    for help in range(len(helpful)):
        #print(helpful[help].get_text())
        if help % 2 == 0:
            helpful_list.append(helpful[help].get_text())
        else:
            not_helpful_list.append(helpful[help].get_text())

browser.quit()
df = pd.DataFrame({"Date": comment_date,
                    'Author':au_list,
                    'Title': title_list,
                    'Comment':comment_list,
                    'Location': loc_list,
                    'Star': star_list,
                    'Helpful': helpful_list,
                    'Not_Helpful': not_helpful_list})

df.to_csv('venus_mask.csv', index=False)

