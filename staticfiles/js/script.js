// API endpoints
const API_ENDPOINTS = {
    products: '/api/products/',
    reviews: '/api/reviews/',
    profile: '/api/users/profile/',
};

// Utility functions
const fetchAPI = async (endpoint, options = {}) => {
    const response = await fetch(endpoint, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            ...options.headers,
        },
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
};

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Product functions
async function loadProducts() {
    try {
        const products = await fetchAPI(API_ENDPOINTS.products);
        displayProducts(products);
    } catch (error) {
        console.error('Error loading products:', error);
        showAlert('Error loading products. Please try again later.', 'danger');
    }
}

function displayProducts(products) {
    const container = document.querySelector('#products-container');
    if (!container) return;

    container.innerHTML = products.map(product => `
        <div class="col-md-4 mb-4">
            <div class="card product-card">
                <img src="${product.image}" class="card-img-top product-image" alt="${product.name}">
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">${product.description}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="price">$${product.price}</span>
                        <button class="btn btn-primary" onclick="viewProduct(${product.id})">View Details</button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Review functions
async function submitReview(productId, rating, comment) {
    try {
        const review = await fetchAPI(API_ENDPOINTS.reviews, {
            method: 'POST',
            body: JSON.stringify({ product: productId, rating, comment }),
        });
        showAlert('Review submitted successfully!', 'success');
        return review;
    } catch (error) {
        console.error('Error submitting review:', error);
        showAlert('Error submitting review. Please try again.', 'danger');
    }
}

// Alert function
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('#alert-container');
    if (!alertContainer) return;

    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

// Initialize components when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Load products if we're on the products page
    if (document.querySelector('#products-container')) {
        loadProducts();
    }
    
    // Setup review form submission
    const reviewForm = document.querySelector('#review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const productId = reviewForm.dataset.productId;
            const rating = reviewForm.querySelector('#rating').value;
            const comment = reviewForm.querySelector('#comment').value;
            await submitReview(productId, rating, comment);
            reviewForm.reset();
        });
    }
});
