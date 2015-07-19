from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class StudentType(db.Model):
    __tablename__ = 'studenttypes'
    id = db.Column(db.Integer, primary_key=True)
    student_type = db.Column(db.String(8))
    students = db.relationship('Student', backref='student_type')


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(64))
    address = db.Column(db.String(256))
    city = db.Column(db.String(64))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    zip_code = db.Column(db.String(11))
    phone_number = db.Column(db.String(16))
    email_address = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    student_type_id = db.Column(db.Integer, db.ForeignKey('studenttypes.id'))
    enrollment_start_date = db.Column(db.Date)
    enrollment_end_date = db.Column(db.Date)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    flights = db.relationship('Flight', backref='student')
    tests = db.relationship('Test', backref='student')

    @staticmethod
    def generate_fake(count=30):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            s = Student(first_name=forgery_py.name.first_name(),
                        last_name=forgery_py.name.last_name(),
                        address=forgery_py.address.street_address(),
                        city=forgery_py.address.city(),
                        state=State.query.filter_by(state='OR').first(),
                        zip_code=forgery_py.address.zip_code(),
                        phone_number='555-555-5555',
                        email_address=forgery_py.internet.email_address(),
                        active=True)
            db.session.add(s)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(64))
    flights = db.relationship('Flight', backref='instructor')
    tests = db.relationship('Test', backref='instructor')
    students = db.relationship('Student', backref='instructor')

    @staticmethod
    def generate_fake(count=30):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            ins = Instructor(first_name=forgery_py.name.first_name(),
                             last_name=forgery_py.name.last_name())
            db.session.add(ins)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(64))
    students = db.relationship('Student', backref='state')


class FlightLesson(db.Model):
    __tablename__ = 'flight_lessons'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(128))
    flights = db.relationship('Flight', backref='flight_lesson')


class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    flight_time = db.Column(db.Float)
    ground_time = db.Column(db.Float)
    flight_lesson_id = db.Column(db.Integer, db.ForeignKey('flight_lessons.id'))
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircraft.id'))
    se_dual = db.Column(db.Float)
    se_solo = db.Column(db.Float)
    se_pic = db.Column(db.Float)
    me_dual = db.Column(db.Float)
    me_pic = db.Column(db.Float)
    xc_pic_solo = db.Column(db.Float)
    xc_dual = db.Column(db.Float)
    night_dual = db.Column(db.Float)
    night_dual_xc = db.Column(db.Float)
    night_pic_solo = db.Column(db.Float)
    se_complex = db.Column(db.Float)
    instrument_hood = db.Column(db.Float)
    instrument_actual = db.Column(db.Float)
    ftd = db.Column(db.Float)
    pcatd = db.Column(db.Float)
    ils = db.Column(db.Integer)
    loc = db.Column(db.Integer)
    vor = db.Column(db.Integer)
    rnav_gps = db.Column(db.Integer)
    ndb = db.Column(db.Integer)
    landings_day = db.Column(db.Integer)
    landings_night = db.Column(db.Integer)


class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    success = db.Column(db.Boolean)
    test_type_id = db.Column(db.Integer, db.ForeignKey('testtypes.id'))
    score = db.Column(db.Float)


class TestType(db.Model):
    __tablename__ = 'testtypes'
    id = db.Column(db.Integer, primary_key=True)
    test_type = db.Column(db.String(32))
    name = db.Column(db.String(32))
    scored = db.Column(db.Boolean)
    tests = db.relationship('Test', backref='test_type')

    def __repr__(self):
        return '<TestType name=%r, scored=%r>' % (self.name, self.scored)


class Aircraft(db.Model):
    __tablename__ = 'aircraft'
    id = db.Column(db.Integer, primary_key=True)
    tail_number = db.Column(db.String(10))
    flights = db.relationship('Flight', backref='aircraft')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
