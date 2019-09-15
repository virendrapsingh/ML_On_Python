# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 23:44:38 2019
@author: Virendra Pratap Singh
Written Using Spyder (Python 3.7)

What this code does?
1) Read a phrase.
2) Split into words.
3) Remove stopwords.
4) Calculate sentiments and divide words in POSITIVE & NEGATIVE words.
5) Store them in list and ignore NEUTRAL words.
6) Assign POSITIVE words to GREEN (POSITIVE) list and NEGATIVE words to RED (NEGATIVE) list.
7) Draw wordcloud with colours decided on GREEN and RED list.
"""

from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, get_single_color_func
import matplotlib.pyplot as plt

def RemoveDuplicateFrom(list_of_words): 
    """
    Very simplistic duplicate removing function
    """
    final_list = [] 
    for word in list_of_words: 
        if word not in final_list: 
            final_list.append(word) 
    return final_list 

class AssignColour(object):
    """
        Assigns colors to words based on a {color:[words]} dictionary 
        using the already available wordcloud.get_single_color_func function.
        Note that [words] is a list - since I am dividing words in
        two possible categories - Positive and Negative
    """
    def __init__(self, colour_words_dict, default):
        self.colour_words_dict = [
            (get_single_color_func(colour), set(words))
            for (colour, words) in colour_words_dict.items()]

        self.default = get_single_color_func(default)

    def get_colour(self, word):
        try:
            colour = next(
                colour for (colour, words) in self.colour_words_dict
                if word in words)
        except StopIteration:
            colour = self.default

        return colour

    def __call__(self, word, **kwargs):
        return self.get_colour(word)(word, **kwargs)

tribute_dickens = """
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

tribute_herge = """
Tintin is sweet, smart and intelligent.
Haddock is strong, loyal and drunk and friend of Tintin.
Calculus is awesome genius, old and very deaf and friend of Haddock.
Thompson and Thomson are funny, stupid and nice and friends of Tintin.
Rastapopuolous is dangerous, enemy and evil and enemy of Tintin.
Castafiore is sweet, arrogant and rich and friend of Haddock.
Dolivera is shrewd, clever and vendor and friend of Tintin.
Abdullah is rascal, sweet and childish and not-friend of Tintin. 
"""

phrase = tribute_dickens
#phrase = tribute_herge
stop_words=set(stopwords.words("english"))
clean_string = phrase.replace(',', '')
words = clean_string.split()
words = RemoveDuplicateFrom(words)
cleaned_lines = dict()
positive_words = []
negative_words = []

sia = SentimentIntensityAnalyzer()
for r in words: 
    if not r.lower() in stop_words: #Exclude words which are in StopWords list
        neg_polarity = sia.polarity_scores(r)['neg']
        pos_polarity = sia.polarity_scores(r)['pos']
        cpd_polarity = sia.polarity_scores(r)['compound']
        sentiment = (neg_polarity+pos_polarity)*cpd_polarity #I know this isn't a great formula
        if (sentiment != 0) : #Not listing any neutral words since they use the default colour
            cleaned_lines[r]=sentiment

print(cleaned_lines)
print(type(cleaned_lines))
            
for key,value in cleaned_lines.items(): #Divide between POSITIVE and NEGATIVE list
    if (value>0):
        positive_words.append(key)
    else:
        negative_words.append(key)

print(positive_words)
print(negative_words)

colour_words_dict = {
    # POSITIVE words are GREEN
    'green': positive_words,
    # NEGATIVE words are RED
    'red': negative_words
}

print(colour_words_dict)

wc = WordCloud(collocations=False, background_color='skyblue').generate(phrase.lower())
grouped_colour_func = AssignColour(colour_words_dict, 'white') #NEUTRAL words are WHITE
wc.recolor(color_func=grouped_colour_func)

plt.figure()
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()