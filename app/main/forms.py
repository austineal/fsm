from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, BooleanField, IntegerField, FloatField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Optional
from ..models import State, Student, Instructor, Skill, FlightLesson


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
    active = BooleanField('Active')
    add_student = SubmitField('Save Student')

    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.state.choices = [(state.id, state.state)
                              for state in State.query.order_by(State.state).all()]


class AddInstructorForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    add_instructor = SubmitField('Save Instructor')


class AddFlightLessonForm(Form):
    number = IntegerField('Lesson Number')
    name = StringField('Lesson Name')
    add_lesson = SubmitField('Save Lesson')


class AddSkillForm(Form):
    name = StringField('Skill Name')
    add_skill = SubmitField('Save Skill')


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


class AddCheckrideForm(Form):
    date = DateField('Date')
    student = SelectField('Student', coerce=int)
    instructor = SelectField('Instructor', coerce=int)
    success = RadioField('Hello!', choices=[(True, 'Pass'), (False, 'Fail')], coerce=bool)
    add_checkride = SubmitField('Save Checkride')

    def __init__(self, *args, **kwargs):
        super(AddCheckrideForm, self).__init__(*args, **kwargs)
        self.student.choices = [(student.id, '%s, %s' % (student.last_name, student.first_name))
                                for student in Student.query.order_by(Student.last_name, Student.first_name).all()]
        self.instructor.choices = [(instructor.id, '%s, %s' % (instructor.last_name, instructor.first_name))
                                   for instructor
                                   in Instructor.query.order_by(Instructor.last_name, Instructor.first_name).all()]


class PassRateForm(Form):
    from_date = DateField('From')
    to_date = DateField('To')
    get_report = SubmitField('Generate Report')