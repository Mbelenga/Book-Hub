document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');

    // Makes the login page interactive
    registerBtn.addEventListener("click", () => {
        container.classList.add('active');
    });

    loginBtn.addEventListener("click", () => {
        container.classList.remove('active');
    });

    // Function to handle signup form submission
    document.querySelector('.sign-up form').addEventListener('submit', async (e) => {
        e.preventDefault();  // Prevent the default form submission

        const name = e.target.querySelector('input[placeholder="Name"]').value;
        const email = e.target.querySelector('input[placeholder="Email"]').value;
        const password = e.target.querySelector('input[placeholder="Password"]').value;

        try {
            // Send signup data to the backend
            const response = await fetch('http://127.0.0.1:5000/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: name, email: email, password: password })
            });

            const data = await response.json();
            if (response.status === 201) {
                alert('Signup successful. Please login.');
                container.classList.remove('active');  // Switch to login form
            } else {
                alert(data.message);
            }
        } catch (err) {
            console.error('Error:', err);
            alert('An error occurred. Please try again.');
        }
    });

    // Function to handle login form submission
    document.querySelector('.sign-in form').addEventListener('submit', async (e) => {
        e.preventDefault();  // Prevent the default form submission

        const email = e.target.querySelector('input[placeholder="Email"]').value;
        const password = e.target.querySelector('input[placeholder="Password"]').value;

        try {
            // Send login data to the backend
            const response = await fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, password: password })
            });

            const data = await response.json();
            if (response.status === 200) {
                localStorage.setItem('token', data.token);  // Store JWT token in localStorage
                window.location.href = 'home.html';  // Redirect to the home page
            } else {
                alert(data.message);
            }
        } catch (err) {
            console.error('Error:', err);
            alert('An error occurred. Please try again.');
        }
    });
});
