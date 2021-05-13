import base64
import datetime
import configparser
from helper_functions.classroom_functions import class_name_2_id
from generate_gmail_credential import generate_gmail_credential
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from generate_classroom_credential import generate_classroom_credential
from helper_functions.quarters import which_quarter_today





config = configparser.ConfigParser()
config.read("classroom_assignments_to_aspen.ini")

if 'QUARTERS' in config:
    quarters = config['QUARTERS']
    q1 = quarters['q1']
    q2 = quarters['q2']
    q3 = quarters['q3']
    q4 = quarters['q4']
else:
    username = ''
    password = ''
if 'OPTIONS' in config:
    options = config['OPTIONS']
    if 'default_category' in options:
        default_category = options['default_category']
else:
    default_category = ''





#
# student_dict = {'21nlei@cpsd.us': '103026788979009218908',
#                 '21atekieteklemariam@cpsd.us': 102189211805773929897}

'''

{'id': '117019328754907443769', 'name': {'givenName': 'THOMAS', 'familyName': 'BREWITT', 'fullName': 'THOMAS BREWITT'}}
{'id': '100437299855115523930', 'name': {'givenName': 'MOHAMMED', 'familyName': 'MUSAWWIR', 'fullName': 'MOHAMMED MUSAWWIR'}}
{'id': '115899787127900489710', 'name': {'givenName': 'Nobel', 'familyName': 'Temam', 'fullName': 'Nobel Temam'}}
{'id': '107372429037627570808', 'name': {'givenName': 'FERNANDO', 'familyName': 'PANEPINTO HATTORI', 'fullName': 'FERNANDO PANEPINTO HATTORI'}}
{'id': '117781278118817502289', 'name': {'givenName': 'SKYLER', 'familyName': 'MARKS', 'fullName': 'SKYLER MARKS'}}
{'id': '117580555014802942323', 'name': {'givenName': 'JONAH', 'familyName': 'JAFFE', 'fullName': 'JONAH JAFFE'}}
{'id': '112667830524174574890', 'name': {'givenName': 'Biruk', 'familyName': 'Alemu', 'fullName': 'Biruk Alemu'}}
{'id': '115853813505606026479', 'name': {'givenName': 'Eden', 'familyName': 'Wegayhu', 'fullName': 'Eden Wegayhu'}}
{'id': '102475404831589545837', 'name': {'givenName': 'Sauvik', 'familyName': 'Roy', 'fullName': 'Sauvik Roy'}}
{'id': '114590111590307965499', 'name': {'givenName': 'Matias', 'familyName': 'Stringa', 'fullName': 'Matias Stringa'}}
{'id': '116668099320993692987', 'name': {'givenName': 'JUSTIN-CORI', 'familyName': 'AZEVEDO', 'fullName': 'JUSTIN-CORI AZEVEDO'}}
{'id': '116104146147212808913', 'name': {'givenName': 'RYAN', 'familyName': 'GUERRERO', 'fullName': 'RYAN GUERRERO'}}
'''
# email_dict = {
#  '100437299855115523930': '23mmusawwir@cpsd.us',
#  '115899787127900489710': '21ntemam@cpsd.us',
#  '107372429037627570808': '22fpanepintohattori@cpsd.us',
#  '117781278118817502289': '22smarks@cpsd.us',
#  '117580555014802942323': '21jjaffe@cpsd.us',
#  '112667830524174574890': '22balemu@cpsd.us',
#  '115853813505606026479': '20ewegayhu@cpsd.us',
#  '102475404831589545837': '22sroy@cpsd.us',
#  '114590111590307965499': '23mstringa@cpsd.us',
#  '116668099320993692987': '22jazevedo@cpsd.us',
#  '116104146147212808913': '21rguerrero@cpsd.us',
# }

students = service_classroom.courses().students().list(courseId=course_id,).execute()
students = students['students']


for student in students:
    student_id = student['userId']
    student_profiles = service_classroom.userProfiles().get(userId=student_id,).execute()
    print(student_profiles)


assignments_id_dict = {}
all_assignments = service_classroom.courses().courseWork().list(courseId=course_id,).execute()
all_assignments = all_assignments['courseWork']
for assignment in all_assignments:
    assignments_id_dict[assignment['id']] = assignment['title']

#print("HERE ARE THE ASSIGNMENTS AND THEIR IDs")
#print(assignments_id_dict)

messages = []
for student in students:
    student_id = student['userId']
    student_email = student['name']['emailAddress']
    message_dict = {}
    message_dict[student_id] = ''
    print("Trying this student ID : " + str(student_id))
    print("this student" + email_dict[student_id])
    student_work = service_classroom.courses().\
        courseWork().studentSubmissions().list(courseId=course_id, courseWorkId='-',userId=student_id).execute()
    student_work = student_work['studentSubmissions']
    for work in student_work:
        if 'late' in work:
            work_id = work['courseWorkId']
            for assignment in all_assignments:
                if work_id == assignment['id']:
                    due_date = assignment['dueDate']

            if work['state'] != 'TURNED_IN' and work['late'] is True:
                d1 = datetime.datetime(due_date['year'], due_date['month'], due_date['day'])
                d2 = datetime.datetime.now()
                q2 = datetime.datetime(2021, 2, 4)
                if d2 >= d1 and d1 > q2:
                    link = work['alternateLink']
                    coursework_id = work['courseWorkId']
                    message_dict[student_id] += "assignment:  {} \nlink to assignment {}\n\n".format(assignments_id_dict[coursework_id], link)
    messages.append(message_dict)
#message_dict = create_message('ewu@cpsd.us', 'ejw50@hotmail.com', 'hello there', 'smell my   feet')
#print(message_dict)
service_gmail = generate_gmail_credential()

print("these are messages")
for message in messages:
    for key in message:
        email_address = email_dict[key]
        print("This person " + str(email_address) + " is missing these (past due) assignments ")
        if not message[key]:
            message[key] = 'Nothing! You have everything turned in that is due.  Great work!'
        else:
            message[key] = "Hello! Here are assignments that are past due that are not turned in yet:\n\n" + message[key]
        message[key] = email_address + '\n' + message[key]


        # message[key] += '\n\nLast day to turn in assignments or extra credit is Friday 01/29/21\n\n'
        # message[key] += 'Create task must be "finalized" by 1/29 and turned in the digital portfolio, even if ' \
        #                 'you are not taking the AP exam.  \n' \
        #                 'link: https://digitalportfolio.collegeboard.org/\n\n' \
        #                 'If you need to edit your AP create task after 1/29, we can "unfinalize" it for you.\n'


        message[key] += '\n\nThis is an automated email\n\n'
        print(message[key])


        msg_text = message[key]
        email_message = MIMEMultipart()
        email_message['to'] = email_address
        email_message['cc'] = 'ewu@cpsd.us'
        email_message['subject'] = 'Cybersecurity/IT2 assignments report'
        email_message.attach(MIMEText(msg_text, 'plain'))
        raw_string = base64.urlsafe_b64encode(email_message.as_bytes()).decode()

      #  send_message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
      #  print(send_message)