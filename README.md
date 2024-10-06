# weather_app
# Overview

I wrote a program that has the user login or create an account then input information on their name, where they live, and their preference of farenheit or celcius. This information is stored in the cloud, and called in multiple functions in order to successfully gather the data from the API. Learning to integrate these together in the same project really helped me understand more fully the process in which API's and databases work together. 

I decided to make this project to learn more about cloud databases, specifically firebase, a Google based cloud database that doesn't require me to pay. I also learned how to use API's in conjuncture with the database. 

[Software Demo Video](https://www.youtube.com/watch?v=OcZq6GpVqpc)

# Cloud Database

I am using a cloud database called Firestore. It is a free-to-use, small-scale database provided by Google and is very intuitive. Firestore offers real-time syncing across devices, making it ideal for building responsive, scalable applications.

I created a very simple data structure using dictionaries, collections, and documents. The collection was called user, and everytime a new user was made, the user ID would be created as a document, which made it very simple to just use the id to access the information based on the user that was logged in. Within the document, there was contained a dictionary with the name, city, and temperature preference within.

# Development Environment

I used VScode to code this project.

This is written in python using the libraries: firebase_admin(database), requests(api), os(local computer), 

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [WeatherAPI](www.weatherapi.com)
- [Firebase](https://console.firebase.google.com)

# Future Work
- Add GUI
- Add user authentication
- Add more variety to display weather
