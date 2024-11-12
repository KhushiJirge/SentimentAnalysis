const axios = require('axios');

async function analyzeSentiment(text) {
  try {
    const response = await axios.post('http://localhost:5000/analyze_sentiment', {
      text: text
    });

    console.log('Sentiment:', response.data.sentiment);
    console.log('Probabilities:', response.data.probabilities);
    
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
  }
}

// Example usage
analyzeSentiment("I ain't sad");
