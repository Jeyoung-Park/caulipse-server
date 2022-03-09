import random
import uuid

user_number = 100
study_number = 10
comment_number = 100
noti_number = 20
notice_number = 10
study_user_number = 300
bookmark_number = 50

user_ids = [str(uuid.uuid4()) for i in range(user_number)]
study_ids = [str(uuid.uuid4()) for i in range(study_number)]
comment_ids = [str(uuid.uuid4()) for i in range(comment_number)]
noti_ids = [str(uuid.uuid4()) for i in range(noti_number)]
notice_ids = [str(uuid.uuid4()) for i in range(notice_number)]

weekday_enum = ['월', '화', '수', '목', '금', '토', '일']
frequency_enum = ['1회','주 2-4회','주 5회 이상']
location_enum = ['비대면','학교 스터디룸','중앙도서관','스터디카페','일반카페','흑석, 상도','서울대입구, 낙성대','기타']

def make_user_insert_statement(id, email, password, is_logout, token):
    return f'''INSERT INTO USER(ID, EMAIL, PASSWORD, IS_LOGOUT, TOKEN, ROLE) VALUES ('{id}', '{email}', '{password}', {is_logout}, '{token}', 'GUEST');\n'''

def make_user_profile_insert_statement(user_id, user_name, dept, grade, bio, user_about, show_dept, show_grade, on_break, link1, link2, short_user_about, user_interest_category):
    return f'''INSERT INTO USER_PROFILE(USER_ID, USER_NAME, DEPT, GRADE, BIO, USER_ABOUT, SHOW_DEPT, SHOW_GRADE, ON_BREAK, LINK1, LINK2, SHORT_USER_ABOUT, USER_INTEREST_CATEGORY)
VALUES('{user_id}', '{user_name}', '{dept}', '{grade}', '{bio}', '{user_about}', {show_dept}, {show_grade}, {on_break}, '{link1}', '{link2}', '{short_user_about}', '{user_interest_category}');\n'''

def make_study_insert_statement(id, title, study_about, weekday, frequency, location, capacity, members_count, vacancy, is_open, category_code, views, host_id):
    return f'''INSERT INTO STUDY(ID, TITLE, STUDY_ABOUT, WEEKDAY, FREQUENCY, LOCATION, CAPACITY, MEMBERS_COUNT, VACANCY, IS_OPEN, CATEGORY_CODE, VIEWS, HOST_ID)
VALUES('{id}', '{title}', '{study_about}', '{weekday}', '{frequency}', '{location}', '{capacity}', '{members_count}', '{vacancy}', '{is_open}', {category_code}, {views}, '{host_id}');\n'''

def make_studyuser_insert_statement(user_id, study_id, is_accepted, temp_bio):
    return f'''INSERT INTO STUDY_USER(USER_ID, STUDY_ID, IS_ACCEPTED, TEMP_BIO) VALUES('{user_id}', '{study_id}', {is_accepted}, '{temp_bio}');\n'''

def make_bookmark_insert_statement(user_id, study_id):
    return f'''INSERT INTO BOOKMARK(USER_ID, STUDY_ID) VALUES('{user_id}', '{study_id}');\n'''

def make_comment_insert_statement(id, user_id, study_id, content):
    return f'''INSERT INTO COMMENT(ID, NESTED_COMMENT_ID, USER_ID, STUDY_ID, IS_NESTED, CONTENT)
VALUES('{id}', NULL, '{user_id}', '{study_id}', 0, '{content}');\n'''

# reset script
with open('reset.sql', 'w') as f:
    f.write('DELETE FROM COMMENT;')
    f.write('DELETE FROM NOTICE;')
    f.write('DELETE FROM NOTIFICATION;')
    f.write('DELETE FROM BOOKMARK;')
    f.write('DELETE FROM STUDY_USER;')
    f.write('DELETE FROM STUDY;')
    f.write('DELETE FROM USER_PROFILE;')
    f.write('DELETE FROM USER_INTEREST_CATEGORY;')
    f.write('DELETE FROM USER_METOO_COMMENT;')
    f.write('DELETE FROM USER;')
    f.write('DELETE FROM CATEGORY;')
    f.write('INSERT INTO CATEGORY(CODE, MAIN, SUB) VALUES(100, \'프로그래밍\', \'c/c++\'), (101, \'프로그래밍\', \'자바스크립트\'), (200, \'어학\', \'토익\'), (201, \'어학\', \'토플\');')
    f.write('INSERT INTO USER(ID, EMAIL, PASSWORD, IS_LOGOUT, TOKEN, ROLE) \
        VALUES(\'28464dc7-7537-4b91-9d52-764b6de32122\', \'testadmin1@cau.ac.kr\', \'$2b$10$18n8DFDZ1QUrhBlf9CDr6O8LiN7cjIRAFX37HfK.SpnyJg1y7c.5K\', 0, \'\', \'ADMIN\'), \
        (\'9b083624-9475-4ad2-b5c0-eb40c98411c2\', \'testuser1@cau.ac.kr\', \'$2b$10$xtp6zwK8.0FqRrq4okZRXOcTkH9oCXhA8X02NJaAXgPockMw9ZFWi\', 0, \'\', \'USER\'), \
        (\'cd915b33-d4c3-4379-b5c1-fe8d389b0de7\', \'testguest1@cau.ac.kr\', \'$2b$10$f69XmMM3DPKDs91.6qgmOebP/bfrdKcCQNQG/ldl71GXet3BYBjEq\', 0, \'\', \'GUEST\'), \
        (\'dea61890-363d-4574-8ad1-ef1fa6fe66db\', \'testadmin2@cau.ac.kr\', \'$2b$10$jsUh3x5kvMfBECfEoiq15.hRnhtrVLRCid2d2r8tMQTtCa6ILNr/u\', 0, \'\', \'ADMIN\'), \
        (\'ec7283be-d2e5-4b39-b723-1cfa000a9303\', \'testuser2@cau.ac.kr\', \'$2b$10$Ls2oCM/bHbss5S18VyWgB.R2jet9xdATWFU8ZdNXZ3JR7PjAoXdwy\', 0, \'\', \'USER\'), \
        (\'492a437d-14ca-4e15-9347-0748ba14e269\', \'testguest2@cau.ac.kr\', \'$2b$10$sGJji6iVcZc/JJTq/cpFcukB3YXwUSbsygBFmKVJvw6QRmhpVPV0m\', 0, \'\', \'GUEST\');') # 테스트계정
    f.write('source userdata.sql;')
    f.write('source studydata.sql;')
    f.write('source userprofiledata.sql;')
    f.write('source studyuserdata.sql;')
    f.write('source bookmarkdata.sql;')
    f.write('source commentdata.sql;')
    f.write('source notificationdata.sql;')
    f.write('source noticedata.sql;')
    f.write('source userinterestcategorydata.sql;')
    f.write('source usermetoocommentdata.sql;')

# user table
with open('userdata.sql', 'w') as f:
    for i in range(user_number):
        stmt = make_user_insert_statement(user_ids[i], f'user{i}@test.com', f'password{i}', 0, f'token{i}')
        f.write(stmt)

# user_profile table
with open('userprofiledata.sql', 'w') as f:
    for i in range(user_number):
        stmt = make_user_profile_insert_statement(user_ids[i], f'user{i}', 'dept', 1, 'bio',
                f'user{i} about', 0, 0, 0, 'link1', 'link2', 'short_user_about', '101, 102')
        f.write(stmt)

# study table
with open('studydata.sql', 'w') as f:
    for i in range(study_number):
        capacity = random.randint(4, 10)
        members_count = random.randint(1, capacity)
        vacancy = capacity - members_count
        stmt = make_study_insert_statement(study_ids[i], f'study{i}', f'study{i}s content',
                weekday_enum[random.randint(0, len(weekday_enum) - 1)], frequency_enum[random.randint(0, len(frequency_enum) - 1)],
                location_enum[random.randint(0, len(location_enum) - 1)], random.randint(5, 10),
                capacity, members_count, vacancy, 101, 0, user_ids[i // study_number])
        f.write(stmt)

# study_user table
with open('studyuserdata.sql', 'w') as f:
    for i in range(study_user_number):
        user = random.randint(0, user_number - 1)
        study = random.randint(0, study_number - 1)
        stmt = make_studyuser_insert_statement(user_ids[user], study_ids[study],
                1 if random.randint(0, 10) > 7 else 1, f'temp bio for user {user_ids[user]}')
        f.write(stmt)

# bookmark table
with open('bookmarkdata.sql', 'w') as f:
    for i in range(bookmark_number):
        user = random.randint(0, user_number - 1)
        study = random.randint(0, study_number - 1)
        stmt = make_bookmark_insert_statement(user_ids[user], study_ids[study])
        f.write(stmt)

# comment table
with open('commentdata.sql', 'w') as f:
    for i in range(comment_number):
        stmt = make_comment_insert_statement(comment_ids[i],
                user_ids[i], study_ids[i // study_number], f'comment content {i}')
        f.write(stmt)

# user_interest_category table
with open('userinterestcategorydata.sql', 'w') as f:
    stmt = f'''INSERT INTO USER_INTEREST_CATEGORY(USER_ID, CATEGORY_CODE)
VALUES ('{user_ids[0]}', 100), ('{user_ids[0]}', 101), ('{user_ids[1]}', 100), ('{user_ids[2]}', 200);'''
    f.write(stmt)

# notification table
with open('notificationdata.sql', 'w') as f:
    for i in range(noti_number):
        stmt = f'''INSERT INTO NOTIFICATION(ID, USER_ID, STUDY_ID, TYPE, `READ`)
VALUES ('{noti_ids[i]}', '{user_ids[i // 5]}', '{study_ids[i // 5]}', 0, 0);'''
        f.write(stmt)

# notice table
with open('noticedata.sql', 'w') as f:
    f.write('INSERT INTO NOTICE(ID, TITLE, ABOUT, VIEWS, HOST_ID) VALUES\n')
    for i in range(notice_number - 1):
        stmt = f'''('{notice_ids[i]}', 'NOTICE_TITLE {i}', 'NOTICE_ABOUT {i}', 0, '{user_ids[i // 10]}'),\n'''
        f.write(stmt)
    f.write(f'''('{notice_ids[notice_number - 1]}', 'NOTICE_TITLE {notice_number - 1}', 'NOTICE_ABOUT {notice_number - 1}', 0, '{user_ids[notice_number - 1 // 10]}');''')

# user_metoo_comment table
with open('usermetoocommentdata.sql', 'w') as f:
    for i in range(noti_number): # comment_number > noti_number
        stmt = f'''INSERT INTO USER_METOO_COMMENT(USER_ID, COMMENT_ID)
VALUES('{user_ids[i // (user_number // comment_number)]}', '{comment_ids[i]}');'''
        f.write(stmt)
