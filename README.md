# Introduction
[![Build Status](https://travis-ci.com/ahmedemad3965/UNotes.svg??branch=master)](https://travis-ci.com/ahmedemad3965/UNotes)

This is a RESTful **API** for a **Notes Taking app**.
The **API** is designed using **Django** and **Postgres** database.
The Project is completely done and fully documented.
The Project is **open-source** and not used commercially be any means.
The **API** is fully tested with **100% Code coverage** with automated **tests** in a separate folder.
The **docker** and **docker-compose** images configuration files are stored with in the project so that you can use it and test it from anywhere with no problems.
You can freely use, edit and learn from this project.

# Documentation

**Firstly we Create a new user profile:**

    POST www.unotes.com/users/signup/
    
    {
        "username": "my_user_name",
        "first_name": "test",
        "last_name": "account",
        "password": "my_super_secret_password"
    }

* note: 
    1. the url domain names used in this docs are NOT real and used only for demonstration.
    2. you can add another field "profile_photo", but the request format will be multipart/form-data.



**For retrieving, updating or deleting your profile, you can use:**

    GET, PUT, PATCH, DELETE www.unotes.com/users/me/


**And For Logging in you can use:**

    POST www.unotes.com/users/login/

    {
        "username": "my_user_name",
        "password": "my_super_secret_password"
    }


**And similarly for logging out you use:**

    POST www.unotes.com/users/logout/

* no data in the request body.


**Now we have created a user account, we can start by adding new NoteBooks:**

    POST www.unotes.com/notebooks/
    
    {
        "title": "my first notebook"
    }

**To List all NoteBooks the user has, we use:**

    GET www.unotes.com/notebooks/


* note: 
   1. every user can have many notebooks, and each notebook can contain many notes.

**To Update a certain NoteBook:**

    PUT www.unotes.com/notebooks/{notebook_slug}/

    {
        "title": "my updated notebook"
    }

**And likewise for deleting a NoteBook:**

    DELETE www.unotes.com/notebooks/{notebook_slug}/


**After We Created a NoteBook, we can add new notes as follows:**

    POST www.unotes.com/notebooks/{notebook_slug}/notes/
    
    {
        "title": "my first note",
        "text": "my first note description"
    }

**To List all notes the user has in a NoteBook, we use:**

    GET www.unotes.com/notebooks/{notebook_slug}/notes/


**To Update a certain note:**

    PUT, PATCH www.unotes.com/notebooks/{notebook_slug}/notes/{note_slug}/

    {
        "title": "my updated note",
        "text": "my updated note text"
    }


**And likewise for retrieving and deleting a certain note:**

    GET, DELETE www.unotes.com/notebooks/{notebook_slug}/notes/{note_slug}/

**A User might want to add an attachment to a note, For this you can do:**

    POST www.unotes.com/notebooks/{notebook_slug}/notes/{note_slug}/attachments/

**And if the user wants to delete the attachment, he can use:**
    
    DELETE www.unotes.com/notebooks/{notebook_slug}/notes/{note_slug}/attachments/{attachment_slug}

* note: 
    1. the uploaded file can be of any format, the file can't be any larger than 2 MB.
    2. the request body must contain a field called "file" which contains the attachment's file, the request format must be multipart/form-data.
