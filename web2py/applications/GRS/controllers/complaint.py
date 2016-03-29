@request.restful()
def details():
	response.view = 'generic.json'
	def GET(*tmp_args,**status_input):
		data = db.complaints(id=request.args[0])
		ret={}
		ret['complaint_id']=data.id
		ret['title']=data.complaint_title
		ret['description']=data.complaint_details
		ret['posted_by']=data.posted_by
		ret['image_id']=data.photo_id
		ret['posted_on']=data.date_posted
		ret['work_started']=data.date_work_taken_on
		ret['resolved_on']=data.date_resolved
		ret['upvote_count']=data.upvotes_count
		ret['downvote_count']=data.downvotes_count
		ret['level_name']=db.complaint_levels(id=db.complaint_domain(id=data.complaint_domain_id).complaint_level_id).complaint_level_name
		ret['level_id']=db.complaint_domain(id=data.complaint_domain_id).complaint_level_id
		ret['domain_name']=db.complaint_domain(id=data.complaint_domain_id).complaint_domain_name
		ret['domain_id']=data.complaint_domain_id

		ret['status_id']=data.status_id

		ret['vote_status']=data.complaint_title

#		ret['undertaken_by']=data.complaint_title

		ret['previously_read']=data.complaint_title

		ret['bookmarked']=check_bookmark(auth.user.id,data.id)
		return dict(data=ret)

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
		if(len(tmp_args) and tmp_args[0]=='comment'):
			ret_status = db[db.status_comments].validate_and_insert(**status_input)
			book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
			for index in range(len(book_usrs)):
				notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=2,notification_item_id=ret_cmnt)
			return ret_status
		else:
			ret_status = db[db.complaint_status].validate_and_insert(**status_input)
			db.executesql("UPDATE complaints SET status_id="+str(ret_status.id)+" WHERE id="+str(request.vars.complaint_id_)+';')
			book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
			for index in range(len(book_usrs)):
				notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=2,notification_item_id=ret_cmnt)
			return ret_status
	def POST(*tmp_args,**status_input):
		if(len(tmp_args) and tmp_args[0]=='comment'):
			ret_status = db[db.status_comments].validate_and_insert(**status_input)
			book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
			for index in range(len(book_usrs)):
				notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=2,notification_item_id=ret_cmnt)
			return ret_status
		else:
			ret_status = db[db.complaint_status].validate_and_insert(**status_input)
			db.executesql("UPDATE complaints SET status_id="+str(ret_status.id)+" WHERE id="+str(request.vars.complaint_id_)+';')
			book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
			for index in range(len(book_usrs)):
				notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=2,notification_item_id=ret_cmnt)
			return ret_status
	return locals()

@request.restful()
def complaints():
	response.view = 'generic.json'
	def GET(*tmp_args,**status_input):
		if not auth.is_logged_in() :
			return dict()
		complaint_section=request.args[0]
		user_id=auth.user.id
		if(complaint_section=='bookmarked'):
			all_made = db(db.bookmarks.complaint_id>0).select()
			ret = []
			for index in range(len(all_made)):
				from_user = all_made[index].user_id
				user_id1 = db.users(id=user_id).id
				if(from_user == user_id1):
					temp=db.complaints(id=all_made[index].complaint_id)
					temp["bookmarked"]=check_bookmark(user_id,all_made[index].complaint_id)
					temp["to_resolve"]=check_resolve(user_id,all_made[index].complaint_id)
					temp["solvable"]=check_solvable(user_id,all_made[index].complaint_id)
					ret.append(temp)
			return dict(data = ret)
		elif(complaint_section=='concern'):
			all_made = db(db.complaints_concerning_user.complaint_id>0).select()
			ret = []
			for index in range(len(all_made)):
				from_user = all_made[index].user_id
				to_group = all_made[index].group_id
				user_id1 = db.users(id=user_id).id
				if(from_user == user_id1):
					temp=db.complaints(id=all_made[index].complaint_id)
					temp["bookmarked"]=check_bookmark(user_id,all_made[index].complaint_id)
					temp["to_resolve"]=check_resolve(user_id,all_made[index].complaint_id)
					temp["solvable"]=check_solvable(user_id,all_made[index].complaint_id)
					ret.append(temp)
				else:
					all_members = db(db.group_members.group_id==to_group).select()
					for index1 in range(len(all_members)):
						user1 = db.users(id=all_members[index1].user_id).id
						if(user1==user_id1):
							temp=db.complaints(id=all_made[index].complaint_id)
							temp["bookmarked"]=check_bookmark(user_id,all_made[index].complaint_id)
							temp["to_resolve"]=check_resolve(user_id,all_made[index].complaint_id)
							temp["solvable"]=check_solvable(user_id,all_made[index].complaint_id)
							ret.append(temp)
			return dict(data = ret)
		elif(complaint_section=='resolve'):
			all_made = db(db.complaints_with_resolving_rights_to_user.complaint_id>0).select()
			ret = []
			for index in range(len(all_made)):
				from_user = all_made[index].user_id
				to_group = all_made[index].group_id
				user_id1 = db.users(id=user_id).id
				if(from_user == user_id1):
					temp=db.complaints(id=all_made[index].complaint_id)
					temp["bookmarked"]=check_bookmark(user_id,all_made[index].complaint_id)
					temp["to_resolve"]=check_resolve(user_id,all_made[index].complaint_id)
					temp["solvable"]=check_solvable(user_id,all_made[index].complaint_id)
					ret.append(temp)
				else:
					all_members = db(db.group_members.group_id==to_group).select()
					for index1 in range(len(all_members)):
						user1 = db.users(id=all_members[index1].user_id).id
						if(user1==user_id1):
							temp=db.complaints(id=all_made[index].complaint_id)
							temp["bookmarked"]=check_bookmark(user_id,all_made[index].complaint_id)
							temp["to_resolve"]=check_resolve(user_id,all_made[index].complaint_id)
							temp["solvable"]=check_solvable(user_id,all_made[index].complaint_id)
							ret.append(temp)
			return dict(data = ret)
		elif(complaint_section=='solve'):
			all_made = db(db.complaints_made_to_user.complaint_id>0).select()
			ret = []
			for index in range(len(all_made)):
				from_user = all_made[index].user_id
				to_group = all_made[index].group_id
				user_id1 = db.users(id=user_id).id
				if(from_user == user_id1):
					temp=db.complaints(id=all_made[index].complaint_id)
					temp["bookmarked"]=check_bookmark(user_id,all_made[index].complaint_id)
					temp["to_resolve"]=check_resolve(user_id,all_made[index].complaint_id)
					temp["solvable"]=check_solvable(user_id,all_made[index].complaint_id)
					ret.append(temp)
				else:
					all_members = db(db.group_members.group_id==to_group).select()
					for index1 in range(len(all_members)):
						user1 = db.users(id=all_members[index1].user_id).id
						if(user1==user_id1):
							temp=db.complaints(id=all_made[index].complaint_id)
							temp["bookmarked"]=check_bookmark(user_id,all_made[index].complaint_id)
							temp["to_resolve"]=check_resolve(user_id,all_made[index].complaint_id)
							temp["solvable"]=check_solvable(user_id,all_made[index].complaint_id)
							ret.append(temp)
			return dict(data = ret)
	return locals()


@request.restful()
def create():
	response.view = 'generic.json'
	def make_complaint(complaint_id,user_id,present_level_name,present_domain_name,affectt,resolvv,solvv):
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
				for index in range(len(solvv)):
					if solvv.type=='1':
						cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=solvv.id)
					else:
						cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=solvv.id)
				for index in range(len(resolvv)):
					if resolvv.type=='1':
						cmplt = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=resolvv.id)
					else:
						cmplt = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=resolvv.id)
					
				for index in range(len(affectt)):
					if resolvv.type=='1':
						cmplt = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=1,group_id=affectt.id)
					else:
						cmplt = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=0,user_id=affectt.id)

		elif present_level_name=='Hostel':

			hstl = db.users(id=user_id).hostel_id;
			hostel_admin_grp = db.hostels(id=hstl).hostel_admin_group_id;
			hostel_res_grp = db.hostels(id=hstl).hostel_residents_group_id;
			mess_secretry = db.hostel_management(hostel_id=hstl).mess_secretary_user_id
			maintenance_secretry = db.hostel_management(hostel_id=hstl).mess_secretary_user_id
			sports_secretry = db.hostel_management(hostel_id=hstl).mess_secretary_user_id
			concern = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_res_grp)
			concern = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=1,group_id=hostel_admin_grp)
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
			concern = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=1,group_id=db.user_group_names(group_name='Institute Administration').id)
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

		elif present_domain_name=='Miscellaneous':
			for index in range(len(solvv)):
				if solvv.type=='1':
					cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=solvv.id)
				else:
					cmplt = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=solvv.id)
			for index in range(len(resolvv)):
				if resolvv.type=='1':
					cmplt = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=resolvv.id)
				else:
					cmplt = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=resolvv.id)
				
			for index in range(len(affectt)):
				if resolvv.type=='1':
					cmplt = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=1,group_id=affectt.id)
				else:
					cmplt = db.complaints_concerning_user.insert(complaint_id=complaint_id,id_type=0,user_id=affectt.id)

	def POST(*tmp_args,**complaint_input):
		cmpln={}
		cmpln['complaint_title']=complaint_input['title']
		cmpln['complaint_details']=complaint_input['description']
		cmpln['posted_by']=auth.user.id
		try:
			cmpln['picture_id']=complaint_input['image_id']
		except:
			print 'missing parameter'
		try:
			cmpln['complaint_level_id']=complaint_input['level_id']
		except:
			print 'missing parameter'
		
		try:
			cmpln['downvotes_count']=0
		except:
			print 'missing parameter'
		
		try:
			cmpln['upvotes_count']=0
		except:
			print 'missing parameter'
		
		try:
			cmpln['complaint_domain_id']=complaint_input['domain_id']
		except:
			print 'missing parameter'
		cmplt = db[db.complaints].validate_and_insert(**cmpln)
		complaint_id = cmplt.id
		user_id = db.users(id=auth.user.id)
		present_domain_name = db.complaint_domain(id=complaint_input['domain_id']).complaint_domain_name
		present_level_name = db.complaint_levels(id=db.complaint_domain(id=request.vars.domain_id).complaint_level_id).complaint_level_name
		affectin={}
		cmpln_to={}
		cmpln_rsslv={}
		
		try:
			affectin=complaint_input['complaint_affecting']
		except:
			print 'missing parameter'

		try:
			cmpl_to=complaint_input['complaint_to']
		except:
			print 'missing parameter'		
		
		try:
			affectin=complaint_input['resolvable_by']
		except:
			print 'missing parameter'
		
		return make_complaint(complaint_id,user_id,present_level_name,present_domain_name,affectin,cmpln_to,cmpln_rsslv)
	def GET(*tmp_args,**complaint_input):
		cmpln={}
		cmpln['complaint_title']=complaint_input['title']
		cmpln['complaint_details']=complaint_input['description']
		cmpln['posted_by']=auth.user.id
		try:
			cmpln['picture_id']=complaint_input['image_id']
		except:
			print 'missing parameter'
		try:
			cmpln['complaint_level_id']=complaint_input['level_id']
		except:
			print 'missing parameter'
		
		try:
			cmpln['downvotes_count']=0
		except:
			print 'missing parameter'
		
		try:
			cmpln['upvotes_count']=0
		except:
			print 'missing parameter'
		
		try:
			cmpln['complaint_domain_id']=complaint_input['domain_id']
		except:
			print 'missing parameter'
		cmplt = db[db.complaints].validate_and_insert(**cmpln)
		complaint_id = cmplt.id
		user_id = db.users(id=auth.user.id)
		present_domain_name = db.complaint_domain(id=complaint_input['domain_id']).complaint_domain_name
		present_level_name = db.complaint_levels(id=db.complaint_domain(id=request.vars.domain_id).complaint_level_id).complaint_level_name
		affectin={}
		cmpln_to={}
		cmpln_rsslv={}
		
		try:
			affectin=complaint_input['complaint_affecting']
		except:
			print 'missing parameter'

		try:
			cmpl_to=complaint_input['complaint_to']
		except:
			print 'missing parameter'		
		
		try:
			affectin=complaint_input['resolvable_by']
		except:
			print 'missing parameter'
		
		return make_complaint(complaint_id,user_id,present_level_name,present_domain_name,affectin,cmpln_to,cmpln_rsslv)
	return locals()

@request.restful()
def follow():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		fllw = db[db.bookmarks].validate_and_insert(**follow_input)
		db.executesql('UPDATE bookmarks SET user_id='+str(auth.user.id)+' WHERE id='+str(fllw.id)+';')
		return dict(success=True)
	def GET(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		fllw = db[db.bookmarks].validate_and_insert(**follow_input)
		db.executesql('UPDATE bookmarks SET user_id='+str(auth.user.id)+' WHERE id='+str(fllw.id)+';')
		return dict(success=True)
	return locals()

@request.restful()
def unfollow():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		db.executesql('DELETE FROM bookmarks WHERE complaint_id='+str(request.vars.complaint_id)+' AND user_id='+str(auth.user.id)+';')
		return dict(success=True)
	def GET(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		db.executesql('DELETE FROM bookmarks WHERE complaint_id='+str(request.vars.complaint_id)+' AND user_id='+str(auth.user.id)+';')
		return dict(success=True)
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
		done = db.executesql('UPDATE complaints SET redirected_to_user_id='+str(userid_to)+', redirected_to_type='+str(redirect_type)+', redirected_by_user_id='+str(userid_from)+' WHERE id='+str(complaint_id)+';')
		if(redirect_type==0):
			solve_add = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=userid_to)
			if(check_resolve(userid_from,complaint_id)):
				resolve_add = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=userid_to)
		else:
			solve_add = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=userid_to)
			userid_frm = db.users(id=userid_from).id
			if(check_resolve(userid_frm,complaint_id)):
				resolve_add = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=userid_to)
		return dict(success=True)
	def GET(*tmp_args,**follow_input):
		userid_from = request.vars.redirect_from
		redirect_type = request.vars.redirect_to_type
		userid_to = request.vars.redirect_to
		complaint_id = request.vars.complaint_id
		done = db.executesql('UPDATE complaints SET redirected_to_user_id='+str(userid_to)+', redirected_to_type='+str(redirect_type)+', redirected_by_user_id='+str(userid_from)+' WHERE id='+str(complaint_id)+';')
		if(redirect_type==0):
			solve_add = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=userid_to)
			if(check_resolve(userid_from,complaint_id)):
				resolve_add = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=0,user_id=userid_to)
		else:
			solve_add = db.complaints_made_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=userid_to)
			userid_frm = db.users(id=userid_from).id
			if(check_resolve(userid_frm,complaint_id)):
				resolve_add = db.complaints_with_resolving_rights_to_user.insert(complaint_id=complaint_id,id_type=1,group_id=userid_to)
		return dict(success=True)
	return locals()


@request.restful()
def comment():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		ret_cmnt = db[db.comments].validate_and_insert(**follow_input)
		db.executesql('UPDATE comments SET user_id='+str(auth.user.id)+' WHERE id='+str(ret_cmnt.id)+';')
		book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
		for index in range(len(book_usrs)):
			notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=0,notification_item_id=ret_cmnt)
		return ret_cmnt
	def GET(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		ret_cmnt = db[db.comments].validate_and_insert(**follow_input)
		db.executesql('UPDATE comments SET user_id='+str(auth.user.id)+' WHERE id='+str(ret_cmnt.id)+';')
		book_usrs = db(db.bookmarks.complaint_id==request.vars.complaint_id).select()
		for index in range(len(book_usrs)):
			notif = db.notifications.insert(user_id=book_usrs[index].user_id,notification_type=0,notification_item_id=ret_cmnt)
		return ret_cmnt
	return locals()


def check_resolve(user_id,complaint_id):
	all_made = db(db.complaints_with_resolving_rights_to_user.complaint_id==complaint_id).select()
	ret = []
	for index in range(len(all_made)):
		from_user = all_made[index].user_id
		to_group = all_made[index].group_id
		user_id1 = user_id
		if(from_user == user_id1):
			ret.append(all_made[index])
		else:
			all_members = db(db.group_members.group_id==to_group).select()
			for index1 in range(len(all_members)):
				user1 = db.users(id=all_members[index1].user_id).id
				if(user1==user_id1):
					ret.append(all_made[index])
	return (len(ret)>0)

@request.restful()
def resolvable():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		else:
			return dict(resolvable = check_resolve(auth.user.id,request.vars.complaint_id))
	def GET(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		else:
			return dict(resolvable = check_resolve(auth.user.id,request.vars.complaint_id))
	return locals()


def check_bookmark(user_id,complaint_id):
	all_made = db(db.bookmarks.complaint_id==complaint_id).select()
	ret = []
	for index in range(len(all_made)):
		from_user = all_made[index].user_id
		user_id1 = user_id
		if(from_user == user_id1):
			ret.append(all_made[index])
	return (len(ret)>0)


@request.restful()
def is_bookmark():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		else:
			return dict(is_bookmark = check_bookmark(auth.user.id,request.vars.complaint_id))
	def GET(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		else:
			return dict(is_bookmark = check_bookmark(auth.user.id,request.vars.complaint_id))
	return locals()


def check_solvable(user_id,complaint_id):
	all_made = db(db.complaints_made_to_user.complaint_id==complaint_id).select()
	ret = []
	for index in range(len(all_made)):
		from_user = all_made[index].user_id
		user_id1 = user_id
		if(from_user == user_id1):
			ret.append(all_made[index])
	return (len(ret)>0)


def ret_vote(user_id,complaint_id):
	all_made = db(db.votes.complaint_id==complaint_id).select()
	ret = 0
	for index in range(len(all_made)):
		from_user = all_made[index].user_id
		user_id1 = user_id
		if(from_user == user_id1):
			ret=all_made[index]
	if not 	ret==0:
		return dict(voted=True,vote=ret)
	else:
		return dict(voted=False)


def correct_vote(user_id,complaint_id):
	all_made = db(db.votes.complaint_id==complaint_id).select()
	ret = 0
	for index in range(len(all_made)):
		from_user = all_made[index].user_id
		user_id1 = user_id
		if(from_user == user_id1):
			ret=all_made[index]
	if not 	ret==0:
		if ret.vote_type==-1 :
			prev = db.complaints(id=complaint_id).downvotes_count
			db.executesql("UPDATE complaints SET downvotes_count="+str(prev-1)+" WHERE id="+str(complaint_id)+';')
		elif ret.vote_type==1:
			prev = db.complaints(id=complaint_id).upvotes_count
			db.executesql("UPDATE complaints SET upvotes_count="+str(prev-1)+" WHERE id="+str(complaint_id)+';')

def correct_vote1(user_id,complaint_id):
	all_made = db(db.votes.complaint_id==complaint_id).select()
	ret = 0
	for index in range(len(all_made)):
		from_user = all_made[index].user_id
		user_id1 = user_id
		if(from_user == user_id1):
			ret=all_made[index]
	if not 	ret==0:
		if ret.vote_type==-1 :
			prev = db.complaints(id=complaint_id).downvotes_count
			db.executesql("UPDATE complaints SET downvotes_count="+str(prev+1)+" WHERE id="+str(complaint_id)+';')
		elif ret.vote_type==1:
			prev = db.complaints(id=complaint_id).upvotes_count
			db.executesql("UPDATE complaints SET upvotes_count="+str(prev+1)+" WHERE id="+str(complaint_id)+';')

@request.restful()
def vote_made():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		else:
			return ret_vote(auth.user.id,request.vars.complaint_id)
	def GET(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		else:
			return ret_vote(auth.user.id,request.vars.complaint_id)
	return locals()


@request.restful()
def vote():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		else:
			correct_vote(auth.user.id,request.vars.complaint_id)
			db.votes.insert(user_id=auth.user.id,vote_type=request.vars.vote_type,complaint_id=request.vars.complaint_id)
			return dict(success=True)
	def GET(*tmp_args,**follow_input):
		if not auth.is_logged_in():
			return dict()
		else:
			correct_vote(auth.user.id,request.vars.complaint_id)
			db.votes.insert(user_id=auth.user.id,vote_type=request.vars.vote_type,complaint_id=request.vars.complaint_id)
			correct_vote1(auth.user.id,request.vars.complaint_id)
			return dict(success=True)
	return locals()


@request.restful()
def mark_resolve():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if (not auth.is_logged_in()) or (not check_resolve(auth.user.id,request.vars.complaint_id)):
			return dict()
		else:
			cmpln=request.vars.complaint_id
			dtnow=str(datetime.now())
			db.executesql("UPDATE complaints SET date_resolved=1 WHERE id="+str(request.vars.complaint_id)+';')
			return dict(success=True)
	def GET(*tmp_args,**follow_input):
		if (not auth.is_logged_in()) or (not check_resolve(auth.user.id,request.vars.complaint_id)):
			return dict()
		else:
			cmpln=request.vars.complaint_id
			dtnow=str(datetime.now())
			db.executesql("UPDATE complaints SET date_resolved=1 WHERE id="+str(request.vars.complaint_id)+';')
			return dict(success=True)
	return locals()


@request.restful()
def is_resolved():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if (not auth.is_logged_in()) or (not check_resolve(auth.user.id,request.vars.complaint_id)):
			return dict()
		else:
			cmpln=request.vars.complaint_id
			return dict(resolved=db.complaint(date_resolved))
	def GET(*tmp_args,**follow_input):
		if (not auth.is_logged_in()) or (not check_resolve(auth.user.id,request.vars.complaint_id)):
			return dict()
		else:
			cmpln=request.vars.complaint_id
			return dict(resolved=(db.complaints(id=cmpln)))
	return locals()

'''
@request.restful()
def is_resolved():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		if (not auth.is_logged_in()) or (not check_resolve(auth.user.id,request.vars.complaint_id)):
			return dict()
		else:
			cmpln=request.vars.complaint_id
			return dict(resolved=db.complaint(date_resolved))
	def GET(*tmp_args,**follow_input):
		if (not auth.is_logged_in()) or (not check_resolve(auth.user.id,request.vars.complaint_id)):
			return dict()
		else:
			cmpln=request.vars.complaint_id
			return dict(resolved=(db.complaints(id=cmpln)))
	return locals()
'''

