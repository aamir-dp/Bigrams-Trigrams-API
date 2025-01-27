// Define the API URL
const API_URL = "https://bigrams-trigrams-api.onrender.com/ngrams"; // Replace with your Render API URL

const form = document.getElementById("ngram-form");
const ngramList = document.getElementById("ngram-list");

form.addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent default form submission

    const text = document.getElementById("input-text").value;
    const ngramSize = document.getElementById("ngram-size").value;
    const apiKey = document.getElementById("api-key").value; // Get the API key from the form

    if (!text.trim() || !apiKey.trim()) {
        alert("Please enter the text and API key.");
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "api_key": apiKey, // Pass the API key from the input
            },
            body: JSON.stringify({
                text: text, // Pass the text
                ngram_size: parseInt(ngramSize), // Pass the n-gram size
            }),
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch n-grams: ${response.statusText}`);
        }

        const data = await response.json();

        // Display the n-grams in the list
        ngramList.innerHTML = data.keywords
            .map((ngram) => `<li>${ngram.keyword} (${ngram.count})</li>`)
            .join("");
    } catch (error) {
        console.error("Error:", error);
        ngramList.innerHTML = "<li>Something went wrong. Please try again.</li>";
    }
});
