import firebase_admin
import requests
from firebase_admin import credentials, firestore, auth
import os
import requests

cred = credentials.Certificate(r"C:\Users\thoma\Desktop\Fall 2024\CSE-310\weather-app-f46a9-firebase-adminsdk-v2lvq-25cf0375d2.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
API_key = '1554f3ea3d354cdd8a6153552243009'
base_URL = "http://api.weatherapi.com/v1/current.json"


def Add_User():
    user = auth.create_user(
    email = input('Please enter your email: '),
    email_verified = False,
    password = input('Please create your password: ')
    )
    print(f'Successfully created new user: {user}')
    return user.email
def Store_User_Data(uid, data):
    db.collection('users').document(uid).set(data)
    print(f'Data stored successfully for user: {uid} with data {data}')
    return
def Find_By_Email(email):
    user = auth.get_user_by_email(f'{email}')
    return user.uid
def Login_User():
    email = input('Enter the email registered with this account: ')
    try:
        user = auth.get_user_by_email(email)
        print(f'Successfully logged in as {email}')
        return user.uid
    except auth.UserNotFoundError:
        print('Error. User not found. Please create account')
        return None   
def Main_Menu():
    while True:
        print('1. Login')
        print('2. Create Account')
        print('3. Exit')

        user_choice = input('Please enter a choice: ')
        user_num = int(user_choice)
        
        if user_num == 1:
            user_id = Login_User() #takes you to line 30, and checks if the email used in the account exists, if it doesn't it will redirect you to create an account.
            if user_id:
                return user_id #gives the user id so the database will be able to find which collection to look into
            else:
                print('Error, please create an account first.')
                Main_Menu() #redirection if the user id is not found
        elif user_num == 2:
            user_email = Add_User() #routes the user to line 15
            user_id = Find_By_Email(user_email) #finds user id to return as the "compass" to the database
            return user_id
        elif user_num == 3:
            return False #exits the while loop
        else:
            print('Error. Invalid input please choose a valid input.')
def Create_New_Data():
    user_data = {
        'name': input('Please enter your name: ').lower(),
        'city': input('Please enter the city you live in: ').lower(),
        'temp_pref': input('Please enter your preference between farenheit (f) or celcius (c): ').lower()
    }
    return user_data
def Get_User_Data(uid):
    try:
        doc_ref = db.collection('users').document(uid)
        #print(doc_ref)
        doc = doc_ref.get()
        #print(dictionary_doc)
        #print(doc)

        if doc:
            user_data = doc.to_dict()
            print(f'User data fetched: {user_data}')
            return user_data
        else:
            print('No such document!')
            return None
    except Exception as e:
        print(f'An error occured: {e}')
        return None
def Get_Weather_Data(uid):
    user_dict = Get_User_Data(uid)
    #print(f'uid: {uid}')
    #print(f'API key: {API_key}')
    #print(f'dictionary: {user_dict}')

    if user_dict and 'city' in user_dict:
        city = user_dict['city']
        request_URL = f"{base_URL}?key={API_key}&q={city}&aqi=no"
        try:
            response = requests.get(request_URL)

            if response.status_code == 200:
                weather_data = response.json()
                return weather_data
            else:
                print(f'Error. {response.status_code}')
                return None
        except Exception as e:
            print(f'There was an error: {e}')
    else:
        print('City not found for user. Please update info.')
    return
def Display_Weather_Data(weather, user_data):


    os.system('cls')
    print(f"City: {weather['location']['name']}")
    print(f"Last updated: {weather['current']['last_updated']}")
    
    if user_data['temp_pref'] == 'c':
        print(f"Temperature: {weather['current']['temp_c']}")
        print(f"Feels Like: {weather['current']['feelslike_c']}")
    elif user_data['temp_pref'] == 'f':
        print(f"Temperature: {weather['current']['temp_f']}")
        print(f"Feels Like: {weather['current']['feelslike_f']}")

    print(f"Cloud Coverage: {weather['current']['cloud']}%")
    print(f"Condition: {weather['current']['condition']['text']}")


    return
def Main():
    uid = Main_Menu()
    if uid:
        while True:
            print('1. Change account information')
            print('2. Open Weather Application')
            print('3. Logout')
            print('4. Exit')

            user_choice = input('Enter your choice: ')
            u_num = int(user_choice)
            
            if u_num == 1:
                new_data = Create_New_Data() #this takes the user to line 63 to create a new dictionary to add into the collections and the document with the name of the user id
                Store_User_Data(uid, new_data) #this takes the data from line 143 and stores it through line 23
            elif u_num == 2:
                weather_data = Get_Weather_Data(uid) #this calls the function on line 88 to find the data through the API
                user_data = Get_User_Data(uid) #takes the user id to line 70 to have the dictionary put into user_data
                Display_Weather_Data(weather_data, user_data) #displays data we found through the API and the database
            elif u_num == 3:
                uid = Main_Menu()
                if not uid:
                    break
                return False
            elif u_num == 4:
                return False
    else:
        print('Error. Please create an account')
if __name__ == "__main__":
    Main()