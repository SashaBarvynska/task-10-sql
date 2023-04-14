from http import HTTPStatus

from flask import jsonify, request, wrappers
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from src import CourseModel, GroupModel, StudentCourseModel, StudentModel, db
from src.app import app


# Add new student
@app.route('/students', methods=['POST'])
def add_student() -> wrappers.Response:
    data = request.get_json()
    new_student = StudentModel(
        first_name=data['first_name'],
        last_name=data['last_name']
        )
    Session = sessionmaker(bind=db)
    session = Session()
    session.add(new_student)
    session.commit()

    return jsonify(
        {
            'student_id': new_student.student_id,
            'first_name': new_student.first_name,
            'last_name': new_student.last_name
        }
      ), HTTPStatus.OK


# Delete student by STUDENT_ID
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id) -> wrappers.Response:
    Session = sessionmaker(bind=db)
    session = Session()
    student = session.query(StudentModel).filter_by(student_id=id).first()
    if not student:
        return jsonify({'error': 'Student by {id} not found.'}), HTTPStatus.NOT_FOUND
    else:
        session.delete(student)
        session.commit()
        return jsonify({'message': f'Student by {id} has been deleted.'}), HTTPStatus.OK


# Find all students related to the course with a given name.
@app.route('/students', methods=['GET'])
def get_courses() -> wrappers.Response:
    course = request.args.get('course')
    Session = sessionmaker(bind=db)
    session = Session()
    students = session.query(StudentModel).join(StudentCourseModel).join(CourseModel).filter(
        CourseModel.name == course
        ).all()

    dict_students = list(map(lambda student: {
            "student_id": student.student_id, "first_name": student.first_name, "last_name": student.last_name
        }, students))
    return jsonify(dict_students), HTTPStatus.OK


# Add a student to the course (from a list)
@app.route('/students/add_course', methods=['POST'])
def add_student_to_course() -> wrappers.Response:
    data = request.get_json()
    Session = sessionmaker(bind=db)
    session = Session()
    query = session.query(CourseModel.course_id).join(StudentCourseModel).join(StudentModel).filter(
        StudentModel.student_id == data['student_id'], CourseModel.course_id.in_(data['course_id'])
        ).all()
    if query:
        return jsonify({'error': f"this course by id {[q[0] for q in query]} already exists"}), HTTPStatus.NOT_FOUND
    else:
        for id in data['course_id']:
            add_course_id = StudentCourseModel(student_id=data['student_id'], course_id=id)
            session.add(add_course_id)
        session.commit()
        return jsonify({'massage': "course was added successfully"}), HTTPStatus.OK


# Remove the student from one of his or her courses
@app.route('/students/<int:id>/courses', methods=['DELETE'])
def delete_course(id) -> wrappers.Response:
    course = request.args.get('course')
    Session = sessionmaker(bind=db)
    session = Session()
    query = session.query(StudentCourseModel).join(CourseModel).join(StudentModel).filter(
        StudentModel.student_id == id, CourseModel.course_id == course
        ).first()
    if not query:
        return jsonify({'error': 'Course by id {query.course_id} not found.'}), HTTPStatus.NOT_FOUND
    session.delete(query)
    session.commit()
    return jsonify({'message': f'Course by id {query.course_id} has been deleted.'}), HTTPStatus.OK


# Find all groups with less or equals student count.
@app.route('/groups', methods=['GET'])
def get_groups() -> wrappers.Response:
    max_students = request.args.get('max_students')
    Session = sessionmaker(bind=db)
    session = Session()
    groups = session.query(GroupModel).join(StudentModel).group_by(
        GroupModel.group_id
        ).having(func.count(StudentModel.student_id) <= max_students).all()
    dict_students = list(map(lambda group: {
            "group_id": group.group_id, "name.": group.name}, groups))
    return jsonify(dict_students), HTTPStatus.OK


@app.errorhandler(404)
def handle_exception(e) -> wrappers.Response:
    return jsonify({"message": "Page Not Found"}, HTTPStatus.NOT_FOUND)
