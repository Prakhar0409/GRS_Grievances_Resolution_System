@request.restful()
def user():
	response.view = 'generic.json'
	def GET(image_id):
		response.view = 'generic.json'
		image = db.pictures(id=image_id)
		return dict(image=image)
	return locals()
