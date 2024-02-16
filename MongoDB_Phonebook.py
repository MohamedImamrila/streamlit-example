import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://rezan:rezan@cluster0.g4aqwe2.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    st.write("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    st.write(e)

record = client.InternalTask.MongoDB

def Create_Contact():
    Name = st.text_input("Enter the name:")
    Number = st.text_input("Enter the Mobile_Number:")
    Email = st.text_input("Enter the Email_ID:")

    if len(Number) == 10 and Number.isdigit() and Email.count('@') == 1 and Email.count('.com') == 1:
        st.write("Mobile Number and Email are valid. Contact is successfully created.")
        data = {"_id": Name, "Mobile_Number": Number, "Email_ID": Email}
        record.insert_one(data)
    else:
        st.write("Mobile Number or Email is not valid. Please check and try again.")

def Search_Contact():
    Search = st.text_input("Enter the name or 10-digit number you want to search for:")
    results = record.find({"$or": [{"_id": {"$regex": Search, "$options": "i"}}, {"Mobile_Number": Search}]})
    for result in results:
        st.write(f"Name: {result['_id']}, Number: {result['Mobile_Number']}")

def Delete_Contact():
    search = st.text_input("Enter the name of the contact you want to delete:")
    result = record.delete_one({"_id": search})
    if result.deleted_count == 1:
        st.write(f"Contact {search} deleted successfully.")
    else:
        st.write("Contact not found.")

def Display_all():
    contacts = record.find()
    for contact in contacts:
        st.write(f"Name: {contact['_id']}, Number: {contact['Mobile_Number']}")

st.title("Contact Management System")

functions = {
    "1": Create_Contact,
    "2": Search_Contact,
    "3": Delete_Contact,
    "4": Display_all
}

for key, value in functions.items():
    st.write(f"{key}. {value.__name__.replace('_', ' ')}")

user_input = st.text_input("Which one you want to do? Select the number (1-4):")

# Call the corresponding function based on user input
if user_input in functions:
    functions[user_input]()
else:
    st.write("Invalid input. Please enter a number between 1 and 4.")
