// script.js
const form = document.getElementById("ngram-form");
const resultDiv = document.getElementById("result");
const ngramList = document.getElementById("ngram-list");

// Your API URL
const API_URL = "https://your-project-name.vercel.app/ngrams";

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
                top_n: 10, // Fetch top 10 n-grams
            }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch n-grams");
        }

        const data = await response.json();

        // Update results on the page
        ngramList.innerHTML = "";
        data.top_ngrams.forEach((ngram) => {
            const listItem = document.createElement("li");
            listItem.textContent = `${ngram.phrase} (${ngram.count})`;
            ngramList.appendChild(listItem);
        });
    } catch (error) {
        console.error(error);
        ngramList.innerHTML = "<li>Something went wrong. Please try again.</li>";
    }
});
