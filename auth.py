from pydantic import BaseModel
from typing import Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import psycopg2
import config as c
import db_func

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sign_in")

users = {
    "pupochek": {
        "username": "pupochek",
        "token": "pupochek",
        "position": "student"
    },
    "secretary2": {
        "username": "secretary2",
        "token": "secretary2",
        "position": "secretary"
    }, 'study_department2': {
        'username': 'study_department2',
        'token': 'study_department2',
        'position': 'study_department'},
    'trainer2': {
        'username': 'trainer2',
        'token': 'trainer2',
        'position': 'trainer'}
}


class User(BaseModel):
    username: str
    token: str
    position: str


async def get_current_user(token: str = Depends(oauth2_scheme)):
    for login, body in users.items():
        print(login, body)
        if body["token"] == token:
            return login

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user_position(token: str = Depends(oauth2_scheme)):
    print(users)
    return users[token]["position"]


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


def create_user(position, first_name, surname, middle_name, login,
                password, id_student,
                institute,
                direction, speciality, direction_military, birth_date):
    if position == 'student' and db_func.user_exist(login) is False:
        db_func.create_student(id_student, first_name, surname, middle_name,
                               institute,
                               direction, speciality, direction_military, login,
                               password, birth_date)
        return "student created"
    elif position in ['study_department', 'trainer', 'secretary'] and db_func.user_exist(login) is False:
        db_func.create_employee(first_name, surname, middle_name, position, login,
                                password)
        return position + " user created"
    elif db_func.user_exist(login):
        return "User exist"
    else:
        return "There is no such position: " + position


def token_user_db(login, password):
    conn = psycopg2.connect(dbname=c.db, user=c.user,
                            password=c.password, host=c.host)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT login_candidate FROM candidate WHERE login_candidate = %s AND password_candidate = crypt(%s,password_candidate);',
        [login, password])
    login_candidate = cursor.fetchone()

    cursor.execute(
        'SELECT login_employee FROM employee WHERE login_employee = %s AND password_employee = crypt(%s, password_employee);',
        [login, password])
    login_employee = cursor.fetchone()
    print(login_candidate)
    print(login_employee)
    if login_candidate is not None:
        users[login] = {"username": login,
                        "token": login,
                        "position": "student"}
        print(users)

        cursor.close()
        conn.close()
        return login_candidate
    elif login_employee is not None:
        print('employee')
        cursor.execute(
            'SELECT name_position FROM classifier_employee WHERE id_position = (SELECT id_position FROM employee WHERE login_employee = %s);',
            [login])
        position = cursor.fetchone()
        print(position)
        users[login] = {"username": login,
                        "token": login,
                        "position": position[0]}
        print(users)
        cursor.close()
        conn.close()
        return login_employee
    else:

        cursor.close()
        conn.close()
        return 'No such user'
