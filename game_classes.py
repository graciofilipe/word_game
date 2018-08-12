from load_dictionary import return_words
from aux_functions import is_only_letters, has_no_duplicate_letter, does_not_end_with_s, \
                          word_to_list_of_bools
from ortools.sat.python import cp_model
from string import ascii_letters as letters
from solver_aux import SolutionPrinter
from collections import defaultdict

lower_case_letters = letters[:26]




class WordGame:

    def __init__(self, word_list, length_of_word):

        self.length_of_word = length_of_word

        # words of the right lenght
        length_filtered_words = [w for w in word_list if len(w) == length_of_word]

        # words that only have letters
        filtered_words = filter(is_only_letters, length_filtered_words)

        # words that have no duplicates
        filtered_words = filter(has_no_duplicate_letter, filtered_words)

        # words that do not end with s
        filtered_words = filter(does_not_end_with_s, filtered_words)

        self.words = list(set(list(filtered_words)))
        self.words.sort()
        self.n_initial_words = len(self.words)


        ## create a dictionary mapping between bools and words
        bool_to_list_of_words = defaultdict(list)
        for word in self.words:
            bool_word = tuple(word_to_list_of_bools(word))
            bool_to_list_of_words[bool_word].append(word)
        self.bool_to_list_of_words = bool_to_list_of_words


        # SOLVER AND CONSTRAINTS #
        model = cp_model.CpModel()
        solver = cp_model.CpSolver()
        self.model = model
        self.solver = solver

        # the main variable
        word_solver_var = [self.model.NewIntVar(0, 1, 'letter_{i}'.format(i=lower_case_letters[i])) for i in range(26)]
        self.word_solver_var = word_solver_var

        # Initial constraints
        self.model.AddSumConstraint(word_solver_var, lb=length_of_word, ub=length_of_word)

        # is in list of words constraint
        list_of_words_in_bool = [word_to_list_of_bools(word) for word in self.words]
        self.model.AddAllowedAssignments(self.word_solver_var, list_of_words_in_bool)



    def add_constraint(self, guess_word, number_of_overlapping_letters):
        guess_word_bool = word_to_list_of_bools(guess_word)
        idxs = [i for i in range(len(lower_case_letters)) if guess_word_bool[i]==1]
        self.model.AddSumConstraint([self.word_solver_var[idx] for idx in idxs],
                                    lb=number_of_overlapping_letters, ub=number_of_overlapping_letters)


    def solve(self):
        solution_printer = SolutionPrinter(self.word_solver_var, self.bool_to_list_of_words)
        status = self.solver.SearchForAllSolutions(self.model, solution_printer)
        self.status = status
        print('\nNumber of solutions found: %i' % solution_printer.SolutionCount())


w = return_words()
w1 = WordGame(w, 5)
w1.add_constraint('virus', 2)
w1.add_constraint('watch', 1)
w1.add_constraint('plant', 2)
w1.add_constraint('swing', 1)
w1.add_constraint('bring', 1)
w1.add_constraint('brine', 2)
w1.add_constraint('crime', 2)
w1.add_constraint('water', 3)








w1.solve()

print('fuck off')
print(w1.words[:10])
print(w1.n_initial_words)