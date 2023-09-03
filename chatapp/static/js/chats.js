document.addEventListener("DOMContentLoaded", function () {
    const chatList = document.querySelector("#chat-list");
    const chatMessages = document.querySelector("#chat-messages");
    

    chatList.addEventListener("click", function (event) {
        if (event.target.tagName === "A") {
            event.preventDefault();
            const conversationId = event.target.getAttribute("data-conversation-id");
            console.log("Anchor tag clicked!");

            // Clear previous messages
            chatMessages.innerHTML = "Loading...";

            fetch(`/get_chat_messages/${conversationId}/`)
                .then((response) => response.json())
                .then((data) => {
                    chatMessages.innerHTML = ""; // Clear the "Loading..." message

                    if (data.messages.length === 0) {
                        chatMessages.innerHTML = "No messages available.";
                        return;
                    }

                    // Display the chat messages
                    data.messages.forEach((message) => {
                        const messageElement = document.createElement("li");
                        messageElement.textContent = `${message.user}: ${message.content} (${message.created_at})`;
                        chatMessages.appendChild(messageElement);
                    });
                })
                .catch((error) => {
                    console.error("Error fetching chat messages:", error);
                    chatMessages.innerHTML = "Failed to load messages.";
                });
        }
    });
});