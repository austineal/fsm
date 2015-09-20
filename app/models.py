from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from markdown import markdown
import bleach
from . import db, login_manager


class Permission:
    ADD_USER = 0x01


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': (0x00, True),
            'Administrator': (Permission.ADD_USER, False),
            'Superuser': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADD_USER)

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
    medical_received = db.Column(db.Date)
    medical_expires = db.Column(db.Date)
    student_certificate_received = db.Column(db.Date)
    student_certificate_expires = db.Column(db.Date)
    tsa_eligibility_doc_id = db.Column(db.Integer, db.ForeignKey('tsa_docs.id'))
    tsa_eligibility_doc_number = db.Column(db.String(128))
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


class TSAEligibilityDoc(db.Model):
    __tablename__ = 'tsa_docs'
    id = db.Column(db.Integer, primary_key=True)
    doc_name = db.Column(db.String(128))
    students = db.relationship('Student', backref='tsa_eligibility_doc')
    instructors = db.relationship('Instructor', backref='tsa_eligibility_doc')


class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(64))
    tsa_eligibility_doc_id = db.Column(db.Integer, db.ForeignKey('tsa_docs.id'))
    tsa_eligibility_doc_number = db.Column(db.String(128))
    medical_received = db.Column(db.Date)
    medical_expires = db.Column(db.Date)
    flight_review_received = db.Column(db.Date)
    flight_review_expires = db.Column(db.Date)
    bfr_received = db.Column(db.Date)
    bfr_expires = db.Column(db.Date)
    ipc_received = db.Column(db.Date)
    ipc_expires = db.Column(db.Date)
    checkout_141 = db.Column(db.Boolean)
    checkout_141_date = db.Column(db.Date)
    night_currency_start_date = db.Column(db.Date)
    night_currency_end_date = db.Column(db.Date)
    me_currency_start_date = db.Column(db.Date)
    me_currency_end_date = db.Column(db.Date)
    tailwheel_currency_start_date = db.Column(db.Date)
    tailwheel_currency_end_date = db.Column(db.Date)
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
    objectives = db.Column(db.String(32000))
    objectives_html = db.Column(db.String(64000))
    completion_standards = db.Column(db.String(32000))
    completion_standards_html = db.Column(db.String(64000))
    flights = db.relationship('Flight', backref='flight_lesson')

    @staticmethod
    def on_changed_objectives(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b' 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong',
                        'ul', 'h1', 'h2', 'h3', 'p']
        target.objectives_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))

    @staticmethod
    def on_changed_completion_standards(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b' 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong',
                        'ul', 'h1', 'h2', 'h3', 'p']
        target.completion_standards_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True
        ))


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

    # these are calculated from the raw values above
    student_solo_time = db.Column(db.Float)
    student_pic_time = db.Column(db.Float)

    def calculate_log_time(self):
        self.student_pic_time = self.se_pic + self.me_pic
        self.student_solo_time = self.se_solo


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

db.event.listen(FlightLesson.objectives, 'set', FlightLesson.on_changed_objectives)
db.event.listen(FlightLesson.completion_standards, 'set', FlightLesson.on_changed_completion_standards)