"""
This file is used as template for Google HashCode
Functions:
- solve():      given problem_instance returns a solution
- solve_all():  
------------------------------------------------------------

REPRESENTATION OF THE DATA:
...



"""


from io_simulate import * #import input/output/simulation functions
import glob         #used to get directories files

#solve the problem
def solve(problem_instance=None):
  if not problem_instance:
    print("no problem given")
    return
  
  #...COMPLETE...
  solution=[0]
  #...COMPLETE...

  return solution


#given a list of input files solve all
def solve_all(files=None,verbose=0):
  if not files:
    print("no files given")
    return -1
  
  print("Scores:")
  for filename in files:
    problem_instance=read_input_file(filename)
    solution=solve(problem_instance)
    score=simulate_solution(solution,problem_instance,verbose)

    print("\t",filename,score)


###################################################

#input files paths
files=glob.glob("*.txt")

#solve 1 single problem
filename=files[0]
problem_instance=read_input_file(filename)
solution=solve(problem_instance)
score=simulate_solution(solution,problem_instance,verbose=0)
print(filename,score)

#solve all problems
#solve_all(files)
