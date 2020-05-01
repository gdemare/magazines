#!/usr/bin/env python
# coding: utf-8

# importer les library 
import sqlite3
from yattag import Doc
import datetime
import os
import glob

# connection a la database
conn = sqlite3.connect('kiosque.db')
c = conn.cursor()

# demander a l'utilisateur de la date du journal
print('Date des articles (par defaut la date d aujourd hui) (aaaa-mm-jj) :')
dateSaisie = input()
if dateSaisie=='' :
    dateSaisie = datetime.date.today()
dateMoisOuvr = dateSaisie + datetime.timedelta(-31)
dateSaisie = dateSaisie.strftime("%Y/%m/%d")
dateMoisOuvr = dateMoisOuvr.strftime("%Y/%m/%d")

# supprimer les anciens fichiers
journaux = [ 'le monde', 'national geographic']
for i in journaux:
    for j in glob.glob('news-papers/' + i + '/' + '*html'):
        os.remove(i)

# recupere les articles
print(dateSaisie)
leMonde = c.execute('''SELECT * FROM lemonde where date=? ORDER BY categorie;''', (dateSaisie,) )
leMonde = list(leMonde)
natGeo = c.execute('''SELECT  * FROM natgeo where date>=? ORDER BY categorie;''', (dateMoisOuvr,) )
natGeo =list(natGeo)

# categories des articles
def categories (liste ,colonne):
    categories = []
    for i in liste:
        categories.append(i[colonne])
    categories = set(categories)
    return categories

catLeMonde = categories(leMonde, 4)
catNatGeo = categories(natGeo, 3)


############## Le Monde################
#creer les balises de l'index
def indexLeMonde (leMonde, catLeMonde):
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):   
        with tag('head'):
            with tag('script', type="text/javascript", src="https://www.w3schools.com/lib/w3.js"):
                text()
            with tag('script', type="text/javascript", src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"):
                text()
            with tag('script', type="text/javascript", src="script.js"):
                text()
            doc.stag('link', id="pagestyle", href="style.css", rel="stylesheet")
        with tag('body'):
            with tag('nav'):
                with tag('header'):
                    with tag('div', id='section'):
                        text('Magazines')
                    with tag('div', id='titre'):
                        text('Le Monde')
            with tag('section', id="menuPanel"):
                with tag('div', id="menu"):
                    with tag('h2'):
                        text('Categories')
                    with tag('div', id='tuile'):
                        text('Tous')
                    for categorie in catLeMonde:
                        with tag('div', id=categorie):
                            text(categorie)
            with tag('section', id="page"):
                with tag('article', id="contenu"):
                    for article in leMonde :
                        with tag('div', klass='tuile ' + article[4]):
                            with tag('a', klass="liste", href= 'le-monde/' + str(article[0]) + '.html'):
                                with tag('ul'):
                                    with tag('li'):
                                        text(article[4] )
                                    with tag('li'):
                                        text(article[3])
                                with tag('h1'):
                                    text(article[6])
                                with tag('p', klass='description'):
                                    text(article[7])

    index = doc.getvalue()
    # enregistrer le fichier
    open('news-papers/le-monde.html', 'w').close()
    fichier = open('news-papers/le-monde.html', "a")
    fichier.write(index)
    fichier.close()

def indexNatGeo (natGeo, catNatGeo):
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):   
        with tag('head'):
            with tag('script', type="text/javascript", src="https://www.w3schools.com/lib/w3.js"):
                text()
            with tag('script', type="text/javascript", src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"):
                text()
            with tag('script', type="text/javascript", src="script.js"):
                text()
            doc.stag('link', id="pagestyle", href="style.css", rel="stylesheet")
        with tag('body'):
            with tag('nav'):
                with tag('header'):
                    with tag('div', id='section'):
                        text('Magazines')
                    with tag('div', id='titre'):
                        text('National Geographic')
            with tag('section', id="menuPanel"):
                with tag('div', id="menu"):
                    with tag('h2'):
                        text('Categories')
                    with tag('div', id='tuile'):
                        text('Tous')
                    for categorie in catNatGeo:
                        with tag('div', id= categorie):
                            text(categorie)
            with tag('section', id="page"):
                with tag('article', id="contenu"):
                    for article in natGeo :
                        with tag('div', klass='tuile ' + article[3]):
                            with tag('a', klass="liste", href= 'national-geographic/' + str(article[0]) + '.html'):
                                with tag('ul'):
                                    with tag('li'):
                                        text(article[3] )
                                with tag('h1'):
                                    text(article[5])
                                with tag('p', klass='description'):
                                    text(article[6])

    index = doc.getvalue()
    # enregistrer le fichier
    open('news-papers/national-geographic.html', 'w').close()
    fichier = open('news-papers/national-geographic.html', "a")
    fichier.write(index)
    fichier.close()

# Article du Monde
def articleLeMonde (leMonde, catLeMonde):
    for article in leMonde:
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('head'):
                doc.stag('link', id="pagestyle", href="../style-article.css", rel="stylesheet")
            with tag('body'):
                with tag('header'):
                    with tag('ul', id = 'metadata'):
                        with tag('li'):
                            text('Categorie : ', article[4] )
                        with tag('li'):
                            text('Type : ', article[3])
                with tag('section'):
                    with tag('h1'):
                        text(article[6])
                    with tag('p', id = 'description'):
                        text(article[7])
                    doc.asis(article[9])
                with tag('footer'):
                    with tag('ul'):
                        with tag('li'):
                            with tag('a', href = article[2], target="_blank"):
                                text('Publie sur Le Monde le ', article[5])
                        with tag('li'):
                            text('Ajoute le ', article[1])
                        with tag('li'):
                            text('Auteur(s) ', article[8])
        fichier = doc.getvalue()
        # enregistrer dans le fichier
        html = 'news-papers/le-monde/'+ str(article[0]) + ".html"
        open(html, 'w').close()
        article = open(html, "a")
        article.write(fichier)
        article.close()

################ National Geographic
def articleNatGeo (natGeo, catNatGeo):
    for article in natGeo:
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('head'):
                doc.stag('link', id="pagestyle", href="../style-article.css", rel="stylesheet")
            with tag('body'):
                with tag('header'):
                    with tag('ul', id = 'metadata'):
                        with tag('li'):
                            text('Categorie : ', article[3] )
                with tag('section'):
                    with tag('h1'):
                        text(str(article[5]))
                    with tag('p', id = 'description'):
                        text(str(article[6]))
                    doc.asis(str(article[8]))
                with tag('footer'):
                    with tag('ul'):
                        with tag('li'):
                            with tag('a', href = article[2], target="_blank"):
                                text('Publie le ', article[4])
                        with tag('li'):
                            text('Ajoute le ', article[1])
                        with tag('li'):
                            text('Auteur(s) ', str(article[7]))

        fichier = doc.getvalue()
        # enregistrer dans le fichier
        html = 'news-papers/national-geographic/'+ str(article[0]) + ".html"
        open(html, 'w').close()
        document = open(html, "a")
        document.write(fichier)
        document.close()

indexLeMonde (leMonde, catLeMonde)
indexNatGeo(natGeo, catNatGeo)

articleNatGeo(natGeo, catNatGeo)
articleLeMonde(leMonde, catLeMonde)
