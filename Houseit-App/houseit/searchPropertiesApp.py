import sqlite3
import requests
import traceback
import sys
import json
from django.db import connection

#
def searchProperties(urifilter,townname,streetname,flattype,year,flatmodel):
    properties = []
    print(urifilter, ';', townname, ';', streetname, ';', flattype, ';', year)

    cursor = connection.cursor()
    if (urifilter == 'Rent'):
        if (year != 'Any'):
            year=year+'%'
        sqlvar = []
        rentalsql = """
                  select r.rentalPropertyID
                              ,substr(r.YYYYMM,6,2)
                              ,substr(r.YYYYMM,1,4)
                              ,t.townName
                              ,s.streetName                          
                              ,r.block
                              ,f.flatType 
                              ,r.monthlyRent 
                         from MasterPropertyRentalData  r
                             ,MasterTownData t
                             ,MasterStreetData s
                             ,MasterFlatTypes f
                         where r.townID  = t.townID 
                           and r.streetID = s.streetid
                           and r.flatTypeID = f.flatTypeID
                        """
        if townname != 'Any':
            rentalsql = rentalsql + ' and t.townName = %s'
            sqlvar.append(townname)

        if streetname != 'Any':
            rentalsql = rentalsql + ' and s.streetName = %s'
            sqlvar.append(streetname)

        if flattype != 'Any':
            rentalsql = rentalsql + ' and f.flatType  = %s'
            sqlvar.append(flattype)

        if year != 'Any':
            rentalsql = rentalsql + ' and r.YYYYMM like %s'
            sqlvar.append(year)

        rentalsql = rentalsql + ' order by r.YYYYMM desc, t.townName, s.streetName'
        if year == 'Any' and townname == 'Any' and streetname == 'Any' and flattype == 'Any':
            rentalsql = rentalsql+ " LIMIT 2000"

        # print('>>>', rentalsql)
        # print('>>>',sqlvar)
        cursor.execute(rentalsql, sqlvar)
        properties = cursor.fetchall()
        #print('>>> sql done ')
    else:
        # print('>>> getting sale')
        if (year != 'Any'):
            year=year+'%'
        # print('Sale Filter -> ', townname, ';', streetname, ';', flattype, ';',flatmodel, ';', year)
        sqlvar = []
        salesql = """
                  select rs.resalePropertyID
                              ,substr(rs.YYYYMM,6,2)
                              ,substr(rs.YYYYMM,1,4)
                              ,t.townName
                              ,f.flatType 
                              ,rs.block
                              ,s.streetName 
                              ,rs.floorAreaInSqm
                              ,m.flatModel
                              ,rs.leaseCommenceDate 
                              ,rs.remainingLeaseYears
                              ,rs.resalePrice   
                         from MasterPropertyReSaleData  rs
                             ,MasterTownData t
                             ,MasterStreetData s
                             ,MasterFlatTypes f
                             ,MasterFlatModelData m
                         where rs.townID  = t.townID 
                           and rs.streetID = s.streetid
                           and rs.flatTypeID = f.flatTypeID
                           and rs.flatModelID=m.flatModelID
                        """
        if townname != 'Any':
            salesql = salesql + ' and t.townName = %s'
            sqlvar.append(townname)

        if streetname != 'Any':
            salesql = salesql + ' and s.streetName = %s'
            sqlvar.append(streetname)

        if flattype != 'Any':
            salesql = salesql + ' and f.flatType  = %s'
            sqlvar.append(flattype)

        if year != 'Any':
            salesql = salesql + ' and rs.YYYYMM like %s'
            sqlvar.append(year)

        salesql = salesql + ' order by rs.YYYYMM desc, t.townName, s.streetName, m.flatmodel'
        if year == 'Any' and townname == 'Any' and streetname == 'Any' and flattype == 'Any':
            salesql = salesql+ " LIMIT 2000"
        #print('>>>', salesql)
        #print('>>>',sqlvar)
        cursor.execute(salesql, sqlvar)
        properties = cursor.fetchall()
        #print('>>> sql done ')


    return properties



