document.addEventListener('DOMContentLoaded', function() 
{
    const banner = document.getElementById('cookie-banner');
    const acceptBtn = document.getElementById('accept-btn');
    const rejectBtn = document.getElementById('reject-btn');

    // Check if user consent is already given
    if (localStorage.getItem('cookieConsent'))
    {
        banner.style.display = 'none';
    }

    acceptBtn.addEventListener('click', function() 
    {
        localStorage.setItem('cookieConsent', 'accepted');
        banner.style.display = 'none';
    });

    rejectBtn.addEventListener('click', function()
    {
        localStorage.setItem('cookieConsent', 'rejected');
        banner.style.display = 'none';
    });
});