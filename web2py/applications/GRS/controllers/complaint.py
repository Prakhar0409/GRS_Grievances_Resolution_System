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
		return dict(data = db(db.complaint_domain.complaint_level_id=level_id).select())
    	return locals()

@request.restful()
def status():
	response.view = 'generic.json'
	def GET(complaint_id):
		return dict(data = db(db.complaint_status.complaint_id=complaint_id).select())
    	return locals()

@request.restful()
def create():
	response.view = 'generic.json'
	def POST(*tmp_args,**complaint_input):
#		return dict(data = db[db.complaints].insert(complaint_level_id=complaint_input[0], complaint_domain_id=complaint_input[1], complaint_date=complaint_input[2], complaint_title=complaint_input[3], complaint_details=complaint_input[4], date_work_taken_on=complaint_input[5], complaint_level_id=complaint_input[6], status_id=complaint_input[7], posted_by=complaint_input[8], date_posted=complaint_input[9], upvotes_count=complaint_input[10], date_resolved=complaint_input[11], photo_id=complaint_input[12], redirected_by_user_id=complaint_input[12], redirected_to_user_id=complaint_input[13]))
		return dict(data=True)
	return locals()


