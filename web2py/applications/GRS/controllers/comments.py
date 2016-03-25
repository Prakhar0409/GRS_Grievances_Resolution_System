@request.restful()
def details():
	response.view = 'generic.json'
	def GET(complaint_id):
		return dict(data = db.comments(complaint_id=complaint_id))
	return locals()

@request.restful()
def status():
	response.view = 'generic.json'
	def GET(status_id):
		return dict(data = db.status_comments(status_id=status_id))
	return locals()


