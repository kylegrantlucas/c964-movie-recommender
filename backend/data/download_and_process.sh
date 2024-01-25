#!/bin/bash

mkdir tmp

cd tmp || exit

# download dataset from kaggle
kaggle datasets download -d ashirwadsangwan/imdb-dataset

# unzip dataset
unzip imdb-dataset.zip

# remove zip file
rm imdb-dataset.zip

# generate timestamp for file
timestamp=$(date +%s)

# proceess with xsv
xsv fixlengths title.basics.tsv/data.tsv > title.basics.tsv/data.fixed.csv
xsv search --select titleType movie title.basics.tsv/data.fixed.csv > title.basics.tsv/data.movies.csv
xsv join 1 title.basics.tsv/data.movies.csv 1 title.ratings.tsv/data.tsv | xsv search --select isAdult 0 | xsv select 1,3,4,6,7,8,9,11,12 > imdb_final.csv

xsv search --select region US title.akas.tsv/data.tsv > eng_titles.csv
xsv join 1 imdb_final.csv 1 eng_titles.csv | xsv select 1,2,3,4,5,6,7,8,9 > imdb_eng_final.csv

awk '!seen[$0]++' imdb_eng_final.csv > imdb_$timestamp.csv

# rename first column from tconst to imadbID
sed -i'.bak' '1s/tconst/imdbID/' imdb_$timestamp.csv

cd .. || exit
mv tmp/imdb_$timestamp.csv imdb.csv
rm -rf tmp