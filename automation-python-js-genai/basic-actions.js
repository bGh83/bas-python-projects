
// basic-actions.js

var element = null;
function setElement(identifier) {
    element = document.querySelector(identifier);
}

function getElement() {
    if(!element)
        throw new Error("Element issue");
    return element;
}

// function to type some text in an element such as textbox, text area etc.
function send(value) {        
    setElement('textarea[name="q"]');    
    getElement().value = value;    
}

// function to click some element such as button, hyperlink etc.
function click() {    
    setElement('input[name="btnK"]');        
    getElement().click();        
}

function openWebPage() {
    window.open('https://www.google.com');
}

