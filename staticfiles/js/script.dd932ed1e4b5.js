// NatureCart AI Custom JavaScript Interactions

document.addEventListener("DOMContentLoaded", function () {
    // ----------------------------------------------------
    // 1. Dynamic CSRF Token Helper
    // ----------------------------------------------------
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
    const csrftoken = getCookie('csrftoken');

    // ----------------------------------------------------
    // 2. AI Chatbot AJAX System
    // ----------------------------------------------------
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatBody = document.getElementById("chat-body");

    if (chatForm && chatInput && chatBody) {
        // Scroll to bottom of chat initial state
        chatBody.scrollTop = chatBody.scrollHeight;

        chatForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const messageText = chatInput.value.trim();
            if (!messageText) return;

            // Append user message bubble
            appendMessage(messageText, "user");
            chatInput.value = "";

            // Show typing indicator
            const typingIndicator = appendTypingIndicator();
            chatBody.scrollTop = chatBody.scrollHeight;

            // AJAX request to backend
            fetch("/ai/chatbot/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({ message: messageText })
            })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                typingIndicator.remove();
                
                if (data.response) {
                    appendMessage(data.response, "bot");
                } else if (data.error) {
                    appendMessage("Sorry, I encountered an issue. Let's try again.", "bot");
                }
                chatBody.scrollTop = chatBody.scrollHeight;
            })
            .catch(error => {
                typingIndicator.remove();
                appendMessage("Network error. Please make sure your server is running.", "bot");
                chatBody.scrollTop = chatBody.scrollHeight;
            });
        });
    }

    function appendMessage(text, sender) {
        const bubble = document.createElement("div");
        bubble.className = `chat-bubble ${sender} animate-fade-in`;
        bubble.innerHTML = text;
        chatBody.appendChild(bubble);
    }

    function appendTypingIndicator() {
        const indicator = document.createElement("div");
        indicator.className = "chat-bubble bot animate-fade-in typing-indicator-bubble";
        indicator.innerHTML = '<span class="spinner-grow spinner-grow-sm text-success" role="status"></span><span class="spinner-grow spinner-grow-sm text-success mx-1" role="status"></span><span class="spinner-grow spinner-grow-sm text-success" role="status"></span>';
        chatBody.appendChild(indicator);
        return indicator;
    }

    // ----------------------------------------------------
    // 3. AI Sustainable Alternatives Finder System
    // ----------------------------------------------------
    const altSearchBtn = document.getElementById("alt-search-btn");
    const altSearchInput = document.getElementById("alt-search-input");
    const altResults = document.getElementById("alt-results");

    if (altSearchBtn && altSearchInput && altResults) {
        altSearchBtn.addEventListener("click", performAltSearch);
        altSearchInput.addEventListener("keypress", function (e) {
            if (e.key === 'Enter') {
                performAltSearch();
            }
        });
    }

    function performAltSearch() {
        const query = altSearchInput.value.trim();
        if (!query) {
            altResults.innerHTML = '<div class="alert alert-warning border-0 rounded-4">Please input a plastic item (e.g. toothbrush) to search!</div>';
            return;
        }

        altResults.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-success" role="status"><span class="visually-hidden">Loading...</span></div><p class="text-muted mt-2">Searching green databases...</p></div>';

        fetch(`/ai/alternatives/?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            altResults.innerHTML = "";
            
            if (data.results && data.results.length > 0) {
                data.results.forEach(item => {
                    const col = document.createElement("div");
                    col.className = "col-12 mt-3 animate-fade-in";
                    
                    const imgHtml = item.alt_image 
                        ? `<img src="${item.alt_image}" class="img-fluid rounded-4 shadow-sm" style="max-height: 140px; width: 100%; object-fit: cover;">` 
                        : `<div class="bg-light rounded-4 d-flex align-items-center justify-content-center text-muted" style="height: 140px; width:100%"><i class="fa-solid fa-leaf fs-1"></i></div>`;
                    
                    col.innerHTML = `
                        <div class="card border-0 shadow-sm rounded-4 p-3 bg-white">
                            <div class="row g-3 align-items-center">
                                <div class="col-md-3 col-sm-4 text-center">
                                    ${imgHtml}
                                </div>
                                <div class="col-md-9 col-sm-8">
                                    <div class="d-flex justify-content-between align-items-start mb-1 flex-wrap">
                                        <h5 class="fw-bold mb-1 text-success">${item.alt_name}</h5>
                                        <span class="badge bg-success-light text-success rounded-pill px-3 py-1">Save ₹ ${item.alt_price}</span>
                                    </div>
                                    <div class="d-flex gap-3 mb-2 flex-wrap text-muted fs-7 font-monospace">
                                        <span><i class="fa-solid fa-cloud text-success"></i> CO₂ Saved: ${item.co2_savings} kg</span>
                                        <span><i class="fa-solid fa-trash text-success"></i> Plastic Saved: ${item.plastic_savings} kg</span>
                                    </div>
                                    <p class="text-muted mb-3 fs-7">${item.reasoning}</p>
                                    <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                                        <span class="fs-8 text-decoration-line-through text-danger">Replaces: ${item.plastic_name}</span>
                                        <div class="d-flex gap-2">
                                            <a href="/product/${item.alt_id}/" class="btn btn-sm btn-outline-success rounded-pill px-3">View Specs</a>
                                            <a href="/cart/add/${item.alt_id}/" class="btn btn-sm btn-accent rounded-pill px-3">Quick Shop</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    altResults.appendChild(col);
                });
            } else {
                altResults.innerHTML = '<div class="alert alert-info border-0 rounded-4 text-center">No exact sustainable match found in database. Try searching for "toothbrush", "straws", "bottle", or "bag"!</div>';
            }
        })
        .catch(error => {
            altResults.innerHTML = '<div class="alert alert-danger border-0 rounded-4">An error occurred while connecting to the database.</div>';
        });
    }
});
