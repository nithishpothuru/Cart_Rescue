import { useState } from "react";
import { Minus, Plus, ShoppingCart } from "lucide-react";
import { useSession } from "../context/SessionContext";

function AddToCartButton({ product }) {
  const { addToCart } = useSession();
  const [showQty, setShowQty] = useState(false);
  const [qty, setQty] = useState(1);

  const handleAdd = () => {
    addToCart(product, qty);
    setShowQty(false);
    setQty(1);
  };

  if (!showQty) {
    return (
      <button className="add-btn" onClick={() => setShowQty(true)}>
        <ShoppingCart size={14} /> Add
      </button>
    );
  }

  return (
    <div className="qty-selector">
      <button onClick={() => setQty((q) => Math.max(1, q - 1))}>
        <Minus size={14} />
      </button>
      <span>{qty}</span>
      <button onClick={() => setQty((q) => q + 1)}>
        <Plus size={14} />
      </button>
      <button className="confirm-add" onClick={handleAdd}>
        Add
      </button>
    </div>
  );
}

export default AddToCartButton;
