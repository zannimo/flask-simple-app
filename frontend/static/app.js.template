const API_BASE = '__API_GATEWAY_URL__';

const fetchAllBtn = document.getElementById("fetchAllBtn");
const filterByYearBtn = document.getElementById("filterByYearBtn");
const getSummaryBtn = document.getElementById("getSummaryBtn");

const yearInput = document.getElementById("yearInput");
const movieIdInput = document.getElementById("movieIdInput");
const summarySection = document.querySelector(".summary-section");
const moviesContainer = document.getElementById("moviesContainer");

fetchAllBtn.addEventListener("click", () => {
  fetch(`${API_BASE}/getmovies`)
    .then(res => res.json())
    .then(data => {
      if (data.movies) {
        displayMovies(data.movies);
        summarySection.classList.remove("hidden");
      }
    })
    .catch(err => console.error("Error fetching movies:", err));
});

filterByYearBtn.addEventListener("click", () => {
  const year = yearInput.value.trim();
  if (!year) return;

  fetch(`${API_BASE}/getmoviesbyyear/${year}`)
    .then(res => res.json())
    .then(data => {
      if (data.movies) {
        displayMovies(data.movies);
      }
    })
    .catch(err => console.error("Error filtering by year:", err));
});

getSummaryBtn.addEventListener("click", () => {
  const id = movieIdInput.value.trim();
  if (!id) return;

  fetch(`${API_BASE}/getmoviesummary/${id}`)
    .then(res => res.json())
    .then(data => {
      if (data.summary) {
        alert(`Summary: ${data.summary}`);
      }
    })
    .catch(err => console.error("Error fetching summary:", err));
});

function displayMovies(movies) {
  moviesContainer.innerHTML = "";

  movies.forEach(movie => {
    const card = document.createElement("div");
    card.className = "movie-card";

    card.innerHTML = `
      <img src="${movie.cover_url}" alt="${movie.title}" />
      <h3>${movie.title}</h3>
      <p><strong>Year:</strong> ${movie.year}</p>
      <p><strong>Genre:</strong> ${movie.genre}</p>
      <p><strong>ID:</strong> ${movie.id}</p>
    `;

    moviesContainer.appendChild(card);
  });
}
