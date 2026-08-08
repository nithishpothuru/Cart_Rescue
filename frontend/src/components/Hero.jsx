import React from "react";

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

                        <button className="primary-btn">
                            Start Shopping →
                        </button>

                        <button className="secondary-btn">
                            Explore Categories
                        </button>

                    </div>

                </div>

                <div className="hero-image">
                    <img
                        src="/hero-ai.jpg"
                        alt="AI powered shopping experience"
                    />
                </div>

            </div>
        </section>
    );
}

export default Hero;