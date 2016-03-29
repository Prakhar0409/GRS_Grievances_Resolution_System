@request.restful()
def complaint():
	response.view = 'generic.json'
	def POST(complaint_id):
		return dict(data = db(db.complaint_status.complaint_id_==complaint_id).select())
	def GET(complaint_id):
		return dict(data = db(db.complaint_status.complaint_id_==complaint_id).select())
	return locals()

@request.restful()
def comment():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		return db[db.status_comments].validate_and_insert(**follow_input)
	def GET(*tmp_args,**follow_input):
		return db[db.status_comments].validate_and_insert(**follow_input)
	return locals()


