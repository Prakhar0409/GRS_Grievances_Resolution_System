@request.restful()
def comment():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		return db[db.status_comments].validate_and_insert(**follow_input)
	def GET(*tmp_args,**follow_input):
		return db[db.status_comments].validate_and_insert(**follow_input)
	return locals()


