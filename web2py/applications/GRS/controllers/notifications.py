@request.restful()
def all():
	response.view = 'generic.json'
	def GET(*tmp_args,**status_input):
		if not auth.is_logged_in():
			return dict()
		usr = auth.user.id
		notif = db(db.notifications.user_id==usr).select()
		return dict(notifications=notif)
	def POST(*tmp_args,**status_input):
		if not auth.is_logged_in():
			return dict()
		usr = request.vars.user_id
		notif = db(db.notifications.user_id==usr).select()
		return dict(notifications=notif)
	return locals()
