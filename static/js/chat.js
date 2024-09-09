class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => {
            console.log('Open button clicked');
            this.toggleState(chatBox);
        });

        sendButton.addEventListener('click', () => {
            console.log('Send button clicked');
            this.onSendButton(chatBox);
        });

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                console.log('Enter key pressed');
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
        
        console.log('Toggle state:', this.state);
    }

    
        // ... (other methods and constructor remain the same)
    
    onSendButton(chatbox) {
            var textField = chatbox.querySelector('input');
            let text1 = textField.value;
            if (text1 === "") {
                return;
            }
    
            if (text1.toLowerCase() === "exit") {
                // Close the chatbox
                this.toggleState(chatbox);
                textField.value = '';
                return;
            }
    
            let msg1 = { name: "User", message: text1 }
            this.messages.push(msg1);
    
            fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                body: JSON.stringify({ message: text1 }),
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(r => r.json())
            .then(r => {
                let msg2 = { name: "Sam", message: r.answer };
                this.messages.push(msg2);
                this.updateChatText(chatbox)
                textField.value = ''
            })
            .catch((error) => {
                console.error('Error:', error);
                this.updateChatText(chatbox)
                textField.value = ''
            });
    
            console.log('Send button clicked');
        }
    
    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;

        console.log('Chat text updated');
    }
}

const chatbox = new Chatbox();
chatbox.display();
