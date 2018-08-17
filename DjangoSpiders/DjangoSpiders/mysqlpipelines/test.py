
class info(object):

	@classmethod
	def sayclassmethod(cls):
		print 'say '
	@classmethod
	def saymethod(cls):
		cls.sayclassmethod()
		print 'ddd'
		
info.saymethod()