import random

def get_const():
    # Параметры алгоритма
    ALPHA = 0.5
    BETA = 0.5
    EVAPORATION_RATE = 0.1
    INITIAL_PHEROMONE = 0.1
    ITERATIONS = 100
    ANTS_COUNT=10
    # Определение начального и конечного узлов
    START_NODE=1
    END_NODE=16
    EDGES = [
    (1, 2), (1, 3), (1, 4),
    (2, 5), (2, 6), (2, 7),
    (3, 5), (3, 6), (3, 7),
    (4, 5), (4, 6), (4, 7),
    (5, 8), (6, 8), (7, 8),
    (8, 9), (8, 10), (8, 11),
    (9, 12), (10, 12), (11, 12),
    (12, 13), (12, 14), (12, 15),
    (13, 16), (14, 16), (15, 16)
]
    return ALPHA, BETA, EVAPORATION_RATE, INITIAL_PHEROMONE, ITERATIONS, ANTS_COUNT, EDGES ,START_NODE, END_NODE

def get_var():
    edge_labels=[]
    hacked_nodes=[]
    return edge_labels,hacked_nodes

# Создание начальных случайных значений параметров
def generate_random_parameters(num_nodes,hacked_nodes):
    connection_quality = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    reliability = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    energy_consumption = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    latency = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    traffic_load = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    interference_noise = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    history = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    availability = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    error_handling = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    activity = [random.uniform(0.8, 1.0) for _ in range(num_nodes)]
    
    # Если узел взломан, устанавливаем низкие параметры
    for node_index in hacked_nodes:
        connection_quality[node_index] = random.uniform(0.2, 0.3)
        reliability[node_index] = random.uniform(0.2, 0.3)
        energy_consumption[node_index] = random.uniform(0.2, 0.3)
        latency[node_index] = random.uniform(0.2, 0.3)
        traffic_load[node_index] = random.uniform(0.2, 0.3)
        interference_noise[node_index] = random.uniform(0.2, 0.3)
        history[node_index] = random.uniform(0.2, 0.3)
        availability[node_index] = random.uniform(0.2, 0.3)
        error_handling[node_index] = random.uniform(0.2, 0.3)
        activity[node_index] = random.uniform(0.2, 0.3)
    
    return (connection_quality, reliability, energy_consumption, latency, traffic_load, interference_noise,
            history, availability, error_handling, activity)

def calculate_trust_scores(params, num_nodes):
    (connection_quality, reliability, energy_consumption, latency, traffic_load, interference_noise,
     history, availability, error_handling, activity) = params
    
    trust_scores = [(connection_quality[i] * reliability[i] * energy_consumption[i] * latency[i] *
                    traffic_load[i] * interference_noise[i] * history[i] * availability[i] *
                    error_handling[i] * activity[i]) ** 0.1 for i in range(num_nodes)]

    trust_scores_dict = {i+1: score for i, score in enumerate(trust_scores)}

    return trust_scores_dict

def print_path(START_NODE,END_NODE,edge_pheromone, G, ALPHA,BETA):
    best_path = []
    current_node = START_NODE
    while current_node != END_NODE:
        edges_from_current_node = list(G.edges(current_node, data=True))
        next_edge_probabilities = []

        for _, v, data in edges_from_current_node:
            edge = (current_node, v)
            if edge in edge_pheromone:
                tau = edge_pheromone[edge]
                eta = 1 / data['weight']
                probability = (tau ** ALPHA) * (eta ** BETA)
                next_edge_probabilities.append((edge, probability))

        if next_edge_probabilities:
            next_edge_probabilities.sort(key=lambda x: x[1], reverse=True)
            next_edge = next_edge_probabilities[0][0]
            best_path.append(current_node)
            current_node = next_edge[1]
        else:
            print("Не удалось найти доступное ребро. Поиск завершен.")
            break

    best_path.append(END_NODE)
    best_path_string = "->".join(map(str, best_path))
    return print(f"Самый лучший путь: {best_path_string}")