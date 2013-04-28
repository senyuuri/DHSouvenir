from main import db
from hashlib import md5

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	uid = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(30), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	orders = db.relationship('Uorder', backref='user',lazy='dynamic')

	def __repr__(self):
		return ('<User %r>' % (self.username))

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.uid)

	def avatar(self, size):
		return ('http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size))

class Store(db.Model):
	pid = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), index = True)
	price = db.Column(db.Float)
	number = db.Column(db.Integer)

	def __repr__(self):
		return '<Product %r>' % (self.name)

	'''
	def dbinit():
    	storelist = [
                (0,"A4 lecture pad", 2.60, 100),
                (1,"7-colour sticky note with pen", 4.20, 100),
                (2,"A5 ring book", 4.80, 100),
                (3,"A5 note book with zip bag", 4.60, 100) ,
                (4,"2B pencil", 0.90, 100),
                (5,"Stainless steel tumbler", 12.90, 100),
                (6,"A4 clear holder", 4.40, 100),
                (7,"A4 vanguard file", 1.00, 100),
                (8,"Name card holder", 10.90, 100),
                (9,"Umbrella", 9.00, 100),
                (10,"School badge (Junior High)", 1.30, 100),
                (11,"School badge (Senior High)", 1.80, 100),
                (12,"Dunman dolls (pair))", 45.00, 100),
    	]
    	for s in storelist:
    	    store = Store(name=s[1],price=s[2],number=s[3])
    	    db.session.add(store)
    	db.session.commit()
    	return 'success!'
    	'''

class Uorder(db.Model):
	oid = db.Column(db.Integer, primary_key = True)
	uid = db.Column(db.Integer,db.ForeignKey('user.uid'))
	pid = db.Column(db.Integer,db.ForeignKey('store.pid'))
	num = db.Column(db.Integer)
		
