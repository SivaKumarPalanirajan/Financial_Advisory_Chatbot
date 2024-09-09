// Get references to the required elements
const importCsvButton = document.querySelector('.importCsvButton');
const inputText = document.querySelector('.chatbox__footer input[type="text"]');
const messagesContainer = document.querySelector('.chatbox__messages');

// Add a click event listener to the "Import CSV" button
importCsvButton.addEventListener('click', function() {
  // Create a file input element
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = '.xlsx';

  // Listen for the file selection
  fileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];

    // Read the contents of the CSV file
    const reader = new FileReader();
    reader.onload = function(e) {
      const csvContents = e.target.result;

      // Process the CSV contents (replace this with your processing logic)
      // For demonstration purposes, we'll just display the CSV contents in a message
      const csvMessage = document.createElement('div');
      csvMessage.classList.add('messages__item', 'messages__item--operator');
      csvMessage.textContent = 'CSV Contents: ' + csvContents;
      messagesContainer.appendChild(csvMessage);
    };
    
    reader.readAsText(file);
  });

  // Trigger the file input dialog
  fileInput.click();
});


