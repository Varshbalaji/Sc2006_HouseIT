import sqlite3
import requests
import traceback
import sys
import json
from django.db import connection
def updateProperty(propertyid,townid,streetid,block,flattypeid,propertyage,saleorrent,monthlyrent,leaseyears,askingprice,propertystatus,beds,baths,garage,sqm,desc):
      #print('<><>',saleorrent)
      if saleorrent == 'Rent':
            viewsql="""
                     update   ListedProperty
                        set   propertyTownID = %s,
                              propertyStreetID = %s,
                              propertyBlock = %s,
                              propertyFlatTypeID = %s,
                              propertyAge = %s,
                              askingMonthlyRent = %s,
                              propertyStatus = %s,
                              numberOfBeds = %s,
                              numberOfBaths =%s,
                              numberOfGarages=%s,
                              floorAreaInSqm=%s,
                              propertyDesc=%s
                            where propertyID = %s 

                    """
            #print(viewsql)
            cursor=connection.cursor()
            cursor.execute(viewsql,(townid,streetid,block,flattypeid,propertyage,monthlyrent,propertystatus,beds,baths,garage,sqm,desc,propertyid,))
      else:
            viewsql="""
                     update   ListedProperty
                        set   propertyTownID = %s,
                              propertyStreetID = %s,
                              propertyBlock = %s,
                              propertyFlatTypeID = %s,
                              propertyAge = %s,
                              remainingLeaseYears = %s,
                              AskingPrice = %s,
                              propertyStatus = %s,
                              numberOfBeds = %s,
                              numberOfBaths =%s,
                              numberOfGarages=%s,
                              floorAreaInSqm=%s,
                              propertyDesc=%s                              
                            where propertyID = %s 
                    """

            cursor=connection.cursor()
            cursor.execute(viewsql,(townid,streetid,block,flattypeid,propertyage,leaseyears,askingprice,propertystatus,beds,baths,garage,sqm,desc,propertyid))
      return