##############################################################
#
# File :- BusinessLogic.py
#
#Description :- This file will call the tsp algorithm for
#calculation of optimal path
#
#Author :- Team Fantastic4
#
###############################################################

from __future__ import absolute_import
import try_tsp
from itertools import tee, islice, chain, izip

import argparse

parser1 = argparse.ArgumentParser(conflict_handler='resolve')


def setParameters(userDestination):

    parser1.add_argument('--Destination', default = userDestination, type = int,
                         help='No of Destination User wants to travel.')
    parser1.add_argument('--tsp_use_random_matrix', default=True, type=bool,
                         help='Use random cost matrix.')
    parser1.add_argument('--tsp_random_forbidden_connections', default = 0,
                        type = int, help='Number of random forbidden connections.')
    parser1.add_argument('--tsp_random_seed', default = 0, type = int,
                        help = 'Random seed.')
    parser1.add_argument('--light_propagation', default = False,
                        type = bool, help = 'Use light propagation')




Uber =[]
Lyft =[]
counter=0


def item_and_next(some_iterable):
    items, nexts = tee(some_iterable, 2)
    nexts = chain(islice(nexts, 1, None), [None])
    return izip(items, nexts)

def Optimalprice(DestinationList):

    Tsp_cor = []
    list = []

    obj = try_tsp.RandomMatrix(len(DestinationList), 0, DestinationList)
    print "hello--->" ,parser1.parse_args()
    Tsp_cor = try_tsp.tsp(parser1.parse_args(), DestinationList)

    print Tsp_cor  #print list of path traversed

    for item, nxt in item_and_next(Tsp_cor):
         if (nxt == None):
             nxt = "0";
         list.append(DestinationList[int(item)][int(nxt)])
         print DestinationList[int(item)][int(nxt)],   #minimum path price
    print list




    return Tsp_cor, list


def CombinedOptimal(pricelistmatrix,type):
    combined = []
    combinedType = []
    global counter
    global Uber
    global Lyft
    priceList = []
    serviceNameList = []
    cordinateList = []

    if type == 'UBER':
        Uber = pricelistmatrix
        counter += 1

    elif type == 'LYFT':
        Lyft = pricelistmatrix
        counter += 1

    if(counter==2):
        counter=0

        for i in range(len(pricelistmatrix)):
            combined.append([])
            combinedType.append([])
            for j in range(len(pricelistmatrix)):
                combined[i].append(0)
                combinedType[i].append("")



        for i in range(len(pricelistmatrix)):
            for j in range(len(pricelistmatrix) ):
                if(Uber[i][j]>Lyft[i][j]):
                    combined[i][j]=Lyft[i][j]
                    combinedType[i][j]='LYFT'


                elif (Uber[i][j]<=Lyft[i][j]):
                    combined[i][j] = Uber[i][j]
                    combinedType[i][j] = 'UBER'

        cordinateList, x =Optimalprice(combined)

        for item, nxt in item_and_next(cordinateList):
            if (nxt == None):
                nxt = "0";

            print combined[int(item)][int(nxt)],
            priceList.append(combined[int(item)][int(nxt)])
            serviceNameList.append(combinedType[int(item)][int(nxt)])
            print combinedType[int(item)][int(nxt)],

    return cordinateList, priceList, serviceNameList
