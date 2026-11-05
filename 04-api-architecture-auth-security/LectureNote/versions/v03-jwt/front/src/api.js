// fetch를 감싼 공통 함수. 서버 오류 형식 {"error": {"code": "..."}}을 Error로 바꾼다.
export async function request(path, { method = 'GET', body, token } = {}) {
  const headers = {}
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(path, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  })

  if (res.status === 204) return null
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    const error = new Error(data?.error?.code ?? `HTTP_${res.status}`)
    error.status = res.status
    throw error
  }
  return data
}
