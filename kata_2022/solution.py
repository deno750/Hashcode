"""
This file is used as template for Google HashCode
Functions:
- solve():      given problem_instance returns a solution
- solve_all():  
------------------------------------------------------------

REPRESENTATION OF THE DATA:
problem_instance=(V,E,R,C,X,videos_size,endpoints)
where:
  endpoint_id-->(datacenter_lat, cache_servers,requests)
                                #cache_servers: server_id-->server_lat
                                #requests [(video_id,quantity),...]
  videos_size: video_id--->video_size

  solution: #[   (cache_id,[video_id1,....]),....  ]


V (1 ≤ V ≤ 10000) - t he n umber o f v ideos
● E (1 ≤ E ≤ 1000) - t he n umber o f e ndpoints
● R (1 ≤ R ≤ 1000000) - t he n umber o f r equest d escriptions
● C (1 ≤ C ≤ 1000) - t he n umber o f c ache s ervers
● X (1 ≤ X ≤ 500000) - t he c apacity o f e ach c ache s erver i n m egabytes

"""


from io_simulate import * #import input/output/simulation functions
import glob         #used to get directories files

#solve the problem
def solve(problem_instance=None):
  if not problem_instance:
    print("no problem given")
    return
  
  V,E,R,C,X,videos_size,endpoints=problem_instance

  caches={} #cache_id-->[video_id1,....]
  for cache_id in range(C):
    space_remaining=X
    for video_id, size in enumerate(videos_size):
      if size<=space_remaining:
        if cache_id not in caches:caches[cache_id]=[]
        caches[cache_id].append(video_id)
        space_remaining-=size
      

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
files=glob.glob("data/*.txt")

#solve 1 single problem
filename=files[0]
problem_instance=read_input_file(filename)
solution=solve(problem_instance)
score=simulate_solution(solution,problem_instance,verbose=0)
print(filename,score)

#solve all problems
#solve_all(files)
