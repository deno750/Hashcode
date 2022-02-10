"""
Task: Given the description of a city plan and planned paths for all cars in that city,
optimize the schedule of traffic lights to minimize the total amount of time spent in
traffic, and help as many cars as possible reach their destination before a given
deadline.

The city plan consists of one-way streets and intersections.

Each street:
● is identified by a unique name,
● leads from one i ntersection to another,
● does not contain any intersections in between (if two streets need to cross
outside an intersection, a bridge or tunnel is used),
● has a fixed amount of time L it takes a car to get from the beginning of the
street to the end. If it takes L seconds to drive through a street and a car
enters it at time T it will arrive at the end of the street precisely at T+L,
independently of how many cars are on the street.

there will never be two streets connecting two i ntersections in the same direction.

Each intersection:
● has a unique i nteger ID (for example 0, 1, 2 ...),
● has at least one street that comes into it, and at least one street coming out of it.

traffic light at the end of every street (just before the intersection).
Each traffic light has two states: green and red

At most one traffic light will be green at each i ntersection at any given time.
While the light is green for an incoming street,
only cars from this street will be allowed to enter the intersection

Queuing up: When the light at the end of a street is red, arriving cars queue up waiting for the
light to turn green. When the light is green, one car can cross the intersection
every second.

Schedule For each intersection: determines the order and duration of green light 
for the incoming streets of the intersection and repeats i tself until the end of the simulation.
The schedule is a list of pairs: incoming street and duration.
Each street can appear at most once in the schedule.
The schedule can ignore some of the incoming streets, those will never get a green light.
By default all lights on all intersections are red.

Each car is described by the path (a sequence of streets) it is going to drive through.
The paths are defined by the input datasets and can't be altered.
we guarantee that each car can go through a single intersection at most once.

Initially, all cars start at the end of the first street in their path,
waiting for the green light (in case the traffic light is red), or ready to move (if it's green).
If two cars starts at the end of the same street, the car listed first in the input file goes first.
Each car then follows a given path, while obeying the traffic lights, and needs to reach the
end of the last street in that path.
When a car enters the last street of its path, it completes its drive until the end of
the street and then is immediately removed from it.


if a car finishes at time T it scores
F + (D - T) points

score for the solution is the sum of scores for all cars.


"""


import glob         #used to get directories files


#read input
def read_input_file(filename):
  f = open(filename, "r")
  D,I,S,V,F=list(map(int,f.readline().strip().split()))

  #read streets
  streets={}  #name -> [id_beg,id_end,lenght]
  for _ in range(S):
    street=f.readline().strip().split(" ")
    B=int(street[0])  #id of the intersection beginning
    E=int(street[1])  #id or intersection end
    name=street[2]
    L=int(street[3])  #lenght in seconds
    streets[name]=[B,E,L]

  #cars' paths
  cars=[]
  for _ in range(V):
    cars.append(f.readline().strip().split(" ")[1:])

  f.close()

  return (D,I,S,V,F,streets,cars)


#Check if the input is readed correctly
def print_input(problem_instance):
  D,I,S,V,F,streets,cars=problem_instance
  
  print(D,I,S,V,F)
  for s in streets:
    print(s,streets[s])
  for p in cars:
    print(p)

  return


#solution= [ [id_inter, [(name,green_time),(name2,green_time2,...)]], ...  ]
def print_problem_instance(intersections):
  A=len(intersections)#num_intersections
  print(A)

  for id_inter in intersections:
    incoming_streets=intersections[id_inter]
    num_incoming_streets=len(incoming_streets)
    print(id_inter)
    print(num_incoming_streets)
    for name,green_time in incoming_streets:
      print(name+" "+str(green_time))


def save_solution(solution=None,filename=None):
  if not solution or not filename:return
  
  f = open(filename, "w")

  intersections=solution
  A=len(intersections)#num_intersections
  f.write(str(A)+"\n")

  for id_inter in intersections:
    incoming_streets=intersections[id_inter]
    num_incoming_streets=str(len(incoming_streets))
    f.write(str(id_inter)+"\n")
    f.write(str(num_incoming_streets)+"\n")
    for name,green_time in incoming_streets:
      f.write(name+" "+str(green_time)+"\n")
  
  f.close()


def read_solution_file(filename):
  f = open(filename, "r")

  A=int(f.readline().strip()) #num_intersections

  intersections={}
  for _ in range(A):
    id_inter=int(f.readline().strip())
    num_incoming_streets=int(f.readline().strip())

    for _ in range(num_incoming_streets):
      #....
      pass


  f.close()
  return intersections

#simulate the solution and return the score
#simulate the solution and return the score
def simulate_solution(solution=None,problem_instance=None,verbose=0):
  if not solution:
    print("empty soluton")
    return
  if not problem_instance:
    print("no problem given")
    return

  #execute solution on given input file
  D,I,S,V,F,streets,cars=problem_instance
  intersections=solution

  score=0
  
  #inter

  #for t in range(D):



  return score

#given a list of input files and
def simulate_all(solution=None,files=None,verbose=0):
  if not solution:
    print("empty solution")
    return -1
  if not files:
    print("no files given")
    return -1
  
  print("Scores:")
  for filename in files:
    print("\t",filename,simulate_solution(solution,filename,verbose))



def solve(problem_instance=None):
  if not problem_instance:
    print_input("no problem given")
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

  return


########################################################################
"""filename="a.txt"
problem_instance=read_input_file(filename)
print_input(problem_instance)"""


ex_solution={1:[("rue-d-athenes",2),("rue-d-amsterdam",1)],
              0:[("rue-de-londres",2)],
              2:[("rue-de-moscou",1)]}
#print_problem_instance()
save_solution(ex_solution,"egs.txt")


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



"""


for each timstamp=0...D:
  remember for each intersection the queue of cars and lights

inter[ingoing]=[(street_name, queue),...]
                              queue=[(car_id,timestamp_end)]
                              a car can pass if it has timestamp<=curr_timestamp
inter[outgoing]=(street_name, ...)
inter[lights]

"""