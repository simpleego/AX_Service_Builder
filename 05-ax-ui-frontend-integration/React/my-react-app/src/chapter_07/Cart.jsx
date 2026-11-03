import { useState, useMemo } from 'react';

function Cart() {
    console.log('Cart 컴포넌트 호출됨...');
    
    const [items, setItems] = useState([
        { id: 1, name: '키보드', price: 50000, qty: 1 },
        { id: 2, name: '마우스', price: 25000, qty: 2 },
    ]);
    const [coupon, setCoupon] = useState('');

    const summary = useMemo(() => {
        console.log('호출됨...')
        const totalQty = items.reduce((sum, item) => sum + item.qty, 0);
        const totalPrice = items.reduce((sum, item) => sum + item.price * item.qty, 0);
        const shipping = totalPrice >= 50000 ? 0 : 3000;
        return { totalQty, totalPrice, shipping, payment: totalPrice + shipping };
    }, [items]); // 쿠폰을 입력할 때는 다시 계산하지 않습니다

    const increase = (id) =>
        setItems(prev => prev.map(item => (item.id === id ? { ...item, qty: item.qty + 1 } : item)));

    return (
        <div>
            {items.map(item => (
                <p key={item.id}>
                    {item.name} x {item.qty} <button onClick={() => increase(item.id)}>+</button>
                </p>
            ))}
            <input value={coupon} onChange={e => setCoupon(e.target.value)} placeholder="쿠폰 코드" />
            <p>총 {summary.totalQty}개 / 상품 금액 {summary.totalPrice.toLocaleString()}원</p>
            <p>배송비 {summary.shipping.toLocaleString()}원</p>
            <h3>결제 금액 {summary.payment.toLocaleString()}원</h3>
        </div>
    );
}

export default Cart;
