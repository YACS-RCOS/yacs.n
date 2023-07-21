Steps:

1. Open docker and go to the yacs_db container

2. Go to the terminal for the yacs_db container

3. Type in psql -d “database_name” -U “username” -W. Database and user name are both

“yacs”

4. Type in the posgtre password (“easy_dev_pass”)

5. Use \dt+ to give an in depth description of all the tables

6. Select * from “tablename” to check columns of the table ( you can also type column

names instead of * to see the entire column )

You can check the database name, username, and password in the inspect tab.



