async function askQuestion() {

    const input = document.getElementById("question");

    const question = input.value.trim();

    if (question === "") {
        return;
    }

    addMessage(question, "user");

    input.value = "";

    try {

        const response = await fetch("/ask", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        addMessage(data.answer, "bot");

    } catch (error) {

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

    }
}


function addMessage(text, type) {

    const chatBox = document.getElementById("chat-box");

    const message = document.createElement("div");

    message.className = "message " + type;

    if (type === "bot") {

        message.innerHTML = `
            <div class="message-icon">🤖</div>
            <div class="message-text">${text}</div>
        `;

    } else {

        message.innerHTML = `
            <div class="message-icon">👤</div>
            <div class="message-text">${text}</div>
        `;
    }

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function quickQuestion(question) {

    const input = document.getElementById("question");

    input.value = question;

    askQuestion();
}


function handleKey(event) {

    if (event.key === "Enter") {
        askQuestion();
    }

}