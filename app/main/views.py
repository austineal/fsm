from datetime import datetime, date
from flask import render_template, flash, redirect, url_for, request, current_app
from flask.ext.login import login_required
from .forms import AddStudentForm, AddInstructorForm, AddFlightLessonForm, AddTestTypeForm, AddFlightForm, AddTestForm, PassRateForm, MonthlyStudentEnrollmentForm
from ..models import Student, Instructor, FlightLesson, TestType, Flight, Test
from .. import db
from . import main


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/add/student', methods=['GET', 'POST'])
@login_required
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
                          active=form.active.data,
                          student_type_id=form.student_type.data,
                          instructor_id=form.instructor.data)
        db.session.add(student)
        db.session.commit()
        flash('New student added.')
        return redirect(url_for('.index'))
    return render_template('add_student.html', form=form)


@main.route('/view/students')
@login_required
def view_students():
    page = request.args.get('page', 1, type=int)
    pagination = Student.query.order_by(Student.last_name, Student.first_name).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    students = pagination.items
    return render_template('view_students.html', students=students, pagination=pagination)


@main.route('/view/students/<student_id>', methods=['GET', 'POST'])
@login_required
def view_student(student_id):
    form = AddStudentForm()
    student = Student.query.filter_by(id=student_id).first()
    if form.validate_on_submit():
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.address = form.address.data
        student.city = form.city.data
        student.state_id = form.state.data
        student.phone_number = form.phone_number.data
        student.email_address = form.email_address.data
        student.enrollment_start_date = form.enrollment_start_date.data
        student.enrollment_end_date = form.enrollment_end_date.data
        student.active = form.active.data
        student.student_type_id = form.student_type.data
        student.instructor_id = form.instructor.data
        db.session.add(student)
        db.session.commit()
        flash('Student updated.')
        return redirect(url_for('.view_students'))
    form.first_name.data = student.first_name
    form.last_name.data = student.last_name
    form.address.data = student.address
    form.city.data = student.city
    form.state.data = student.state_id
    form.phone_number.data = student.phone_number
    form.email_address.data = student.email_address
    form.enrollment_start_date.data = student.enrollment_start_date
    form.enrollment_end_date.data = student.enrollment_end_date
    form.active.data = student.active
    form.student_type.data = student.student_type_id
    form.instructor.data = student.instructor_id
    return render_template('edit_student.html', form=form)


@main.route('/add/instructor', methods=['GET', 'POST'])
@login_required
def add_instructor():
    form = AddInstructorForm()
    if form.validate_on_submit():
        instructor = Instructor(first_name=form.first_name.data,
                                last_name=form.last_name.data)
        db.session.add(instructor)
        db.session.commit()
        flash('New instructor added.')
        return redirect(url_for('.index'))
    return render_template('add_instructor.html', form=form)


@main.route('/view/instructors')
@login_required
def view_instructors():
    page = request.args.get('page', 1, type=int)
    pagination = Instructor.query.order_by(Instructor.last_name, Instructor.first_name).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    instructors = pagination.items
    return render_template('view_instructors.html', instructors=instructors, pagination=pagination)


@main.route('/view/instructors/<instructor_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def add_flight_lesson():
    form = AddFlightLessonForm()
    if form.validate_on_submit():
        lesson = FlightLesson(number=form.number.data,
                              name=form.name.data)
        db.session.add(lesson)
        db.session.commit()
        flash('New flight lesson added.')
        return redirect(url_for('.index'))
    return render_template('add_flight_lesson.html', form=form)


@main.route('/view/lessons')
@login_required
def view_flight_lessons():
    page = request.args.get('page', 1, type=int)
    pagination = FlightLesson.query.order_by(FlightLesson.number).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    lessons = pagination.items
    return render_template('view_flight_lessons.html', lessons=lessons, pagination=pagination)


@main.route('/view/lessons/<lesson_id>', methods=['GET', 'POST'])
@login_required
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


@main.route('/add/testtype', methods=['GET', 'POST'])
@login_required
def add_testtype():
    form = AddTestTypeForm()
    if form.validate_on_submit():
        testtype = TestType(name=form.name.data, scored=form.scored.data)
        db.session.add(testtype)
        db.session.commit()
        flash('New test type added.')
        return redirect(url_for('.index'))
    return render_template('admin/add_testtype.html', form=form)


@main.route('/view/testtypes')
@login_required
def view_testtypes():
    page = request.args.get('page', 1, type=int)
    pagination = TestType.query.order_by(TestType.id).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    testtypes = pagination.items
    return render_template('admin/view_testtypes.html', testtypes=testtypes, pagination=pagination)


@main.route('/view/testtype/<testtype_id>', methods=['GET', 'POST'])
@login_required
def view_testtype(testtype_id):
    form = AddTestTypeForm()
    testtype = TestType.query.filter_by(id=testtype_id).first()
    if form.validate_on_submit():
        testtype.name = form.name.data
        testtype.scored = form.scored.data
        db.session.add(testtype)
        db.session.commit()
        flash('Test type updated.')
        return redirect(url_for('.view_testtypes'))
    form.name.data = testtype.name
    form.scored.data = testtype.scored
    return render_template('admin/edit_testtype.html', form=form)


@main.route('/add/flight', methods=['GET', 'POST'])
@login_required
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
        db.session.commit()
        flash('New flight added.')
        return redirect(url_for('.index'))
    return render_template('add_flight.html', form=form)


@main.route('/view/flights')
@login_required
def view_flights():
    page = request.args.get('page', 1, type=int)
    pagination = Flight.query.order_by(Flight.date).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    flights = pagination.items
    return render_template('view_flights.html', flights=flights, pagination=pagination)


@main.route('/view/flight/<flight_id>', methods=['GET', 'POST'])
@login_required
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
        db.session.commit()
        flash('Flight updated.')
        return redirect(url_for('.view_flights'))
    form.date.data = flight.date
    form.student.data = flight.student_id
    form.instructor.data = flight.instructor_id
    form.flight_time.data = flight.flight_time
    form.flight_lesson.data = flight.flight_lesson_id
    return render_template('edit_flight.html', form=form)


@main.route('/add/test', methods=['GET', 'POST'])
@login_required
def add_test():
    form = AddTestForm()
    if form.validate_on_submit():
        test = Test()
        test.date = form.date.data
        test.student_id = form.student.data
        test.instructor_id = form.instructor.data
        test.test_type_id = form.test_type.data
        if form.success.raw_data[0] == 'False':
            test.success = False
        else:
            test.success = True
        test.score = form.score.data
        db.session.add(test)
        db.session.commit()
        flash('New test added.')
        return redirect(url_for('.index'))
    return render_template('add_test.html', form=form)


@main.route('/view/tests')
@login_required
def view_tests():
    page = request.args.get('page', 1, type=int)
    pagination = Test.query.order_by(Test.date).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    tests = pagination.items
    return render_template('view_tests.html', tests=tests, pagination=pagination)


@main.route('/view/test/<test_id>', methods=['GET', 'POST'])
@login_required
def view_test(test_id):
    form = AddTestForm()
    test = Test.query.filter_by(id=test_id).first()
    if form.validate_on_submit():
        test.date = form.date.data
        test.student_id = form.student.data
        test.instructor_id = form.instructor.data
        test.test_type_id = form.test_type.data
        test.score = form.score.data
        if form.success.raw_data[0] == 'False':
            test.success = False
        else:
            test.success = True
        db.session.add(test)
        db.session.commit()
        flash('Test updated.')
        return redirect(url_for('.view_tests'))
    form.date.data = test.date
    form.student.data = test.student_id
    form.instructor.data = test.instructor_id
    form.test_type.data = test.test_type_id
    form.success.data = test.success
    form.score.data = test.score
    return render_template('edit_test.html', form=form)


@main.route('/report/enrollment', methods=['GET', 'POST'])
@login_required
def monthly_student_enrollment_report():
    form = MonthlyStudentEnrollmentForm()
    if form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
        student_type_id = form.student_type.data
        instructor_id = form.instructor.data
        return redirect(url_for('.monthly_student_enrollment_report', from_date=from_date, to_date=to_date,
                                student_type_id=student_type_id, instructor_id=instructor_id))
    if 'from_date' in request.values and 'to_date' in request.values:
        from_date = datetime.strptime(request.values.get('from_date'), '%Y-%m-%d').date()
        to_date = datetime.strptime(request.values.get('to_date'), '%Y-%m-%d').date()
        student_type_id = int(request.values.get('student_type_id'))
        instructor_id = int(request.values.get('instructor_id'))
        form.from_date.data = from_date
        form.to_date.data = to_date
        form.student_type.data = student_type_id
        form.instructor.data = instructor_id

        students_query = Student.query.order_by(Student.last_name, Student.first_name)
        if student_type_id:
            students_query = students_query.filter_by(student_type_id=student_type_id)
        if instructor_id:
            students_query = students_query.filter_by(instructor_id=instructor_id)

        students = []
        today = date.today()
        for student in students_query.all():
            enrollment_start = student.enrollment_start_date
            if not enrollment_start:
                enrollment_start = today
            enrollment_end = student.enrollment_end_date
            if not enrollment_end:
                enrollment_end = today
            latest_start = max(from_date, enrollment_start)
            earliest_end = min(to_date, enrollment_end)
            overlap = (earliest_end - latest_start).days + 1
            print student.first_name, student.last_name
            print enrollment_start, enrollment_end
            print overlap
            if overlap > 0:
                students.append(student)

        num_students = len(students)

        return render_template('reports/monthly_student_enrollment.html', form=form, from_date=from_date,
                               to_date=to_date, students=students, num_students=num_students)
    else:
        return render_template('reports/monthly_student_enrollment.html', form=form)


@main.route('/report/pass_rate', methods=['GET', 'POST'])
@login_required
def pass_rate_report():
    form = PassRateForm()
    if form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
        return redirect(url_for('.pass_rate_report', from_date=from_date, to_date=to_date))
    from_date = request.values.get('from_date')
    to_date = request.values.get('to_date')
    form.from_date.data = from_date
    form.to_date.data = to_date
    return render_template('pass_rate_report.html', form=form, from_date=from_date, to_date=to_date)