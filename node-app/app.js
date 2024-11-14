const axios = require('axios');

async function analyzeSentiment(text) {
  try {
    const response = await axios.post('http://localhost:5000/classify_genre', {
      text: text
    });

    console.log('Sentiment:', response.data.sentiment);
    console.log('Probabilities:', response.data.probabilities);
    
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
  }
}

analyzeSentiment("To bake a simple vanilla cake, start by preheating your oven to 350°F (175°C) and greasing two 9-inch round cake pans. In a bowl, mix together the dry ingredients—flour, baking powder, and salt. In a separate large bowl, beat together softened butter and sugar until light and fluffy, then add eggs one at a time, followed by vanilla extract. Gradually add the dry ingredients to the butter mixture, alternating with milk, and mix until just combined. Pour the batter evenly into the prepared pans and bake for 25-30 minutes, or until a toothpick inserted in the center comes out clean. Let the cakes cool before frosting with your favorite frosting or enjoying them plain.");
