import { ShoppingCart } from "lucide-react";

function Navbar() {
    return (
        <header className="navbar">
            <div className="navbar-container">

                {/* Logo */}
                <div className="logo">
                    <ShoppingCart size={27} strokeWidth={2.2} />
                    <span>
                        CartRescue <strong>AI</strong>
                    </span>
                </div>

                {/* Navigation */}
                <nav className="nav-links">
                    <a className="active" href="#home">Home</a>
                    <a href="#products">Products</a>
                    <a href="#categories">Categories</a>
                    <a href="#offers">Offers</a>
                    <a href="#about">About</a>
                    <a href="#contact">Contact</a>
                </nav>

                {/* Auth */}
                <div className="nav-actions">
                    <button className="login-btn">Login</button>
                    <button className="register-btn">Register</button>
                </div>

            </div>
        </header>
    );
}

export default Navbar;