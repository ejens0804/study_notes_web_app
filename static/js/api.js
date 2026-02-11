// File: static/js/api.js

let requestCount = 0;

async function fetchData(endpoint) {
    requestCount++;
    document.getElementById('requestCount').textContent = requestCount;
    
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    
    loading.style.display = 'block';
    result.textContent = '';

    try {
        const response = await fetch(endpoint);
        const data = await response.json();
        
        loading.style.display = 'none';
        result.textContent = JSON.stringify(data, null, 2);
        document.getElementById('lastStatus').textContent = '✓';
    } catch (error) {
        loading.style.display = 'none';
        result.textContent = 'Error: ' + error.message;
        document.getElementById('lastStatus').textContent = '✗';
    }
}