##############################################################
#
# File :- main.py
#
# Description :- This file interacts with the UI
#
# Author :- Team Fantastic4
#
###############################################################

from __future__ import absolute_import

import operator
from operator import itemgetter
import requests

import BusinessLogic
import re

from model import db
from model import createdb
from model import TripResult

createdb()
# creating table if not already created
db.create_all()

from flask import Flask, render_template, request, Response, redirect, session

import Lyft
import uber


pattern = re.compile('[^A-Za-z0-9 -]')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome():
    return render_template('index.html')


@app.route('/getAPIData', methods=['POST'])
def getAPIData():
    city = request.form['city']
    category = request.form['category']
    print city
    print category

    json1 = requests.get(
        'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + city + '+' + category + '&rankby=prominence&language=en&key=AIzaSyBJKFIXw9apHqYtt6bbQlhYX-a-AlwBb9E')
    # json1=json1.json()
    json1 = json1.json()
    name = []
    rating = []
    open_now = []
    formatted_address = []
    lat = []
    lng = []
    count = 0
    result = {}
    rating = {}
    finalResult = []
    ratingDect = {}
    temp=""
    pressure=""
    humidity=""
    description=""
    for key in json1['results']:
        list = []
        if (key['name']):
            list.append(key['name'])
        else:
            list.append("")
        if 'rating' not in key:
            list.append("")
            rating[key['id']] = 0
        else:
            list.append(key['rating'])
            rating[key['id']] = key['rating']
        if 'opening_hours' not in key or key['opening_hours']['open_now'] is "" :
            list.append("")
        else:
            list.append(key['opening_hours']['open_now'])
        list.append(key['formatted_address'])
        lat=key['geometry']['location']['lat']
        list.append(lat)
        lon=key['geometry']['location']['lng']
        list.append(lon)

        if description is "":
            print 'http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid=0092ca563ea76f5fc100d16acaeea3db'
            json2 = requests.get(
               'http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid=0092ca563ea76f5fc100d16acaeea3db')
            json2 = json2.json()
            temp = json2['main']['temp']
            pressure = json2['main']['pressure']
            humidity = json2['main']['humidity']
            description = json2['weather'][0]['description']
        list.append(description)
        list.append(temp)
        list.append(humidity)


        result[key['id']] = list
    sorted_rating = sorted(rating.items(), key=operator.itemgetter(1), reverse=True)

    if(len(sorted_rating)<5):
        for k in sorted_rating[0:len(sorted_rating)]:
            print result[k[0]]
            finalResult.append(result[k[0]])
    else:
        for k in sorted_rating[0:5]:
            print result[k[0]]
            finalResult.append(result[k[0]])
    return render_template('places.html', result=finalResult)


@app.route('/price', methods=['GET'])
def priceGet():
    return render_template('index.html')


@app.route('/analysis', methods=['GET'])
def analyse():
    from sqlalchemy import func
    uberPriceList = []
    lyftPricelist = []
    lyftcount = ""
    ubercount = ""
    try:
        analysis_query = db.session.query(TripResult.bestprovider, func.count(TripResult.id).label('count'),
                                          func.sum(TripResult.uberprice).label('totaluber'),
                                          func.sum(TripResult.lyftprice).label('totallyft')).group_by(
            TripResult.bestprovider).all()
        for row in analysis_query:

            if row.bestprovider == "LYFT":
                lyftcount = row.count
            if row.bestprovider == "UBER":
                ubercount = row.count

        analysis_query_last_rows = db.session.query(TripResult.uberprice, TripResult.lyftprice).order_by(
            TripResult.id.desc()).limit(10).all()
        for row in analysis_query_last_rows:
            uberPriceList.append(round(float(str(row.uberprice)), 2))
            lyftPricelist.append(round(float(str(row.lyftprice)), 2))
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print e
        return render_template('server_error.html', result=e)

    analysis_result = {'ubercount': ubercount, 'lyftcount': lyftcount, 'uberPriceList': uberPriceList,
                       'lyftPricelist': lyftPricelist}
    return render_template('analysis.html', result=analysis_result)


@app.route('/price', methods=['POST'])
def price():

    locationList = []
    DestList =[]
    if (request.form.get('latlng1')):
        source = request.form.get('latlng1')
        locationList.append(source)
    if (request.form.get('latlng2')):
        DestList.append(request.form.get('latlng2'))
    if (request.form.get('latlng3')):
        DestList.append(request.form.get('latlng3'))
    if (request.form.get('latlng4')):
        DestList.append(request.form.get('latlng4'))
    if (request.form.get('latlng5')):
        DestList.append(request.form.get('latlng5'))
    print "place1"+request.form['placename1']


    source_dest_list = []
    places1 = ""
    places2 = ""
    places3 = ""
    places4 = ""
    places5 = ""

    if (request.form['placename1'] and request.form.get('latlng1')):
        source_dest_list.append(str("1:"+request.form['placename1']))
        places1 = "1:"+request.form['placename1']
    if (request.form['placename2'] and request.form.get('latlng2')):
        source_dest_list.append(str("2:"+request.form['placename2']))
        places2 = "2:" + request.form['placename2']
    if (request.form['placename3'] and request.form.get('latlng3')) :
        source_dest_list.append(str("3:"+request.form['placename3']))
        places3 = "3:" + request.form['placename3']
    if (request.form['placename4'] and request.form.get('latlng4')):
        source_dest_list.append(str("4:"+request.form['placename4']))
        places4 = "4:" + request.form['placename4']
    if (request.form['placename5'] and request.form.get('latlng5')):
        source_dest_list.append(str("5:"+request.form['placename5']))
        places5 = "5:" + request.form['placename5']

    locationList.extend(DestList)
    BusinessLogic.setParameters(len(locationList))
    try:
        lyftOptimalPathList, lyftPriceList, useRoutepriceLyft = Lyft.lyftPrice(locationList)
        uberOptimalPathList, uberPriceList, cordinateList, priceList, serviceNameList, userRouteUberPrice = uber.uberPrice(
            locationList)
    except Exception as e:

        print e
        if str(e) == "1":
            return render_template('404.html', result=e)
        elif str(e) == "need more than 2 values to unpack":
            return render_template("noservice.html", result=e)
        else:
            return render_template('server_error.html')
    print '\n'
    print uberPriceList
    print lyftPriceList
    print priceList
    print source_dest_list

    optimalRoute = {'BestRouteUsingLyft': lyftOptimalPathList, 'PriceForLyft': lyftPriceList,
                    'PriceForUber': uberPriceList, 'BestRouteUsingUber': uberOptimalPathList,
                    'BestRouteUsingBoth': cordinateList, 'BestPrice': priceList, 'InvolvedProviders': serviceNameList,
                    'userInput': source_dest_list, 'useRoutepriceLyft': useRoutepriceLyft, 'place1': places1, 'place2': places2, 'place3': places3, 'place4': places4, 'place5': places5,
                    'userRouteUberPrice': userRouteUberPrice}

    totaluberprice = sum(uberPriceList)
    totallyftprice = sum(lyftPriceList)
    bestprovider = "LYFT"
    if (totallyftprice > totaluberprice):
        bestprovider = "UBER"
    totalpriceList = sum(priceList)
    #locationDesc = source_dest_list.split(';')
    sourcelocation = source_dest_list[0]
    destinations = source_dest_list[1:]
    x = ', '.join(destinations)

    print totallyftprice
    print type(totallyftprice)
    try:
        db_obj = TripResult(sourcelocation=sourcelocation, destinations=x, uberprice=totaluberprice,
                            lyftprice=totallyftprice, optimalprice=totalpriceList,
                            bestprovider=bestprovider)
        db.session.add(db_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print e
        #return render_template('server_error.html', result=e)
    return render_template('display.html', result=optimalRoute)
    #return render_template('server_error.html')



if __name__ == '__main__':
    print "Inside Run"
    app.run('127.0.0.1', port=8080)
