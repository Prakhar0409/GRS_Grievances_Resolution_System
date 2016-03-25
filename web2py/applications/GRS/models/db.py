# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.get('db.uri'), 
             pool_size = myconf.get('db.pool_size'),
             migrate_enabled = myconf.get('db.migrate'),
             check_reserved = ['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


from datetime import datetime,timedelta


db.define_table(
    'hostels',
    Field('hostel_admin_group_id', 'integer'),
    Field('hostel_residents_group_id', 'integer'),
    Field('hostel_name', length=32, unique=True),
 )


db.define_table(
    'users',
    Field('username', length=32, unique=True),
    Field('password', 'password', length=32, readable=False, label='Password'),
    Field('first_name', 'string', length=32, default=''),
    Field('last_name', 'string', length=32, default=''),
    Field('email_id', 'string', length=32),
    Field('degree_name', 'string', length=32),
    Field('hostel_id', db.hostels),
    Field('picture_id', 'integer'),
    Field('year_of_degree', 'integer'),
 )


custom_auth_table = db['users']

auth.settings.table_user = custom_auth_table
auth.settings.table_user_name = 'users'    #Very important to mention
auth.settings.login_userfield = 'username'        #the loginfield will be username
auth.define_tables(username=False)    #Creating the table


db.define_table(
    'group_members',
    Field('user_id', db.users),
    Field('group_id', 'integer'),
    Field('member_post', 'integer'),
    Field('is_validated', 'boolean'),
 )


db.define_table(
    'hostel_management',
    Field('hostel_id', db.hostels),
    Field('mess_secretary_user_id', db.users),
    Field('house_secretary_user_id', db.users),
    Field('maintenance_secretary_user_id', db.users),
    Field('sports_secretary_user_id', db.users),
    Field('cultural_secretary_user_id', db.users),
 )


db.define_table(
    'complaint_levels',
    Field('complaint_level_name', 'string', length=64),
)


db.define_table(
    'complaint_domain',
    Field('complaint_domain_name', 'string', length=64),
    Field('complaint_level_id', db.complaint_levels),
)


db.define_table(
    'complaints',
    Field('complaint_level_id', db.complaint_levels),
    Field('complaint_domain_id', 'integer'),
    Field('complaint_date', 'datetime', default=datetime.now),
    Field('complaint_title', 'string', length=256),
    Field('complaint_details', 'string', length=2048),
    Field('date_work_taken_on', 'datetime', default=datetime.now),
    Field('complaint_level_id', 'integer'),
    Field('status_id', 'integer'),
    Field('posted_by', db.users),
    Field('date_posted', 'datetime', default=datetime.now),
    Field('upvotes_count', 'integer'),
    Field('downvotes_count', 'integer'),
    Field('date_resolved', 'datetime', default=datetime.now),
    Field('photo_id', 'integer'),
    Field('redirected_by_user_id', db.users),
    Field('redirected_to_user_id', db.users),
)


db.define_table(
    'pictures',
    Field('picture_name', 'upload'),
    Field('picture_caption', 'string', length=512),
)


db.define_table(
    'votes',
    Field('user_id', db.users),
    Field('vote_type', 'integer'), #0 downvote ,1 upvote
    Field('complaint_id', db.complaints),
    Field('detailed_status', 'string', length=2048),
)


db.define_table(
    'comments',
    Field('user_id', db.users),
    Field('comment_made', 'string', length=2048),
    Field('date_commented', 'datetime', default=datetime.now),
    Field('complaint_id', db.complaints),
    Field('detailed_status', 'string', length=2048),
)


db.define_table(
    'complaint_status',
    Field('status_name', 'string', length=512),
    Field('detailed_status', 'string', length=2048),
    Field('complaint_id', db.complaints),
)


db.define_table(
    'status_comments',
    Field('user_id', db.users),
    Field('comment_made', 'string', length=2048),
    Field('date_commented', 'datetime', default=datetime.now),
    Field('status_id', db.complaint_status),
)


db.define_table(
    'bookmarks',
    Field('complaint_id', db.complaints),
    Field('user_id', db.users),
)


db.define_table(
    'complaints_concerning_user',
    Field('complaint_id', db.complaints),
    Field('id_type', 'integer'),	#0 user 1 group
    Field('group_id', 'integer'),
    Field('user_id', db.users),
    Field('is_hidden', 'boolean'),
)


db.define_table(
    'complaints_with_resolving_rights_to_user',
    Field('complaint_id', db.complaints),
    Field('id_type', 'integer'),
    Field('group_id', 'integer'),
    Field('user_id', db.users),
    Field('is_hidden', 'boolean'),
)


db.define_table(
    'complaints_made_to_user',
    Field('complaint_id', db.complaints),
    Field('id_type', 'integer'),
    Field('group_id', 'integer'),
    Field('user_id', db.users),
    Field('is_hidden', 'boolean'),
)

