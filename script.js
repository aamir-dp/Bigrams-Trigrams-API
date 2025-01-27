// script.js
const form = document.getElementById("ngram-form");
const resultDiv = document.getElementById("result");
const ngramList = document.getElementById("ngram-list");

// Your API URL
const API_URL = "http://127.0.0.1:8000/ngrams"; // Replace with your actual deployed URL

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Get user input
    const text = document.getElementById("input-text").value;
    const ngramSize = document.getElementById("ngram-size").value;

    // Send request to the API
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                text: text,
                ngram_size: parseInt(ngramSize),
            }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch n-grams");
        }

        const data = await response.json();

        // Update results on the page
        ngramList.innerHTML = "";
        data.keywords.forEach((ngram) => {
            const listItem = document.createElement("li");
            listItem.textContent = `${ngram.keyword} (${ngram.count})`;
            ngramList.appendChild(listItem);
        });
    } catch (error) {
        console.error(error);
        ngramList.innerHTML = "<li>Something went wrong. Please try again.</li>";
    }
});
