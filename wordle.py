import numpy as np
import pandas as pd

def check(guess, true):
    """
    Gives wordle output based on guess

    Parameters
    ----------
    guess : str
        guessed word to be tested
    true  : str
        true word to be checked against

    Returns
    -------
    5 character string of some combination of B, Y, G (black, yellow, green)
    """
    output=np.array(list('BBBBB'))
    occurrences_true  = {letter:true.count(letter) for letter in set(true)}
    GY_guess = {letter:0 for letter in set(guess)}
    for i, guess_letter in enumerate(guess):
        # First past to decide which letters are green
        if guess_letter == true[i]:
            GY_guess[guess_letter] += 1
            output[i]='G'
    for i, guess_letter in enumerate(guess):
        # Second pass to decide which letters are yellow
        if output[i] != 'G':
            if (guess_letter in true):
                if (GY_guess[guess_letter] < occurrences_true[guess_letter]): # cannot combine both if statements because guess letter may not occur in occurences_true
                    GY_guess[guess_letter] += 1
                    output[i] = 'Y'
            else:
                output[i] = 'B'
    return output[0]+output[1]+output[2]+output[3]+output[4]

class wordle_solver():
    """
    Class to provid the best guesses for Wordle
    """
    def __init__(self):
        self.valid_words = np.loadtxt('valid_guesses.txt', dtype='str')
#         self.valid_words = np.loadtxt('wordles.txt', dtype='str')
        self.wordles = self.valid_words # a current list of possible wordles given guesses and outputs
        
    def update_possible_wordles(self, guess, output):
        """
        Reduce the possible wordles given the output of a guess

        Parameters
        ----------
        guess : str
            guessed word
        output : str
            output from Wordle for the given guess
        """
        test = np.zeros(shape=(len(self.wordles)),dtype='<U5')
        for i, word in enumerate(self.wordles):
            test[i] = check(guess,word)
        df = pd.DataFrame(data={'word':self.wordles,'output':test}, dtype='<U5').set_index('word')
        self.wordles = df[df['output']==output].index.values
        print('-'*20+f'\n{len(self.wordles)} possible wordles:')
        print(self.wordles)
        print('-'*20)
        
    def calculate_std(self):
        """
        Calculate and display the top 5 best next guesses. Lower std corresponds to a better guess.
        """
        std = []
        for j, word1 in enumerate(self.wordles):   
            test = np.zeros(shape=(len(self.wordles)), dtype='<U5')
            for i, word2 in enumerate(self.wordles):
                test[i] = check(word1,word2)
            df = pd.DataFrame(test, columns = ['output'], dtype='<U5')
            a = df.groupby('output').size()
            combinations = pd.read_csv('combinations.txt', names=['output'], index_col = 0, squeeze=True)
            combinations['counts']=0
            combinations.loc[a.index, 'counts'] = a.values
            std.append(combinations.std()[0]) # correct std
        
        standard_dev = pd.DataFrame(data={'words':self.wordles,'std':std}).sort_values('std', ignore_index=True)
        best_word = standard_dev.loc[0,'words']
        print('Best next guess:\n'+'-'*20)
        print(standard_dev.head())
        print('-'*20)
        return best_word
        
ws = wordle_solver()

for i in range(1,6):
    guess = input(f'Guess {i}:')
    output = input(f'Output {i}:')
    ws.update_possible_wordles(guess, output)
    ws.calculate_std()