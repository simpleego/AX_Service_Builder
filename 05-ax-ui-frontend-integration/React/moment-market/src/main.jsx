import React, {
  useState,
  useEffect,
  useReducer,
  useContext,
  createContext,
  useMemo,
  useCallback,
  useRef,
  useId,
  useDeferredValue,
  useTransition,
  useLayoutEffect,
  useImperativeHandle,
  forwardRef,
  useDebugValue,
} from "react";
import { createRoot } from "react-dom/client";
import {
  ShoppingBag,
  Search,
  Heart,
  ArrowUpRight,
  ArrowRight,
  X,
  Plus,
  Minus,
  Check,
  SlidersHorizontal,
  Code2,
  Sun,
  Moon,
  Package,
  Truck,
  RefreshCw,
} from "lucide-react";
import "./style.css";
const money = (n) => n.toLocaleString("ko-KR") + "원";
const items = [
  ["세라믹 라운드 머그", "키친", 18000, "photo-1514228742587-6b1558fcca3d"],
  ["내추럴 캔버스 토트", "패션", 29000, "photo-1553062407-98eeb64c6a62"],
  ["데스크 미니 조명", "리빙", 48000, "photo-1507473885765-e6ed057f782c"],
  ["우드 다이닝 체어", "리빙", 128000, "photo-1598300042247-d088f8ab3a91"],
  ["데일리 무선 헤드폰", "디지털", 89000, "photo-1546435770-a3e426bf472b"],
  ["슬로우 브루 커피메이커", "키친", 64000, "photo-1517668808822-9ebb02f2a0e6"],
  ["클래식 아날로그 워치", "패션", 78000, "photo-1524805444758-089113d48a6d"],
  [
    "포터블 블루투스 스피커",
    "디지털",
    59000,
    "photo-1608043152269-423dbba4e7e1",
  ],
  ["소프트 코튼 쿠션", "리빙", 24000, "photo-1584100936595-c0654b55a2e2"],
  ["에센셜 스니커즈", "패션", 69000, "photo-1549298916-b41d501d3772"],
  ["유리 플라워 베이스", "리빙", 22000, "photo-1578500494198-246f612d3b3d"],
  ["미니멀 데스크 노트", "문구", 12000, "photo-1531346878377-a5be20888e57"],
];
const image = (id, w = 650) =>
  `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&q=80`;
// 커스텀 훅: 초기 값을 지연 초기화하고 변경할 때 저장합니다.
// useDebugValue의 값은 React DevTools에서 확인합니다.
function useLocalStorage(key, initial) {
  const [v, set] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem(key)) ?? initial;
    } catch {
      return initial;
    }
  });
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(v));
    } catch {}
  }, [key, v]);
  useDebugValue(key);
  return [v, set];
}
// 커스텀 훅: API 요청·로딩·실패·재시도를 묶습니다.
// effect 정리 시 요청을 취소해 StrictMode와 화면 전환에 대응합니다.
function useProducts() {
  const [state, set] = useState({ data: [], loading: true, error: "" });
  const [retry, reload] = useReducer((n) => n + 1, 0);
  useEffect(() => {
    const c = new AbortController();
    set({ data: [], loading: true, error: "" });
    fetch("https://jsonplaceholder.typicode.com/posts?_limit=12", {
      signal: c.signal,
    })
      .then((r) => {
        if (!r.ok) throw Error("HTTP " + r.status);
        return r.json();
      })
      .then((data) =>
        set({
          data: data.map((p, i) => ({
            ...p,
            name: items[i][0],
            category: items[i][1],
            price: items[i][2],
            image: items[i][3],
          })),
          loading: false,
          error: "",
        }),
      )
      .catch((e) => {
        if (e.name !== "AbortError")
          set({
            data: [],
            loading: false,
            error: "상품을 불러오지 못했습니다. 네트워크 연결을 확인해 주세요.",
          });
      });
    return () => c.abort();
  }, [retry]);
  return { ...state, reload };
}
const ShopContext = createContext(null);
// 리듀서는 기존 배열을 직접 변경하지 않고 새 상태를 반환합니다.
function cartReducer(state, a) {
  if (a.type === "clear") return [];
  if (a.type === "add") {
    const old = state.find((p) => p.id === a.product.id);
    return old
      ? state.map((p) => (p.id === old.id ? { ...p, qty: p.qty + 1 } : p))
      : [...state, { ...a.product, qty: 1 }];
  }
  if (a.type === "qty")
    return state
      .map((p) => (p.id === a.id ? { ...p, qty: p.qty + a.delta } : p))
      .filter((p) => p.qty > 0);
  return state;
}
// Context로 여러 컴포넌트에서 사용하는 쇼핑 상태와 동작을 공유합니다.
function Provider({ children }) {
  const [saved, setSaved] = useLocalStorage("moment-cart", []);
  const [cart, dispatch] = useReducer(cartReducer, saved);
  const [favorites, setFavorites] = useLocalStorage("moment-likes", []);
  const [dark, setDark] = useLocalStorage("moment-dark", false);
  useEffect(() => setSaved(cart), [cart, setSaved]);
  const add = useCallback((product) => dispatch({ type: "add", product }), []);
  const like = useCallback(
    (id) =>
      setFavorites((v) =>
        v.includes(id) ? v.filter((x) => x !== id) : [...v, id],
      ),
    [setFavorites],
  );
  return (
    <ShopContext.Provider
      value={{ cart, dispatch, add, favorites, like, dark, setDark }}
    >
      {children}
    </ShopContext.Provider>
  );
}
// ref와 useImperativeHandle: 부모에게 DOM 전체 대신 focus 기능만 공개합니다.
const SearchBox = forwardRef(function SearchBox({ value, onChange }, ref) {
  const input = useRef(null),
    id = useId();
  useImperativeHandle(ref, () => ({ focus: () => input.current.focus() }), []);
  return (
    <div className="search">
      <Search size={18} />
      <label className="sr" htmlFor={id}>
        상품 검색
      </label>
      <input
        id={id}
        ref={input}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="어떤 순간을 찾고 있나요?"
      />
      <kbd>/</kbd>
    </div>
  );
});
// 레이아웃 effect로 표시 직후 초점을 이동하고 닫힐 때 복원합니다.
function Modal({ children, onClose, title }) {
  const ref = useRef(null),
    titleId = useId();
  useLayoutEffect(() => {
    const prev = document.activeElement;
    ref.current.focus();
    const old = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = old;
      prev?.focus();
    };
  }, []);
  return (
    <div className="overlay" onClick={onClose}>
      <section
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        tabIndex={-1}
        ref={ref}
        onClick={(e) => e.stopPropagation()}
        onKeyDown={(e) => {
          if (e.key === "Escape") onClose();
          if (e.key === "Tab") {
            const els = ref.current.querySelectorAll("button,input,select,a");
            const first = els[0],
              last = els[els.length - 1];
            if (e.shiftKey && document.activeElement === first) {
              e.preventDefault();
              last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
              e.preventDefault();
              first.focus();
            }
          }
        }}
      >
        <header>
          <h2 id={titleId}>{title}</h2>
          <button className="icon" aria-label="닫기" onClick={onClose}>
            <X />
          </button>
        </header>
        {children}
      </section>
    </div>
  );
}
const hookRows = [
  ["useState", "검색어, 필터, 모달 등 화면 상태"],
  ["useEffect", "API 호출·요청 취소, 저장소 동기화"],
  ["useReducer", "장바구니 추가·수량 변경·비우기"],
  ["useContext", "장바구니·찜·테마 공유"],
  ["useMemo", "필터링·정렬과 주문 합계 계산"],
  ["useCallback", "상품 추가·찜 함수 참조 유지"],
  ["useRef", "검색창과 모달 DOM 참조"],
  ["useId", "접근성 label·dialog ID 생성"],
  ["useDeferredValue", "검색어보다 결과 렌더링 우선순위 낮추기"],
  ["useTransition", "카테고리·정렬 전환"],
  ["useLayoutEffect", "모달 표시 직후 포커스·스크롤 잠금"],
  ["useImperativeHandle", "검색창의 focus()만 외부에 공개"],
  ["useDebugValue", "커스텀 훅 DevTools 표시"],
];
// useDeferredValue는 검색 결과 렌더링의 우선순위를 낮춥니다.
// useTransition은 카테고리와 정렬 전환을 긴급하지 않은 업데이트로 표시합니다.
function App() {
  const { cart, dispatch, add, favorites, like, dark, setDark } =
    useContext(ShopContext);
  const { data, loading, error, reload } = useProducts();
  const [q, setQ] = useState(""),
    [category, setCategory] = useState("전체"),
    [sort, setSort] = useState("추천순"),
    [onlyLikes, setOnlyLikes] = useState(false),
    [modal, setModal] = useState(null),
    [toast, setToast] = useState(""),
    [ordering, setOrdering] = useState(false),
    [orderError, setOrderError] = useState("");
  const [isPending, startTransition] = useTransition();
  const deferred = useDeferredValue(q),
    search = useRef(null),
    timer = useRef(null);
  useEffect(() => {
    const fn = (e) => {
      if (
        e.key === "/" &&
        !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)
      ) {
        e.preventDefault();
        search.current.focus();
      }
    };
    window.addEventListener("keydown", fn);
    return () => {
      window.removeEventListener("keydown", fn);
      clearTimeout(timer.current);
    };
  }, []);
  const notify = useCallback((t) => {
    setToast(t);
    clearTimeout(timer.current);
    timer.current = setTimeout(() => setToast(""), 2500);
  }, []);
  const products = useMemo(() => {
    let r = data.filter(
      (p) =>
        (category === "전체" || p.category === category) &&
        (!onlyLikes || favorites.includes(p.id)) &&
        `${p.name} ${p.title}`.toLowerCase().includes(deferred.toLowerCase()),
    );
    if (sort === "낮은 가격순") r.sort((a, b) => a.price - b.price);
    if (sort === "높은 가격순") r.sort((a, b) => b.price - a.price);
    return r;
  }, [data, category, onlyLikes, favorites, deferred, sort]);
  const total = useMemo(
    () => cart.reduce((s, p) => s + p.price * p.qty, 0),
    [cart],
  );
  const count = cart.reduce((s, p) => s + p.qty, 0),
    shipping = total === 0 || total >= 50000 ? 0 : 3000;
  const addItem = (p) => {
    add(p);
    notify("장바구니에 담았습니다");
  };
  async function order() {
    setOrdering(true);
    setOrderError("");
    try {
      const r = await fetch("https://jsonplaceholder.typicode.com/posts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: "모먼트 마켓 데모 주문",
          body: JSON.stringify(cart),
          userId: 1,
        }),
      });
      if (!r.ok) throw Error();
      const result = await r.json();
      dispatch({ type: "clear" });
      setModal({ type: "success", id: result.id });
    } catch {
      setOrderError("주문 요청에 실패했습니다. 다시 시도해 주세요.");
    } finally {
      setOrdering(false);
    }
  }
  return (
    <div className={dark ? "app dark" : "app"}>
      <div className="announcement">
        작은 취향이 만드는 좋은 일상{" "}
        <span>
          50,000원 이상 무료배송 <ArrowRight size={12} />
        </span>
      </div>
      <nav>
        <a className="brand" href="#">
          moment<span>market</span>
          <i>✳</i>
        </a>
        <div className="navlinks">
          <a className="active" href="#catalog">
            쇼핑하기
          </a>
          <button onClick={() => setModal({ type: "about" })}>
            브랜드 이야기
          </button>
        </div>
        <div className="navtools">
          <button
            className="icon"
            aria-label="테마 전환"
            onClick={() => setDark((v) => !v)}
          >
            {dark ? <Sun size={20} /> : <Moon size={20} />}
          </button>
          <button
            className={"icon " + (onlyLikes ? "selected" : "")}
            aria-label="찜한 상품 보기"
            onClick={() => {
              setOnlyLikes((v) => !v);
              document.getElementById("catalog").scrollIntoView();
            }}
          >
            <Heart size={21} />
          </button>
          <button className="bag" onClick={() => setModal({ type: "cart" })}>
            <ShoppingBag size={20} />
            <span>장바구니</span>
            <b>{count}</b>
          </button>
        </div>
      </nav>
      <main>
        <section className="hero">
          <div className="hero-copy">
            <div className="eyebrow">THOUGHTFULLY CHOSEN, EVERYDAY.</div>
            <h1>
              당신의 일상에,
              <br />
              좋은 순간 하나.
            </h1>
            <p>
              오래 곁에 두고 싶은 것들.
              <br />
              나만의 취향으로 채우는 작은 라이프스타일 숍.
            </p>
            <a className="primary" href="#catalog">
              취향 발견하기 <ArrowUpRight size={19} />
            </a>
            <div className="hero-bottom">
              <span className="little-line" /> SELECTED FOR YOUR EVERYDAY
            </div>
          </div>
          <div
            className="hero-photo"
            style={{
              backgroundImage: `url(${image("photo-1490312278390-ab64016e0aa9", 1400)})`,
            }}
          >
            <div className="photo-label">
              <span>THE SLOW LIVING COLLECTION</span>
              <strong>조금 더 여유로운 하루</strong>
              <ArrowUpRight />
            </div>
            <span className="issue">01 / EVERYDAY ESSENTIALS</span>
          </div>
        </section>
        <section className="perks">
          <span>
            <Truck size={17} /> 5만원 이상 무료배송
          </span>
          <span>
            <Package size={17} /> 일상을 위한 세심한 선택
          </span>
          <span>
            <RefreshCw size={17} /> 수령 후 7일 이내 교환·반품{" "}
            <small>(데모 안내)</small>
          </span>
        </section>
        <section id="catalog">
          <div className="section-title">
            <div className="eyebrow">OUR CURATED SELECTION</div>
            <h2>
              지금, 눈여겨볼 것들<span>Everyday favorites</span>
            </h2>
          </div>
          <div className="toolbar">
            <div className="categories">
              {["전체", "리빙", "키친", "패션", "디지털", "문구"].map((c) => (
                <button
                  className={category === c ? "chosen" : ""}
                  key={c}
                  onClick={() => startTransition(() => setCategory(c))}
                >
                  {c}
                </button>
              ))}
            </div>
            <SearchBox ref={search} value={q} onChange={setQ} />
          </div>
          <div className="resultbar">
            <span>
              {onlyLikes ? "찜한 상품" : "전체 상품"} <b>{products.length}</b>
              {onlyLikes && (
                <button onClick={() => setOnlyLikes(false)}>필터 해제 ×</button>
              )}
            </span>
            <label>
              <SlidersHorizontal size={14} />
              <select
                aria-label="상품 정렬"
                value={sort}
                onChange={(e) => startTransition(() => setSort(e.target.value))}
              >
                {["추천순", "낮은 가격순", "높은 가격순"].map((s) => (
                  <option key={s}>{s}</option>
                ))}
              </select>
            </label>
          </div>
          {error ? (
            <div className="empty">
              <p>{error}</p>
              <button className="primary" onClick={reload}>
                다시 불러오기
              </button>
            </div>
          ) : loading ? (
            <div className="grid">
              {Array.from({ length: 8 }, (_, i) => (
                <div key={i} className="skeleton" />
              ))}
            </div>
          ) : (
            <div
              className="grid"
              style={{ opacity: isPending || q !== deferred ? 0.7 : 1 }}
            >
              {products.map((p, i) => (
                <article className="product" key={p.id}>
                  <div className="product-image">
                    <button
                      className="image-button"
                      onClick={() => setModal({ type: "product", product: p })}
                      aria-label={p.name + " 상세 보기"}
                    >
                      <img src={image(p.image)} alt={p.name} loading="lazy" />
                    </button>
                    {i < 2 && category === "전체" && (
                      <span className="badge">{i === 0 ? "BEST" : "NEW"}</span>
                    )}
                    <button
                      className={
                        "favorite " + (favorites.includes(p.id) ? "liked" : "")
                      }
                      onClick={() => like(p.id)}
                      aria-label={
                        p.name +
                        " 찜 " +
                        (favorites.includes(p.id) ? "해제" : "추가")
                      }
                    >
                      <Heart
                        size={18}
                        fill={
                          favorites.includes(p.id) ? "currentColor" : "none"
                        }
                      />
                    </button>
                    <button className="quick-add" onClick={() => addItem(p)}>
                      <Plus size={16} /> 장바구니 담기
                    </button>
                  </div>
                  <div className="product-meta">
                    <span>{p.category}</span>
                    <span>
                      ★ {(4.6 + (p.id % 4) / 10).toFixed(1)}{" "}
                      <small>· 샘플</small>
                    </span>
                  </div>
                  <button
                    className="product-name"
                    onClick={() => setModal({ type: "product", product: p })}
                  >
                    {p.name}
                  </button>
                  <div className="price">
                    {money(p.price)}
                    <small>
                      무료배송 {p.price >= 50000 ? "가능" : "5만원부터"}
                    </small>
                  </div>
                </article>
              ))}
            </div>
          )}
          {!loading && !error && products.length === 0 && (
            <div className="empty">
              조건에 맞는 상품이 없습니다.
              <button
                onClick={() => {
                  setQ("");
                  setCategory("전체");
                  setOnlyLikes(false);
                }}
              >
                전체 상품 보기
              </button>
            </div>
          )}
        </section>
        <section className="editorial">
          <div>
            <div className="eyebrow">LESS, BUT BETTER.</div>
            <h2>
              많은 것보다,
              <br />
              마음에 드는 것.
            </h2>
          </div>
          <p>
            매일 사용하는 물건 하나에도 취향이 담기니까.
            <br />
            모먼트 마켓은 일상의 작은 변화를 제안합니다.
          </p>
          <ArrowUpRight size={44} />
        </section>
      </main>
      <footer>
        <a className="brand" href="#">
          moment<span>market</span>
          <i>✳</i>
        </a>
        <p>일상의 좋은 순간을 모으는 곳.</p>
        <button
          className="dev-button"
          onClick={() => setModal({ type: "hooks" })}
        >
          <Code2 size={16} /> React Hooks 살펴보기 <ArrowUpRight size={15} />
        </button>
        <div className="footer-bottom">
          <span>© 2026 MOMENT MARKET</span>
          <span>
            React 학습용 쇼핑몰 · 실제 결제 없음 · JSONPlaceholder API
          </span>
        </div>
      </footer>
      {toast && (
        <div className="toast" role="status">
          <Check size={18} />
          {toast}
        </div>
      )}
      {modal && (
        <Modal
          title={
            modal.type === "cart"
              ? "장바구니"
              : modal.type === "hooks"
                ? "이 쇼핑몰에 사용한 React Hooks"
                : modal.type === "product"
                  ? modal.product.name
                  : modal.type === "success"
                    ? "데모 주문 완료"
                    : "모먼트 마켓 이야기"
          }
          onClose={() => setModal(null)}
        >
          {modal.type === "cart" ? (
            <>
              {cart.length ? (
                cart.map((p) => (
                  <div className="cart-row" key={p.id}>
                    <img src={image(p.image, 150)} alt={p.name} />
                    <div>
                      <b>{p.name}</b>
                      <p>{money(p.price)}</p>
                      <div className="quantity">
                        <button
                          aria-label={p.name + " 수량 줄이기"}
                          onClick={() =>
                            dispatch({ type: "qty", id: p.id, delta: -1 })
                          }
                        >
                          <Minus size={14} />
                        </button>
                        {p.qty}
                        <button
                          aria-label={p.name + " 수량 늘리기"}
                          onClick={() =>
                            dispatch({ type: "qty", id: p.id, delta: 1 })
                          }
                        >
                          <Plus size={14} />
                        </button>
                      </div>
                    </div>
                    <strong>{money(p.price * p.qty)}</strong>
                  </div>
                ))
              ) : (
                <div className="empty">장바구니가 비어 있습니다.</div>
              )}
              {cart.length > 0 && (
                <>
                  <div className="totals">
                    <p>
                      상품 금액 <b>{money(total)}</b>
                    </p>
                    <p>
                      배송비 <b>{money(shipping)}</b>
                    </p>
                    <p>
                      합계 <b>{money(total + shipping)}</b>
                    </p>
                  </div>
                  <p className="notice">
                    학습용 모의 주문입니다. 실제 결제·배송은 없으며 서버에 영구
                    저장되지 않습니다.
                  </p>
                  {orderError && <p role="alert">{orderError}</p>}
                  <button
                    className="primary full"
                    disabled={ordering}
                    onClick={order}
                  >
                    {ordering ? "주문 요청 중…" : "데모 주문하기"}
                    <ArrowRight size={18} />
                  </button>
                </>
              )}
            </>
          ) : modal.type === "product" ? (
            <>
              <img
                className="detail-image"
                src={image(modal.product.image)}
                alt={modal.product.name}
              />
              <div className="detail-info">
                <span>{modal.product.category}</span>
                <h3>{money(modal.product.price)}</h3>
                <p>
                  일상을 위한 큐레이션 상품입니다. 상품명·가격·카테고리·이미지는
                  학습을 위해 별도로 구성했습니다.
                </p>
                <details>
                  <summary>
                    JSONPlaceholder 원본 데이터 #{modal.product.id}
                  </summary>
                  <h4>{modal.product.title}</h4>
                  <p>{modal.product.body}</p>
                </details>
                <button
                  className="primary full"
                  onClick={() => addItem(modal.product)}
                >
                  장바구니 담기 <Plus size={18} />
                </button>
              </div>
            </>
          ) : modal.type === "hooks" ? (
            <>
              <p className="notice">
                13가지 기본 훅과 useProducts, useLocalStorage 커스텀 훅을 실제
                기능에 연결했습니다. 소스의 각 함수에서 확인할 수 있습니다.
              </p>
              <div className="hook-list">
                {hookRows.map(([n, d]) => (
                  <div key={n}>
                    <code>{n}</code>
                    <span>{d}</span>
                  </div>
                ))}
              </div>
            </>
          ) : modal.type === "success" ? (
            <div className="empty">
              <Check size={40} />
              <h3>모의 주문 요청이 완료되었습니다.</h3>
              <p>API 응답 ID: {modal.id}</p>
              <p>
                JSONPlaceholder는 요청을 모의 처리하며 실제 주문을 저장하지
                않습니다.
              </p>
              <button className="primary" onClick={() => setModal(null)}>
                계속 쇼핑하기
              </button>
            </div>
          ) : (
            <div className="detail-info">
              <h3>일상을 더 좋아하게 만드는 작은 선택.</h3>
              <p>
                모먼트 마켓은 React 훅과 API 연동을 익히기 위한 라이프스타일
                쇼핑몰 예제입니다.
              </p>
              <p>
                JSONPlaceholder /posts의 ID·제목·본문을 불러와 상품의 원본
                데이터로 사용합니다. 실제 상품 API가 아니므로 상품명, 이미지,
                가격과 카테고리는 예시 데이터로 결합했습니다.
              </p>
            </div>
          )}
        </Modal>
      )}
    </div>
  );
}
createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider>
      <App />
    </Provider>
  </React.StrictMode>,
);
