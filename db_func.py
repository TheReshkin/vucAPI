import psycopg2
import config as c

from psycopg2.extensions import AsIs


# получение номера студента
def select_id_student(login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id_student FROM candidate WHERE login_candidate = %s;',
        [login])
    id_student = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return id_student


# Создание кандидата (передаются названия)
def create_student(id_student, first_name, surname, middle_name,
                   institute,
                   direction, speciality, direction_military, login_candidate,
                   password_candidate, birth_date):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    cursor.execute(
        'CALL create_student(%s, %s, %s, %s, find_institute(%s), find_direction(%s), find_speciality(%s),find_direction_military(%s), %s, %s, %s);',
        [id_student, first_name, surname, middle_name,
         institute,
         direction, speciality, direction_military, login_candidate,
         password_candidate, birth_date])
    conn.commit()
    cursor.close()
    conn.close()
    return 'Student created'


#   добавление родителя
def add_parent(first_name, surname, middle_name, job, phone_number, login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    id_student = select_id_student(login)
    role = login
    cursor.execute("""SET ROLE %s;
            INSERT INTO parent(first_name, surname, middle_name, job, phone_number, id_student) VALUES(%s, %s, %s, %s, %s, %s);""",
                   [role, first_name, surname, middle_name, job, phone_number, id_student])
    conn.commit()
    cursor.close()
    conn.close()
    return "Parent inserted"


#   добавление паспорта
def add_passport(number_passport, series_passport, issue_date, issued_by, subdivision_code, login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    id_student = select_id_student(login)
    role = login
    cursor.execute("""SET ROLE %s;
            INSERT INTO passport(number_passport, series_passport, issue_date, issued_by, subdivision_code, id_student) VALUES(%s, %s, %s, %s, %s, %s);""",
                   [role, number_passport, series_passport, issue_date, issued_by, subdivision_code, id_student])
    conn.commit()
    cursor.close()
    conn.close()
    return "Passport Inserted"


#   добавление военного билета
def add_military_doc(series_military, number_military, m_commissar, issue_date, doc_type, login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    id_student = select_id_student(login)
    role = login
    cursor.execute("""SET ROLE %s;
            INSERT INTO military_doc(series_military, number_military, m_commissar, issue_date, doc_type, id_student) VALUES(%s, %s, %s, %s, %s, %s);""",
                   [role, series_military, number_military, m_commissar, issue_date, doc_type, id_student])
    conn.commit()
    cursor.close()
    conn.close()
    return "military_doc Inserted"


#   добавление мед. карты
def add_med_card(decision, professional_category, id_category, login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    role = login
    id_student = select_id_student(login)
    cursor.execute("""SET ROLE %s;
            INSERT INTO medical_card(decision, professional_category, id_student, id_category) VALUES(%s, %s, %s, find_category_military(%s));""",
                   [role, decision, professional_category, id_student, id_category])
    conn.commit()
    cursor.close()
    conn.close()
    return "Medical Card Inserted"


#   добавление адреса (2 типа)
def add_address(address_type, post_address, login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    role = login
    id_student = select_id_student(login)
    cursor.execute("""SET ROLE %s;
            INSERT INTO address(address_type, post_address, id_student) VALUES(%s, %s, %s);""",
                   [role, address_type, post_address, id_student])
    conn.commit()
    cursor.close()
    conn.close()
    return "Address Inserted"


#   добавление заявления
def add_application(login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    role = login
    id_student = select_id_student(login)
    cursor.execute("""SET ROLE %s;
            INSERT INTO application(id_student) VALUES(%s);""",
                   [role, id_student])
    conn.commit()
    cursor.close()
    conn.close()
    return "Application Inserted"


#   просмотр своих результатов
def select_results(login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    response = []
    role = login
    cursor.execute("""SET ROLE %s;
            SELECT grade, physical_grade FROM get_my_results""",
                   [role])
    column_names = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        response.append(dict(zip(column_names, row)))
    cursor.close()
    conn.close()
    return response


# Создание работника (создание тренера, создание секретаря, учебного отдела)
def create_employee(first_name, surname, middle_name, position, login_employee,
                    password_employee):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)

    cursor = conn.cursor()
    cursor.execute(
        'CALL create_employee(%s, %s, %s, find_employee_pos(%s), %s, %s);',
        [first_name, surname, middle_name, position, login_employee,
         password_employee])
    conn.commit()
    cursor.close()
    conn.close()
    return 'Employee created'


#       Добавление физ. оценки
def add_training(id_student, value, login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    role = login
    cursor.execute("""SET ROLE %s;
            CALL add_training(%s, %s)""",
                   [role, id_student, value])
    conn.commit()
    cursor.close()
    conn.close()
    return "Training results added"


#       добавление оценки
def add_grade(id_student, value, login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    role = login
    cursor.execute("""SET ROLE %s;
            CALL add_grade(%s, %s)""",
                   [role, id_student, value])
    conn.commit()
    cursor.close()
    conn.close()
    return "Grade results added"


#       просмотр готовых кандидатов
def select_ready_candidate(login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    response = []
    role = login
    cursor.execute("""SET ROLE %s;
            SELECT id_student FROM get_ready_candidates""",
                   [role])
    column_names = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        response.append(dict(zip(column_names, row)))
    cursor.close()
    conn.close()
    return response


#       зачет всех документов (создание личного дела с отзывом роли)
def confirm_all_docs(id_student, login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    role = login
    cursor.execute("""SET ROLE %s;
            CALL confirm_all_docs(%s)""",
                   [role, id_student])
    # добавить проверку на наличие в student_file
    conn.commit()
    cursor.close()
    conn.close()
    return "All documents confirmed"


# создание файла студента, отзыв роли


def user_exist(login):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    role = login
    cursor.execute("""
            SELECT COUNT(*) FROM pg_roles WHERE rolname = %s""",
                   [role])
    count = cursor.fetchone()
    cursor.close()
    conn.close()
    if count[0] > 0:
        return True
    else:
        return False


def select_table(login, table_name):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    role = login
    response = []
    cursor.execute("""SET ROLE %s;
            SELECT * FROM %s""",
                   [role, AsIs(table_name)])

    column_names = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        response.append(dict(zip(column_names, row)))
    cursor.close()
    conn.close()
    return response



