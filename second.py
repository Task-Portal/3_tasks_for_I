
# region imports
from heapq import heapify, heappop, heappush
import re
from collections import OrderedDict
import time
# endregion
#function to check the time 
def timer(func):
    def inner(*args, **kwargs):
        t1 = time.time()
        f = func(*args, **kwargs)
        t2 = time.time()
        print(f"Время выполнения заняло {t2-t1:.6f} ceкyнд")
        return f
    return inner

# region class Graph to calculate distances
class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph

    def shortest_distances(self, source: str):
        # Initialize the values of all nodes with infinity
        distances = {node: float("inf") for node in self.graph}
        distances[source] = 0  # Set the source value to 0

        # Initialize a priority queue
        pq = [(0, source)]
        heapify(pq)

        # Create a set to hold visited nodes
        visited = set()

        while pq:  # While the priority queue isn't empty
            current_distance, current_node = heappop(
                pq
            )  # Get the node with the min distance

            if current_node in visited:
                continue  # Skip already visited nodes
            visited.add(current_node)  # Else, add the node to visited set

            for neighbor, weight in self.graph[current_node].items():
                # Calculate the distance from current_node to the neighbor
                tentative_distance = current_distance + weight
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    heappush(pq, (tentative_distance, neighbor))

        predecessors = {node: None for node in self.graph}

        for node, distance in distances.items():
            for neighbor, weight in self.graph[node].items():
                if distances[neighbor] == distance + weight:
                    predecessors[neighbor] = node

        return distances, predecessors

    def shortest_path(self, source: str, target: str):
        # Generate the predecessors dict
        _, predecessors = self.shortest_distances(source)

        path = []
        current_node = target

        # Backtrack from the target node using predecessors
        while current_node:
            path.append(current_node)
            current_node = predecessors[current_node]

        # Reverse the path and return it
        path.reverse()

        return path

# endregion

# region Change towns names function
# this function converts data to needed view for Graph class
# Graph class accepts this kind of dict
# graph = {
#     "A": {"B": 3, "C": 3},


def change_towns_names(data: list) -> list:
    new_data = []
    for i in data:
        towns = [j for j in i['graph']]
        new_graph: dict = {}
        for k in i['graph']:
            new_graph[k] = {}

            for l in i['graph'][k]:
                town_int, cost = l.split(" ")
                town_from_list = towns[int(town_int)-1]
                new_graph[k][town_from_list] = int(cost)

        new_data.append(
            {
                'number_of_test_cases': i['number_of_test_cases'],
                'number_of_towns': i['number_of_towns'],
                'graph': new_graph,
                'paths': i['paths']
            }
        )
    return new_data

# endregion


example_input = """
1
4
gdansk
2
2 1
3 3
bydgoszcz
3
1 1
3 1
4 4
torun
3
1 3
2 1
4 1
warszawa
2
2 4
3 1
2
gdansk warszawa
bydgoszcz warszawa

2
4
gdansksss
2
2 1
3 3
bydgoszczsss
3
1 1
3 1
4 4
torunsss
3
1 3
2 1
4 1
warszawasss
2
2 4
3 1
2
gdansksss warszawasss
bydgoszczsss warszawasss

"""


# region Parse input function
# this function parses the input data to array of dictionaries
# the output of the function looks like this
# region data that I get from parse input
# [
#  {
#    'number_of_test_cases': '1',
#    'number_of_towns': '4',
#    'graph': OrderedDict({
#      'gdansk': [
#        '2 1',
#        '3 3'
#      ],
#       ....
#    }),
#    'paths': [
#      'gdansk warszawa',
#      'bydgoszcz warszawa'
#    ]
#  },
#  {
#    'number_of_test_cases': '2',
#   ...
#  }
# ]
# endregion
def parse_input(input_data):
    input_lines: list[str] = input_data.split("\n")
    number_of_test_cases = None
    number_of_towns = None
    graph = OrderedDict()
    test_cases = []
    paths = []
    name = ""
    # regular epxression to parse towns, their values, number of test cases, numbers of towns
    regex = r"^(?P<town_num_or_test_num>[0-9]+)$|^(?P<town>[a-zA-Z]+)$|^(?P<values>[0-9]+ [0-9])$|^(?P<paths>[a-zA-Z]+ [a-zA-Z]+)$"
    try:
        for l in input_lines:
            l = l.strip()
            m = re.match(regex, l)
            # in this if we saving our data from lines. Forgive me Martin :-)
            if m:
                if m.group('town_num_or_test_num'):
                    if number_of_test_cases is None:
                        number_of_test_cases = l
                    elif number_of_towns is None:
                        number_of_towns = l
                elif m.group('town'):
                    graph[l] = []
                    name = l
                elif m.group('values'):
                    graph[name].append(l)
                elif m.group('paths'):
                    paths.append(l)
            elif l == "" and number_of_test_cases:
                # here we saving our data to dictionary
                test_cases.append({
                    'number_of_test_cases': number_of_test_cases,
                    'number_of_towns': number_of_towns,
                    'graph': graph,
                    'paths': paths
                })
                number_of_test_cases = None
                number_of_towns = None
                paths = []
                graph = OrderedDict()
    except Exception as e:
        print(e)
        return []
    return test_cases

# endregion


# region Solve (Main function)
# this function run the whole programs
# 1 It takes input data and calls parser
# 2 when we have data arranges than we can calculate distances using Graph class
# 3 outputting results
@timer
def solve(input_data):
    test_cases = change_towns_names(parse_input(input_data))
    if len(test_cases)==0:
        return "Couldn't parse the data"
    results = []

    for i in range(len(test_cases)):
        graph = test_cases[i]['graph']
        paths = test_cases[i]['paths']
        G = Graph(graph)
        for j in paths:
            src, dest = j.split(" ")
            distances = G.shortest_distances(src)
            results.append(distances[0][dest])

    # Output the results
    for result in results:
        print(result)
    return results

try:
    if __name__=="__main__":
        solve(example_input)
except Exception as e:
    print(e)
# endregion
