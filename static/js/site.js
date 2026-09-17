document.addEventListener("DOMContentLoaded", function () {

    // Scroll animations
    if (window.AOS) {
        AOS.init({ duration: 700, once: true, offset: 60 });
    }

    // Navbar shrink/shadow on scroll
    const navbar = document.getElementById("siteNavbar");
    if (navbar) {
        window.addEventListener("scroll", function () {
            navbar.classList.toggle("scrolled", window.scrollY > 40);
        });
    }

    // Animated counters (About section)
    const counters = document.querySelectorAll(".counter");
    if (counters.length) {
        const animateCounter = (el) => {
            const target = parseInt(el.dataset.target, 10) || 0;
            const duration = 1200;
            const start = performance.now();

            const step = (now) => {
                const progress = Math.min((now - start) / duration, 1);
                el.textContent = Math.floor(progress * target).toLocaleString();
                if (progress < 1) requestAnimationFrame(step);
                else el.textContent = target.toLocaleString();
            };
            requestAnimationFrame(step);
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach((el) => observer.observe(el));
    }

    // Reviews carousel
    if (window.Swiper && document.querySelector(".reviewsSwiper")) {
        new Swiper(".reviewsSwiper", {
            slidesPerView: 1,
            spaceBetween: 24,
            loop: true,
            autoplay: { delay: 5000, disableOnInteraction: false },
            pagination: { el: ".swiper-pagination", clickable: true },
        });
    }

});
