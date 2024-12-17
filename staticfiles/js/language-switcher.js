document.addEventListener('DOMContentLoaded', function() {
    // Handle language form submission
    const languageForms = document.querySelectorAll('.language-form');
    
    languageForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const language = formData.get('language');
            
            fetch('/i18n/setlang/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    // Store the selected language in localStorage
                    localStorage.setItem('selectedLanguage', language);
                    
                    // Force reload from server, not from cache
                    window.location.reload(true);
                }
            })
            .catch(error => {
                console.error('Error switching language:', error);
            });
        });
    });

    // Check if we need to restore a previously selected language
    const storedLanguage = localStorage.getItem('selectedLanguage');
    const currentLanguage = document.documentElement.lang;
    
    if (storedLanguage && storedLanguage !== currentLanguage) {
        // Find and submit the form for the stored language
        const form = document.querySelector(`form input[value="${storedLanguage}"]`).closest('form');
        if (form) {
            const formData = new FormData(form);
            
            fetch('/i18n/setlang/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload(true);
                }
            })
            .catch(error => {
                console.error('Error restoring language:', error);
            });
        }
    }

    // Update RTL/LTR
    const htmlElement = document.documentElement;
    if (currentLanguage === 'ar') {
        htmlElement.setAttribute('dir', 'rtl');
        document.body.classList.add('rtl');
    } else {
        htmlElement.setAttribute('dir', 'ltr');
        document.body.classList.remove('rtl');
    }
});
