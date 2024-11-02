// create a class that controls chatbot buttons and chatbot messages
class Chatbot {
    // create a constructor that will initialize the class
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            inputField: document.querySelector('.chatbox__footer textarea')
        }
        // create an object that will store the state of the chatbot
        this.state = false;
        this.messages = [];
        this.typingInterval = null;
    }

    // create a method that will open the chatbot
    display() {
        // Refresh selectors in case they were not available at construction
        this.args.openButton = document.querySelector('.chatbox__button button');
        this.args.chatBox = document.querySelector('.chatbox__support');
        this.args.sendButton = document.querySelector('.send__button');
        this.args.inputField = document.querySelector('.chatbox__footer textarea');

        const { openButton, chatBox, sendButton, inputField } = this.args;

        if (openButton) {
            openButton.onclick = () => this.toggleState(chatBox);
        }

        if (sendButton) {
            sendButton.onclick = () => this.onSendButton(chatBox);
        }

        if (inputField) {
            inputField.onkeydown = (event) => {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault(); // Prevent line break on Enter
                    this.onSendButton(chatBox);
                }
            };
        }
    }

    // create a method that will toggle the chatbot state
    toggleState(chatBox) {
        this.state = !this.state;
        // shows or hide the chatbox
        if (this.state) {
            chatBox.classList.add('chatbox--active');
        } else {
            chatBox.classList.remove('chatbox--active');
        }
    }

    // create a method that will handle the send button
    async onSendButton(chatBox) {
        const { inputField, sendButton } = this.args;
        const text1 = inputField.value.trim();
        if (text1 === '') {
            return;
        }

        // Disable input and button during processing
        inputField.disabled = true;
        sendButton.disabled = true;

        // Retrieve or create the session ID from cookies
        let sessionId = this.getCookie('session_id');
        if (!sessionId) {
            sessionId = this.createSessionId();
            this.setCookie('session_id', sessionId, 365); // Expire in 365 days
        }

        try {
            // create an object that will store the message
            // Note: IP and Timestamp are now handled by the backend
            let msg1 = { name: 'User', message: text1 };
            this.messages.push(msg1);
            this.updateChatText(chatBox);

            // Start the typing animation
            this.startTypingAnimation(chatBox);

            // chatbot response
            const response = await fetch('/agent', {
                method: 'POST',
                body: JSON.stringify({ message: text1, config: sessionId }),
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const r = await response.json();

            // Stop the typing animation
            this.stopTypingAnimation(chatBox);

            // create an object that will store the chatbot response
            let msg2 = { name: 'Chatbot', message: r.answer || "Sorry, I couldn't process that." };
            this.messages.push(msg2);
            this.updateChatText(chatBox);
            inputField.value = ''; // Clear the textarea

        } catch (error) {
            console.error('Error in onSendButton:', error);
            this.stopTypingAnimation(chatBox);
            let errorMsg = { name: 'Chatbot', message: 'Error: Could not reach the agent. Please try again later.' };
            this.messages.push(errorMsg);
            this.updateChatText(chatBox);
        } finally {
            // Re-enable input and button after processing (always runs)
            inputField.disabled = false;
            sendButton.disabled = false;
            inputField.focus();
        }
    }


    // create a method that will start the typing animation
    startTypingAnimation(chatBox) {
        let typingMsg = { name: 'Chatbot', message: 'Agent is typing ' };
        this.messages.push(typingMsg);
        const animationChars = ['|', '/', '-', '\\'];
        let charIndex = 0;

        this.typingInterval = setInterval(() => {
            typingMsg.message = 'Agent is typing ' + animationChars[charIndex];
            this.updateChatText(chatBox);
            charIndex = (charIndex + 1) % animationChars.length;
        }, 100);
    }

    // create a method that will stop the typing animation
    stopTypingAnimation(chatBox) {
        if (this.typingInterval) {
            clearInterval(this.typingInterval);
            this.typingInterval = null;
        }
        // Remove the typing message
        this.messages = this.messages.filter(msg => !msg.message.startsWith('Agent is typing'));
        this.updateChatText(chatBox);
    }

    // create a method that will update the chat text
    updateChatText(chatBox) {
        var html = '';
        this.messages.forEach(function (item, index) {
            if (item.name === 'User') {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            }
            else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });
        const chatmessage = chatBox.querySelector('.chatbox__messages > div');
        if (chatmessage) {
            chatmessage.innerHTML = html;
        }

        // Scroll to the bottom of the chat messages
        const chatboxMessages = chatBox.querySelector('.chatbox__messages');
        if (chatboxMessages) {
            chatboxMessages.scrollTop = chatboxMessages.scrollHeight;
        }
    }

    // Helper function to create a session ID
    createSessionId() {
        const date = new Date();
        const mm = ('0' + (date.getMonth() + 1)).slice(-2);
        const dd = ('0' + date.getDate()).slice(-2);
        const yyyy = date.getFullYear();
        const randomNum = Math.floor(100 + Math.random() * 900);
        return `${mm}${dd}${yyyy}${randomNum}-agent_portfolio`;
    }

    // Helper function to set a cookie
    setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    // Helper function to get a cookie
    getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }
}
