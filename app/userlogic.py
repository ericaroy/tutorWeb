from app.auth import connect_database

#cache

# Search Tutors - Profiles

def grab_all_tutors():

    connected = connect_database()
    users = connected.child("users").order_by_child("isTutor").equal_to(True).get()

    all_tutors = [dict(user.val()) for user in users.each()]

    return all_tutors

# Filter Program from All Tutors


def grab_tutor_applications():
    connected = connect_database()
    applications = connected.child("tutorapplications").order_by_child("approved").equal_to(False).get()

    all_applications = [dict(user.val()) for user in applications.each()]

    return all_applications


# Add Courses to My Profile
def add_course_to_profile():
    pass

def add_session():
    pass


#Approve Tutors from my Profile as Admin


# Add new sessions


# Grab all sessions from all departments
