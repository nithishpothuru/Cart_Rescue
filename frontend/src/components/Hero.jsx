import { Link } from "react-router-dom";

function Hero() {
  return (
    <section className="hero">
      <div className="hero-content">
        <div className="hero-text">
          <span className="hero-badge">
            ✨ AI-OPTIMIZED CHECKOUT PLATFORM
          </span>

          <h1>
            Shop Smarter.
            <br />
            Experience Faster
            <br />
            Checkout.
          </h1>

          <p>
            Discover amazing products with a seamless shopping experience.
            Backed by state-of-the-art predictive cart analysis to rescue
            abandoned deals instantly.
          </p>

          <div className="hero-buttons">
            <Link to="/shop" className="primary-btn">
              Start Shopping →
            </Link>
            <Link to="/shop" className="secondary-btn">
              Explore Categories
            </Link>
          </div>
        </div>

        <div className="hero-image">
          <img
            src="https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=800&q=80"
            alt="AI powered shopping experience"
          />
        </div>
      </div>
    </section>
  );
}

export default Hero;
