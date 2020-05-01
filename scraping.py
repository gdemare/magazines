#!/usr/bin/env python
# coding: utf-8

# In[15]:


##############################################
#### COMMUN
##############################################


# In[40]:


import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date
import chardet
import html


# In[53]:


# date d'ajout
dateAjout = date.today().strftime("%Y/%m/%d")
#database
conn = sqlite3.connect('kiosque.db')
c = conn.cursor()


# In[42]:


# obtenir la liste des articles
def riviere (site, onglets):
    print('Obtention des liens des articles...')
    riviere = []
    for onglet in onglets:
        requete = site + onglet
        riviere.append(pageHTML(requete))
    return riviere


# In[43]:


def pageHTML (site):
    page = requests.get(site)
    soup = BeautifulSoup(page.content.decode('UTF-8'), 'html.parser')
    return soup


# In[44]:


##############################################
#### National Geographics
##############################################


# In[45]:


# Renvoie les urls des articles a telecharger et l'unite du 'avancement du chargement
def natgeoURL (liens):
    # ajouter les liens nouveaux
    c.executemany('''INSERT OR REPLACE INTO natgeo (url) VALUES (?)''', liens )
    conn.commit()
    # articles a ajouter
    articles = c.execute('SELECT url FROM natgeo WHERE dateAjout IS NULL;')
    articles = list(articles)
    #Compteur pour suivre l'evolution
    compteur = c.execute('SELECT count(*) FROM natgeo WHERE dateAjout IS NULL;').fetchone()[0]
    unite = round(compteur/10,0)
    print('0 % Debut du telechargement des donnnee...')
    return articles, unite


# In[46]:


print('National Geographique')
site = "https://www.nationalgeographic.fr/"
onglets = ['animaux', 'environnement', 'espace', 'sciences']

# liens des articles
liens = []
river = riviere(site, onglets)
for i in range(0,len(onglets)):
    articles = river[i].findAll(class_='card-item')
    for j in articles:
        lien = j.find('a', href=True)['href']
        if lien.find('video')==-1 and lien.find(onglets[i])==1 and site+lien[1:]!=site+onglets[i] :
            liens.append([site + lien[1:]])

# liens des articles a ajouter
articles, unite = natgeoURL(liens)

# telechargement des articles
insertion = []
i = 0

for article in articles:
    #compteur information pourcentage avancement
    if i%unite == 0:
        print(i*10/unite, ' %')
    i = i + 1
    # telecharger la page
    url = article[0]
    soup = pageHTML(url)
    # titre
    titre = soup.find(class_ = 'ngart-hl__title').get_text()
    titre = titre
    # categorie
    debut = len(site)
    fin = debut + url[debut:].find('/')
    categorie = url[debut:fin]
    # date
    annee = url[fin+1:fin+5]
    mois = url[fin+6:fin+8]
    if soup.find(class_ = 'ngart-hl__date') is None :
        jour = '1'
    else :
        jourDeb = soup.find(class_ = 'ngart-hl__date').get_text().find(' ')+1
        jour = soup.find(class_ = 'ngart-hl__date').get_text()[jourDeb:jourDeb+2] 
    if len(jour.strip())==1 :
        jour = '0'+jour.strip()
    dateArticle = annee+'/'+mois+'/'+jour
    # description
    description = soup.find(class_ = 'ngart-hl__deck').get_text()
    description = description
    # auteur
    auteur = soup.find(class_ = 'ng-sharekit__contributors').get_text()
    auteur = auteur
    # contenu de l'article
    contenu = soup.find(class_= 'article-cntr')
    contenu = str(contenu)
    #charger
    insertion.append([dateAjout, url, categorie, dateArticle, titre, description, auteur, contenu])
print('100.0%')
# Charger les articles dans la bdd
c.executemany('''REPLACE INTO natgeo (dateAjout, url, categorie, date, titre, description, auteur, article) VALUES (?,?,?,?,?,?,?,?)''', insertion)
conn.commit()


# In[27]:


##############################################
#### Le Monde
##############################################


# In[48]:


# Renvoie les urls des articles a telecharger et l'unite du 'avancement du chargement
def lemondeURL (liens):
    # ajouter les liens nouveaux
    c.executemany('''INSERT OR REPLACE INTO lemonde (url) VALUES (?)''', liens )
    conn.commit()
    # articles a ajouter
    articles = c.execute('SELECT url FROM lemonde WHERE dateAjout IS NULL;')
    articles = list(articles)
    #Compteur pour suivre l'evolution
    compteur = c.execute('SELECT count(*) FROM lemonde WHERE dateAjout IS NULL;').fetchone()[0]
    unite = round(compteur/10,0)
    print('0 % Debut du telechargement des donnnee...')
    return articles, unite


# In[57]:


print('Le Monde')
site = "https://www.lemonde.fr/"
onglets =  ['economie', 'international', 'politique', 'societe', 'planete', 'sciences']

# obtenir la liste des articles
liens = []
river = riviere(site, onglets)
for i in range(0,len(onglets)):
    articles = river[i].find(id='river')
    for lien in articles.findAll('a', {'class' : 'teaser__link'} ,href=True):
        if "/article/" in lien['href']:
            liens.append([lien['href']])

# liens des articles a ajouter
articles, unite = lemondeURL(liens)

# telechargement des articles
insertion = []
i = 0
for article in articles:
    #compteur information pourcentage avancement
    if i%unite == 0:
        print(i*10/unite, ' %')
    i = i + 1
    # telecharger la page
    url = article[0]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # titre
    titre = soup.find(class_ = {'article__heading', 'article__header'}).find(class_ = 'article__title').get_text()
    # description
    description = soup.find(class_ = 'article__desc').get_text()
    # auteur
    auteur = soup.find(class_ = {'article__author-link', 'article__author-identity', 'meta__author'})
    if auteur is None:
        auteur = ''
    else :
        auteur = auteur.get_text()
    # type d'article
    if not soup.find(class_ = 'article__section') is None:
        arType = soup.find(class_ = 'article__section').get_text()
    else :
        arType = 'Article'
    # contenu de l'article
    article = soup.findAll(class_=  ['article__paragraph', 'article__sub-title'])
    contenu = ''
    for paragraphe in article:
        contenu = contenu + str(paragraphe)
    # date d'ajout
    dateAjout = date.today().strftime("%Y/%m/%d")
    # categorie
    leMonde = "https://www.lemonde.fr/"
    debut = len(leMonde)
    fin = url.find("/article/")
    categorie = url[debut:fin]
    # date de publication
    debut = url.find("/article/") + len("/article/")
    fin = debut + 10
    dateArticle = url[debut:fin]
    #charger
    insertion.append([dateAjout, url, arType, categorie, dateArticle, titre, description, auteur, contenu])
print('100.0%')

# Charger les articles dans la bdd
c.executemany('''REPLACE INTO lemonde (dateAjout, url, type, categorie, date, titre, description, auteur, article) VALUES (?,?,?,?,?,?,?,?,?)''', insertion)
conn.commit()


# In[ ]:


conn.close()

