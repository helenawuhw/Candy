To run code: 
Install python 2.7
Open command window and in folder of files run:
    python gen_resp.py
Open a second command window and in folder run: 
    python -m SimpleHTTPServer
Open a chrome browser and type in url: 
    http://localhost:8000/test.html
Say what you want to say. Stick to sentences like:
    “I am hungry”
    “I am not hungry”
    “I want to go home”
This will appear in the database. We have not implemented a way to be read back into the front end.
Database: https://fiery-heat-7465.firebaseio.com/