# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
import os	#os库用来解决相对路径问题

WORDLIST_FILENAME = (os.path.abspath(os.path.dirname(__file__))+"\\words.txt")
#要求单词表文件 words.txt与.py在同一个目录


def load_words():

	print("Loading word list from file...")
	# inFile: file
	inFile = open(WORDLIST_FILENAME, 'r')
	# line: string
	line = inFile.readline()
	# wordlist: list of strings
	wordlist = line.split()
	print("  ", len(wordlist), "words loaded.")
	return wordlist



def choose_word(wordlist):

	return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
	#对于选择的单词，如果每个字母都已经被猜中则返回True
	for letter in secret_word:
		if letter not in letters_guessed:
			return False
	return True



def get_guessed_word(secret_word, letters_guessed):
	#先创建一个字符串并赋值为选择的词
	guessed_word = secret_word
	for i in guessed_word :
		if i not in letters_guessed:
			guessed_word = guessed_word.replace(i,"_ ")
			#对于未被猜中的字母则用_替代
	return guessed_word



def get_available_letters(letters_guessed):
	#创建一个字母表
	available_letters = string.ascii_lowercase
	for i in available_letters:
		if i in letters_guessed:
			available_letters = available_letters.replace(i,'')
			#已经被猜测过的字母在表中剔除
	return available_letters


def hangman(secret_word):

	#初始化一些关键变量
	guesses_remaining = 6
	warnings_remaining = 3
	unique_letters = 0		#字符串中不同的字母个数
	letters_guessed = []
	flag_win = False
	
	print("Welcome to the game Hangman!")
	print("I am thinking the of a word that is "+str(len(secret_word))+" letters long.")
	print("You have "+str(warnings_remaining)+" warnings left.")
	while(guesses_remaining > 0 and not flag_win):
	#继续条件：还有机会 且 还没赢
		print("----------------------------------")
		print("You have "+str(guesses_remaining)+" guesses left")
		print("Available letters: "+get_available_letters(letters_guessed))
		letter_guessed = input("Please guess a letter: ")
		if len(letter_guessed)!=1 or letter_guessed not in get_available_letters(letters_guessed):
		#如果出现非法输入则：（如果不是一个字符也认为是非法输入）
			if warnings_remaining > 0:
				warnings_remaining -= 1
				if len(letter_guessed)!=1:
					print("Oops! You need to input only a letter. You now have "+str(warnings_remaining)+" warnings: ")
				else:
					print("Oops! You've already guessed that letter. You now have "+str(warnings_remaining)+" warnings: ")
				print(get_guessed_word(secret_word, letters_guessed))
				#扣减警告次数
			else:
				print("Oops! You've already guessed that letter. You have no warnings left")				
				guesses_remaining -= 1
				print("so you lose one guess: "+get_guessed_word(secret_word, letters_guessed))
				#扣减猜测次数
			continue
		letters_guessed.append(letter_guessed)
		if letter_guessed in secret_word:
			print("Good guess!: "+get_guessed_word(secret_word, letters_guessed))
			unique_letters += 1
			#猜对了的话，所选字符串不同的字母数+1（因为需要猜对的次数等于所选择的字符串不同字母的个数）
		else:
			print("Oops! That letter is not in my word: "+get_guessed_word(secret_word, letters_guessed))
			if letter_guessed in ['a','e','i','o']:
				guesses_remaining -= 1	#部分元音字母多扣1次机会
			guesses_remaining -= 1
		flag_win = is_word_guessed(secret_word, letters_guessed)
		#判断胜负
	Total_score = guesses_remaining* unique_letters
	if(flag_win):
		print("Congratulations, you won!")
		print("Your total score for this game is: "+str(Total_score ))
		#胜利则出分数
	else:
		print("Sorry, you ran out of guesses. The word was "+str(secret_word))


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
	myword_not_b = my_word.replace(' ','')
	#将被_屏蔽的字符串中的空格全部剔除
	if(len(myword_not_b) != len(other_word)):
		#如果两个词长度不一样就一定不同
		return False
	for i in range(len(myword_not_b)):
		if myword_not_b[i] != '_' and myword_not_b[i] != other_word[i]:
		#出现除_外不同的字母时说明两个词不匹配
			return False
	return True



def show_possible_matches(my_word):
	matches_flag = False
	for word in wordlist:
		if match_with_gaps(my_word,word):
		#根据匹配函数在字典中找到匹配的单词打印出来
			print(word,end='')
			print(" ",end='')
			matches_flag = True
	if not matches_flag:
		print("No matches found")
	else:
		print("")



def hangman_with_hints(secret_word):
	#同hangman()，增设*判断
	guesses_remaining = 6
	warnings_remaining = 3
	unique_letters = 0
	letters_guessed = []
	flag_win = False
	
	print("Welcome to the game Hangman!")
	print("I am thinking the of a word that is "+str(len(secret_word))+" letters long.")
	print("You have "+str(warnings_remaining)+" warnings left.")
	while(guesses_remaining > 0 and not flag_win):
		print("----------------------------------")
		print("You have "+str(guesses_remaining)+" guesses left")
		print("Available letters: "+get_available_letters(letters_guessed))
		letter_guessed = input("Please guess a letter: ")
		if letter_guessed == '*':
		# * 判断，如果文件输入了*，则展示所有匹配的单词
			print("Possible word matches are: ")
			show_possible_matches(get_guessed_word(secret_word, letters_guessed))
			continue
		if len(letter_guessed)!=1 or letter_guessed not in get_available_letters(letters_guessed):
			if warnings_remaining > 0:
				warnings_remaining -= 1
				if len(letter_guessed)!=1:
					print("Oops! You need to input only a letter. You now have "+str(warnings_remaining)+" warnings: ")
				else:
					print("Oops! You've already guessed that letter. You now have "+str(warnings_remaining)+" warnings: ")
				print(get_guessed_word(secret_word, letters_guessed))
			else:
				print("Oops! You've already guessed that letter. You have no warnings left")				
				guesses_remaining -= 1
				print("so you lose one guess: "+get_guessed_word(secret_word, letters_guessed))

			continue
		letters_guessed.append(letter_guessed)
		if letter_guessed in secret_word:
			print("Good guess!: "+get_guessed_word(secret_word, letters_guessed))
			unique_letters += 1
		else:
			print("Oops! That letter is not in my word: "+get_guessed_word(secret_word, letters_guessed))
			if letter_guessed in ['a','e','i','o']:
				guesses_remaining -= 1
			guesses_remaining -= 1
		flag_win = is_word_guessed(secret_word, letters_guessed)
	Total_score = guesses_remaining* unique_letters
	if(flag_win):
		print("Congratulations, you won!")
		print("Your total score for this game is: "+str(Total_score ))
	else:
		print("Sorry, you ran out of guesses. The word was "+str(secret_word))


	pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
	# pass

	# To test part 2, comment out the pass line above and
	# uncomment the following two lines.
	#show_possible_matches("t_ _ t")
	secret_word = choose_word(wordlist)
	mod = input("Which mod do you want to play?\n 0.hangman 1.hangman_with_hints\n")
	if(mod == '1'):#两种模式可以自行选择
		hangman_with_hints(secret_word)
	else:
		hangman(secret_word)

	#pass

###############

	# To test part 3 re-comment out the above lines and 
	# uncomment the following two lines. 
	
	#secret_word = choose_word(wordlist)
	#hangman_with_hints(secret_word)