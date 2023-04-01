import sqlite3
import requests
import traceback
import sys
import json
from django.db import connection
def viewOwnerProperty(userid, pk):
      viewsql="""
                     select       l.propertyID
                                 ,t.townName
                                 ,s.streetName                          
                                 ,l.propertyBlock
                                 ,f.flatType 
                                 ,l.propertyAge
                                 ,l.saleOrRentalFlag
                                 ,l.askingMonthlyRent
                                 ,l.remainingLeaseYears 
                                 ,l.AskingPrice
                                 ,l.propertyStatus
                                 ,l.propertyImage
                                 ,l.floorAreaInSqm
                                 ,l.numberOfBeds
                                 ,l.numberOfBaths
                                 ,l.numberOfGarages
                                 ,l.propertyDesc
                            from ListedProperty l
                                ,MasterTownData t
                                ,MasterStreetData s
                                ,MasterFlatTypes f
                            where l.propertyTownID  = t.townID 
                              and l.propertyStreetID = s.streetid
                              and l.propertyFlatTypeID = f.flatTypeID
                              and l.propertyOwnerID= %s
                              and l.propertyID= %s
            """

      cursor=connection.cursor()
      cursor.execute(viewsql,(userid,pk,))
      property=cursor.fetchall()
      return property