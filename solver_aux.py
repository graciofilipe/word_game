from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self, variables, bool_to_list_of_words):
    self.__variables = variables
    self.__solution_count = 0
    self.bool_to_list_of_words = bool_to_list_of_words

  def NewSolution(self):
    self.__solution_count += 1
    bool_word = tuple([self.Value(v) for v in self.__variables])
    print(self.bool_to_list_of_words[bool_word])

  def SolutionCount(self):
    return self.__solution_count