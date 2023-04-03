'''
This is a sandbox area for UI testing.
Currently mostly copy and pasta from: https://www.tutorialspoint.com/how-to-get-the-input-from-the-tkinter-text-widget
'''
from tkinter import *
import tkinter as tk
 

  
root=tk.Tk()
 
# setting the windows size
root.geometry("600x400")


# declaring string variable
# for storing name and password
wordle_guess = tk.StringVar()
color_pattern = tk.StringVar()
 
  
# defining a function that will
# get the name and password and
# print them on the screen
def submit():
 
    guess = wordle_guess.get()
    pattern = color_pattern.get()
     
    print("The name is : " + guess)
    print("The password is : " + pattern)
     
    return guess, pattern
     
     
# creating a label for
# name using widget Label
name_label = tk.Label(root, text = 'Wordle Guess', font=('calibre',10, 'bold'))
  
# creating a entry for input
# name using widget Entry
name_entry = tk.Entry(root, textvariable = wordle_guess, font=('calibre',10,'normal'))
  
# creating a label for password
passw_label = tk.Label(root, text = 'Password', font = ('calibre',10,'bold'))
  
# creating a entry for password
passw_entry=tk.Entry(root, textvariable = color_pattern, font = ('calibre',10,'normal'), show = '*')
  
# creating a button using the widget
# Button that will call the submit function
sub_btn=tk.Button(root,text = 'Submit', command = submit)
  
# placing the label and entry in
# the required position using grid
# method
name_label.grid(row=0,column=0)
name_entry.grid(row=0,column=1)
passw_label.grid(row=1,column=0)
passw_entry.grid(row=1,column=1)
sub_btn.grid(row=2,column=1)
  
# performing an infinite loop
# for the window to display
root.mainloop()