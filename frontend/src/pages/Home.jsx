import { useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Categories from "../components/Categories";
import FeaturedProducts from "../components/FeaturedProducts";
import Testimonials from "../components/Testimonials";
import Newsletter from "../components/Newsletter";
import Footer from "../components/Footer";
import { useSession } from "../context/SessionContext";

function Home() {
  const { trackEvent } = useSession();

  useEffect(() => {
    trackEvent({ event_type: "page_view", page: "home" });
  }, []);

  return (
    <div className="app">
      <Navbar />
      <main>
        <Hero />
        <Categories />
        <FeaturedProducts />
        <Testimonials />
        <Newsletter />
      </main>
      <Footer />
    </div>
  );
}

export default Home;
