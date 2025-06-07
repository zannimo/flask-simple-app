const API_BASE = 'https://skwzmtuvsd.execute-api.us-east-1.amazonaws.com/dev';

function displayMovies(movies) {
  const container = document.getElementById('movies-container');
  container.innerHTML = '';

  movies.forEach(movie => {
    const div = document.createElement('div');
    div.className = 'movie-card';
    div.innerHTML = `
      <img src="${movie.cover_url}" alt="${movie.title}" />
      <h3>${movie.title}</h3>
      <p>${movie.genre} (${movie.year})</p>
      <button onclick="getSummary('${movie.id}')">Get Summary</button>
      <div id="summary-${movie.id}" class="summary"></div>
    `;
    container.appendChild(div);
  });
}

function fetchAllMovies() {
  fetch(`${API_BASE}/getmovies`)
    .then(res => res.json())
    .then(data => displayMovies(data.movies))
    .catch(err => console.error('Error fetching movies:', err));
}

function fetchMoviesByYear() {
  const year = document.getElementById('yearInput').value;
  if (!year) return;

  fetch(`${API_BASE}/getmoviesbyyear/${year}`)
    .then(res => res.json())
    .then(data => displayMovies(data.movies))
    .catch(err => console.error('Error fetching by year:', err));
}

function getSummary(movieId) {
  fetch(`${API_BASE}/getmoviesummary/${movieId}`)
    .then(res => res.json())
    .then(data => {
      const summaryDiv = document.getElementById(`summary-${movieId}`);
      summaryDiv.innerText = data.summary || 'No summary available.';
    })
    .catch(err => console.error('Error fetching summary:', err));
}

// Initial load
fetchAllMovies();
