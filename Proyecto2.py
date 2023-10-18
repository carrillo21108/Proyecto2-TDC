from graphviz import Digraph
import time

class Node:
    def __init__(self, symbol, children=[]):
        self.symbol = symbol
        self.children = children

    def __repr__(self):
        return self.symbol

#Visualiza el tree usando graphviz.
def visualize_tree(node):
    dot = Digraph(comment='Parse Tree')
    build_graph(dot, node)
    dot.view()

#Construye el grafo con recursividad.
def build_graph(dot, node, parent_name=None):
    name = node.symbol + str(id(node))
    dot.node(name, node.symbol)
    if parent_name:
        dot.edge(parent_name, name)
    for child in node.children:
        build_graph(dot, child, name)

#Imprime el tree con recursividad.
def print_tree(node, indent=0):
    print(' ' * indent + node.symbol)
    for child in node.children:
        print_tree(child, indent + 2)

#Convierte el array de gramatica a un diccionario
def convert_to_grammar(rules_list):
    grammar = {}
    for rule in rules_list:
        left, right = rule.split("→")
        left = left.strip()
        productions = [prod.strip().split() for prod in right.split("|")]
        if left not in grammar:
            grammar[left] = []
        grammar[left].extend(productions)
    return grammar

#Algoritmo CYK, devuelve el parse tree
def cyk(grammar, W):

    n = len(W)
    P = {}
    
    #Inicializar P con símbolos no terminales que producen terminales
    #Implementacion de la condición base de programación dinámica.
    #Se identifican las derivaciones directas
    for i in range(n):
        P[(i, i + 1)] = []
        for A, productions in grammar.items():
            for prod in productions:
                if len(prod) == 1 and prod[0] == W[i]:
                    P[(i, i + 1)].append(Node(A, [Node(prod[0])]))
    
    # AProgramación dinámica: se llena la matriz P de manera iterativa.
    # Para cada subcadena de la palabra, se buscan todas las posibles derivaciones.
    for span in range(2, n + 1):
        for start in range(n - span + 1):
            end = start + span
            P[(start, end)] = []
            # Se consideran todas las posibles biparticiones de la subcadena
            for split in range(start + 1, end):
                # Se verifica si cada regla de producción se puede aplicar
                for A, productions in grammar.items():
                    for prod in productions:
                        if len(prod) == 2:
                            B, C = prod
                            # Revisamos las soluciones ya almacenadas para las subcadenas [start, split] y [split, end].
                            # Si encontramos coincidencias, construimos una derivación y la agregamos a nuestra matriz P.
                            for b_node in P[(start, split)]:
                                if b_node.symbol == B:
                                    for c_node in P[(split, end)]:
                                        if c_node.symbol == C:
                                            P[(start, end)].append(Node(A, [b_node, c_node]))
    
    # Devuelve el árbol de análisis si existe alguno para la cadena completa
    for node in P[(0, n)]:
        if node.symbol == "S":
            return node
    return None

rules_list = [
    "S → NP VP",
    "VP → VP PP",
    "VP → V NP",
    "VP → cooks | drinks | eats | cuts",
    "PP → P NP",
    "NP → Det N",
    "NP → he | she",
    "V → cooks | drinks | eats | cuts",
    "P → in | with",
    "N → cat | dog",
    "N → beer | cake | juice | meat | soup",
    "N → fork | knife | oven | spoon",
    "Det → a | the"
]

grammar = convert_to_grammar(rules_list)
W = "she eats a cake with a fork"
start_time = time.time()
parse_tree = cyk(grammar, W.split())
if parse_tree:
    print("La expresión 𝑤 SI pertenece al lenguaje descrito por la gramática.")
    visualize_tree(parse_tree)
else:
    print("La expresión 𝑤 NO pertenece al lenguaje descrito por la gramática.")
end_time = time.time()
duration = end_time - start_time
print(f"El algoritmo tardó {duration:.4f} segundos en realizar la validación.")
