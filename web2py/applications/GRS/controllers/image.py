@request.restful()
def download():
	response.view = 'generic.json'
	def GET(image_id):
		response.view = 'generic.json'
		image = db.pictures(id=image_id)
		return dict(image=image)
	return locals()

@request.restful()
def upload():
	response.view = 'generic.json'
	def POST(*tmp_args,**sign_input):
		ret = db[db.pictures].validate_and_insert(**sign_input)
		return dict(image=ret)
	def GET(*tmp_args,**sign_input):
		ret = db[db.pictures].validate_and_insert(**sign_input)
		return dict(image=ret)
	return locals()
