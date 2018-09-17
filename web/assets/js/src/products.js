$(document).ready(function() {

    $.ajax({
        url: '/etsy/listings/',
    }).done(function(response) {
        renderListings(response);
    });

    function renderListings(listings) {
        var $listingsContainer = $('#products__listings');
        listings.forEach(function(listing) {
            $listingsContainer.append(
                '<div class=\"product-listing\">' +
                    '<h4>' + listing.title + '</h4>' +
                    '<img src=\"' + listing.main_image.url_75x75 + '\">' +
                '</div>'
            );
        });
    }
});