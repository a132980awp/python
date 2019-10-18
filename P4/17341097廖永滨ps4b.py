# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
import copy
### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        #由于strings对象不可变，可以不拷贝直接返回
        return self.message_text

    def get_valid_words(self):
        #深拷贝副本保护源列表
        return copy.deepcopy(self.valid_words)

    def build_shift_dict(self, shift):
        dict_low = dict(zip(string.ascii_lowercase, string.ascii_lowercase[shift:] + string.ascii_lowercase[:shift]))
        dict_high = dict(zip(string.ascii_uppercase, string.ascii_uppercase[shift:] + string.ascii_uppercase[:shift]))
        dict_high.update(dict_low)  #合并
        return dict_high

    def apply_shift(self, shift):
        # 利用self.build_shift_dict方法得到映射字典
        dict_map = self.build_shift_dict(shift)
        # 题目要求忽略的标点符号
        symbols = " !@#$%^&*()-_+={}[]|\:;'<>?,./\""
        # 根据偏移获取要求的加密字符串，特殊符号不偏移
        result = ''
        for letter in self.get_message_text():
            if letter in symbols:
                result = result + letter    #直接拼接
            else:
                result = result + dict_map[letter]  #偏移后拼接
        return result

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        #继承的父类要进行初始化
        Message.__init__(self, text)
        #偏移量
        self.shift = shift
        # 调用继承来的build_shift_dict函数得到映射表
        self.encryption_dict = self.build_shift_dict(shift)
        # 调用继承来apply_shift得到加密后的字符串
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        return shift

    def get_encryption_dict(self):
        #深拷贝保护源字典
        return copy.deepcopy(self.encryption_dict)

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        #利用修改后的shift重新初始化类对象
        self.__init__(self.get_message_text(), shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text)

    def decrypt_message(self):
        # 最好的偏移量
        best_shift = 0
        # 最多合法的单词数
        max_words = 0
        # 解密后最好的字符串
        best_msg = ''
        # 遍历0-25个偏移量
        for i in range(26):
            num = 0             #偏移i单位的匹配单词数
            temp = self.apply_shift(i)  #偏移i单位的解密字符串
            '''
            将所有单词都分割出来，此处只处理正常语法的message，也就是词与词之间必有空格
            若要将类似 hello，world 这种词与词之间没有空格而只有标点符号的字符串需要import re，用re里的方法，此处不考虑这种情况
            '''
            temp_list = temp.split()
            # 计算合法单词数
            for word in temp_list:
                if is_word(self.get_valid_words(), word):
                    num += 1
            # 如果这个偏移量得到的单词数，比当前最大的还大就改变
            if num > max_words:
                max_words = num
                best_shift = i
                best_msg = temp

            # 如果合法单词数等于全部单词数，直接返回
            if num == len(temp_list):
                break

        return (best_shift, best_msg)

if __name__ == '__main__':
#    #Example test case (PlaintextMessage)
     test ="abc,bcd,efg!aaa sss"
     plaintext = PlaintextMessage('hello', 2)
     print('Expected Output: jgnnq')
     print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
     ciphertext = CiphertextMessage('jgnnq')  #正确语法下，词与词之间必有空格
     print('Expected Output:', (24, 'hello'))
     print('Actual Output:', ciphertext.decrypt_message())

# Example test case (PlaintextMessage)
     plaintext = PlaintextMessage('I am very happy', 2)
     print('Expected Output: K co xgta jcrra')
     print('Actual Output:', plaintext.get_message_text_encrypted())
     # Example test case (CiphertextMessage)
     ciphertext = CiphertextMessage('K co xgta jcrra')
     print('Expected Output:', (24, 'I am very happy'))
     print('Actual Output:', ciphertext.decrypt_message())
     # Example test case (PlaintextMessage)
     plaintext = PlaintextMessage('I am so sad', 10)
     print('Expected Output: S kw cy ckn')
     print('Actual Output:', plaintext.get_message_text_encrypted())
     # Example test case (CiphertextMessage)
     ciphertext = CiphertextMessage('S kw cy ckn')
     print('Expected Output:', (16, 'I am so sad'))
     print('Actual Output:', ciphertext.decrypt_message())

     #TODO: WRITE YOUR TEST CASES HERE

    #TODO: best shift value and unencrypted story 
    

