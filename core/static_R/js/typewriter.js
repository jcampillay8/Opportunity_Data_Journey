const typewriterText = ["Finances", "Business", "Thecnologies", "Investment", "Engineer"];
let textPosition = 0;
let index = 0;

function typeWriter() {
  if (textPosition < typewriterText.length) {
    let currentText = typewriterText[textPosition];
    let letter = currentText.slice(0, ++index);

    document.getElementById('typewriter').textContent = letter;
    if (letter.length === currentText.length) {
      textPosition++;
      index = 0;
      setTimeout(typeWriter, 1000);
    } else {
      setTimeout(typeWriter, 80);
    }
  } else {
    textPosition = 0;
    setTimeout(typeWriter, 1000);
  }
}

typeWriter();