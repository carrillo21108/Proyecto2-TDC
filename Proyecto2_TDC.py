import re
import itertools as it
from graphviz import Digraph
import time

#CNF
def simbolosAnulables(gramatica):
    anulables = set()
    cambio = True

    while cambio:
        cambio = False
        for produccion in gramatica:
            cabeza, cuerpo = produccion.split(' → ')
            cuerpos = cuerpo.split(' | ')
            for cuerpo in cuerpos:
                cuerpo = cuerpo.split(' ')
                if 'ε' in cuerpo or all(simbolo in anulables for simbolo in cuerpo):
                    if cabeza not in anulables:
                        anulables.add(cabeza)
                        cambio = True
        
    return anulables

def eliminarProdsEpsilon(gramatica):
    anulables = simbolosAnulables(gramatica)
        
    nuevaGram = []

    for produccion in gramatica:
        cabeza, cuerpo = produccion.split(' → ')
        cuerpos = cuerpo.split(' | ')

        nuevosCuerpos = set(cuerpos)
        
        for cuerpo in cuerpos:
            cuerpo = cuerpo.split(' ')
            
            anulables_cuerpo = []
            for i in range(len(cuerpo)):
                if cuerpo[i] in anulables:
                    anulables_cuerpo.append({"simbolo":cuerpo[i],"position":i})
                     
            for i in range(1,len(anulables_cuerpo)+1):
                combinations = it.combinations(anulables_cuerpo, r=i)

                for combination in combinations:
                    nuevoCuerpo = cuerpo.copy()
                    for item in combination:
                        i = item["position"]
                        nuevoCuerpo[i]=" "
                    
                    while " " in nuevoCuerpo:
                        nuevoCuerpo.remove(" ")
                        
                    if len(nuevoCuerpo)>0:
                        nuevosCuerpos.add(' '.join(nuevoCuerpo))
                    
                        
                    
        if 'ε' in nuevosCuerpos:
            nuevosCuerpos.remove('ε')
        
        if len(nuevosCuerpos)>0:
            nuevaGram.append(cabeza + ' → ' + ' | '.join(nuevosCuerpos))
        

    return nuevaGram

def prodValida(pattern,production):
    return bool(re.match(pattern, production))
    

def simbolosNoTerminales(gramatica):
    no_terminales = set()

    for produccion in gramatica:
        no_terminales.add(produccion.split(' → ')[0])
    
    for produccion in gramatica:
        cabeza, cuerpo = produccion.split(' → ')
        cuerpos = cuerpo.split(' | ')
        
        for cuerpo in cuerpos:
            cuerpo = cuerpo.split(' ')
            for simbolo in cuerpo:
                if simbolo.isupper():
                    no_terminales.add(simbolo)
        
    return no_terminales

def simbolosTerminales(gramatica):
    no_terminales = simbolosNoTerminales(gramatica)
    terminales = set()

    for produccion in gramatica:
        cabeza, cuerpo = produccion.split(' → ')
        cuerpos = cuerpo.split(' | ')
        
        for cuerpo in cuerpos:
            cuerpo = cuerpo.split(' ')
            for simbolo in cuerpo:
                if simbolo not in no_terminales:
                    terminales.add(simbolo)
        
    return terminales

def prodsUnarias(gramatica,no_terminales):
    prods_unarias = set()
    for produccion in gramatica:
        cabeza, cuerpo = produccion.split(' → ')
        cuerpos = cuerpo.split(' | ')
        
        for cuerpo in cuerpos:
            if cuerpo in no_terminales:
                prods_unarias.add((cabeza,cuerpo))
    
    return prods_unarias

def prodsNoUnarias(gramatica,no_terminales):
    prods_no_unarias = set()
    for produccion in gramatica:
        cabeza, cuerpo = produccion.split(' → ')
        cuerpos = cuerpo.split(' | ')
        
        for cuerpo in cuerpos:
            if cuerpo not in no_terminales:
                prods_no_unarias.add((cabeza,cuerpo))
    
    return prods_no_unarias
                

def eliminarProdsUnarias(gramatica):
    nuevaGram = []
    no_terminales = simbolosNoTerminales(gramatica)
    prods_unarias = prodsUnarias(gramatica,no_terminales)
    prods_no_unarias = prodsNoUnarias(gramatica,no_terminales) 

    parejas_unarias = set()
    for simbolo in no_terminales:
        parejas_unarias.add((simbolo,simbolo))
    
    cambio = True
    
    parejas_nueva_gram = set()
    
    while cambio:
        cambio=False
        for pareja in parejas_unarias.copy():
            for prod in prods_unarias:
                if pareja[1]==prod[0] and (pareja[0],prod[1]) not in parejas_unarias:
                    parejas_unarias.add((pareja[0],prod[1]))
                    cambio=True
                    
    for pareja in parejas_unarias:
        for prod in prods_no_unarias:
            if pareja[1]==prod[0]:
                parejas_nueva_gram.add((pareja[0],prod[1]))
    
    for simbolo in no_terminales:
        nuevosCuerpos = set()
        
        for pareja in parejas_nueva_gram:
            if simbolo==pareja[0]:
                nuevosCuerpos.add(pareja[1])
        
        if len(nuevosCuerpos)>0:
            nuevaGram.append(simbolo + ' → ' + ' | '.join(nuevosCuerpos))
            
    return nuevaGram

def simbolosGeneran(gramatica):
    simbolos_generan = simbolosTerminales(gramatica)
    
    cambio = True

    while cambio:
        cambio = False
        for produccion in gramatica:
            cabeza, cuerpo = produccion.split(' → ')
            cuerpos = cuerpo.split(' | ')
            for cuerpo in cuerpos:
                cuerpo = cuerpo.split(' ')
                if all(simbolo in simbolos_generan for simbolo in cuerpo):
                    if cabeza not in simbolos_generan:
                        simbolos_generan.add(cabeza)
                        cambio = True
                        
    return simbolos_generan
    
def eliminarSimbolosNoGeneran(gramatica):
    simbolos_generan = simbolosGeneran(gramatica)
    nuevaGram = []
    
    for produccion in gramatica:
        if produccion.split(' → ')[0] in simbolos_generan:
            nuevaGram.append(produccion)
        
    for produccion in nuevaGram.copy():
        cabeza, cuerpo = produccion.split(' → ')
        cuerpos = cuerpo.split(' | ')
        nuevosCuerpos = set(cuerpos)
        
        for cuerpo in cuerpos:
            cuerpo = cuerpo.split(' ')
            if any(simbolo not in simbolos_generan for simbolo in cuerpo):
                nuevosCuerpos.remove(' '.join(cuerpo))
        
        nuevaGram.remove(produccion)
        if len(nuevosCuerpos)>0:
            nuevaGram.append(cabeza + ' → ' + ' | '.join(nuevosCuerpos))
    
    return nuevaGram

def simbolosAlcanzables(gramatica,simboloInicial):
    simbolos_alcanzables = set(simboloInicial)
    cambio = True

    while cambio:
        cambio = False
        for produccion in gramatica:
            cabeza, cuerpo = produccion.split(' → ')
            cuerpos = cuerpo.split(' | ')
            
            if cabeza in simbolos_alcanzables:
                for cuerpo in cuerpos:
                    cuerpo = cuerpo.split(' ')
                    for simbolo in cuerpo:
                        if simbolo not in simbolos_alcanzables:
                            simbolos_alcanzables.add(simbolo)
                            cambio = True
                        
    return simbolos_alcanzables

def eliminarSimbolosNoAlcanzables(gramatica,simboloInicial):
    simbolos_alcanzables = simbolosAlcanzables(gramatica,simboloInicial)
    nuevaGram = []
                    
    for produccion in gramatica:
        if produccion.split(' → ')[0] in simbolos_alcanzables:
            nuevaGram.append(produccion)
    
    for produccion in nuevaGram.copy():
        cabeza, cuerpo = produccion.split(' → ')
        cuerpos = cuerpo.split(' | ')
        nuevosCuerpos = set(cuerpos)
        
        for cuerpo in cuerpos:
            cuerpo = cuerpo.split(' ')
            if any(simbolo not in simbolos_alcanzables for simbolo in cuerpo):
                nuevosCuerpos.remove(' '.join(cuerpo))
        
        nuevaGram.remove(produccion)
        if len(nuevosCuerpos)>0:
            nuevaGram.append(cabeza + ' → ' + ' | '.join(nuevosCuerpos))

    return nuevaGram

def eliminarSimbolosInutiles(gramatica,simboloInicial):
    nuevaGram = eliminarSimbolosNoGeneran(gramatica)
    nuevaGram = eliminarSimbolosNoAlcanzables(nuevaGram,simboloInicial)
    
    return nuevaGram

def generarSimbolo(state):
    return state[0:2]+chr(ord(state[2]) + 1)    


def cnfA(gramatica):
    state_counter = 'X_0'
    terminales = simbolosTerminales(gramatica)
    nuevaGram = []
    nuevasProd = set()
    
    for produccion in gramatica:
        cabeza, cuerpo = produccion.split(' → ')
        cuerpos = cuerpo.split(' | ')
        
        for cuerpo in cuerpos:
            if cuerpo not in terminales:
                cuerpo = cuerpo.split(' ')
                
                for simbolo in cuerpo:
                    if simbolo in terminales and simbolo not in [item[1] for item in nuevasProd]:
                        state_counter = generarSimbolo(state_counter)
                        nuevasProd.add((state_counter,simbolo))
     
    for item in nuevasProd:
        nuevaGram.append(item[0] + ' → ' + item[1])

    for produccion in gramatica:
        cabeza, cuerpo = produccion.split(' → ')
        cuerpos = cuerpo.split(' | ')
        
        nuevosCuerpos = set()
        
        for cuerpo in cuerpos:
            if cuerpo not in terminales:
                cuerpo = cuerpo.split(' ')
                
                for simbolo in cuerpo:
                    for item in nuevasProd:
                        if simbolo==item[1]:
                            i = cuerpo.index(simbolo)
                            cuerpo[i] = item[0]
            
                cuerpo=' '.join(cuerpo)
            
            nuevosCuerpos.add(cuerpo)
            
        if len(nuevosCuerpos)>0:
            nuevaGram.append(cabeza + ' → ' + ' | '.join(nuevosCuerpos))
                   
    return nuevaGram

def cnfB(gramatica):
    state_counter = 'C_0'
    terminales = simbolosTerminales(gramatica)
    cambio=True
    
    while cambio:
        nuevaGram = []
        nuevasProd = set()
        cambio=False
        for produccion in gramatica:
            cabeza, cuerpo = produccion.split(' → ')
            cuerpos = cuerpo.split(' | ')
        
            for cuerpo in cuerpos:
                if cuerpo not in terminales:
                    cuerpo = cuerpo.split(' ')
                    if len(cuerpo)>=3 and (cuerpo[len(cuerpo)-2],cuerpo[len(cuerpo)-1]) not in [item[1] for item in nuevasProd]:
                            state_counter = generarSimbolo(state_counter)
                            nuevasProd.add((state_counter,(cuerpo[len(cuerpo)-2],cuerpo[len(cuerpo)-1])))
                            cambio=True
                        
        for item in nuevasProd:
            nuevaGram.append(item[0] + ' → ' + item[1][0] + ' ' + item[1][1])
        
        for produccion in gramatica:
            cabeza, cuerpo = produccion.split(' → ')
            cuerpos = cuerpo.split(' | ')
        
            nuevosCuerpos = set()
        
            for cuerpo in cuerpos:
                if cuerpo not in terminales:
                    cuerpo = cuerpo.split(' ')
                
                    if len(cuerpo)>=3:
                        for item in nuevasProd:
                            if (cuerpo[len(cuerpo)-2],cuerpo[len(cuerpo)-1])==item[1]:
                                cuerpo[len(cuerpo)-2] = item[0]
                                cuerpo[len(cuerpo)-1] = " "
                
                    while " " in cuerpo:
                            cuerpo.remove(" ")
                    cuerpo=' '.join(cuerpo)
            
                nuevosCuerpos.add(cuerpo)
            
            if len(nuevosCuerpos)>0:
                nuevaGram.append(cabeza + ' → ' + ' | '.join(nuevosCuerpos))
            
        gramatica = nuevaGram    

    return nuevaGram

def cnf(gramatica):
    nuevaGram = cnfA(gramatica)
    nuevaGram = cnfB(nuevaGram)
    
    return nuevaGram

#CYK
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
    dot.view(filename='Parse Tree',cleanup=True)

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
def cyk(grammar, W,simboloInicial):

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
        if node.symbol == simboloInicial:
            return node
    return None



#Ejecucion
pattern = r"([A-Z]+)\s*→\s*(\w|\s)+"
gramatica = []
denegade = False
simboloInicial = ""

with open("gramatica.txt", 'r') as f:
    print("\n---------------------")
    print("GRAMATICA ORIGINAL: ")
    lineas = f.readlines()
    for i, linea in enumerate(lineas):
        linea = linea.strip()
        linea = linea.replace("â†’","→")
        linea = linea.replace("Îµ","ε")
            
        respuesta = prodValida(pattern,linea)
            
        if respuesta:
            gramatica.append(linea)
            if i==0:
                simboloInicial = linea.split(' → ')[0]
            print(linea)
        else:
            print("\n¡ERROR! La linea: "+linea+" de la gramatica.txt es incorrecta.")
            denegade =True
            break
        
if denegade is False:
    nuevaGramatica = eliminarProdsEpsilon(gramatica)
    print("\nGRAMATICA SIN PRODUCCIONES ε: ")
    for item in nuevaGramatica:
        print(item)
    
    nuevaGramatica = eliminarProdsUnarias(nuevaGramatica)
    print("\nGRAMATICA SIN PRODUCCIONES UNARIAS: ")
    for item in nuevaGramatica:
        print(item)

    nuevaGramatica = eliminarSimbolosInutiles(nuevaGramatica,simboloInicial)
    print("\nGRAMATICA SIN SIMBOLOS INUTILES: ")
    for item in nuevaGramatica:
        print(item)
    
    nuevaGramatica = cnf(nuevaGramatica)
    print("\nGRAMATICA EN CNF: ")
    for item in nuevaGramatica:
        print(item)
        
    grammar = convert_to_grammar(nuevaGramatica)
    
    #Ingreso de cadena
    W = input("\nIngrese la cadena 𝑤. Separe con espacios en blanco cada no terminal. Ejemplo: ( id * id ) + id\n")
    start_time = time.time()
    parse_tree = cyk(grammar, W.split(), simboloInicial)
    if parse_tree:
        print("\nLa expresión 𝑤 SI pertenece al lenguaje descrito por la gramática.")
        visualize_tree(parse_tree)
    else:
        print("La expresión 𝑤 NO pertenece al lenguaje descrito por la gramática.")
    end_time = time.time()
    duration = end_time - start_time
    print(f"El algoritmo tardó {duration:.4f} segundos en realizar la validación.")