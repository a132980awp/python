# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string
import os	#os库用来解决相对路径问题
from copy import deepcopy

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = (os.path.abspath(os.path.dirname(__file__))+"\\words.txt")

def load_words():

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):

    word = word.lower()                                 #规范大小写
    component1 = 0                                      #乘积的第一部分
    for letter in word:
        component1 += SCRABBLE_LETTER_VALUES.get(letter,0)   #component1 : 第一部分的分数，word各个字母对应分数之和
    word_len = len(word)                                #word_len : 单词长度
    component2 = 7*word_len - 3*(n-word_len)            #按公式计算出来的结果与1作比较，取较大值为乘积第二部分
    component2 = component2 if component2>1 else 1
    return component1*component2                        #返回乘积

def display_hand(hand):

    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):

    #由于不能修改原字典，所以要用深拷贝
    new_hand = deepcopy(hand)                   #用到 copy 库 要在顶部import
    word = word.lower()                         #规范大小写
    for letter in word:
        if new_hand.get(letter, 0) != 0:         #若a存在于newhand中
            if(new_hand[letter] > 0):
                new_hand[letter] -= 1           #则使对应的值减一

    #删去新hand中值为0的元素
    flag = True
    while(flag):
        flag = False
        for key in new_hand:
            if new_hand[key] == 0:
                del new_hand[key]
                flag = True
                break
    return new_hand


def is_valid_word(word, hand, word_list):
    #检测单词是否在词库中
    word = word.lower()
    cnt = 0
    if '*' in word:                                  #当输入有'*'时
        flag = 1
        for letter in "aeiou":                       #将'*'分别换成五个元音字母，若对应的五个单词都不存在则返回False
            word_x = word.replace('*', letter)
            if word_x in word_list:
                flag = 0
        if flag:
            return False
    else:                                            #当输入无'*'时
        if word not in word_list:                    #如果单词不存在，则返回False
            return False
    #检测单词是否在对应hand中
    temp_hand = deepcopy(hand)                       #用深拷贝
    for letter in word:                              #对于word的每一个字母
        if temp_hand.get(letter,0) == 0:             #如果hand中无这个字母，则返回False
            return False
        else:                                        #如果有这个字母，则其在字典中的值减一
            temp_hand[letter] = temp_hand[letter] - 1
            if temp_hand[letter] < 0:
                return False
    return True


def calculate_handlen(hand):

    ans = 0
    for letter in hand.values():
        ans += letter
    return ans

def play_hand(hand, word_list):
    # Keep track of the total score
    total_score = 0
    # As long as there are still letters left in the hand:
    while (calculate_handlen(hand) > 0):
        # Display the hand
        print("Current hand: ", end=' ')
        display_hand(hand)
        # Ask user for input
        input_word = input("Enter word, or \"!!\" to indicate that you are finished: ")
        # If the input is two exclamation points:
        if input_word == "!!":
            # End the game (break out of the loop)
            break
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(input_word, hand, word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                earned_score = get_word_score(input_word,calculate_handlen(hand))
                total_score += earned_score
                print("\""+input_word+"\" earned "+str(earned_score)+" points. Total: "+str(total_score)+" points ")
            else:
                # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word .")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, input_word)
    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if calculate_handlen(hand) <= 0:
        print("Ran out of letters")
    print("Total score for this hand:  %d point " % total_score)
    print("--------------")
    # Return the total score as result of function
    return total_score

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):

    if letter not in hand:                          #如果想替换的字母不存于hand中，则不进行操作
        return hand
    n = hand[letter]                                #得到这个字母的数量
    list_temp = []                                  #创建一个可替换的字母表
    for k in "abcdefghijklmnopqrstuvwxyz":
        if k not in hand:                      #在字母表中但不在hand中
            list_temp.append(k)
    new_letter = random.choice(list_temp)
    del hand[letter]                                #删去被替换字母
    hand.update({new_letter: n})                    #加入新字母
    return hand
       
    
def play_game(word_list):
    hands_num = int(input("Enter total number of hands: "))
    total_score = 0
    while(hands_num > 0):
        hand = deal_hand(HAND_SIZE)
        t = 0                 #当前手牌到现在总共玩的次数
        score = 0             #当前手牌所取得的最高分
        hand_temp = deepcopy(hand)
        while(1):
            print("Current hand: ", end='')
            display_hand(hand_temp)
            if t == 0:              #只有第一次能换单词
                tmp = input("Would you like to substitute a letter?")
                if tmp.lower() == "yes":
                    replaced_letter = input("Which letter would you like to replace:")
                    substitute_hand(hand_temp, replaced_letter)
            score_new = play_hand(hand_temp, word_list)
            score = score if score > score_new else score_new   #如果再一次玩分数更高则取更高
            t += 1
            if t > 1:                  #一副手牌最多能玩的次数 <= 1
                break
            tmp = input("Would you like to replay the hand? ")
            if tmp.lower() != "yes":
                break
        total_score += score
        hands_num -= 1
    print("Total score over all hands: "+str(total_score)+" point")

# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
