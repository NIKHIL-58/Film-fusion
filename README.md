# 🎬 Movie Recommendation System (Film-fusion)

A **web application** built using **Flask**, **MongoDB**, **HTML**, **CSS**, and **JavaScript**. The app allows users to explore, search, and manage movies, watch trailers, store their favorites, and more.

---

## 🚀 Features  
- **User Authentication**:  
  - Signup/Login  
  - Password reset with OTP-based verification  
  - JWT-based session management  

- **Movie Search & Recommendations**  
  - Search for movies by name  
  - Get details from OMDB API  
  - View YouTube trailers  

- **Favorites Management**  
  - Add/remove movies to favorites  
  - Display favorite movies in grid view  

- **Recently Watched Section**  
  - List of movies the user has interacted with  

- **Profile Management**  
  - Update user profiles  
  - Upload profile pictures  

---

## 📁 Project Structure  

```plaintext
├── app/                 # Flask application
│   ├── templates/       # HTML templates
│   ├── static/          # CSS, JavaScript, and other static files
│   ├── config.py        # Configuration settings  
│   ├── utils.py         # Utility functions  
│   ├── routes/          # Routes for various features  
│   │   ├── login.py     
│   │   ├── signup.py   
│   │   ├── movies_search.py  
│   │   ├── reset_password.py  
│   │   └── favorites_movie.py  
├── uploads/             # User profile uploads  
├── requirements.txt     # Python dependencies  
├── README.md            # Documentation  
└── run.py               # Application entry point  
```

---

## ⚙️ Installation  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. **Set up a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**  
   - Install and run MongoDB locally or use **MongoDB Atlas**.  
   - Create a database named `MovieDB` and a collection for users and movie data.

5. **Configure environment variables**  
   Update `app/config.py` with your **OMDB API** and **YouTube API keys**.

6. **Run the application**  
   ```bash
   python run.py
   ```
   The app will be available at: [http://localhost:5000](http://localhost:5000)

---

## 🛠️ API Endpoints  

- **User Authentication**  
  - `/signup` (POST) – Register a new user  
  - `/login` (POST) – User login  
  - `/reset-password` (POST) – Reset password using OTP  

- **Movie Management**  
  - `/api/movie/search` (POST) – Search for a movie  
  - `/api/movie_details/<imdbID>` (GET) – Get movie details  

- **Favorites Management**  
  - `/api/favorites` (GET) – Get all favorite movies  
  - `/api/favorites/<imdbID>` (POST) – Add to favorites  

---

## 📋 Technologies Used  

- **Backend**: Flask, PyMongo, JWT  
- **Database**: MongoDB  
- **Frontend**: HTML, CSS, JavaScript  
- **APIs**: OMDB API, YouTube Data API  

---

## 🌐 Demo  

Link: [https://drive.google.com/file/d/18-oYERGVeMPCISavc5Oqy7WiXXWns17I/view?usp=sharing](https://drive.google.com/file/d/18-oYERGVeMPCISavc5Oqy7WiXXWns17I/view?usp=sharing)

Link: [https://drive.google.com/file/d/1oDcRZhvMNxk9K7TBFchf7LP0ENWiZFgL/view?usp=sharing](https://drive.google.com/file/d/1oDcRZhvMNxk9K7TBFchf7LP0ENWiZFgL/view?usp=sharing)

---

## 📸 Screenshots

1. ![Dashboard](https://github.com/user-attachments/assets/25c9e7b3-3d64-4932-a73b-9622f8b51df9)![work1](https://github.com/user-attachments/assets/28f7565f-509a-4c2d-a4a1-c9cb5b5627c7)
![work6](https://github.com/user-attachments/assets/bdd19a64-aa3a-4929-aee1-3d69c66176a7)
![work5](https://github.com/user-attachments/assets/b3a98ff6-5157-49f6-bb4a-3f0532733ca6)
![work4](https://github.com/user-attachments/assets/c81844a0-6680-45cb-af2d-fd20c7ffcbdc)
![work3](https://github.com/user-attachments/assets/59845906-29ba-4264-afa1-b240340bfa5d)
![work2](https://github.com/user-attachments/assets/ba5ad3cc-b5af-4c95-8f8e-f7d20f2b930d)

2. ![Search Movies](https://github.com/user-attachments/assets/7daf4b5a-d762-452e-a02f-f6ab6d6497b2)
3. ![Movie Details](https://github.com/user-attachments/assets/48016d28-cff9-4d1a-a17a-36c8d265cbed)
4. ![Favorites](https://github.com/user-attachments/assets/2bd46a6d-a83b-40e8-9f95-475c6cecd932)
5. ![Profile Page](https://github.com/user-attachments/assets/3947cbd0-c640-494d-ad6c-b79234219b91)
6. ![Trailer Integration](https://github.com/user-attachments/assets/fb779e81-5685-4c4e-922d-c0a4ece4d2bd)
7. ![Watch Trailer](https://github.com/user-attachments/assets/f6aeafb9-bccb-4642-8041-16e03b0d88de)
8. ![User Settings](https://github.com/user-attachments/assets/66de882c-be85-4efe-9755-7983156fe570)
9. ![Logout](https://github.com/user-attachments/assets/79c0f902-8df6-4c5f-b156-dfc6d18c3ee9)
10. ![JWT Session Expiry](https://github.com/user-attachments/assets/e7f7e166-a595-4b33-b498-078f5a776a5d)

---


## 🛡️ Security  

- Passwords are hashed using `generate_password_hash`.  
- JWT is used for session management.  
- Secure file uploads using `secure_filename`.  

---

## 📜 License  

This project is licensed under the **NIKHIL** – see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgments  

- [OMDB API](http://www.omdbapi.com/) for movie data  
- [YouTube Data API](https://developers.google.com/youtube/) for fetching trailers  

---

## 📧 Contact  

For any inquiries or support, contact me at **nikhildubey183@gmail.com**.  

