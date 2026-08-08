import AddToCartButton from "../components/AddToCartButton";

const products = [
  {
    product_id: "P2001",
    name: "SonicBass Wireless Headset",
    category: "Electronics",
    price: 149.0,
    rating: 4.8,
    reviews: 48,
    image:
      "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
  },
  {
    product_id: "P2002",
    name: "Chronos Smartwatch Elite",
    category: "Electronics",
    price: 299.0,
    rating: 4.7,
    reviews: 48,
    image:
      "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
  },
  {
    product_id: "P2003",
    name: "AeroDry Sport Sneakers",
    category: "Sports",
    price: 120.0,
    rating: 4.9,
    reviews: 48,
    image:
      "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80",
  },
  {
    product_id: "P2004",
    name: "Nebula Smart Projector",
    category: "Electronics",
    price: 450.0,
    rating: 4.6,
    reviews: 48,
    image:
      "https://images.unsplash.com/photo-1601944179066-29786cb9d32a?auto=format&fit=crop&w=800&q=80",
  },
];

function FeaturedProducts() {
  return (
    <section className="featured-products">
      <div className="section-header">
        <h2>Featured Products</h2>
        <a href="/shop" className="view-all">
          View All Products <span>›</span>
        </a>
      </div>

      <div className="products-grid">
        {products.map((product) => (
          <div className="product-card" key={product.product_id}>
            <div className="product-image-container">
              <img
                src={product.image}
                alt={product.name}
                className="product-image"
              />
              <button className="wishlist-button">♡</button>
            </div>

            <div className="product-details">
              <p className="product-name">{product.name}</p>

              <div className="rating">
                <span className="stars">★★★★★</span>
                <span className="review-count">({product.reviews})</span>
              </div>

              <div className="product-bottom">
                <span className="product-price">
                  ${product.price.toFixed(2)}
                </span>

                {/* ✅ New quantity selector button */}
                <AddToCartButton product={product} />
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default FeaturedProducts;
