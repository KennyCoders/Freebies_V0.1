document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');

    // Fetch games from the JSON file
    fetch('games.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched data:', data);

            // Extract the games array from the data object
            const games = data.games;

            if (!Array.isArray(games)) {
                throw new Error('Games data is not an array');
            }

            // Group games by platform
            const groupedGames = games.reduce((acc, game) => {
                if (!acc[game.platform]) {
                    acc[game.platform] = [];
                }
                acc[game.platform].push(game);
                return acc;
            }, {});

            console.log('Grouped games:', groupedGames);

            // Iterate through each platform in the grouped data
            Object.keys(groupedGames).forEach(platform => {
                const tilesContainer = document.getElementById(`${platform}-tiles`);
                console.log(`Looking for container: ${platform}-tiles`);

                if (tilesContainer) {
                    console.log(`Found container for ${platform}`);
                    groupedGames[platform].forEach(game => {
                        const article = document.createElement('article');
                        article.innerHTML = `
                            <a href="${game.link}" target="_blank">
                                <div class="image">
                                    <img src="${game.image}" alt="${game.title}" />
                                </div>
                                <h2>${game.title}</h2>
                            </a>
                            <div class="video-container"></div>
                        `;
                        article.setAttribute('data-trailer', game.trailer);
                        tilesContainer.appendChild(article);
                    });
                } else {
                    console.error(`Container not found for ${platform}`);
                }
            });

            // Event listener for game tiles
            document.querySelectorAll('.tiles article').forEach(article => {
                article.addEventListener('click', function(event) {
                    // Prevent the default link behavior
                    event.preventDefault();

                    const videoContainer = this.querySelector('.video-container');

                    // If video is already playing, do nothing
                    if (videoContainer.querySelector('iframe')) {
                        console.log('Video already playing, doing nothing');
                        return;
                    }

                    // Load the YouTube video
                    const trailerUrl = this.getAttribute('data-trailer');
                    console.log('Trailer URL:', trailerUrl);
                    
                    if (!trailerUrl) {
                        console.error('No trailer URL found');
                        return;
                    }

                    // Show loading indicator
                    videoContainer.innerHTML = '<div class="loading">Loading video...</div>';

                    const embedUrl = trailerUrl.replace('watch?v=', 'embed/') + '?autoplay=1';
                    console.log('Embed URL:', embedUrl);

                    const iframe = document.createElement('iframe');
                    iframe.src = embedUrl;
                    iframe.width = '100%';  // Set width to 100%
                    iframe.height = '100%';  // Set height to 100%
                    iframe.frameBorder = '0';
                    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
                    iframe.allowFullscreen = true;

                    // Replace loading indicator with the iframe
                    videoContainer.innerHTML = '';
                    videoContainer.appendChild(iframe);

                    // Add the 'playing' class to show the video
                    this.classList.add('playing');
                });
            });
        })
        .catch(error => {
            console.error('Error fetching or processing data:', error);
        });
});
