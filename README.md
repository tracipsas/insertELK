# InsertELK

*Dernière version fonctionnelle : 26/10/20*

## Description

Script python récupérant les EXIFs d'images jpg pour les insérer dans une pile ELK.

## Prérequis

### Installation d'exiftool et du module elasticsearch

```
$ sudo apt install libimage-exiftool-perl python3-pip
$ sudo pip3 install elasticsearch
```

## Installation

```
$ git clone https://github.com/tracipsas/insertELK
$ cd insertELK
$ python3 insert.py -d ./dir -i localhost -p 9200 -I indexElastic
```

## Documentation
```
usage: insert.py [-h] [-d DIR] [-i IP] [-p PORT] [-I INDEX]

insert exif on elastic

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     images dir
  -i IP, --ip IP        ip or host elastic
  -p PORT, --port PORT  port elastic
  -I INDEX, --index INDEX
                        index
```
## Remarques

Les `id` des éléments insérés sont simplements une itération. Il peut donc y avoir concurence sur ces ids.
Une release futur devra régler ce soucis.

## Sources
* [Geo-point datatype](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/geo-point.html)
