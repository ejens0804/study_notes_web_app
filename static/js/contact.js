// File: static/js/contact.js

async function submitContact() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    if (!name || !email || !message) {
        alert('Please fill in all fields');
        return;
    }
    
    const contactOutput = document.getElementById('contactOutput');
    const contactResult = document.getElementById('contactResult');
    
    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, message })
        });
        
        const data = await response.json();
        
        contactOutput.style.display = 'block';
        contactResult.textContent = JSON.stringify(data, null, 2);
        
        // Clear form
        document.getElementById('name').value = '';
        document.getElementById('email').value = '';
        document.getElementById('message').value = '';
    } catch (error) {
        contactOutput.style.display = 'block';
        contactResult.textContent = 'Error: ' + error.message;
    }
}