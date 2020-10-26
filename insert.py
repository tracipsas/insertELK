#!/usr/bin/python3

from elasticsearch import Elasticsearch
import argparse
from os import listdir
from os.path import isfile, join
import subprocess


def connect(ip, port):
    """Méthode de connexion à elastic
    """
    es=Elasticsearch([{'host':ip,'port':port}])
    return es

def parseExif(lines):
    """Méthode de récupération des exif
    """
    results = dict()
    loc_dict = dict()
    for line in lines.decode('UTF-8').split('\n'):
        data = line.split(':')
        if len(line) > 0:
            #transformation des lignes de coordonnées des EXIF en tuple pour elastic
            if "GPS Latitude" in data[0] and not "Ref" in data[0]:
                latitude = data[1].split("'")
                lat = latitude[0].split(" deg ")
                loc_dict['lat'] = float("{}.{}".format(lat[0], lat[1]))
            elif "GPS Longitude" in data[0] and not "Ref" in data[0]:
                longitude = data[1].split("'")
                long = longitude[0].split(" deg ")
                loc_dict['lon'] = float("{}.{}".format(long[0], long[1]))
            else:
                results[data[0].rstrip()] = data[1].rstrip('\n').rstrip()
    if 'lat' in loc_dict and 'lon' in loc_dict:
        results['location'] = loc_dict
    return results

def main(path, ip, port, index):
    """méthode principale appelant la methode parseExif(lines) pour chaque fichier jpeg trouvé
    """
    #settings du champs location pour l'index elastic afin de pouvoir utiliser la carte de kibana
    settings = {
"mappings": {
    "properties": {
    "location": {
        "type": "geo_point"
    }
    }
}
}
    #connection à elastic
    es = connect(ip=ip, port=port)
    #création de l'index
    es.indices.create(index, body=settings)
    #liste des fichiers
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    i = 1
    for onlyfile in onlyfiles:
        cmd = "exiftool {}".format(onlyfile)
        #analyse de la sortie de la commande exiftool
        data = parseExif(lines=subprocess.check_output(cmd, shell=True))
        #insertion du dictionnaire de sortie de la commande précédente dans l'index elastic
        res = es.index(index=index,id=i,body=data)
        i += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='insert exif on elastic')
    parser.add_argument('-d', '--dir', help='images dir')
    parser.add_argument('-i', '--ip', help='ip or host elastic')
    parser.add_argument('-p', '--port', help='port elastic')
    parser.add_argument('-I', '--index', help='index')
    args = parser.parse_args()
    main(path=args.dir, ip=args.ip, port=args.port, index=args.index)
