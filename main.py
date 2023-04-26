from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import auth
import db_func

app = FastAPI()


@app.post("/sign_up")
async def sign_up(position, first_name, surname, middle_name, login,
                  password, id_student: str = None,
                  institute: str = None,
                  direction: str = None, speciality: str = None, direction_military: str = None,
                  birth_date: str = None):
    if position != 'student':
        return auth.create_user(position, first_name, surname, middle_name, login,
                                password, id_student,
                                institute,
                                direction, speciality, direction_military, birth_date)
    elif None not in [position, first_name, surname, middle_name, login,
                      password, id_student,
                      institute,
                      direction, speciality, direction_military] and position == 'student':
        return auth.create_user(position, first_name, surname, middle_name, login,
                                password, id_student,
                                institute,
                                direction, speciality, direction_military, birth_date)
    else:
        return 'Students must fill all lines!'


@app.post("/sign_in")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_login = auth.token_user_db(form_data.username, form_data.password)
    if user_login == 'No such user':
        return 'No such user or password incorrect'

    return {"access_token": user_login, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: auth.User = Depends(auth.get_current_active_user)):
    return current_user


@app.get("/users/position")
async def read_users_me(current_user: auth.User = Depends(auth.get_current_user_position)):
    return current_user


@app.post("/student/parent")
async def parent_add(first_name, surname, middle_name, job, phone_number,
                     current_user_position: auth.User = Depends(auth.get_current_user_position),
                     current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'student':
        return db_func.add_parent(first_name, surname, middle_name, job, phone_number, current_user)
    else:
        return 'Callable only by students'


@app.post("/student/passport")
async def passport_add(number_passport, series_passport, issue_date, issued_by, subdivision_code,
                       current_user_position: auth.User = Depends(auth.get_current_user_position),
                       current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'student':
        return db_func.add_passport(number_passport, series_passport, issue_date, issued_by, subdivision_code,
                                    current_user)
    else:
        return 'Callable only by students'


@app.post("/student/military_doc")
async def military_doc_add(series_military, number_military, m_commissar, issue_date, doc_type,
                           current_user_position: auth.User = Depends(auth.get_current_user_position),
                           current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'student':
        return db_func.add_military_doc(series_military, number_military, m_commissar, issue_date, doc_type,
                                        current_user)
    else:
        return 'Callable only by students'


@app.post("/student/med_card")
async def med_card_add(decision, professional_category, id_category,
                       current_user_position: auth.User = Depends(auth.get_current_user_position),
                       current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'student':
        return db_func.add_med_card(decision, professional_category, id_category,
                                    current_user)
    else:
        return 'Callable only by students'


@app.post("/student/address")
async def address_add(address_type, post_address,
                      current_user_position: auth.User = Depends(auth.get_current_user_position),
                      current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'student':
        return db_func.add_address(address_type, post_address,
                                   current_user)
    else:
        return 'Callable only by students'


@app.post("/student/application")
async def application_add(
        current_user_position: auth.User = Depends(auth.get_current_user_position),
        current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'student':
        return db_func.add_application(
            current_user)
    else:
        return 'Callable only by students'


@app.post("/student/results")
async def results_select(
        current_user_position: auth.User = Depends(auth.get_current_user_position),
        current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'student':
        return db_func.select_results(current_user)
    else:
        return 'Callable only by students'


@app.post("/trainer/add")
async def training_add(id_student, value,
                       current_user_position: auth.User = Depends(auth.get_current_user_position),
                       current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'trainer':
        return db_func.add_training(id_student, value,
                                    current_user)
    else:
        return 'Callable only by trainers'


@app.post("/study_department/add")
async def education_add(id_student, value,
                        current_user_position: auth.User = Depends(auth.get_current_user_position),
                        current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'study_department':
        return db_func.add_grade(id_student, value,
                                 current_user)
    else:
        return 'Callable only by study_department'


@app.post("/secretary/ready_candidate")
async def ready_candidate_select(
        current_user_position: auth.User = Depends(auth.get_current_user_position),
        current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'secretary':
        return db_func.select_ready_candidate(
            current_user)
    else:
        return 'Callable only by secretary'


@app.post("/secretary/confirm_all_docs")
async def all_docs_confirm(id_student,
                           current_user_position: auth.User = Depends(auth.get_current_user_position),
                           current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position == 'secretary':
        return db_func.confirm_all_docs(id_student,
                                        current_user)
    else:
        return 'Callable only by secretary'


@app.get("/user/select")
async def table_select(table_name,
                       current_user_position: auth.User = Depends(auth.get_current_user_position),
                       current_user: auth.User = Depends(auth.get_current_active_user)):
    if current_user_position in ['study_department', 'trainer', 'secretary', 'student'] and \
            table_name in ['candidate', 'parent', 'passport', 'address', 'application', 'medical_card', 'military_doc']:
        return db_func.select_table(current_user, table_name)
    else:
        return 'You have no access'


