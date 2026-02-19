---
name: client-onboarding
description: >-
  Standardized client onboarding workflow for new web design projects.
  Use when user says "new client", "onboard client", "start project with client",
  "client intake", "kickoff meeting", or begins working with a new web design customer.
  Generates intake questionnaires, welcome emails, project briefs, and sets up
  project structure. Coordinates with proposal-generator and project-workflow skills.
---

# Client Onboarding

Standardized process for onboarding new Oskris web design clients from first contact to project kickoff.

## Onboarding Pipeline

```
Lead Contact → Qualification → Proposal → Agreement → Onboarding → Kickoff
```

### Phase 1: Lead Qualification (Day 0)
Ask/confirm these questions:
1. Business name, industry, location
2. Current website (if any) — get URL
3. What problem are they trying to solve?
4. Budget range and timeline expectations
5. Decision maker(s) — who approves?
6. How they found us (referral, search, social?)

Score the lead:
- **Hot** (ready to buy, clear budget, urgent need)
- **Warm** (interested, needs convincing, flexible timeline)
- **Cold** (just exploring, no budget committed)

### Phase 2: Discovery Call Prep
Generate a discovery call guide with:
- Personalized questions based on their industry
- Competitor website analysis (2-3 competitors)
- Preliminary recommendations to show expertise
- Talking points that address their pain points

### Phase 3: Proposal & Agreement
- Trigger `client-proposal-generator` skill for formal proposal
- Include service agreement template with:
  - Scope of work
  - Payment terms (50/50 or 40/30/30)
  - Revision policy (3 rounds included)
  - Timeline commitments
  - IP ownership transfer on final payment
  - Cancellation terms

### Phase 4: Client Onboarding Kit
After agreement signed, generate:

1. **Welcome Email** — Thank them, introduce next steps, set expectations
2. **Content Collection Checklist**:
   - Logo files (SVG/PNG, high-res)
   - Brand colors (hex codes if known)
   - Business photos (team, products, location)
   - Copy/text for each page
   - Social media links
   - Google Business Profile access
3. **Brand Questionnaire**:
   - Describe your brand in 3 words
   - Target audience description
   - Websites you like (and why)
   - Websites you dislike (and why)
   - Must-have features
   - Competitor URLs
4. **Project Timeline** — Milestone dates
5. **Communication Plan** — WhatsApp group setup, weekly update schedule

### Phase 5: Project Kickoff
- Create project folder structure (local + GitHub)
- Set up project tracking
- Schedule kickoff meeting
- Assign internal milestones

## Templates

### Welcome Email Template (Malay/Chinese/English)
Subject: Welcome to Oskris! Your Website Project Starts Now 🎉

Hi [Client Name],

Thank you for choosing Oskris for your website project! We're excited to work with you.

Here's what happens next:
1. Please complete the attached questionnaire (5-10 minutes)
2. Send us your logo, photos, and text content
3. We'll schedule a kickoff call within [X] days
4. First draft delivery: [Date]

Questions? WhatsApp us anytime at [Number].

Best regards,
Oskris Web Design Team

## Automation Rules
- Auto-create GitHub project folder: `projects/websites/[client-name]/`
- Auto-generate discovery/ subfolder with all intake documents
- Store client info in structured format for future reference
- Set calendar reminders for follow-ups
