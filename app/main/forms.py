from datetime import date
from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, SelectField, BooleanField, IntegerField, FloatField, RadioField, \
    TextAreaField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Optional, Length, Email, Regexp, EqualTo, ValidationError
from ..models import State, Student, Instructor, FlightLesson, StudentType, TestType, Aircraft, TSAEligibilityDoc, User


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class AddStudentForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    address = StringField('Address')
    city = StringField('City')
    state = SelectField('State', coerce=int)
    zip = StringField('ZIP Code')
    phone_number = StringField('Phone Number')
    email_address = StringField('Email Address')
    enrollment_start_date = DateField('Enrollment Start Date')
    enrollment_end_date = DateField('Enrollment End Date', validators=[Optional()])
    active = BooleanField('Active')
    student_type = SelectField('Student Type', coerce=int)
    instructor = SelectField('Instructor', coerce=int)
    medical_received = DateField('Medical Received', validators=[Optional()])
    medical_expires = DateField('Medical Expires', validators=[Optional()])
    student_cert_received = DateField('Student Certificate Received', validators=[Optional()])
    student_cert_expires = DateField('Student Certificate Expires', validators=[Optional()])
    tsa_proof = SelectField('Proof of TSA Eligibility', coerce=int)
    add_student = SubmitField('Save Student')

    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.state.choices = [(state.id, state.state)
                              for state in State.query.order_by(State.state).all()]
        self.student_type.choices = [(student_type.id, student_type.student_type)
                                     for student_type in StudentType.query.order_by(StudentType.student_type).all()]
        self.instructor.choices = [(instructor.id, '%s, %s' % (instructor.last_name, instructor.first_name))
                                   for instructor
                                   in Instructor.query.order_by(Instructor.last_name, Instructor.first_name).all()]
        self.tsa_proof.choices = [(doc.id, doc.doc_name)
                                  for doc in TSAEligibilityDoc.query.order_by(TSAEligibilityDoc.doc_name).all()]


class AddInstructorForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    tsa_proof = SelectField('Proof of TSA Eligibility', coerce=int)
    medical_received = DateField('Medical Received', validators=[Optional()])
    medical_expires = DateField('Medical Expires', validators=[Optional()])
    flight_review_received = DateField('Flight Review Received', validators=[Optional()])
    flight_review_expires = DateField('Flight Review Expires', validators=[Optional()])
    bfr_received = DateField('BFR Received', validators=[Optional()])
    bfr_expires = DateField('BFR Expires', validators=[Optional()])
    ipc_received = DateField('IPC Received', validators=[Optional()])
    ipc_expires = DateField('IPC Expires', validators=[Optional()])
    checkout_141 = BooleanField('141 Checkout', validators=[Optional()])
    checkout_141_date = DateField('141 Checkout Date', validators=[Optional()])
    night_currency_start_date = DateField('Night Currency Start', validators=[Optional()])
    night_currency_end_date = DateField('Night Currency End', validators=[Optional()])
    me_currency_start_date = DateField('ME Currency Start', validators=[Optional()])
    me_currency_end_date = DateField('ME Currency End', validators=[Optional()])
    tailwheel_currency_start_date = DateField('Tail Wheel Currency Start', validators=[Optional()])
    tailwheel_currency_end_date = DateField('Tail Wheel Currency End', validators=[Optional()])
    add_instructor = SubmitField('Save Instructor')

    def __init__(self, *args, **kwargs):
        super(AddInstructorForm, self).__init__(*args, **kwargs)
        self.tsa_proof.choices = [(doc.id, doc.doc_name)
                                  for doc in TSAEligibilityDoc.query.order_by(TSAEligibilityDoc.doc_name).all()]



class AddAircraftForm(Form):
    tail_number = StringField('Tail Number', validators=[Required()])
    add_aircraft = SubmitField('Save Aircraft')


class AddFlightLessonForm(Form):
    number = IntegerField('Lesson Number')
    name = StringField('Lesson Name')
    objectives = PageDownField('Objectives', validators=[Optional(), Length(max=32000)])
    completion_standards = PageDownField('Completion Standards', validators=[Optional(), Length(max=32000)])
    add_lesson = SubmitField('Save Lesson')


class AddFlightForm(Form):
    date = DateField('Date', validators=[Required()])
    student = SelectField('Student', coerce=int)
    instructor = SelectField('Instructor', coerce=int)
    flight_lesson = SelectField('Lesson', coerce=int)
    aircraft = SelectField('Aircraft', coerce=int)
    ground_time = FloatField('Pre/Post Ground', default=0)
    flight_time = FloatField('Flight Time', default=0)
    se_dual = FloatField('SE Dual', default=0)
    se_solo = FloatField('SE Solo', default=0)
    se_pic = FloatField('SE PIC', default=0)
    me_dual = FloatField('ME Dual', default=0)
    me_pic = FloatField('ME PIC', default=0)
    xc_pic_solo = FloatField('XC PIC Solo', default=0)
    xc_dual = FloatField('XC Dual', default=0)
    night_dual = FloatField('Night Dual', default=0)
    night_dual_xc = FloatField('Night Dual XC', default=0)
    night_pic_solo = FloatField('Night PIC Solo', default=0)
    se_complex = FloatField('SE Complex', default=0)
    instrument_hood = FloatField('Instrument Hood', default=0)
    instrument_actual = FloatField('Instrument Actual', default=0)
    ftd = FloatField('FTD', default=0)
    pcatd = FloatField('PCATD', default=0)
    ils = IntegerField('ILS', default=0)
    loc = IntegerField('LOC', default=0)
    vor = IntegerField('VOR', default=0)
    rnav_gps = IntegerField('RNAV/GPS', default=0)
    ndb = IntegerField('NDB', default=0)
    landings_day = IntegerField('Landings Day', default=0)
    landings_night = IntegerField('Landings Night', default=0)
    complete = RadioField(choices=[(True, 'Lesson completed'), (False, 'Lesson not completed')], default=True, coerce=bool)
    completed_objectives = TextAreaField('Objectives completed this lesson')

    add_flight = SubmitField('Save Flight')

    def __init__(self, *args, **kwargs):
        super(AddFlightForm, self).__init__(*args, **kwargs)
        self.student.choices = [(student.id, '%s, %s' % (student.last_name, student.first_name))
                                for student in Student.query.order_by(Student.last_name, Student.first_name).all()]
        self.instructor.choices = [(instructor.id, '%s, %s' % (instructor.last_name, instructor.first_name))
                                   for instructor
                                   in Instructor.query.order_by(Instructor.last_name, Instructor.first_name).all()]
        self.flight_lesson.choices = [(lesson.id, '%d: %s' % (lesson.number, lesson.name))
                                      for lesson in FlightLesson.query.order_by(FlightLesson.number).all()]
        self.aircraft.choices = [(plane.id, plane.tail_number) for plane
                                 in Aircraft.query.order_by(Aircraft.tail_number).all()]

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if self.complete.raw_data[0] == 'False':
            if not self.completed_objectives.data:
                self.completed_objectives.errors.append('Please specify which objectives were completed in this lesson.')
                return False

        return True


class AddTestTypeForm(Form):
    name = StringField('Test Name')
    scored = BooleanField('Scored')
    add_testtype = SubmitField('Save Test Type')


class AddTestForm(Form):
    date = DateField('Date')
    student = SelectField('Student', coerce=int)
    instructor = SelectField('Instructor', coerce=int)
    test_type = SelectField('Test Type', coerce=int)
    success = RadioField(choices=[(True, 'Pass'), (False, 'Fail')], coerce=bool)
    score = FloatField('Score', validators=[Optional()])
    add_test = SubmitField('Save Test')

    def __init__(self, *args, **kwargs):
        super(AddTestForm, self).__init__(*args, **kwargs)
        self.student.choices = [(student.id, '%s, %s' % (student.last_name, student.first_name))
                                for student in Student.query.order_by(Student.last_name, Student.first_name).all()]
        self.instructor.choices = [(instructor.id, '%s, %s' % (instructor.last_name, instructor.first_name))
                                   for instructor
                                   in Instructor.query.order_by(Instructor.last_name, Instructor.first_name).all()]
        self.test_type.choices = [(test_type.id, test_type.name) for test_type in
                                  TestType.query.order_by(TestType.id).all()]


class MonthlyStudentEnrollmentForm(Form):
    today = date.today()
    from_date = DateField('From', default=date(today.year, today.month, 1), validators=[Required()])
    to_date = DateField('To', default=today, validators=[Required()])
    student_type = SelectField('Student Type', coerce=int, validators=[Optional()])
    instructor = SelectField('Instructor', coerce=int, validators=[Optional()])
    get_report = SubmitField('Generate Report')

    def __init__(self, *args, **kwargs):
        super(MonthlyStudentEnrollmentForm, self).__init__(*args, **kwargs)
        self.student_type.choices = [(0, 'All')]
        self.student_type.choices.extend([(student_type.id, student_type.student_type) for student_type in
                                          StudentType.query.order_by(StudentType.student_type).all()])
        self.instructor.choices = [(0, 'All')]
        self.instructor.choices .extend([(instructor.id, '%s, %s' % (instructor.last_name, instructor.first_name))
                                         for instructor
                                         in Instructor.query.order_by(Instructor.last_name, Instructor.first_name).all()])


class LogbookForm(Form):
    today = date.today()
    from_date = DateField('From', default=date(today.year, today.month, 1), validators=[Required()])
    to_date = DateField('To', default=today, validators=[Required()])
    student = SelectField('Student', coerce=int, validators=[Required()])
    get_report = SubmitField('Generate Report')

    def __init__(self, *args, **kwargs):
        super(LogbookForm, self).__init__(*args, **kwargs)
        self.student.choices = [(student.id, '%s, %s' % (student.last_name, student.first_name))
                                for student in Student.query.order_by(Student.last_name, Student.first_name).all()]