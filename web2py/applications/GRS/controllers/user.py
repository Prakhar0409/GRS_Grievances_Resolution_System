@request.restful()
def validation():
	response.view = 'generic.json'
	def GET():			#######TO DO
		return dict(data = True)
	return locals()

@request.restful()
def login():
	response.view = 'generic.json'
	def POST(*tmp_args,**complaint_input):
		user = auth.login_bare(**complaint_input)
    		return dict(success=False if not user else True, user=user)
	def GET(*tmp_args,**complaint_input):
		user = auth.login_bare(**complaint_input)
    		return dict(success=False if not user else True, user=user)
	return locals()

@request.restful()
def signup():
	response.view = 'generic.json'
	def POST(*tmp_args,**complaint_input):
		form = auth.register(**complaint_input)
    		return dict(success=False)
	def GET(*tmp_args,**complaint_input):
		form = auth.register(**complaint_input)
    		return dict(success=False)
	return locals()
