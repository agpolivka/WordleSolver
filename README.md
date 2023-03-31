# WordleSolver
This is my first implementation of a Wordle helper that will solve a Wordle game. This solver isn't perfect yet but I intend to keep making updates, so I will call this Version 1.0

I will try to explain the UI as concisely as possible, since the documentation in the UI is lacking.
You currently must put in a word on the wordle website and see what the result of that word is. 
Once you have typed that word into the website, you will put that same word into the "Wordle Guess" textbox.
You will then examine the color contents of each letter, from the word you just entered, on the Wordle website. 
After examining those colors, you will enter a 5 character string into the "Color Pattern" textbox. This 5 
character string should be made up of only the characters 'b', 'y', or 'g'. There should be no spaces in this 5 
character string. The character 'b' refers to a gray box. The character 'y' refers to a yellow box. The character 
'g' refers to a green box. 

For example, if you put in the word 'plate' on the Wordle website and the 'p' box was green, the 'l' box was
green, the 'a' box was grey, the 't' box was yellow, and the 'e' box was gray, you would enter the string
'ggbyb' into the "Color Pattern" box.

I hope this helper *cough cough* helps.
