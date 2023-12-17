document.addEventListener('DOMContentLoaded', function() {
    
        var pastelModeButton = document.getElementById('pastel-mode');
        if (pastelModeButton) {
            pastelModeButton.addEventListener('click', function() {
                if (document.documentElement.classList.contains('pastel')) {
                    document.documentElement.classList.remove('pastel');
                    localStorage.theme = 'light';
                } else {
                    document.documentElement.classList.add('pastel');
                    localStorage.theme = 'pastel';
                }
            });
        }
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








