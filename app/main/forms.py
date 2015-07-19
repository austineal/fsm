from datetime import date
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, BooleanField, IntegerField, FloatField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Optional
from ..models import State, Student, Instructor, FlightLesson, StudentType, TestType


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class AddStudentForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    address = StringField('Address')
    city = StringField('City')
    state = SelectField('State', coerce=int)
    phone_number = StringField('Phone Number')
    email_address = StringField('Email Address')
    enrollment_start_date = DateField('Enrollment Start Date')
    enrollment_end_date = DateField('Enrollment End Date', validators=[Optional()])
    active = BooleanField('Active')
    student_type = SelectField('Student Type', coerce=int)
    instructor = SelectField('Instructor', coerce=int)
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


class AddInstructorForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    add_instructor = SubmitField('Save Instructor')


class AddFlightLessonForm(Form):
    number = IntegerField('Lesson Number')
    name = StringField('Lesson Name')
    add_lesson = SubmitField('Save Lesson')


class AddFlightForm(Form):
    date = DateField('Date')
    student = SelectField('Student', coerce=int)
    instructor = SelectField('Instructor', coerce=int)
    flight_time = FloatField('Time this Lesson')
    flight_lesson = SelectField('Lesson', coerce=int)
    landings_day = FloatField('Landings Day', validators=[Optional()])
    landings_night = FloatField('Landings Night', validators=[Optional()])
    instrument = FloatField('Instrument', validators=[Optional()])
    night = FloatField('Night', validators=[Optional()])
    solo_cross_country = FloatField('Solo Cross Country', validators=[Optional()])
    solo_local = FloatField('Solo Local', validators=[Optional()])
    dual_cross_country = FloatField('Dual Cross Country', validators=[Optional()])
    dual_local = FloatField('Dual Local', validators=[Optional()])
    aircraft_registration = StringField('Aircraft Registration', validators=[Optional()])
    type_aircraft = StringField('Type Aircraft', validators=[Optional()])
    briefing_time = FloatField('Briefing Time', validators=[Optional()])
    flight_training_device = StringField('Flight Training Device', validators=[Optional()])
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


class PassRateForm(Form):
    from_date = DateField('From')
    to_date = DateField('To')
    get_report = SubmitField('Generate Report')


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
