// frontend/PaymentForm.jsx
import { useState } from "react";

export default function PaymentForm() {
  const [cardNumber, setCardNumber] = useState("");
  const [cvv, setCvv] = useState("");
  const [expiry, setExpiry] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/api/payment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cardNumber, cvv, expiry }),
    });

    const data = await res.json();
    alert(data.status);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Card Number"
        value={cardNumber}
        onChange={(e) => setCardNumber(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="CVV"
        value={cvv}
        onChange={(e) => setCvv(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="MM/YY"
        value={expiry}
        onChange={(e) => setExpiry(e.target.value)}
        required
      />
      <button type="submit">Pay Securely</button>
    </form>
  );
}
