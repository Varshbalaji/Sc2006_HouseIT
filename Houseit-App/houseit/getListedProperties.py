import sqlite3
import requests
import traceback
import sys
import json
from django.db import connection
def getListedProperties(uritownname,uristreetname,uriflattype,uribeds,uribaths,urigarage,urifilter):
   listings=[]
   sqlvar = []
   # print(urifilter,'**',uritownname,'**',uristreetname,'**',uriflattype,'**',uribeds,'**',uribaths,'**',urigarage)
   viewsql="""
                     select       l.propertyID
                                  ,l.propertyImage
                                  ,t.townName
                                  ,s.streetName
                                  ,f.flatType 
                                  ,l.propertyBlock
                                  ,l.propertyAge
                                  ,l.floorAreaInSqm
                                  ,l.numberOfBeds
                                  ,l.numberOfBaths
                                  ,l.numberOfGarages
                                  ,l.propertyDesc
                                  ,l.askingMonthlyRent 
                                  ,l.remainingLeaseYears 
                                  ,l.AskingPrice
                                  ,u.first_name
                                  ,u.last_name
                                  ,u.address
                                  ,u.email
                                  ,u.phone                                                                  
                            from ListedProperty l
                                ,MasterTownData t
                                ,MasterStreetData s
                                ,MasterFlatTypes f
                                ,houseit_user u                                
                            where l.propertyTownID  = t.townID 
                              and l.propertyStreetID = s.streetid
                              and l.propertyFlatTypeID = f.flatTypeID
                              and l.saleOrRentalFlag= %s
                              and l.propertyStatus = 'Available' 
                              and l.propertyOwnerID = u.id
                           """

   sqlvar.append(urifilter)
   if uritownname != 'Any':
      viewsql = viewsql + ' and t.townName = %s'
      sqlvar.append(uritownname)

   if uristreetname != 'Any':
      viewsql = viewsql + ' and s.streetName = %s'
      sqlvar.append(uristreetname)

   if uriflattype != 'Any':
      viewsql = viewsql + ' and f.flatType  = %s'
      sqlvar.append(uriflattype)

   if uribeds != 'Any':
      viewsql = viewsql + ' and l.numberOfBeds  = %s'
      sqlvar.append(uribeds)

   if uribaths != 'Any':
      viewsql = viewsql + ' and l.numberOfBaths  = %s'
      sqlvar.append(uribaths)

   if urigarage != 'Any':
      viewsql = viewsql + ' and l.numberOfGarages  = %s'
      sqlvar.append(urigarage)

   viewsql = viewsql + ' order by l.propertyID desc'

   # print(viewsql, sqlvar)
   cursor = connection.cursor()
   cursor.execute(viewsql, sqlvar)
   listings = cursor.fetchall()
   return listings
