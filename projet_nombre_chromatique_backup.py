import networkx as nx
import matplotlib.pyplot as pyplot

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

    def matrix_to_lists(self):
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
            print("Coloration de %d avec %d" % (self._colors.index('F'), self.chromatic_number))
            # Selection du premier noeud non colorié
            last_colored_index = self._colors.index('F')
            self._colors[self._colors.index('F')] = self.chromatic_number
            # Parcours des noeuds du graphe
            for i, node in enumerate(self._sorted_graph_index):
                # Si le noeud n'est pas coloré (F = pas de couleur)
                if(self._colors[self._sorted_graph_index[i]] == 'F'):
                    # On parcours tout les noeuds portant la couleur actuelle
                    indices = [t for t, x in enumerate(self._colors) if x == self.chromatic_number]
                    intersect = False
                    # On parcours les noeuds qui ont la même couleur
                    for indice in indices:
                        if(self._graph[self._sorted_graph_index[indice]][self._sorted_graph_index[i]]== 1):
                            print("%d et %d sont adjacents" % (self._sorted_graph_index[indice], self._sorted_graph_index[i]))
                            intersect = True
                        else:
                            print("%d et %d ne sont pas adjacents" % (self._sorted_graph_index[indice], self._sorted_graph_index[i]))
                    # Si pas de voisin (adjacent) trouvé, on colore le noeuds
                    if(intersect == False):
                        print('Coloration de %d avec %d' % (self._sorted_graph_index[i], self.chromatic_number))
                        self._colors[self._sorted_graph_index[i]] = self.chromatic_number
                        last_colored_index = self._sorted_graph_index[i]
            # On augmente le nombre chromatique car on a parcouru la liste en entier
            self.chromatic_number+=1
        print('____________________')

#### SUITE: - Coloré le 1er noeud de la liste
###         - dans lordre de la liste, jusqu'a la fin, parcourir les noeuds 
###           en essayant d'attribué la meme couleur a un noeud non adjacent
###           au noeud en cours de traitement et non coloré
###         - Quand fin de liste, reprendre étape 1 avec une autre couleur
###         - Fin quand tout les noeuds sont colorés

if __name__ == '__main__':
    '''_graph = [[0,1,0,1],
                [1,0,1,0],
                [0,1,0,1],
                [1,0,1,0]]
    '''

    _color_list = ['blue', 'red', 'yellow', 'green','purple']
    _graph = [[0,1,0,1,1],
            [1,0,1,0,0],
            [0,1,0,1,0],
            [1,0,1,0,1],
            [1,0,0,1,0]]

    # Création de l'instance graphe
    G = Graph(_graph)
    # Création et calcul du tableau de degrees
    G.set_degrees()
    print(G._graph)
    G._sorted_graph_index = sorted(range(len(G._colors))
        , key=lambda k : G._degrees[k], reverse=True)

    # Création du graphe trié et du tableau d'indice trié,
    # en fonction des degrées (décroissant)
    G.order_by_degree()

    print("\n\nTableau d'index du graphe trié: \n",G._sorted_graph_index)
    print(G._sorted_graph,'\n\n')
    print('____________________')
    G.get_chromatic_number()
    print("\nCouleur du graphe:", G._colors)
    print("Nombre chromatique: ", G.chromatic_number)

    G._color_lemma_list = [_color_list[G._colors[i]] for i in range(0, G.V)]

    G.matrix_to_lists()
    print('EDGES_LIST IS ', G._edges_list, '\n')

    G2 = nx.path_graph(G.V)
    G2.add_edges_from(G._edges_list)
    fig = pyplot.gcf()
    fig.canvas.set_window_title('Coloration de graphes')
    nx.draw(G2, node_color=G._color_lemma_list, with_labels=True)
    pyplot.show()

