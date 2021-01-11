# Set up React  
0. `cd ~/environment && git clone https://https://github.com/NJIT-CS490/project2-m1-cl678 && cd project2-m1-cl678`
1. Install your stuff!    
  a) `npm install`    
  b) `pip install flask-socketio`    
  c) `pip install eventlet`    
  d) `npm install -g webpack`    
  e) `npm install --save-dev webpack`    
  f) `npm install socket.io-client --save`    
:warning: :warning: :warning: If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install` :warning: :warning: :warning:    
2. If you already have psql set up, **SKIP THE REST OF THE STEPS AND JUST DO THE FOLLOWING COMMAND**:   
`sudo service postgresql start`    
3. Copy your `sql.env` file into your new directory. Create your 'sql.env'
  
# Getting PSQL to work with Python  
  
1. Update yum: `sudo yum update`, and enter yes to all prompts    
2. Upgrade pip: `sudo /usr/local/bin/pip install --upgrade pip`  
3. Get psycopg2: `sudo /usr/local/bin/pip install psycopg2-binary`    
4. Get SQLAlchemy: `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`    
  
# Setting up PSQL  
  
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`    
    Enter yes to all prompts.    
2. Initialize PSQL database: `sudo service postgresql initdb`    
3. Start PSQL: `sudo service postgresql start`    
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER`    
    :warning: :warning: :warning: If you get an error saying "could not change directory", that's okay! It worked! :warning: :warning: :warning:    
5. Make a new database: `sudo -u postgres createdb $USER`    
        :warning: :warning: :warning: If you get an error saying "could not change directory", that's okay! It worked! :warning: :warning: :warning:    
6. Make sure your user shows up:    
    a) `psql`    
    b) `\du` look for ec2-user as a user    
    c) `\l` look for ec2-user as a database    
7. Make a new user:    
    a) `psql` (if you already quit out of psql)    
    ## REPLACE THE [VALUES] IN THIS COMMAND! Type this with a new (short) unique password.   
    b) I recommend 4-5 characters - it doesn't have to be very secure. Remember this password!  
        `create user [some_username_here] superuser password '[some_unique_new_password_here]';`    
    c) `\q` to quit out of sql    
8. `cd` into `lect11` and make a new file called `sql.env` and add `SQL_USER=` and `SQL_PASSWORD=` in it  
9. Fill in those values with the values you put in 7.b)
10 Add the following lines:
a) SQL_USER='<user>' where creating the user
   SQL_PASSWORD='<pass>' where creating the password
b)'postgresql://<user>:<pass>@localhost/postgres' where user and pass are the value is created.
  
  
# Enabling read/write from SQLAlchemy  
There's a special file that you need to enable your db admin password to work for:  
1. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
2. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
3. After changing those lines, run `sudo service postgresql restart`  
4. Ensure that `sql.env` has the username/password of the superuser you created!  
5. Run your code!    
  a) `npm run watch`. If prompted to install webpack-cli, type "yes"    
  b) In a new terminal, `python app.py`    
  c) Preview Running Application (might have to clear your cache by doing a hard refresh) 
  
# Deloying Heroku and pushing the database
1. Log into Heroku: 'heroku login -i'
2. Create heroku app: 'heroku create'
3. Create heroku postgresql: 'heroku addons:create heroku-postgresql:hobby-dev'
4. Enter 'ALTER DATABASE postgres OWNER TO <user>
5. Push local database to Heroku: 'PGUSER= <user> heroku pg:push postgres DATABASE_URL'
6. Check if it worked: 'heroku pg: psql' and 'SELECT * FROM messages'
7. Configure your PROCIFILE and requirements.txt
8. Push your app to heroku: 'git push heroku master'

# ISSUES
1. First, where I get lect11 the length of the size was too small which allows up to 120 char, but I changed to up to 1000 chars. So that I can write the long sentences that there would be no errors
2. Technical issue was pushing database to heroku. sqlalchemy.exc. Programming Error. I tried several times to pg: push, it would not work. So I try to redo it create heroku postgresql, push local database to Heroku. And make sure clean cookies and cache website server.
3. Technical issue was having the current user to update automatically someone connected or disconnected.
4. Technical issue was putting user names be displayed under the messages.
5. Technical issue was GOOGLE Button clientID does not activate in my developer google website. I changed to other gmail that I'm able to create "External"
6. Technical issue was to redirect to . I figured it out that I had to add a ReactDOM.render to call GOOGLEButton.jsx.

# Improvements
1. First, I was hard to display the commands of using bot chat api where I get https://rapidapi.com/ and funtranslate
2. second, I was unaware of using db.session.add,commit, and rollback, the way I figure it out I searched the google with specific explanations.
3. I'm getting improved to create the GOOGLE login page seperately with adding funcationality to the chatbot.
4. I tried to figure out how to render chatbot images inlines.
5. I need more styling for user messages and chatbot messages.
