const axios = require('axios');

async function analyzeGenre(text) {
  try {
    const response = await axios.post('http://localhost:5000/classify_genre', {
      text: text
    });

    console.log('Predicted Genre:', response.data.predicted_genre);
    console.log('Probabilities:', response.data.probabilities);
    
  } catch (error) {
    console.error('Error analyzing genre:', error);
  }
}

async function getSuggestions(text) {
  try {
    const response = await axios.post('http://localhost:5000/generate-suggestions', {
      text: text
    });

    let str = response.data.suggestions; // Assuming this is the string
    let newStr = str.replace(text, ''); // Remove 'RemoveThisText' from the start
    console.log(newStr);
    
  } catch (error) {
    console.error('Error generating suggestions:', error);
  }
}
text = "Late at night, Lisa awoke to the sound of soft footsteps echoing through the dark house. She checked the hallway, but it was empty. Shrugging it off, she returned to bed, only to catch a glimpse of herself in the full-length mirror across the room. The reflection grinned back at her—not the tired, startled face she knew, but a wide, malicious smile, twisting as if it were someone else wearing her skin. As her heart raced, the reflection lifted a finger to its lips, whispering, Don't wake up."
//analyzeGenre(text);
getSuggestions(text);