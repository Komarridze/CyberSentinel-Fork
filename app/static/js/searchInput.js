document.addEventListener("DOMContentLoaded", function()
{
    const searchInput = document.querySelector("#search-form input[type='text']");

    searchInput.addEventListener("input", function() 
    {
        const query = this.value;

        fetch(`/api/search_logs?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                console.log("Search results: ", data);
            })
            .catch(error => console.error("Error during search: ", error));
    });
});