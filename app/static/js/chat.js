document.addEventListener("DOMContentLoaded", () => {
    // Connect to the Socket.IO server.
    const socket = io.connect(window.location.origin);
    const messageArea = document.getElementById("message-area");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");

    // Listen for incoming messages from the server on the correct event.
    socket.on("message", (data) => {
        // 'data' should be an object containing 'sender' and 'message'
        appendMessage(data.sender, data.message);
    });

    // Send message when the Send button is clicked.
    sendButton.addEventListener("click", sendMessage);

    // Allow sending a message by pressing Enter (without Shift)
    messageInput.addEventListener("keyup", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    // Function to send the message to the server.
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message !== "") {
            // Emit a custom "send_message" event carrying a JSON object.
            socket.emit("message", { message: message });
            messageInput.value = "";
        }
    }

    // Function to append a message to the chat area and style it.
    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");

        // Style differently based on the sender.
        if (sender === "User") {
            messageDiv.classList.add("chat-message");
        } else if (sender === "AI") {
            messageDiv.classList.add("ai-message");
        } else {
            messageDiv.classList.add("chat-message");
        }

        // Set the text with a sender prefix.
        messageDiv.textContent = `${sender}: ${message}`;

        messageArea.appendChild(messageDiv);

        // Auto-scroll to the bottom when a new message arrives.
        messageArea.scrollTop = messageArea.scrollHeight;
    }
});
