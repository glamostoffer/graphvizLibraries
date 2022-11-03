from graphviz import Digraph
import requests

g = 0

def dependence_search(package):
    url = 'https://pypi.org/pypi/{}/json'
    json = requests.get(url.format(package)).json()

    try:
        var = json['info']['requires_dist']
    except:
        return

    if var is None:
        return []

    for i in range(len(var)):
        var[i] = var[i][:var[i].find('(') - 1]
    var = sorted(set(var), key=lambda x: var.index(x))
    return var


def creating_edges(graph, list, package):
    if list is None or graph is None:
        return

    # for require in list:
    #     graph.node(require)

    for require in list:
        graph.edge(package, require)
    return graph


def depth_search(depend_list, graph):
    global g
    if depend_list is None or g > 3:
        return

    for lib in depend_list:
        dep_lib = dependence_search(lib)
        graph = creating_edges(graph, dep_lib, lib)
        depth_search(dep_lib, graph)
    g += 1
    return graph


pack = input("Введите название библиотеки: ")

my_graph = Digraph(comment="Dependencies")
my_graph.node(pack)

list_of_depend = dependence_search(pack)
my_graph = creating_edges(my_graph, list_of_depend, pack)
my_graph = depth_search(list_of_depend, my_graph)

print(my_graph.source)
