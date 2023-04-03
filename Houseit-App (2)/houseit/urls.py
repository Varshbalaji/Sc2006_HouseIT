
from django.urls import path, include
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

# Shared URL's
 path('', views.login_form, name='home'),
 path('home', views.login_form, name='home'),
 path('login/', views.loginView, name='login'),
 path('logout/', views.logoutView, name='logout'),
 path('regform/', views.register_form, name='regform'),
 path('register/', views.registerView, name='register'),
 path('usrhome/', views.userHome,name='userhome'),
 path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
 path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
 path('forgotpassword/<username>', views.forgotpassword, name='forgotpassword'),
 path('resetpassword', views.resetpassword, name='resetpassword'),
 path('viewuser/<username>', views.viewuser, name='viewuser'),

 # Admin URL's
path('houseitadmin/', views.houseitadmin, name='houseitadmin'),
path('masterrefresh/', views.invokemasterrefresh, name='masterrefresh'),
path('research/', views.researchView, name='research'),

 #Owner URL's
 path('houseitowner/', views.houseitowner, name='houseitowner'),
 path('createrental', views.createRentalView, name='createrental'),
 path('createrental/', views.createRentalView, name='createrental'),
 path('createresale', views.createResaleView, name='createresale'),
 path('createresale/', views.createResaleView, name='createresale'),
 path('listownerproperties/', views.listownerproperties, name='listownerproperties'),
 path('getpropertydesc/<int:pk>', views.PropertyDetailsView,name='getpropertydesc'),

 # Buyer URL's
 path('houseitbuyer/', views.listedPropertySearch, name='houseitbuyer'),
 #path('searchresale/', views.searchresale, name='searchresale'),
# Tenant URL's

 path('houseittenant/', views.listedPropertySearch, name='houseittenant'),
 #path('searchrental/', views.searchrental, name='searchrental'),
# Buyer/Tenant URL

 path('listedPropertySearch/', views.listedPropertySearch, name='listedPropertySearch'),
 path('bookmarkedproperties/', views.bookmarkedproperties, name='bookmarkedproperties'),
 path('showpropertydetail/<int:pk>', views.showPropertyDetail,name='showpropertydetail'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)