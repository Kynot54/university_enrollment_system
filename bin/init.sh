#!/bin/sh
sqlite3 ./var/db/users/primary/fuse/database.db < ./share/users/users.sql
sqlite3 ./var/db/users/primary/fuse/database.db < ./share/users/roles.sql
sqlite3 ./var/db/users/primary/fuse/database.db < ./share/users/userRoles.sql

python3 ./share/enrollment/classes.py
python3 ./share/enrollment/enrollments.py
python3 ./share/enrollment/instructors.py
python3 ./share/enrollment/registrar.py
python3 ./share/enrollment/sections.py
python3 ./share/enrollment/students.py
python3 ./share/enrollment/enrollment_count.py