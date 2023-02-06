import codecs #permet l'importation de fichier à lire
from urllib.error import HTTPError #valeur de retour pour des cas particulier
from urllib.request import urlopen #permet de tester l'ouverture des pages
from urllib.parse import quote #decompose les elt d'une URL pour faire une URL "absolue"
from bs4 import BeautifulSoup #bibliothèque python pour lire XML et HTML

fichier = "new 1.txt" #nom du fichier txt utilisé
with codecs.open(fichier,"r","utf8") as f:
    text = f.readlines() #va lire chaque ligne par ligne

recherche ={} #recherche dans le dico
tlfi = "https://www.cnrtl.fr/definition/"
larouss = "https://www.larousse.fr/dictionnaires/francais/"
wiki = "https://fr.wiktionary.org/wiki/"

for mot in text: #boucle pour tester chaque mot
    mot = mot.strip() #va lire uniquement le mot marqué tel quel
    url = larouss + quote(mot) #assigne la variable larousse + quote qui est le mot du fichier txt
    page = urlopen(url)
    bs = BeautifulSoup(page.read(), "html.parser") 
    definition = bs.find("li",{"class":"DivisionDefinition"}) #dirige le script dans la page url
    recherche[mot] = definition
    if recherche[mot] == None: #boucle qui met une condition pour rediriger vers un autre site
        url = tlfi + quote(mot)
        page = urlopen(url)
        bs = BeautifulSoup(page.read(), "html.parser")
        definition = bs.find("span",{"class":"tlf_cdefinition"}) #dirige le script dans la page url
        recherche[mot] = definition
        
        if recherche[mot] == None: #boucle qui met une condition pour rediriger vers un autre site
            url = wiki + quote(mot)
            try: #demande d'essayer ça 
                page = urlopen(url)
            except HTTPError: #permet de continuer le script meme si la definition n'est pas trouvé après les 3 sites
                #print("la definition n'est pas trouvéé", url)
                recherche[mot] = "Malheureusement, aucune définition n'a été trouvé sur Larousse, Wikidictionary ou TLFI" 
            else: 
                bs = BeautifulSoup(page.read(),"html.parser")
                definition = bs.find("dd")
                recherche[mot] = definition
                if recherche[mot] == None:
                    recherche[mot] = "None"     
                else:
                    recherche[mot] = definition.get_text() #on demande uniquement la definition, pas les elt de codage autour
                    #print(mot, ":", definition.get_text())
        else:
            recherche[mot] = definition.get_text()#on demande uniquement la definition, pas les elt de codage autour
            #print(mot, ":", definition.get_text())
    else:
        recherche[mot] = definition.get_text()#on demande uniquement la definition, pas les elt de codage autour
        #print(mot+":", definition.get_text())
        
resultat = "final1.txt" #fichier txt où sera écrit le rendu
with codecs.open(resultat, "w", "utf8") as h: #boucle pour ouvrir un fichier txt et lui donner un format
    for elt in recherche: #boucle pour repéter l'odre suivant
        #print(elt, recherche[elt])
        h.write(elt+"\t"+ recherche[elt]+"\n") #écrit chaque mot, un espace, sa definition, un retour ligne 