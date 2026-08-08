import { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { useSession } from "../context/SessionContext";
import { Heart, ShoppingCart, ChevronLeft, ChevronRight } from "lucide-react";
import "./Shop.css";
import AddToCartButton from "../components/AddToCartButton";

const API = "http://127.0.0.1:5000";

function Shop() {
  const [products, setProducts] = useState([]);
  const { addToCart, trackEvent } = useSession();

  useEffect(() => {
    axios.get(`${API}/api/products`).then((res) => {
      if (res.data.success) setProducts(res.data.products);
    });
    trackEvent({ event_type: "page_view", page: "shop" });
  }, []);

  const flashProducts = products.filter((p) => p.badge);
  const recommended = products.filter((p) => !p.badge);

  return (
    <div className="shop-page">
      <Navbar />

      {/* Banner */}
      <div className="flash-banner">
        <div className="banner-content">
          <span className="member-badge">MEMBER ONLY ACCESS</span>
          <h1>
            Exclusive AI Flash Drop:
            <br />
            Save 20% on all Carbon Tech Gear
          </h1>
        </div>
      </div>

      <div className="container">
        {/* Flash Sale */}
        <section className="flash-sale">
          <div className="section-header">
            <div className="timer">
              <span>Flash Sale</span>
              <div className="countdown">
                <span>02</span>:<span>45</span>:<span>18</span>
              </div>
            </div>
            <div className="nav-arrows">
              <button><ChevronLeft size={18} /></button>
              <button><ChevronRight size={18} /></button>
            </div>
          </div>

          <div className="products-grid">
            {flashProducts.map((p) => (
              <ProductCard key={p.product_id} product={p} onAdd={addToCart} />
            ))}
          </div>
        </section>

        {/* Recommended */}
        <section className="recommended">
          <div className="section-header">
            <h2>
              Recommended For You{" "}
              <span className="ai-badge">AI PERSONALIZED</span>
            </h2>
          </div>

          <div className="products-grid">
            {recommended.map((p) => (
              <ProductCard key={p.product_id} product={p} onAdd={addToCart} />
            ))}
          </div>
        </section>
      </div>

      <Footer />
    </div>
  );
}

function ProductCard({ product, onAdd }) {
  return (
    <div className="product-card">
      <div className="product-image-wrap">
        {product.badge && <span className="discount-badge">{product.badge}</span>}
        <button className="wishlist"><Heart size={16} /></button>
        <img src={product.image} alt={product.name} />
      </div>
      <div className="product-info">
        <h3>{product.name}</h3>
        <div className="rating">
          ★★★★★ <span>({product.reviews})</span>
        </div>
        <div className="price-row">
          <span className="price">${product.price.toFixed(2)}</span>
          <AddToCartButton product={product} />
        </div>
      </div>
    </div>
  );
}

export default Shop;
