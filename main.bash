#!/bin/bash
dossier='/home/guigui/Applications/magazines/'
cd $dossier

# recuperer les donnnes
echo 'Telecharger les derniers articles (y) :'
read telecharger
if [ $telecharger = 'y' ]; then
	echo 'Scraping des donnees...'
	python3 scraping.py
fi

# extraction et affichage des articles
echo 'Afficher les articles d un jour pour Le Monde.'
echo '......................du dernier mois ouvrant pour National Geographics.'
echo 'Mettre a jour les articles disponibles (y) :'
read update
if [ update='y' ]; then
	python3 printing.py
fi
