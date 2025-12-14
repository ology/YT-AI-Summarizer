document.getElementById('sendBtn').addEventListener('click', async () => {
    const statusDiv = document.getElementById('result');
    statusDiv.style.display = 'block';
    statusDiv.innerText = "Sending...";
    // get current active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.url) {
        statusDiv.innerText = "Error: No URL found";
        return;
    }
    try {
        const response = await fetch("http://192.168.99.50:8000/api/url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: tab.url })
        });
        const html = await response.text();
        statusDiv.className = "success";
        statusDiv.innerHTML = html;
    } catch (error) {
        statusDiv.className = "error";
        statusDiv.innerText = "Failed to connect to server.";
    }
});