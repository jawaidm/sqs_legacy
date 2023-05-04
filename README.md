# Boranga

# Install Boranga Project
```
 cd /var/www
 git clone https://github.com/dbca-wa/sqs.git
 cd sqs

 virtualenv venv
 . venv/bin/activate

 pip install -r requirements.txt 
```
     
## Create a DB
```
 jawaidm@jawaidm:/var/www/pipsim$ sudo -u postgres psql
 psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1))
 Type "help" for help.

 postgres=# CREATE ROLE test WITH PASSWORD 'my_passwd' SUPERUSER;
 CREATE ROLE

 postgres=# ALTER ROLE test LOGIN;
 ALTER ROLE

 postgres=# create database sqs_dev;
 CREATE DATABASE

 postgres=# quit

 # Check Connection to new DB
 /var/www/sqs$ psql -U test -W -h localhost -d sqs_dev -p 5432
 Password: 

 psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1))
 SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
 Type "help" for help.

 sqs_dev=# 
```

## Add in .env
```
 DATABASE_URL="postgis://test:my_passwd@localhost:5432/sqs_dev"
 
 ./apply_initial_migrations.sh
 
 # If a user exists in the Ledger DB Server, test to see if you can connect to it (Assumes Ledger server is running - see below)
 EmailUserRO.objects.get(email='firstname.lastname@dbca.wa.gov.au')
 
 # Build NPM
 cd /var/www/sqs/sqs/frontend/sqs
 npm install
 npm run build
 
 cd /var/www/sqs/sqs
 ./manage.py collectstatic --noinput
 ./manage.py runserver 0.0.0.0:8000
 
 # GO TO:
     http://localhost:8000/ledger/admin/
     1. Create 'Boranga Admin' Group
```

## .env file for Boranga Application
NOTE: 
    1. LEDGER_API_KEY can be retrived from the LEDGER Server Admin (under group API)
    2. In Boranga Admin, must create SYSTEM GROUP 'Boranga Admin'

```  
DEBUG=True
DATABASE_URL="postgis://test:my_passwd@localhost:5432/sqs_dev"
LEDGER_DATABASE_URL='postgis://test:my_passwd@localhost:5432/sqs_dev'
LEDGER_API_URL="http://localhost:8000"
LEDGER_API_KEY="ledger_api_key__from__ledger_api_admin"
SYSTEM_GROUPS=['Boranga Admin']
SITE_PREFIX='sqs-dev'
SITE_DOMAIN='dbca.wa.gov.au'
SECRET_KEY='SECRET_KEY_YO'
PRODUCTION_EMAIL=False
NOTIFICATION_EMAIL='firstname.lastname@dbca.wa.gov.au'
CRON_NOTIFICATION_EMAIL='[firstname.lastname]'
NON_PROD_EMAIL='firstname.lastname@dbca.wa.gov.au'
EMAIL_INSTANCE='DEV'
EMAIL_HOST='smtp.corporateict.domain'
DJANGO_HTTPS=True
DEFAULT_FROM_EMAIL='no-reply@dbca.wa.gov.au'
ALLOWED_HOSTS=['*']
DEV_APP_BUILD_URL="http://localhost:8080/app.js"
CONSOLE_EMAIL_BACKEND=True

```

# Install Ledger as an Independent Server
```
cd /var/www/ledger
git clone https://github.com/dbca-wa/ledger.git .

virtualenv venv (-p python3.8)
. venv/bin/activate
pip install -r requirements.txt

patch venv/lib/python3.8/site-packages/django/contrib/gis/geos/libgeos.py libgeos.py.patch

./manage_ledgergw.py shell_plus
## check user exists
u=EmailUser.objects.get(email='firstname.lastname@dbca.wa.gov.au')
u.is_staff=True
u.is_superuser=True
u.save()

## change password for above user
./manage_ledgergw.py changepassword firstname.lastname@dbca.wa.gov.au

## start server
./manage_ledgergw.py runserver 0.0.0.0:8000

# go to http://localhost:8000/admin
# Login with the above credentials (email: firstname.lastname@dbca.wa.gov.au, pw: my_password)
# From th Admin view 
#     1. create group 'Boranga Admin' (in Group section)
#     2. in API sections
         a. click Add API
         b. System Name: Boranga
            System id:   0111 (some aritrary number for now)
            Allowed ips: 127.0.0.1/32
            Active:      active
         c. Click save, and this should generate an Api key (shown in the screenshot below)
         d. this Api key is needed to be set in your .env file
```

### .env file for Ledger Server
```                                                                                                                                                               
DEBUG=True
ALLOWED_HOSTS=['*']
SECRET_KEY='my_secret_key'
DATABASE_URL='postgis://test:my_passwd@localhost:5432/db_name'
ORACLE_FINANCE_DB='postgis://test:my_passwd@localhost:5432/db_name'
EMAIL_HOST='my_smtp_server'
BPOINT_USERNAME='bpoint_username'
BPOINT_PASSWORD='bpoint_password'
BPOINT_BILLER_CODE='bpoint_biller_code'
BPOINT_MERCHANT_NUM='bpoint_merchant_number'
BPAY_BILLER_CODE='bpay_biller_code'
CMS_URL="https://itassets.dbca.wa.gov.au"
DEFAULT_FROM_EMAIL='no-reply@dbca.wa.gov.au'
NOTIFICATION_EMAIL='firstname.lastname@dbca.wa.gov.au'
CRON_NOTIFICATION_EMAIL='firstname.lastname@dbca.wa.gov.au'
NON_PROD_EMAIL='firstname.lastname@dbca.wa.gov.au'
EMAIL_INSTANCE='DEV'
PRODUCTION_EMAIL=False
BPAY_ALLOWED=False
LEDGER_GST=10
SITE_PREFIX=''
SITE_DOMAIN=''
SITE_URL='localhost:8000'
DISABLE_EMAIL=False
DEV_APP_BUILD_URL="http://localhost:8080/app.js"
CONSOLE_EMAIL_BACKEND=True
SUPPORT_EMAIL="support@dbca.wa.gov.au"
CSRF_MIDDLEWARE_TOKEN='my_csrf_middleware_token'
```

# Test  
ogrinfo qml/data/json/dpaw_regions.json

ogrinfo -so qml/data/json/dpaw_regions.json dpaw_regions

./manage.py ogrinspect --name-field region --blank true --null true --layer dpaw_regions --mapping --multi world/data/json/dpaw_regions.json DpawRegion

# Test from shell  

## Load cddp:dpaw_region data into DpawRegion model 
### (https://kmi.dbca.wa.gov.au/geoserver/cddp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=cddp:dpaw_regions&maxFeatures=50&outputFormat=application%2Fjson)  
from qml.utils import load_dpaw  
load_dpaw.run()  


poly = {'type': 'FeatureCollection',  
 'features': [{'type': 'Feature',  
   'properties': {},  
   'geometry': {'type': 'Polygon',   
    'coordinates': [[[122.40966796874999, -28.709860843942845],  
      [128.38623046875, -28.709860843942845],  
      [128.38623046875, -22.28909641872304],  
      [122.40966796874999, -22.28909641872304],  
      [122.40966796874999, -28.709860843942845]]]}}]}  

from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon  
import json  

geom_str = json.dumps(poly['features'][0]['geometry'])  
geom = GEOSGeometry(geom_str)  
multipoly = MultiPolygon([geom])  

intersection_geom = []  

for region in DpawRegion.objects.filter(geom__intersects=multipoly):  
    intersection_geom.append(multipoly.intersection(region.geom))  
    print(region)  

GOLDFIELDS  
PILBARA  




from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon  
import json  

with open('qml/data/json/south_wa.json') as f:  
    data = json.load(f)  

for ft in data['features']:  
    geom_str = json.dumps(ft['geometry'])  
    geom = GEOSGeometry(geom_str)  
    try:  
        if isinstance(geom, MultiPolygon):  
            continue  
        elif isinstance(geom, Polygon):  
            geom = MultiPolygon([geom])  
     
            intersection_geom = []   
            for region in DpawRegion.objects.filter(geom__intersects=geom):  
                intersection_geom.append(geom.intersection(region.geom))  
                print(region)  
    except TypeError as e:   
        print(e)  


