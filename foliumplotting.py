#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
import re
import googlemaps
import requests
import json
import folium


def getTwitterResults():

    listOfPossibleLocations = []

    #Authentification keys nessccesary to utilize the Twitter API:
    consumer_key = '*********'
    consumer_secret = '*********'
    access_token = '*************'
    access_token_secret = '**************'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    #Specifying which users timeline to scrap, and how many tweets:
    timeline = api.user_timeline(id = '*********', count = 100)

    for status in timeline:
        update = (status.text)

        #Regex to search the tweets for place names
        mostcomplex_match = re.findall(r'[A-ZÆØÅ]\w*\s+\d+\s+\w*', update)
        medium_complex_match = re.findall(r'[A-ZÆØÅ]\w*\s+\d+\s', update)
        least_complex_match = re.findall(r'\b[A-ZÆØÅ].*?\b', update)
        another_try = re.findall(r'[A-ZÆØÅ]\S+', update)

        if mostcomplex_match:
            dicti = {'Match': mostcomplex_match, 'Message': update}
            listOfPossibleLocations.append(dicti)

        elif medium_complex_match:
            dicti = {'Match': medium_complex_match, 'Message': update}
            listOfPossibleLocations.append(dicti)

        elif another_try:
            dicti = {'Match': another_try, 'Message': update}
            listOfPossibleLocations.append(dicti)

        elif least_complex_match:
            dicti = {'Match': least_complex_match, 'Message': update}
            listOfPossibleLocations.append(dicti)

        else:
            print('No match')

    return listOfPossibleLocations

def getPlaceCoordinates(listOfPossibleLocations):
    """Function gets the list of possible place names from getTwitterResults
        and tries to find coordinates using googlemaps api"""

    listofpoints = []

    for words in listOfPossibleLocations:

        dictionary = words
        words = (dictionary['Match'])
        message = (dictionary['Message'])

        for items in words:

            words = str(items)
            words = re.sub(r'[:]', '', words)

        try:

            googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'
            gmaps = googlemaps.Client(key='************')

            # Geocoding and address:
            geocode_result = gmaps.geocode(address = words ,region ='NO')
            parsed_json = json.dumps(geocode_result)
            parsed_json = json.loads(parsed_json)

            googleresults = parsed_json[0]['geometry']['location']
            results = {'googleresults': googleresults, 'Message': message}
            listofpoints.append(results)

        except (AttributeError, IndexError) as e:
            print(e)

    return listofpoints

def plotcoordinates(listofpoints):

    #Defines which part of the map is initially shown:
    map_osm = folium.Map(location=[80.1489544, 6.0143431], zoom_start=9)

    for items in listofpoints:
        message = items['Message']
        access = items['googleresults']
        lat = access['lat']
        lng = access['lng']
        map_osm.simple_marker([lat, lng], popup= message)

    map_osm.create_map(path='map.html')


locations = getTwitterResults()
coordinates = getPlaceCoordinates(locations)
points = plotcoordinates(coordinates)
