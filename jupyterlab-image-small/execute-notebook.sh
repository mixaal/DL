#!/bin/bash -x


#jupyter nbconvert --execute Pokus.ipynb  --to notebook
# jupyter nbconvert --execute Pokus.nbconvert.ipynb  --to html

OS_DIR="/tata"
NB_TO_RUN=${NB_TO_RUN:-/tata/cv-19-cz/Covid-19-2021.ipynb}


[ -d "$OS_DIR" ] || {
	echo "Exit since no object store mounted!"
	exit 1
}

ls -l "$OS_DIR"

#[ -z "$NB_TO_RUN" ] && {
#        echo "Notebook to run not defined!"
#        exit 1
#}


cd "$OS_DIR"
jupyter nbconvert --execute "$NB_TO_RUN"  --to notebook

no_ext=$(echo "$NB_TO_RUN" | sed -e 's/.ipynb//')
iso_date=$(date --iso-8601)
mv "${no_ext}.nbconvert.ipynb"  "${no_ext}.${iso_date}.ipynb"

