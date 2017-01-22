##############################################################
#
# File :- Lyft.py
#
#Description :- This file interacts with the lyft API and provides
#the output to calcuate optimal solution
#
#Author :- Team Fantastic4
#
###############################################################

from __future__ import absolute_import
import json

from flask import Flask, render_template, request, redirect, session

import requests
import BusinessLogic



app = Flask(__name__)
app.requests_session = requests.Session()



def generate_ride_headers(token):
    """Generate the header object that is used to make api requests."""
    return {
        'Authorization': 'bearer %s' % token,
        'Content-Type': 'application/json',
    }

def lyftPrice(locationList):
    list1 = ['1', '2', '3', '4']
    lyftpricelistmatrix = []
    print locationList


    for i in range(len(locationList)):
        lyftpricelistmatrix.append([])
        for j in range(len(locationList)):
            lyftpricelistmatrix[i].append(0)
    print lyftpricelistmatrix

    d = {}
    #print "inside"
    url = 'https://api.lyft.com/v1/cost'
    for i in range(len(locationList)-1):
        print '\n'
        counter = int(i)

        for j in range(int(i) + 1, len(locationList), 1):


            param = {
                'start_lat': locationList[i].split(',')[0],
                'start_lng': locationList[i].split(',')[1],
                'end_lat': locationList[j].split(',')[0],
                'end_lng': locationList[j].split(',')[1],
            }
            response = app.requests_session.get(
                url,
                headers=generate_ride_headers('gAAAAABYNRqZS_x7fOJQpH5-qDrtq6-Zyzy8ONTDuWJAFELjruND-Ipbh-aIs9fJ0rgSx9Ljf4rnxXVn6DQscHO1dWj0wfccucXwoqw9uRJpaSrNunPPaEQL3Hh1TFa1sdJ3MOi9_kqKs4XrZU7Ur8ikOFjWrLIZ3R9lyBwbsb2A3c57YnfZg6U='),
                params=param,
            )
            print "inside j Lyft loop: After request"
            if response.status_code != 200:
                return 'There was an error', response.status_code
            print response.json()
            for key, value in response.json().iteritems():
                for x in value:
                    if x['ride_type'] == 'lyft':
                        d = x
            for k, v in d.iteritems():
                if (k == "estimated_cost_cents_min"):
                    lyftpricelistmatrix[int(i)][counter+1] = int(d.get(k))/100.0
                    counter=counter+1

                    #print d.get(k),


    for i in range(len(lyftpricelistmatrix)):
        for j in range(i,len(lyftpricelistmatrix)):
            lyftpricelistmatrix[j][i]=lyftpricelistmatrix[i][j]

    print lyftpricelistmatrix
    lyftOptimalPathList, lyftPriceList = BusinessLogic.Optimalprice(lyftpricelistmatrix)
    BusinessLogic.CombinedOptimal(lyftpricelistmatrix,'LYFT')

    #Logic for User Added Route Output
    useRouteprice = []
    for s in range(len(lyftpricelistmatrix) - 1):

        value = lyftpricelistmatrix[s][s + 1]
        useRouteprice.append(value)

        if (s == (len(lyftpricelistmatrix) - 2)):
            val = lyftpricelistmatrix[s + 1][0]
            useRouteprice.append(val)


    return lyftOptimalPathList, lyftPriceList, useRouteprice

