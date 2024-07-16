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
        # Ouverture du fichier
        self.file = open(path,"r")
        # Lance l'appel récursif
        self.loadRec(self.root,0)
        # lecture du premier noeud
        line = file.readline()
        line = line.rstrip()
        # Determine le niveau en calculant le nombre de caractères vides au début de la ligne
        linelevel = len(line)-len(line.lstrip())
        # récupère d'arbre de cette ligne
        newNode = self.loadRec(line,linelevel)
        # Ajoute ce noeud
        self.nodes.append(newNode)

            for line in file:
                
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

    
    # Chargement recursif à partir de la ligne et d'un niveau
    # Retourne le noeud crée à partir de cette ligne et le reste de l'arbre
    def loadRec(line,level):
        newNode = SyntaxNode.new(line)

        # Lecture d'une ligne du fichier
        line = file.readline()
        # Niveau de la ligne lue
        linelevel = level
        # Test fin de fichier
        while line and linelevel == level:
            # On n'est pas à la fin du fichier
            line = line.rstrip()
            # Determine le niveau en calculant le nombre de caractères vides au début de la ligne
            linelevel = len(line)-len(line.lstrip())
            newNode = SyntaxNode.new(line)
            if linelevel == level:
                node.append(newNode)
            elif linelevel > level:
                # Ce niveau est terminé
                return
            else:
    # Retourne la liste des noeuds de ce niveau
    def parse_tree(current_indent=0):
        nodes = []
        line = file.readline()
        # Tant qu'on n'est pas à la fin du fichier
        while line:
            stripped_line = line.lstrip()
            indent_level = len(line) - len(stripped_line)
            # 
            if indent_level < current_indent:
                break
            
            node = TreeNode(int(stripped_line))
            if lines and len(lines[0]) - len(lines[0].lstrip()) > indent_level:
                node.children = parse_tree(lines, indent_level + 1)
            nodes.append(node)
        
        return nodes





syntax = Syntax("dx7_meaning.txt")
print(vars(syntax))