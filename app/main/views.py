from __future__ import division

from datetime import datetime, date
from collections import defaultdict, namedtuple
from sqlalchemy import func
from flask import render_template, flash, redirect, url_for, request, current_app
from flask.ext.login import login_required
from .forms import AddStudentForm, AddInstructorForm, AddFlightLessonForm, AddTestTypeForm, AddFlightForm, AddTestForm, MonthlyStudentEnrollmentForm, LogbookForm, AddAircraftForm
from ..models import Student, Instructor, FlightLesson, TestType, Flight, Test, Aircraft
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
                          instructor_id=form.instructor.data,
                          medical_received=form.medical_received,
                          medical_expires=form.medical_expires)
        db.session.add(student)
        db.session.commit()
        flash('New student added.')
        return redirect(url_for('.index'))
    return render_template('add_student.html', form=form)


@main.route('/add/aircraft', methods=['GET', 'POST'])
@login_required
def add_aircraft():
    form = AddAircraftForm()
    if form.validate_on_submit():
        aircraft = Aircraft(tail_number=form.tail_number.data)
        db.session.add(aircraft)
        db.session.commit()
        flash('New aircraft added.')
        return redirect(url_for('.index'))
    return render_template('add_aircraft.html', form=form)


@main.route('/view/aircraft')
@login_required
def view_all_aircraft():
    page = request.args.get('page', 1, type=int)
    pagination = Aircraft.query.order_by(Aircraft.tail_number).paginate(
        page, per_page=current_app.config['STUDENTS_PER_PAGE'],
        error_out=False)
    aircraft = pagination.items
    return render_template('view_aircraft.html', aircraft=aircraft, pagination=pagination)


@main.route('/view/aircraft/<aircraft_id>', methods=['GET', 'POST'])
@login_required
def view_aircraft(aircraft_id):
    form = AddAircraftForm()
    aircraft = Aircraft.query.filter_by(id=aircraft_id).first()
    if form.validate_on_submit():
        aircraft.tail_number = form.tail_number.data
        db.session.add(aircraft)
        db.session.commit()
        flash('Aircraft updated.')
        return redirect(url_for('.view_all_aircraft'))
    form.tail_number.data = aircraft.tail_number
    return render_template('edit_aircraft.html', form=form)


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
        student.medical_received = form.medical_received.data
        student.medical_expires = form.medical_expires.data
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
    form.medical_received.data = student.medical_received
    form.medical_expires.data = student.medical_expires
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
def view_testtype(testtype_itd):
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


@main.route('/delete/testtype/<testtype_id>', methods=['GET', 'POST'])
@login_required
def delete_test(testtype_id):
    testtype = TestType.query.filter_by(id=testtype_id).first()
    db.session.delete(testtype)
    db.session.commit()
    flash('Test type deleted.')
    return redirect(url_for('.view_testtypes'))


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
        flight.aircraft_id = form.aircraft.data
        flight.ground_time = form.ground_time.data
        flight.se_dual = form.se_dual.data
        flight.se_solo = form.se_solo.data
        flight.se_pic = form.se_pic.data
        flight.me_dual = form.me_dual.data
        flight.me_pic = form.me_pic.data
        flight.xc_pic_solo = form.xc_pic_solo.data
        flight.xc_dual = form.xc_dual.data
        flight.night_dual = form.night_dual.data
        flight.night_dual_xc = form.night_dual_xc.data
        flight.night_pic_solo = form.night_pic_solo.data
        flight.se_complex = form.se_complex.data
        flight.instrument_hood = form.instrument_hood.data
        flight.instrument_actual = form.instrument_actual.data
        flight.ftd = form.ftd.data
        flight.pcatd = form.pcatd.data
        flight.ils = form.ils.data
        flight.loc = form.loc.data
        flight.vor = form.vor.data
        flight.rnav_gps = form.rnav_gps.data
        flight.ndb = form.ndb.data
        flight.landings_day = form.landings_day.data
        flight.landings_night = form.landings_night.data

        flight.calculate_log_time()
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
        flight.aircraft_id = form.aircraft.data
        flight.ground_time = form.ground_time.data
        flight.se_dual = form.se_dual.data
        flight.se_solo = form.se_solo.data
        flight.se_pic = form.se_pic.data
        flight.me_dual = form.me_dual.data
        flight.me_pic = form.me_pic.data
        flight.xc_pic_solo = form.xc_pic_solo.data
        flight.xc_dual = form.xc_dual.data
        flight.night_dual = form.night_dual.data
        flight.night_dual_xc = form.night_dual_xc.data
        flight.night_pic_solo = form.night_pic_solo.data
        flight.se_complex = form.se_complex.data
        flight.instrument_hood = form.instrument_hood.data
        flight.instrument_actual = form.instrument_actual.data
        flight.ftd = form.ftd.data
        flight.pcatd = form.pcatd.data
        flight.ils = form.ils.data
        flight.loc = form.loc.data
        flight.vor = form.vor.data
        flight.rnav_gps = form.rnav_gps.data
        flight.ndb = form.ndb.data
        flight.landings_day = form.landings_day.data
        flight.landings_night = form.landings_night.data
        flight.calculate_log_time()
        db.session.add(flight)
        db.session.commit()
        flash('Flight updated.')
        return redirect(url_for('.view_flights'))
    form.date.data = flight.date
    form.student.data = flight.student_id
    form.instructor.data = flight.instructor_id
    form.flight_time.data = flight.flight_time
    form.flight_lesson.data = flight.flight_lesson_id
    form.aircraft.data = flight.aircraft_id
    form.ground_time.data = flight.ground_time
    form.se_dual.data = flight.se_dual
    form.se_solo.data = flight.se_solo
    form.se_pic.data = flight.se_pic
    form.me_dual.data = flight.me_dual
    form.me_pic.data = flight.me_pic
    form.xc_pic_solo.data = flight.xc_pic_solo
    form.xc_dual.data = flight.xc_dual
    form.night_dual.data = flight.night_dual
    form.night_dual_xc.data = flight.night_dual_xc
    form.night_pic_solo.data = flight.night_pic_solo
    form.se_complex.data = flight.se_complex
    form.instrument_hood.data = flight.instrument_hood
    form.instrument_actual.data = flight.instrument_actual
    form.ftd.data = flight.ftd
    form.pcatd.data = flight.pcatd
    form.ils.data = flight.ils
    form.loc.data = flight.loc
    form.vor.data = flight.vor
    form.rnav_gps.data = flight.rnav_gps
    form.ndb.data = flight.ndb
    form.landings_day.data = flight.landings_day
    form.landings_night.data = flight.landings_night
    return render_template('edit_flight.html', form=form)


@main.route('/delete/flight/<flight_id>', methods=['GET', 'POST'])
@login_required
def delete_flight(flight_id):
    flight = Flight.query.filter_by(id=flight_id).first()
    db.session.delete(flight)
    db.session.commit()
    flash('Flight deleted.')
    return redirect(url_for('.view_flights'))


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
            if overlap > 0:
                students.append(student)

        num_students = len(students)

        return render_template('reports/monthly_student_enrollment.html', form=form, students=students,
                               num_students=num_students)
    else:
        return render_template('reports/monthly_student_enrollment.html', form=form)


@main.route('/report/graduation', methods=['GET', 'POST'])
@login_required
def graduation_report():
    form = MonthlyStudentEnrollmentForm()
    if form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
        student_type_id = form.student_type.data
        instructor_id = form.instructor.data
        return redirect(url_for('.graduation_report', from_date=from_date, to_date=to_date,
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

        tests_per_student = defaultdict(lambda: defaultdict(list))
        test_statistics = defaultdict(lambda: defaultdict(int))

        tests = Test.query.join(Student).filter(from_date <= Test.date).filter(to_date >= Test.date).order_by(Test.student_id, Test.date)
        if student_type_id:
            tests = tests.filter(Student.student_type_id == student_type_id)
        if instructor_id:
            tests = tests.filter_by(instructor_id=instructor_id)
        for test in tests.all():
            tests_per_student[test.student_id][test.test_type.id, test.test_type.name, test.test_type.scored].append((test.success, test.score))

        for student_id in tests_per_student:
            for key in tests_per_student[student_id]:
                test_statistics[key]['num_attempts_first'] += 1
                test_statistics[key]['num_attempts_any'] += len(tests_per_student[student_id][key])
                passes = [1 if entry[0] else 0 for entry in tests_per_student[student_id][key]]
                test_statistics[key]['num_passes_first'] += passes[0]
                test_statistics[key]['num_passes_any'] += sum(passes)
                scores = [entry[1] for entry in tests_per_student[student_id][key] if entry[1]]
                if scores:
                    test_statistics[key]['sum_score_first'] += scores[0]
                    test_statistics[key]['sum_score_any'] += sum(scores)

        for key in test_statistics:
            test_statistics[key]['pass_rate_first'] = '%1.1f%%' % (test_statistics[key]['num_passes_first']*100/test_statistics[key]['num_attempts_first'])
            test_statistics[key]['pass_rate_any'] = '%1.1f%%' % (test_statistics[key]['num_passes_any']*100/test_statistics[key]['num_attempts_any'])
            test_statistics[key]['num_fails'] = test_statistics[key]['num_attempts_any'] - test_statistics[key]['num_passes_any']
            if key[2]:
                test_statistics[key]['avg_score_first'] = test_statistics[key]['sum_score_first']/test_statistics[key]['num_passes_first']
                test_statistics[key]['avg_score_any'] = test_statistics[key]['sum_score_any']/test_statistics[key]['num_passes_any']
            else:
                test_statistics[key]['avg_score_first'] = '-'
                test_statistics[key]['avg_score_any'] = '-'

        test_statistics_tuples = []
        for key, value in test_statistics.items():
            test_statistics_tuples.append((key[0], key[1], value))

        return render_template('reports/graduation.html', form=form, test_stats=sorted(test_statistics_tuples))

    else:
        return render_template('reports/graduation.html', form=form)


@main.route('/report/logbook', methods=['GET', 'POST'])
@login_required
def logbook_report():
    form = LogbookForm()
    if form.validate_on_submit():
        from_date = form.from_date.data
        to_date = form.to_date.data
        student_id = form.student.data
        return redirect(url_for('.logbook_report', from_date=from_date, to_date=to_date,
                                student_id=student_id))
    if 'from_date' in request.values and 'to_date' in request.values:
        from_date = datetime.strptime(request.values.get('from_date'), '%Y-%m-%d').date()
        to_date = datetime.strptime(request.values.get('to_date'), '%Y-%m-%d').date()
        student_id = int(request.values.get('student_id'))
        form.from_date.data = from_date
        form.to_date.data = to_date
        form.student.data = student_id

        flights = db.session.query(Flight).join(Instructor).filter(student_id==Flight.student_id).filter(from_date <= Flight.date).filter(to_date >= Flight.date).order_by(Flight.date).all()
        return render_template('reports/logbook.html', form=form, flights=flights)
    else:
        return render_template('reports/logbook.html', form=form)