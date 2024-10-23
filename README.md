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

1. ![Dashboard](https://github.com/user-attachments/assets/ba5ad3cc-b5af-4c95-8f8e-f7d20f2b930d)
![work1](https://github.com/user-attachments/assets/28f7565f-509a-4c2d-a4a1-c9cb5b5627c7)
![work6](https://github.com/user-attachments/assets/bdd19a64-aa3a-4929-aee1-3d69c66176a7)
![work5](https://github.com/user-attachments/assets/b3a98ff6-5157-49f6-bb4a-3f0532733ca6)
![work4](https://github.com/user-attachments/assets/c81844a0-6680-45cb-af2d-fd20c7ffcbdc)
![work3](https://github.com/user-attachments/assets/59845906-29ba-4264-afa1-b240340bfa5d)

  

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

