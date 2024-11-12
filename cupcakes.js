function generateCupcakeHTML(cupcake) {
    return `
        <div class="col-md-4 mb-4">
            <div class="card">
                <img class="card-img-top" src="${cupcake.image}" alt="${cupcake.flavor} cupcake">
                <div class="card-body">
                    <h5 class="card-title">${cupcake.flavor}</h5>
                    <p class="card-text">
                        Size: ${cupcake.size}<br>
                        Rating: ${cupcake.rating}
                    </p>
                </div>
            </div>
        </div>
    `;
}

async function showCupcakes() {
    const response = await axios.get('/api/cupcakes');
    const cupcakes = response.data.cupcakes;
    
    $('#cupcakes-list').empty();
    for (let cupcake of cupcakes) {
        const cupcakeHTML = generateCupcakeHTML(cupcake);
        $('#cupcakes-list').append(cupcakeHTML);
    }
}

$('#new-cupcake-form').on('submit', async function(evt) {
    evt.preventDefault();

    const flavor = $('#flavor').val();
    const size = $('#size').val();
    const rating = $('#rating').val();
    const image = $('#image').val();

    const newCupcakeResponse = await axios.post('/api/cupcakes', {
        flavor,
        size,
        rating,
        image
    });

    const newCupcake = newCupcakeResponse.data.cupcake;
    const newCupcakeHTML = generateCupcakeHTML(newCupcake);
    $('#cupcakes-list').append(newCupcakeHTML);
    $('#new-cupcake-form').trigger('reset');
});

$('#search-form').on('submit', async function(evt) {
    evt.preventDefault();
    const searchTerm = $('#search-term').val();
    const response = await axios.get('/api/cupcakes/search', {
        params: { q: searchTerm }
    });
    $('#cupcakes-list').empty();
    for (let cupcake of response.data.cupcakes) {
        const cupcakeHTML = generateCupcakeHTML(cupcake);
        $('#cupcakes-list').append(cupcakeHTML);
    }
});

// For real-time search (no submit required):
$('#search-term').on('input', async function() {
    const searchTerm = $(this).val();
    const response = await axios.get('/api/cupcakes/search', {
        params: { q: searchTerm }
    });
    $('#cupcakes-list').empty();
    for (let cupcake of response.data.cupcakes) {
        const cupcakeHTML = generateCupcakeHTML(cupcake);
        $('#cupcakes-list').append(cupcakeHTML);
    }
});

// Load cupcakes when page loads
$(showCupcakes); 