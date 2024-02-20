import random
import networkx as nx

data_graphic = []
probabilities_on = False
button_print_probabilities = False

def get_data_graphic():
    return data_graphic

def set_probabilities_on(value):
    global probabilities_on
    probabilities_on = value

def get_probabilities_button_value():
    return button_print_probabilities

def set_probabilities_button(value):
    global button_print_probabilities
    button_print_probabilities = value

def ant_colony_iteration(G, ANTS_COUNT, ALPHA, BETA,
                         EVAPORATION_RATE, edge_pheromone,
                         START_NODE, END_NODE, ITERATIONS,
                         trust_scores):
    
    probabilities_all = [[] for _ in range(END_NODE)]
    next_edge_index_all = [[] for _ in range(END_NODE)]
    edges_from_current_node_all = [[] for _ in range(END_NODE)]
    for _ in range(ANTS_COUNT):
        probabilities_and_trust = []
        current_node = START_NODE
        visited_edges = []
        trust_threshold = 0.5
        i=0
        while current_node != END_NODE:
            edges_from_current_node = list(G.edges(current_node, data=True))
            probabilities = []
            trusts=[]

            for _, v, data in edges_from_current_node:
                edge = (current_node, v)
                tau = edge_pheromone[edge]
                trust = trust_scores[v]
                eta = 1 / data['weight']
                probability = (tau ** ALPHA) * (eta ** BETA)
                probabilities.append((probability))
                trusts.append((trust))

            # Проверка на случай нулевой суммы вероятностей
            if sum(probability for probability in probabilities) == 0:
                # Если вероятности равны нулю, выбираем случайное доступное ребро
                next_edge_index_temp = random.choice(range(len(edges_from_current_node)))
            else:
                # Иначе, используем вероятности для выбора следующего ребра
                # probabilities_temp = [(probability / sum(probability for probability in probabilities))  for probability in probabilities]
                sum_probabilities = sum(probabilities)
                probabilities_and_trust = [(p*t / sum_probabilities)  for p,t in zip(probabilities, trusts)]
                # probabilities_temp2 = [(p*t)  for p, t in zip(probabilities_temp, trusts)]
                next_edge_index_temp = random.choices(range(len(edges_from_current_node)), probabilities_and_trust)[0]

            # probabilities_all.append(probabilities_and_trust)
            probabilities_all[i].append(probabilities_and_trust)
            next_edge_index_all[i].append(next_edge_index_temp)
            if not edges_from_current_node_all[i]:
                edges_from_current_node_all[i].extend(edges_from_current_node)
             
            # if trusts[next_edge_index] < trust_threshold:
            # # Если доверие узла ниже порога, вернуться на предыдущий узел
            #     if visited_edges:
            #         current_node = visited_edges.pop()[0]
            # else:
            #     # Если доверие узла выше порога, переместиться на следующий узел
            #         next_edge = (current_node, edges_from_current_node[next_edge_index][1])
            #         visited_edges.append(next_edge)
            #         current_node = next_edge[1]

            next_edge = (current_node, edges_from_current_node[next_edge_index_temp][1])
            visited_edges.append(next_edge)
            current_node = next_edge[1]
            i=i+1

        delta_pheromone = 1 / sum(G[u][v]['weight'] for u, v in visited_edges)
        for edge in visited_edges:
            edge_pheromone[edge] += delta_pheromone
            
    if (probabilities_on):
        global data_graphic
        data_graphic = build_ant_probablity(ANTS_COUNT,edges_from_current_node_all,probabilities_all,next_edge_index_all)

        if (button_print_probabilities):
            print_probabilities(ANTS_COUNT,edges_from_current_node_all,probabilities_all,next_edge_index_all)

    for edge in G.edges():
        if edge_pheromone[edge] > 5:
            edge_pheromone[edge] = 5
        edge_pheromone[edge] *= (1 - EVAPORATION_RATE)


def print_probabilities(ANTS_COUNT,edges_from_current_node_all,probabilities_all,next_edge_index_all):

    edges_from_current_node_all = [list_temp for list_temp in edges_from_current_node_all if list_temp]
    probabilities_all = [list_temp for list_temp in probabilities_all if list_temp]
    next_edge_index_all = [list_temp for list_temp in next_edge_index_all if list_temp]


    # Цикл для обхода муравьев
    for ant in range(ANTS_COUNT):
        path_str = f"Муравей {ant + 1} и его вероятности:"

        # Вывод пути муравья
        path_str += f"\nПуть: 1->"
        for i, next_edge_index in enumerate(next_edge_index_all):
            edge = edges_from_current_node_all[i][next_edge_index[ant]]
            path_str += f"{edge[1]}"
            if i < len(next_edge_index_all) - 1:
                path_str += "->"

        # Вывод вероятностей ребер на каждом проходе
        for i, (edge_indexes_for_step, probability_list) in enumerate(zip(next_edge_index_all, probabilities_all)):
            next_edge_index = edge_indexes_for_step[ant]
            path_str += f"\nДля прохода {i + 1} ребра:"
            for edge_index, edge in enumerate(edges_from_current_node_all[i]):
                path_str += f"\n{edge[0]}->{edge[1]}"
                if edge_index == next_edge_index:
                    path_str += " - выбранная вероятность = "
                else:
                    path_str += " - вероятность = "
                path_str += f"{probability_list[ant][edge_index]}"
        print(path_str)
        print()


def build_ant_probablity(ANTS_COUNT,edges_from_current_node_all,probabilities_all,next_edge_index_all):

    edges_from_current_node_all = [list_temp for list_temp in edges_from_current_node_all if list_temp]
    probabilities_all = [list_temp for list_temp in probabilities_all if list_temp]
    next_edge_index_all = [list_temp for list_temp in next_edge_index_all if list_temp]


    ants_data = []

    for ant in range(ANTS_COUNT):
        ant_dict = {f"Муравей {ant + 1}": []}

        for i, (edge_indexes_for_step, probability_list) in enumerate(zip(next_edge_index_all, probabilities_all)):
            next_edge_index = edge_indexes_for_step[ant]
            
            for edge_index, edge in enumerate(edges_from_current_node_all[i]):
                edge_path = f"{edge[0]} -> {edge[1]}"
                probability = probability_list[ant][edge_index]
                            
                ant_dict[f"Муравей {ant + 1}"].append((edge_path, probability))
                    
        ants_data.append(ant_dict)

    # Используйте переменную ants_data, чтобы вывести данные о муравьях
    return ants_data
    