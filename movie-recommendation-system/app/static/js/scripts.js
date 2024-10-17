document.addEventListener("DOMContentLoaded", () => {
  const loginText = document.querySelector(".title-text .login");
  const loginForm = document.querySelector("form.login");
  const signupForm = document.querySelector("form.signup");
  const loginBtn = document.querySelector("label.login");
  const signupBtn = document.querySelector("label.signup");
  const signupLink = document.querySelector("form .signup-link a");
  const searchButton = document.getElementById("searchButton");
  const topRatedButton = document.getElementById("topRatedButton");
  const closeTrailer = document.getElementById("closeTrailer");
  const trailerModal = document.getElementById("trailerModal");
  const trailerContainer = document.getElementById("trailerContainer");
  const logoutButton = document.getElementById("logoutButton");
  const searchInput = document.getElementById("searchInput");
  const uploadForm = document.getElementById("uploadForm");
  const fileInput = document.getElementById("fileInput");
  const userPhoto = document.getElementById("userPhoto");
  const userName = document.getElementById("userName");
  const userEmail = document.getElementById("userEmail");
  const userMobile = document.getElementById("userMobile");
  const navLinks = document.querySelectorAll(".nav-link");
  const mainContent = document.getElementById("main-content");
  const userProfile = document.getElementById("userProfile");
  const aboutSection = document.getElementById("aboutSection");
  const contactSection = document.getElementById("contactSection");
  const resultsDiv = document.getElementById("results");
  const favoritesDiv = document.getElementById("favoritesMovies");
  const container = document.getElementById("recently-watched-movies");
  const trailersContainer = document.getElementById(
    "recommendedTrailersContainer"
  );

  const defaultMovies = [
    // { title: "Inception", imdbID: "tt1375666" },
    // { title: "The Dark Knight", imdbID: "tt0468569" },
    // { title: "Interstellar", imdbID: "tt0816692" },
    { title: "Jawan", imdbID: "tt15354916" },
    { title: "Thor: Love and Thunder", imdbID: "tt10648342" },
    // { title: "Stree 2", imdbID: "tt27510174" },
    { title: "Bad Newz", imdbID: "tt24517830" },
    // { title: "Dunki", imdbID: "tt15428134" },
    // { title: "Asuran", imdbID: "tt9477520" },
    { title: "1920: Horrors of the Heart", imdbID: "tt25403492" },
    { title: "1920 London", imdbID: "tt5638500" },
    // { title: "Murder Mystery", imdbID: "tt1618434" },
    // { title: "Dil ek mandir", imdbID: "tt23455928" },
    // { title: "Crazy, Stupid, Love", imdbID: "tt1570728" },
    // { title: "fighter", imdbID: "tt13818368" },
    // { title: "Avengers: Age of Ultron", imdbID: "tt2395427" },
    // { title: "Avengers: Endgame", imdbID: "tt4154796" },
    // { title: "The Avengers", imdbID: "tt0054518" },
    // { title: "Bhool Bhulaiyaa 2", imdbID: "tt6455162" },
    // { title: "Avengers: Infinity War", imdbID: "tt4154756" },

    // Add more default movies as needed
  ];

  if (signupBtn && loginForm && loginText) {
    signupBtn.addEventListener("click", () => {
      loginForm.style.marginLeft = "-50%";
      loginText.style.marginLeft = "-50%";
    });
  }

  if (loginBtn && loginForm && loginText) {
    loginBtn.addEventListener("click", () => {
      loginForm.style.marginLeft = "0%";
      loginText.style.marginLeft = "0%";
    });
  }

  if (signupLink && signupBtn) {
    signupLink.addEventListener("click", () => {
      signupBtn.click();
      return false;
    });
  }

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("login-email").value;
      const password = document.getElementById("login-password").value;

      try {
        const response = await fetch("http://127.0.0.1:5000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });

        const data = await response.json();
        if (response.ok) {
          // Show success notification
          displayNotification("success", "Login successful!");

          // Redirect to home page after a short delay
          setTimeout(() => {
            window.location.href = "/home";
          }, 1500); // Adjust the delay as needed
        } else {
          // Show error notification with server-provided message
          displayNotification(
            "error",
            data.message || "Invalid email or password."
          );
        }
      } catch (error) {
        console.error("Login error:", error);
        // Show error notification for network or other unexpected errors
        displayNotification(
          "error",
          "An error occurred while trying to log in. Please try again later."
        );
      }
    });
  }

  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      // Collect form values
      const name = document.getElementById("signup-name").value.trim();
      const mobile = document.getElementById("signup-mobile").value.trim();
      const email = document.getElementById("signup-email").value.trim();
      const password = document.getElementById("signup-password").value;
      const confirmpassword = document.getElementById(
        "signup-confirm-password"
      ).value;

      // Name validation: ensure it doesn't contain numbers
      if (!/^[a-zA-Z\s]+$/.test(name)) {
        displayNotification(
          "error",
          "Name cannot contain numbers or special characters."
        );
        return;
      }

      // Mobile validation: ensure it contains only numbers and is 10 digits
      if (!/^\d{10}$/.test(mobile)) {
        displayNotification(
          "error",
          "Mobile number must be exactly 10 digits."
        );
        return;
      }

      if (!name || !mobile || !email || !password || !confirmpassword) {
        displayNotification("error", "All fields are required.");
        return;
      }

      // Email format validation
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(email)) {
        displayNotification("error", "Invalid email format.");
        return;
      }

      // Password validation
      if (password !== confirmpassword) {
        displayNotification("error", "Passwords do not match.");
        return;
      }

      // Advanced Password Validation
      const passwordErrors = [];
      if (password.length < 6) {
        passwordErrors.push("at least 6 characters");
      }
      if (!/[a-z]/.test(password)) {
        passwordErrors.push("lowercase");
      }
      if (!/[A-Z]/.test(password)) {
        passwordErrors.push("uppercase");
      }
      if (!/[0-9]/.test(password)) {
        passwordErrors.push("number");
      }
      if (!/[!@#$%^&*()_+{}\[\]:;\"'<>,.?/~`\\|-]/.test(password)) {
        passwordErrors.push("special character");
      }

      if (passwordErrors.length > 0) {
        displayNotification(
          "error",
          `Password must include ${passwordErrors.join(", ")}.`
        );
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:5000/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name,
            mobile,
            email,
            password,
            confirmpassword,
          }),
        });

        const data = await response.json();
        if (response.ok) {
          displayNotification(
            "success",
            data.message || "User registered successfully!"
          );
          setTimeout(() => {
            window.location.href = "/index";
          }, 1000); // Redirect after 1 second if signup is successful
        } else {
          displayNotification("error", data.message || "Signup failed.");
        }
      } catch (error) {
        console.error("Signup error:", error);
        displayNotification(
          "error",
          "An error occurred. Please try again later."
        );
      }
    });
  }

  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      fetch("http://127.0.0.1:5000/logout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // Include cookies in the request
      })
        .then((response) => {
          if (response.ok) {
            displayNotification("success", "Logout successful.");
            setTimeout(() => {
              window.location.href = "/index"; // Redirect to login page after successful logout
            }, 2000); 
          } else {
            displayNotification("error", "Logout failed. Please try again.");
          }
        })
        .catch((error) => {
          console.error("Error during logout:", error);
          displayNotification("error", "Logout failed. Please try again.");
        });
    });
  }


  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const target = e.currentTarget.dataset.target;
      hideAllSections(); // Hide all sections before showing the targeted one

      switch (target) {
        case "home":
          mainContent.style.display = "block";
          break;
        case "account":
          userProfile.style.display = "flex";
          break;
        case "about":
          aboutSection.style.display = "block";
          break;
        case "contact":
          contactSection.style.display = "block";
          break;
      }
    });
  });

  function hideAllSections() {
    if (mainContent) mainContent.style.display = "none";
    if (userProfile) userProfile.style.display = "none";
    if (aboutSection) aboutSection.style.display = "none";
    if (contactSection) contactSection.style.display = "none";
  }
  // Initial setup: Only display the main content on page load
  hideAllSections();
  if (mainContent) mainContent.style.display = "block";

  // Handle photo upload form submission
  if (uploadForm && fileInput && userPhoto) {
    uploadForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      let file = fileInput.files[0];

      if (!file) {
        displayNotification("error", "No file selected.");
        return;
      }

      let formData = new FormData();
      formData.append("profile_picture", file); // The key here should match the Flask route

      try {
        let response = await fetch(
          "http://127.0.0.1:5000/upload_profile_picture",
          {
            method: "POST",
            body: formData,
            credentials: "include",
          }
        );

        if (response.ok) {
          let userData = await response.json();
          if (userData.profile_picture) {
            userPhoto.src = `uploads/${userData.profile_picture}`;
          } else {
            userPhoto.src = "uploads/default-profile-image.png"; // Correct this path
          }
          displayNotification("success", "Photo uploaded successfully.");
        } else {
          userPhoto.src = "uploads/default-profile-image.png";
          displayNotification("error", "Failed to upload photo.");
        }
      } catch (error) {
        console.error("Error uploading photo:", error);
        displayNotification(
          "error",
          "An error occurred while uploading the photo."
        );
      }
    });
  }

  // Fetch user profile data and display profile picture in the circle
async function fetchUserProfile() {
  try {
    let response = await fetch("http://127.0.0.1:5000/api/user-profile", {
      method: "GET",
      credentials: "include",
    });

    if (response.ok) {
      let userData = await response.json();
      userName.textContent = userData.name || "Name";
      userEmail.textContent = userData.email || "Email";
      userMobile.textContent = userData.mobile || "Mobile";

      // Display user's uploaded profile picture or a default one
      if (userData.profile_picture) {
        userPhoto.src = `uploads/${userData.profile_picture}`;
      } else {
        userPhoto.src = "uploads/default-profile-image.png";
      }

      displayNotification("success", "Profile data fetched successfully.");
    }
  } catch (error) {
    console.error("Error fetching profile:", error);
    displayNotification("error", "Failed to fetch profile data.");
  }
}
fetchUserProfile();


  function saveUserProfile(name, email, mobile) {
    fetch("http://127.0.0.1:5000/update_profile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userName: name,
        userEmail: email,
        userMobile: mobile,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          displayNotification("success", "Profile updated successfully!");
        } else {
          displayNotification("error", "No changes detected.");
        }
      })
      .catch((error) => {
        console.error("Error updating profile:", error);
        displayNotification(
          "error",
          "An error occurred while updating the profile."
        );
      });
  }

  if (searchButton && searchInput) {
    searchButton.addEventListener("click", () => {
      const query = searchInput.value.trim();

      if (query) {
        showLoader(); // Show loader when search starts

        // Fetch data from your API
        fetch("http://127.0.0.1:5000/search", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${sessionStorage.getItem("token")}`,
          },
          body: JSON.stringify({ query }), // Only send the query
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            displayMovies(data || []);
            displayNotification(
              "success",
              "Search results loaded successfully."
            );
          })
          .catch((error) => {
            console.error("Error:", error);
            displayNotification(
              "error",
              "An error occurred while fetching search results."
            );
          })
          .finally(() => {
            hideLoader(); // Hide loader once the search operation is complete
          });
      } else {
        displayNotification("error", "Search query is required.");
      }
    });
  }

  async function fetchTopRatedMovies() {
    try {
      showLoader(); // Show loader when fetching starts

      const response = await fetch("http://127.0.0.1:5000/top-rated-movies");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Top rated movies data:", data);
      displayMovies(data);
      displayNotification("success", "Top-rated movies loaded successfully!");
    } catch (error) {
      console.error("Error fetching top-rated movies:", error);
      displayNotification(
        "error",
        "An error occurred while fetching top-rated movies."
      );
    } finally {
      hideLoader(); // Hide loader once the fetch operation is complete
    }
  }

  if (topRatedButton) {
    topRatedButton.addEventListener("click", fetchTopRatedMovies);
  }

  if (closeTrailer) {
    closeTrailer.addEventListener("click", () => {
      closeTrailerModal();
    });
  }

  window.addEventListener("click", (event) => {
    if (event.target === trailerModal) {
      closeTrailerModal();
      fetchRecommendedTrailers();
      fetchTrailers();
    }
  });

  function closeTrailerModal() {
    if (trailerModal && trailerContainer) {
      trailerModal.style.display = "none";
      trailerContainer.innerHTML = "";
      displayNotification("info", "Trailer modal closed.");
    }
  }

  function showLoader() {
    document.getElementById("page-loader").style.display = "flex";
  }

  function hideLoader() {
    document.getElementById("page-loader").style.display = "none";
  }

  // Function to fetch and display movies
  async function displayMovies(movies) {
    const favoriteMovies = await fetchFavorites();

    if (!resultsDiv) return;

    resultsDiv.innerHTML = "";

    if (movies.length === 0) {
      resultsDiv.innerHTML = "<p>No movies found.</p>";
      hideLoader();
      return;
    }

    for (let movie of movies) {
      const movieDiv = document.createElement("div");

      movieDiv.className = "movie";

      let movieDetails;
      try {
        const response = await fetch(
          `http://www.omdbapi.com/?i=${movie.imdbID}&apikey=dd39691a`
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        movieDetails = await response.json();
      } catch (error) {
        console.error("Error fetching movie details:", error);
        continue;
      }

      const poster =
        movieDetails.Poster !== "N/A"
          ? movieDetails.Poster
          : "path/to/placeholder.jpg";
      const title = movieDetails.Title || "No Title Available";

      const isFavorited = favoriteMovies.some(
        (favMovie) => favMovie.imdbID === movie.imdbID
      );

      movieDiv.innerHTML = `
        <div class="movie-item">
          <a href="movie_detail.html?imdbID=${movie.imdbID}">
          <img src="${poster}" alt="${title}">
          <div class="movie-item-title">${title}</div>
          </a>
        </div>
        <button class="trailerButton" data-movie-title="${title}">Watch Trailer</button>
        <div class="heart-button ${
          isFavorited ? "favorited" : ""
        }" data-movie-id="${movie.imdbID}">
            <div class="heart-icon"></div>
        </div>
      `;

      resultsDiv.appendChild(movieDiv);

      // Add event listeners for trailer buttons
      movieDiv.querySelector(".trailerButton").addEventListener("click", () => {
        const movieTitle = title;
        fetchTrailer(movieTitle);
        addToLastWatchedTrailers(movieTitle, poster, movie.imdbID);
      });

      // Add event listeners for heart buttons
      movieDiv
        .querySelector(".heart-button")
        .addEventListener("click", function () {
          const movieId = movie.imdbID;
          if (this.classList.contains("favorited")) {
            removeFromFavorites(movieId);
            this.classList.remove("favorited");
          } else {
            addToFavorites(movieId);
            this.classList.add("favorited");
          }
        });
    }

    hideLoader();
  }
  displayMovies(defaultMovies);

  // Function to fetch favorite movies
  async function fetchFavorites() {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/get_favorites");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      return [];
    }
  }

  // Function to handle adding a movie to favorites
  function addToFavorites(movieId) {
    showLoader(); // Show loader when the operation starts
    fetch("http://127.0.0.1:5000/api/add_favorite", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ imdbID: movieId }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
        displayNotification("success", data.message);
        debugger;
        fetchFavorites();
        fetchFavoriteMovies();
        updateFavoriteButton(movieId, true);
      })
      .catch((error) => {
        console.error("Error adding to favorites:", error);
        displayNotification("error", "Error adding movie to favorites.");
      })
      .finally(() => {
        hideLoader(); // Hide loader once the operation is complete
      });
  }

  // Function to update the heart button state
  function updateFavoriteButton(movieId, isFavorited) {
    const heartButton = document.querySelector(
      `.heart-button[data-movie-id="${movieId}"]`
    );
    if (heartButton) {
      if (isFavorited) {
        heartButton.classList.add("favorited");
      } else {
        heartButton.classList.remove("favorited");
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    fetchFavoriteMovies();
  });

  async function fetchFavoriteMovies() {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/get_favorites");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const favoriteMovies = await response.json();
      displayFavoriteMovies(favoriteMovies);
    } catch (error) {}
  }

  function displayFavoriteMovies(movies) {
    if (!favoritesDiv) return;

    favoritesDiv.innerHTML = "";

    if (movies.length === 0) {
      favoritesDiv.innerHTML = "<p>No favorite movies found.</p>";
      return;
    }

    movies.forEach((movie) => {
      const movieDiv = document.createElement("div");
      movieDiv.className = "favorite-movie";

      const poster =
        movie.Poster !== "N/A" ? movie.Poster : "path/to/placeholder.jpg"; // Placeholder image if no poster

      movieDiv.innerHTML = `
            <img src="${poster}" alt="${movie.Title}">
            <h3>${movie.Title}</h3>
            <p>Year: ${movie.Year}</p>
            <div class="heart-button" data-movie-id="${movie.imdbID}">
                <div class="heart-icon"></div>
            </div>
        `;

      favoritesDiv.appendChild(movieDiv);

      // Set initial favorite state
      updateFavoriteButton(movie.imdbID, true);

      // Add event listener for heart button (double-click to remove)
      movieDiv
        .querySelector(".heart-button")
        .addEventListener("dblclick", () => {
          showLoader(); // Show loader when starting the operation
          removeFromFavorites(movie.imdbID)
            .then(() => {
              hideLoader(); // Hide loader when operation is complete
            })
            .catch(() => {
              hideLoader(); // Ensure loader is hidden even if there's an error
            });
        });
    });
  }
  fetchFavoriteMovies();

  // Function to remove a movie from favorites
  function removeFromFavorites(movieId) {
    showLoader(); // Show loader when the operation starts
    fetch("http://127.0.0.1:5000/api/remove_favorite", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ imdbID: movieId }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
        displayNotification("success", data.message);
        updateFavoriteButton(movieId, false);
        fetchFavoriteMovies(); // Refresh the favorite movies list
      })
      .catch((error) => {
        console.error("Error removing from favorites:", error);
        displayNotification("error", "Error removing movie from favorites.");
      })
      .finally(() => {
        hideLoader(); // Hide loader once the operation is complete
      });
  }

  // Function to update the heart button state
  function updateFavoriteButton(movieId, isFavorited) {
    const heartButton = document.querySelector(
      `.heart-button[data-movie-id="${movieId}"]`
    );
    if (heartButton) {
      if (isFavorited) {
        heartButton.classList.add("favorited");
      } else {
        heartButton.classList.remove("favorited");
      }
    }
  }

  function fetchTrailer(movieTitle) {
    const apiKey = "AIzaSyAHX3vfeBZ51GkPTHV6TWWK4y4NIoPwOxY";
    const searchQuery = encodeURIComponent(`${movieTitle} trailer`);
    const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${searchQuery}&type=video&key=${apiKey}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        if (data.items && data.items.length > 0) {
          const videoId = data.items[0].id.videoId;
          const trailerUrl = `https://www.youtube.com/embed/${videoId}`;
          lastWatchedTrailer = trailerUrl;
          showTrailer(trailerUrl);
          saveTrailerToDb(movieTitle, trailerUrl);
          displayNotification("success", "Trailer fetched successfully!");
        } else {
          console.error("No trailer found for this movie.");
          displayNotification(
            "error",
            "Sorry, no trailer found for this movie."
          );
        }
      })
      .catch((error) => {
        console.error("Error fetching trailer:", error);
        displayNotification("error", "Sorry, the trailer could not be loaded.");
      });
  }

  function saveTrailerToDb(movieTitle, trailerUrl) {
    fetch("http://127.0.0.1:5000/save_trailer", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        trailer_url: trailerUrl,
        movie_title: movieTitle,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          console.log("Trailer saved successfully!");
          displayNotification("success", "Trailer saved successfully!");
        } else {
          console.error("Failed to save trailer");
          displayNotification("error", "Failed to save trailer.");
        }
      })
      .catch((error) => {
        console.error("Error saving trailer:", error);
        displayNotification("error", "Error saving trailer.");
      });
  }

  function fetchTrailers() {
    fetch("http://127.0.0.1:5000/watch_home")
      .then((response) => response.json())
      .then((trailers) => {
        const trailersContainer = document.getElementById(
          "lastWatchedTrailers"
        );
        trailersContainer.innerHTML = ""; // Clear existing trailers

        trailers.forEach((trailer) => {
          const trailerItem = document.createElement("div");
          trailerItem.classList.add("trailer-item");

          const title = document.createElement("h2");
          title.textContent = trailer.movie_title;
          trailerItem.appendChild(title);

          const iframe = document.createElement("iframe");
          iframe.src = trailer.trailer_url;
          trailerItem.appendChild(iframe);

          trailersContainer.appendChild(trailerItem);
        });
      })
      .catch((error) => {});
  }
  fetchTrailers(); // Load trailers on page load

  // Function to show a trailer in a modal
  function showTrailer(url) {
    if (trailerContainer && trailerModal) {
      trailerContainer.innerHTML = `<iframe width="100%" height="350" src="${url}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
      trailerModal.style.display = "block";
      displayNotification("info", "Trailer is now playing.");
    }
  }

  function togglePasswordVisibility(toggleId, inputId) {
    const toggleIcon = document.getElementById(toggleId);
    const passwordField = document.getElementById(inputId);

    if (toggleIcon && passwordField) {
      toggleIcon.addEventListener("click", function () {
        const type =
          passwordField.getAttribute("type") === "password"
            ? "text"
            : "password";
        passwordField.setAttribute("type", type);
        this.classList.toggle("fa-eye");
        this.classList.toggle("fa-eye-slash");
      });
    }
  }

  togglePasswordVisibility("toggle-login-password", "login-password");
  togglePasswordVisibility("toggle-signup-password", "signup-password");
  togglePasswordVisibility(
    "toggle-signup-confirm-password",
    "signup-confirm-password"
  );

  fetch("http://127.0.0.1:5000/api/recently_watched")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((movies) => {
      if (movies.length === 0) {
        container.innerHTML = "<p>No recently searched movies available.</p>";
        displayNotification("info", "No recently searched movies available.");
        return;
      }

      movies.forEach((movie) => {
        const movieItem = `
              <div class="movie-item">
                  <a href="${movie.details_url}">
                      <img src="${movie.poster}" alt="${movie.title}">
                  </a>
                  <div class="movie-item-title">${movie.title}</div>
              </div>
          `;
        container.insertAdjacentHTML("beforeend", movieItem);
      });

      displayNotification(
        "success",
        "Recently searched movies loaded successfully."
      );
    })
    .catch((error) => {});

  document.getElementById("editIcon").addEventListener("click", function () {
    // Enable editing
    document.getElementById("userName").setAttribute("contenteditable", "true");
    document.getElementById("userEmail").setAttribute("contenteditable", "true");
    document.getElementById("userMobile").setAttribute("contenteditable", "true");

    // Show the save button
    document.getElementById("saveButton").classList.remove("hidden");

    // Show the upload form
    document.getElementById("uploadForm").style.display = "block";

    // Show the message box (info message)
    displayNotification("info", "Update your profile details.");
  });

  document.getElementById("saveButton").addEventListener("click", function () {
    // Disable editing
    document.getElementById("userName").setAttribute("contenteditable", "false");
    document.getElementById("userEmail").setAttribute("contenteditable", "false");
    document.getElementById("userMobile").setAttribute("contenteditable", "false");
    // Get updated values
    const updatedName = document.getElementById("userName").innerText;
    const updatedEmail = document.getElementById("userEmail").innerText;
    const updatedMobile = document.getElementById("userMobile").innerText;

    // Save updated values to the database
    saveUserProfile(updatedName, updatedEmail, updatedMobile);

    // Hide the save button
    document.getElementById("saveButton").classList.add("hidden");

    // Hide the upload form
    document.getElementById("uploadForm").style.display = "none";
  });

  function displayNotification(type, message) {
    // Generate a unique ID for this message
    const uniqueId = `messageContainer_${new Date().getTime()}`;

    // Create the message container
    let messageContainer = document.createElement("div");
    messageContainer.id = uniqueId;
    messageContainer.style.position = "fixed";
    messageContainer.style.top = "10%";
    messageContainer.style.right = "0px";
    messageContainer.style.padding = "10px 20px";
    messageContainer.style.borderRadius = "10px";
    messageContainer.style.zIndex = "1000px";
    messageContainer.style.transition = "opacity 0.5s ease-in-out";
    messageContainer.style.opacity = "0"; // Initially invisible

    // Create the message text element
    let messageText = document.createElement("span");
    messageText.innerText = message;
    messageContainer.appendChild(messageText);

    // Apply styling based on message type
    if (type === "success") {
      messageContainer.style.backgroundColor = "#4CAF50"; // green
      messageContainer.style.color = "#fff";
    } else if (type === "error") {
      messageContainer.style.backgroundColor = "#f44336"; // red
      messageContainer.style.color = "#fff";
    } else if (type === "info") {
      messageContainer.style.backgroundColor = "#2196F3"; // blue
      messageContainer.style.color = "#fff";
    }

    // Append the message container to the body
    document.body.appendChild(messageContainer);

    // Fade in the message
    setTimeout(() => {
      messageContainer.style.opacity = "1";
    }, 10); // Small delay to ensure transition works

    // Hide and remove the message after 5 seconds
    setTimeout(() => {
      messageContainer.style.opacity = "0";
      setTimeout(() => {
        document.body.removeChild(messageContainer);
      }, 300); // Wait for the transition to complete before removing
    }, 3000);
  }

  function fetchRecommendedTrailers() {
    fetch("http://127.0.0.1:5000/recommend_trailers")
      .then((response) => response.json())
      .then((trailers) => {
        trailersContainer.innerHTML = ""; // Clear existing trailers

        trailers.forEach((trailer) => {
          const trailerItem = document.createElement("div");
          trailerItem.classList.add("trailer-item");

          const iframe = document.createElement("iframe");
          iframe.src = trailer.trailer_url;
          trailerItem.appendChild(iframe);

          trailersContainer.appendChild(trailerItem);
        });
      })
      .catch((error) =>
        console.error("Error fetching recommended trailers:", error)
      );
  }
  fetchRecommendedTrailers();

  document
    .getElementById("view All")
    .addEventListener("click", function (event) {
      event.preventDefault();
      location.reload();
    });
});
