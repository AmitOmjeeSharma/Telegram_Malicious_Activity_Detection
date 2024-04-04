from telethon.sync import TelegramClient
from telethon.tl.types import PeerChat
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import errors
import json
from pymongo import MongoClient
import base64
from .forms import MessageForm
from django.shortcuts import render
import pymongo
from bson import ObjectId
from datetime import datetime
import os
import joblib

model1 = joblib.load(os.path.dirname(__file__) + "\\mySVCModel1.pkl")

# Create a MongoDB client and database connection
mongo_client = MongoClient("mongodb://localhost:/")
db = mongo_client["telegramDB"]

# JSON encoder to handle datetime and bytes objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return base64.b64encode(o).decode("utf-8")  # Encode bytes as base64
        return super().default(o)

# Define a global variable for collection name
new_collection_name = None

# Define an asynchronous view function to handle the message form
async def message_form(request):
    global new_collection_name  # Access the global variable
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            group_link = form.cleaned_data["group_link"]

            # Telegram API credentials
            api_id = # 8 digit api id
            api_hash = "telegram api hash"
            api_hash = str(api_hash)
            phone = "+91 mobile number"
            username = "username"

            async def main(phone):
                global new_collection_name  # Use the nonlocal keyword

                telethon_client = TelegramClient(username, api_id, api_hash)

                await telethon_client.start()

                if not await telethon_client.is_user_authorized():
                    await telethon_client.send_code_request(phone)
                    try:
                        await telethon_client.sign_in(phone, input("Enter the code: "))
                    except errors.SessionPasswordNeededError:
                        await telethon_client.sign_in(password=input("Password: "))

                me = await telethon_client.get_me()

                group_input_entity = group_link

                if group_input_entity.isdigit():
                    entity = PeerChat(int(group_input_entity))
                else:
                    entity = group_input_entity

                group = await telethon_client.get_entity(entity)

                offset_id = 0
                limit = 1000
                all_messages = []

                while True:
                    history = await telethon_client(GetHistoryRequest(
                        peer=group,
                        offset_id=offset_id,
                        offset_date=None,
                        add_offset=0,
                        limit=limit,
                        max_id=0,
                        min_id=0,
                        hash=0,
                    ))
                    if not history.messages:
                        break
                    messages = history.messages
                    # Inside the message retrieval loop
                    for message in messages:
                        # Check if message.message is not None
                        if message.message:
                            # Extract the ID, date, and message text
                            message_dict = {
                                "id": message.id,
                                "date": message.date,
                                "message": message.message,
                            }
                            # Predict the category using your ML model
                            category = model1.predict([message.message])[0]
                            message_dict["category"] = category
                            all_messages.append(message_dict)
                        else:
                            # Handle cases where message.message is None (if needed)
                            pass
                    offset_id = messages[-1].id  # Use negative index to get the last message

                # Use the group title as the JSON filename, group name, and collection name
                group_title = group.title if hasattr(group, "title") else "UnnamedGroup"
                filename = f"{group_title}_messages.json"
                collection_name = group_title
                print("group_title", group_title)
                # Assigning collection name to global variable
                new_collection_name = group_title

                with open(filename, "w") as outfile:
                    json.dump(all_messages, outfile, cls=DateTimeEncoder)

                # Insert data into the collection
                collection = db[collection_name]
                collection.insert_many(all_messages)

                print(f"Data inserted into MongoDB collection: {collection_name}")

                await telethon_client.disconnect()

                # Render a template to select the category
                return render(request, "chart.html", {"group_link": group_link})

            result = await main(phone)

            return result  # Return the result from the async function
    else:
        form = MessageForm()
    return render(request, "message_form.html", {"form": form})




# # View function to render the chart template
# def chart(request):
#     return render(request, "chart.html")



# # Define the view function to render the chart template
# Define the view function to render the chart template
def chart(request):
    global new_collection_name
    # Set up the connection to MongoDB server
    client = pymongo.MongoClient("mongodb://localhost:/")  # Replace with your MongoDB server URI

    if request.method == "POST":
        # Retrieve the selected category from the form
        selected_category = request.POST.get("category")

        # Retrieve the list of database names from the MongoDB server
        db_names = client.list_database_names()

        # Define the target collection name
        target_collection_name = new_collection_name  # Replace with your default collection name
        print("new_collection_name",new_collection_name)
        # Check if the target collection exists in any of the databases
        target_db_name = None
        for db_name in db_names:
            db = client[db_name]
            collections = db.list_collection_names()
            if target_collection_name in collections:
                target_db_name = db_name
                break

        # If the target collection doesn't exist, create it
        if not target_db_name:
            target_db_name = target_collection_name
            # Create the new collection with the default name
            db = client[target_db_name]
            collection = db[target_collection_name]

        # Access the target database and collection
        db = client[target_db_name]
        collection = db[target_collection_name]

        # Define the query to find documents with the selected category
        query = {"category": selected_category}

        # Define the projection fields you want to retrieve
        projection = {
            "_id": 0,  # Exclude _id field
            "sender_id": 1,
            "date": 1,
            "message": 1,
            "category": 1
        }  # You can specify projection fields here if needed

        # Find documents in the collection that match the query
        results = collection.find(query, projection)

        # Create a list to store the matching documents
        matching_documents = []

        # Loop through the results and append them to the list
        for result in results:
            # Convert the ObjectId to a string
            if "_id" in result:
                result["_id"] = str(result["_id"])
            # Convert datetime to string
            if "date" in result and isinstance(result["date"], datetime):
                result["date"] = result["date"].strftime("%Y-%m-%d %H:%M:%S")
            matching_documents.append(result)

        # Close the MongoDB connection
        client.close()

        # Render the chart template with the matching documents
        return render(request, "chart.html", {"matching_documents": matching_documents})

    # Render the initial chart template without data if it's a GET request
    return render(request, "chart.html")





