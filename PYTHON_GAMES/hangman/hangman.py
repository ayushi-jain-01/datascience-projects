import random

words = ["hangman","hello","useful","abcdeffg","nopes","important"]

stages = [
    '''
    +--+
    |  |
       |
       |
       |
       |

    ****
    ''',

    '''
    +--+
    |  |
    0   |
       |
       |
       |

    ****
    ''',
    
    '''
    +--+
    |  |
    0   |
    |   |
       |
       |

    ****
    ''',
    
    '''
    +--+
    |  |
    0   |
   /|   |
       |
       |

    ****
    ''',
        
    '''
    +--+
    |  |
    0   |
   /|\\  |
       |
       |

    ****
    ''',
            
    '''
    +--+
    |  |
    0   |
   /|\\  |
   /    |
       |

    ****
    ''',
                
    '''
    +--+
    |  |
    0   |
   /|\\  |
   / \\  |
       |

    ****
    ''',
]

user_word = random.choice(words)
hidden_words = ["_"]*len(user_word)
lives = 6

print("HANGMAN GAME")

while lives>0:

    print(" ".join(hidden_words))
    guess = input("Guess a letter: ")

    if guess in user_word:
        for i in range(len(user_word)):
            if user_word[i] ==  guess:
                hidden_words[i] = guess
                print("Correct Guess!")
    else:
        lives -=1
        print("WRONG GUESS! Lives left: ",lives)
        print(stages[6-lives])
    
    if "_" not in hidden_words:
        print("YOU WON! Word: ",user_word)
        break

else:
    print("YOU LOST! Word: ",user_word)      