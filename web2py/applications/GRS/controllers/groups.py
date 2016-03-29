@request.restful()
def list():
	response.view = 'generic.json'
	def GET():
		return dict(data = db(db.user_group_names.id>0).select())
	return locals()

@request.restful()
def request_membership():
	response.view = 'generic.json'
	def GET(*tmp_args,**var_input):
		if not auth.is_logged_in():
			return dict()
		group_id=db.user_group_names(group_name=request.args[0])
		group_head=db.group_heads(group_id=group_id).head_user_id
		db.validation_requests.insert(group_id=group_id,to_user_id=group_head,from_user_id=auth.user.id)
		return dict(success = True)
	return locals()


