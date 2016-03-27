@request.restful()
def details():
	response.view = 'generic.json'
	def GET(complaint_id):
		return dict(data = db.complaints(id=complaint_id))
    	return locals()

@request.restful()
def levels():
	response.view = 'generic.json'
	def GET():
		return dict(data = db(db.complaint_levels.id>0).select())
    	return locals()

@request.restful()
def domains():
	response.view = 'generic.json'
	def GET(level_id):
		return dict(data = db(db.complaint_domain.complaint_level_id==level_id).select())
    	return locals()

@request.restful()
def bookmark():
	response.view = 'generic.json'
	def GET(complaint_id):
		data = db(db.bookmarks.complaint_id==complaint_id).select()
		if len(data)>0:
			return dict(bookmarked = True)
		else:
			return dict(bookmarked = False)
    	return locals()

@request.restful()
def status():
	response.view = 'generic.json'
	def GET(complaint_id):
		return dict(data = db(db.complaint_status.complaint_id==complaint_id).select())
    	return locals()

@request.restful()
def complaints():
	response.view = 'generic.json'
	def GET(complaint_section):
		if(complaint_section=='bookmarked'):
			return dict(data = db(db.bookmarks.complaint_id>0).select())
		elif(complaint_section=='concern'):
			return dict(data = db(db.complaints_concerning_user.complaint_id>0).select())
		elif(complaint_section=='resolve'):
			return dict(data = db(db.complaints_with_resolving_rights_to_user.complaint_id>0).select())
		elif(complaint_section=='solve'):
			return dict(data = db(db.complaints_made_to_user.complaint_id>0).select())
    	return locals()

@request.restful()
def create():
	response.view = 'generic.json'
	def POST(*tmp_args,**complaint_input):
		return db[db.complaints].validate_and_insert(**complaint_input)
	def GET(*tmp_args,**complaint_input):
		return db[db.complaints].validate_and_insert(**complaint_input)
	return locals()

@request.restful()
def vote():
	response.view = 'generic.json'
	def POST(*tmp_args,**vote_input):
		return db[db.votes].validate_and_insert(**vote_input)
	def GET(*tmp_args,**vote_input):
		return db[db.votes].validate_and_insert(**vote_input)
	return locals()

@request.restful()
def follow():
	response.view = 'generic.json'
	def POST(*tmp_args,**follow_input):
		return db[db.bookmarks].validate_and_insert(**follow_input)
	def GET(*tmp_args,**follow_input):
		return db[db.bookmarks].validate_and_insert(**follow_input)
	return locals()

@request.restful()
def status():
	response.view = 'generic.json'
	def POST(*tmp_args,**status_input):
		return db[db.complaint_status].validate_and_insert(**status_input)
	def GET(*tmp_args,**status_input):
		return db[db.complaint_status].validate_and_insert(**status_input)
	return locals()

