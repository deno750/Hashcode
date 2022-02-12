from math import degrees
from pydoc import cli
import random
import numpy as np
import threading

class Client:
    def __init__(self, liked, disliked):
        self.liked = liked
        self.disliked = disliked

##### FUNCTIONS #######

# A client comes to pizzeria only if all the ingredients they like are present and none of the ingredients they like are not present
def calculate_points(clients, ingredients_chosen):
    count = 0
    for client in clients:
        has_liked = [ing for ing in ingredients_chosen if ing in client.liked]
        has_not_disliked = [ing for ing in ingredients_chosen if ing in client.disliked]
        if len(has_liked) == len(client.liked) and len(has_not_disliked) == 0:
            count += 1
    return count

def write_output(file_name, selected_ingredients): 
    with open(f"./output/{file_name}.out.txt", "w") as f:
        f.write(str(len(selected_ingredients)))
        f.write(" ")
        for i in range(len(selected_ingredients)):
            ing = selected_ingredients[i]
            f.write(ing)
            if i < len(selected_ingredients) - 1:
                f.write(" ")

# Incidence matrix where the rows are clients and columns are ingredients. Value 1 if client i likes an ingredient j, value -1 if client i dislikes ingredient j
def construct_matrix(clients, ingredients):
    matrix = []
    for client in clients:
        ing_list = [0 for _ in range(len(ingredients))]
        
        liked = [i for i in range(len(ingredients)) if ingredients[i] in client.liked]
        for l in liked:
            ing_list[l] = 1
        
        disliked = [i for i in range(len(ingredients)) if ingredients[i] in client.disliked]
        for l in disliked:
            ing_list[l] = -1
        matrix.append(ing_list)
    return np.array(matrix)

# Constructs adjacency matrix of clients that have ingredients in conflict. i.e. client i likes potatoes and client j dislikes potatoes
def construct_conflict_matrix(clients, ingredients):
    problem_matrix = construct_matrix(clients, ingredients)
    conflict_matrix = np.zeros([len(clients), len(clients)])
    
    for ing in range(problem_matrix.shape[1]):
        liked_indexes = np.where(problem_matrix[:, ing] == 1)[0]
        disliked_indexes = np.where(problem_matrix[:, ing] == -1)[0]
        if len(liked_indexes) == 0 or len(disliked_indexes) == 0:
            continue
        for i in liked_indexes:
            for j in disliked_indexes:
                if i == j:
                    continue
                conflict_matrix[i][j] = 1
                conflict_matrix[j][i] = 1
        #for i in disliked_indexes:
        #    for j in liked_indexes:
        #        if i == j:
        #            continue
        #        conflict_matrix[i][j] = 1
        

    return conflict_matrix

def measure_score(clients_indexes, clients):
    ingredients = []
    for index in clients_indexes:
        for ing in clients[index].liked:
            if ing not in ingredients:
                ingredients.append(ing)
    return calculate_points(clients, ingredients)

def ingredients_from_anticlique(anticlique, clients):
    selected_ingredients = []
    for i in anticlique:
        for ing in clients[i].liked:
            if ing not in selected_ingredients:
                selected_ingredients.append(ing)
    return selected_ingredients

def caclulate_vertices_degree(conflict_matrix):
    degrees = []
    for v in range(conflict_matrix.shape[0]):
        degrees.append(np.sum(conflict_matrix[v]))
    return np.array(degrees)

# Initialization algoithms.
# Best initialization algorithm so far. Returns the anti_clique
def clique_degree_heur(conflict_matrix):
    degrees = caclulate_vertices_degree(conflict_matrix)
    sorted_degrees = np.argsort(degrees)
    anti_clique = []
    for v in sorted_degrees:
        toAdd = True
        for u in anti_clique:
            if conflict_matrix[v][u] == 1:
                toAdd = False
                break
        if toAdd:
            anti_clique.append(v)

    return anti_clique

###### SOLVING STRATEGIES ##########

### BEST EURISTIC SO FAR
# Finds an anti-clique with a constrcutive heuristic. 
# For each step, it removes half of nodes from anti-clique and adds new nodes from the graph that satisty the anti-clique constraint
# If a better clique is found, update the clique
def clique_heuristic(clients, ingredients):
    conflict_matrix = construct_conflict_matrix(clients, ingredients)
    anti_clique = clique_degree_heur(conflict_matrix)
    best_anti_clique = anti_clique
    best_score = measure_score(anti_clique, clients)
    print(f"Initial solution: {best_score} clique size: {len(anti_clique)}")
    num_iter = 1000

    for i in range(num_iter):
        min_removals = len(anti_clique) // 8 # Hyperparameter
        max_removals = len(anti_clique) // 2 # Hyperparameter
        num_removals = max_removals#random.choice(range(min_removals, max_removals)) 
        removed = np.random.choice(anti_clique, num_removals)
        anti_clique = [x for x in anti_clique if x not in removed]
        
        ### Adds to the anti-clique the nodes with lowest degree first
        degrees = caclulate_vertices_degree(conflict_matrix)
        sorted_degrees = np.argsort(degrees)
        for v in sorted_degrees:
            if v in removed or v in anti_clique:
                continue
            toadd = True
            for u in anti_clique:
                if conflict_matrix[v][u] == 1:
                    toadd = False
                    break
            if toadd:
                anti_clique.append(v)
        for v in sorted(removed):
            if v in anti_clique:
                continue
            toadd = True
            for u in anti_clique:
                if conflict_matrix[v][u] == 1:
                    toadd = False
                    break
            if toadd:
                anti_clique.append(v)


        score = measure_score(anti_clique, clients)
        if score > best_score:
            best_score = score
            best_anti_clique = anti_clique
            print(f"New score: {best_score}     len is {len(anti_clique)}")
            
    return ingredients_from_anticlique(best_anti_clique, clients)
    

def clique_simulated_annealing(clients, ingredients):
    conflict_matrix = construct_conflict_matrix(clients, ingredients)
    anti_clique = clique_degree_heur(conflict_matrix)
    best_anti_clique = anti_clique
    best_score = measure_score(anti_clique, clients)

    temperature = 200
    alpha = 0.8
    max_iter = 1000
    for k in range(max_iter):
        
        
        
        
        temperature = alpha * temperature

def solve_problem(clients, ingredients):
    selected_ingredients = clique_heuristic(clients, ingredients)
    return selected_ingredients

def main():
    #file_name = "a_an_example"
    #file_name = "b_basic"
    #file_name = "c_coarse"
    file_name = "d_difficult"
    #file_name = "d_simple"
    #file_name = "e_elaborate"

    with open(f"./data/{file_name}.in.txt", "r") as f:
        input = f.readlines()

    
    ingredients = []
    clients = []
            
    num_clients = int(input[0])
    for i in range(1, 2 * num_clients, 2):
        liked_ingredients = input[i].split(" ")[1:]
        liked = []
        for ing in liked_ingredients:
            ing = ing.replace('\n', '')
            liked.append(ing)
            if ing not in ingredients:
                ingredients.append(ing) 

        disliked_ingredients = input[i + 1].split(" ")[1:]
        disliked = []
        for ing in disliked_ingredients:
            ing = ing.replace('\n', '')
            disliked.append(ing)
            if ing not in ingredients:
                ingredients.append(ing) 

        client = Client(liked, disliked)
        clients.append(client)

    conflict_matrix = construct_conflict_matrix(clients, ingredients)
    #anti_clique = clique_degree_heur(conflict_matrix)
    #colors = ['red' if node in anti_clique else 'green' for node in range(conflict_matrix.shape[0])]
    #import networkx as nx 
    #G = nx.DiGraph()
    #G = nx.from_numpy_matrix(conflict_matrix)
    #import matplotlib.pyplot as plt 
    #nx.draw( G , node_color=colors) 
    #plt.show()
        
    
    print(caclulate_vertices_degree(conflict_matrix))

    print(conflict_matrix)

    selected_ingredients = solve_problem(clients, ingredients)

    print(f"Score: {calculate_points(clients, selected_ingredients)}")

    write_output(file_name, selected_ingredients)


if __name__ == "__main__":
    main()