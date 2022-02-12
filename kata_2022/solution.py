"""
This file is used as template for Google HashCode
Functions:
- solve():      given problem_instance returns a solution
- solve_all():  
------------------------------------------------------------

REPRESENTATION OF THE DATA:
problem_instance=(V,E,R,C,X,videos_size,endpoints)
where:
  endpoint_id-->(datacenter_lat, cache_servers, requests)
                                #cache_servers: server_id-->server_lat
                                #requests [(video_id,quantity),...]
  videos_size: video_id--->video_size

  solution: #[   (cache_id,[video_id1,....]),....  ]


V (1 ≤ V ≤ 10000) - t he n umber o f v ideos
● E (1 ≤ E ≤ 1000) - t he n umber o f e ndpoints
● R (1 ≤ R ≤ 1000000) - t he n umber o f r equest d escriptions
● C (1 ≤ C ≤ 1000) - t he n umber o f c ache s ervers
● X (1 ≤ X ≤ 500000) - t he c apacity o f e ach c ache s erver i n m egabytes


endpoint[endpoint_id][2][server_id]

"""


from io_simulate import * #import input/output/simulation functions
import glob         #used to get directories files

#solve the problem
def solve_random(problem_instance=None):
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

  solution=[]
  for cache_id in caches:
    solution.append((cache_id,caches[cache_id]))

  return solution
##################################################################


"""

videos={}   #video_id-->[quantity,size]
for each endpoint:
  for each request:
    add to videos[video_id], quantity
convert videos in list
sort by quanity




IDEA: 
for each video (sorted by decreasing quantity and increasing size):
  for each endpoint che lo richiede:
    
    sort caches connected to this enpoint by increasing latency

    if this video is already present in this cache, continue with next video
    if the video_size < remaining space in the cache:
      if the cache is more distant than the datacenter, break.
      put the video in the cache if there is space, 
    otherwise try with the next cache






IDEA2: 
for each video (sorted by decreasing quantity and increasing size):
  for each endpoint che lo richiede:
    
    sort caches connected to this enpoint by increasing latency

    if this video is already present in one of the caches of the endpoint, continue with next video
    if the video_size < remaining space in the cache:
      if the cache is more distant than the datacenter, break.
      put the video in the cache if there is space, 
    otherwise try with the next cache




"""

def solve_new(problem_instance=None):
  if not problem_instance:
    print("no problem given")
    return
  
  V,E,R,C,X,videos_size,endpoints=problem_instance

  #print(endpoints)

  #SORT videos by quantity,size
  videos={}
  for endpoint_id in endpoints:
    datacenter_lat, cache_servers,requests=endpoints[endpoint_id]
    for video_id,quantity in requests:
      if video_id not in videos: videos[video_id]=[0,0,set()] #quantity,size,requested by
      videos[video_id][0]+=quantity
      videos[video_id][1]=videos_size[video_id]
      videos[video_id][2].add(endpoint_id)
  videoss=[]
  for video_id in videos:
    quantity,size,requested_by=videos[video_id]
    videoss.append([quantity,size,video_id,requested_by])
  videos=videoss
  videos.sort(key=lambda x:(-x[0],x[1]))  #sort by quantity,size

  #print(videos)

  servers={}  #id--->(remaining_space,videos)
  #for each video
  for quantity,size,video_id,requested_by in videos:
    #for each endpoint che lo richiede
    for endpoint_id in requested_by:

      #sort caches connected to the enpoint by increasing latency
      caches=[] #[  (lat,cache_id),... ]      
      for cache_id in endpoints[endpoint_id][1]:
        lat=endpoints[endpoint_id][1][cache_id]
        caches.append((lat,cache_id))
      caches.sort(key=lambda x: x[0])

      
      
      #put the video in the cache if there is space, otherwise try with the next cache
      for lat,cache_id in caches:
        #if the cache is more distant than the datacenter, break.
        if lat>=endpoints[endpoint_id][0]: break

        #if there is no space in this cache, try with next one
        if cache_id not in servers:servers[cache_id]=[X,set()]
        if servers[cache_id][0]<size: continue

        #if this cache already contain this video: break
        if video_id in servers[cache_id][1]:break

        servers[cache_id][1].add(video_id)
        servers[cache_id][0]-=size
        break #this video is available for the current enpoint

  solution=[]
  print(servers)
  for cache_id in servers:
    remaining_size,videosss=servers[cache_id]
    videosss=list(videosss)
    if len(videos)>0:
      solution.append((cache_id,videosss))



  return solution


def solve_2(problem_instance=None):
  if not problem_instance:
    print("no problem given")
    return
  
  V,E,R,C,X,videos_size,endpoints=problem_instance

  #print(endpoints)

  #SORT videos by quantity,size
  videos={}
  for endpoint_id in endpoints:
    datacenter_lat, cache_servers,requests=endpoints[endpoint_id]
    for video_id,quantity in requests:
      if video_id not in videos: videos[video_id]=[0,0,set()] #quantity,size,requested by
      videos[video_id][0]+=quantity
      videos[video_id][1]=videos_size[video_id]
      videos[video_id][2].add(endpoint_id)
  videoss=[]
  for video_id in videos:
    quantity,size,requested_by=videos[video_id]
    videoss.append([quantity,size,video_id,requested_by])
  videos=videoss
  videos.sort(key=lambda x:(-x[0],x[1]))  #sort by quantity,size

  #print(videos)

  videos_seen={}  #endpoint_id--->set(video_id,...)

  servers={}  #id--->(remaining_space,videos)
  #for each video
  for quantity,size,video_id,requested_by in videos:
    #for each endpoint che lo richiede
    for endpoint_id in requested_by:

      if endpoint_id in videos_seen and video_id in videos_seen[endpoint_id]:
        continue

      #sort caches connected to the enpoint by increasing latency
      caches=[] #[  (lat,cache_id),... ]      
      for cache_id in endpoints[endpoint_id][1]:
        lat=endpoints[endpoint_id][1][cache_id]
        caches.append((lat,cache_id))
      caches.sort(key=lambda x: x[0])

      #put the video in the cache if there is space, otherwise try with the next cache
      for lat,cache_id in caches:
        #if the cache is more distant than the datacenter, break.
        if lat>=endpoints[endpoint_id][0]: break

        #if there is no space in this cache, try with next one
        if cache_id not in servers:servers[cache_id]=[X,set()]
        if servers[cache_id][0]<size: continue
        
        #
        if endpoint_id not in videos_seen:
          videos_seen[endpoint_id]=set()
        videos_seen[endpoint_id].add(video_id)

        #print(videos_seen)

        #if this cache already contain this video: break
        if video_id in servers[cache_id][1]:
          if endpoint_id not in videos_seen:videos_seen[endpoint_id]=set()
          videos_seen[endpoint_id].add(video_id)
          break

        servers[cache_id][1].add(video_id)
        servers[cache_id][0]-=size

        if endpoint_id not in videos_seen:videos_seen[endpoint_id]=set()
        videos_seen[endpoint_id].add(video_id)

        break #this video is available for the current enpoint

  solution=[]
  #print(servers)
  #print(videos_seen)
  for cache_id in servers:
    remaining_size,videosss=servers[cache_id]
    videosss=list(videosss)
    if len(videos)>0:
      solution.append((cache_id,videosss))



  return solution



#given a list of input files solve all
def solve_all(files=None,verbose=0):
  if not files:
    print("no files given")
    return -1
  
  print("Scores:")
  for filename in files:
    problem_instance=read_input_file(filename)
    solution=solve_random(problem_instance)
    score=simulate_solution(solution,problem_instance,verbose)

    print("\t",filename,score)


###################################################

#input files paths
files=glob.glob("data/*.in")

#solve 1 single problem
filename=files[1]
problem_instance=read_input_file(filename)
solution=solve_2(problem_instance)
#print(solution)
savefile="solutions/new_"+filename[5:-3]+".out"
save_solution(solution, savefile)

"""for filename in files[1:]:
  problem_instance=read_input_file(filename)
  solution=solve(problem_instance)
  print(filename)
  savefile="solutions/"+filename[5:-3]+".out"

  save_solution(solution, savefile)"""
#score=simulate_solution(solution,problem_instance,verbose=0)
#print(filename,score)

#solve all problems
#solve_all(files)
