from app.auth import connect_database



# Search Tutors - Profiles

def grab_all_tutors():

    connected = connect_database()
    users = connected.child("users").order_by_child("isTutor").equal_to(True).get()

    all_tutors = [dict(user.val()) for user in users.each()]


    return all_tutors


# Grab Sessions - By Date
