# This bot return you the text massage ,link ,photo ,video ,audio which you provide by you in code
# This code has been generated by Om Lathiya


# line numbers for replace Line : 19 for bot token
#                          if your run code on your pc then use your drive path
#                          else can use the online compiler or editor like "Google colab" then use your online drive path
#                          Line : 96 (optional) for text massage
#                          Line : 98 (optional) for link
#                          Line : 100 for photo path
#                          Line : 102 for video path
#                          line : 104 for audio path



import requests
import time

base_url = "https://api.telegram.org/bot<|Your_Bot_Token|>"

# Function to send a text message
def send_text(chat_id, text):
    parameters = {
        "chat_id": chat_id,
        "text": text
    }
    resp = requests.post(base_url + "/sendMessage", data=parameters)
    print(resp.text)

# Function to send a clickable link
def send_link(chat_id, link_text, link_url):
    message = f"[{link_text}]({link_url})"  # Markdown format for clickable link
    parameters = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    resp = requests.post(base_url + "/sendMessage", data=parameters)
    print(resp.text)

# Function to send a photo
def send_photo(chat_id, photo_path):
    with open(photo_path, "rb") as photo_file:
        files = {
            "photo": photo_file
        }
        parameters = {
            "chat_id": chat_id
        }
        resp = requests.post(base_url + "/sendPhoto", data=parameters, files=files)
        print(resp.text)

# Function to send a video
def send_video(chat_id, video_path):
    with open(video_path, "rb") as video_file:
        files = {
            "video": video_file
        }
        parameters = {
            "chat_id": chat_id
        }
        resp = requests.post(base_url + "/sendVideo", data=parameters, files=files)
        print(resp.text)

# Function to send an audio file
def send_audio(chat_id, audio_path):
    with open(audio_path, "rb") as audio_file:
        files = {
            "audio": audio_file
        }
        parameters = {
            "chat_id": chat_id
        }
        resp = requests.post(base_url + "/sendAudio", data=parameters, files=files)
        print(resp.text)

# Function to process incoming messages
def read_message(offset):
    parameters = {
        "offset": offset,
        "limit": 10
    }
    resp = requests.get(base_url + "/getUpdates", params=parameters)
    data = resp.json()

    if not data.get("result"):
        return offset

    for result in data["result"]:
        if "message" in result and "text" in result["message"]:
            chat_id = result["message"]["chat"]["id"]
            message_text = result["message"]["text"].lower()

            # Respond based on commands
            if message_text == "send text":
                send_text(chat_id, "This is a text message.")
            elif message_text == "send link":
                send_link(chat_id, "Visit Telegram", "https://telegram.org")
            elif message_text == "send photo":
                send_photo(chat_id, "# Replace with the correct photo path")  
            elif message_text == "send video":
                send_video(chat_id, "# Replace with the correct video path")  
            elif message_text == "send audio":
                send_audio(chat_id, "# Replace with the correct audio path")
                  
    # Return the latest update_id to avoid processing old messages
    return data["result"][-1]["update_id"] + 1

# Start polling for messages
offset = 0
while True:
    offset = read_message(offset)
    time.sleep(2)  # Avoid hitting API rate limits
