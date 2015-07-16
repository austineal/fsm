from flask import render_template, flash, redirect, url_for, request, current_app
from .forms import AddStudentForm, AddInstructorForm, AddFlightLessonForm, AddSkillForm, AddFlightForm, AddCheckrideForm, PassRateForm
from ..models import Student, Instructor, FlightLesson, Skill, Flight, Checkride
from .. import db
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/add/student', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        student = Student(first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          address=form.address.data,
                          city=form.city.data,
                          state_id=form.state.data,
                          phone_number=form.phone_number.data,
                          email_address=form.email_address.data,
                          active=form.active.data)
        db.session.add(student)
        flash('New student added.')
        return redirect(url_for('.index'))
    return render_template('add_student.html', form=form)


@main.route('/view/students')
def view_students():
    page = request.args.get('page', 1, type=int)
    pagination = Student.query.order_by(Student.last_name, Student.first_name).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    students = pagination.items
    return render_template('view_students.html', students=students, pagination=pagination)


@main.route('/view/students/<student_id>', methods=['GET', 'POST'])
def view_student(student_id):
    form = AddStudentForm()
    student = Student.query.filter_by(id=student_id).first()
    form.first_name.data = student.first_name
    form.last_name.data = student.last_name
    form.address.data = student.address
    form.city.data = student.city
    form.state.data = student.state_id
    form.phone_number.data = student.phone_number
    form.email_address.data = student.email_address
    form.active.data = student.active
    if form.validate_on_submit():
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.address = form.address.data
        student.city = form.city.data
        student.state_id = form.state.data
        student.phone_number = form.phone_number.data
        student.email_address = form.email_address.data
        student.active = form.active.data
        db.session.add(student)
        db.session.commit()
        flash('Student updated.')
        return redirect(url_for('.view_students'))
    return render_template('edit_student.html', form=form)


@main.route('/add/instructor', methods=['GET', 'POST'])
def add_instructor():
    form = AddInstructorForm()
    if form.validate_on_submit():
        instructor = Instructor(first_name=form.first_name.data,
                                last_name=form.last_name.data)
        db.session.add(instructor)
        flash('New instructor added.')
        return redirect(url_for('.index'))
    return render_template('add_instructor.html', form=form)


@main.route('/view/instructors')
def view_instructors():
    page = request.args.get('page', 1, type=int)
    pagination = Instructor.query.order_by(Instructor.last_name, Instructor.first_name).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    instructors = pagination.items
    return render_template('view_instructors.html', instructors=instructors, pagination=pagination)


@main.route('/view/instructors/<instructor_id>', methods=['GET', 'POST'])
def view_instructor(instructor_id):
    form = AddInstructorForm()
    instructor = Instructor.query.filter_by(id=instructor_id).first()
    if form.validate_on_submit():
        instructor.first_name = form.first_name.data
        instructor.last_name = form.last_name.data
        db.session.add(instructor)
        db.session.commit()
        flash('Instructor updated.')
        return redirect(url_for('.view_instructors'))
    form.first_name.data = instructor.first_name
    form.last_name.data = instructor.last_name
    return render_template('edit_instructor.html', form=form)


@main.route('/add/lesson', methods=['GET', 'POST'])
def add_flight_lesson():
    form = AddFlightLessonForm()
    if form.validate_on_submit():
        lesson = FlightLesson(number=form.number.data,
                              name=form.name.data)
        db.session.add(lesson)
        flash('New flight lesson added.')
        return redirect(url_for('.index'))
    return render_template('add_flight_lesson.html', form=form)


@main.route('/view/lessons')
def view_flight_lessons():
    page = request.args.get('page', 1, type=int)
    pagination = FlightLesson.query.order_by(FlightLesson.number).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    lessons = pagination.items
    return render_template('view_flight_lessons.html', lessons=lessons, pagination=pagination)


@main.route('/view/lessons/<lesson_id>', methods=['GET', 'POST'])
def view_flight_lesson(lesson_id):
    form = AddFlightLessonForm()
    lesson = FlightLesson.query.filter_by(id=lesson_id).first()
    if form.validate_on_submit():
        lesson.number = form.number.data
        lesson.name = form.name.data
        db.session.add(lesson)
        db.session.commit()
        flash('Flight lesson updated.')
        return redirect(url_for('.view_flight_lessons'))
    form.number.data = lesson.number
    form.name.data = lesson.name
    return render_template('edit_flight_lesson.html', form=form)


@main.route('/add/skill', methods=['GET', 'POST'])
def add_skill():
    form = AddSkillForm()
    if form.validate_on_submit():
        skill = Skill(name=form.name.data)
        db.session.add(skill)
        flash('New skill added.')
        return redirect(url_for('.index'))
    return render_template('add_skill.html', form=form)


@main.route('/view/skills')
def view_skills():
    page = request.args.get('page', 1, type=int)
    pagination = Skill.query.order_by(Skill.id).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    skills = pagination.items
    return render_template('view_skills.html', skills=skills, pagination=pagination)


@main.route('/view/skills/<skill_id>', methods=['GET', 'POST'])
def view_skill(skill_id):
    form = AddSkillForm()
    skill = Skill.query.filter_by(id=skill_id).first()
    if form.validate_on_submit():
        skill.name = form.name.data
        db.session.add(skill)
        db.session.commit()
        flash('Skill updated.')
        return redirect(url_for('.view_skills'))
    form.name.data = skill.name
    return render_template('edit_skill.html', form=form)


@main.route('/add/flight', methods=['GET', 'POST'])
def add_flight():
    form = AddFlightForm()
    if form.validate_on_submit():
        flight = Flight()
        flight.date = form.date.data
        flight.student_id = form.student.data
        flight.instructor_id = form.instructor.data
        flight.flight_time = form.flight_time.data
        flight.flight_lesson_id = form.flight_lesson.data
        db.session.add(flight)
        flash('New flight added.')
        return redirect(url_for('.index'))
    return render_template('add_flight.html', form=form)


@main.route('/view/flights')
def view_flights():
    page = request.args.get('page', 1, type=int)
    pagination = Flight.query.order_by(Flight.date).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    flights = pagination.items
    return render_template('view_flights.html', flights=flights, pagination=pagination)


@main.route('/view/flight/<flight_id>', methods=['GET', 'POST'])
def view_flight(flight_id):
    form = AddFlightForm()
    flight = Flight.query.filter_by(id=flight_id).first()
    if form.validate_on_submit():
        flight.date = form.date.data
        flight.student_id = form.student.data
        flight.instructor_id = form.instructor.data
        flight.flight_time = form.flight_time.data
        flight.flight_lesson_id = form.flight_lesson.data
        db.session.add(flight)
        flash('Flight updated.')
        return redirect(url_for('.view_flights'))
    form.date.data = flight.date
    form.student.data = flight.student_id
    form.instructor.data = flight.instructor_id
    form.flight_time.data = flight.flight_time
    form.flight_lesson.data = flight.flight_lesson_id
    return render_template('edit_flight.html', form=form)


@main.route('/add/checkride', methods=['GET', 'POST'])
def add_checkride():
    form = AddCheckrideForm()
    if form.validate_on_submit():
        checkride = Checkride()
        checkride.date = form.date.data
        checkride.student_id = form.student.data
        checkride.instructor_id = form.instructor.data
        checkride.success = form.success.data
        db.session.add(checkride)
        flash('New checkride added.')
        return redirect(url_for('.index'))
    return render_template('add_checkride.html', form=form)


@main.route('/view/checkrides')
def view_checkrides():
    page = request.args.get('page', 1, type=int)
    pagination = Checkride.query.order_by(Checkride.date).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    checkrides = pagination.items
    return render_template('view_checkrides.html', checkrides=checkrides, pagination=pagination)


@main.route('/view/checkride/<checkride_id>', methods=['GET', 'POST'])
def view_checkride(checkride_id):
    form = AddCheckrideForm()
    checkride = Checkride.query.filter_by(id=checkride_id).first()
    if form.validate_on_submit():
        checkride.date = form.date.data
        checkride.student_id = form.student.data
        checkride.instructor_id = form.instructor.data
        checkride.success = form.success.data
        db.session.add(checkride)
        flash('Checkride updated.')
        return redirect(url_for('.view_checkrides'))
    form.date.data = checkride.date
    form.student.data = checkride.student_id
    form.instructor.data = checkride.instructor_id
    form.success.data = checkride.success
    return render_template('edit_checkride.html', form=form)


@main.route('/report/pass_rate', methods=['GET', 'POST'])
def pass_rate_report():
    form = PassRateForm()
    if form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
        return redirect(url_for('.pass_rate_report', from_date=from_date, to_date=to_date))
    print request.values
    from_date = request.values.get('from_date')
    to_date = request.values.get('to_date')
    form.from_date.data = from_date
    form.to_date.data = to_date
    return render_template('pass_rate_report.html', form=form, from_date=from_date, to_date=to_date)