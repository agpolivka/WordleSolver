'''
Created by Alex Polivka
This script is used to generate the word_file.txt file.
It is currently used based on a weird and slightly incorrect english
word set. 
'''
from english_words import get_english_words_set
web2lowerset = get_english_words_set(['web2'], lower=True)


word_file = open("word_file.txt", 'w')

for word in web2lowerset:
    if len(word) >= 5 and len(word) <= 5:

        word_file.writelines(word+"\n")
