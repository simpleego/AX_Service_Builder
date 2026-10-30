import React, { useState } from 'react';
import { convertText, parseTemperature, toCelsius, toFahrenheit } from './temperature.js';
function TemperatureInput({ label, value, onChange }) {
  return <label>{label}<input inputMode="decimal" value={value} onChange={event => onChange(event.target.value)} /></label>;
}
export default function TemperaturePractice() {
  const [input, setInput] = useState({ scale: 'c', text: '' });
  const celsius = input.scale === 'c' ? input.text : convertText(input.text, toCelsius);
  const fahrenheit = input.scale === 'f' ? input.text : convertText(input.text, toFahrenheit);
  const raw = parseTemperature(input.text);
  const numericCelsius = raw === null ? null : input.scale === 'c' ? raw : toCelsius(raw);
  return <section>
    <TemperatureInput label="섭씨" value={celsius} onChange={text => setInput({ scale: 'c', text })} />
    <TemperatureInput label="화씨" value={fahrenheit} onChange={text => setInput({ scale: 'f', text })} />
    <p role="status">{numericCelsius === null ? '유효한 온도를 입력하세요.' : numericCelsius >= 100 ? '물이 끓는 온도입니다.' : '끓는점보다 낮습니다.'}</p>
    <small>표준 대기압의 물을 가정합니다. 표시값만 소수 셋째 자리로 반올림합니다.</small>
  </section>;
}
