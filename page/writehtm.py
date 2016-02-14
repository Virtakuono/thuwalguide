#!/usr/bin/python

import overpy
import time
import os

class restaurant():

    def __init__(self,name='',lat=0.0,lon=0.0,descPara=[],tags=[],rating=(3,3,3),phones=[],idNum=0,numPics=0):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.descPara = descPara
        self.tags = tags
        self.rating = rating
        self.phones = phones
        self.idNum = idNum
        self.numPics = numPics
        self.identifier = self.name+':('+str(self.lat)+str(self.lon)+')'
        if self.idNum:
            self.identifier = 'restaurant%04d'%(self.idNum)
        for foo in range(len(self.identifier)):
            if not self.identifier[foo].isalnum():
                self.identifier = self.identifier[:foo]+'_'+self.identifier[foo+1:]

    def htmlstr(self):

        rv = '<a id="%s"></a>\n'%(self.identifier,)
        rv += '<p class="header2">%s</p>\n'%(self.name)
        if self.numPics:
            smallPhoto = './pics/%04d_%d_s.jpg'%(self.idNum,1)
            fullPhoto = './pics/%04d_%d.jpg'%(self.idNum,1)
            rv += '<p class="plaintext">\n<img class="kayakphoto" src="%s"/>\n</p>\n'%(smallPhoto,)
        for para in self.descPara:
            rv += '<p class="plaintext">%s</p>\n'%(para)
        rv += '<p class="plaintext">\n'
        rv += '<table class="rating">\n'
        rv += '<tr><td>Taste</td><td><img class="rating" height="40" width="200" src="./%ds.svg" title="%d/5" label="%d/5" /></td></tr>\n'%(self.rating[0],self.rating[0],self.rating[0])
        rv += '<tr><td>Cost</td><td><img class="rating" height="40" width="200" src="./%ds.svg" title="%d/5" label="%d/5" /></td></tr>\n'%(self.rating[1],self.rating[1],self.rating[1])
        rv += '<tr><td>Ease</td><td><img class="rating" height="40" width="200" src="./%ds.svg" title="%d/5" label="%d/5" /></td></tr>\n'%(self.rating[2],self.rating[2],self.rating[2])
        rv += '</table>\n'
        rv += '</p>\n'
        
        if self.numPics:
            rv += '<p class="plaintext">\n'
            for foo in range(1,self.numPics+1):
                thumbPhoto = './pics/%04d_%d_t.jpg'%(self.idNum,foo)
                fullPhoto = './pics/%04d_%d.jpg'%(self.idNum,foo)
                rv += '<a href="%s" target="_blank"><img class="thumb" src="%s" /></a>'%(fullPhoto,thumbPhoto)
            rv += '</p>\n'
        if self.tags:
            rv += '<p class="plaintext">\n'
            rv += 'Tags:\n'
            for tag in self.tags:
                rv += '%s,\n'%(tag,)
            rv = '%s\n'%(rv[:-2])
            rv += '</p>\n'
        if self.phones:
            rv += '<p class="plaintext">\n'
            rv += 'Phone:\n'
            for phone in self.phones:
                rv += '<a href="tel:%s">%s</a>,\n'%(phone,phone)
            rv = '%s\n'%(rv[:-2])
            rv += '</p>\n'
            
        #if self.numPics:
        #    for foo in range(1,self.numPics+1):
        #        smallPhoto = './pics/%04d_%d_s.jpg'%(self.idNum,foo)
        #        fullPhoto = './pics/%04d_%d.jpg'%(self.idNum,foo)
        #        rv += '<p class="plaintext"><a href="%s"><img class="kayakphoto" src="%s" /></a></p>\n'%(fullPhoto,smallPhoto)

        rv += '<p class="plaintext"><a href="%s">Location</a></p>\n'%(self.locationLink())
        #rv += '<hr />\n'
        return rv

    def locationLink(self):
        return 'https://www.openstreetmap.org/?mlat=%f&mlon=%f#map=19/%f/%f'%(self.lat,self.lon,self.lat,self.lon)

def printWebPage(restaurants=[],outputFile='index.htm',title='Culinarist\'s guide to Thuwal'):
    rv = '<!DOCTYPE html>\n<html>\n<head>'
    rv += '<title>%s</title>\n'%(title,)
    rv += '<meta charset="utf-8" />\n'
    rv += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    rv += '<link rel="stylesheet" href="./stylesheet.css" />\n'
    rv += '</head>\n'
    rv += '<body background="./bghuge_small.jpg">\n'
    rv += '<div class="text">\n'
    rv += '<p class="themainheader">%s</p>\n'%(title,)
    rv += '<p class="plaintext">Thuwal is one of the most underexploited and underrated tourist destinations of Hejaz. This magnificent small town offers dozens of options for the traveller keen on buying electronics, praying, having their hair cut and more. This short guide is a tribute to the pearl of the Hejazi and the restaurants therein.</p>\n'
    rv += '<p class="plaintext">All names are reported verbatim as they are written on the street with the exception of the places that have only arabic signs, in which case an arabic-sounding pseudonym that best describes the ambience of the restaurant in question has been assigned.</p>\n'
    rv += '<p class="header2">Restaurants</p>\n'
    rv += '<p class="plaintext">\n'
    counter = 1
    for restaurant in restaurants:
        rv += '<a href="#%s">%d. %s</a><br />'%(restaurant.identifier,counter,restaurant.name)
        counter += 1
    rv += ''
    rv += '<div class="map" id="map" style="width: 598px; height: 400px"></div>\n'
    for restaurant in restaurants:
        rv+= restaurant.htmlstr()

    rv += '<p class="plaintext">Page created on %s. Restaurant locations from <a href="https://www.openstreetmap.org/">OSM</a>. Other content by Juho H&auml;pp&ouml;l&auml; and Grace Gruendler. Available under <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a></p>'%(time.ctime())

    rv += '</div>\n'
    rv += '<script src="./leaflet.js"></script>'
    rv += '<script>\n'
    rv += 'var tehIcon = L.icon({\n'
    rv += 'iconUrl: \'./pin.png\',\n'
    rv += 'iconSize: [32,37],\n'
    rv += 'iconAnchor: [16,37],\n'
    rv += 'popupAnchor: [0,-20]\n'
    rv += '});\n'

    rv += 'var map = L.map(\'map\').setView([22.28425, 39.11296], 15);\n'

    for restaurant in restaurants:
        rv += 'L.marker([%f,%f],{icon: tehIcon}).bindPopup("<a href=\\"#%s\\">%s</a>").addTo(map);\n'%(restaurant.lat,restaurant.lon,restaurant.identifier,restaurant.name)

    rv += 'L.tileLayer(\'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoidmlydGFrdW9ubyIsImEiOiJMeXlPMHY4In0.r8EBq4jbNvFGpxrDldIVCg\', {\n'
    rv += 'maxZoom: 20,\n'
    rv += 'minZoom: 12,\n'
    rv += 'attribution: \'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \' +\n'
    rv += '\'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, \' +'
    rv += '\'Imagery &copy; <a href="http://mapbox.com">Mapbox</a>\',\n'
    rv += 'id: \'virtakuono.31a13bfd\'\n'
    rv += '}).addTo(map);\n'
    rv += '</script>\n'
    rv += '</body>\n'
    rv += '</html>\n'
    f=open(outputFile,'w')
    f.writelines([rv,])
    f.close()
    return rv


def overpassQuery(ID=1,e=37.0,n=24.0,s=20.0,w=40.0):
    valueString = '%04d'%(ID,)
    keyString = 'thuwalguide_id'
    rv = '<osm-script output="json" timeout="25">\n'
    rv += '<union into="_">\n'
    rv += '<query into="_" type="node">\n'
    rv += '<has-kv k="%s" modv="" v="%s"/>\n'%(keyString,valueString)
    rv += '<bbox-query e="%f" into="_" n="%f" s="%f" w="%f"/>\n'%(e,n,s,w)
    rv += '</query>\n'
    rv += '<query into="_" type="way">\n'
    rv += '<has-kv k="%s" modv="" v="%s"/>\n'%(keyString,valueString)
    rv += '<bbox-query e="%f" into="_" n="%f" s="%f" w="%f"/>\n'%(e,n,s,w)
    rv += '</query>\n'
    rv += '<query into="_" type="relation">\n'
    rv += '<has-kv k="%s" modv="" v="%s"/>\n'%(keyString,valueString)
    rv += '<bbox-query e="%f" into="_" n="%f" s="%f" w="%f"/>\n'%(e,n,s,w)
    rv += '</query>\n'
    rv += '</union>\n'
    rv += '<print e="" from="_" geometry="skeleton" limit="" mode="body" n="" order="id" s="" w=""/>\n'
    rv += '<recurse from="_" into="_" type="down"/>\n'
    rv += '<print e="" from="_" geometry="skeleton" limit="" mode="skeleton" n="" order="quadtile" s="" w=""/>\n'
    rv += '</osm-script>\n'
    return rv

def overpassQuery(ID=1,w=37.0,e=40.0,n=24.0,s=19.0):
    rv = '<osm-script output="json" timeout="25">\n'
    rv +=  '<union into="_">\n'
    rv +=   '<query into="_" type="node">\n'
    rv +=      '<has-kv k="thuwalguide_id" modv="" v="%04d"/>\n'%(ID,)
    rv +=       '<bbox-query e="%f" into="_" n="%f" s="%f" w="%f"/>\n'%(e,n,s,w)
    rv +=     '</query>\n'
    rv +=     '<query into="_" type="way">\n'
    rv +=       '<has-kv k="thuwalguide_id" modv="" v="%04d"/>\n'%(ID,)
    rv +=       '<bbox-query e="%f" into="_" n="%f" s="%f" w="%f"/>\n'%(e,n,s,w)
    rv +=     '</query>\n'
    rv +=   '</union>\n'
    rv +=  '<print e="" from="_" geometry="skeleton" limit="" mode="body" n="" order="id" s="" w=""/>\n'
    rv +=  '<recurse from="_" into="_" type="down"/>\n'
    rv +=  '<print e="" from="_" geometry="skeleton" limit="" mode="skeleton" n="" order="quadtile" s="" w=""/>\n'
    rv += '</osm-script>\n'
    return rv

def wayCenter(way):
    maxLat = float(way.nodes[0].lat)
    maxLon = float(way.nodes[0].lon)
    minLat = 1*maxLat
    minLon = 1*maxLon
    for node in way.nodes[1:]:
        la = float(node.lat)
        lo = float(node.lon)
        maxLat = max(maxLat,la)
        minLat = min(minLat,la)
        maxLon = max(maxLon,lo)
        minLon = min(minLon,lo)
    return (0.5*(maxLat+minLat),0.5*(maxLon+minLon))

queryID = lambda ID: overpy.Overpass().query(overpassQuery(ID))

def getRestaurants(fn='restaurants.tsv'):
    f = open(fn,'r')
    lines = f.readlines()[1:]
    f.close()
    rv = []
    lineCounter = 1
    for line in lines:
        print('Processing line %4d of input file %s ...'%(lineCounter,fn))
        lineCounter+=1
        if len(line)>4:
            if line[-1] =='\n':
                truncLine = line[:-1]
            else:
                truncLine = line
            if truncLine[-1] == '\r':
                truncLine = truncLine[:-1]
            tabLoc = truncLine.find('\t')
            tName = truncLine[:tabLoc]
            truncLine = truncLine[tabLoc+1:]
            tabLoc = truncLine.find('\t')
            tID = truncLine[:tabLoc]
            truncLine = truncLine[tabLoc+1:]
            tabLoc = truncLine.find('\t')
            tTaste = int(truncLine[:tabLoc])
            truncLine = truncLine[tabLoc+1:]
            tabLoc = truncLine.find('\t')
            tCost = int(truncLine[:tabLoc])
            truncLine = truncLine[tabLoc+1:]
            tabLoc = truncLine.find('\t')
            tEase = int(truncLine[:tabLoc])
            truncLine = truncLine[tabLoc+1:]
            tRevParas = []
            while '\t' in truncLine:
                tabLoc = truncLine.find('\t')
                if tabLoc:
                    tRevParas.append(truncLine[:tabLoc])
                truncLine = truncLine[tabLoc+1:]
            if truncLine:
                tRevParas.append(truncLine)
            picId =1
            thumbNailSize = 100
            pixelCount = 500*500
            while '%04d_%d.jpg'%(int(tID),picId) in os.listdir('./pics/'):
                command1 =  'convert ./pics/%04d_%d.jpg -thumbnail %dx%d^ -gravity center -extent %dx%d ./pics/%04d_%d_t.jpg'%(int(tID),picId,thumbNailSize,thumbNailSize,thumbNailSize,thumbNailSize,int(tID),picId)
                command2 = 'convert ./pics/%04d_%d.jpg -resize %d@ ./pics/%04d_%d_s.jpg'%(int(tID),picId,pixelCount,int(tID),picId)
                os.system(command1)
                os.system(command2)
                picId += 1
            ### query from osm database
            queryResult = queryID(int(tID))
            if queryResult.ways:
                tehWay = queryResult.ways[0]
                latLon = wayCenter(tehWay)
                keys = tehWay.tags.keys()
                phones = []
                if u'phone' in keys:
                    tempString = str(tehNode.tags[u'phone'])
                    if ';' in tempString:
                        while ';' in tempString:
                            loc = tempString.find(';')
                            phones.append('%s'%(tempString[:loc]))
                            tempString = '%s'%(tempString[loc+1])
                        phones.append('%s'%(tempString))
                    else:
                        phones.append('%s'%(tempString))
                tagsAdd = []
                if u'cuisine' in keys:
                    cuisineValue = str(tehNode.tags[u'cuisine']).lower()
                    if 'pakistani' in cuisineValue:
                        tagsAdd.append('Pakistani')
                    if 'seafood' in cuisineValue:
                        tagsAdd.append('Seafood')
                    if 'chicken' in cuisineValue:
                        tagsAdd.append('Chicken')
                    if 'turkish' in cuisineValue:
                        tagsAdd.append('Turkish')
                    if 'kebab' in cuisineValue:
                        tagsAdd.append('Shwarma')
                    if u'family_seating' in keys:
                        if str(tehNode.tags[u'family_seating']).lower() == 'yes':
                            tagsAdd.append('Family seating')
                    if u'takeaway' in keys:
                        if str(tehNode.tags[u'takeaway']).lower() == 'only':
                            tagsAdd.append('Takeaway')
                rv.append(restaurant(name=tName,lat=latLon[0],lon=latLon[1],descPara=tRevParas,tags=tagsAdd,rating=(tTaste,tCost,tEase),phones=phones,idNum=int(tID),numPics=picId-1))
            else:
                try:
                    tehNode = queryResult.nodes[0]
                    keys = tehNode.tags.keys()
                    phones = []
                    if u'phone' in keys:
                        tempString = str(tehNode.tags[u'phone'])
                        while ';' in tempString:
                            phones.append(tempString[:tempString.find(';')])
                            tempString=tempString[tempString.find(';')+1:]
                            while tempString[0].isspace():
                                tempString = tempString[1:]
                        phones.append(tempString)
                    tagsAdd = []
                    if u'cuisine' in keys:
                        cuisineValue = str(tehNode.tags[u'cuisine']).lower()
                        if 'pakistani' in cuisineValue:
                            tagsAdd.append('Pakistani')
                        if 'seafood' in cuisineValue:
                            tagsAdd.append('Seafood')
                        if 'chicken' in cuisineValue:
                            tagsAdd.append('Chicken')
                        if 'turkish' in cuisineValue:
                            tagsAdd.append('Turkish')
                        if 'kebab' in cuisineValue:
                            tagsAdd.append('Shwarma')
                    if u'family_seating' in keys:
                        if str(tehNode.tags[u'family_seating']).lower() == 'yes':
                            tagsAdd.append('Family seating')
                    if u'takeaway' in keys:
                        if str(tehNode.tags[u'takeaway']).lower() == 'only':
                            tagsAdd.append('Takeaway')
                    rv.append(restaurant(name=tName,lat=float(tehNode.lat),lon=float(tehNode.lon),descPara=tRevParas,tags=tagsAdd,rating=(tTaste,tCost,tEase),phones=phones,idNum=int(tID),numPics=picId-1))
                except IndexError:
                    pass
    return rv
    
restaurantList = getRestaurants()
printWebPage(restaurants=restaurantList)
