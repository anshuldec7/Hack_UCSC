class CrimeReportService(ServiceBase):
    @rpc(Unicode, Unicode,Unicode, _returns=Unicode)
    def checkcrime(ctx, lat, lon, radius):
        json1 = requests.get(
            'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + city +'+'+ categories + '&rankby=prominence&language=en&key=AIzaSyDmjLulL2RJWCbb3ewYnwC9VfHNZRpRK-o')
        json1 = json1.json()
        json2 = json1["categories"]
        rowcategories=[]
        dictcategoriesdetails = {}
        for row in json2:
            name = row['name']
            address = row['formatted_address']
            lat = row['lat']
            lng = row['long']
            open_now = row['open_now']
            data = [name, address, lat, lng, open_now]
            rowcategories.append(data)

         for i in rowcategories:
             dictcategoriesdetails[rowcategories[i][0]] = rowcategories[i]
