// Animate in the movie tiles
$('.movie-tile').hide().first().show('fast', function showNext() {
    $(this).next('article').show('fast', showNext);
});

// We'll show videos in a modal for modern browsers with JavaScript enabled
if ('matchMedia' in window) {
    // Disable video links
    $('.movie-tile a').removeAttr('href');

    // Pause the video when the modal is closed
    $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
        // Remove the src so the player itself gets removed, as this is the only
        // reliable way to ensure the video stops playing in IE
        $('#trailer-video-container').empty();
    });

    // Start playing the video whenever the trailer modal is opened
    $(document).on('click', '.movie-tile', function (event) {
        var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
        var sourceUrl = 'https://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
        $('#trailer-video-container').empty().append($('<iframe></iframe>', {
            'id': 'trailer-video',
            'type': 'text-html',
            'src': sourceUrl,
            'frameborder': 0
        }));
    });
} else {
    // Prevent video modal from opening, since it is not supported
    $('.movie-tile').removeAttr('data-target');
}
