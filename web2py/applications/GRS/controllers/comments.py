@request.restful()
def complaint():
	response.view = 'generic.json'
	def GET(complaint_id):
		return dict(data = db(db.comments.complaint_id==complaint_id).select())
	return locals()

@request.restful()
def status():
	response.view = 'generic.json'
	def GET(status_id):
		return dict(data = db(db.status_comments.status_id==status_id).select())
	return locals()


