const checkboxes = document.querySelectorAll('input[type="checkbox"]')

checkboxes.forEach(item => item.addEventListener('click', handleCheck));