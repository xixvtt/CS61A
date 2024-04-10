"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    for p in paragraphs:
        # if select is true 
        if select(p):
            k -=1
        if k == -1:
            return p 
    return '' 

# ps = ['short', 'really long', 'tiny']
# s = lambda p: len(p) <= 5
# choose(ps, s, 0)

def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    def check_parag(parag):
        punc = '$#@&*"-+<>=()\'_!.'
        for ch in parag:
            if ch in punc:
                parag = parag.replace(ch, '')
        parag = parag.lower().split()

        for t in topic:
            if t in parag:
                return True 
        return False 
    return check_parag


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    correct_count = 0 

    if not typed_words:
        return 0.0
    
    for i in range(len(typed_words)):
        if i < len(reference_words) and typed_words[i] == reference_words[i]:
            correct_count +=1
    
    return (correct_count / len(typed_words)) * 100

    
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    # check te legth of typed, / 5 , check 60 / elaspe 
    if len(typed) == 0:
        return 0.0
    else:
        return (60 / elapsed) * (len(typed) / 5)
        
    # END PROBLEM 4

def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    closest_word = None
    smallest_diff = float('inf')
    # BEGIN PROBLEM 5
    # user_word in valid_words else -> run diff_func
    if user_word in valid_words:
        return user_word
    
    # looping through the valid words
    for word in valid_words:
        curr_diff = diff_function(user_word, word, limit)
        if curr_diff < smallest_diff:
            smallest_diff = curr_diff
            closest_word = word 
        if smallest_diff == 0: break 
    
    if smallest_diff > limit:
        return user_word
    else:
        return closest_word

def diff_function(user_word, word, limit):
    diff = abs(len(user_word) - len(word))

    for u, w in zip(user_word, word):
        if u != w:
            diff += 1
    # anycase all will return the num    
    return diff
    # END PROBLEM 5

# first_diff = lambda w1, w2, limit: 1 if w1[0] != w2[0] else 0
# autocorrect('inside', ['idea', 'inside'], first_diff, 1)

def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    
    # if one of the string is empty 
    if not start or not goal:
        return abs(len(start) - len(goal))
    
    # recursion 
    if start[0] == goal[0]:
        return shifty_shifts(start[1:], goal[1:], limit)
    # if differ 
    else:
        # max than limit
        if limit == 0:
            return limit + 1
        else:
            return 1+ shifty_shifts(start[1:], goal[1:], limit - 1)
    # END PROBLEM 6

# shifty_shifts('awful', 'awesome', 5)

def meowstake_matches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if limit < 0: # Fill in the condition
        return limit + 1

    if not start or not goal:
        return abs(len(start) - len(goal))
    
    if start[0] == goal[0]:
        return meowstake_matches(start[1:], goal[1:], limit)

    # three differ operations and check which op is the min step
    # check how many extra ch in goal we need to match 
    add_diff = 1 + meowstake_matches(start, goal[1:], limit - 1)
    remove_diff = 1 + meowstake_matches(start[1:], goal, limit - 1)
    substitute_diff = 1 + meowstake_matches(start[1:], goal[1:], limit - 1)

    return min(add_diff, remove_diff, substitute_diff)



def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    # first report_por func going to return the 100 correct word 
    correctness = 0
    for t, p in zip(typed, prompt):
        if t == p:
            correctness += 1
        else:
            break 
    
    progress = correctness / len(prompt)

    message = {'id': id, 'progress': progress}
    send(message)
    return progress
    # END PROBLEM 8
# print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
# typed = ['I', 'have', 'begun']
# prompt = ['I', 'have', 'begun', 'to', 'type']
# report_progress(typed, prompt, 1, print_progress)

def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    # times_per_p -> return 2D Array 
    
    # create player for each list 
    time_cost = [[] for _ in range(len(times_per_player))]

    for player_idx, player_time in enumerate(times_per_player):
        # time consume calc from idx 1
        for i in range(1, len(player_time)):
            time_consume = player_time[i] - player_time[i - 1]
            time_cost[player_idx].append(time_consume)
    return game(words, time_cost)
    # END PROBLEM 9

# p = [[0,2,3],[2,4,7]]
# game = time_per_word(p, ['hello', 'world'])


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    players = range(len(all_times(game)))  # An index for each player
    words = range(len(all_words(game)))    # An index for each word
    # BEGIN PROBLEM 10
    # create player slots 
    player_word_slot = [[] for _ in range(len(players))]
    
    for word_idx in words:
        # each word time  looping by each player in players 
        word_time = [time(game, player, word_idx) for player in players]

        faster_player = word_time.index(min(word_time))
        player_word_slot[faster_player].append(word_at(game, word_idx))

    return player_word_slot
    # return player_word_slot
    # END PROBLEM 10



def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]



def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = True  # Change to True when you
# p0 = [2, 2, 3]
# p1 = [6, 1, 3]
# fastest_words(game(['What', 'great', 'luck'], [p0, p1]))
# ##########################
# Extra Credit #
##########################

key_distance = get_key_distances()
def key_distance_diff(start, goal, limit):
    """ A diff function that takes into account the distances between keys when
    computing the difference score."""

    start = start.lower() #converts the string to lowercase
    goal = goal.lower() #converts the string to lowercase

    # BEGIN PROBLEM EC1
    "*** YOUR CODE HERE ***"
    # END PROBLEM EC1

def memo(f):
    """A memoization function as seen in John Denero's lecture on Growth"""

    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return memoized

key_distance_diff = count(key_distance_diff)


def faster_autocorrect(user_word, valid_words, diff_function, limit):
    """A memoized version of the autocorrect function implemented above."""

    # BEGIN PROBLEM EC2
    "*** YOUR CODE HERE ***"
    # END PROBLEM EC2


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)