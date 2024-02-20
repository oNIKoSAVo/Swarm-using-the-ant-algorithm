import random
from matplotlib.gridspec import GridSpec
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.animation import FuncAnimation
import numpy as np

from ant_colony import ant_colony_iteration, get_probabilities_button_value,print_probabilities, set_probabilities_button
from graph_helpers import draw_graph, display_info,draw_diagram
from util import get_const, get_var, print_path, generate_random_parameters, calculate_trust_scores

# Граф
G = nx.DiGraph()

# Определение рёбер в графе, констант и переменных
ALPHA, BETA, EVAPORATION_RATE, INITIAL_PHEROMONE, ITERATIONS, ANTS_COUNT, EDGES ,START_NODE, END_NODE = get_const()
edge_labels, hacked_nodes = get_var()

# Добавили веса для новых рёбер
random_weights = [random.randint(1, 9) for _ in range(len(EDGES))]
G.add_weighted_edges_from(zip([u for u, v in EDGES], [v for u, v in EDGES], random_weights))
# Добавление узлов с иконками компьютеров
G.add_node(1, image="computer_start.png", pos=(0, 0), size=100)
G.add_node(16, image="computer_end.png", pos=(5, 0), size=100)
# Инициализация феромонов с нуля
edge_pheromone = {(u, v): float(INITIAL_PHEROMONE) for u, v in G.edges()}

# Функция веса и оценок для графика
def update_parameters_and_scores_graph(frame):
    update_parameters_and_scores()

# Функция тика прохода агентов  
def update(frame):
    # Затем обновите граф и любые другие элементы вашей анимации
    edge_labels = {(u, v): round(edge_pheromone[(u, v)], 2) for u, v in G.edges()}
    plt.sca(ax_graph)
    plt.cla()
    draw_graph(G, edge_labels, pos, node_colors)
    draw_diagram(ax_diagram)
    display_info(ax_info, edge_pheromone, G)
    plt.draw()

    # вызываем ant_colony_iteration для обновления состояния алгоритма
    ant_colony_iteration(G, ANTS_COUNT, ALPHA, BETA, EVAPORATION_RATE, edge_pheromone, START_NODE, END_NODE, ITERATIONS, trust_scores)
    print_path(START_NODE,END_NODE,edge_pheromone, G, ALPHA,BETA)

# Функция веса и оценок
def update_parameters_and_scores():
    global parameters, trust_scores
    parameters = generate_random_parameters(G.number_of_nodes(),hacked_nodes)
    trust_scores = calculate_trust_scores(parameters, G.number_of_nodes())

# Добавили веса для узлов
# Создание начальных параметров и оценок доверия
update_parameters_and_scores()

pos = nx.spring_layout(G)

plt.ion()
# fig, (ax_graph, ax_info,ax_diagram) = plt.subplots(1, 2, 3, figsize=(20, 10))



# Создайте объект GridSpec с 2 строками и 2 столбцами
gs = GridSpec(nrows=2, ncols=2, height_ratios=[1, 1])

# Создание Figure
fig = plt.figure(figsize=(20, 10))

# Добавляйте независимые графики (Axes), и задавайте их расположение на GridSpec
ax_graph = fig.add_subplot(gs[:, 0])  # Весь первый столбец
ax_info = fig.add_subplot(gs[0, 1])  # Верхняя правая область
ax_diagram = fig.add_subplot(gs[1, 1])  # Нижняя правая область


node_colors = {node: 'orange' for node in G.nodes()}



hack_button_ax = plt.axes([0.01, 0.96, 0.1, 0.03])
hack_button = Button(hack_button_ax, 'Взлом узла', color='red', hovercolor='lightcoral')

node_input_ax = plt.axes([0.2, 0.96, 0.1, 0.03])
node_input = TextBox(node_input_ax, 'Узел:')

print_prohabilities_ax = plt.axes([0.35, 0.96, 0.2, 0.03])
print_prohabilities = Button(print_prohabilities_ax, 'Вывести в консоль вероятности и пути', color='green',hovercolor='lightcoral' )

# Функция для взлома узла
def hack_node(event):
    node_index = int(node_input.text) - 1
    # Устанавливаем цвет узла на красный, чтобы обозначить взлом
    hacked_nodes.append(node_index)
    node_colors[node_index+1] = 'red'  # Обновляем цвет узла в словаре
    # Перерисовываем граф с обновленными цветами узлов
    plt.sca(ax_graph)
    plt.cla()
    edge_labels = {(u, v): round(edge_pheromone[(u, v)], 2) for u, v in G.edges()}
    draw_graph(G, edge_labels, pos, node_colors)
    display_info(ax_info, edge_pheromone, G)
    draw_diagram(ax_diagram)
    plt.draw()
    
def print_probabilities_button(event):
    global value
    value = get_probabilities_button_value()
    set_probabilities_button(not value)

#Привязываем функцию взлома к кнопке
hack_button.on_clicked(hack_node)

#Привязываем функцию вывода в консоль к кнопке
print_prohabilities.on_clicked(print_probabilities_button)


ani = FuncAnimation(fig, update_parameters_and_scores_graph, interval=2000)
ant_ani = FuncAnimation(fig, update, interval=2000)
    

plt.ioff()
plt.subplots_adjust(top=1)
plt.show()