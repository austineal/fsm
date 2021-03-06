from __future__ import division

from datetime import datetime, date, timedelta
from collections import defaultdict, namedtuple
from sqlalchemy import func
from flask import render_template, flash, redirect, url_for, request, current_app, make_response
from flask.helpers import send_file
from flask.ext.login import login_required
from flask_weasyprint import HTML, render_pdf
from .forms import AddStudentForm, AddInstructorForm, AddFlightLessonForm, AddTestTypeForm, AddFlightForm, AddTestForm, MonthlyStudentEnrollmentForm, LogbookForm, AddAircraftForm
from ..models import Student, Instructor, FlightLesson, TestType, Flight, Test, Aircraft, User, Role
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
                          zip_code=form.zip.data,
                          phone_number=form.phone_number.data,
                          email_address=form.email_address.data,
                          active=form.active.data,
                          student_type_id=form.student_type.data,
                          instructor_id=form.instructor.data,
                          medical_received=form.medical_received.data,
                          medical_expires=form.medical_expires.data,
                          tsa_eligibility_doc_id=form.tsa_proof.data,
                          student_certificate_received=form.student_cert_received.data,
                          student_certificate_expires=form.student_cert_expires.data)
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
        student.zip_code = form.zip.data
        student.phone_number = form.phone_number.data
        student.email_address = form.email_address.data
        student.enrollment_start_date = form.enrollment_start_date.data
        student.enrollment_end_date = form.enrollment_end_date.data
        student.active = form.active.data
        student.student_type_id = form.student_type.data
        student.instructor_id = form.instructor.data
        student.medical_received = form.medical_received.data
        student.medical_expires = form.medical_expires.data
        student.tsa_eligibility_doc_id = form.tsa_proof.data
        student.student_certificate_received = form.student_cert_received.data
        student.student_certificate_expires = form.student_cert_expires.data
        db.session.add(student)
        db.session.commit()
        flash('Student updated.')
        return redirect(url_for('.view_students'))
    form.first_name.data = student.first_name
    form.last_name.data = student.last_name
    form.address.data = student.address
    form.city.data = student.city
    form.state.data = student.state_id
    form.zip.data = student.zip_code
    form.phone_number.data = student.phone_number
    form.email_address.data = student.email_address
    form.enrollment_start_date.data = student.enrollment_start_date
    form.enrollment_end_date.data = student.enrollment_end_date
    form.active.data = student.active
    form.student_type.data = student.student_type_id
    form.instructor.data = student.instructor_id
    form.medical_received.data = student.medical_received
    form.medical_expires.data = student.medical_expires
    form.tsa_proof.data = student.tsa_eligibility_doc_id
    form.student_cert_received.data = student.student_certificate_received
    form.student_cert_expires.data = student.student_certificate_expires
    return render_template('edit_student.html', form=form)


@main.route('/delete/students/<student_id>', methods=['GET', 'POST'])
@login_required
def delete_student(student_id):
    student = Student.query.filter_by(id=student_id).first()
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted.')
    return redirect(url_for('.view_students'))


@main.route('/add/instructor', methods=['GET', 'POST'])
@login_required
def add_instructor():
    form = AddInstructorForm()
    if form.validate_on_submit():
        instructor = Instructor(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                tsa_eligibility_doc_id=form.tsa_proof.data,
                                medical_received=form.medical_received.data,
                                medical_expires=form.medical_expires.data,
                                flight_review_received=form.flight_review_received.data,
                                flight_review_expires=form.flight_review_expires.data,
                                bfr_received=form.bfr_received.data,
                                bfr_expires=form.bfr_expires.data,
                                ipc_received=form.ipc_received.data,
                                ipc_expires=form.ipc_expires.data,
                                checkout_141=form.checkout_141.data,
                                checkout_141_date=form.checkout_141_date.data,
                                night_currency_start_date=form.night_currency_start_date.data,
                                night_currency_end_date=form.night_currency_end_date.data,
                                me_currency_start_date=form.me_currency_start_date.data,
                                me_currency_end_date=form.me_currency_end_date.data,
                                tailwheel_currency_start_date=form.tailwheel_currency_start_date.data,
                                tailwheel_currency_end_date=form.tailwheel_currency_end_date.data)
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
        instructor.tsa_eligibility_doc_id = form.tsa_proof.data
        instructor.medical_received = form.medical_received.data
        instructor.medical_expires = form.medical_expires.data
        instructor.flight_review_received = form.flight_review_received.data
        instructor.flight_review_expires = form.flight_review_expires.data
        instructor.bfr_received = form.bfr_received.data
        instructor.bfr_expires = form.bfr_expires.data
        instructor.ipc_received = form.ipc_received.data
        instructor.ipc_expires = form.ipc_expires.data
        instructor.checkout_141 = form.checkout_141.data
        instructor.checkout_141_date = form.checkout_141_date.data
        instructor.night_currency_start_date = form.night_currency_start_date.data
        instructor.night_currency_end_date = form.night_currency_end_date.data
        instructor.me_currency_start_date = form.me_currency_start_date.data
        instructor.me_currency_end_date = form.me_currency_end_date.data
        instructor.tailwheel_currency_start_date = form.tailwheel_currency_start_date.data
        instructor.tailwheel_currency_end_date = form.tailwheel_currency_end_date.data
        db.session.add(instructor)
        db.session.commit()
        flash('Instructor updated.')
        return redirect(url_for('.view_instructors'))
    form.first_name.data = instructor.first_name
    form.last_name.data = instructor.last_name
    form.tsa_proof.data = instructor.tsa_eligibility_doc_id
    form.medical_received.data = instructor.medical_received
    form.medical_expires.data = instructor.medical_expires
    form.flight_review_received.data = instructor.flight_review_received
    form.flight_review_expires.data = instructor.flight_review_expires
    form.bfr_received.data = instructor.bfr_received
    form.bfr_expires.data = instructor.bfr_expires
    form.ipc_received.data = instructor.ipc_received
    form.ipc_expires.data = instructor.ipc_expires
    form.checkout_141.data = instructor.checkout_141
    form.checkout_141_date.data = instructor.checkout_141_date
    form.night_currency_start_date.data = instructor.night_currency_start_date
    form.night_currency_end_date.data = instructor.night_currency_end_date
    form.me_currency_start_date.data = instructor.me_currency_start_date
    form.me_currency_end_date.data = instructor.me_currency_end_date
    form.tailwheel_currency_start_date.data = instructor.tailwheel_currency_start_date
    form.tailwheel_currency_end_date.data = instructor.tailwheel_currency_end_date

    return render_template('edit_instructor.html', form=form)


@main.route('/delete/instructors/<instructor_id>', methods=['GET', 'POST'])
@login_required
def delete_instructors(instructor_id):
    instructor = Instructor.query.filter_by(id=instructor_id).first()
    db.session.delete(instructor)
    db.session.commit()
    flash('Instructor deleted.')
    return redirect(url_for('.view_instructors'))


@main.route('/add/lesson', methods=['GET', 'POST'])
@login_required
def add_flight_lesson():
    form = AddFlightLessonForm()
    if form.validate_on_submit():
        lesson = FlightLesson(number=form.number.data,
                              name=form.name.data,
                              objectives=form.objectives.data,
                              completion_standards=form.completion_standards.data)
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
        lesson.objectives = form.objectives.data
        lesson.completion_standards = form.completion_standards.data
        db.session.add(lesson)
        db.session.commit()
        flash('Flight lesson updated.')
        return redirect(url_for('.view_flight_lessons'))
    form.number.data = lesson.number
    form.name.data = lesson.name
    form.objectives.data = lesson.objectives
    form.completion_standards.data = lesson.completion_standards
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
def delete_testtype(testtype_id):
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
        if form.complete.raw_data[0] == 'True':
            flight.complete = True
        else:
            flight.complete = False
        if flight.complete:
            flight.completed_objectives = ''
        else:
            flight.completed_objectives = form.completed_objectives.data

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
        if 'add_flight' in request.form:  # if the Save Flight button was clicked
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
            if form.complete.raw_data[0] == 'True':
                flight.complete = True
            else:
                flight.complete = False
            if flight.complete:
                flight.completed_objectives = ''
            else:
                flight.completed_objectives = form.completed_objectives.data
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
    form.complete.data = flight.complete
    form.completed_objectives.data = flight.completed_objectives
    return render_template('edit_flight.html', form=form)


@main.route('/view/flight/<flight_id>/pdf', methods=['GET', 'POST'])
@login_required
def view_flight_pdf(flight_id):
    flight = Flight.query.filter_by(id=flight_id).first()
    html = render_template('edit_flight_pdf.html', flight=flight)
    filename = '%s_%s_lesson%s.pdf' % (flight.student.last_name, flight.date, flight.flight_lesson.number)
    return render_pdf(HTML(string=html), download_filename=filename)


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


@main.route('/delete/test/<test_id>', methods=['GET', 'POST'])
@login_required
def delete_test(test_id):
    test = Test.query.filter_by(id=test_id).first()
    db.session.delete(test)
    db.session.commit()
    flash('Test deleted.')
    return redirect(url_for('.view_tests'))


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
            first_flight_for_student = Flight.query.filter_by(student_id=test.student_id).order_by(Flight.date).first()
            if first_flight_for_student:
                days_to_test = (test.date - first_flight_for_student.date).days
                if days_to_test < 0:
                    days_to_test = None
            else:
                days_to_test = None
            tests_per_student[test.student_id][test.test_type.id, test.test_type.name, test.test_type.scored].append((test.success, test.score, days_to_test))

        for student_id in tests_per_student:
            for key in tests_per_student[student_id]:
                test_statistics[key]['num_attempts_first'] += 1
                test_statistics[key]['num_attempts_any'] += len(tests_per_student[student_id][key])
                passes = [1 if entry[0] else 0 for entry in tests_per_student[student_id][key]]
                test_statistics[key]['num_passes_first'] += passes[0]
                test_statistics[key]['num_passes_any'] += sum(passes)
                scores = [entry[1] for entry in tests_per_student[student_id][key] if entry[0] and entry[1]]
                if scores:
                    test_statistics[key]['sum_score_first'] += scores[0]
                    test_statistics[key]['sum_score_any'] += sum(scores)

                # the min here should be unnecessary because each student should only pass each test once, but in case
                # there is more than one pass for the same student for the same test, we will take the first one
                days_to_completion_list = [entry[2] for entry in tests_per_student[student_id][key] if entry[0] and entry[2]]
                if days_to_completion_list:
                    days_to_completion = min(days_to_completion_list)
                    if 'days_to_completion' in test_statistics[key]:
                        test_statistics[key]['days_to_completion'].append(days_to_completion)
                    else:
                        test_statistics[key]['days_to_completion'] = [days_to_completion]

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
            if 'days_to_completion' in test_statistics[key]:
                test_statistics[key]['min_days_to_completion'] = '%d days' % min(test_statistics[key]['days_to_completion'])
                test_statistics[key]['avg_days_to_completion'] = '%1.1f days' % (sum(test_statistics[key]['days_to_completion'])/len(test_statistics[key]['days_to_completion']))
            else:
                test_statistics[key]['min_days_to_completion'] = '-'
                test_statistics[key]['avg_days_to_completion'] = '-'

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


@main.route('/report/currency', methods=['GET', 'POST'])
@login_required
def currency_report():

    td = date.today()
    td_plus_30 = td + timedelta(days=30)
    td_minus_30 = td - timedelta(days=30)

    ## students
    students = []

    # medical
    students_medical = Student.query.filter(Student.medical_expires <= td_plus_30)
    for student in students_medical:
        students.append((student, 'medical', student.medical_expires, (student.medical_expires - td).days))

    # student certificate
    students_certificate = Student.query.filter(Student.student_certificate_expires <= td_plus_30)
    for student in students_certificate:
        students.append((student, 'student_cert', student.student_certificate_expires, (student.student_certificate_expires - td).days))

    # last flight
    # NOTE: will ignore students who have not logged *any* flights
    student_flight = Student.query.filter(Student.active).join(Student.flights)
    for student in student_flight:
        print student.id, student.first_name, student.last_name
        most_recent_flight = sorted(student.flights, key=lambda x: x.date)[-1]
        if most_recent_flight.date <= td_minus_30:
            students.append((student, 'no_flight', most_recent_flight.date, (most_recent_flight.date - td).days))

    ## instructors
    instructors = []

    # medical
    instructors_medical = Instructor.query.filter(Instructor.medical_expires <= td_plus_30)
    for instructor in instructors_medical:
        instructors.append((instructor, 'medical', instructor.medical_expires, (instructor.medical_expires - td).days))

    # flight review
    instructors_flight_review = Instructor.query.filter(Instructor.flight_review_expires <= td_plus_30)
    for instructor in instructors_flight_review:
        instructors.append((instructor, 'flight_review', instructor.flight_review_expires, (instructor.flight_review_expires - td).days))

    # bfr
    instructors_bfr = Instructor.query.filter(Instructor.bfr_expires <= td_plus_30)
    for instructor in instructors_bfr:
        instructors.append((instructor, 'bfr', instructor.bfr_expires, (instructor.bfr_expires - td).days))

    # ipc
    instructors_ipc = Instructor.query.filter(Instructor.ipc_expires <= td_plus_30)
    for instructor in instructors_ipc:
        instructors.append((instructor, 'ipc', instructor.ipc_expires, (instructor.ipc_expires - td).days))

    # night currency
    instructors_night_currency = Instructor.query.filter(Instructor.night_currency_end_date <= td_plus_30)
    for instructor in instructors_night_currency:
        instructors.append((instructor, 'night_currency', instructor.night_currency_end_date, (instructor.night_currency_end_date - td).days))

    # me currency
    instructors_me_currency = Instructor.query.filter(Instructor.me_currency_end_date <= td_plus_30)
    for instructor in instructors_me_currency:
        instructors.append((instructor, 'me_currency', instructor.me_currency_end_date, (instructor.me_currency_end_date - td).days))

    # tail wheel currency
    instructors_tailwheel_currency = Instructor.query.filter(Instructor.tailwheel_currency_end_date <= td_plus_30)
    for instructor in instructors_tailwheel_currency:
        instructors.append((instructor, 'tail_wheel_currency', instructor.tailwheel_currency_end_date, (instructor.tailwheel_currency_end_date - td).days))

    return render_template('reports/currency.html',
                           students=sorted(students,
                                           key=lambda x: (x[2], x[1], x[0].last_name, x[0].first_name)),
                           instructors=sorted(instructors,
                                              key=lambda x: (x[2], x[1], x[0].last_name, x[0].first_name))
                           )