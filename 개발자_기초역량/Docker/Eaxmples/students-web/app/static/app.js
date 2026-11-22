// 화면과 API가 같은 주소(같은 FastAPI)에서 나오므로 '/api/...' 만 쓰면 된다.
// → 주소(localhost, VM_IP)가 바뀌어도 코드 수정이 필요 없고, CORS 설정도 필요 없다.

const rowsEl = document.getElementById("rows");
const statusEl = document.getElementById("status");
const majorEl = document.getElementById("major");

async function loadStudents(major = "") {
  statusEl.className = "";
  statusEl.textContent = "불러오는 중…";

  const url = major
    ? `/api/students?major=${encodeURIComponent(major)}`
    : "/api/students";

  try {
    const res = await fetch(url);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    const students = await res.json();
    render(students);
    statusEl.textContent = `${students.length}명`;
  } catch (e) {
    rowsEl.innerHTML = "";
    statusEl.className = "error";
    statusEl.textContent = `오류: ${e.message}`;
  }
}

function render(students) {
  rowsEl.innerHTML = "";
  for (const s of students) {
    const tr = document.createElement("tr");
    // textContent로 넣어야 DB 값에 HTML이 들어 있어도 그대로 글자로 보인다 (XSS 방지)
    for (const value of [s.id, s.name, s.major ?? "", formatDate(s.created_at)]) {
      const td = document.createElement("td");
      td.textContent = value;
      tr.appendChild(td);
    }
    rowsEl.appendChild(tr);
  }
}

function formatDate(value) {
  // "2026-11-21T19:40:12" → "2026-11-21 19:40"
  return value ? value.replace("T", " ").slice(0, 16) : "";
}

document.getElementById("searchBtn").addEventListener("click", () => {
  loadStudents(majorEl.value.trim());
});
document.getElementById("resetBtn").addEventListener("click", () => {
  majorEl.value = "";
  loadStudents();
});
majorEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") loadStudents(majorEl.value.trim());
});

loadStudents();
