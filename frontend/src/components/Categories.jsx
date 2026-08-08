import {
    Laptop,
    Shirt,
    ShoppingBag,
    House,
    Trophy
} from "lucide-react";

const categories = [
    {
        name: "Electronics",
        icon: Laptop
    },
    {
        name: "Fashion",
        icon: Shirt
    },
    {
        name: "Groceries",
        icon: ShoppingBag
    },
    {
        name: "Home",
        icon: House
    },
    {
        name: "Sports",
        icon: Trophy
    }
];

function Categories() {
    return (
        <section className="categories-section" id="categories">

            <div className="section-container">

                <h2>Popular Categories</h2>

                <div className="category-grid">

                    {categories.map((category) => {

                        const Icon = category.icon;

                        return (
                            <div className="category-card" key={category.name}>

                                <div className="category-icon">
                                    <Icon size={25} />
                                </div>

                                <span>{category.name}</span>

                            </div>
                        );
                    })}

                </div>

            </div>

        </section>
    );
}

export default Categories;