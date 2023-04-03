''' 
    Input: None
    Returns: words (This is all 5 letter words in our database)
    Gives us all possible 5 letter words in our word database
'''
import operator

from itertools import islice


def wordOptionGenerator():
    
    words = []
    with open("C:/Users/agpolivka/Wordle/word_file.txt", "r") as f:
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


'''
This method gives a frequency based on where every character is most likely to be in a 5 letter word
'''
def location_frequency(words):
    loc_frequency =   {'a': [0,0,0,0,0], 'b': [0,0,0,0,0], 'c': [0,0,0,0,0], 'd': [0,0,0,0,0], 'e': [0,0,0,0,0], 
                            'f': [0,0,0,0,0], 'g': [0,0,0,0,0], 'h': [0,0,0,0,0], 'i': [0,0,0,0,0], 'j': [0,0,0,0,0], 
                            'k': [0,0,0,0,0], 'l': [0,0,0,0,0], 'm': [0,0,0,0,0], 'n': [0,0,0,0,0], 'o': [0,0,0,0,0], 
                            'p': [0,0,0,0,0], 'q': [0,0,0,0,0], 'r': [0,0,0,0,0], 's': [0,0,0,0,0], 't': [0,0,0,0,0], 
                            'u': [0,0,0,0,0], 'v': [0,0,0,0,0], 'w': [0,0,0,0,0], 'x': [0,0,0,0,0], 'y': [0,0,0,0,0], 
                            'z': [0,0,0,0,0] }
    
    for word in words:
        for key in loc_frequency:
            if key == word[0]:
                loc_frequency[key][0] += 1
            if key == word[1]:
                loc_frequency[key][1] += 1
            if key == word[2]:
                loc_frequency[key][2] += 1
            if key == word[3]:
                loc_frequency[key][3] += 1
            if key == word[4]:
                loc_frequency[key][4] += 1

    return loc_frequency        

'''
Point conversion for the location frequency
'''
def location_conversion(loc_frequency, frequency):

    for char in loc_frequency:
            loc_frequency[char][0] = (loc_frequency[char][0]/frequency[char])*100
            loc_frequency[char][1] = (loc_frequency[char][1]/frequency[char])*100
            loc_frequency[char][2] = (loc_frequency[char][2]/frequency[char])*100
            loc_frequency[char][3] = (loc_frequency[char][3]/frequency[char])*100
            loc_frequency[char][4] = (loc_frequency[char][4]/frequency[char])*100
    return loc_frequency

'''
I think this method may merge words better based on their location frequency and general
frequency, idk
'''
def test_merger(ranks, loc_conversion):
    for key in ranks:
        for char in loc_conversion:
            if char == key[0]:
                ranks[key] = (loc_conversion[char][0]+ranks[key][0], ranks[key][1])
            if char == key[1]:
                ranks[key] = (loc_conversion[char][1]+ranks[key][0], ranks[key][1])
            if char == key[2]:
                ranks[key] = (loc_conversion[char][2]+ranks[key][0], ranks[key][1])
            if char == key[3]:
                ranks[key] = (loc_conversion[char][3]+ranks[key][0], ranks[key][1])
            if char == key[4]:
                ranks[key] = (loc_conversion[char][4]+ranks[key][0], ranks[key][1])

    ranks = dict(sorted(ranks.items(), key=operator.itemgetter(1), reverse=True))
    return ranks
    

'''
From: https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
'''
def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))

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
    
    loc_frequency = location_frequency(words)
    loc_frequency = location_conversion(loc_frequency, letter_frequency)

    new_ranks = test_merger(ranks, loc_frequency)

    counter = 0
    # for key in ranks:
    #     print(key, ranks[key])
    #     if counter ==9:
    #         break
    #     counter += 1
    # print()
    # counter = 0
    # for nkey in new_ranks:
    #     print(nkey, new_ranks[nkey])
    #     if counter ==9:
    #         break
    #     counter += 1
    # deals with displaying UI and running the updates to each word choice
    while True:
        words = []
        new_words = []

        if len(ranks) >15:
            words = take(15, ranks.items())
        else:
            words = take(len(ranks), ranks.items())
        print()
        # if len(new_ranks) >15:
        #     new_words = take(15, new_ranks.items())
        # else:
        #     new_words = take(len(new_ranks), new_ranks.items())

        print(words)
        print(new_words)

        ans = input("what is your word guess?: ")
        pattern = input("color pattern?: ")

        ranks = update(ans, pattern, ranks)
        #new_ranks = update(ans, pattern, new_ranks)
        
    pass

if __name__ == '__main__':
    main()