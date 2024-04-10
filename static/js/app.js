function add(){
  var newField = document.createElement('input');
  newField.setAttribute('type','text');
  newField.setAttribute('name', `text`);
  newField.setAttribute('class','form-control mt-1');
  formfield.appendChild(newField);
}

function remove(){
  var input_tags = formfield.getElementsByTagName('input');
  if(input_tags.length > 1) {
    formfield.removeChild(input_tags[(input_tags.length) - 1]);
  }
  counter -= 1;
}

function resetLinkStates() {
    const links = document.querySelectorAll('.attribute-link');
    links.forEach(link => {
        const linkId = link.getAttribute('id');
        localStorage.removeItem(linkId); // Remove the clicked state from local storage
        link.classList.remove('disabled-link'); // Remove the disabled visual state
        link.onclick = null; // Remove the click prevention
    });
}

