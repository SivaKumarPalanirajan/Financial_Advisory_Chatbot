$(document).ready(function() {
    $("#sendbutton").click(function() {
        var userMessage = $("#user-input").val();
        sendMessage(userMessage);
    });

    // Function to send user message to the server
    function sendMessage(userMessage) {
        // Make an AJAX POST request to your Flask route
        $.post("/chat", { user_message: userMessage }, function(data) {
            var botResponse = data.bot_response;
            // Display the bot's response in the chatbox
            $("#chatbox").append("<p>User: " + userMessage + "</p>");
            $("#chatbox").append("<p>Bot: " + botResponse + "</p>");
            // Clear the user input field
            $("#user-input").val("");
        });
    }
});