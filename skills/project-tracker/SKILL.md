---
name: project-tracker
description: >-
  Track web design project progress, milestones, and deliverables.
  Use when user asks "project status", "where are we with [project]",
  "update project", "track progress", "milestone check", "project report",
  or needs to review or update any ongoing web design project status.
  Maintains project state in GitHub and generates status reports.
---

# Project Tracker

Track and report on all active Oskris web design projects.

## Project States
```
Discovery → Design → Development → Review → Testing → Launch → Maintenance
```

Each state has defined entry/exit criteria:

| State | Entry Criteria | Exit Criteria | Typical Duration |
|-------|---------------|---------------|-----------------|
| Discovery | Client signed agreement | Requirements doc approved | 2-3 days |
| Design | Requirements approved | Design mockup approved by client | 3-5 days |
| Development | Design approved | All pages coded and functional | 7-14 days |
| Review | Development complete | Internal QA passed | 2-3 days |
| Testing | QA passed | Client preview approved | 2-3 days |
| Launch | Client approved | Site live, DNS propagated | 1-2 days |
| Maintenance | Site launched | Ongoing (monthly) | Continuous |

## Project File Structure
Each project tracked in GitHub:
```
projects/websites/[client-name]/
├── README.md              # Project overview + current status
├── discovery/
│   ├── requirements.md    # Client requirements
│   └── competitor-analysis.md
├── design/
│   ├── brand-kit.md       # Colors, fonts, style
│   └── wireframes/        # Page wireframes
├── build/                 # Actual website files
├── review/
│   └── review-report.md   # QA results
└── launch/
    └── launch-checklist.md
```

## Status Report Format

### Quick Status (for WhatsApp/chat)
```
📊 [Project Name] Status Update
━━━━━━━━━━━━━━━━━━
📍 Phase: [Current Phase] ([X]% complete)
✅ Done: [Last completed milestone]
🔄 Current: [What's being worked on]
⏭️ Next: [Next milestone]
📅 ETA: [Expected completion date]
⚠️ Blockers: [Any issues] or None
```

### Detailed Report (for formal updates)
Generate comprehensive report with:
- Project overview and timeline
- Completed milestones with dates
- Current phase progress percentage
- Upcoming deliverables
- Budget tracking (spent vs. remaining)
- Risk assessment
- Client action items pending

## Commands

- "Show all projects" → List all active projects with quick status
- "Update [project] to [phase]" → Move project to new phase
- "Project report for [client]" → Generate detailed status report
- "What's blocked?" → Show all projects with blockers
- "This week's tasks" → Show deliverables due this week

## Automation
- Update project README.md on GitHub when status changes
- Alert when project is behind schedule (compare actual vs. planned dates)
- Generate weekly summary of all active projects every Monday
- Track revision count per project (warn at revision #3)
