import warnings
warnings.filterwarnings("ignore")

import networkx as nx
import matplotlib.pyplot as pyplot
from matplotlib.widgets import TextBox
from matplotlib import rcParams
import ast

### Calcul du nombre chromatique d'un graphe ###
### Entrée: Matrice d'adjascence ###
### Sortie: Le nombre chromatique, le graphe coloré ###
# V = Nombre de sommet du graphe (donc V =  nombre de ligne/colonne de la matrice d'adjacence)
class Graph:
    def __init__(self, _graph):
        self._graph = _graph
        self.V = len(_graph) 
        self._sorted_graph = []
        self._sorted_graph_index = []
        self._colors = ['F' for i in range(0,self.V)]
        self._color_lemma_list = []
        self._degrees = [0 for i in range(0,self.V)]
        self.chromatic_number = 0
        self._edges_list= []

        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def matrix_to_edges_lists(self):
        for i, node in enumerate(self._graph):
            for y, edge in enumerate(node):
                if(edge == 1):
                    tupl=(i,y)
                    #print("tupl =", tupl, 'reversed =',tupl[::-1])
                    if(tupl in self._edges_list or tupl[::-1] in self._edges_list):
                        continue
                    self._edges_list.append(tupl)

    # Parcours de la matrice pour établir le degres de chaque sommet
    def set_degrees(self):
        # Loop sur chaque sommet
        for i, row in enumerate(self._graph):
            degrees_count = 0
            # Calcul du degré de ce sommet
            for cell in row:
                if(int(cell) == 1):
                    degrees_count+=1
            self._degrees[i] = degrees_count

    # Retourne une matrice d'adjascence trié par degrees (decroissant)
    def order_by_degree(self):
        tmp_graph = [x[:] for x in self._graph]
        tmp_degrees = [x for x in self._degrees]
        for i, d in enumerate(self._degrees):
            # On prend le 1er plus grand (max())
            self._sorted_graph.append(tmp_graph[tmp_degrees.index(max(tmp_degrees))])
            # Suppression du noeud examiné dans le graphe temporaire
            tmp_graph.remove(tmp_graph[tmp_degrees.index(max(tmp_degrees))])
            # Suppression du noeud examiné dans le tableau des degrees 
            del tmp_degrees[tmp_degrees.index(max(tmp_degrees))]
            
    # Calcul du nombre chromatique et attribution des couleurs
    def get_chromatic_number(self):
        # Indice du dernier noeud qui a été coloré (par indice) 
        last_colored_index = 0
        # Tant que tout les noeuds ne sont pas colorés
        while(self._colors.count('F') != 0):
            print("Coloration de début de tour de %d avec la couleur %d" % (self._colors.index('F'), self.chromatic_number))
            # Selection du premier noeud non colorié
            print("Sorted_graph indice:",self._sorted_graph_index)
            last_colored_index = self._colors.index('F')
            #On colorie le premier noeud non-colorié

            self._colors[self._colors.index('F')] = self.chromatic_number
            # Parcours des noeuds du graphe trié
            for i, node in enumerate(self._sorted_graph_index):
                
                print("TOUR",i)
                # Si le noeud n'est pas coloré (F = pas de couleur)
                if(self._colors[i] == 'F'):
                    print(self._sorted_graph_index[i], 'non coloré')
                    # On parcours tout les noeuds portant la couleur actuelle
                    indices = [t for t, x in enumerate(self._colors) if x == self.chromatic_number]
                    print("indice des noeuds portant la couleur", self.chromatic_number, " :", indices)

                    intersect = False
                    # On parcours les noeuds _sorted_graph_indes[indice] qui ont la couleur en cours
                    # pour voir si ils intersectent avec le noeud choisit _sorted_graph_index[i]
                    for colored_indice in indices:
                        print("subtour ", i,"test sur graph", self._sorted_graph_index[colored_indice],self._sorted_graph_index[i], "==", self._graph[self._sorted_graph_index[colored_indice]][self._sorted_graph_index[i]])
                        if(colored_indice == i):
                            print("%d et %d sont adjacents par boucle" % (self._sorted_graph_index[colored_indice], self._sorted_graph_index[i]))
                            intersect = True
                            
                        elif(self._graph[self._sorted_graph_index[colored_indice]][self._sorted_graph_index[i]] == 1):
                            print("%d et %d sont adjacents" % (self._sorted_graph_index[colored_indice], self._sorted_graph_index[i]))
                            intersect = True
                        else:
                            print("%d et %d ne sont pas adjacents" % (self._sorted_graph_index[colored_indice], self._sorted_graph_index[i]))
                    # Si pas de voisin (adjacent) trouvé, on colore le noeuds
                    if(intersect == False):
                        print("%d et %d ne sont pas adjacents" % (self._sorted_graph_index[colored_indice], self._sorted_graph_index[i]))
                        print('Coloration de %d avec la couleur %d' % (self._sorted_graph_index[i], self.chromatic_number))
                        self._colors[i] = self.chromatic_number
                        last_colored_index = i
                    else:
                        print('Rien a colorié ce subtour\n')
                else:
                    print('Noeud', i,"du graphe trié déjà colorié\n")
            # On augmente le nombre chromatique car on a parcouru la liste en entier
            self.chromatic_number+=1

        print('____________________')
        copy_color = self._colors.copy()
        copy_index = self._sorted_graph_index.copy()
  
        temp = [0] * len(copy_color); 
  
        for i in range(0,len(copy_color)): 
            temp[copy_index[i]] = copy_color[i]
      
        # Copy temp[] to arr[] 
        for i in range(0,len(copy_color)): 
            copy_color[i] = temp[i] 
            copy_index[i] = i 
          
        print(copy_color)
        self._colors = copy_color

    # text to array
def changeGraph(text):
    print("\n\nCHANGING")
    
    tmp = list(ast.literal_eval(text))
          
    test = convert(text)
            
    test = edges_lists_to_matrix(test)

    fig = pyplot.figure(1); pyplot.clf()
    fig.canvas.set_window_title('Calcul de nombre chromatique')

    #fig.canvas.manager.toolbar._Button("PREVIOUS", "back_large", print('ok'))
    axbox = pyplot.axes([0.1, 0.05, 0.8, 0.075])
    text_box = TextBox(axbox, 'Input', initial=text)
    ax1 = fig.add_subplot(111)

    allInOne(test,text_box,ax1)
        
def convert(in_str):
    result = []
    current_tuple = []
    for token in in_str.split(","):
        number = int(token.replace("(","").replace(")", ""))
        current_tuple.append(number)
        if ")" in token:
            result.append(tuple(current_tuple))
            current_tuple = []
    return result     

def edges_lists_to_matrix(text):
    size = 0
    for tupl in text:
        if(size < max(tupl)):
            size = max(tupl)
    size +=1
    matrix = [[0 for col in range(size)] for row in range(size)]

    if(text == [] or text == None):
        print("ERROR: no edge list to convert")
        return -1

    for tupl in text:
        matrix[tupl[0]][tupl[1]] = 1
        matrix[tupl[1]][tupl[0]] = 1
    return matrix  

def allInOne(graph,text_box,ax1):
  
    # Création de l'instance graphe
    G = Graph(graph)

    # Création et calcul du tableau de degrees
    G.set_degrees()

    # Trie du graph
    G._sorted_graph_index = sorted(range(len(G._colors))
        , key=lambda k : G._degrees[k], reverse=True)

    print(G._graph)
    
    G.order_by_degree()

    print("\n\nTableau d'index du graphe trié: \n",G._sorted_graph_index)
    print(G._sorted_graph,'\n\n')
    print('____________________\n')
    print(G.OKBLUE+'Début de la coloration du graphe:'+G.ENDC)
    
    G.get_chromatic_number()

    print("\nCouleur du graphe:", G._colors)
    print(G.OKBLUE+"Nombre chromatique:"+G.OKGREEN, G.chromatic_number, G.ENDC)

    G._color_lemma_list = [_color_list[G._colors[i]] for i in range(0, G.V)]

    G.matrix_to_edges_lists()
        
    print('EDGES_LIST IS :', G._edges_list, '\n')

    print('taille du graphe: ', G.V)
    G2 = nx.path_graph(G.V)
    
    G2.add_edges_from(G._edges_list)
    print(G2.edges())

    pos = nx.spring_layout(G2, iterations=50) 
    nx.draw(G2, pos=pos, node_color=G._color_lemma_list, with_labels=True, ax=ax1)

    text_box.on_submit(changeGraph)
    pyplot.show()
  

#### SUITE: - Coloré le 1er noeud de la liste
###         - dans lordre de la liste, jusqu'a la fin, parcourir les noeuds 
###           en essayant d'attribué la meme couleur a un noeud non adjacent
###           au noeud en cours de traitement et non coloré
###         - Quand fin de liste, reprendre étape 1 avec une autre couleur
###         - Fin quand tout les noeuds sont colorés

if __name__ == '__main__':

    _color_list = ['blue', 'red', 'yellow', 'green','purple']
    
    #changeGraph('(0, 1),(1, 2)')
    #changeGraph('(0, 1),(1, 2),(2,3)')
    changeGraph('(0, 1),(0, 3),(0, 4),(1, 2),(2, 3),(3, 4)')

    