import sqlite3
import requests
import traceback
import sys
import json
from django.db import connection
def getPropertyDetail( pk):
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
                                  ,l.saleOrRentalFlag
                            from ListedProperty l
                                ,MasterTownData t
                                ,MasterStreetData s
                                ,MasterFlatTypes f
                                ,houseit_user u                                
                                
                            where l.propertyTownID  = t.townID 
                              and l.propertyStreetID = s.streetid
                              and l.propertyFlatTypeID = f.flatTypeID
                              and l.propertyOwnerID = u.id
                              and l.propertyID= %s
            """
      #print(viewsql)
      cursor=connection.cursor()
      cursor.execute(viewsql,(pk,))
      property=cursor.fetchall()
      return property