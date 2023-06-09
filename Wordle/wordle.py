import operator
from tkinter import *
import tkinter as tk

'''
Created by Alex Polivka
This is a wordle solving application.

Thanks to:
https://www.tutorialspoint.com/index.htm -- helped get my UI started with one
of their tutorials for recieving tkinter input

https://github.com/tabatkins/wordle-list -- tabatkins supplied the wordle list
that is used for my "database". It is supposedly the verified wordle data set. 
I have found on other sites like wordplay.com/new, some of the words my helper
gives as best options aren't recognized as words. So not sure if that is a other
website issue or a data set issue.

It has been proven that this application can win you a game of Wordle but improvements 
are still needed. The biggest improvement can come from the update() method. There needs to be 
some memoization added to improve speed performance, better word choice, and more. 
Improvement List:
-- Dictionary word rankings:
    I believe my original idea for rankings was a good start, but the ranking of words
    character by character may not be the most efficient/best practice to find your first best
    choice
-- Display first "best word" rankings:
    This is now working but may still need to be revamped with the first item on the improvement list.
-- Validation checks:
    Their is no validation of inputs from the UI that the user provides in the text box. 
    Obviously this is no bueno and will immediately crash stuff.
-- Improved UI:
    Not much to say, its ugly and sucks and is confusing unless you created the game.
-- Cleaning of code:
    To say the code is hideous right now might be an understatement. I adhere to the 
    principle of MVP (Minimally Viable Product) and that is what I have produced here
    on version 1.0. So TL;DR: CODE UGLY AND BAD
-- Logical Think:
    I'm not sure if this will come with fixing first improvement list item but I need to really
    sit down and think about where letters are most likely going to be and what logically makes sense.
    Just played a game where I went Soare, Relit, Derny, and then the helper made a bad suggestion so 
    I chose a more reasonable option which was Fewer, and that guess got me to the correct word of Fever.
-- Reupdate Ranks:
    I believe re updating ranks in the update method would be beneficial. 
-- More stuff:
    More improvements are needed but I'm not sure what they all are right now.
    Oh, better documentation of course.

Personal Stats:
    Win Count: 4
    Win Streak: 4
    Longest Win Streak: 4
    Last Win: 4/3/2023
    Winning Word: Stock
    Number of Attempts: 4
    First Win Photo: 1stWordleBotWin.png

Interesting Cases:
Remit: bot got down to 4 words with only 3 attempts left

Idiot: can be gotten in 3

State: bot was right in the order of guesses but I took over
and got us to lose on the word Stave.
'''

''' 
    Input: None
    Returns: words (This is all 5 letter words in our database)
    Gives us all possible 5 letter words in our word database
'''
def wordOptionGenerator():
    
    words = []
    with open("./word_file.txt", "r") as f:
        allText = f.read()
        words = list(map(str, allText.split()))

    return words

'''
    Input: words (This is the list of all words)
    Returns: letter_frequency (This will be the dictionary that holds the frequency of each letter), 
             total_chars (This will be the total number of charss)
    
    This method takes all the possible words and finds the frequency of each letter in the words.
'''
def frequency(words):
    letter_frequency = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 
                        'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0,
                        'w': 0, 'x': 0, 'y': 0, 'z': 0 }
    
    total_chars = 0

    for word in words:
        total_chars += len(word)
        for key in letter_frequency:
            if key in word:
                letter_frequency[key] += word.count(key)

    return dict(sorted(letter_frequency.items(), key=lambda x:x[1])), total_chars

'''
    Input:  letter_frequency (This will be the dictionary that holds the frequency of each letter), 
            total_chars (This will be the total number of charss)
    Returns: points (This holds the number of points each character is worth)
    
    This method takes the frequencies and assigns points to them based on how
    frequent they are compared to the total number of chars.
'''
def frequency_conversion(letter_frequency, total_chars):
    points = {}

    for key in letter_frequency:
        point = (letter_frequency[key]/total_chars)*100
        points[key] = point
        
    return points
'''
Simple dicitonary merger
'''
def dict_merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

'''
    Input:  words (This is the list of all words) 
            points (This holds the number of points each character is worth)
    Returns: final_dictionary (This is the final ranking of all words and where they stand at to be guessed)
    
    This method takes the frequencies and assigns points to them based on how
    frequent they are compared to the total number of chars.
'''
def ranking(words, points):
    five_unique = {}
    four_unique = {}
    three_unique = {}
    two_unique = {}
    points_and_unique = {}

    for word in words:
        points_and_unique[word] = [0, 0]
        for key in points:
            point = word.count(key) * points[key]
            unique = 1 if point > 0.0 else 0

            points_and_unique[word][0] += point
            points_and_unique[word][1] += unique

        # Splitting up the sorts into amount of unique letters
        if points_and_unique[word][1] == 5:
            five_unique[word] = (points_and_unique[word][0], 5)
        if points_and_unique[word][1] == 4:
            four_unique[word] = (points_and_unique[word][0], 4)
        if points_and_unique[word][1] == 3:
            three_unique[word] = (points_and_unique[word][0], 3)
        if points_and_unique[word][1] == 2:
            two_unique[word] = (points_and_unique[word][0], 2)

    # Run sort on each set of words based on their character scores
    five_unique = dict(sorted(five_unique.items(), key=operator.itemgetter(1), reverse=True))
    four_unique = dict(sorted(four_unique.items(), key=operator.itemgetter(1), reverse=True))
    three_unique = dict(sorted(three_unique.items(), key=operator.itemgetter(1), reverse=True))
    two_unique = dict(sorted(two_unique.items(), key=operator.itemgetter(1), reverse=True))

    # Combine dictionaries
    final_dictionary = dict_merge(five_unique, four_unique)
    final_dictionary = dict_merge(final_dictionary, three_unique)
    final_dictionary = dict_merge(final_dictionary, two_unique)

    # start testing
    return final_dictionary

def update(wordle_guess, color_pattern, ranks):
    '''
    This whole method assumes valid input, validation checks are still
    needed throughout most of the code but most certainly this method.
    This method has a lot of weird turns. I learned that for whatever 
    reasons, there are duplicates in the words_to_del that would cause
    some errors when trying to delete certain values, because obviously 
    once you have deleted a unique value from a dictionary, you can't
    delete them again.
    This method needs major optimization. The if statements are annoying
    and so is the checking method. There needs to be some memoization
    or dynamic programming done that keeps track of certain things.
    For example, if you are given a 'g' in the color_list, there is
    no reason to ever check that charater in the wordle_list ever again.
    Other than some optimization and weird bugs, I believe this method 
    works as it should.
    '''

    color_list = [*color_pattern]
    wordle_list = [*wordle_guess]
    
    words_to_del = []

    for x in range(5):
        for key in ranks:

            if color_list[x] == 'b':
                if wordle_list[x] in key:
                    words_to_del.append(key)
            elif color_list[x] == 'y':
                if wordle_list[x] not in key or wordle_list[x] == key[x]:
                    words_to_del.append(key)
            else:
                if wordle_list[x] != key[x]:
                    words_to_del.append(key)

    words_to_del = [*set(words_to_del)]

    for word in words_to_del:
        del ranks[word]

    return ranks



def display(ranks):

    root=tk.Tk()
    
    # setting the windows size
    root.geometry("600x800")


    # declaring string variable
    # for storing name and password
    wordle_guess = tk.StringVar()
    color_pattern = tk.StringVar()
    
    
    # defining a function that will
    # get the name and password and
    # print them on the screen
    def submit(ranks):
    
        guess = wordle_guess.get()
        pattern = color_pattern.get()

        print("The guess is : " + guess)
        print("The pattern is : " + pattern)

        
        ranks = update(guess, pattern, ranks)

        # This code displays best options
        counter = 0
        options = ""
        for key in ranks:

            options += key + '\n'
            counter += 1
            if counter == 30:
                break
        # This updates our text label
        t["text"] = options


    # creating a label for
    # name using widget Label
    name_label = tk.Label(root, text = 'Wordle Guess', font=('calibre',10, 'bold'))
    
    # creating a entry for input
    # name using widget Entry
    name_entry = tk.Entry(root, textvariable = wordle_guess, font=('calibre',10,'normal'))
    
    # creating a label for password
    passw_label = tk.Label(root, text = 'Color Pattern', font = ('calibre',10,'bold'))
    
    # creating a entry for password
    passw_entry=tk.Entry(root, textvariable = color_pattern, font = ('calibre',10,'normal'))
    
    # creating an explanation for the color pattern format
    pattern_text = "When entering your color pattern, enter a single character for each square. For grey entries, enter the character 'b', for yellow, enter the character 'y', for green, enter the character 'g'."
    color_patter_label = tk.Label(root, text = pattern_text, font = ('calibre',10,'bold'), wraplength=550)
    # creating a button using the widget
    # Button that will call the submit function
    sub_btn=tk.Button(root,text = 'Submit', command = lambda r = ranks:  submit(r))
    
    # placing the label and entry in
    # the required position using grid
    # method
    name_label.pack(side = TOP)
    name_entry.pack(side = TOP)
    passw_label.pack(side = TOP)
    passw_entry.pack(side = TOP)
    color_patter_label.pack(side=TOP)
    sub_btn.pack(side = TOP)
    
    # The frame that will display the best options for the user
    options_frame = Frame(root)
    options_frame.pack(side = BOTTOM)

    # This code displays best options
    counter = 0
    options = ""
    for key in ranks:
        options += key + '\n'
        counter += 1
        if counter == 30:
            break

    t = Label(options_frame, font = ('calibre',10,'bold'), text = options)
    t.pack()

    
    # performing an infinite loop
    # for the window to display
    root.mainloop()
    
def main():
    # gets possible 5 letter words
    words = wordOptionGenerator()

    # determines how frequent each character is from the words database
    letter_frequency, total_chars = frequency(words)

    # assigns a total number of possible points per word
    points = frequency_conversion(letter_frequency, total_chars)

    # dicitonary that holds each word and its respective rank compared to
    # other words. Words are ranked by character uniqueness and point value
    ranks = ranking(words, points)
    
    # deals with displaying UI and running the updates to each word choice
    display(ranks)

    pass

if __name__ == '__main__':
    main()