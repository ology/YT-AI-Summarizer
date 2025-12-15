chrome.action.onClicked.addListener((tab) => {
    if (!tab.url) return;

    console.log("Sending URL:", tab.url);

    fetch("http://192.168.99.50:8000/api/url", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: tab.url })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);
        chrome.action.setBadgeText({ text: "OK", tabId: tab.id });
        chrome.action.setBadgeBackgroundColor({ color: "#4CAF50" });
        setTimeout(() => {
            chrome.action.setBadgeText({ text: "", tabId: tab.id });
        }, 1500);
    })
    .catch(error => {
        console.error("Error:", error);
        chrome.action.setBadgeText({ text: "ERR", tabId: tab.id });
        chrome.action.setBadgeBackgroundColor({ color: "#F44336" });
    });
});
