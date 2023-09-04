#!/bin/bash

# Remove the existing database file
rm -f planguin.db

# Create finance.db
code planguin.db

# Execute SQLite commands to create a new database
cat planguin.db.sql | sqlite3 planguin.db
