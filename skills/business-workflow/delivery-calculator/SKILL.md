---
name: delivery-calculator
description: >-
  Calculate transport delivery fees for Kong Kiong Hardware (KKH).
  Use when user mentions "delivery fee", "transport cost", "运费", "运输费",
  "KKH delivery", "lorry fee", "送货费", or needs to calculate transport
  charges for hardware store deliveries. Supports 4 main routes from Kota Tinggi
  with driver commission calculations. All prices in RM.
---

# Delivery Calculator — Kong Kiong Hardware

Calculate transport fees and driver commissions for KKH deliveries.

## Route Map

### Route 1: Jalan Kg Sayang
| Distance | Small Lorry | Large Lorry |
|----------|------------|------------|
| 0-5 km | RM 10-30 | RM 20-60 |
| 5-10 km | RM 30-60 | RM 60-120 |
| 10-20 km | RM 60-120 | RM 120-240 |

### Route 2: Jalan Sedili Kecil
| Distance | Small Lorry | Large Lorry |
|----------|------------|------------|
| 0-10 km | RM 20-50 | RM 40-100 |
| 10-20 km | RM 50-100 | RM 100-200 |
| 20-30 km | RM 100-150 | RM 200-300 |

### Route 3: Jalan Sedili Besar
| Distance | Small Lorry | Large Lorry |
|----------|------------|------------|
| 0-10 km | RM 20-50 | RM 40-100 |
| 10-20 km | RM 50-120 | RM 100-240 |
| 20-40 km | RM 120-200 | RM 240-400 |

### Route 4: Tanjung Sedili
| Distance | Small Lorry | Large Lorry |
|----------|------------|------------|
| 0-15 km | RM 30-80 | RM 60-160 |
| 15-30 km | RM 80-150 | RM 160-300 |
| 30+ km | RM 150-250 | RM 300-500 |

## Pricing Rules
- Large lorry = 2x small lorry fee
- Heavy/bulky items (sand, cement, steel) may add 10-20% surcharge
- Weekend/holiday delivery: +RM 20-50
- Urgent same-day: +30%
- Multiple delivery points: +RM 20 per stop

## Commission Calculator

### Single Driver
```
Commission = Transport Fee × 10%
```

### Driver + Assistant
```
Driver Commission = Transport Fee × 8%
Assistant Commission = Transport Fee × 2%
Total Commission = Transport Fee × 10%
```

## Quick Calculator

Input needed:
1. Route (1-4)
2. Lorry size (small/large)
3. Approximate distance (km)
4. Crew type (solo/with assistant)

Output:
```
🚛 KKH Delivery Quote
━━━━━━━━━━━━━━━━━━
📍 Route: [Route name]
📏 Distance: ~[X] km
🚗 Lorry: [Small/Large]
💰 Transport Fee: RM [amount]
👨‍✈️ Driver Commission: RM [amount] ([%])
👷 Assistant Commission: RM [amount] ([%])
━━━━━━━━━━━━━━━━━━
💵 Total Cost: RM [amount]
```

## Bulk Calculation
For monthly reports, calculate totals for multiple deliveries:
- Total deliveries count
- Total transport fees
- Total commissions (driver + assistant breakdown)
- Average fee per delivery
- Most common route
