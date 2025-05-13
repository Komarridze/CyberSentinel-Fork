document.addEventListener("DOMContentLoaded", function()
{
    const form = document.getElementById("register-form");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");

    form.addEventListener("submit", function(event) 
    {
        let valid = true;
        emailError.style.display = "none";
        passwordError.style.display = "none";

        // Email validation
        const emailPattern = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
        if (!emailPattern.test(emailInput.value))
        {
            emailError.textContent = "Please enter a valid email address.";
            emailError.style.display = "block";
            valid = false;
        }

        // Password validation (minimum 8 characters, at least 1 number)
        if (passwordInput.value.lenght < 8 || !/\d/.test(passwordInput.value))
        {
            passwordError.textContent = "Password must be at least 8 characters long and contain at least one number";
            passwordError.style.display = "block";
            valid = false;
        }

        if (!valid)
        {
            event.preventDefault();
        }
    });
});