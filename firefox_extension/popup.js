document.getElementById('sendBtn').addEventListener('click', async () => {
    const statusDiv = document.getElementById('result');
    statusDiv.style.display = 'block';
    statusDiv.innerText = "Summarizing...";
    // get current active tab
    // const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const xbrowser = globalThis.browser ?? globalThis.chrome;
    const [tab] = await xbrowser.tabs.query({ active: true, currentWindow: true });
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
        const data = await response.json();
        statusDiv.className = "success";
        let text = 'Transcript:<p></p>' + data['transcript']
        text = text + '<p></p>Comments:<p></p>' + data['comments']
        statusDiv.innerHTML = text;
    } catch (error) {
        statusDiv.className = "error";
        statusDiv.innerText = "Failed to connect to server.";
    }
});