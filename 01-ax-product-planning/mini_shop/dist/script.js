// 장바구니는 브라우저의 localStorage에 저장합니다.
// 서버 없이도 페이지를 이동한 뒤 상품 정보가 유지되는 간단한 학습 예제입니다.
const CART_KEY = "sodam-cart";

function getCart() {
  return JSON.parse(localStorage.getItem(CART_KEY) || "[]");
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  updateCartCount();
}

function updateCartCount() {
  const count = getCart().reduce((sum, item) => sum + item.quantity, 0);
  document.querySelectorAll(".cart-count").forEach(element => element.textContent = count);
}

function formatPrice(number) {
  return number.toLocaleString("ko-KR") + "원";
}

// 목록에서 누른 상품 번호에 맞춰 상세 페이지 내용을 바꿉니다.
const PRODUCTS = {
  "1": { name: "구름 머그컵", category: "리빙", label: "SODAM LIVING", price: 12000, badge: "BEST", image: "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=1000&q=90", cartImage: "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=300&q=80", alt: "테이블 위의 흰색 머그컵", description: "포근한 구름을 닮은 부드러운 곡선의 머그컵입니다. 매일 마시는 차와 커피 시간을 조금 더 다정하게 만들어 드려요." },
  "2": { name: "데일리 캔버스백", category: "패션", label: "SODAM FASHION", price: 29000, badge: "DAILY", image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1000&q=90", cartImage: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=300&q=80", alt: "밝은색 데일리 가방", description: "가볍고 넉넉해서 매일 들기 좋은 캔버스백입니다. 어떤 옷차림에도 자연스럽게 어울리는 담백한 디자인입니다." },
  "3": { name: "숲 향초", category: "리빙", label: "SODAM LIVING", price: 18500, badge: "NEW", image: "https://images.unsplash.com/photo-1616172890963-a45e7da8de31?auto=format&fit=crop&w=1000&q=90", cartImage: "https://images.unsplash.com/photo-1616172890963-a45e7da8de31?auto=format&fit=crop&w=300&q=80", alt: "투명한 유리 용기에 담긴 흰색 향초", description: "고요한 숲을 떠올리게 하는 편안한 향초입니다. 차분한 향과 은은한 불빛으로 나만의 휴식 시간을 만들어 보세요." },
  "4": { name: "수제 딸기잼", category: "푸드", label: "SODAM FOOD", price: 9800, badge: "HANDMADE", image: "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?auto=format&fit=crop&w=1000&q=90", cartImage: "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?auto=format&fit=crop&w=300&q=80", alt: "병에 담긴 수제 잼", description: "잘 익은 딸기의 맛과 향을 천천히 담은 수제 잼입니다. 빵과 요거트에 곁들이면 산뜻한 아침이 완성됩니다." },
  "5": { name: "린넨 테이블 매트", category: "리빙", label: "SODAM LIVING", price: 15000, badge: "NATURAL", image: "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1000&q=90", cartImage: "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=300&q=80", alt: "린넨 소재의 테이블 소품", description: "자연스러운 질감이 매력적인 린넨 테이블 매트입니다. 평범한 식탁에 따뜻하고 편안한 분위기를 더해 줍니다." },
  "6": { name: "드립백 커피 세트", category: "푸드", label: "SODAM FOOD", price: 16000, badge: "BEST", image: "https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=1000&q=90", cartImage: "https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&w=300&q=80", alt: "원두와 커피 도구", description: "언제 어디서나 간편하게 즐기는 향긋한 드립백 커피 세트입니다. 서로 다른 풍미의 원두를 골고루 담았습니다." }
};

function renderProductDetail() {
  const image = document.querySelector("#detail-image");
  if (!image) return;
  const id = new URLSearchParams(location.search).get("id") || "1";
  const product = PRODUCTS[id] || PRODUCTS["1"];
  image.src = product.image;
  image.alt = product.alt;
  document.querySelector("#detail-category").textContent = product.category;
  document.querySelector("#breadcrumb-name").textContent = product.name;
  document.querySelector("#detail-label").textContent = product.label;
  document.querySelector("#detail-name").textContent = product.name;
  document.querySelector("#detail-price").textContent = formatPrice(product.price);
  document.querySelector("#detail-description").textContent = product.description;
  document.querySelector("#detail-badge").textContent = product.badge;
  document.title = `${product.name} | 소담상점`;
  const cartButton = document.querySelector("#detail-cart-button");
  cartButton.dataset.id = id;
  cartButton.dataset.name = product.name;
  cartButton.dataset.price = product.price;
  cartButton.dataset.image = product.cartImage;
}

renderProductDetail();

// 상품 카드와 상세 화면의 '담기' 버튼
document.querySelectorAll(".add-cart").forEach(button => {
  button.addEventListener("click", () => {
    const cart = getCart();
    const oldItem = cart.find(item => item.id === button.dataset.id);
    const quantityInput = document.querySelector("#detail-quantity");
    const quantity = quantityInput ? Number(quantityInput.value) : 1;

    if (oldItem) oldItem.quantity += quantity;
    else cart.push({
      id: button.dataset.id,
      name: button.dataset.name,
      price: Number(button.dataset.price),
      image: button.dataset.image,
      quantity
    });

    saveCart(cart);
    const toast = document.querySelector("#toast");
    if (toast) {
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 1800);
    }
  });
});

// 상품 검색과 카테고리 필터
const searchInput = document.querySelector("#product-search");
const filterButtons = document.querySelectorAll(".filter-button");
let selectedCategory = "all";

function filterProducts() {
  const keyword = (searchInput?.value || "").trim().toLowerCase();
  let visibleCount = 0;
  document.querySelectorAll(".product-card").forEach(card => {
    const keywordMatch = card.dataset.name.toLowerCase().includes(keyword);
    const categoryMatch = selectedCategory === "all" || card.dataset.category === selectedCategory;
    card.hidden = !(keywordMatch && categoryMatch);
    if (!card.hidden) visibleCount++;
  });
  const noResults = document.querySelector("#no-results");
  if (noResults) noResults.hidden = visibleCount > 0;
}

searchInput?.addEventListener("input", filterProducts);
filterButtons.forEach(button => button.addEventListener("click", () => {
  selectedCategory = button.dataset.category;
  filterButtons.forEach(item => item.classList.remove("active"));
  button.classList.add("active");
  filterProducts();
}));

// 장바구니 페이지 만들기
function renderCart() {
  const container = document.querySelector("#cart-items");
  if (!container) return;
  const cart = getCart();

  if (cart.length === 0) {
    container.innerHTML = '<div class="empty-cart"><h2>장바구니가 비어 있어요.</h2><p>마음에 드는 상품을 담아보세요.</p><a class="button dark" href="index.html">상품 보러가기</a></div>';
  } else {
    container.innerHTML = cart.map(item => `
      <article class="cart-item">
        <img src="${item.image}" alt="${item.name}">
        <div><h3>${item.name}</h3><p>${formatPrice(item.price)}</p><div class="quantity"><button data-action="minus" data-id="${item.id}" aria-label="수량 줄이기">−</button><span>${item.quantity}</span><button data-action="plus" data-id="${item.id}" aria-label="수량 늘리기">+</button></div></div>
        <div class="item-price"><b>${formatPrice(item.price * item.quantity)}</b><br><button class="remove-item" data-action="remove" data-id="${item.id}">삭제</button></div>
      </article>`).join("");
  }

  container.querySelectorAll("button[data-action]").forEach(button => button.addEventListener("click", () => {
    const nextCart = getCart();
    const item = nextCart.find(product => product.id === button.dataset.id);
    if (button.dataset.action === "plus") item.quantity++;
    if (button.dataset.action === "minus") item.quantity = Math.max(1, item.quantity - 1);
    if (button.dataset.action === "remove") nextCart.splice(nextCart.indexOf(item), 1);
    saveCart(nextCart);
    renderCart();
  }));

  updateSummary(cart, "subtotal", "shipping", "cart-total");
  const checkoutLink = document.querySelector("#checkout-link");
  if (checkoutLink) checkoutLink.style.pointerEvents = cart.length ? "auto" : "none";
}

function updateSummary(cart, subtotalId, shippingId, totalId) {
  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const shipping = subtotal === 0 || subtotal >= 30000 ? 0 : 3000;
  document.querySelector(`#${subtotalId}`)?.replaceChildren(formatPrice(subtotal));
  document.querySelector(`#${shippingId}`)?.replaceChildren(formatPrice(shipping));
  document.querySelector(`#${totalId}`)?.replaceChildren(formatPrice(subtotal + shipping));
}

renderCart();
updateSummary(getCart(), "checkout-subtotal", "checkout-shipping", "checkout-total");
updateCartCount();

// 예제용 로그인 및 결제 폼 처리
document.querySelector("#login-form")?.addEventListener("submit", event => {
  event.preventDefault();
  alert("로그인되었습니다. (학습용 예제)");
  location.href = "index.html";
});

document.querySelector("#checkout-form")?.addEventListener("submit", event => {
  event.preventDefault();
  localStorage.removeItem(CART_KEY);
  location.href = "complete.html";
});

// WebMCP를 지원하는 브라우저에서는 AI 도우미도 상품을 장바구니에 담을 수 있습니다.
// 일반 브라우저에서는 아래 코드가 실행되지 않으므로 기존 기능에 영향을 주지 않습니다.
if (document.modelContext?.registerTool) {
  document.modelContext.registerTool({
    name: "add_product_to_cart",
    title: "상품 장바구니 담기",
    description: "상품 번호, 이름, 가격을 받아 소담상점 장바구니에 상품을 추가합니다.",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string" },
        name: { type: "string" },
        price: { type: "number", minimum: 1 },
        quantity: { type: "integer", minimum: 1, maximum: 10 }
      },
      required: ["id", "name", "price"],
      additionalProperties: false
    },
    annotations: { readOnlyHint: false, untrustedContentHint: false },
    execute(input) {
      if (!input || typeof input.id !== "string" || typeof input.name !== "string" ||
          !Number.isFinite(input.price) || input.price < 1) {
        throw new Error("올바른 상품 정보를 입력해 주세요.");
      }
      const quantity = input.quantity ?? 1;
      if (!Number.isInteger(quantity) || quantity < 1 || quantity > 10) {
        throw new Error("수량은 1개부터 10개까지 입력할 수 있습니다.");
      }
      const cart = getCart();
      const oldItem = cart.find(item => item.id === input.id);
      if (oldItem) oldItem.quantity += quantity;
      else cart.push({ id: input.id, name: input.name, price: input.price, image: "", quantity });
      saveCart(cart);
      renderCart();
      return { added: true, productId: input.id, quantity, cartCount: getCart().reduce((sum, item) => sum + item.quantity, 0) };
    }
  });
}
