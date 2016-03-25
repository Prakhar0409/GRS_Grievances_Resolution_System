@request.restful()
def validation():
	response.view = 'generic.json'
	def GET():			#######TO DO
		return dict(data = True)
	return locals()



