#!/bin/bash

# Remove the existing database file
rm -f finance.db

# Create finance.db
code finance.db

# Execute SQLite commands to create a new database
cat finance.db.sql | sqlite3 finance.db
