import React from "react";

import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Categories from "../components/Categories";
import FeaturedProducts from "../components/FeaturedProducts";
import Testimonials from "../components/Testimonials";
import Newsletter from "../components/Newsletter";
import Footer from "../components/Footer";

function Home() {
    return (
        <>
            <Navbar />

            <main>
                <Hero />
                <Categories />
                <FeaturedProducts />
                <Testimonials />
                <Newsletter />
            </main>

            <Footer />
        </>
    );
}

export default Home;