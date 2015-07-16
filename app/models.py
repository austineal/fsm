from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


flights_has_skills = db.Table('flights_has_skills',
                              db.Column('flight_id', db.Integer, db.ForeignKey('flights.id')),
                              db.Column('skill_id', db.Integer, db.ForeignKey('skills.id')))


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
    flights = db.relationship('Flight', backref='student')
    checkrides = db.relationship('Checkride', backref='student')

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
    checkrides = db.relationship('Checkride', backref='instructor')

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


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    flights = db.relationship('Flight',
                              secondary=flights_has_skills,
                              backref=db.backref('skills', lazy='dynamic'),
                              lazy='dynamic')


class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    flight_time = db.Column(db.Float)
    flight_lesson_id = db.Column(db.Integer, db.ForeignKey('flight_lessons.id'))


class Checkride(db.Model):
    __tablename__ = 'checkrides'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    success = db.Column(db.Boolean)

    def __repr__(self):
        return '<Checkride id=%r, date=%r, student_id=%r, instructor_id=%r, success=%r>' % (self.id, self.date,
                                                                                            self.student_id,
                                                                                            self.instructor_id,
                                                                                            self.success)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
