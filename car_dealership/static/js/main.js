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

// Add CSRF token to all htmx requests
document.body.addEventListener('htmx:configRequest', function(evt) {
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
        evt.detail.headers['X-CSRFToken'] = csrftoken;
    }
});

// Rest of your existing code...
document.body.addEventListener('reviewUpdated', function(evt) {
    const reviewId = evt.detail.reviewId;
    const reviewElement = document.getElementById(`review-${reviewId}`);
    
    if (reviewElement) {
        reviewElement.classList.add('updated');
        setTimeout(() => {
            reviewElement.classList.remove('updated');
        }, 2000);
        reviewElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});

document.body.addEventListener('reviewDeleted', function(evt) {
    const carId = evt.detail.carId;
    htmx.ajax('GET', `/reviews/car/${carId}/review-form/`, '#review-form-container');
    showNotification('Review deleted successfully');
});

document.body.addEventListener('htmx:afterRequest', function(evt) {
    if (evt.detail.successful && evt.detail.target.classList.contains('review-form')) {
        const form = evt.detail.target.querySelector('form');
        if (form) {
            form.reset();
        }
    }
});

document.body.addEventListener('htmx:responseError', function(evt) {
    if (evt.detail.xhr.status === 400) {
        showNotification('Please check your review and try again', 'error');
    }
});

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 10px 20px;
        background-color: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        border-radius: 4px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

document.body.addEventListener("htmx:afterRequest", function (evt) {
			if (evt.detail.pathInfo.requestPath.includes("add-to-cart")) {
				let toast = new bootstrap.Toast(document.getElementById('cartToast'));
				toast.show();
			}
		});


// banner video pause background------------
document.getElementById('carouselExampleCaptions')
.addEventListener('slide.bs.carousel', function () {

    // pause all videos
    document.querySelectorAll("video").forEach(video => {
        video.pause();
        video.currentTime = 0;
    });
});

// play only active video
document.getElementById('carouselExampleCaptions')
.addEventListener('slid.bs.carousel', function () {
    let active = document.querySelector('.carousel-item.active video');
    if (active) active.play();
});
// -------------------