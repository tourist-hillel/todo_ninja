document.addEventListener('DOMContentLoaded', function() {
    const price1 = document.querySelector('#id_form-0-price');
    const fieldDescription = document.querySelectorAll('.field-description');
    if (fieldDescription.innerText === '-') {
        fieldDescription.innerText = 'Not provided';
    }
    price1.addEventListener('input', function() {
        if (parseFloat(this.value) > 5.0) {
            this.style.border = '2px solid red';
        } else {
            this.style.border = '2px solid green';
        }
    });
    const price2 = document.querySelector('#id_form-1-price');
    price2.addEventListener('input', function() {
        if (parseFloat(this.value) > 5.0) {
            this.style.border = '2px solid red';
        } else {
            this.style.border = '2px solid green';
        }
    });
});