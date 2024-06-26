# Test de la modélisation de paramètres


# Format des données
# index = permet d'identifier les paramètres ou donner un ordre
# domain : le domaine d'application de paramètre
# sub-domain : 
# name : son nom raccourcis, domain+name = Identifiant unique

# Cette description n'indique pas de codage
#class P:
#    __init__(self,id,):
class SyntaxNode:
    def __init__(self,id,name):
        self.id = id # Identifiand du noeud, quelques lettres en majuscule
        self.name = name
        self.nodes = [] # Noeuds fils

    # Décode la description d'un noeud et crée un nouveau noeud
    @staticmethod
    def new(line):
        line = line.lstrip()
        content = line.split(':')
        return SyntaxNode(content[0],content[1])

    # Ajoute un noeud fils
    def append(self,node):
        self.nodes.append(node)

    def __repr__(self) -> str:
        return '{'+self.id+','+self.name+','+str(self.nodes)+'}'


class Syntax:
    def __init__(self,path):
        self.nodes = []
        self.load(path)

    
    # Charge une syntaxe de puis le fichier
    def load(self,path):
        current_level = 0
        space_per_level = 0
        current_node = None
        with open(path,"r") as file:
            for line in file:
                line = line.rstrip()
                # Determine le niveau
                level = len(line)-len(line.lstrip())
                # Trouve le nombre d'espaces par niveau
                if level != 0:
                    if space_per_level == 0:
                        space_per_level = level
                        level = 1
                    else:
                        # Calcule le niveau par comptage du nombre d'espaces
                        level = int(level / space_per_level)
                # Si on retourne au niveau 0 on redémmage avec un nouveau noeud racine
                if level == 0:
                    # Nouveau noeud de niveau zéro
                    node = SyntaxNode.new(line)
                    self.nodes.append(node)
                    current_node = node
                    current_level = 0
                else:
                    if level == current_level:
                        # Ajoute un noeud au noeud courant
                        current_node.append(SyntaxNode.new(line))
                    elif level == current_level + 1:
                        # Descent d'un niveau 
                        node = SyntaxNode.new(line)
                        # Ajoute ce nouveau noeud au noeud courant
                        current_node.append(node)
                        # met à jour le suivit
                        current_level = level
                        current_node = node
                #print(level,line)

syntax = Syntax("dx7_meaning.txt")
print(vars(syntax))