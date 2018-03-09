# 6.00 Problem Set 3A Solutions
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
#

import random
import string
from perm import *

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

	The score for a word is the sum of the points for letters
	in the word multiplied by the length of the word, plus 50
	points if all n letters are used on the first go.

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    score = 0
    for letter in word:
        score += SCRABBLE_LETTER_VALUES[letter]
    score *= len(word)
    score += 50 if (len(word) == n) else 0
    return score
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                            # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
	In other words, this assumes that however many times
	a letter appears in 'word', 'hand' has at least as
	many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()
    for letter in word:
        new_hand[letter] -= 1
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """

    if (word not in word_list):
        return False
    for letter in word:
        if (not hand.has_key(letter)):
            return False
    new_hand = update_hand(hand, word)
    for value in new_hand.values():
        if (value < 0):
            return False
    return True

def calculate_handlen(hand):
    handlen = 0
    for v in hand.values():
        handlen += v
    return handlen

def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    possible_word = '.'
    possible_word_score = 0
    for i in range(HAND_SIZE + 1, 2, -1):
        perms = get_perms(hand, i)
        for word in perms:
            if (word in word_list):
                word_score = get_word_score(word, HAND_SIZE)
                if (word_score > possible_word_score):
                    possible_word = word
                    possible_word_score = word_score
    if possible_word != '.':
        print possible_word
    return possible_word

#
# Problem #4: Playing a hand
#
def play_hand(hand, word_list, score, computer):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      score: integer
      computer: boolean
      
    """
    word = ''
    while(calculate_handlen(hand) > 0 and word != '.'):
        if (computer):
            word = comp_choose_word(hand, word_list)
        else:
            word = hand_prompt(hand)
        if (is_valid_word(word, hand, word_list)):
            word_score = get_word_score(word, HAND_SIZE)
            score += word_score
            hand = update_hand(hand, word)
            if (computer):
                print('The computer scored ' + str(word_score) + ' points.')
                print('The computer\'s total score is ' + str(score) + ' points.')
            else:
                print('Excellent! You scored ' + str(word_score) + ' points.')
                print('Your total score is ' + str(score) + ' points.')
        elif (word != '.'):
            print('That is not a valid word.')
    return score
        
def hand_prompt(hand):
    print('\nHere is your current hand: ')
    display_hand(hand)
    return raw_input('Enter a word> ')
#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    option = 'n'
    score = 0
    comp_score = 0
    hand = deal_hand(HAND_SIZE)
    while (option != 'e'):
        option = start_prompt()
        if (option == 'n'):
            hand = deal_hand(HAND_SIZE)
        elif (option == 'r'):
            None
        elif (option == 'e'):
            break
        else:
            option = start_prompt
        option = next_prompt()
        if (option == 'u'):
            score = play_hand(hand, word_list, score, False)
        elif (option == 'c'):
            comp_score = play_hand(hand, word_list, comp_score, True)
        elif (option == 'e'):
            break
        else:
            option = next_prompt()
    print('\nThank you for playing. Your final score is ' + str(score))
    print('The computer\'s final score is ' + str(comp_score) + '\n')
    
def start_prompt():
    print('\n')
    print('Please input one of the following options:\n')
    print('\tn: Play a new random hand\n')
    print('\tr: Play the last hand again\n')
    print('\te: Exit the game\n')
    return raw_input('> ')

def next_prompt():
    print
    print('Please input one of the following options:\n')
    print('\tu: You play the hand\n')
    print('\tc: The computer plays the hand\n')
    print('\te: Exit the game\n')
    return raw_input('> ')
    
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)