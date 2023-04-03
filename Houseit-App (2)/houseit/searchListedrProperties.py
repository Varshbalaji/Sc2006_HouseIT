import sqlite3
import requests
import traceback
import sys
import json
from django.db import connection
def searchListedProperties(urirentsale,uritownname,uristreetname,uriflattype):
   listings=[]
   sqlvar = []
   # print(urirentsale,'**',uritownname,'**',uristreetname,'**',uriflattype)
   if urirentsale=='Rent':
      viewsql="""
                     select       l.propertyImage
                                 ,t.townName
                                 ,s.streetName
                                 ,f.flatType 
                                 ,l.propertyBlock
                                 ,l.propertyAge
                                 ,l.askingMonthlyRent 
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
                              and l.saleOrRentalFlag= 'Rent'
                              and l.propertyStatus = 'Available' 
                              and l.propertyOwnerID = u.id
                           """
      if uritownname != '-':
         viewsql = viewsql + ' and t.townName = %s'
         sqlvar.append(uritownname)

      if uristreetname != '-':
         viewsql = viewsql + ' and s.streetName = %s'
         sqlvar.append(uristreetname)

      if uriflattype != '-':
         viewsql = viewsql + ' and f.flatType  = %s'
         sqlvar.append(uriflattype)


   if urirentsale == 'Sale':
      viewsql = """
                      select       l.propertyImage
                                  ,t.townName
                                  ,s.streetName
                                  ,f.flatType 
                                  ,l.propertyBlock
                                  ,l.floorAreaInSqm
                                  ,l.propertyAge
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
                               and l.saleOrRentalFlag= 'Sale'
                               and l.propertyStatus = 'Available' 
                               and l.propertyOwnerID = u.id
                            """
      if uritownname != '-':
         viewsql = viewsql + ' and t.townName = %s'
         sqlvar.append(uritownname)

      if uristreetname != '-':
         viewsql = viewsql + ' and s.streetName = %s'
         sqlvar.append(uristreetname)

      if uriflattype != '-':
         viewsql = viewsql + ' and f.flatType  = %s'
         sqlvar.append(uriflattype)

   # print(viewsql, sqlvar)
   cursor = connection.cursor()
   cursor.execute(viewsql, sqlvar)
   listings = cursor.fetchall()
   return listings
