// 서버 오류코드를 사용자에게 보여줄 한국어 문장으로 바꾼다.
const MESSAGES = {
  EMAIL_EXISTS: '이미 가입된 이메일입니다.',
  LOGIN_FAILED: '이메일 또는 비밀번호가 올바르지 않습니다.',
  VALIDATION_ERROR: '입력값을 확인해 주세요.',
  UNAUTHORIZED: '로그인이 필요합니다.',
  NO_REFRESH_TOKEN: '로그인이 필요합니다.',
  INVALID_REFRESH: '세션이 만료되었습니다. 다시 로그인해 주세요.',
  REFRESH_REUSED_OR_EXPIRED: '세션이 만료되었습니다. 다시 로그인해 주세요.',
  TODO_NOT_FOUND: '할 일을 찾을 수 없습니다.',
  OAUTH_NOT_CONFIGURED: '서버에 Google 로그인이 설정되지 않았습니다.',
  INVALID_STATE: 'Google 로그인 요청이 만료되었거나 올바르지 않습니다. 다시 시도해 주세요.',
  OAUTH_DENIED: 'Google 로그인이 취소되었습니다.',
  OAUTH_FAILED: 'Google 인증에 실패했습니다.',
  INVALID_HANDOFF: '로그인 코드가 만료되었습니다. 다시 시도해 주세요.',
  INTERNAL_ERROR: '서버 오류가 발생했습니다.',
};

/** 422 응답의 fields를 { email: '...', password: '...' } 형태로 바꾼다. */
export function fieldErrorsOf(error) {
  const result = {};
  for (const field of error?.fields || []) {
    const name = field.loc[field.loc.length - 1];
    if (name === 'email') result.email = '올바른 이메일 형식이 아닙니다.';
    else if (name === 'password') result.password = '비밀번호는 12자 이상 128자 이하여야 합니다.';
    else result[name] = field.message;
  }
  return result;
}

export function messageOf(error) {
  if (!error) return '';
  if (error.code && MESSAGES[error.code]) return MESSAGES[error.code];
  if (error instanceof TypeError) return '서버에 연결할 수 없습니다. 백엔드가 실행 중인지 확인하세요.';
  return error.message || '알 수 없는 오류가 발생했습니다.';
}
