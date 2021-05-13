def class_name_2_id(p_service_classroom, name):
    """
    Converts the name of the class to the Google classroom course id.
    Note, this will give the first match, so if you have multiple, it will die.
    :param p_service_classroom:  Google classroom API service object (google classroom api object)
    :param name: Name of the course
    :return:
    """
    print("Converting the Google classroom name to course id")
    results = p_service_classroom.courses().list().execute()
    courses = results.get('courses', [])
    count = 0
    save_index = 0
    course_names = []
    for index, course in enumerate(courses):
        if course['courseState'] == 'ARCHIVED':
            continue
        course_names.append(course['name'])
        if name == course['name']:
            count += 1
            save_index = index
    if count > 1:
        print(f'Check your Google classroom.  You have two or more courses with the same name.\n'
              f'Here is the list of courses:\n{course_names}')
        input("Press enter to continue")
        raise ValueError(f'Check your Google classroom.  You have two or more courses with the same name.\n'
                         f'Here is the list of courses:\n{course_names}')
    elif count == 1:
        course_id = courses[save_index]['id']
    else:
        print(f'Could not find the name of the course you requested.  You requested this course:\n{name}\n'
              f'Here is the list of courses:\n{course_names}')
        input("Press enter to continue")
        raise ValueError(f'Could not find the name of the course you requested.  You requested this course:\n{name}\n'
                         f'Here is the list of courses:\n{course_names}')
    return course_id


def get_assignments_from_classroom(p_service_classroom, p_course_id, p_quarter_start_obj):
    """
    Gets all the assignments from the classroom, given a course ID and start date
    :param p_service_classroom:  Google classroom API service object (google classroom api object)
    :param p_course_id: course ID of Google classroom (str)
    :param p_quarter_start_obj: datetime object, 1st day of current quarter (datetime obj)
    :return:
    """
    import datetime

    print("In get_assignments_from_classroom.  Getting all assignments that are due after this quarter OR "
          "that have no due date")
    final_courseworks = []
    p_courseworks = p_service_classroom.courses().\
        courseWork().list(courseId=p_course_id).execute().get('courseWork', [])
    for coursework in p_courseworks:
        if 'dueDate' in coursework:
            due_date = coursework['dueDate']
            due_date_obj = datetime.datetime(due_date['year'], due_date['month'], due_date['day'])
            if due_date_obj > p_quarter_start_obj:
                print("This assignment will be processed: " + str(coursework['title']))
                final_courseworks.append(coursework)
            else:
                print("     --- Skipping this assignment, due date was before start of this quarter: " +
                      str(coursework['title']))
        else:
            final_courseworks.append(coursework)
    return final_courseworks


def get_student_profiles(p_service_classroom, course_id):
    """
    Gets the student profiles, given a particular classroom in GC
    :param p_service_classroom:  Google classroom API service object (google classroom api object)
    :param course_id: course ID for this class (string)
    :return: dictionary with keys id and name, student INFo and IDs (dict)
    """
    students = p_service_classroom.courses().students().list(courseId=course_id, ).execute()
    students = students['students']
    gc_students = {}
    # print("In getting_assignments, getting students")
    for student in students:
        p_student_id = student['userId']
        student_profiles = p_service_classroom.userProfiles(). \
            get(userId=p_student_id, ).execute()
        # print(student_profiles)
        print(student_profiles['emailAddress'])
        gc_students[p_student_id] = student_profiles['name']['fullName']
    # print("students!" + str(gc_students))
    return gc_students


def get_assignment_scores_from_classroom(p_service_classroom, p_student_profiles, p_courseworks, p_course_id):
    """
    Given a classroom, students profiles, and courseworks, finds assignments that are returned and potentially
    up for putting into Aspen
    :param p_service_classroom:  Google classroom API service object (google classroom api object)
    :param students_dict: dictionary with keys id and name, student INFo and IDs (dict)
    :param p_courseworks: Dictionary of student courseworks in Google classroom
    :param p_course_id: ID of the course (str)
    :return: dictionary of lists.  assignments_scores_to_aspen = {'python1.040': [ [111142, 40], [123123, 50]} etc...
    """
    import datetime
    import re
    from helper_functions.quarters import which_quarter_today

    p_quarter_start_obj = which_quarter_today()
    assignments_scores_to_aspen = {}
    for coursework in p_courseworks:
        coursework_id = coursework['id']
        coursework_title = coursework['title']
        if 'dueDate' in coursework:
            due_date = coursework['dueDate']
            due_date_obj = datetime.datetime(due_date['year'], due_date['month'], due_date['day'])
            if due_date_obj > p_quarter_start_obj:
                student_works = p_service_classroom.courses(). \
                    courseWork().studentSubmissions().list(courseId=p_course_id, courseWorkId=coursework_id).execute()
                student_works = student_works['studentSubmissions']
                for student_work in student_works:
                    if 'assignedGrade' in student_work.keys():
                        if student_work['state'] == 'RETURNED':
                            coursework_title = re.sub(r'\s:-\)', '', coursework_title) # remove the smiley from title
                            p_student_id = student_work['userId']
                            student_name = p_student_profiles[p_student_id]
                            grade = student_work['assignedGrade']
                            if coursework_title in assignments_scores_to_aspen.keys():
                                assignments_scores_to_aspen[coursework_title].append([student_name, grade])
                            else:
                                assignments_scores_to_aspen[coursework_title] = [[student_name, grade]]
    return assignments_scores_to_aspen


def verify_due_date_exists(p_courseworks):
    """
    Verifies every assignment has a due date
    :param p_courseworks:  courseworks list of coursework objects
    :return: NOne
    """

    bad_courseworks = []
    for coursework in p_courseworks:
        if 'dueDate' not in coursework:
            bad_courseworks.append(coursework['title'])
    if bad_courseworks:
        print((f"Every assignment should have a due date.  Here are the assignments without a due date:"
               f" {bad_courseworks} \nProgram will exit now."))
        input("Press enter to continue.")
        raise ValueError(f"Every assignment should have a due date.  Here are the assignments without a due date:"
                         f" {bad_courseworks}  \nProgram will exit now.")


def verify_points_exists(p_courseworks):
    """
    Verifies every assignment has a due date
    :param p_courseworks:  list of google classroom coursework objects
    :return: NOne
    """

    bad_courseworks = []
    for coursework in p_courseworks:
        # print(coursework)
        if 'maxPoints' not in coursework:
            bad_courseworks.append(coursework['title'])
    if bad_courseworks:
        print(f"Every assignment should have a points.  Here are the assignments without points for the "
              f"assignment:"
              f" {bad_courseworks} ")
        input("Press enter to continue.")
        raise ValueError(f"Every assignment should have a points.  Here are the assignments without points for the "
                         f"assignment:"
                         f" {bad_courseworks} ")


def scrub_courseworks(p_courseworks, list_name, p_list, p_content_knowledge):
    """
    takes courseworks and if the assignment is in p_list, removes that from courseworks
    :param p_courseworks: list of Google classroom coursework objects
    :param list_name: name of list (for printouts) string
    :param p_list: list of items that you don't want the column to be (list of str)
    :param p_content_knowledge: Whether or not you are doing content knowledge aspen entries (changes length) Boolean
    :return: new courseworks
    """
    from helper_functions.aspen_functions import convert_assignment_name

    new_courseworks = []
    for coursework in p_courseworks:
        found = False
        new_proposed_name = convert_assignment_name(coursework['title'], p_content_knowledge)
        if new_proposed_name in p_list or new_proposed_name + '-C' in p_list or \
                new_proposed_name + '-K' in p_list:
            found = True
            print("Skipping this assignment, is in " + str(list_name) + " already:" + str(coursework['title']))
        if found is False:
            new_courseworks.append(coursework)
    return new_courseworks



def scrub_assignment_scores_student_id(p_gc_assignment_scores_student_id, p_rows):
    """
    Takes google classroom assignment name + student ID + scores dictionary, and query from DB
    and returns only unique values
    :param p_gc_assignment_scores_student_id: dictionary of google classroom student ID
    :param p_rows: Rows from query of DB
    :return:  Scrubbed  gc_assignment_scores_student_id, the anti-union of gc_assignment_scores_student_id and rows
    """

    new_gc_assignment_scores_student_id = {}
    # print(f"p rows {p_rows}")
    new_p_rows = [x[1:] for x in p_rows]
    # print(new_p_rows)
    for key in p_gc_assignment_scores_student_id:
        turnins = p_gc_assignment_scores_student_id[key]  # a turnin is a list with student, and score.
                                                          # Made up term.  turnin_list is all turnins for that
                                                          # assignment
        for turnin in turnins:
            # print(f"This is the turnin {turnin}")
            turnin_tuple = (key, turnin[0], turnin[1])
            if turnin_tuple not in new_p_rows: # duplicate
                if key in new_gc_assignment_scores_student_id.keys():
                    new_gc_assignment_scores_student_id[key].append([turnin[0], turnin[1]])
                else:
                    new_gc_assignment_scores_student_id[key] = [[turnin[0], turnin[1]]]
    return new_gc_assignment_scores_student_id


def get_assignments_from_classroom_and_students(p_service_classroom, course_id, p_quarter_start_obj):
    """
    :param p_service_classroom: Google classroom API service object (google classroom api object)
    :param course_id: Google classroom course ID (string)
    :param p_quarter_start_obj: start of the quarter, datetime format
    :return: dictionary.  Keys are assignment names, value is a list with items [student name, score] i.e. nested list
    """

    import datetime
    import re
    # Getting students
    students = p_service_classroom.courses().students().list(courseId=course_id,).execute()
    students = students['students']
    gc_students = {}
    #print("In getting_assignments, getting students")
    for student in students:
        p_student_id = student['userId']
        student_profiles = p_service_classroom.userProfiles().\
            get(userId=p_student_id,).execute()
        #print(student_profiles)
        # print(student_profiles['emailAddress'])
        gc_students[p_student_id] = student_profiles['name']['fullName']
    #  print(gc_students)
    # print("Getting assignments")
    p_courseworks = p_service_classroom.courses().\
        courseWork().list(courseId=course_id).execute().get('courseWork', [])
    assignments_scores_to_aspen = {}
    for coursework in p_courseworks:
        coursework_id = coursework['id']
        coursework_title = coursework['title']
        # print(coursework)
        if 'dueDate' in coursework:
            due_date = coursework['dueDate']
            due_date_obj = datetime.datetime(due_date['year'], due_date['month'], due_date['day'])
            # print(f"Coursework {coursework} duedate {due_date_obj} quarter {p_quarter_start_obj}")
            if due_date_obj > p_quarter_start_obj:
                student_works = p_service_classroom.courses(). \
                    courseWork().studentSubmissions().list(courseId=COURSE_ID, courseWorkId=coursework_id).execute()
                student_works = student_works['studentSubmissions']
                for student_work in student_works:
                    # print(f"STUDENT WORK {student_work}")
                    if 'assignedGrade' in student_work.keys():
                        # print("yes")
                        if student_work['state'] == 'RETURNED':
                            print(f"doing this one:  {student_work}")
                            print(coursework_title)
                            print(assignments_scores_to_aspen)
                            coursework_title = re.sub(r'\s:-\)', '', coursework_title)
                            p_student_id = student_work['userId']
                            student_name = gc_students[p_student_id]
                            grade = student_work['assignedGrade']
                            # print(f"grade {grade} student id {student_id} student name {student_name}")

                            if coursework_title in assignments_scores_to_aspen.keys():
                                assignments_scores_to_aspen[coursework_title].append([student_name, grade])
                            else:
                                assignments_scores_to_aspen[coursework_title] = [[student_name, grade]]
    return assignments_scores_to_aspen
