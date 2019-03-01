"""
Something I wrote to make working with open weather a bit easier for myself and to reduce having to repeat myself on my website.
Thanks to otto for helping me through the process.
"""

import requests #Recommended by python documentation
import json

apiKeyGlobal = 'your key goes here'

#Error Code
#401 invalid key
#403 accessing commercial information
#404 Not found
#200 Acceptable

class APIKeyError(Exception): pass
class CommercialAccessError(Exception): pass
class NotFoundError(Exception): pass

class CurrentWeatherRequest:
    def __init__(self, apiKey, simpleInfo=True):
        self.apiKey = apiKey
        self.simpleInfo = simpleInfo

    def _responseCodeHandler(self, responseObject): #looks better than printing a string
        code = str(responseObject['cod'])
        exceptionDictionary = {'401': APIKeyError,
                               '403': CommercialAccessError,
                               '404': NotFoundError}
        if code == '200':
            pass
        else:
            raise exceptionDictionary[code]

    def simpleInfoParser(self, responseObject): #takes the raw json from open weather and makes it a bit easier to handle
        responseOutput = []
        try:
            responseList = responseObject['list']
        except KeyError:
            responseObject['coord']['Lat'] = responseObject['coord'].pop('lat') #lat and lon have different key names if its a multi-city call or a single city call (seriously)
            responseObject['coord']['Lon'] = responseObject['coord'].pop('lon')
            responseList = [responseObject] #if we dont put it in a list it will iterate through its keys

        for response in responseList:
            responseRelevantInformation = {'name':response['name'],
                                           'id':response['id'],
                                           'description':response['weather'][0]['main'],
                                           'temp':response['main']['temp'],
                                           'max temp':response['main']['temp_max'],
                                           'min temp':response['main']['temp_min'],
                                           'pressure':response['main']['pressure'],
                                           'wind speed':response["wind"]["speed"],
                                           'wind direction':response["wind"]["deg"],
                                           'latitude':response["coord"]["Lat"],
                                           'longitude':re
                                           sponse["coord"]["Lon"]}
            responseOutput.append(responseRelevantInformation)
        if len(responseOutput) == 1:
            responseOutput = responseOutput[0]
        return responseOutput
        

    def byZipCode(self, zipCode, countryCode='us'): #Zipcode Call
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?zip={zipCode},{countryCode}&appid={self.apiKey}').json()
        self._responseCodeHandler(response)
        if self.simpleInfo == True:
            response = self.simpleInfoParser(response)
        return response
    
    def byCityName(self, cityName, countryCode='us'): #City Call
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={cityName},{countryCode}&appid={self.apiKey}').json()
        self._responseCodeHandler(response)
        if self.simpleInfo == True:
            response = self.simpleInfoParser(response)
        return response
    
    def byLatLong(self, lat, long): #Geographical Call
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={self.apiKey}').json()
        self._responseCodeHandler(response)
        if self.simpleInfo == True:
            response = self.simpleInfoParser(response) #might throw this whole handler and if simple==true thing into a method so its not as messy and easier to maintain
        return response

    def byBox(self, longLeft, longRight, latBottom, latTop):
        response = requests.get(f'http://api.openweathermap.org/data/2.5/box/city?bbox={longLeft},{latBottom},{longRight},{latTop},10&appid={self.apiKey}').json() #the 10 after the paramaters is the zoom,
                                                                                                                                                                #unknown what it currently does
                                                                                                                                                                #testing has shown this to be sufficent
        self._responseCodeHandler(response)
        if self.simpleInfo == True:
            response = self.simpleInfoParser(response)
        return response
