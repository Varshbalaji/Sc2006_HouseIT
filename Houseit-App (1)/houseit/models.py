from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=32, unique=True,default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(('email address'), unique=True)
    phone = models.TextField(max_length=15,blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=255, blank=True)
    user_type = models.CharField(max_length=10)

    class Meta:
        swappable = 'AUTH_USER_MODEL'



class Masterflatmodeldata(models.Model):
    flatmodelid = models.AutoField(db_column='flatModelID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    flatmodel = models.TextField(db_column='flatModel', blank=True, null=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MasterFlatModelData'


class Masterflattypes(models.Model):
    flattypeid = models.AutoField(db_column='flatTypeID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    flattype = models.TextField(db_column='flatType', blank=True, null=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MasterFlatTypes'



class Masterstreetdata(models.Model):
    streetid = models.AutoField(db_column='streetID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    streetname = models.TextField(db_column='streetName', blank=True, null=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MasterStreetData'


class Mastertowndata(models.Model):
    townid = models.AutoField(db_column='townID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    townname = models.TextField(db_column='townName', blank=True, null=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MasterTownData'


class Masterpropertyresaledata(models.Model):
    resalepropertyid = models.AutoField(db_column='resalePropertyID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    yyyymm = models.TextField(db_column='YYYYMM', blank=True, null=False)  # Field name made lowercase.
    townid = models.IntegerField(db_column='townID', blank=True, null=False)  # Field name made lowercase.
    flattypeid = models.IntegerField(db_column='flatTypeID', blank=True, null=False)  # Field name made lowercase.
    block = models.TextField(blank=True, null=False)
    streetid = models.IntegerField(db_column='streetID', blank=True, null=False)  # Field name made lowercase.
    floorareainsqm = models.TextField(db_column='floorAreaInSqm', blank=True, null=False)  # Field name made lowercase.
    flatmodelid = models.IntegerField(db_column='flatModelID', blank=True, null=False)  # Field name made lowercase.
    leasecommencedate = models.TextField(db_column='leaseCommenceDate', blank=True, null=False)  # Field name made lowercase.
    remainingleaseyears = models.TextField(db_column='remainingLeaseYears', blank=True, null=False)  # Field name made lowercase.
    resaleprice = models.DecimalField(db_column='resalePrice', max_digits=10, decimal_places=5, blank=True, null=False)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'MasterPropertyResaleData'


class Masterpropertyrentaldata(models.Model):
    rentalpropertyid = models.AutoField(db_column='rentalPropertyID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    yyyymm = models.TextField(db_column='YYYYMM', blank=True, null=False)  # Field name made lowercase.
    townid = models.ForeignKey(Mastertowndata,on_delete=models.CASCADE)
    block = models.TextField(blank=True, null=False)
    streetid = models.IntegerField(db_column='streetID', blank=True, null=False)  # Field name made lowercase.
    flattypeid = models.IntegerField(db_column='flatTypeID', blank=True, null=False)  # Field name made lowercase.
    monthlyrent = models.IntegerField(db_column='monthlyRent', blank=True, null=False)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MasterPropertyRentalData'


class Listedproperty(models.Model):
    propertyid = models.AutoField(db_column='propertyID', primary_key=True, null=False)  # Field name made lowercase.
    propertyownerid = models.IntegerField(db_column='propertyOwnerID', blank=True, null=True)  # Field name made lowercase.
    # propertyflattypeid = models.ForeignKey('Masterflattypes', models.DO_NOTHING, db_column='propertyFlatTypeID', blank=True, null=True)  # Field name made lowercase.
    propertyflattypeid = models.IntegerField(db_column='propertyFlatTypeID', blank=True, null=True)  # Field name made lowercase.
    propertyblock = models.TextField(db_column='propertyBlock', blank=True, null=True)  # Field name made lowercase.
    propertytownid = models.IntegerField(db_column='propertyTownID', blank=True, null=True)  # Field name made lowercase.
    propertyflatmodelid = models.IntegerField(db_column='propertyFlatModelID', blank=True, null=True)  # Field name made lowercase.
    propertystreetid = models.IntegerField(db_column='propertyStreetID', blank=True, null=True)  # Field name made lowercase.
    propertyage = models.IntegerField(db_column='propertyAge', blank=True, null=True)  # Field name made lowercase.
    floorareainsqm = models.IntegerField(db_column='floorAreaInSqm', blank=True, null=True)  # Field name made lowercase.
    saleorrentalflag = models.TextField(db_column='saleOrRentalFlag', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    askingmonthlyrent = models.IntegerField(db_column='askingMonthlyRent', blank=True, null=True)  # Field name made lowercase.
    leasecommencedate = models.DateField(db_column='leaseCommenceDate', blank=True, null=True)  # Field name made lowercase.
    remainingleaseyears = models.IntegerField(db_column='remainingLeaseYears', blank=True, null=True)  # Field name made lowercase.
    askingprice = models.IntegerField(db_column='AskingPrice', blank=True, null=True)  # Field name made lowercase.
    propertystatus = models.TextField(db_column='propertyStatus', blank=True, null=True)  # Field name made lowercase.
    propertyimage = models.ImageField(db_column='propertyImage',upload_to='houseitapp/', null=True, blank=True)
    numberofbeds = models.IntegerField(db_column='numberOfBeds', blank=True, null=True)  # Field name made lowercase.
    numberofbaths = models.IntegerField(db_column='numberOfBaths', blank=True, null=True)  # Field name made lowercase.
    numberofgarages = models.IntegerField(db_column='numberOfGarages', blank=True, null=True)  # Field name made lowercase.
    propertydesc = models.TextField(db_column='propertyDesc', blank=True,null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'ListedProperty'
