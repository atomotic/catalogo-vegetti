# catalogo-vegetti
various scripts to scrape, refine, reconcile data from Vegetti catalogue


## scrape-authors

scrape authors from http://www.fantascienza.com/catalogo/autori/

	$ parallel -j 10 python scrape-authors.py ::: `echo {A..Z}`