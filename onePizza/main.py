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
        if len(liked_indexes) == len(clients) or len(liked_indexes) == 0 or len(disliked_indexes) == len(clients) or len(disliked_indexes) == 0:
            continue
        for i in liked_indexes:
            for j in disliked_indexes:
                if i == j:
                    continue
                conflict_matrix[i][j] = 1
        for i in disliked_indexes:
            for j in liked_indexes:
                if i == j:
                    continue
                conflict_matrix[i][j] = 1
        

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

# Initialization algoithms. Each of them returns the anti-clique
def calculate_anticlique_with_greedy(clients, conflict_matrix, start_node):
    anti_clique = []
    
    for v in range(start_node, len(clients)):
        if v in anti_clique:
            continue

        toadd = True
        for u in anti_clique:
            if conflict_matrix[v][u] == 1: # Checks if the node v violates the anti-clique constraint with the nodes added in anti-clique list
                toadd = False
                break
        
        if toadd:
            anti_clique.append(v)
    return anti_clique

# Best initialization algorithm so far
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
def clique_solver_greedy(clients, conflict_matrix, start_node):
    selected_ingredients = []
    anti_clique = calculate_anticlique_with_greedy(clients, conflict_matrix, start_node)

    print(np.array(sorted(anti_clique)) + 1)

    for i in anti_clique:
        for ing in clients[i].liked:
            if ing not in selected_ingredients:
                selected_ingredients.append(ing)
    
    return selected_ingredients

def clique_solver_greedy_multistart(clients, ingredients):
    conflict_matrix = construct_conflict_matrix(clients, ingredients)
    best_ingredients = []
    best_score = 0
    for node in range(len(clients)):
        selected_ingr = clique_solver_greedy(clients, conflict_matrix, node)
        score = calculate_points(clients, selected_ingr)
        if score > best_score:
            best_score = score
            best_ingredients = selected_ingr
            print(f"New score: {best_score}")
    return best_ingredients

def clique_solver_randomized_greedy(clients, ingredients):
    conflict_matrix = construct_conflict_matrix(clients, ingredients)
    random_node = random.choice(range(len(clients)))
    return clique_solver_greedy(clients, conflict_matrix, random_node)

def clique_multi_random_greedy(clients, ingredients):
    conflict_matrix = construct_conflict_matrix(clients, ingredients)
    num_iter = 500
    best_ingredients = []
    best_score = 0
    for i in range(num_iter):
        random_node = random.choice(range(len(clients)))
        selected_ingr = clique_solver_greedy(clients, conflict_matrix, random_node)
        score = calculate_points(clients, selected_ingr)
        if score > best_score:
            best_score = score
            best_ingredients = selected_ingr
            print(f"New score: {best_score}")
    return best_ingredients


def clique_tabu(clients, ingredients):
    conflict_matrix = construct_conflict_matrix(clients, ingredients)
    anti_clique = clique_degree_heur(conflict_matrix)
    best_anti_clique = anti_clique
    best_score = measure_score(anti_clique, clients)
    print(f"Initial solution: {best_score}")
    tabulist = np.zeros(len(clients))
    tenure_iter = 15
    tot_iter = 1000
    min_tenure = 5#int(len(clients) * 0.05)
    max_tenure = len(clients) // 4
    curr_tenure = min_tenure

    def is_node_tabu(node, iter, tenure):
        if tabulist[node] < 0:
            return False
        #print(f"{node} Tabu value is {tabulist[node]}")
        if iter - tabulist[node] >= tenure:
            tabulist[node] = 0
            return False
        return True

    for curriter in range(1, tot_iter):
        print(f"{curriter}/{tot_iter}  {curr_tenure}   len: {len(anti_clique)}  tabulen {np.count_nonzero(tabulist > 0)}")
        removed = np.random.choice(anti_clique, curr_tenure)
        anti_clique = [x for x in anti_clique if x not in removed]

        for r in removed:
            tabulist[r] = curriter
        
        added = 0
        for v in range(len(clients)):
            if is_node_tabu(v, curriter, curr_tenure) or v in anti_clique:
                continue
            toadd = True
            for u in anti_clique:
                if conflict_matrix[v][u] == 1:
                    toadd = False
                    break
            if toadd:
                anti_clique.append(v)
                added += 1
        print(f"Added {added}")
        
        score = measure_score(anti_clique, clients)
        if score > best_score:
            best_score = score
            best_anti_clique = anti_clique
            print(f"New score: {best_score}     len is {len(anti_clique)}")
        
        # Step policy
        if curriter % tenure_iter == 0:
            curr_tenure = min_tenure if curr_tenure == max_tenure else max_tenure
            print(f"Changed tenure: {curr_tenure}")
    
    return ingredients_from_anticlique(best_anti_clique, clients)

### BEST EURISTIC SO FAR
# Finds an anti-clique with a constrcutive heuristic. 
# For each step, it removes half of nodes from anti-clique and adds new nodes from the graph that satisty the anti-clique constraint
# If a better clique is found, update the clique
def clique_heuristic(clients, ingredients):
    conflict_matrix = construct_conflict_matrix(clients, ingredients)
    anti_clique = clique_degree_heur(conflict_matrix)
    best_anti_clique = anti_clique
    best_score = measure_score(anti_clique, clients)
    print(f"Initial solution: {best_score}")
    num_iter = 100

    for i in range(num_iter):
        min_removals = len(anti_clique) // 8 # Hyperparameter
        max_removals = len(anti_clique) // 2 # Hyperparameter
        num_removals = len(anti_clique) // 4#random.choice(range(min_removals, max_removals)) 
        removed = np.random.choice(anti_clique, num_removals)
        anti_clique = [x for x in anti_clique if x not in removed]
        
        ### METHOD 1
        ### Adds the clique using greedy
        #for v in range(len(clients)):
        #    if v in removed or v in anti_clique:
        #        continue
        #    toadd = True
        #    for u in anti_clique:
        #        if conflict_matrix[v][u] == 1:
        #            toadd = False
        #            break
        #    if toadd:
        #        anti_clique.append(v)

        ### METHOD 2
        ### Adds to the anti-clique the nodes with lowest degree first
        #degrees = caclulate_vertices_degree(conflict_matrix)
        #sorted_degrees = np.argsort(degrees)
        #for v in sorted_degrees:
        #    if v in removed or v in anti_clique:
        #        continue
        #    toadd = True
        #    for u in anti_clique:
        #        if conflict_matrix[v][u] == 1:
        #            toadd = False
        #            break
        #    if toadd:
        #        anti_clique.append(v)

        ### METHOD 3
        ### Picks randomly a node to add to the clique
        for _ in range(len(clients)):
            v = np.random.choice(range(len(clients)))
            #if v in removed or v in anti_clique:
            if v in anti_clique:
                continue
            toAdd = True
            for u in anti_clique:
                if conflict_matrix[u][v] == 1:
                    toAdd = False
                    break
            if toAdd:
                anti_clique.append(v)


        score = measure_score(anti_clique, clients)
        if score > best_score:
            best_score = score
            best_anti_clique = anti_clique
            print(f"New score: {best_score}     len is {len(anti_clique)}")
            
    return ingredients_from_anticlique(best_anti_clique, clients)

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