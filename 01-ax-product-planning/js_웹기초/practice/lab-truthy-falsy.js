const falsyList = [false, 0, "", null, undefined, NaN];
falsyList.forEach(v => console.log(v, "->", v ? "truthy" : "falsy"));

console.log(Boolean([]), Boolean({}), Boolean("0"), Boolean("false"), Boolean(" "));

let tokenCount = 0;
if(!tokenCount) console.log("토큰 0개를 falsy로 보고 실패로 처리 - 버그");

let userName = "";
console.log(userName || "익명");
console.log(userName ?? "익명");

let score = 0;
console.log(score || 100);
console.log(score ?? 100);

const logs = [
  { id: 1, prompt: "보고서 써줘", tokens: 120 },
  { id: 2, prompt: "", tokens: 0 },
  { id: 3, prompt: "번역", tokens: null },
  { id: 4, prompt: "0", tokens: 50 },
];

function getValidPrompts(logs){ return logs.filter(log => log.prompt.trim() !== ""); }
function normalizeTokens(logs){ return logs.map(log => ({...log, tokens: log.tokens ?? 0})); }
function printLog(log){
  if(!log) return;
  if(!log.prompt){ console.log(`[ID:${log.id}] 프롬프트 없음`); return; }
  console.log(`[ID:${log.id}] ${log.prompt} (${log.tokens ?? 0} 토큰)`);
}
logs.forEach(printLog);
