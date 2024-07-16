# Teste simple inspiré du site
# https://pageperso.lis-lab.fr/benoit.favre/pstaln/01_pytorch-mlp.html
# Le but de ce test est d'apprendre un reseau à déterminer si des points sont dans un cercle 
# Le cercle est centré sur zéro et de taille 1
# La sortie est la valeur de la classe 1 si c'est dans le cercle
# Le réseau n'a qu'une couche donc ne réussi pas à trouver
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import TensorDataset, DataLoader


# Fonction de création des exemples d'apprentissage ou de validation
def createSample(n):
    # Création de n exemples dans l'espace [-1,5, + 1,5]
    # Attention il faut que le nombre d'exemples soient un multipe du batch sinon lors de l'apprentissage le dernier batch sera imcomplet
    # Il existe un paramètre dans le Dataloader "droplast" à mettre à true pour cela
    X = torch.rand(n, 2) * 3 - 1.5

    # Création d'un tenseur qui contient les étiquettes
    # C'est 1 si la somme des carrée des 2 paramètres est inférieur à 1
    Y = X[:,0] ** 2 + X[:,1] ** 2 < 1

    # Transformer le tableau Y de True et False en entiers longs
    # NB: pour connaitre le type des données d'un tenseur pyTorch 
    #print(Y.type())
    Y = Y.long()
    #print(Y.type())
    # Visualisation du résultat
    #show(X,Y)
    return X,Y

# Visualise une séquence de points X avec 2 classes 0 ou 1 en Y
def show(X,Y):
    plt.scatter(X[:,0], X[:,1], c=Y)
    plt.show()

# Création d'un modele avec une seule couche avec 2 entrée et 2 étiquettes de sortie
# Le constructeur construit la couche
# La méthode forward passe à travers de la couche
class LinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Linear(2, 2)
    def forward(self, x):
        return self.l1(x)

# Fonction de calcul de l'apprentissage
# Passer le modèle et le nombre d'épochs (tours)
def fit(model, epochs):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())
    # Nombre d'époch
    for epoch in range(epochs):
        total_loss = 0
        num = 0
        for x, y in train_loader:
            # Reset les gradiants
            optimizer.zero_grad()
            # Calcule le score de ce batch
            y_scores = model(x)
            # Calcule la cross entropie sur les valeurs du batch
            loss = criterion(y_scores, y)
            # Propage la loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            num += len(y)
        if epoch % (epochs // 10) == 0:
            # Affiche le loss moyen
            print(epoch, total_loss / num)

# Partie principale

# Création du modèle
model = LinearModel()

# Mise en place des données d'apprentissage : les points avec la classe
X,Y = createSample(1000)
train_set = TensorDataset(X, Y)

# Mise en place du date loader avec une taille de batch et un choix random par batch
train_loader = DataLoader(train_set, batch_size=4, shuffle=True)

epochs = 50
print('Lance le modèle sur',epochs,'epochs')
fit(model,epochs)

# Verification des résultats sur un autre 