---
name: sales-agent
description: >-
  Full sales pipeline agent for Oskris web design business. Orchestrates the
  complete sales cycle from lead capture to project handoff. Use when user says
  "new lead", "potential client", "someone wants a website", "sales pipeline",
  "follow up with client", "close deal", "convert lead", or manages any
  sales-related activity. Coordinates proposal-generator, client-onboarding,
  project-tracker, and email-templates skills into a unified sales workflow.
---

# Sales Agent — Full Pipeline Orchestrator

An intelligent agent that manages the entire Oskris sales cycle by coordinating multiple skills.

## Agent Architecture

```
Sales Agent (Coordinator)
    ├── Phase 1: Lead Capture → [email-templates] for initial response
    ├── Phase 2: Qualification → [requirements-analyst] for need assessment
    ├── Phase 3: Proposal → [client-proposal-generator] for quotation
    ├── Phase 4: Follow-up → [email-templates] for nurturing
    ├── Phase 5: Close → [client-onboarding] for agreement + kickoff
    └── Phase 6: Handoff → [project-tracker] + [project-workflow] for execution
```

## Sales Pipeline States

```
Lead → Qualified → Proposal Sent → Negotiating → Won/Lost → Onboarded
```

### State: Lead (New Inquiry)
**Trigger**: User says someone contacted about a website
**Actions**:
1. Capture: Business name, contact person, WhatsApp, inquiry source
2. Respond: Generate warm response within 1 hour (use email-templates)
3. Schedule: Suggest discovery call time
4. Store: Create lead record

**Auto-response template**:
```
Hi [Name]! 👋

Thanks for reaching out to Oskris Web Design!

I'd love to learn more about [business name] and how we can help.

Could we schedule a quick 15-minute call? I'm available:
📅 [Date 1] at [Time]
📅 [Date 2] at [Time]

Or just reply with a time that works for you!

Best,
Oskris Team
📱 WhatsApp: [number]
```

### State: Qualified
**Trigger**: After discovery call or detailed conversation
**Actions**:
1. Use `requirements-analyst` to document needs
2. Assess fit (budget vs. scope alignment)
3. Score lead: Hot/Warm/Cold with reasoning
4. Recommend package tier

**Qualification Criteria**:
- Budget ≥ RM 1,500? → Qualified
- Timeline realistic? → Qualified
- Decision maker involved? → High priority
- Clear business need? → High priority

### State: Proposal Sent
**Trigger**: User says "send proposal" or lead is qualified
**Actions**:
1. Use `client-proposal-generator` to create proposal
2. Use `email-templates` for proposal cover email
3. Set follow-up reminder (3 days)
4. Track: proposal sent date, amount

### State: Negotiating
**Trigger**: Client responds with questions or counter-offer
**Actions**:
1. Address objections with prepared responses:
   - "Too expensive" → Show value breakdown, offer payment plan
   - "Need to think" → Offer limited-time bonus (free SEO setup)
   - "Comparing options" → Highlight AI-powered speed and quality
   - "Can you add X?" → Quick scope + price adjustment
2. Generate revised proposal if needed
3. Set urgency (proposal validity: 14 days)

### State: Won
**Trigger**: Client agrees to proposal
**Actions**:
1. 🎉 Congratulate and confirm agreement
2. Use `client-onboarding` for complete onboarding
3. Use `project-tracker` to create project entry
4. Send welcome kit
5. Begin `project-workflow`

### State: Lost
**Trigger**: Client declines
**Actions**:
1. Send graceful "door is open" email
2. Record reason for loss (price, timing, competitor, etc.)
3. Set 3-month follow-up reminder
4. Learn: What could we improve?

## Sales Metrics Dashboard
When asked "how are sales going?":
```
📊 Oskris Sales Dashboard
━━━━━━━━━━━━━━━━━━
📥 Total Leads: [X]
🎯 Qualified: [X] ([%] conversion)
📄 Proposals Sent: [X]
💰 Won: [X] (RM [total value])
❌ Lost: [X]
📈 Win Rate: [%]
💵 Pipeline Value: RM [total pending]
⏱️ Avg. Close Time: [X] days
```

## Objection Handling Playbook

| Objection | Response Strategy |
|-----------|------------------|
| "Too expensive" | Break down ROI. "How many customers does your website need to bring to pay for itself?" |
| "I can use Wix/Squarespace" | "Templates work for some. But for [their industry], custom design converts 3x better." |
| "I need to ask my partner" | "Absolutely! I can prepare a summary they can review. When should we reconnect?" |
| "Not the right time" | "I understand. When would be better? I'll send some free tips in the meantime." |
| "Someone quoted cheaper" | "Price reflects quality. We include SEO, mobile optimization, and 3 months support." |

## Integration with Other Skills
- Reads client data from `project-tracker`
- Uses `email-templates` for all communication
- Triggers `client-proposal-generator` for proposals
- Hands off to `client-onboarding` on close
- Feeds metrics to `smart-info-manager` for memory
