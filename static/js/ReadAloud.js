<<<<<<< HEAD
function readAloud(text) {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.8; // Slower for seniors
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    window.speechSynthesis.speak(utterance);
  } else {
    alert('Read aloud is not supported in your browser. Please call our helpline for assistance.');
  }
=======
function readAloud(text) {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.8; // Slower for seniors
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    window.speechSynthesis.speak(utterance);
  } else {
    alert('Read aloud is not supported in your browser. Please call our helpline for assistance.');
  }
>>>>>>> 79692b4 (Initial commit)
}
