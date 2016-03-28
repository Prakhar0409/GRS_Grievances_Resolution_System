@request.restful()
def details():
	response.view = 'generic.json'
	def GET(complaint_id):
		return dict(data = db.complaints(id=complaint_id))
	return locals()

@request.restful()
def levels():
	response.view = 'generic.json'
	def GET():
		return dict(data = db(db.complaint_levels.id>0).select())
	return locals()

@request.restful()
def domains():
	response.view = 'generic.json'
	def GET(level_id):
		return dict(data = db(db.complaint_domain.complaint_level_id==level_id).select())
	return locals()

@request.restful()
def bookmark():
	response.view = 'generic.json'
	def GET(complaint_id):
		data = db(db.bookmarks.complaint_id==complaint_id).select()
		if len(data)>0:
			return dict(bookmarked = True)
		else:
			return dict(bookmarked = False)
	return locals()

@request.restful()
def status():
	response.view = 'generic.json'
	def GET(*tmp_args,**status_input):
		if(tmp_args[0]=='comment'):
			ret_status = db[db.status_comments].validate_and_insert(**status_input)
			book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
			for index in range(len(book_usrs)):
				notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=2,notification_item_id=ret_cmnt)
			return ret_status
		else
			ret_status = db[db.complaint_status].validate_and_insert(**status_input)
			book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
			for index in range(len(book_usrs)):
				notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=2,notification_item_id=ret_cmnt)
			return ret_status
	def POST(*tmp_args,**status_input):
		if(tmp_args[0]=='comment'):
			ret_status = db[db.status_comments].validate_and_insert(**status_input)
			book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
			for index in range(len(book_usrs)):
				notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=2,notification_item_id=ret_cmnt)
			return ret_status
		else
			ret_status = db[db.complaint_status].validate_and_insert(**status_input)
			book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
			for index in range(len(book_usrs)):
				notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=2,notification_item_id=ret_cmnt)
			return ret_status
	return locals()

@request.restful()
def complaints():
	response.view = 'generic.json'
	def GET(complaint_section,user_id):
		def is_in_group(grp_id,usr_id):
			if not grp_id :
				return False
			membership = db(db.group_members.user_id==usr_id and db.group_members.group_id==58).select()
			return dict(mem=membership)
			if (not membership):
				return False
			return True
		#return is_in_group(58,user_id)
		if(complaint_section=='bookmarked'):
			all_made = db(db.bookmarks.complaint_id>0).select()
			ret = []
			for index in range(len(all_made)):
				from_user = all_made[index].user_id
				to_group = all_made[index].group_id
				user_id1 = db.users(id=user_id).id
				if(from_user == user_id1):
					ret.append(all_made[index])
				else:
					all_members = db(db.group_members.group_id==to_group).select()
					for index1 in range(len(all_members)):
						user1 = db.users(id=all_members[index1].user_id).id
						return dict(efw = user1, ewq=user_id1, ewdd=(user1==user_id1))
						if(user1==user_id1):
							ret.append(all_made[index])
			return dict(data = ret)
		elif(complaint_section=='concern'):
			all_made = db(db.complaints_concerning_user.complaint_id>0).select()
			ret = []
			for index in range(len(all_made)):
				from_user = all_made[index].user_id
				to_group = all_made[index].group_id
				user_id1 = db.users(id=user_id).id
				if(from_user == user_id1):
					ret.append(all_made[index])
				else:
					all_members = db(db.group_members.group_id==to_group).select()
					for index1 in range(len(all_members)):
						user1 = db.users(id=all_members[index1].user_id).id
						return dict(efw = user1, ewq=user_id1, ewdd=(user1==user_id1))
						if(user1==user_id1):
							ret.append(all_made[index])
			return dict(data = ret)
		elif(complaint_section=='resolve'):
			all_made = db(db.complaints_with_resolving_rights_to_user.complaint_id>0).select()
			ret = []
			for index in range(len(all_made)):
				from_user = all_made[index].user_id
				to_group = all_made[index].group_id
				user_id1 = db.users(id=user_id).id
				if(from_user == user_id1):
					ret.append(all_made[index])
				else:
					all_members = db(db.group_members.group_id==to_group).select()
					for index1 in range(len(all_members)):
						user1 = db.users(id=all_members[index1].user_id).id
						return dict(efw = user1, ewq=user_id1, ewdd=(user1==user_id1))
						if(user1==user_id1):
							ret.append(all_made[index])
			return dict(data = ret)
		elif(complaint_section=='solve'):
			all_made = db(db.complaints_made_to_user.complaint_id>0).select()
			ret = []
			for index in range(len(all_made)):
				from_user = all_made[index].user_id
				to_group = all_made[index].group_id
				user_id1 = db.users(id=user_id).id
				if(from_user == user_id1):
					ret.append(all_made[index])
				else:
					all_members = db(db.group_members.group_id==to_group).select()
					for index1 in range(len(all_members)):
						user1 = db.users(id=all_members[index1].user_id).id
						return dict(efw = user1, ewq=user_id1, ewdd=(user1==user_id1))
						if(user1==user_id1):
							ret.append(all_made[index])
			return dict(data = ret)
	return locals()


@request.restful()
def create():
	response.view = 'generic.json'
	def POST(*tmp_args,**complaint_input):
		cmplt = db[db.complaints].validate_and_insert(**complaint_input)
		complaint_id = cmplt.id
		user_id = request.vars.user_id
		concern = db.complaints_concerning_user.insert(complaint_id=complaint_id,user_id=user_id)
		present_domain_name = db.complaint_domain.complaint_domain_name(id=request.vars.complaint_domain_id)
		return dict(ret = present_domain_name)
		#if
		#	cmplt = db[db.complaints].validate_and_insert(**complaint_input)
	def GET(*tmp_args,**complaint_input):
		cmplt = db[db.complaints].validate_and_insert(**complaint_input)
		complaint_id = cmplt.id
		user_id = db.users(id=request.vars.posted_by)
		present_domain_name = db.complaint_domain(id=request.vars.complaint_domain_id).complaint_domain_name
		present_level_name = db.complaint_levels(id=db.complaint_domain(id=request.vars.complaint_domain_id).complaint_level_id).complaint_level_name
		if present_level_name=='Individual':
			cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=user_id)
			concern = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=0,user_id=user_id)
			if present_domain_name=='Electricity':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Electricity Department').id)
			elif present_domain_name=='Plumbing':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Plumbing Department').id)
			elif present_domain_name=='Carpentry':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Carpentry Department').id)
			elif present_domain_name=='UG Section':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='UG Section').id)
			elif present_domain_name=='PG Section':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='PG Section').id)
			elif present_domain_name=='Accounts Section':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Accounts Section').id)
			elif present_domain_name=='Students Counselling Service':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Students Counselling Service').id)
			elif present_domain_name=='Ragging':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Students Counselling Service').id)
			elif present_domain_name=='Hostel Administration':
				hstl = db.users(id=user_id).hostel_id;
				hostel_admin_grp = db.hostels(id=hstl).hostel_admin_group_id;
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)
			elif present_domain_name=='Security':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Security Department').id)
			

			elif present_domain_name=='Miscellaneous':
				cmplt = db[db.complaints].validate_and_insert(**complaint_input)


		elif present_level_name=='Hostel':

			hstl = db.users(id=user_id).hostel_id;
			hostel_admin_grp = db.hostels(id=hstl).hostel_admin_group_id;
			hostel_res_grp = db.hostels(id=hstl).hostel_residents_group_id;
			mess_secretry = db.hostel_management(hostel_id=hstl).mess_secretary_user_id
			maintenance_secretry = db.hostel_management(hostel_id=hstl).mess_secretary_user_id
			sports_secretry = db.hostel_management(hostel_id=hstl).mess_secretary_user_id
			concern = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_res_grp)
			if present_domain_name=='Infrastructure':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)
			elif present_domain_name=='Mess':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=mess_secretry)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=mess_secretry)
			elif present_domain_name=='Administration':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)
			elif present_domain_name=='Security':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)
			elif present_domain_name=='Sports':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=sports_secretry)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=sports_secretry)
			elif present_domain_name=='Maintenance':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=maintenance_secretry)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=maintenance_secretary)

			elif present_domain_name=='Miscellaneous':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)

		elif present_level_name=='Institute':
			concern = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute').id)
			if present_domain_name=='Infrastructure':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
			elif present_domain_name=='Administration':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
			elif present_domain_name=='Canteen and Food Outlets':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='BSW').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='BSW').id)
			elif present_domain_name=='Security':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='BSW').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='BSW').id)
			elif present_domain_name=='Sports':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='BSA').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='BSA').id)
			elif present_domain_name=='Culture':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='BRCA').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='BRCA').id)
			elif present_domain_name=='Academics':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
			elif present_domain_name=='Computer Services Centre':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Computer Services Centre').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Computer Services Centre').id)
			elif present_domain_name=='Maintenance':
				cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
				cmplt_rslv = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)


			elif present_domain_name=='Miscellaneous':
				cmplt = db[db.complaints].validate_and_insert(**complaint_input)


		else:	return dict(status = 'TO do===Miscellaneous')
	return locals()

@request.restful()
def vote():
	response.view = 'generic.json'
	def POST(*tmp_args,**vote_input):
		return db[db.votes].validate_and_insert(**vote_input)
	def GET(*tmp_args,**vote_input):
		return db[db.votes].validate_and_insert(**vote_input)
	return locals()

@request.restful()
def follow():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		return db[db.bookmarks].validate_and_insert(**follow_input)
	def GET(*tmp_args,**follow_input):
		return db[db.bookmarks].validate_and_insert(**follow_input)
	return locals()

@request.restful()
def read():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		return db[db.complaint_read].validate_and_insert(**follow_input)
	def GET(*tmp_args,**follow_input):
		return db[db.complaint_read].validate_and_insert(**follow_input)
	return locals()

@request.restful()
def is_read():
	response.view = 'generic.json'
	def GET(complaint_id):
		data = db(db.complaint_read.complaint_id==complaint_id).select()
		if len(data)>0:
			return dict(read = True)
		else:
			return dict(read = False)
    	return locals()

@request.restful()
def redirect():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		userid_from = request.vars.redirect_from
		redirect_type = request.vars.redirect_to_type
		userid_to = request.vars.redirect_to
		complaint_id = request.vars.complaint_id
		done = db.executesql('UPDATE complaints SET redirected_to_user_id='+userid_to+', redirected_to_type='+redirect_type+', redirected_by_user_id='+userid_from+' WHERE id='+complaint_id+';')
		if(redirect_type==0):
			solve_add = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=userid_to)
		else:
			solve_add = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=userid_to)
		return dict(success=True)
	def GET(*tmp_args,**follow_input):
		userid_from = request.vars.redirect_from
		redirect_type = request.vars.redirect_to_type
		userid_to = request.vars.redirect_to
		complaint_id = request.vars.complaint_id
		done = db.executesql('UPDATE complaints SET redirected_to_user_id='+userid_to+', redirected_to_type='+redirect_type+', redirected_by_user_id='+userid_from+' WHERE id='+complaint_id+';')
		if(redirect_type==0):
			solve_add = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=userid_to)
		else:
			solve_add = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=userid_to)
		return dict(success=True)
	return locals()


@request.restful()
def comment():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		ret_cmnt = db[db.comments].validate_and_insert(**follow_input)
		book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
		for index in range(len(book_usrs)):
			notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=0,notification_item_id=ret_cmnt)
		return ret_cmnt
	def GET(*tmp_args,**follow_input):
		ret_cmnt = db[db.comments].validate_and_insert(**follow_input)
		book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
		for index in range(len(book_usrs)):
			notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=0,notification_item_id=ret_cmnt)
		return ret_cmnt
	return locals()


