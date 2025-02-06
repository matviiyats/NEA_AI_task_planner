# importing all the necessary libraries
import PySimpleGUI as sg
import random
import mysql.connector
import schedule
import time
from datetime import datetime
import hashlib
import threading
from openai import OpenAI
from win11toast import toast
import textwrap
import dotenv
import os

#base64 strings for the button switch images
switch_button_off = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAED0lEQVRYCe1WTWwbRRR+M/vnv9hO7BjHpElMKSlpqBp6gRNHxAFVcKM3qgohQSqoqhQ45YAILUUVDRxAor2VAweohMSBG5ciodJUSVqa/iikaePEP4nj2Ovdnd1l3qqJksZGXscVPaylt7Oe/d6bb9/svO8BeD8vA14GvAx4GXiiM0DqsXv3xBcJU5IO+RXpLQvs5yzTijBmhurh3cyLorBGBVokQG9qVe0HgwiXLowdy9aKsY3g8PA5xYiQEUrsk93JTtjd1x3siIZBkSWQudUK4nZO1w3QuOWXV+HuP/fL85klAJuMCUX7zPj4MW1zvC0Ej4yMp/w++K2rM9b70sHBYCjo34x9bPelsgp/XJksZ7KFuwZjr3732YcL64ttEDw6cq5bVuCvgy/sje7rT0sI8PtkSHSEIRIKgCQKOAUGM6G4VoGlwiqoVd2Za9Vl8u87bGJqpqBqZOj86eEHGNch+M7otwHJNq4NDexJD+59RiCEQG8qzslFgN8ibpvZNsBifgXmFvJg459tiOYmOElzYvr2bbmkD509e1ylGEZk1Y+Ssfan18n1p7vgqVh9cuiDxJPxKPT3dfGXcN4Tp3dsg/27hUQs0qMGpRMYjLz38dcxS7Dm3nztlUAb38p0d4JnLozPGrbFfBFm79c8hA3H2AxcXSvDz7/+XtZE1kMN23hjV7LTRnKBh9/cZnAj94mOCOD32gi2EUw4FIRUMm6LGhyiik86nO5NBdGRpxYH14bbjYfJteN/OKR7UiFZVg5T27QHYu0RBxoONV9W8KQ7QVp0iXdE8fANUGZa0QAvfhhXlkQcmjJZbt631oIBnwKmacYoEJvwiuFgWncWnXAtuVBBEAoVVXWCaQZzxmYuut68b631KmoVBEHMUUrJjQLXRAQVSxUcmrKVHfjWWjC3XOT1FW5QrWpc5IJdQhDKVzOigEqS5dKHMVplnNOqrmsXqUSkn+YzWaHE9RW1FeXL7SKZXBFUrXW6jIV6YTEvMAUu0W/G3kcxPXP5ylQZs4fa6marcWvvZfJu36kuHjlc/nMSuXz+/ejxgqPFpuQ/xVude9eu39Jxu27OLvBGoMjrUN04zrNMbgVmOBZ96iPdPZmYntH5Ls76KuxL9NyoLA/brav7n382emDfHqeooXyhQmARVhSnAwNNMx5bu3V1+habun5nWdXhwJZ2C5mirTesyUR738sv7g88UQ0rEkTDlp+1wwe8Pf0klegUenYlgyg7bby75jUTITs2rhCAXXQ2vwxz84vlB0tZ0wL4NEcLX/04OrrltG1s8aOrHhk51SaK0us+n/K2xexBxljcsm1n6x/Fuv1PCWGiKOaoQCY1Vb9gWPov50+fdEqd21ge3suAlwEvA14G/ucM/AuppqNllLGPKwAAAABJRU5ErkJggg=='
switch_button_on = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAD+UlEQVRYCe1XzW8bVRCffbvrtbP+2NhOD7GzLm1VoZaPhvwDnKBUKlVyqAQ3/gAkDlWgPeVQEUCtEOIP4AaHSI0CqBWCQyXOdQuRaEFOk3g3IMWO46+tvZ+PeZs6apq4ipON1MNafrvreTPzfvub92bGAOEnZCBkIGQgZOClZoDrh25y5pdjruleEiX+A+rCaQo05bpuvJ/+IHJCSJtwpAHA/e269g8W5RbuzF6o7OVjF8D3Pr4tSSkyjcqfptPDMDKSleW4DKIggIAD5Yf+Oo4DNg6jbUBlvWLUNutAwZu1GnDjzrcXzGcX2AHw/emFUV6Sfk0pqcKpEydkKSo9q3tkz91uF5aWlo1Gs/mYc+i7tz4//19vsW2AU9O381TiioVCQcnlRsWeQhD3bJyH1/MiFLICyBHiuzQsD1arDvypW7DR9nzZmq47q2W95prm+I9fXfqXCX2AF2d+GhI98Y8xVX0lnxvl2UQQg0csb78ag3NjEeD8lXZ7pRTgftmCu4864OGzrq+5ZU0rCa3m+NzXlzvoAoB3+M+SyWQuaHBTEzKMq/3BMbgM+FuFCDBd9kK5XI5PJBKqLSev+POTV29lKB8rT0yMD0WjUSYLZLxzNgZvIHODOHuATP72Vwc6nQ4Uiw8MUeBU4nHS5HA6TYMEl02wPRcZBJuv+ya+UCZOIBaLwfCwQi1Mc4QXhA+PjWRkXyOgC1uIhW5Qd8yG2TK7kSweLcRGKKVnMNExWWBDTQsH9qVmtmzjiThQDs4Qz/OUSGTwcLwIQTLW58i+yOjpXDLqn1tgmDzXzRCk9eDenjo9yhvBmlizrB3V5dDrNTuY0A7opdndStqmaQLPC1WCGfShYRgHdLe32UrV3ntiH9LliuNrsToNlD4kruN8v75eafnSgC6Luo2+B3fGKskilj5muV6pNhk2Qqg5v7lZ51nBZhNBjGrbxfI1+La5t2JCzfD8RF1HTBGJXyDzs1MblONulEqPDVYXgwDIfNx91IUVbAbY837GMur+/k/XZ75UWmJ77ou5mfM1/0x7vP1ls9XQdF2z9uNsPzosXPNFA5m0/EX72TBSiqsWzN8z/GZB08pWq9VeEZ+0bjKb7RTD2i1P4u6r+bwypo5tZUumEcDAmuC3W8ezIqSGfE6g/sTd1W5p5bKjaWubrmWd29Fu9TD0GlYlmTx+8tTJoZeqYe2BZC1/JEU+wQR5TVEUPptJy3Fs+Vkzgf8lemqHumP1AnYoMZSwsVEz6o26i/G9Lgitb+ZmLu/YZtshfn5FZDPBCcJFQRQ+8ih9DctOFvdLIKHH6uUQnq9yhFu0bec7znZ+xpAGmuqef5/wd8hAyEDIQMjAETHwP7nQl2WnYk4yAAAAAElFTkSuQmCC'
sg.set_options(font=("Arial Bold", 16)) #setting all objects/texts in overall program to be big enough for comfortable use

dotenv.load_dotenv() #loading environment from .env file

def setDatabase(): #subroutine to set MySQL database password
  layout = [[sg.Text("Input password to your MySQL database"), sg.InputText("", key = "MYSQLPASS")], #defining our window layout
    [sg.Push(), sg.Button("Set MySQL password", key="SETMYSQLPASS", button_color="green")]
    ]
  window = sg.Window("Input your database pass", layout)  # defining our GUI window and its title
  while True:
   event,values = window.read()
   if event == sg.WIN_CLOSED: #stop outputting the window if closed
      break
   if event == "SETMYSQLPASS": #if button to change pressed
     try:
       mysqlpass = values["MYSQLPASS"] #getting user's input
       dotenv_file = dotenv.find_dotenv() #getting location of .env file
       dotenv.set_key(dotenv_file, "DATABASE_PASS", mysqlpass) #setting new database password in the .env file
       window.close()
       return mysqlpass
     except Exception as e: #if error occurred, output warning
       sg.popup_error(f"The error occurred while trying to set .env file. Try to edit the file manually with the Windows notepad. Exception - {e}")
  window.close()

def hash256(stringtohash): #subroutine, that encodes string (taken as a parameter) into a sha256 hash
  hash_object = hashlib.sha256(stringtohash.encode())
  result = hash_object.hexdigest()
  return result

def userGreeting(): #subroutine to get a greeting for the user
  now = datetime.now() #getting current time from user's computer
  current_time = now.strftime("%H") #deducing only current hour in 24 hours format
  current_time = int(current_time) #converting to integer
  #bunch of if statements to determine a proper greeting, relevant to a time parsed from computer
  if current_time >= 17:
    greeting = "Good evening"
  elif current_time >= 12 and current_time < 17:
    greeting = "Good afternoon"
  elif current_time >= 6 and current_time < 12:
    greeting = "Good morning"
  else:
    greeting = "Good night"
  return greeting

def interactiveButton(window, event, variable): # Subroutine, that defines interactive switch with three parameters: window (to define the window in which it's used),
    # event (how the button will be called), and variable (a variable to be updated).
  event.metadata = not event.metadata # Toggle the metadata of the event. If metadata is True, set it to False; if False, set it to True.
  event.update(image_data=switch_button_on if event.metadata else switch_button_off) # Update the image of the button based on the current state of metadata

  if event.metadata: #Update the variable based on the current state of metadata.
    variable = True
  else:
    variable = False

  return variable #Returning updated variable

def dbcheck(): #function to check whether database and all compulsory components are created and running
  try:
    try:
      database_pass = os.getenv("DATABASE_PASS")
      db = mysql.connector.connect( #piece of code initialising connection to MySQL databases
        host = "localhost",
        user = "root",
        passwd = database_pass
    )
    except Exception as e:
      sg.popup_error(f"Ensure, that MySQL database is running locally. If it's your first program launch or your MySQL password changed, please change it in the next window. Exception - {e}", title="Unable to establish connection to database!")
      database_pass = setDatabase()
    try:
      db = mysql.connector.connect(  # piece of code initialising connection and checking whether particular database exists
        host="localhost",
        user="root",
        passwd=database_pass,
        database="USERS")
    except:
      mycursor = db.cursor() #initialise database cursor
      mycursor.execute("CREATE DATABASE USERS")
    try: #checking whether necessary table users is created
      mycursor = db.cursor()
      mycursor.execute("CREATE TABLE Users(UserID INTEGER(100), Login VARCHAR(250), Password VARCHAR(1500), Salt INTEGER(100), Authorised BOOL, PRIMARY KEY (UserID))") #creating table with necessary columns
      return db
    except:
      return db
  except:
    sg.popup_error("Unable to check integrity of database!", title = "Unable to check database")
def usercheck(): #subroutine that traverses database in search of previously authorised users
  try:
    authQuery = "SELECT Login, UserID FROM users WHERE Authorised=True"
    mycursor.execute(authQuery)
    authResults = mycursor.fetchall()
    if not authResults: #if no results found, continue to choice of options register/login
      return authentication()
    else: #else load saved session
      login = authResults[0][0]
      userID = authResults[0][1]
      return main(login, userID)
  except Exception as e: #if error occurred, warn user and provide him with error
    sg.popup_error(f"Possible problem with database access! The following error occurred {e}")
db = dbcheck() #initialise default database to use all over all subroutines
mycursor = db.cursor() #global to use all over all subroutines
def checkfornumbers(string): # subroutine to check if there any numbers in given string
  for char in string:
    if char.isnumeric(): #returns True if there's a number in the string
      return True
    else:
      continue

def complexitycheck(string): # subroutine to check if given string is complex (contains numbers and special characters)
  special_characters = "!@#$%^&*()-+?_=,<>/"""  # string with special characters
  special_char = bool(any(letter in special_characters for letter in string)) # Boolean check on special characters
  conditions = (special_char, checkfornumbers(string)) # tuple with conditions to consider string complex
  if all(conditions) is True: #if all conditions are met
    return True


def splitWithAI(task, apikey): #subroutine that makes a request to OpenAI API to split one provided task into few subtasks
  client = OpenAI( #defining our request body
    api_key=apikey, #setting our api key
  )

  chat_completion = client.chat.completions.create(
    messages=[ #setting the message to send to AI model
      {
        "role": "user",
        "content": f"Split the task {task} into a sub-tasks to complete. No more than 5 concise sub-tasks.",
      }
    ],
    model="gpt-3.5-turbo",
    temperature=0 #maximum response precision set
  )
  subtasks = chat_completion.choices[0].message.content.strip() #getting the AI model response and returning it back
  return subtasks

def registration():
  layout = [ #laying out input fields and buttons for GUI
    [sg.Text("Set your login"), sg.Push(), sg.InputText(key="setlogin")],
    [sg.Text("Set your password"), sg.InputText(key="setpass", password_char="*")],
    [sg.Text("Save session?"),
      sg.Button(image_data=switch_button_off, key='-TOGGLE-GRAPHIC-', button_color=(sg.theme_background_color()), border_width=0, metadata=False),
        sg.Push(), sg.Button("Register", key="Register")
]
 ]
  window = sg.Window("Register", layout) #defining our GUI window and its title
  autosafe = False
  while True: #constantly outputting registration window and recording all actions
   event,values = window.read()
   if event == sg.WIN_CLOSED: #stop outputting the window if closed
      break
   if event == '-TOGGLE-GRAPHIC-': #if switch is toggled
     autosafe = interactiveButton(window, window[event], autosafe)
   if event == "Register": #if "Register" button is selected, getting user input and assigning it to variables
     name = values["setlogin"].strip()
     passwrd = values["setpass"]
     if len(name) <= 2: #check if login is long enough
       sg.popup_error("The login can't be less than 3 characters!", title = "Login is too short!")
       continue
     if len(passwrd) < 8: #check if password is long enough
       sg.popup_error("The password can't be less than 8 characters!", title = "Password is too short!")
       continue
     finalcheck = complexitycheck(passwrd)
     if finalcheck == True:
       pass #continue to user account creation if check is passed
     else:
       sg.popup_error("The password must contain digits and special characters!", title = "No digits or special characters!")
       continue #back again to retry and enter complex password
     salt = random.randint(1000, 9999) #generating random salt to prevent rainbow table attacks
     newPassword = f"{passwrd}{salt}" #appending salt to password
     passwrdhashed = hash256(newPassword) #hashing password with salt appended
     #send password and name to database here
     checkMaxIdQuery = "SELECT MAX(UserID) FROM users" #selecting highest value of userId among existing users
     mycursor.execute(checkMaxIdQuery)
     idResults = mycursor.fetchall()
     idCheckResult = idResults[0][0] #getting result from our query
     if idCheckResult == None: #if there’s no users yet, assign value 1 to UserID
       userId = 1
     else:
       userId = idCheckResult + 1 #else add 1 to current biggest value of UserID create a next UserID
     checkUserQuery = f'SELECT * FROM users WHERE Login="{name}"' #check whether user already exists
     mycursor.execute(checkUserQuery)
     userResults = mycursor.fetchall() #getting result from our query
     if not userResults: #if there's no results, there's no users with the same username
       pass
     else: #else warn the user
       sg.popup_error(f"The user {name} already exists. Please, select a different login.", title = 'User already exists')
       continue
     reqQuery = "INSERT INTO users (UserID, Login, Password, Salt, Authorised) VALUES (%s, %s, %s, %s, %s)" #query with placeholders to add values in table users
     userInfo = [userId, name, passwrdhashed, salt, autosafe] #list with placeholders inserted
     mycursor.execute(reqQuery, userInfo)
     db.commit() #commit changes to database
     sg.popup_ok("Success", f"Account {name} is successfully registered!") #test quote for passing tests
     window.close()
     main(name, userId)
  window.close()

def authentication(): #window, where user selects between authorisation/authentication
  layout = [
  [sg.Text(f"{userGreeting()}! Select an option")],
  [sg.Button("Login", size=(25, 1))], #custom size for the buttons, to lay them out neatly
  [sg.Button("Register", size=(25, 1))]
  ]
  window = sg.Window('Authentication', layout, auto_size_buttons=False)
  while True:
      event, values = window.read()
      if event == sg.WIN_CLOSED: #close window if cross is pressed
          break
      if event == "Login": #open login window if "Login" button selected
        window.close()
        login()
      if event == "Register": #open registration window if "Register" button selected
        window.close()
        registration()
  window.close()

def login(): #defining login window subroutine
  layout = [ #defining layout of the window
    [sg.Text("Login"), sg.Push(), sg.InputText(key="-LOGIN-")],
    [sg.Text("Password"), sg.Push(), sg.InputText(do_not_clear=False, password_char="*", key="-PASS-")], #password field automatically clears after each failed attempt
    [sg.Text("Save session?"), #switch to save session
     sg.Button(image_data=switch_button_off, key='-TOGGLE-GRAPHIC-2-', button_color=(sg.theme_background_color()),
               border_width=0, metadata=False),
     sg.Push(), sg.Button("Login")]
  ]
  window = sg.Window("Login", layout)
  autosafe = False #setting autosafe to false initially
  while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: #close, if window is closed
      break
    if event == "-TOGGLE-GRAPHIC-2-": #if toggle switch triggered, change the value of variable autosafe
      autosafe = interactiveButton(window, window[event], autosafe)
    if event == "Login": #if login button pressed, get inputted login/password values from window
      login = values["-LOGIN-"].strip()
      inputPasswrd = values["-PASS-"]
      try:
        saltQuery = f"SELECT Salt, UserID FROM users WHERE Login='{login}'" #getting salt and UserId from database
        mycursor.execute(saltQuery)
        results = mycursor.fetchall()
        salt = results[0][0]
        userID = results[0][1]
        inputPasswrdHashed = hash256(f"{inputPasswrd}{salt}") #appending salt to password and hashing, to compare with valid password from database
        comparePassQuery = f"SELECT Password FROM users WHERE Login='{login}'" #getting valid hashed password from database
        mycursor.execute(comparePassQuery)
        validPass = mycursor.fetchall()
        validPass = validPass[0][0]
        if validPass != inputPasswrdHashed: #if hash differs, assume that inputted password is invalid
          sg.popup_error("Invalid password!")
          continue
        else: #else let user in
          if autosafe == True: #if autosafe is True (switch toggled), update Autosafe boolean value in database
            changeAutosafeQuery = f"UPDATE users SET Authorised = 1 WHERE UserID = {userID}"
            mycursor.execute(changeAutosafeQuery)
            db.commit()
          window.close() #the window remained opened
          return main(login, userID)
      except Exception as e: #if error is occurred, assume that user is not existing and issue a warning
        sg.popup_error(f"Incorrect login! Exception - {e}", grab_anywhere=True)
        window["-LOGIN-"].update("Try again")
        continue
  window.close()

def dataConvert(timestamp): #subroutine to return a converted timestamp difference between current time and timestamp
  current_time = datetime.now() #getting current time from computer
  current_time_stamp = int(current_time.timestamp()) #converting current time into a timestamp
  time_difference = timestamp - current_time_stamp #getting difference between the current time and checked timestamp
  if time_difference < 0: #bunch of if/elif statements to determine, which measure of time will be suitable to display in:
    status = "OVERDUE"
    return status
  elif time_difference > 0 and time_difference < 3600:
    time_difference = int(time_difference/60)
    if time_difference < 1:
      status = "Less than minute"
      return status
    measure_of_time = "minute"
  elif time_difference > 3600 and time_difference < 86400:
      time_difference = int(time_difference / 3600)
      measure_of_time = "hour"
  elif time_difference > 86400 and time_difference < 2592000:
      time_difference = int(time_difference / 86400)
      measure_of_time = "day"
  elif time_difference > 2592000 and time_difference < 31536000:
      time_difference = int(time_difference / 2592000)
      measure_of_time = "month"
  else:
      time_difference = int(time_difference / 31536000)
      measure_of_time = "year"
  time_difference = str(time_difference) #converting time difference into string with purpose to get the last character from it
  length = len(time_difference) #getting length of the time difference
  last_number = time_difference[length-1] #getting last integer
  if last_number == "1" and len(time_difference) == 1: #if the last number is 1, don't add plural form
      ending = ""
  else: #else add plural form
      ending = "s"
  status = f"{time_difference} {measure_of_time}{ending}" #concatenate all info obtained earlier together
  return status #return status of the task

def getTasks(userID): #subroutine to get all the tasks data from the database
  td = [] #list, in which the data from database will be appended
  getTasksCountQuery = f"SELECT COUNT(*) FROM tasks WHERE UserID = {userID}" #database query to get tasks count from database
  mycursor.execute(getTasksCountQuery)
  tasksCount = mycursor.fetchall()
  count = tasksCount[0][0] # getting task count
  getTasksQuery = f"SELECT Task, Description, Timestamp, TaskID, checkedOff FROM tasks WHERE UserID = {userID}" #database query to get tasks data from database
  mycursor.execute(getTasksQuery)
  tasksCurrent = mycursor.fetchall()
  for i in range(0, count): # getting task data represented in the table, depending on the task count
    time = dataConvert(tasksCurrent[i][2])
    task = [tasksCurrent[i][0], tasksCurrent[i][1], time]
    td.append(task)
  task_headings = [] # task headings for timer
  for task in td: # adding each task heading into a separate list to display them in timer tab
    task_headings.append(task[0])
  return td, tasksCurrent, task_headings #returning back task data

def refreshTasks(userID, window): #function to refresh tasks in the main window
  td, tasksCurrent, task_headings = getTasks(userID) #getting fresh data by calling tasks data grab function getTasks()
  window['-TASKTABLE-'].update(td) #updating our table with fresh data
  window['TASKSELECT'].update(value='', values=task_headings)
  return td, tasksCurrent, task_headings #returning back updated task data

def createUserTables(): #subroutine, that creates task and settings table, if they weren't created before. Usually applies for the first run of the program.
  try:
    taskTableQuery = "CREATE TABLE Tasks(UserID INTEGER(100), Task VARCHAR(250), Description VARCHAR(1500), TaskID INTEGER(100), Timestamp INTEGER(100), checkedOff BOOL, FOREIGN KEY (UserID) REFERENCES Users(UserID), PRIMARY KEY (TaskID))"
    mycursor.execute(taskTableQuery)
  except:
    pass
  try:
    settingsTableQuery = "CREATE TABLE Settings(UserID INTEGER(100), Theme VARCHAR(1500), Notifications VARCHAR(1500), NotificationTime INTEGER(100), APIkey VARCHAR(1500), FOREIGN KEY (UserID) REFERENCES Users(UserID))"
    mycursor.execute(settingsTableQuery)
  except:
    pass

def checkUserSettings(userID): #check user settings table and creates a default record, if no settings were recorded before
  try:
    checkUserQuery = f"SELECT * FROM settings WHERE UserID = {userID}"
    mycursor.execute(checkUserQuery)
    results = mycursor.fetchall()
    if not results: #if no settings were created before
      setDefaultSettingQuery = f'INSERT INTO settings (UserID, Theme, Notifications, NotificationTime, APIkey) VALUES ({userID}, "DarkBlue3", "Push", 3600, "Notset")' #query with default settings
      mycursor.execute(setDefaultSettingQuery) #set string with default settings for that user
      db.commit() #commit changes to the database
    else:
      pass
  except Exception as e: #except output an error with
    sg.popup_error(f"Table is not created. The following error occurred: {e}")
  finally: #get values from database and set them into our settings tab
    mycursor.execute(checkUserQuery) #executing query again to get the fresh data
    results = mycursor.fetchall()
    theme = results[0][1]
    notifications = results[0][2]
    notificationsTime = results[0][3]
    apikey = results[0][4]
    return theme, notifications, notificationsTime, apikey  # returning the values into the program


def checkTaskDeadline(userID, notifytime, tasksCurrent, window, runornot): #subroutine to check task deadlines and output following notifications. Takes userID and default time to notify, set by the user, as a parameter.
  if runornot != "Push": #if notifications are disabled by the user, don't execute them
    quit()
  else:
    td, tasksCurrent, task_headings = getTasks(userID)
    current_time = datetime.now()  # getting current time from computer
    current_time_stamp = int(current_time.timestamp())  # converting current time into a timestamp
    for task in tasksCurrent: #for each task currently added
      checkedOff = task[4]
      if checkedOff == 1: #if task already notified about, skip
        continue
      taskId = task[3]
      checkOffQuery = f"UPDATE tasks SET checkedOff = 1 WHERE TaskID = {taskId}"
      heading = task[0] #get heading
      deadline = task[2] #get deadline timestamp
      difference = deadline - current_time_stamp #get difference between deadline and current time in seconds
      if difference < 0: #if difference is less than 0, the task is overdue. Output the proper toast notifications with the sound.
        toast("Task is overdue", f"The task {heading} is overdue!", audio='ms-winsoundevent:Notification.Reminder')
        mycursor.execute(checkOffQuery)
        db.commit()
      elif difference <= notifytime: #if notifytime is bigger/equal difference, the task is due soon. Output the proper toast notifications with the sound.
        toast("Task is due soon", f"The task {heading} is due in {dataConvert(deadline)}!", audio='ms-winsoundevent:Notification.Reminder')
        mycursor.execute(checkOffQuery)
        db.commit()
      else: #else, skip the task, as it's not due soon.
        pass

def main(name, userID): #main window after successful authorisation. Takes parameters of user login and userID passed earlier by other subroutines.
  try: #attempt to create a table tasks linked by foreign key with table users and their settings table. Usually applied for first program launch.
    createUserTables()
  except: #if there are already tables created, skip
    pass
  theme, notifications, notificationsTime, apikey = checkUserSettings(userID) #getting user settings from the database
  all_themes = sg.theme_list() #getting all possible customisation options for the program (colour layouts)
  sg.theme(f"{theme}") #setting theme, chosen by the user
  def start_timer(hours, minutes): #subroutine, that starts a timer
    seconds = hours * 3600 + minutes * 60 #converting into seconds from minutes and hours
    end_time = time.time() + seconds #getting ending time
    current_time = int(time.time()) #getting current time
    while True:
      if int(time.time()) != current_time: #if time changed (second passed)
        time_left = int(end_time - time.time()) # time left, displayed as a countdown on the screen
        hours, remainder = divmod(time_left, 3600) #get hours to display
        minutes, seconds = divmod(remainder, 60) #get minutes and seconds to display
        window["TESTTEXT"].update(f"{hours:02d}:{minutes:02d}:{seconds:02d}", visible=True) #dynamically update countdown on the screen
      if window["TESTTEXT"].get() == "00:00:00" or event == "TIMERSTOP": #if timer gets to 0
        toast("Time is up!", audio='ms-winsoundevent:Notification.Looping.Alarm') # toast notification
        window["TIMERSTOP"].update(visible=False)
        window["TESTTEXT"].update("Finished!") #output finish message
        window["TASKFOCUSTEXT"].update(visible=False)
        window["STARTTIMER"].update(visible=True)
        stop_flag = threading.Event() #stopping thread for a timer
        stop_flag.set() #stopping thread for a timer
        try:
          timer_thread.join() #stopping thread for a timer
        except: #eliminating possible errors
          break
  td, tasksCurrent, task_headings = getTasks(userID) #tasks data from database will go here
  headings = ['Task', 'Description', 'Due'] #headings for table
  taskMenuLayout = [
  [sg.Text(f"{userGreeting()}, {name}. Do you want to add some tasks?")],
  [sg.Table(td, headings, key='-TASKTABLE-', auto_size_columns=False, col_widths=[30,30], justification='left', row_height=35)], #table, in which tasks will be displayed
  [sg.Button("Add task", key = "-NEWTASK-"), sg.Button("View/edit task", key = "-EDIT-", button_color="#8B8000"), #add task button
  sg.Button("Delete task", key="TASKDEL", button_color="red")] #delete task button
  ]
  timerLayout = [[sg.Text("Focus on task"), sg.Combo(task_headings, key = "TASKSELECT", readonly=True, default_value="Select task", size=(30,30))], #dynamic selector, from which you can select task, to focus on. Dynamically updated to follow all changes in the database.
                   [sg.Text("For"), sg.Spin(list(range(0,23)), key='-HOURSFOCUS-', s=3), sg.Text("Hours"), sg.Spin(list(range(0,60)), key='-MINUTESFOCUS-', s=3), sg.Text("Minutes")], #minutes and hours selectors
                 [sg.Button("Start", key = "STARTTIMER")],
                 [sg.Text("Focusing on the task", key = "TASKFOCUSTEXT", text_color="black", font=("Helvetica", 30, "bold"), visible=False)], #invisible text, that updates when timer is started
                 [sg.Text("INVISIBLE", key="TESTTEXT", text_color="black", font=("Helvetica", 50, "bold"), visible=False)], #invisible text, that updates when timer is started
                 [sg.Button("Reset timer", key="TIMERSTOP", button_color="red", visible=False)]
                 ]
  settingsLayout = [[sg.Text("Choose customisation theme: "), sg.Combo(all_themes, key = "THEME", readonly=True, size=(50, 10), default_value=theme)], #customisation theme selector, that takes all possible GUIs colours, that PySimpleGUI library has to offer. Initial value of the selector is returned from the user settings table.
                    [sg.Text("Choose notifications type: "), sg.Combo(values=["Push", "None"], key="NOTIFSET", size=(33, 10), readonly=True, default_value=notifications)], #ability to disable notifications. Initial value of the selector is returned from the user settings table.
                    [sg.Text("Choose default notification time before the task is due:"), sg.Spin(list(range(1,60)), key='DUESECVALUE', s=3), sg.Combo(values=["minutes", "hours", "days"], key="DEFNOTIFICATION", size=(33, 10), readonly=True, default_value="hours")], #default notification time, which is later converted to seconds. Initial value of the selector is returned from the user settings table.
                    [sg.Text("OpenAI API key: "), sg.InputText(f"{apikey}", key="AIAPI")], #field to input your OpenAI AI API key. Initial value of the selector is returned from the user settings table.
                    [sg.Button("Save changes", key="UPDATESETTNG"), sg.Button("LOG OUT", key="LOGOUT", button_color="red")] #logout button, to log users out and end the session.
    ]
  layout = [[sg.TabGroup([ #tab group for our main window
    [sg.Tab('Tasks', taskMenuLayout),
     sg.Tab('Timer', timerLayout, element_justification='c'), #justifying all elements at the centre
     sg.Tab("Settings", settingsLayout)]])],
]
  window = sg.Window("Main", layout) #defined window
  timer_thread = None #setting timer variable to be inactive
  while True:
    event, values = window.read(timeout=60000)
    schedule.every(1).minute.do(refreshTasks, userID, window) #every minute refresh user window to reflect changes in the program
    schedule.every(60).seconds.do(checkTaskDeadline, userID, notificationsTime, tasksCurrent, window, notifications)
    schedule.run_pending() #loop to constantly check for schedule tasks such as whether it's time to refresh window
    if event == sg.WIN_CLOSED: #break if window closed
      break
    if event == "STARTTIMER": #if timer is started
      confirmation = sg.popup_yes_no("Warning! The timer will be run as a separate thread. As the PySimpleGUI is not suited for threading, starting a timer may lead to possible errors and exceptions occurring in the console. There's a small chance, that it will impact performance of overall program. Would you still like to continue?", title="Timer might lead to console errors") #warning, that the timer might lead to harmless errors in the console
      if confirmation == None or confirmation == "No": #if yes is not selected, don't start the timer
        continue
      task_selected = values["TASKSELECT"] #get selected task
      if len(task_selected) > 30: #if title length is too long
        sg.popup_error("The task title is too long! It might cause errors, as there's no enough space in the window. Please, select task with less characters.", title="Too long task title!")
        continue
      try: #try to check whether valid type of time is inputted and can be converted into int
        hours_focus = int(values["-HOURSFOCUS-"]) #converting hours to int
        minutes_focus = int(values["-HOURSFOCUS-"])#converting minutes to int
      except: #else output an error popup
        sg.popup_error("Please enter a whole number for hours and minutes!", title="Invalid time")
        continue
      timer_conditions = (0<=minutes_focus<=59, hours_focus>=0) #conditions to check time
      if all(timer_conditions): #if all conditions are True, pass test
        pass
      else: #else output an error popup
        sg.popup_error("Please enter valid values of hours and minutes!", title="Invalid time")
        continue
      window["STARTTIMER"].update(visible=False) #update button to start timer to be invisible
      window["TIMERSTOP"].update(visible=True) #update button to stop timer to be visible
      window["TASKFOCUSTEXT"].update(f'Focusing on task {task_selected}', visible=True) #update and display selected task, that user is working on
      if timer_thread is None or not timer_thread.is_alive(): #if timer is not running currently
        timer_thread = threading.Thread(target=start_timer, args=(int(values["-HOURSFOCUS-"]), int(values["-MINUTESFOCUS-"]))) #start the timer in a separate thread
        timer_thread.start()
    if event == "-NEWTASK-": #if button "New Task" pressed
      addTaskWindow(userID, apikey) #open up a popup window, where user can input task details
      td, tasksCurrent, task_headings = refreshTasks(userID, window)
    if event == "-EDIT-": # if button "Edit" is pressed
      try:
        editRow = values['-TASKTABLE-'][0] #getting the currently selected edit row
        taskView(tasksCurrent[editRow][3], tasksCurrent[editRow][0], tasksCurrent[editRow][1]) #open up a window with the selected task details
        td, tasksCurrent, task_headings = refreshTasks(userID, window) #refreshing tasks after the change to the task was made
      except Exception as e:
        sg.popup_error(f"No tasks were selected. Please, select a task to edit. Exception - {e}", title="No tasks selected!")  # output a warning if no tasks were selected
        continue
    if event == "TASKDEL": #if button to delete task pressed
      try:
        editRow = values['-TASKTABLE-'][0]  #getting the currently selected row
        idTaskToDelete = tasksCurrent[editRow][3] #getting the ID of task that needs to be deleted
        taskDeleteQuery = f"DELETE FROM tasks WHERE TaskID = {idTaskToDelete}" #query to delete the task from database
        mycursor.execute(taskDeleteQuery)
        db.commit() #submit changes to database
        td, tasksCurrent, task_headings = refreshTasks(userID, window) #refresh tasks
      except:
        sg.popup_error("No tasks were selected. Please, select a task to delete", title="No tasks selected!") #output a warning if no tasks were selected
    if event == "LOGOUT": #if the logout button pressed
      logOutQuery = f"UPDATE users SET Authorised = 0 WHERE UserID = {userID}" #query to end user session in the database
      mycursor.execute(logOutQuery)
      db.commit() #commiting changes
      window.close()
      authentication() #readdressing the logged out user back to the authentication stage
    if event == "UPDATESETTNG": #if update settings button is pressed
      selectedTheme = values['THEME'] #getting all values of current inputs on the settings page
      selectedNotif = values['NOTIFSET']
      selectedNotifTime = values['DUESECVALUE']
      selectedNotifTimeMeasure = values['DEFNOTIFICATION']
      selectedApi = values['AIAPI']
      if selectedNotifTimeMeasure == "minutes": #determining the multiplier, in which we'll multiply first value to the second to get seconds
        multiplier = 60
      elif selectedNotifTimeMeasure == "hours":
        multiplier = 3600
      else:
        multiplier = 86400
      selectedNotifTime = multiplier * selectedNotifTime #converting our time to seconds
      updateSettingsQuery = f'UPDATE settings SET Theme = "{selectedTheme}", Notifications = "{selectedNotif}", NotificationTime = "{selectedNotifTime}", APIkey = "{selectedApi}" WHERE UserID = {userID}' #query to update the settings record in database for the user with fresh data.
      mycursor.execute(updateSettingsQuery)
      db.commit() #commiting the changes to the database
      sg.popup_ok("Changes will be applied after the program re-launch!") #formal popup, to inform that changes will be applied after the program relaunch
  window.close()
def addTaskWindow(userID, apikey): #subroutine, that creates a window to add tasks
  layout = [ #defining window layout
    [sg.Text("Add task name:"), sg.Push(), sg.InputText(key="-TASKNAME-")], #field to add task name
    [sg.Text("Add task description:"), sg.InputText(key="-TASKDESCRIPTION-")], #field to add task description
    [sg.CalendarButton("Select date due", target='-DATEDISPLAY-', format="%d/%m/%Y"), sg.In("2025/01/01", key = "-DATEDISPLAY-", #calendar, where user can select a date, on which the task is due
    enable_events=True, visible=False), sg.Spin(list(range(1,24)), key='-HOURS-', s=3), sg.Text(":", text_color="black", font=("Helvetica", 12, "bold")),
     sg.Spin(list(range(0, 60)), key='-MIN-', s=3), sg.Text("Sub-tasks AI split?"), sg.Button(image_data=switch_button_off, key='AISPLIT', button_color=(sg.theme_background_color()), border_width=0, metadata=False), #two spin selectors, separated with a comma, with a purpose to select hour and minute in which the task is due
     sg.Push(), sg.Button("Add task", key = "-TASKADD-", button_color="green")]
  ]
  window = sg.Window("Add task", layout)
  aisplit = False #setting ai split bool to false initially
  while True:
    event, values = window.read() #defined window
    if event == sg.WIN_CLOSED: #break if window closed
      break
    if event == "AISPLIT": #if aisplit switch triggered, set the value of aiswitch to true
      aisplit = interactiveButton(window, window[event], aisplit)
    if event == "-DATEDISPLAY-": #if new date is selected from calendar
      dateSelected = values['-DATEDISPLAY-'] #getting date from calendar
      hourSelected = values['-HOURS-'] #getting hours from user input
      minuteSelected = values['-MIN-'] #getting minutes from user input
      try: #validating time robustness
        date_conditions = (0 <= minuteSelected <= 59, 23 >= hourSelected >= 0)
      except Exception as e:
        sg.popup_error("Input correct time!")
        continue
      if not all(date_conditions):
        sg.popup_error("Input correct time!")
        continue
      timeSelected = f"{dateSelected}/{hourSelected}/{minuteSelected}" #combining all the variables together to get a defined day, hour and a minute when the task is due
      try:
        stamp = int(datetime.strptime(timeSelected, "%d/%m/%Y/%H/%M").timestamp()) #converting the time selected to a timestamp
      except:
        sg.popup_error("Time due is invalid! Please ensure that you inputted proper values!", title="Invalid time")
        continue
    if event == "-TASKADD-": #if task add button is pressed
      addTaskQuery = "INSERT INTO tasks (UserID, Task, Description, TaskID, Timestamp, checkedOff) VALUES (%s, %s, %s, %s, %s, %s)" #query to add new task into the database
      taskName = values['-TASKNAME-'] #gets the value of task name
      taskDescription = values['-TASKDESCRIPTION-'] #gets the value of task description
      if not taskName.replace(" ", "").isalpha():  # special check whether only letters are inputted
        sg.popup_error("Please input only letters in the task name", title="Input only letters")
        continue
      if aisplit == True: #if ai split to sub-tasks selected
        try:
          sg.popup_ok("Splitting will take approximately 5 seconds of idle time. Please, wait for a while.")
          taskDescription = splitWithAI(taskName, apikey) #try to split with AI
        except Exception as e: #except error output the error
          sg.popup_error(f"Check whether your API key is valid / your internet connection. The error occurred - {e}")
          continue
      try:
        checkMaxIdQuery = "SELECT MAX(TaskID) FROM tasks"  # selecting highest value of TaskID among existing users
        mycursor.execute(checkMaxIdQuery)
        idResults = mycursor.fetchall()
        idCheckResult = idResults[0][0]  # getting result from our query
        if idCheckResult == None:  # if there’s no users yet, assign value 1 to TaskID
          taskID = 1
        else:
          taskID = idCheckResult + 1  # else add 1 to current biggest value of TaskID create a next TaskID
        checkedoff = 0 #declaring bool false for checkoff task
        task = [userID, taskName, taskDescription, taskID, stamp, checkedoff]
        mycursor.execute(addTaskQuery, task)
        db.commit()  # commit changes to database
        window.close()
      except Exception as e: #in case of error, issue warning
        sg.popup_error(f"Please double-check your inputted data. Error has occurred and your task might not saved to the database. Error code - {e}", title = "Error")
  window.close()
def taskView(TaskID, heading, description): #subroutine to view task details
  extended_description = textwrap.fill(description, 50) #wrapping text to new line each 50 characters
  layout = [[sg.Text("Task name: "), sg.Text(f"{heading}" , key = "TASKNAME", enable_events=True)], #task heading is loaded here. When clicked on, it transforms into an editable field.
            [sg.Text("Task description: "), sg.Text(f"{extended_description}" , key = "TASKDESC", enable_events=True)], #task description is loaded here. When clicked on, it transforms into an editable field.
            [sg.Button("Save changes", key="SAVECHANGE", button_color="green")] #button to save changes
            ]
  window = sg.Window("Task editor", layout) #initialising window
  while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: #break if window is closed
      break
    if event == "TASKNAME": #if clicked on task name text
      editHeading = [[sg.Multiline(f"{heading}", key = "TASKNAMEEDIT")]]
      window.extend_layout(window["TASKNAME"], rows=editHeading) #change the text into the input field with retaining previous values of task heading
    if event == "TASKDESC": #if clicked on task description text
      editDesc = [[sg.Multiline(default_text=extended_description, key = "TASKDESCEDIT", auto_size_text=True, auto_refresh=True, size=(50, 10))]]
      window.extend_layout(window["TASKDESC"], rows=editDesc) #change the text into the input field with retaining previous values of task description
    if event == "SAVECHANGE": #if save changes button is pressed
      try:
        newHeading = values["TASKNAMEEDIT"] #get current heading from input field
        addHeading = True #setting bool to true if task heading was changed
      except:
        addHeading = False #else set to false
      try:
        newDescription = values["TASKDESCEDIT"].strip().replace("\n", " ")  # get current description from input field
        addDesc = True #setting bool to true if task description was changed
      except:
        addDesc = False #else set bool to false
      if addHeading == True: #if heading was edited
        if len(newHeading) < 3:  # if new heading is less than 3 characters long issue warning
          sg.popup_error("The task must be at least 3 characters long!", title="Very short task title")
          continue
      if addHeading == False and addDesc == False: #if task was just viewed, close window
        break
      elif addDesc == False: #if no description was edited, but only heading
        if not newHeading.replace(" ", "").isalpha():  # special check whether only letters are inputted
          sg.popup_error("Please input only letters in the task name", title="Input only letters")
          continue
        editQuery = f'UPDATE tasks SET Task="{newHeading}" WHERE TaskID = {TaskID}'
      elif addHeading == False: #if no heading was edited, but only description
        editQuery = f'UPDATE tasks SET Description="{newDescription}" WHERE TaskID = {TaskID}'
      else: # if both heading and description were added
        editQuery = f'UPDATE tasks SET Task="{newHeading}", Description="{newDescription}" WHERE TaskID = {TaskID}'
        if not newHeading.replace(" ", "").isalpha():  # special check whether only letters are inputted
          sg.popup_error("Please input only letters in the task name", title="Input only letters")
          continue
      mycursor.execute(editQuery) #update task heading and description in database
      db.commit() #submitting changes
      window.close() #close the window after changes were submitted
  window.close()
usercheck() #run the user check, which will determine, whether the session should be loaded



