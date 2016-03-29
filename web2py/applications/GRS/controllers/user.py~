@request.restful()
def validation():
	response.view = 'generic.json'
	def POST(*tmp_args,**complaint_input):
		if not auth.is_logged_in :
			return dict()
		user_id=auth.user.id
		if(len(request.args)==0):
			valid_list = db(db.validation_requests.to_user_id==user_id).select()
			return dict(validation_list=valid_list)
		elif(len(request.args)==1):
			val_id=request.vars.validation_id
			new_user=db.validation_requests(id=request.vars.validation_id).from_user_id
			vdt=request.vars.validate
			grp=request.args[0]
			if(vdt=='1'):
				db.executesql("UPDATE group_members SET is_validated='true' WHERE user_id="+str(new_user)+' AND group_id='+str(grp)+';')
				db.executesql('DELETE FROM validation_requests WHERE id='+val_id+';')
				db.notifications.insert(user_id=user_id,notification_type=-1,notification='Your membership request for group '+db.user_group_names(id=int(grp)).group_name+' has been accepted')
			if(vdt=='0'):
				db.executesql("DELETE FROM group_members WHERE user_id="+str(new_user)+' AND group_id='+str(grp)+';')
				db.executesql('DELETE FROM validation_requests WHERE from_user_id='+str(new_user)+' AND group_id='+str(grp)+';')
				db.notifications.insert(user_id=user_id,notification_type=-1,notification='Your membership request for group '+db.user_group_names(id=int(grp)).group_name+' has been rejected')
			return dict(success=True)
	def GET(*tmp_args,**complaint_input):
		if not auth.is_logged_in :
			return dict()
		user_id=auth.user.id
		if(len(request.args)==0):
			valid_list = db(db.validation_requests.to_user_id==user_id).select()
			return dict(validation_list=valid_list)
		elif(len(request.args)==1):
			val_id=request.vars.validation_id
			new_user=db.validation_requests(id=request.vars.validation_id).from_user_id
			vdt=request.vars.validate
			grp=request.args[0]
			if(vdt=='1'):
				db.executesql("UPDATE group_members SET is_validated='true' WHERE user_id="+str(new_user)+' AND group_id='+str(grp)+';')
				db.executesql('DELETE FROM validation_requests WHERE id='+val_id+';')
				db.notifications.insert(user_id=user_id,notification_type=-1,notification='Your membership request for group '+db.user_group_names(id=int(grp)).group_name+' has been accepted')
			if(vdt=='0'):
				db.executesql("DELETE FROM group_members WHERE user_id="+str(new_user)+' AND group_id='+str(grp)+';')
				db.executesql('DELETE FROM validation_requests WHERE from_user_id='+str(new_user)+' AND group_id='+str(grp)+';')
				db.notifications.insert(user_id=user_id,notification_type=-1,notification='Your membership request for group '+db.user_group_names(id=int(grp)).group_name+' has been rejected')
			return dict(success=True)
	return locals()
@request.restful()
def login():
	response.view = 'generic.json'
	def POST(*tmp_args,**complaint_input):
		username=request.vars.username
		password=request.vars.password
		user = auth.login_bare(username=username,password=password)
    		return dict(success=False if not user else True, user=user)
	def GET(*tmp_args,**complaint_input):
		username=request.vars.username
		password=request.vars.password
		user = auth.login_bare(username=username,password=password)
		return dict(success=False if not user else True, user=user)
	return locals()

@request.restful()
def logout():
	response.view = 'generic.json'
	return dict(success=True, loggedout=auth.logout())

@request.restful()
def signup():
	response.view = 'generic.json'
	def POST(*tmp_args,**sign_input):
		ret = db[db.users].validate_and_insert(**sign_input)
		return dict(user=ret)
	def GET(*tmp_args,**sign_input):
		ret = db[db.users].validate_and_insert(**sign_input)
		return dict(user=ret)
	return locals()
def profile():
	response.view = 'generic.json'
	if not auth.is_logged_in:
		return dict()
	user=auth.user
	user["hostel_name"]=db.hostels(id=user.hostel_id).hostel_name
	return dict(user=user)
