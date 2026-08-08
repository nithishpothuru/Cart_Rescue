const testimonials = [
    {
        name: "Sarah Jenkins",
        initials: "SJ",
        text:
            '"I saved almost 15 minutes at checkout! CartRescue predicted my shipping details instantly and applied a smart discount."'
    },
    {
        name: "David Miller",
        initials: "DM",
        text:
            '"The most premium, high-speed checkout flow I have ever experienced. Simply Apple-level sophistication."'
    },
    {
        name: "Jessica Alva",
        initials: "JA",
        text:
            '"Stunning AI recommendations. The products shown on my home screen feel exactly like things I wanted to buy anyway."'
    }
];

function Testimonials() {
    return (
        <section className="testimonials-section">

            <div className="section-container">

                <h2 className="testimonial-title">
                    What Our Shoppers Say
                </h2>

                <div className="testimonial-grid">

                    {testimonials.map((item) => (

                        <div className="testimonial-card" key={item.name}>

                            <div className="testimonial-user">

                                <div className="avatar">
                                    {item.initials}
                                </div>

                                <div>
                                    <h4>{item.name}</h4>

                                    <div className="testimonial-stars">
                                        ★★★★★
                                    </div>
                                </div>

                            </div>

                            <p>{item.text}</p>

                        </div>

                    ))}

                </div>

            </div>

        </section>
    );
}

export default Testimonials;