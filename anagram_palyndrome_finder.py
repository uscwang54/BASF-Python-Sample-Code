# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 10:01:34 2022

@author: Yu Wang
"""

from itertools import permutations
import requests
from bs4 import BeautifulSoup
import string
from collections import defaultdict

class StringParent:
    
    def __init__(self, existing=""):
        self.existing = existing
    
    def __str__(self):
        return self.existing
    
    def append(self, new):
        self.existing += new
        return self.existing
    
    def remove(self, substring):
        self.existing = self.existing.replace(substring, "")
        return self.existing
    
    def mirror(self):
        self.existing = self.existing[::-1]
        return self.existing
    
    def load_from_file(self, file_path):
        with open(file_path, "r") as f:
            content = f.read()
            self.existing = content
    
    def save_to_file(self, file_path):
        with open(file_path, "w") as f:
            f.write(self.existing)

class Anagram(StringParent):
    
    def anagrams(self):
        all_anagrams = []
        for perm in permutations(self.existing):
            all_anagrams.append("".join(perm))
        return all_anagrams
    
class Palindrome(StringParent):
    
    def __init__(self):
        self.palindromes = []
    
    def isPalindrome(self, new):
        return new == new[::-1]
    
    def storePalindrome(self, new):
        if self.isPalindrome(new):
            self.palindromes.append(new)
        return self.palindromes
    
def anagram_palyndrome_finder(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    text = soup.text
    punctuations = string.punctuation
    clean_text = text.translate(str.maketrans('', '', punctuations))
    words = clean_text.split()
    
    palyndrome_set = set()
    for word in words:
        if word==word[::-1] and len(word)>1:
            palyndrome_set.add(word)
    print("Palyndromes:")
    for word in palyndrome_set:
        print(word)
    print()
    
    word_ordsum = {}
    for word in words:
        ordsum = 0
        for char in word:
            ordsum += ord(char)
        word_ordsum[word] = ordsum
    
    ordsum_word = defaultdict(set)    
    for ordsum1 in word_ordsum.values():
        for word, ordsum2 in word_ordsum.items():
            if ordsum1 == ordsum2:
                ordsum_word[ordsum1].add(word)
                
    print("Anagrams:")
    for ordsum, word_set in ordsum_word.items():
        if len(word_set)>1:
            for word1 in word_set:
                if len(word1)<10: #limit of the length of the word
                    anagrams = Anagram(word1).anagrams()
                    for word2 in word_set:
                        if word2 in anagrams and word2!=word1:
                            print(f"{word1}<->{word2}")