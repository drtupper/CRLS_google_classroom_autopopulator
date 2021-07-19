def read_quarter_info(p_filename):
    import configparser
    import datetime
    config = configparser.ConfigParser()
    config.read(p_filename)

    if 'QUARTERS' in config:
        quarters = config['QUARTERS']
        q1 = quarters['q1']
        q2 = quarters['q2']
        q3 = quarters['q3']
        q4 = quarters['q4']
        summer = quarters['summer']
    else:
        raise ValueError("Need to have a file called: " + str(p_filename) + "\n"
                         "This file needs to have a QUARTERS section with variables q1, q2, q3, and q4")

    q1_list = q1.split('/')
    q1 = datetime.datetime(int(q1_list[0]), int(q1_list[1]), int(q1_list[2]))
    q2_list = q2.split('/')
    q2 = datetime.datetime(int(q2_list[0]), int(q2_list[1]), int(q2_list[2]))
    q3_list = q3.split('/')
    q3 = datetime.datetime(int(q3_list[0]), int(q3_list[1]), int(q3_list[2]))
    q4_list = q4.split('/')
    q4 = datetime.datetime(int(q4_list[0]), int(q4_list[1]), int(q4_list[2]))
    summer_list = summer.split('/')
    summer = datetime.datetime(int(summer_list[0]), int(summer_list[1]), int(summer_list[2]))

    return [q1, q2, q3, q4, summer]


def read_classes_info(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)

    p_all_classes = {}

    if 'DEFAULT' in config:
        gc1 = config.get('DEFAULT', 'gc_class1', fallback='')
        gc2 = config.get('DEFAULT', 'gc_class2', fallback='')
        gc3 = config.get('DEFAULT', 'gc_class3', fallback='')
        gc4 = config.get('DEFAULT', 'gc_class4', fallback='')
        gc5 = config.get('DEFAULT', 'gc_class5', fallback='')
        gc6 = config.get('DEFAULT', 'gc_class6', fallback='')
        gc7 = config.get('DEFAULT', 'gc_class7', fallback='')
        gc8 = config.get('DEFAULT', 'gc_class8', fallback='')
    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a DEFAULT section with variables gc_class1, and so on")

    if 'DEFAULT' in config:
        aspen1 = config.get('DEFAULT', 'aspen_class1', fallback='')
        aspen2 = config.get('DEFAULT', 'aspen_class2', fallback='')
        aspen3 = config.get('DEFAULT', 'aspen_class3', fallback='')
        aspen4 = config.get('DEFAULT', 'aspen_class4', fallback='')
        aspen5 = config.get('DEFAULT', 'aspen_class5', fallback='')
        aspen6 = config.get('DEFAULT', 'aspen_class6', fallback='')
        aspen7 = config.get('DEFAULT', 'aspen_class7', fallback='')
        aspen8 = config.get('DEFAULT', 'aspen_class8', fallback='')
    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a DEFAULT section with variables aspen1, and so on")

    if gc1 and aspen1:
        p_all_classes[gc1] = aspen1
    if gc2 and aspen2:
        p_all_classes[gc2] = aspen2
    if gc3 and aspen3:
        p_all_classes[gc3] = aspen3
    if gc4 and aspen4:
        p_all_classes[gc4] = aspen4
    if gc5 and aspen5:
        p_all_classes[gc5] = aspen5
    if gc6 and aspen6:
        p_all_classes[gc6] = aspen6
    if gc7 and aspen7:
        p_all_classes[gc7] = aspen6
    if gc8 and aspen8:
        p_all_classes[gc8] = aspen6

    return p_all_classes


def read_mailer_info(p_filename):
    import configparser
    config = configparser.ConfigParser()
    config.read(p_filename)

    if 'MAILER' in config:
        p_send_email = config.getboolean('MAILER', 'send_email', fallback=False)
        p_mailclass1 = config.get('MAILER', 'mailclass1', fallback='')
        p_mailclass2 = config.get('MAILER', 'mailclass2', fallback='')
        p_mailclass3 = config.get('MAILER', 'mailclass3', fallback='')
        p_mailclass4 = config.get('MAILER', 'mailclass4', fallback='')
        p_mailclass5 = config.get('MAILER', 'mailclass5', fallback='')
        p_mailclass6 = config.get('MAILER', 'mailclass6', fallback='')
        p_mailclass7 = config.get('MAILER', 'mailclass7', fallback='')
        p_mailclass8 = config.get('MAILER', 'mailclass8', fallback='')
        p_teachercc1 = config.get('MAILER', 'teachercc1', fallback='')
        p_teachercc2 = config.get('MAILER', 'teachercc2', fallback='')
        p_teachercc3 = config.get('MAILER', 'teachercc3', fallback='')
        p_teachercc4 = config.get('MAILER', 'teachercc4', fallback='')
        p_teachercc5 = config.get('MAILER', 'teachercc5', fallback='')
        p_teachercc6 = config.get('MAILER', 'teachercc6', fallback='')
        p_teachercc7 = config.get('MAILER', 'teachercc7', fallback='')
        p_teachercc8 = config.get('MAILER', 'teachercc8', fallback='')
        p_message1 = config.get('MAILER', 'message1', fallback='')
        p_message2 = config.get('MAILER', 'message2', fallback='')
        p_message3 = config.get('MAILER', 'message3', fallback='')
        p_message4 = config.get('MAILER', 'message4', fallback='')
        p_message5 = config.get('MAILER', 'message5', fallback='')
        p_message6 = config.get('MAILER', 'message6', fallback='')
        p_message7 = config.get('MAILER', 'message7', fallback='')
        p_message8 = config.get('MAILER', 'message8', fallback='')
        p_student1 = config.get('MAILER', 'email1', fallback='')
        p_student2 = config.get('MAILER', 'email2', fallback='')
        p_student3 = config.get('MAILER', 'email3', fallback='')
        p_student4 = config.get('MAILER', 'email4', fallback='')
        p_student5 = config.get('MAILER', 'email5', fallback='')
        p_student6 = config.get('MAILER', 'email6', fallback='')

        p_guardian1 = config.get('MAILER', 'guardian1', fallback='')
        p_guardian2 = config.get('MAILER', 'guardian2', fallback='')
        p_guardian3 = config.get('MAILER', 'guardian3', fallback='')
        p_guardian4 = config.get('MAILER', 'guardian4', fallback='')
        p_guardian5 = config.get('MAILER', 'guardian5', fallback='')
        p_guardian6 = config.get('MAILER', 'guardian6', fallback='')
    else:
        raise ValueError("Need to have a file called: " +
                         str(p_filename) +
                         "\nThis file needs to have a "
                         "MAILER section with variables mailclass1, send_email, etc...")

    p_mailclasses= [p_mailclass1, p_mailclass2, p_mailclass3, p_mailclass4, p_mailclass5, p_mailclass6, p_mailclass7,
                    p_mailclass8]
    p_teachercc = [p_teachercc1, p_teachercc2, p_teachercc3, p_teachercc4, p_teachercc5, p_teachercc6,
                  p_teachercc7, p_teachercc8]
    p_messages = [p_message1, p_message2, p_message3, p_message4, p_message5, p_message6, p_message7, p_message8]
    p_student_cc = {p_student1: p_guardian1, p_student2: p_guardian2, p_student3: p_guardian3, p_student4: p_guardian4,
                    p_student5: p_guardian5, p_student6: p_guardian6}

    return [p_mailclasses, p_teachercc, p_messages, p_student_cc, p_send_email, ]
