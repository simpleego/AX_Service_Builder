export const toCelsius = value => (value - 32) * 5 / 9;
export const toFahrenheit = value => value * 9 / 5 + 32;
export function parseTemperature(text) {
  const trimmed = text.trim();
  // 소수와 부호를 허용하고, '12abc', Infinity, 지수 표기는 거부합니다.
  if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(trimmed)) return null;
  const value = Number(trimmed);
  return Number.isFinite(value) ? value : null;
}
export function convertText(text, converter) {
  const value = parseTemperature(text);
  if (value === null) return '';
  const output = converter(value);
  return Number.isFinite(output) ? String(Math.round(output * 1000) / 1000) : '';
}
