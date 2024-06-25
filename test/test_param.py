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
        self.id = id
        self.name = name
        self.next_level = []

    def __repr__(self) -> str:
        return '{'+self.id+','+self.name+','+str(self.next_level)+'}'


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
                if level == 0:
                    # Nouveau noeud de niveau zéro
                    node = SyntaxNode('TST',"Test")
                    self.nodes.append(node)
                #print(level,line)

syntax = Syntax("dx7_meaning.txt")
print(vars(syntax))