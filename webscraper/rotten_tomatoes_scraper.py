# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 17:13:50 2018

@author: katmal
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd


reviews = []



for i in range(1,51):
    
    url = "url_part_1" + str(i) +"url_part_2"
    
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'lxml')
    
    result = soup.find_all('', {'class': 'col-xs-16'})
    for r in result:
        review = str(r).split("</div>")[-3]
        stars = str(r).count("glyphicon-star")
        review = [stars, review]
        reviews.append(review)
    resp.close()


df = pd.DataFrame(np.asarray(reviews), columns = ['rating', 'text'])

df.to_csv("file.csv")
    

    

    