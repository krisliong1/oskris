---
name: frontend-builder
description: Professional frontend development implementation following design specifications. Use when building websites, implementing designs, converting mockups to code, creating responsive layouts, or developing interactive features. Prioritizes clean code, performance, and maintainability.
---

# Frontend Builder Skill

This skill guides the implementation of web designs into functional, production-ready code. It emphasizes best practices, performance, and code quality.

## When to Use This Skill

- Implementing approved designs
- Building website layouts from mockups
- Creating responsive components
- Developing interactive features
- Code review and optimization
- Technical implementation planning

## Input Requirements

Works best when you have:
- Design mockups or wireframes
- Design specifications (from design-consultant skill)
- Technical requirements (from requirements-analyst skill)
- Content and assets ready
- Hosting environment prepared

## Technology Stack Recommendations

### For Simple Websites (5-10 pages, informational)

**Recommended**: Static HTML + CSS + Vanilla JS
- Fast loading
- Easy to maintain
- Low hosting costs
- No database needed

```
Structure:
├── index.html
├── about.html
├── services.html
├── contact.html
├── css/
│   └── style.css
├── js/
│   └── script.js
└── images/
```

### For WordPress Sites (Most Malaysian SMEs)

**Recommended**: WordPress + Custom Theme / Child Theme
- Client-friendly CMS
- Easy content updates
- Plugin ecosystem
- Local hosting support

```
Theme Structure:
├── style.css
├── functions.php
├── index.php
├── header.php
├── footer.php
├── page.php
├── single.php
├── archive.php
├── template-parts/
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── inc/
    └── custom-functions.php
```

### For E-commerce (WooCommerce)

**Recommended**: WordPress + WooCommerce + Custom Theme
- Proven e-commerce platform
- Malaysian payment gateways support
- Inventory management
- Order tracking

**Essential Plugins**:
- WooCommerce
- Payment Gateway (FPX, Stripe)
- Shipping plugins (Ninja Van, J&T)
- SEO (Yoast/RankMath)
- Performance (WP Rocket, Imagify)

### For Custom Web Apps

**Recommended**: Next.js / React + Tailwind CSS
- Modern, fast
- SEO-friendly
- Scalable
- Component-based

```
Structure:
├── pages/
├── components/
├── public/
├── styles/
└── lib/
```

## Development Best Practices

### 1. Code Organization

**HTML Structure**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Page Title] | [Site Name]</title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="[Description]">
    <meta name="keywords" content="[Keywords]">
    
    <!-- Open Graph for Social Sharing -->
    <meta property="og:title" content="[Title]">
    <meta property="og:description" content="[Description]">
    <meta property="og:image" content="[Image URL]">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <!-- Header -->
    <header>
        <nav>
            <!-- Navigation -->
        </nav>
    </header>

    <!-- Main Content -->
    <main>
        <section>
            <!-- Content sections -->
        </section>
    </main>

    <!-- Footer -->
    <footer>
        <!-- Footer content -->
    </footer>

    <!-- Scripts -->
    <script src="js/script.js"></script>
</body>
</html>
```

**CSS Structure**:
```css
/* ==========================================================================
   Base Styles
   ========================================================================== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    /* Color Variables */
    --primary-color: #0A192F;
    --secondary-color: #00D1FF;
    --accent-color: #F97316;
    --text-dark: #111827;
    --text-light: #6B7280;
    --bg-light: #F9FAFB;
    
    /* Typography */
    --font-heading: 'Orbitron', sans-serif;
    --font-body: 'Inter', sans-serif;
    
    /* Spacing */
    --spacing-xs: 0.5rem;
    --spacing-sm: 1rem;
    --spacing-md: 2rem;
    --spacing-lg: 4rem;
    
    /* Breakpoints */
    --mobile: 768px;
    --tablet: 1024px;
    --desktop: 1280px;
}

/* ==========================================================================
   Typography
   ========================================================================== */
body {
    font-family: var(--font-body);
    font-size: 16px;
    line-height: 1.6;
    color: var(--text-dark);
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: var(--spacing-sm);
}

/* ==========================================================================
   Layout
   ========================================================================== */
.container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}

/* ==========================================================================
   Components
   ========================================================================== */
/* Navigation, Buttons, Cards, Forms, etc. */

/* ==========================================================================
   Responsive
   ========================================================================== */
@media (max-width: 768px) {
    /* Mobile styles */
}
```

### 2. Responsive Development

**Mobile-First Approach**:
```css
/* Base styles (mobile) */
.grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
    .grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
    }
}
```

**Testing Breakpoints**:
- Mobile: 375px (iPhone SE)
- Tablet: 768px (iPad)
- Desktop: 1280px (Laptop)
- Large: 1920px (Desktop monitor)

### 3. Performance Optimization

**Image Optimization**:
```html
<!-- Use WebP with fallback -->
<picture>
    <source srcset="image.webp" type="image/webp">
    <source srcset="image.jpg" type="image/jpeg">
    <img src="image.jpg" alt="Description" loading="lazy">
</picture>

<!-- Or modern img with srcset -->
<img 
    src="image-800.jpg"
    srcset="image-400.jpg 400w,
            image-800.jpg 800w,
            image-1200.jpg 1200w"
    sizes="(max-width: 600px) 400px,
           (max-width: 1000px) 800px,
           1200px"
    alt="Description"
    loading="lazy"
>
```

**CSS Optimization**:
- Minify CSS in production
- Remove unused CSS
- Use CSS Grid/Flexbox instead of floats
- Limit @import statements
- Inline critical CSS

**JavaScript Optimization**:
```html
<!-- Defer non-critical scripts -->
<script src="script.js" defer></script>

<!-- Async for independent scripts -->
<script src="analytics.js" async></script>

<!-- Module scripts -->
<script type="module" src="app.js"></script>
```

### 4. Accessibility (WCAG Standards)

**Semantic HTML**:
```html
<!-- Good -->
<header>
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
        </ul>
    </nav>
</header>

<main>
    <article>
        <h1>Article Title</h1>
        <p>Content...</p>
    </article>
</main>

<!-- Bad -->
<div class="header">
    <div class="nav">
        <div class="menu">
            <div class="item"><a href="/">Home</a></div>
        </div>
    </div>
</div>
```

**ARIA Labels**:
```html
<button aria-label="Close menu">×</button>
<nav aria-label="Main navigation">...</nav>
<input type="text" aria-label="Search" placeholder="Search...">
```

**Keyboard Navigation**:
```css
/* Visible focus states */
a:focus, button:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
}

/* Skip to content link */
.skip-to-content {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px;
    z-index: 100;
}

.skip-to-content:focus {
    top: 0;
}
```

### 5. Forms Best Practices

**Contact Form Example**:
```html
<form action="/submit" method="POST" id="contact-form">
    <div class="form-group">
        <label for="name">Name *</label>
        <input 
            type="text" 
            id="name" 
            name="name" 
            required
            aria-required="true"
        >
    </div>

    <div class="form-group">
        <label for="email">Email *</label>
        <input 
            type="email" 
            id="email" 
            name="email" 
            required
            aria-required="true"
        >
    </div>

    <div class="form-group">
        <label for="phone">Phone</label>
        <input 
            type="tel" 
            id="phone" 
            name="phone"
            pattern="[0-9]{10,11}"
        >
    </div>

    <div class="form-group">
        <label for="message">Message *</label>
        <textarea 
            id="message" 
            name="message" 
            rows="5"
            required
            aria-required="true"
        ></textarea>
    </div>

    <button type="submit" class="btn-primary">
        Send Message
    </button>
</form>

<script>
// Form validation
document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(this);
    
    // Basic validation
    if (!formData.get('name') || !formData.get('email')) {
        alert('Please fill in required fields');
        return;
    }
    
    // Submit via AJAX
    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Message sent successfully!');
            this.reset();
        }
    })
    .catch(error => {
        alert('Error sending message. Please try again.');
    });
});
</script>
```

### 6. SEO Implementation

**Meta Tags**:
```html
<!-- Title (50-60 characters) -->
<title>Hardware Store Kota Tinggi | Kong Kiong Hardware</title>

<!-- Description (150-160 characters) -->
<meta name="description" content="Kong Kiong Hardware - Your trusted hardware store in Kota Tinggi. Quality tools, building materials, and expert service since 1985.">

<!-- Keywords (less important now, but include) -->
<meta name="keywords" content="hardware store Kota Tinggi, building materials, tools Malaysia">

<!-- Open Graph -->
<meta property="og:title" content="Kong Kiong Hardware - Kota Tinggi">
<meta property="og:description" content="Quality hardware and building materials">
<meta property="og:image" content="https://kongkiong.com/og-image.jpg">
<meta property="og:url" content="https://kongkiong.com">
<meta property="og:type" content="website">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Kong Kiong Hardware">
<meta name="twitter:description" content="Quality hardware store in Kota Tinggi">
<meta name="twitter:image" content="https://kongkiong.com/twitter-image.jpg">

<!-- Canonical URL -->
<link rel="canonical" href="https://kongkiong.com">

<!-- Structured Data (JSON-LD) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HardwareStore",
  "name": "Kong Kiong Hardware",
  "image": "https://kongkiong.com/logo.png",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "Kota Tinggi",
    "addressRegion": "Johor",
    "postalCode": "81900",
    "addressCountry": "MY"
  },
  "telephone": "+60123456789",
  "openingHours": "Mo-Sa 08:00-18:00",
  "priceRange": "$$"
}
</script>
```

### 7. Malaysian-Specific Integrations

**WhatsApp Click-to-Chat**:
```html
<a href="https://wa.me/60123456789?text=Hi%20I%20want%20to%20inquire%20about" 
   class="whatsapp-btn"
   target="_blank">
    <img src="whatsapp-icon.svg" alt="WhatsApp">
    Chat on WhatsApp
</a>

<style>
.whatsapp-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #25D366;
    color: white;
    padding: 12px 20px;
    border-radius: 50px;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    text-decoration: none;
    z-index: 1000;
}
</style>
```

**Malaysian Payment Gateway Integration**:
```php
// FPX Payment (example with Billplz API)
<?php
$api_key = 'your_billplz_api_key';
$collection_id = 'your_collection_id';

$data = [
    'collection_id' => $collection_id,
    'email' => $_POST['email'],
    'name' => $_POST['name'],
    'amount' => $_POST['amount'] * 100, // in cents
    'callback_url' => 'https://yoursite.com/payment/callback',
    'description' => 'Order #' . $order_id
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://www.billplz.com/api/v3/bills');
curl_setopt($ch, CURLOPT_USERPWD, $api_key . ':');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$result = curl_exec($ch);
curl_close($ch);

$bill = json_decode($result);
header('Location: ' . $bill->url);
?>
```

**Google Maps Integration**:
```html
<div id="map" style="width: 100%; height: 400px;"></div>

<script>
function initMap() {
    const location = { lat: 1.7379, lng: 103.8984 }; // Kota Tinggi
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: location
    });
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        title: 'Kong Kiong Hardware'
    });
}
</script>
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap" async defer></script>
```

## Component Library

### Navigation Bar

**Desktop + Mobile Responsive**:
```html
<nav class="navbar">
    <div class="container">
        <a href="/" class="logo">
            <img src="logo.png" alt="Company Logo">
        </a>
        
        <button class="mobile-toggle" aria-label="Toggle menu">
            <span></span>
            <span></span>
            <span></span>
        </button>
        
        <ul class="nav-menu">
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/services">Services</a></li>
            <li><a href="/products">Products</a></li>
            <li><a href="/contact">Contact</a></li>
        </ul>
    </div>
</nav>

<style>
.navbar {
    background: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
}

.logo img {
    height: 50px;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
}

.mobile-toggle {
    display: none;
    flex-direction: column;
    gap: 4px;
    background: none;
    border: none;
    cursor: pointer;
}

.mobile-toggle span {
    width: 25px;
    height: 3px;
    background: #333;
    border-radius: 2px;
}

@media (max-width: 768px) {
    .mobile-toggle {
        display: flex;
    }
    
    .nav-menu {
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        background: #fff;
        flex-direction: column;
        gap: 0;
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }
    
    .nav-menu.active {
        max-height: 500px;
    }
    
    .nav-menu li {
        border-bottom: 1px solid #eee;
    }
    
    .nav-menu a {
        display: block;
        padding: 1rem 2rem;
    }
}
</style>

<script>
const mobileToggle = document.querySelector('.mobile-toggle');
const navMenu = document.querySelector('.nav-menu');

mobileToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});
</script>
```

### Hero Section

```html
<section class="hero">
    <div class="container">
        <h1>Your Trusted Hardware Partner</h1>
        <p>Quality tools and building materials since 1985</p>
        <div class="hero-cta">
            <a href="/products" class="btn btn-primary">Browse Products</a>
            <a href="/contact" class="btn btn-secondary">Contact Us</a>
        </div>
    </div>
</section>

<style>
.hero {
    background: linear-gradient(135deg, #0A192F 0%, #1E40AF 100%);
    color: white;
    padding: 8rem 2rem;
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.hero-cta {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.btn {
    padding: 1rem 2rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    transition: transform 0.2s;
}

.btn:hover {
    transform: translateY(-2px);
}

.btn-primary {
    background: #F97316;
    color: white;
}

.btn-secondary {
    background: white;
    color: #0A192F;
}

@media (max-width: 768px) {
    .hero {
        padding: 4rem 1rem;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
    
    .hero p {
        font-size: 1rem;
    }
}
</style>
```

### Product Card

```html
<div class="product-card">
    <div class="product-image">
        <img src="product.jpg" alt="Product name" loading="lazy">
        <span class="badge">New</span>
    </div>
    <div class="product-info">
        <h3>Product Name</h3>
        <p class="product-description">Brief description of the product</p>
        <div class="product-price">
            <span class="original-price">RM 150</span>
            <span class="sale-price">RM 120</span>
        </div>
        <button class="btn-add-to-cart">Add to Cart</button>
    </div>
</div>

<style>
.product-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.product-image {
    position: relative;
    padding-top: 100%; /* 1:1 Aspect Ratio */
    overflow: hidden;
}

.product-image img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: #F97316;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 600;
}

.product-info {
    padding: 1.5rem;
}

.product-info h3 {
    font-size: 1.125rem;
    margin-bottom: 0.5rem;
}

.product-description {
    color: #6B7280;
    font-size: 0.875rem;
    margin-bottom: 1rem;
}

.product-price {
    margin-bottom: 1rem;
}

.original-price {
    text-decoration: line-through;
    color: #9CA3AF;
    margin-right: 0.5rem;
}

.sale-price {
    font-size: 1.5rem;
    font-weight: 700;
    color: #F97316;
}

.btn-add-to-cart {
    width: 100%;
    padding: 0.75rem;
    background: #0A192F;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
}

.btn-add-to-cart:hover {
    background: #1E40AF;
}
</style>
```

## WordPress Development Checklist

When developing WordPress themes:

- [ ] Enqueue styles and scripts properly
- [ ] Use WordPress functions (wp_nav_menu, the_post_thumbnail)
- [ ] Implement template hierarchy correctly
- [ ] Add customizer options
- [ ] Make theme translation-ready
- [ ] Follow WordPress coding standards
- [ ] Sanitize and validate all inputs
- [ ] Use nonces for forms
- [ ] Implement proper error handling
- [ ] Test on multiple WordPress versions

## Testing Checklist

Before delivering to client:

**Functionality**:
- [ ] All links work
- [ ] Forms submit correctly
- [ ] Navigation works on all pages
- [ ] Search functionality (if applicable)
- [ ] Payment gateway (if e-commerce)
- [ ] Contact forms send emails

**Responsiveness**:
- [ ] Test on iPhone (Safari)
- [ ] Test on Android (Chrome)
- [ ] Test on iPad
- [ ] Test on Desktop (1920px)
- [ ] Test on Laptop (1280px)

**Performance**:
- [ ] PageSpeed Insights score > 80
- [ ] Images optimized
- [ ] CSS and JS minified
- [ ] Caching enabled
- [ ] Lazy loading implemented

**Browser Compatibility**:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers

**SEO**:
- [ ] Meta tags on all pages
- [ ] Alt text on images
- [ ] Proper heading hierarchy
- [ ] Sitemap.xml
- [ ] Robots.txt
- [ ] Google Analytics installed

**Security**:
- [ ] HTTPS/SSL installed
- [ ] Forms have CSRF protection
- [ ] No sensitive data in frontend code
- [ ] WordPress plugins updated
- [ ] Strong admin passwords

**Accessibility**:
- [ ] Color contrast passes WCAG
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Focus states visible
- [ ] ARIA labels where needed

## Handover Documentation

Create a client guide including:

1. **Login Credentials**
2. **How to Update Content**
3. **How to Add Products** (if e-commerce)
4. **How to Check Orders** (if e-commerce)
5. **How to Update Images**
6. **Backup Instructions**
7. **Emergency Contacts**
8. **Maintenance Schedule**

## Integration with Other Skills

Receives input from:
- **design-consultant**: Design specifications, mockups, color schemes
- **requirements-analyst**: Technical requirements, features list

Provides output to:
- **project-workflow**: Completed website, deployment details

## Quality Standards

All code must:
- Be clean and well-commented
- Follow consistent naming conventions
- Be properly indented
- Have no console errors
- Load in under 3 seconds
- Score 80+ on PageSpeed Insights
- Be responsive on all devices
- Pass W3C validation (or have documented exceptions)

---

**Remember**: Clean code is better than clever code. Future you (or other developers) will thank you for writing maintainable, well-documented code.
