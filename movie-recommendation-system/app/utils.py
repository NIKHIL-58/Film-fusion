import jwt
from bson import ObjectId
from flask import request
import requests  
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def verify_jwt_token(token: str, secret_key: str, algorithms: list) -> dict:
    """
    Verifies a JWT token and returns the decoded payload if the token is valid.
    """
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=[algorithms])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise ValueError("The token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token. Could not decode.")


def convert_objectid(doc):
    if isinstance(doc, list):
        for item in doc:
            convert_objectid(item)
    elif isinstance(doc, dict):
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
            elif isinstance(value, (dict, list)):
                convert_objectid(value)

def fetch_movie_data(query, api_key):
    url = f'http://www.omdbapi.com/?s={query}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print('Error: Unable to parse JSON.')
    else:
        print(f'Error: Failed to retrieve data for {query}. HTTP Status Code: {response.status_code}')
    return None

def get_youtube_trailer(title):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{title} trailer",
        "key": "AIzaSyAHX3vfeBZ51GkPTHV6TWWK4y4NIoPwOxY",
        "type": "video",
        "maxResults": 1
    }
    response = requests.get(search_url, params=params)
    video_data = response.json().get("items", [])

    if video_data:
        video_id = video_data[0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

def fetch_related_trailers(movie_title):
    # YouTube API logic to fetch related trailers
    apiKey = "AIzaSyAHX3vfeBZ51GkPTHV6TWWK4y4NIoPwOxY"
    search_query = f"{movie_title} trailer"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&type=video&key={apiKey}"

    response = requests.get(url)  # Ensure requests is imported
    data = response.json()

    related_trailers = []
    if data.get('items'):
        for item in data['items']:
            video_id = item['id']['videoId']
            trailer_url = f"https://www.youtube.com/embed/{video_id}"
            related_trailers.append({
                'movie_title': item['snippet']['title'],
                'trailer_url': trailer_url
            })
    return related_trailers

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def send_otp_email(email, otp):
    try:
        sender_email = "nikhildubey183@gmail.com"
        sender_password = "jemw ilfy dcjc flns"  
        receiver_email = email

        subject = "OTP for Reset Password"
        body = f"""Dear user,

        Your OTP (One-Time Password) for reset your password is: {otp}

        This otp is valid for the next 5 minutes. Please do not share this otp with anyone.
        If you did not request this, please ignore this email.


        Thank you,"""

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Setting up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Log in using app password
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)  # Send the email
        server.quit()  # Close the server connection

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")