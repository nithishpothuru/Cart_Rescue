function Newsletter() {
    return (
        <section className="newsletter">

            <div className="newsletter-content">

                <h2>Stay Ahead of the Curve</h2>

                <p>
                    Subscribe to our weekly curated newsletters for exclusive
                    tech drops, early offers, and AI shopping insight hacks.
                </p>

                <div className="newsletter-form">

                    <input
                        type="email"
                        placeholder="Enter your email address"
                    />

                    <button>
                        Subscribe
                    </button>

                </div>

            </div>

        </section>
    );
}

export default Newsletter;
