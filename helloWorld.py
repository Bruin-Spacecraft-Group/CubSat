#import the function sleep from the time module
from time import sleep

# print statements read like English, 
# just specify as a string what you would like to display
print("running hello world script:")

# to get user input, use the input function
# this will save whatever is typed in the command line
# to the variable name when the user presses enter
name = input("what is your name?\n")
# the backslash is used as an escape character in the string, 
# allowing \n to be interpreted not as two characters but as the 
# "new line" character, pushing the user's input area to the next line

# we can concatenate strings and variables containing strings
print("hello " + name + ", nice to meet you")

delay = input("how long would you like to wait between blinks?\n")

try:
	# since input() reads the input as a string, we must convert the string to 
	# an int so that we can use it in later functions
	delay = int(delay)
except:
	# if the user provides us with unexpected input that cannot be converted directly
	# into a string (i.e. input is not a number), stop the program before it breaks later
	print('sorry, "' + delay + \
		'" is not an acceptable delay, please input a numeric time delay')
	exit()

while True:
	print("Blink!")
	sleep(delay) # this function takes a time input in seconds