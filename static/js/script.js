// On page load or when changing themes, best to add inline in `head` to avoid FOUC
document.addEventListener('DOMContentLoaded', function() {
    var addPostUrlElement = document.getElementById('addPostUrl');
    if (addPostUrlElement) { // Проверка существования элемента
        addPostUrlElement.addEventListener('change', function() {
            if (this.files[0]) {
                var picture = new FileReader();
                picture.readAsDataURL(this.files[0]);
                picture.addEventListener('load', function(event) {
                    var addPostImage = document.getElementById('addPostImage');
                    if (addPostImage) {
                        addPostImage.setAttribute('src', event.target.result);
                        addPostImage.style.display = 'block';
                    }
                });
            }
        });
    }
});








