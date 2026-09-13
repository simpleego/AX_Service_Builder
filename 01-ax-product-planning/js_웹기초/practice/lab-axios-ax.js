import axios from 'axios';

const aiApi = axios.create({
  baseURL: 'https://api.openai.com/v1',
  headers: { 'Authorization': `Bearer ${process.env.OPENAI_API_KEY}` },
  timeout: 60000
});

async function chat(prompt){
  const { data } = await aiApi.post('/chat/completions', {
    model: 'gpt-4o-mini',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.7
  });
  return data.choices[0].message.content;
}
