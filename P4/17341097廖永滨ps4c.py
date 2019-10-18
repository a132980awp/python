# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx
import string
import copy
from ps4a import get_permutations

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


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        return copy.deepcopy(self.valid_words)
                
    def build_transpose_dict(self, vowels_permutation):
        dict_low = dict(zip(CONSONANTS_LOWER, CONSONANTS_LOWER))
        dict_high = dict(zip(CONSONANTS_UPPER, CONSONANTS_UPPER))
        dict_low_vowel = dict(zip(VOWELS_LOWER, vowels_permutation.lower()))
        dict_high_vowel = dict(zip(VOWELS_UPPER, vowels_permutation.upper()))
        dict_high.update(dict_low)  #合并
        dict_high.update(dict_low_vowel)
        dict_high.update(dict_high_vowel)
        return dict_high
    
    def apply_transpose(self, transpose_dict):
        symbols = " !@#$%^&*()-_+={}[]|\:;'<>?,./\""
        result = ''
        for letter in self.get_message_text():
            if letter in symbols:
                result = result + letter
            else:
                result = result + transpose_dict[letter]
        return result
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        # 获取映射字典
        perm_list = get_permutations(VOWELS_LOWER)
        # 最大合法单词数
        max_words = 0
        # 当前最好的匹配字符串
        best_msg = self.get_message_text()
        # 遍历每个组合
        for perm in perm_list:
            num = 0
            # 创建映射字典
            temp_transpose_dict = self.build_transpose_dict(perm)
            # 解密 - 反向加密
            temp = self.apply_transpose(temp_transpose_dict)
            # 字符串通过空格分割成单词组,同ps4b，只分割带空格的
            temp_list = temp.split()
            # 判断合法单词数
            for word in temp_list:
                if is_word(self.get_valid_words(), word):
                    num += 1
            # 如果合法单词数比当前多
            if num > max_words:
                max_words = num
                best_msg = temp
            # 如果合法单词数等于单词总数就退出
            if num == len(temp_list):
                break
        return best_msg
    

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE

    # Example test case
    message = SubMessage("aeiou")
    permutation = "iouea"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "iouea")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    # Example test case
    message = SubMessage("Good job!")
    permutation = "ieauo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Guud jub!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    # Example test case
    message = SubMessage("Sad is happy!")
    permutation = "ieauo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Sid as hippy!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

