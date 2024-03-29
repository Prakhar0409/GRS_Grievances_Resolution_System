# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)



if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'], migrate=True)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb', migrate=True)
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] # if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


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

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.sender')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

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
    'user_group_names',
    Field('group_name', 'string', length=64),
 )


db.define_table(
    'hostels',
    Field('hostel_admin_group_id', 'integer'),
    Field('hostel_residents_group_id', 'integer'),
    Field('hostel_name', length=32, unique=True),
 )


db.define_table(
    'users',
    Field('username', length=32, unique=True),
    Field('password', 'password', length=512, readable=False, label='Password'),
    Field('registration_key', 'string', length=512),
    Field('registration_id', 'string', length=512),
    Field('first_name', 'string', length=32, default=''),
    Field('last_name', 'string', length=32, default=''),
    Field('email_id', 'string', length=32, unique=True),
    Field('degree_name', 'string', length=32),
    Field('hostel_id', db.hostels),
    Field('picture_id', 'integer'),
    Field('year_of_degree', 'integer'),
    Field('contact_no', 'integer'),
 )


db.define_table(
    'group_members',
    Field('user_id', db.users),
    Field('group_id', db.user_group_names),
    Field('member_post', 'integer'),
    Field('is_validated', 'boolean'),
 )


custom_auth_table = db['users']

auth.settings.table_user = custom_auth_table
auth.settings.table_user_name = 'users'    #Very important to mention
auth.settings.table_group_name = 'user_group_names'
#auth.settings.table_membership_name = 'group_members'
#auth.settings.table_permission_name = 'user_permission'
auth.settings.table_event_name = 'user_event'
auth.settings.login_userfield = 'username'        #the loginfield will be username
auth.define_tables(username=False)    #Creating the table

custom_auth_table.username.requires = IS_NOT_IN_DB(db,custom_auth_table.username), IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.email_id.requires = IS_EMAIL(error_message=auth.messages.invalid_email),IS_NOT_IN_DB(db,custom_auth_table.email_id)

db.define_table(
    'hostel_management',
    Field('hostel_id', db.hostels, unique=True),
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
    Field('complaint_domain_id', db.complaint_domain),
    Field('complaint_date', 'datetime', default=datetime.now),
    Field('complaint_title', 'string', length=256),
    Field('complaint_details', 'string', length=2048),
    Field('date_work_taken_on', 'datetime'),
    Field('status_id', 'integer'),
    Field('posted_by', db.users),
    Field('date_posted', 'datetime', default=datetime.now),
    Field('upvotes_count', 'integer'),
    Field('downvotes_count', 'integer'),
    Field('date_resolved', 'datetime'),
    Field('photo_id', 'integer'),
    Field('redirected_by_user_id', db.users),
    Field('redirected_to_type', 'integer'),	#0 for user,1 for group
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
)


db.define_table(
    'complaint_status',
    Field('status_name', 'string', length=512),
    Field('detailed_status', 'string', length=2048),
    Field('complaint_id', db.complaints),
    Field('date_commented', 'datetime', default=datetime.now),
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
    Field('is_hidden', 'boolean',default='False'),
)


db.define_table(
    'complaints_with_resolving_rights_to_user',
    Field('complaint_id', db.complaints),
    Field('id_type', 'integer'),
    Field('group_id', 'integer'),
    Field('user_id', db.users),
    Field('is_hidden', 'boolean',default='False'),
)


db.define_table(
    'complaints_made_to_user',
    Field('complaint_id', db.complaints),
    Field('id_type', 'integer'),
    Field('group_id', 'integer'),
    Field('user_id', db.users),
    Field('is_hidden', 'boolean',default='False'),
)


db.define_table(
    'notifications',
    Field('user_id', db.users),
    Field('notification_type', 'integer'),	#-1-stated in notification,0 comment, 1 status,2 status_comment
    Field('notification_item_id', 'integer'),	#id of status/comment
    Field('notification', 'string','512'),
)


db.define_table(
    'complaint_read',
    Field('complaint_id', db.complaints),
    Field('user_id', db.users),
)


db.define_table(
    'status_read',
    Field('status_id', db.complaints),
    Field('user_id', db.users),
)

db.define_table(
    'validation_requests',
    Field('from_user_id', db.users),
    Field('to_user_id', db.users),
    Field('group_id', db.user_group_names),
)

db.define_table(
    'group_heads',
    Field('group_id', db.user_group_names),
    Field('head_user_id', db.users),
)
