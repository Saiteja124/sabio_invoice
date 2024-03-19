// document.addEventListener('DOMContentLoaded', function() {
//     const loginForm = document.getElementById('loginForm');
//     const uploadForm = document.getElementById('uploadForm');
//     const uploadStatus = document.getElementById('uploadStatus');
//     const uploadSection = document.getElementById('uploadSection');
//     const downloadButton = document.getElementById('downloadCSV');
//     let uploadedFileName = '';

//     let isAuthenticated = false; // Track authentication status

//     loginForm.addEventListener('submit', function(event) {
//         event.preventDefault();
//         const username = loginForm.querySelector('#username').value.trim();
//         const password = loginForm.querySelector('#password').value.trim();

//         // Validate username and password
//         if (!isValidCredentials(username, password)) {
//             alert('Invalid username or password.');
//             return;
//         }

//         // Send login data to server for authentication
//         fetch('/login', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 username: username,
//                 password: password,
//             }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 alert('Login successful!');
//                 loginContainer.style.display = 'none'; // Hide the login container
//                 uploadContainer.style.display = 'block'; // Display the upload container
//                 // isAuthenticated = true; // Set authentication status to true
//                 // uploadSection.style.display = 'block'; // Display the upload form
//                 // loginForm.querySelector('button[type="submit"]').disabled = true; // Disable the login button
//             } else {
//                 alert('Authentication failed. ' + data.message);
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert('An error occurred during authentication.');
//         });
//     });

//     uploadForm.addEventListener('submit', function(event) {
//         event.preventDefault();

//         // Check if the user is authenticated before allowing file upload
//         // if (!isAuthenticated) {
//         //     alert('Please log in before uploading a file.');
//         //     return;
//         // }

//         const fileInput = uploadForm.querySelector('#pdfFile');
//         const file = fileInput.files[0];
//         if (file) {
//             // Create a FormData object to send the file to the server
//             const formData = new FormData();
//             formData.append('pdf_file', file);

//             // Use Fetch API to send the file to the server for processing
//             fetch('/process_text', {
//                 method: 'POST',
//                 body: formData
//             })
//             .then(response => response.json())
//             .then(data => {
//                 // Display the server response or handle further actions
//                 if (data.success) {
//                     uploadStatus.innerText = 'PDF processed successfully.';

//                     // Enable the download button
//                     downloadButton.disabled = false;
//                     // Store the uploaded filename for later use
//                     uploadedFileName = file.name;
//                 } else {
//                     uploadStatus.innerText = 'Error processing PDF.';
//                 }
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//                 uploadStatus.innerText = 'Error processing PDF.';
//             });
//         } else {
//             uploadStatus.innerText = 'Please select a PDF file.';
//         }
//     });

//     downloadButton.addEventListener('click', function() {
//         // Make a request to the server to initiate the download
//         fetch('/download_csv', {
//             method: 'GET',
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Download failed. Please try again.');
//             }
//             return response.text(); // Assuming the CSV data is sent as plain text
//         })
//         .then(csvData => {
//             // Create a Blob with the CSV data
//             const blob = new Blob([csvData], { type: 'text/csv' });
            
//             // Create a link element to trigger the download
//             const url = window.URL.createObjectURL(blob);
//             const a = document.createElement('a');

//             // Set the custom filename here (e.g., 'custom_filename.csv')
//             const customFilename = 'C:\PRASANNA_SABIO_FILES\Invoice_Project\Sabio_Intefrating_webpage\output\processed_result.csv';

//             a.href = url;
//             a.download = uploadedFileName.replace('.pdf', '.csv');
//             document.body.appendChild(a);
//             a.click();
//             document.body.removeChild(a);
//             window.URL.revokeObjectURL(url);
//             // Remove the downloading icon after download is complete
//             downloadButton.classList.remove('downloading');
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert(error.message);
//         });
//     });

//     function isValidCredentials(username, password) {
//         // Perform validation here
//         // Username must contain only alphabets
//         const usernamePattern = /^[A-Za-z0-9]+$/;
//         // For simplicity, let's assume any non-empty username and password is valid
//         return usernamePattern.test(username) && username !== '' && password !== '';
//     }
// });

uploadForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = uploadForm.querySelector('#pdfFile');
    const file = fileInput.files[0];
    if (file) {
        // You can perform PDF extraction here if necessary
        uploadStatus.innerText = 'PDF uploaded successfully: ' + file.name;
        loginForm.querySelector('button[type="submit"]').disabled = true; // Disable the login button after upload
    } else {
        uploadStatus.innerText = 'Please select a PDF file.';
    }
});


// downloadButton.addEventListener('click', function() {
//     // Generate and download the CSV file
//     // Replace this with your CSV generation logic
//     const csvData = 'Your CSV Data Here';
//     const blob = new Blob([csvData], { type: 'text/csv' });
//     const url = window.URL.createObjectURL(blob);
//     const a = document.createElement('a');
//     a.href = url;
//     a.download = uploadedFileName.replace('.pdf', '.csv');
//     a.download = 'data.csv';
//     document.body.appendChild(a);
//     a.click();
//     document.body.removeChild(a);
//     window.URL.revokeObjectURL(url);
//      // Remove the downloading icon after download is complete
//      downloadButton.classList.remove('downloading');
// });

// function isValidCredentials(username, password) {
//     // Perform validation here
//     // Username must contain only alphabets
//     const usernamePattern = /^[A-Za-z]+$/;
//     // For simplicity, let's assume any non-empty username and password is valid
//     return usernamePattern.test(username) && username !== '' && password !== '';
// }

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const uploadForm = document.getElementById('uploadForm');
    const uploadStatus = document.getElementById('uploadStatus');
    const uploadSection = document.getElementById('uploadSection');
    const downloadButton = document.getElementById('downloadCSV');
    let uploadedFileName = '';

    let isAuthenticated = false; // Track authentication status

    

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = loginForm.querySelector('#username').value.trim();
        const password = loginForm.querySelector('#password').value.trim();

        // Validate username and password
        if (!isValidCredentials(username, password)) {
            alert('Invalid username or password.');
            return;
        }

        // Send login data to server for authentication
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Login successful!');

                // Redirect to the upload page after successful login
                window.location.href = 'Sabio_use_cases';

                loginContainer.style.display = 'none'; // Hide the login container
                uploadContainer.style.display = 'block'; // Display the upload container
                // isAuthenticated = true; // Set authentication status to true
                // uploadSection.style.display = 'block'; // Display the upload form
                // loginForm.querySelector('button[type="submit"]').disabled = true; // Disable the login button
            } else {
                alert('Authentication failed. ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during authentication.');
        });
    });

    function isValidCredentials(username, password) {
        // Perform validation here
        // Username must contain only alphabets
        const usernamePattern = /^[A-Za-z0-9]+$/;
        // For simplicity, let's assume any non-empty username and password is valid
        return usernamePattern.test(username) && username !== '' && password !== '';
    }
});

    // Disable the download button initially
    // downloadButton.disabled = true;
//     uploadForm.addEventListener('submit', function(event) {
//         event.preventDefault();

//         // Check if the user is authenticated before allowing file upload
//         // if (!isAuthenticated) {
//         //     alert('Please log in before uploading a file.');
//         //     return;
//         // }

//         const fileInput = uploadForm.querySelector('#pdfFile');
//         const file = fileInput.files[0];
//         if (file) {
//             // Create a FormData object to send the file to the server
//             const formData = new FormData();
//             formData.append('pdf_file', file);

//             // Use Fetch API to send the file to the server for processing
//             fetch('/process_text', {
//                 method: 'POST',
//                 body: formData
//             })
//             .then(response => response.json())
//             .then(data => {
//                 // Display the server response or handle further actions
//                 if (data.success) {
//                     message='PDF processed successfully.'
//                     // uploadStatus.innerText = 'PDF processed successfully.';

//                     // Enable the download button
//                     downloadButton.disabled = false;
//                     // Store the uploaded filename for later use
//                     uploadedFileName = file.name;
//                 } 
//                 // else {
//                 //     uploadStatus.innerText = 'Error processing PDF.';
//                 // }
//             })
//             // .catch(error => {
//             //     console.error('Error:', error);
//             //     uploadStatus.innerText = 'Error processing PDF.';
//             //     // downloadButton.disabled = true; // Disable the download button
//             // });
//         } else {
//             uploadStatus.innerText = 'Please select a PDF file.';
//         }
//     });

//     downloadButton.addEventListener('click', function() {
//         // Make a request to the server to initiate the download
//         fetch('/download_csv', {
//             method: 'GET',
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Download failed. Please try again.');
//             }
//             return response.text(); // Assuming the CSV data is sent as plain text
//         })
//         .then(csvData => {
//             // Create a Blob with the CSV data
//             const blob = new Blob([csvData], { type: 'text/csv' });
            
//             // Create a link element to trigger the download
//             const url = window.URL.createObjectURL(blob);
//             const a = document.createElement('a');

//             // Set the custom filename here (e.g., 'custom_filename.csv')
//             // const customFilename = 'C:\PRASANNA_SABIO_FILES\Invoice_Project\Sabio_Intefrating_webpage\output\processed_result.csv';

//             a.href = url;
//             a.download = uploadedFileName.replace('.pdf', '.csv');
//             document.body.appendChild(a);
//             a.click();
//             document.body.removeChild(a);
//             window.URL.revokeObjectURL(url);
//             // Remove the downloading icon after download is complete
//             downloadButton.classList.remove('downloading');
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert(error.message);
//         });
//     });

//     function isValidCredentials(username, password) {
//         // Perform validation here
//         // Username must contain only alphabets
//         const usernamePattern = /^[A-Za-z0-9]+$/;
//         // For simplicity, let's assume any non-empty username and password is valid
//         return usernamePattern.test(username) && username !== '' && password !== '';
//     }
// });