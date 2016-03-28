@request.restful()
def all():
	response.view = 'generic.json'
	def GET(*tmp_args,**status_input):
		usr = request.vars.user_id
		notif = db(db.notifications.user_id=usr).select()
		return notif
	def POST(*tmp_args,**status_input):
		usr = request.vars.user_id
		notif = db(db.notifications.user_id=usr).select()
		return notif
	return locals()
