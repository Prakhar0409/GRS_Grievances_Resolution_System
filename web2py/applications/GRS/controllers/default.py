# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def clear_all():
	for table in db.tables():
		try:
			db(db[table].id>0).delete()
			print "Cleared",table
		except Exception, e:
			print "Couldn't clear",table

def complaint_levels_set():
	db.complaint_levels.insert(
		complaint_level_name="Individual",
	)

	db.complaint_levels.insert(
		complaint_level_name="Hostel",
	)

	db.complaint_levels.insert(
		complaint_level_name="Institute",
	)

	db.complaint_levels.insert(
		complaint_level_name="Miscellaneous",
	)

def institute_complaint_domain_set():
	db.complaint_domain.insert(
		complaint_domain_name="Infrastructure",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Administration",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Canteen and Food Outlets",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Security",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Sports",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Culture",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Academics",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Computer Services Centre",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Maintenance",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Miscellaneous",
		complaint_level_id=db.complaint_levels(complaint_level_name='Institute'),
	)

def hostel_complaint_domain_set():
	db.complaint_domain.insert(
		complaint_domain_name="Infrastructure",
		complaint_level_id=db.complaint_levels(complaint_level_name='Hostel'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Mess",
		complaint_level_id=db.complaint_levels(complaint_level_name='Hostel'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Administration",
		complaint_level_id=db.complaint_levels(complaint_level_name='Hostel'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Security",
		complaint_level_id=db.complaint_levels(complaint_level_name='Hostel'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Sports",
		complaint_level_id=db.complaint_levels(complaint_level_name='Hostel'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Maintenance",
		complaint_level_id=db.complaint_levels(complaint_level_name='Hostel'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Miscellaneous",
		complaint_level_id=db.complaint_levels(complaint_level_name='Hostel'),
	)

def individual_complaint_domain_set():
	db.complaint_domain.insert(
		complaint_domain_name="Electricity",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Plumbing",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Carpentry",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="UG Section",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="PG Section",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Accounts Section",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Students Counselling Service",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Ragging",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Hostel Administration",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Security",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

	db.complaint_domain.insert(
		complaint_domain_name="Miscellaneous",
		complaint_level_id=db.complaint_levels(complaint_level_name='Individual'),
	)

def group_names_set():
	db.user_group_names.insert(
		group_name="Institute",
	)

	db.user_group_names.insert(
		group_name="Institute Administration",
	)

	db.user_group_names.insert(
		group_name="UG Section",
	)

	db.user_group_names.insert(
		group_name="PG Section",
	)

	db.user_group_names.insert(
		group_name="BSA",
	)

	db.user_group_names.insert(
		group_name="BRCA",
	)

	db.user_group_names.insert(
		group_name="BHM",
	)

	db.user_group_names.insert(
		group_name="BSW",
	)

	db.user_group_names.insert(
		group_name="BSP",
	)


	db.user_group_names.insert(
		group_name="Electricity Department",
	)


	db.user_group_names.insert(
		group_name="Plumbing Department",
	)


	db.user_group_names.insert(
		group_name="Carpentry Department",
	)


	db.user_group_names.insert(
		group_name="Canteen Department",
	)


	db.user_group_names.insert(
		group_name="Accounts Section",
	)


	db.user_group_names.insert(
		group_name="Security Department",
	)


	db.user_group_names.insert(
		group_name="Accounts Section",
	)


	db.user_group_names.insert(
		group_name="Computer Services Centre",
	)


	db.user_group_names.insert(
		group_name="Students Counselling Service",
	)


	db.user_group_names.insert(
		group_name="Aravali Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Karakoram Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Nilgiri Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Jwalamukhi Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Kumaon Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Vindhyachal Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Shivalik Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Satpura Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Zanskar Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Girnar Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Udaigiri Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Kailash Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Himadri Hostel Admin Group",
	)


	db.user_group_names.insert(
		group_name="Aravali Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Karakoram Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Nilgiri Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Jwalamukhi Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Kumaon Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Vindhyachal Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Shivalik Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Satpura Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Zanskar Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Girnar Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Udaigiri Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Kailash Hostel Residents Group",
	)


	db.user_group_names.insert(
		group_name="Himadri Hostel Residents Group",
	)

def hostels_set():
	admin_grp = db.user_group_names(group_name="Aravali Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Aravali Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Aravali",
	)


	admin_grp = db.user_group_names(group_name="Karakoram Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Karakoram Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Karakoram",
	)


	admin_grp = db.user_group_names(group_name="Nilgiri Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Nilgiri Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Nilgiri",
	)


	admin_grp = db.user_group_names(group_name="Jwalamukhi Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Jwalamukhi Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Jwalamukhi",
	)


	admin_grp = db.user_group_names(group_name="Kumaon Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Kumaon Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Kumaon",
	)


	admin_grp = db.user_group_names(group_name="Vindhyachal Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Vindhyachal Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Vindhyachal",
	)


	admin_grp = db.user_group_names(group_name="Shivalik Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Shivalik Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Shivalik",
	)


	admin_grp = db.user_group_names(group_name="Satpura Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Satpura Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Satpura",
	)


	admin_grp = db.user_group_names(group_name="Zanskar Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Zanskar Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Zanskar",
	)


	admin_grp = db.user_group_names(group_name="Girnar Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Girnar Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Girnar",
	)


	admin_grp = db.user_group_names(group_name="Udaigiri Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Udaigiri Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Udaigiri",
	)


	admin_grp = db.user_group_names(group_name="Kailash Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Kailash Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Kailash",
	)


	admin_grp = db.user_group_names(group_name="Himadri Hostel Admin Group")
	res_grp = db.user_group_names(group_name="Himadri Hostel Residents Group")
	db.hostels.insert(
		hostel_admin_group_id=admin_grp,
		hostel_residents_group_id=res_grp,
		hostel_name="Himadri",
	)

def hostel_management_set():
	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Aravali").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Karakoram").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Nilgiri").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Jwalamukhi").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Kumaon").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Vindhyachal").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Shivalik").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Satpura").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Zanskar").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Girnar").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Udaigiri").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Kailash").id
	)

	db.hostel_management.insert(
		hostel_id=db.hostels(hostel_name="Himadri").id
	)

def add_to_grp(grp_name,user_id):
	db.group_members.insert(user_id=user_id,group_id=db.user_group_names(group_name=grp_name),)

def users_add():
	usr=db.users.insert(
		username='std1',
		first_name='student',
		last_name='1',
		password='12345',
		hostel_id=db.hostels(hostel_name="Aravali").id,
	)
	add_to_grp("Institute",usr)
	add_to_grp("Aravali Hostel Residents Group",usr)

	usr=db.users.insert(
		username='std2',
		first_name='student',
		last_name='2',
		password='12345',
		hostel_id=db.hostels(hostel_name='Aravali').id,
	)
	
	add_to_grp("Institute",usr)
	add_to_grp("Aravali Hostel Residents Group",usr)
	#Make him mess secretry of Aravali
	hstl_id = db.hostels(hostel_name="Aravali").id
	db.executesql('UPDATE hostel_management SET mess_secretary_user_id='+str(usr.id)+' WHERE hostel_id='+str(hstl_id)+';')

	#Adding 2 electricians
	usr=db.users.insert(
		username='ell1',
		first_name='electrician',
		last_name='1',
		password='12345',
	)
	add_to_grp("Electricity Department",usr)
	
	usr=db.users.insert(
		username='ell2',
		first_name='electrician',
		last_name='2',
		password='12345',
	)
	add_to_grp("Electricity Department",usr)
	
def reset_db():
	clear_all()
	complaint_levels_set()
	individual_complaint_domain_set()
	hostel_complaint_domain_set()
	institute_complaint_domain_set()
	group_names_set()
	hostels_set()
	hostel_management_set()
	users_add()
