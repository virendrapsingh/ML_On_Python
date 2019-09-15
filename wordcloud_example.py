# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 12:38:10 2019

@author: Aditya
"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt

two_cities = """
It was the best of times, 
it was the worst of times, 
it was the age of wisdom, 
it was the age of foolishness, 
it was the epoch of belief, 
it was the epoch of incredulity,
 it was the season of Light, 
 it was the season of Darkness, 
 it was the spring of hope, 
 it was the winter of despair, 
 we had everything before us, 
 we had nothing before us, 
 we were all going direct to Heaven, 
 we were all going direct the other way.
"""

cloud_two_cities = WordCloud().generate(two_cities)
print(cloud_two_cities)
plt.imshow(cloud_two_cities, interpolation='bilinear')

plt.axis('off')
plt.show()
