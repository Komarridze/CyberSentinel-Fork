document.addEventListener("DOMContentLoaded", function()
{
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;

    // Check localStorage for user preference
    if (localStorage.getItem("theme") === "light")
    {
        body.classList.add("light-mode");
    }

    themeToggle.addEventListener("click", function()
    {
        body.classList.toggle("light-mode");

        // Store user preference in localStorage
        if (body.classList.contains("light-mode"))
        {
            localStorage.setItem("theme", "light");
        }
        else
        {
            localStorage.setItem("theme", "dark");
        }
    });
});