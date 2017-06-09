import boto3

class MyDynamo(object):

	"""docstring for MyDynamo"""
	def __init__(self, arg):
		super(MyDynamo, self).__init__()
		self.arg = arg

	def put(self, tablename, row):
		_get_table(tablename).put_item(row)


	def get(self, tablename, key):
		_get_table(tablename).get_item(key)

	def update(self):
		pass 

	def _get_table(tablename):
		dynamo_db = boto3.resource('dynamodb')
		return dynamo_db.Table(tablename)

	def scan_table(tablename, attribute=None, value=None):
		if not attribute:
			_get_table(tablename).scan()
		else:
			_get_table()
