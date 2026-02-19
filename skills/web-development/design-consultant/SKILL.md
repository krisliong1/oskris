---
name: design-consultant  
description: Professional web design consultation and proposal creation. Use when translating requirements into design solutions, creating design proposals, selecting color schemes, planning layouts, or presenting design concepts to clients. Works with output from requirements-analyst skill.
---

# Design Consultant Skill

This skill helps you create professional design proposals and visual concepts based on client requirements. It bridges business needs with aesthetic solutions.

## When to Use This Skill

- After requirements are gathered (from requirements-analyst skill)
- Creating design proposals for clients
- Selecting appropriate visual styles
- Planning website layouts and structure
- Presenting design options to clients
- Making design decisions during development

## Input Requirements

This skill works best when you have:
- Completed requirements document
- Understanding of client's business
- Knowledge of target audience
- Budget constraints
- Brand assets (if available)

## Core Design Framework

### 1. Style Analysis (风格分析)

Based on client's business type, recommend appropriate design styles:

**E-commerce / Gaming**:
- Modern, tech-forward aesthetics
- Dark themes with neon accents
- High contrast for CTAs
- Grid-based product layouts
- Fast-loading, image-optimized
- Example: GameShop.my style

**Corporate / Professional Services**:
- Clean, minimal design
- Trust-building elements
- Professional color schemes (blues, grays)
- Clear hierarchy
- Certificate/award displays

**Creative / Portfolio**:
- Bold, unique layouts
- Showcase-focused design
- Artistic typography
- Generous white space
- Interactive elements

**Local Retail / Hardware**:
- Practical, functional design
- Clear navigation
- Product-focused layout
- Mobile-friendly (Malaysian users browse on phones)
- WhatsApp integration

### 2. Color Scheme Selection (配色方案)

#### Process:
1. **Analyze brand colors** (if existing logo/brand)
2. **Consider industry standards**
3. **Test for accessibility** (WCAG compliance)
4. **Create palette variants** (light/dark themes)

#### Recommended Palettes by Industry:

**Gaming/Tech**:
```
Primary: #0A192F (Deep Space Blue)
Secondary: #00D1FF (Neon Blue)
Accent: #F97316 (Energy Orange)
Background: #111827 (Dark)
Text: #FFFFFF, #E5E7EB
```

**Professional/Corporate**:
```
Primary: #1E40AF (Professional Blue)
Secondary: #6B7280 (Neutral Gray)
Accent: #10B981 (Success Green)
Background: #F9FAFB (Light)
Text: #111827, #6B7280
```

**Creative/Modern**:
```
Primary: #7C3AED (Vibrant Purple)
Secondary: #EC4899 (Pink)
Accent: #F59E0B (Amber)
Background: #FFFFFF
Text: #1F2937
```

**Local/Traditional**:
```
Primary: #DC2626 (Red - Malaysian preference)
Secondary: #059669 (Green)
Accent: #F59E0B (Gold)
Background: #FFFFFF
Text: #1F2937
```

### 3. Typography Selection (字体选择)

#### Principles:
- Maximum 2-3 font families
- Pair display font with readable body font
- Consider multilingual support (English + Chinese/Malay)
- Web-safe fonts or Google Fonts

#### Recommended Pairings:

**Modern/Tech**:
- Headers: Orbitron / Space Grotesk
- Body: Inter / Roboto

**Professional**:
- Headers: Playfair Display / Merriweather
- Body: Open Sans / Lato

**Friendly/Approachable**:
- Headers: Poppins / Nunito
- Body: Mukta / Noto Sans

**Malaysian Multi-lingual**:
- Use: Noto Sans (supports Chinese characters)
- Or: Roboto + Noto Sans CJK

### 4. Layout Planning (布局规划)

#### Standard Page Layouts:

**Homepage Structure**:
```
1. Hero Section
   - Headline + Subheadline
   - CTA button
   - Hero image/video

2. Trust Indicators
   - Years in business
   - Certifications
   - Customer count

3. Services/Products Overview
   - 3-4 key offerings
   - With icons/images

4. Social Proof
   - Testimonials
   - Case studies
   - Logos of clients

5. Call-to-Action
   - Contact form
   - WhatsApp button
   - Phone number

6. Footer
   - Site map
   - Contact info
   - Social media
```

**Product Page (E-commerce)**:
```
1. Product Images (gallery)
2. Product name + price
3. Description
4. Specifications
5. Add to cart button
6. Related products
7. Reviews
```

**About Page**:
```
1. Company story
2. Team photos
3. Values/mission
4. Timeline
5. Certifications
```

### 5. Component Design (组件设计)

#### Essential Components:

**Navigation Bar**:
- Logo (left)
- Main menu (center/right)
- Search (if e-commerce)
- Shopping cart icon (if e-commerce)
- Language switcher (if multilingual)
- Mobile hamburger menu

**Hero Section Options**:
- Full-width image + text overlay
- Split (image left, text right)
- Video background
- Carousel/slider
- Illustrated

**Product Cards**:
```
- Product image
- Product name
- Price (with/without discount)
- Quick view button
- Add to cart button
- Rating stars
- Badge (NEW / SALE / OUT OF STOCK)
```

**Contact Forms**:
```
Fields:
- Name (required)
- Email (required)
- Phone (required)
- Subject (optional)
- Message (required)
- Submit button

Include:
- WhatsApp quick contact
- Phone click-to-call
- Business hours display
```

**Footer Design**:
```
Columns:
1. About + Logo
2. Quick Links
3. Services
4. Contact Info

Bottom Bar:
- Copyright
- Privacy Policy
- Terms
- Payment methods icons
```

### 6. Mobile-First Considerations

**Malaysian Market Insights**:
- 70%+ users browse on mobile
- Mobile speed is critical
- WhatsApp integration essential
- Touch-friendly buttons (min 44x44px)
- Simplified mobile navigation

**Mobile Optimizations**:
- Single column layouts
- Larger touch targets
- Sticky CTA buttons
- Lazy-load images
- Compressed assets
- AMP pages (optional)

### 7. Cultural & Local Adaptations

**For Malaysian Clients**:

**Color Psychology**:
- Red: Popular, associated with prosperity
- Gold: Premium, luxury
- Green: Islamic significance, growth
- Avoid: Excessive black (funeral associations)

**Imagery**:
- Reflect Malaysian diversity
- Include multiple ethnicities
- Local landmarks (if relevant)
- Avoid culturally insensitive images

**Language Considerations**:
- Offer BM / EN / CN options
- Use proper translations (not machine)
- Right-to-left not needed (Arabic not common)

**Payment Icons**:
- Display FPX, Boost, TNG, GrabPay
- Credit card logos
- "Secure Payment" badges

## Design Proposal Template

Create proposals in this format:

```markdown
# Design Proposal
**Project**: [Client Name] Website  
**Date**: [Date]  
**Prepared by**: Oskris Web Development

## 1. Design Concept Overview

[Brief description of the overall design direction]

## 2. Visual Style

**Design Mood**: [Modern / Professional / Creative / Traditional]

**Key Characteristics**:
- [Characteristic 1]
- [Characteristic 2]
- [Characteristic 3]

**Inspiration Sources**:
- [Reference website 1]
- [Reference website 2]

## 3. Color Palette

**Primary Color**: [Hex code] - [Usage]
**Secondary Color**: [Hex code] - [Usage]
**Accent Color**: [Hex code] - [Usage]
**Background**: [Hex code]
**Text Colors**: [Hex codes]

[Include color swatch visual if possible]

## 4. Typography

**Headings**: [Font name]
- H1: [Size]px, [Weight]
- H2: [Size]px, [Weight]
- H3: [Size]px, [Weight]

**Body Text**: [Font name]
- Regular: [Size]px
- Line height: [Value]

**Special Elements**: [Font for buttons, labels, etc.]

## 5. Layout Structure

### Homepage:
- Hero: [Description]
- Section 1: [Content type]
- Section 2: [Content type]
- Section 3: [Content type]
- Footer

### Product/Service Pages:
[Layout description]

### About/Contact Pages:
[Layout description]

## 6. Key Design Elements

**Navigation**:
- [Style description]
- [Mobile behavior]

**Buttons**:
- Primary CTA: [Style]
- Secondary actions: [Style]

**Forms**:
- [Style description]

**Icons**:
- [Icon style - line / filled / custom]

## 7. Responsive Behavior

**Desktop (1280px+)**: [Description]
**Tablet (768-1279px)**: [Description]
**Mobile (<768px)**: [Description]

## 8. Special Features

- [Feature 1]
- [Feature 2]
- [Feature 3]

## 9. Design Deliverables

**Phase 1 - Wireframes**:
- Homepage wireframe
- Inner page wireframes
- Mobile wireframes

**Phase 2 - Mockups**:
- Homepage design (desktop + mobile)
- 2-3 inner pages
- Component library

**Phase 3 - Assets**:
- Logo (if designing new)
- Icons
- Illustrations (if any)
- Stock photos selection

## 10. Timeline

- Wireframes delivery: [Date]
- Design mockups: [Date]
- Revisions completed: [Date]
- Final design approval: [Date]

## 11. Revision Policy

- Included: [Number] rounds of revisions
- Additional revisions: RM [Amount] per round

## 12. Next Steps

1. Review and approve this proposal
2. Provide feedback on style direction
3. Proceed to wireframe phase
```

## Design Decision Framework

When making design choices, ask:

1. **Does it serve the user goal?**
   - Easy to find information?
   - Clear call-to-action?
   - Reduces friction?

2. **Does it reflect the brand?**
   - Matches brand personality?
   - Consistent with existing materials?
   - Appeals to target audience?

3. **Is it technically feasible?**
   - Can be built within budget?
   - Will load quickly?
   - Works on all devices?

4. **Is it accessible?**
   - Color contrast ratio ≥ 4.5:1
   - Text is readable
   - Works with screen readers
   - Keyboard navigable

5. **Is it maintainable?**
   - Client can update content?
   - Design system is documented?
   - Scales with growth?

## Common Design Challenges & Solutions

### Challenge 1: Client wants "everything above the fold"

**Solution**:
- Explain user scroll behavior (they do scroll!)
- Prioritize most important content
- Use visual hierarchy to guide attention
- Progressive disclosure strategy

### Challenge 2: "Make the logo bigger"

**Solution**:
- Explain balance and visual hierarchy
- Show examples of professional sites
- A/B test if needed
- Compromise: prominent placement vs size

### Challenge 3: Too many colors/fonts

**Solution**:
- Educate on brand consistency
- Show examples of cohesive designs
- Limit palette to 3-4 colors
- Maximum 2 font families

### Challenge 4: Client provides low-quality images

**Solution**:
- Explain image quality importance
- Offer photography service (+ RM fee)
- Source stock photos
- Use illustrations as alternative

### Challenge 5: "Make it like [famous brand]"

**Solution**:
- Understand what they like specifically
- Explain budget differences
- Create inspired-by version
- Set realistic expectations

## Integration with Other Skills

Receives input from:
- **requirements-analyst**: Business needs, target audience, budget

Provides output to:
- **frontend-builder**: Design specifications for implementation
- **project-workflow**: Design milestones and deliverables

## Tools & Resources

**Design Tools** (for creating mockups):
- Figma (free, collaborative)
- Canva (quick mockups)
- Adobe XD (professional)

**Color Tools**:
- Coolors.co (palette generator)
- Adobe Color (harmony rules)
- WebAIM Contrast Checker

**Typography**:
- Google Fonts
- Font Pair (pairing suggestions)

**Inspiration**:
- Dribbble
- Awwwards
- SiteInspire
- Local Malaysian websites

**Stock Photos**:
- Unsplash (free)
- Pexels (free)
- Pixabay (free)

## Quality Checklist

Before presenting design proposal:

- [ ] Color palette has good contrast
- [ ] Typography is readable at all sizes
- [ ] Layout works on mobile
- [ ] Matches client's brand (if existing)
- [ ] Appeals to target audience
- [ ] Technically feasible within budget
- [ ] All required pages planned
- [ ] CTA buttons are prominent
- [ ] Forms are user-friendly
- [ ] Footer has all necessary info
- [ ] Design system is documented
- [ ] Client can understand the proposal
- [ ] Timeline is realistic
- [ ] Revision policy is clear

---

**Remember**: Good design is invisible - it works so well users don't notice it. Focus on usability first, aesthetics second.
