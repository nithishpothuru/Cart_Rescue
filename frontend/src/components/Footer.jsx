import React from "react";
import {
    CreditCard,
    ShieldCheck,
    Headphones,
    WalletCards,
} from "lucide-react";

function Footer() {
    return (
        <footer className="footer">

            <div className="footer-container">

                {/* Brand */}
                <div className="footer-brand">
                    <h3>
                        ✨ CartRescue AI
                    </h3>

                    <p>
                        Experience lightning-fast checkouts and AI-driven
                        recommendations tailored exclusively for you.
                    </p>
                </div>

                {/* Company */}
                <div className="footer-column">
                    <h4>COMPANY</h4>

                    <a href="#">About Us</a>
                    <a href="#">Careers</a>
                    <a href="#">Press</a>
                    <a href="#">Blog</a>
                </div>

                {/* Shop */}
                <div className="footer-column">
                    <h4>SHOP</h4>

                    <a href="#">Categories</a>
                    <a href="#">Popular Offers</a>
                    <a href="#">AI Features</a>
                    <a href="#">New Drops</a>
                </div>

                {/* Support */}
                <div className="footer-column">
                    <h4>SUPPORT</h4>

                    <a href="#">Help Center</a>
                    <a href="#">Safe Checkout</a>
                    <a href="#">Track Order</a>
                    <a href="#">Refund Policy</a>
                </div>

                {/* Payment */}
                <div className="footer-column payment-column">
                    <h4>PAYMENT & TRUST</h4>

                    <div className="payment-icons">

                        <span>
                            <CreditCard size={18} />
                        </span>

                        <span>
                            <ShieldCheck size={18} />
                        </span>

                        <span>
                            <Headphones size={18} />
                        </span>

                        <span>
                            <WalletCards size={18} />
                        </span>

                    </div>
                </div>

            </div>

            {/* Bottom */}
            <div className="footer-bottom">

                <p>
                    © 2026 CartRescue AI Inc. All rights reserved.
                </p>

                <div className="footer-links">
                    <a href="#">Privacy Policy</a>
                    <a href="#">Terms of Service</a>
                    <a href="#">Cookies</a>
                </div>

            </div>

        </footer>
    );
}

export default Footer;