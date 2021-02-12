# EIT Timetable to Google Calendar CSV

Converts timetables generated from http://mytimetable1.eit.ac.nz/ to CSV files compatible with [Google Calendar](https://calendar.google.com)


### Setup
Use python version >= 3.6

Setup a virtual environment
```bash
$ python3 -m venv venv
```
Activate the virtual environment.
```bash
# On Linux / POSIX
$ source ./venv/bin/activate
# On Windows with cmd.exe
C:\> venv\Scripts\activate.bat
# On Windows with powershell
C:\> venv\Scripts\Activate.ps1
```
Install the requirements
```bash
$ pip install -r requirements.txt
```

### Creating `urls.txt`
Create the file `urls.txt` in the current working directory.

The urls are retrieved by the following:
1. Navigating to http://mytimetable1.eit.ac.nz
2. Clicking on the **Courses** button.
3. Searching for your course & selecting it from the dropdown box.
4. Clicking on the **View Timetable** button.
5. Coping the url in the address bar.

What the file should look like: (look at `example.urls.txt`)

```
http://mytimetable1.eit.ac.nz/Home/Timetable...
http://mytimetable1.eit.ac.nz/Home/Timetable...
http://mytimetable1.eit.ac.nz/Home/Timetable...
http://mytimetable1.eit.ac.nz/Home/Timetable...
http://mytimetable1.eit.ac.nz/Home/Timetable...
http://mytimetable1.eit.ac.nz/Home/Timetable...
http://mytimetable1.eit.ac.nz/Home/Timetable...
http://mytimetable1.eit.ac.nz/Home/Timetable...

```

### Running the script
```bash
python scrape.py
```
This saves a `calendar.csv` file in the current working directory.

### [How to import into Google Calendar](https://support.google.com/calendar/answer/37118)

