import sqlite3
import requests
import traceback
import sys
import json
from django.db import connection
def viewOwnerProperties(userid, urifilter):
   listings=[]
   sqlvar = []
   status = ''
   print(urifilter)
   sqlvar.append(userid)

   if urifilter == 'All':
      status = status + '\"Available\"' + ',' + '\"Closed\"' + ',' + '\"Delisted\"'

   if urifilter == 'Available+Closed':
      status = status + '\"Available\"' + ',' + '\"Closed\"'

   if urifilter == 'Available':
      status = status + '\"Available\"'

   if urifilter == 'Closed':
      status = status + '\"Closed\"'

   if urifilter == 'Delisted':
      status = status + '\"Delisted\"'

   status = '('+status+')'


   viewsql="""
                     select       l.propertyID
                                 ,t.townName
                                 ,s.streetName                          
                                 ,l.propertyBlock
                                 ,f.flatType 
                                 ,l.propertyAge
                                 ,l.askingMonthlyRent
                                 ,l.AskingPrice 
                                 ,l.propertyStatus
                                 ,l.propertyImage
                                 ,l.saleOrRentalFlag
                                 ,l.floorAreaInSqm
                                 ,l.numberOfBeds   
                                 ,l.numberOfBaths  
                                 ,l.numberOfGarages
                            from ListedProperty l
                                ,MasterTownData t
                                ,MasterStreetData s
                                ,MasterFlatTypes f
                            where l.propertyTownID  = t.townID 
                              and l.propertyStreetID = s.streetid
                              and l.propertyFlatTypeID = f.flatTypeID
                              and l.propertyOwnerID= %s
                              and l.propertyStatus in  
                           """ + status + "order by l.propertyStatus asc , l.propertyID desc"

   cursor=connection.cursor()
   cursor.execute(viewsql,sqlvar)
   listings=cursor.fetchall()
   # print("listings = ", listings)
   return listings

