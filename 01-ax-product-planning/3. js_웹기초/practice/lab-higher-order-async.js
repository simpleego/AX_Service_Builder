// AI 로그 분석기 실습
const aiLogs = [
  { user: '철수', prompt: '불량 원인?', tokens: 120, success: true, time: 1.2 },
  { user: '영희', prompt: '보고서 써줘', tokens: 800, success: true, time: 3.5 },
  { user: '철수', prompt: '번역해줘', tokens: 50, success: false, time: 0.8 },
  { user: '민수', prompt: '코드 짜줘', tokens: 600, success: true, time: 2.9 },
];

const successPrompts = aiLogs.filter(log => log.success).map(log => log.prompt);
console.log(successPrompts);

const tokenByUser = aiLogs.reduce((acc, log) => {
  acc[log.user] = (acc[log.user]||0) + log.tokens;
  return acc;
}, {});
console.log(tokenByUser);

function fakeAISummary(prompt){
  return new Promise(resolve => setTimeout(()=> resolve(`'${prompt}' 요약 완료`), 1000));
}

async function runAllSummary(){
  console.time('병렬 처리');
  const promises = aiLogs.map(log => fakeAISummary(log.prompt));
  const results = await Promise.all(promises);
  console.timeEnd('병렬 처리');
  console.log(results);
}
runAllSummary();
