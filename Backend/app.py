## goal of app.py: essentially will act as the backend server 
# overview:
# react frontend
# User uploads image
        #↓
# Flask backend receives image
        #↓
# predict.py preprocesses image and runs model
        #↓
# Flask backend sends prediction back
        #↓
# React frontend displays result

# will need to routes, get and post route, GET to check if the 
# backend is running and POST to get the prediction but it accepts 
# and image file which means we are sending data to the backend 

# will also need the import CORS since react will use a different port than Flask,
# and by default browsers may block some requests between different origins for security reasons
# CORS(app) allows for the React frontend to call this backend