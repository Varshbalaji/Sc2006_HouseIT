from datetime import datetime

from django.conf import settings as conf_settings
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core import serializers
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
#from bootstrap_modal_forms.mixins import PassRequestMixin

from .masterRefreshApp import masterRefresh
from .models import User, Mastertowndata, Masterflattypes, Masterstreetdata, Masterflatmodeldata, Masterpropertyrentaldata, Masterpropertyresaledata,Listedproperty
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import UserForm
from . import models, forms
import operator
import itertools
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .searchPropertiesApp import searchProperties
from .viewOwnerProperties import viewOwnerProperties
from .viewOwnerProperty import  viewOwnerProperty
from .updateProperty import  updateProperty
from .searchListedrProperties import searchListedProperties
from .getListedProperties import getListedProperties
from .getPropertyDetail import getPropertyDetail
# Shared Views
def login_form(request):
    return render(request, 'houseit/login.html')


def logoutView(request):
    logout(request)
    return redirect('home')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('houseitadmin')
            elif user.user_type=='Buyer':
                return redirect('houseitbuyer')
            elif user.user_type=='Owner':
                return redirect('houseitowner')
            else:
                return redirect('houseittenant')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('home')


def register_form(request):
    return render(request, 'houseit/register.html')


def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already Exists !!')
            return render(request, 'houseit/register.html')
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already Exists !!')
            return redirect('regform')
        phone = request.POST['phone']
        password = request.POST['password']
        password = make_password(password)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        user_type = request.POST['user_type']

        a = User(username=username, email=email, password=password,first_name=first_name,last_name=last_name,address=address,user_type=user_type,phone=phone)
        a.save()
        messages.success(request, 'Account was created successfully')
        return redirect('home')
    else:
        messages.error(request, 'Registration fail, try again later')
        return redirect('regform')


# Houseit Admin views
@login_required
def houseitadmin(request):
    #user = User.objects.all().count()
    # current_user = request.user
    # print('>>> User >>> ' ,current_user)
    #context = {'user':user}
    return render(request, 'houseitadmin/adminhome.html')

@login_required
def invokemasterrefresh(request):
    # invoke masterRefresh
    global returnCode, returnMsg, connection, refreshFlag
    returnCode = "";
    returnMsg = "";

    masterRefresh()
    #user = User.objects.all().count()
    #context = {'user':user}
    messages.success(request, 'Master Data has been refreshed successfully !!')
    return render(request, 'houseitadmin/adminhome.html')

#Owner Views
@login_required
def houseitowner(request):
    return render(request, 'houseitowner/ownerhome.html')

#Buyer Views
@login_required
def houseitbuyer(request):
    return render(request, 'houseitbuyer/buyerhome.html')

#Tenant Views
@login_required
def houseittenant(request):
    return render(request, 'houseittenant/tenanthome.html')

def createRentalView(request, user=None):
        streetlist = Masterstreetdata.objects.all().order_by('streetname')
        townlist = Mastertowndata.objects.all().order_by('townname')
        flattypelist = Masterflattypes.objects.all().order_by('flattype')
        uritownname = '-'
        uriblock='-'
        uristreetname = '-'
        uriflattype = '-'
        uriage= 0
        urirent=0
        uriimage = '-'
        listings = []
        # print(request.method)
        if request.method == 'POST':
            uritownname = request.POST['townname']
            uristreetname = request.POST['streetname']
            uriflattype = request.POST['flattype']
            uriblock = request.POST['block']
            uriage = request.POST['age']
            urirent = request.POST['rent']
            uriimage=request.FILES['image']
            uritownname = uritownname.replace('+', ' ')
            uristreetname = uristreetname.replace('+', ' ')
            userid = User.objects.filter(username=request.user).values('id')
            userid = userid[0]['id']
            flattypeid = Masterflattypes.objects.filter(flattype=uriflattype).values('flattypeid')
            flattypeid=flattypeid[0]['flattypeid']
            townid=Mastertowndata.objects.filter(townname=uritownname).values('townid')
            townid = townid[0]['townid']
            streetid = Masterstreetdata.objects.filter(streetname=uristreetname).values('streetid')
            streetid = streetid[0]['streetid']
            uribeds = request.POST['beds']
            uribaths = request.POST['baths']
            urigarage = request.POST['garage']
            uridesc = request.POST['desc']
            urisqm = request.POST['sqm']

            a = Listedproperty(propertyownerid=userid, propertyflattypeid=flattypeid, propertyblock=uriblock,
                               propertytownid=townid, propertystreetid=streetid, propertyage=uriage,
                               saleorrentalflag='Rent', floorareainsqm=urisqm, askingmonthlyrent=urirent, propertystatus='Available',
                               propertyimage=uriimage, numberofbeds=uribeds, numberofbaths=uribaths,
                               numberofgarages=urigarage, propertydesc=uridesc)

            a.save()
            messages.success(request, 'Rental Property has been listed successfully')
            return render(request, 'houseitowner/ownerhome.html')

        # else:
        #     messages.error(request, 'Property was not created successfully')
        #     return render(request, 'houseitowner/ownerhome.html')
       # listings= viewProperties(uritownname,uristreetname,uriflattype,uriblock,uriage,uriimage)

        return render(request, 'houseitowner/createrental.html',  { 'flattypelist': flattypelist,'townlist': townlist,'streetlist': streetlist })


def createResaleView(request):
    streetlist = Masterstreetdata.objects.all().order_by('streetname')
    townlist = Mastertowndata.objects.all().order_by('townname')
    flattypelist = Masterflattypes.objects.all().order_by('flattype')
    uritownname = '-'
    uriblock = '-'
    uristreetname = '-'
    uriflattype = '-'
    uriage = 0
    urisqm = 0
    urileaseyears = 0
    uriaskingprice = 0
    uriimage = '-'
    listings = []
    # print(request.method)
    if request.method == 'POST':
        uritownname = request.POST['townname']
        uristreetname = request.POST['streetname']
        uriflattype = request.POST['flattype']
        uriblock = request.POST['block']
        uriage = request.POST['age']
        urisqm = request.POST['sqm']
        urileaseyears = request.POST['leaseyears']
        uriaskingprice = request.POST['askingprice']
        uriimage = request.FILES['image']
        uritownname = uritownname.replace('+', ' ')
        uristreetname = uristreetname.replace('+', ' ')
        uribeds = request.POST['beds']
        uribaths = request.POST['baths']
        urigarage = request.POST['garage']
        uridesc = request.POST['desc']
        userid = User.objects.filter(username=request.user).values('id')
        userid = userid[0]['id']
        flattypeid = Masterflattypes.objects.filter(flattype=uriflattype).values('flattypeid')
        flattypeid = flattypeid[0]['flattypeid']
        townid = Mastertowndata.objects.filter(townname=uritownname).values('townid')
        townid = townid[0]['townid']
        streetid = Masterstreetdata.objects.filter(streetname=uristreetname).values('streetid')
        streetid = streetid[0]['streetid']

        a = Listedproperty(propertyownerid=userid, propertyflattypeid=flattypeid, propertyblock=uriblock,
                           propertytownid=townid, propertystreetid=streetid, propertyage=uriage,
                           saleorrentalflag='Sale', floorareainsqm=urisqm, remainingleaseyears=urileaseyears, askingprice=uriaskingprice, propertystatus='Available',
                           propertyimage=uriimage, numberofbeds=uribeds, numberofbaths=uribaths, numberofgarages=urigarage, propertydesc=uridesc)
        a.save()
        messages.success(request, 'Resale Property has been listed successfully')
        return render(request, 'houseitowner/ownerhome.html')

    return render(request, 'houseitowner/createresale.html',  { 'flattypelist': flattypelist,'townlist': townlist,'streetlist': streetlist })

def listownerproperties(request):
    # print('request => ', request)

    urifilter = 'All'

    properties = []
    #listURL = request.build_absolute_uri()

    # extract uriparms so we can pass it to search properties
    if 'filter' in request.GET:
        urifilter = request.GET['filter']


    userid = User.objects.filter(username=request.user).values('id')
    userid = userid[0]['id']
    properties = viewOwnerProperties(userid, urifilter)
    # print(properties)

    return render(request, 'houseitowner/viewListings.html',
                  { 'properties': properties,
                    'urifilter': urifilter
                    })
def PropertyDetailsView(request,pk) :

    streetlist = Masterstreetdata.objects.all().order_by('streetname')
    townlist = Mastertowndata.objects.all().order_by('townname')
    flattypelist = Masterflattypes.objects.all().order_by('flattype')
    propertystatuslist = ['Available','Closed','Delisted']
    saleorrentlist =  ['Sale','Rent']
    userid = User.objects.filter(username=request.user).values('id')
    userid = userid[0]['id']

    if request.method == 'POST':
        uripropertyid = request.POST['propertyid']
        townname = request.POST['townname']
        streetname = request.POST['streetname']
        block = request.POST['block']
        flattype = request.POST['flattype']
        propertyage = request.POST['propertyage']
        saleorrent =  request.POST['saleorrent']
        beds =  request.POST['beds']
        baths =  request.POST['baths']
        garage =  request.POST['garage']
        sqm =  request.POST['sqm']
        desc =  request.POST['desc']

        if saleorrent == 'Rent':
            monthlyrent = request.POST['monthlyrent']
            leaseyears = None
            askingprice = None
        else:
            askingprice = request.POST['askingprice']
            leaseyears = request.POST['leaseyears']
            monthlyrent = None
        propertystatus =  request.POST['status']


        flattypeid = Masterflattypes.objects.filter(flattype=flattype).values('flattypeid')
        flattypeid = flattypeid[0]['flattypeid']
        townid = Mastertowndata.objects.filter(townname=townname).values('townid')
        townid = townid[0]['townid']
        streetid = Masterstreetdata.objects.filter(streetname=streetname).values('streetid')
        streetid = streetid[0]['streetid']

        updateProperty(uripropertyid,townid,streetid,block,flattypeid,propertyage,saleorrent,monthlyrent,leaseyears,askingprice,propertystatus
                       ,beds,baths,garage,sqm,desc)

        messages.success(request, 'Property Details Updated Successfully')

    property = viewOwnerProperty(userid, pk)
    return render(request, 'houseitowner/viewProperty.html',
                  { 'property': property,
                    'flattypelist': flattypelist,
                    'townlist': townlist,
                    'streetlist': streetlist,
                    'propertystatuslist': propertystatuslist,
                    'saleorrentlist': saleorrentlist
                  })



def researchView(request):
    # print('request => ', request)
    streetlist = Masterstreetdata.objects.all().order_by('streetname')
    townlist   = Mastertowndata.objects.all().order_by('townname')
    flattypelist = Masterflattypes.objects.all().order_by('flattype')
    flatmodellist= Masterflatmodeldata.objects.all().order_by('flatmodel')
    year = datetime.today().year
    years = []
    for year in range(2017,year+1):
        year = str(year).strip()
        years.append(year)
    user = User.objects.filter(username=request.user).values('user_type')
    # print(user)
    usertype = user[0]['user_type']
    urifilter = 'Rent'
    uritownname = 'Any'
    uristreetname = 'Any'
    uriflattype = 'Any'
    uriflatmodel = 'Any'
    uriyear = 'Any'

    properties = []
    #If invoked with URI parameters then do database search
    if request.method == 'GET':
        #extract uriparms so we can pass it to search properties
        if 'townname' in request.GET:
            uritownname = request.GET['townname']
        if 'streetname' in request.GET:
            uristreetname = request.GET['streetname']
        if 'flattype' in request.GET:
            uriflattype = request.GET['flattype']
        if 'filter' in request.GET:
            urifilter = request.GET['filter']
        else:
            if usertype == 'Tenant':
                urifilter = 'Rent'
            else:
                urifilter = 'Sale'
        if 'year' in request.GET:
            uriyear = request.GET['year']
        # replace + in uritownname & uristreetname with space viz. http://127.0.0.1:8000/research/?rentsale=rental&townname=ANG+MO+KIO&streetname=-&flattype=-&year=-
        uritownname = uritownname.replace('+', ' ')
        uristreetname = uristreetname.replace('+', ' ')

        properties = searchProperties(urifilter,uritownname,uristreetname,uriflattype,uriyear,uriflatmodel)
        #print(properties)

    return render(request, 'research/search.html',
                  {'streetlist': streetlist, 'townlist': townlist, 'flattypelist': flattypelist, 'years': years, 'flatmodellist': flatmodellist ,'properties': properties,
                   'urifilter':urifilter, 'uritownname':uritownname,'uristreetname': uristreetname, 'uriflattype': uriflattype, 'uriyear': uriyear })

def userHome(request):
        user = request.user
        #print('>>> userHome >>>', user)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('houseitadmin')
            elif user.user_type=='Buyer':
                return redirect('houseitbuyer')
            elif user.user_type=='Owner':
                return redirect('houseitowner')
            else:
                return redirect('houseittenant')
        else:
            return redirect('home')

@login_required
def searchresale(request):
    streetlist = Masterstreetdata.objects.all().order_by('streetname')
    townlist = Mastertowndata.objects.all().order_by('townname')
    flattypelist = Masterflattypes.objects.all().order_by('flattype')
    uritownname = ''
    uristreetname = '-'
    uriflattype = '-'
    urirentsale = 'Sale'

    properties = []
    # If invoked with URI parameters then do database search
    if request.method == 'GET' and 'townname' in request.GET:
        uritownname = request.GET['townname']
        uristreetname = request.GET['streetname']
        uriflattype = request.GET['flattype']
        # replace + in uritownname & uristreetname with space viz. http://127.0.0.1:8000/research/?rentsale=rental&townname=ANG+MO+KIO&streetname=-&flattype=-&year=-
        uritownname = uritownname.replace('+', ' ')
        uristreetname = uristreetname.replace('+', ' ')
        properties = searchListedProperties(urirentsale,uritownname,uristreetname,uriflattype)

    return render(request, 'houseitbuyer/searchresale.html',
                  {'streetlist': streetlist, 'townlist': townlist, 'flattypelist': flattypelist, 'properties': properties,
                   'uritownname':uritownname,'uristreetname': uristreetname, 'uriflattype': uriflattype})
@login_required
def listedPropertySearch(request):
    streetlist = Masterstreetdata.objects.all().order_by('streetname')
    townlist = Mastertowndata.objects.all().order_by('townname')
    flattypelist = Masterflattypes.objects.all().order_by('flattype')
    user = User.objects.filter(username=request.user).values('user_type')
    # print(user)
    usertype = user[0]['user_type']

    uritownname = 'Any'
    uristreetname = 'Any'
    uriflattype = 'Any'
    uribeds = 'Any'
    uribaths = 'Any'
    urigarage = 'Any'

    properties = []
    # If invoked with URI parameters then do database search
    if request.method == 'GET':
        if 'townname' in request.GET:
            uritownname = request.GET['townname']
        if 'streetname' in request.GET:
            uristreetname = request.GET['streetname']
        if 'flattype' in request.GET:
            uriflattype = request.GET['flattype']
        if 'beds' in request.GET:
            uribeds = request.GET['beds']
        if 'baths' in request.GET:
            uribaths = request.GET['baths']
        if 'garage' in request.GET:
            urigarage = request.GET['garage']
        if 'filter' in request.GET:
            urifilter = request.GET['filter']
        else:
            if usertype == 'Tenant':
                urifilter = 'Rent'
            else:
                urifilter = 'Sale'

        # replace + in uritownname & uristreetname with space viz. http://127.0.0.1:8000/research/?rentsale=rental&townname=ANG+MO+KIO&streetname=-&flattype=-&year=-
        uritownname = uritownname.replace('+', ' ')
        uristreetname = uristreetname.replace('+', ' ')
        properties = getListedProperties(uritownname,uristreetname,uriflattype,uribeds,uribaths,urigarage,urifilter)

    return render(request, 'houseitcommon/listedPropertySearch.html',
                  {'streetlist': streetlist, 'townlist': townlist, 'flattypelist': flattypelist, 'properties': properties,
                   'uritownname':uritownname,'uristreetname': uristreetname, 'uriflattype': uriflattype, 'uribeds': uribeds
                   , 'uribaths': uribaths, 'urigarage': urigarage, 'urifilter': urifilter})
@login_required
def searchrental(request):
    streetlist = Masterstreetdata.objects.all().order_by('streetname')
    townlist = Mastertowndata.objects.all().order_by('townname')
    flattypelist = Masterflattypes.objects.all().order_by('flattype')
    uritownname = ''
    uristreetname = '-'
    uriflattype = '-'
    urirentsale = 'Rent'

    properties = []
    # If invoked with URI parameters then do database search
    if request.method == 'GET' and 'townname' in request.GET:
        uritownname = request.GET['townname']
        uristreetname = request.GET['streetname']
        uriflattype = request.GET['flattype']
        # replace + in uritownname & uristreetname with space viz. http://127.0.0.1:8000/research/?rentsale=rental&townname=ANG+MO+KIO&streetname=-&flattype=-&year=-
        uritownname = uritownname.replace('+', ' ')
        uristreetname = uristreetname.replace('+', ' ')
        properties = searchListedProperties(urirentsale,uritownname,uristreetname,uriflattype)

    return render(request, 'houseittenant/searchtenant.html',
                  {'streetlist': streetlist, 'townlist': townlist, 'flattypelist': flattypelist, 'properties': properties,
                   'uritownname':uritownname,'uristreetname': uristreetname, 'uriflattype': uriflattype})
@login_required
def showPropertyDetail(request,pk) :
    propertydetail = getPropertyDetail(pk)
    #print(propertydetail)
    return render(request, 'houseitcommon/showProperty.html',
                  { 'propertydetail': propertydetail
                  })

def forgotpassword(request,username="") :
    messages.warning(request, 'On Clicking, an one-time password reset  token is sent to your email id and mobile. Use that token to reset your password ')

    return render(request, 'houseit/forgotpassword.html',
                  { 'username': username
                  })

def resetpassword(request) :

    username=""
    otp=""
    if request.method == 'POST':
        username = request.POST['username']

    if 'otp' in request.POST:
        otp = request.POST['otp']
        newpassword = request.POST['password']
        if otp != '123456':
            messages.error(request,'You have entered an invalid One-time password')
            return render(request, 'houseit/resetpassword.html',
                          {'username': username
                           })
        else:
            user = User.objects.get(username=username)
            #print(user,user.password)
            newpassword=make_password(newpassword)
            user.password=newpassword
            user.save()
            #print(user)
            messages.success(request, 'Password has been reset for user ' + username)
            return render(request, 'houseit/login.html')

    print(">>> username = ", username)
    if User.objects.filter(username=username).exists():
        user = User.objects.filter(username=username).values()
        email =  user[0]['email']
        phone =  user[0]['phone']
        messages.success(request,'A One-time password reset token has been sent to  ' + email + ' and mobile ' + phone)
        # print(email,'**',phone)
    else:
        messages.error(request,'User Does not Exist!!')
        return render(request, 'houseit/forgotpassword.html',
                      {'username': username
                       })

    return render(request, 'houseit/resetpassword.html',
                    {'username': username
                     })

def viewuser(request,username="") :
    user = User.objects.filter(username=username).values()
    firstname =user[0]['first_name']
    lastname = user[0]['last_name']
    email = user[0]['email']
    usertype = user[0]['user_type']
    address =  user[0]['address']
    phone =  user[0]['phone']
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        usertype = request.POST['usertype']
        address = request.POST['address']
        phone = request.POST['phone']
        user = User.objects.get(username=username)
        user.first_name=firstname
        user.last_name=lastname
        user.email=email
        user.user_type=usertype
        user.address=address
        user.phone=phone
        user.save()
        messages.success(request, 'User Profile Updated!!')
        #print(user)
    return render(request, 'houseit/userprofile.html',
                    {'username': username,
                     'firstname': firstname,
                     'lastname':lastname,
                     'email':email,
                     'usertype':usertype,
                     'address':address,
                     'phone':phone
    })
