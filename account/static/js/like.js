$('.like-button').click(function() {
    var photoId = $(this).data('photo-id');

    $.post('{% url "like_create" %}', { 'photo_id': photoId })
        .done(function(data) {
            alert('Thank you for liking!');
        });
});
