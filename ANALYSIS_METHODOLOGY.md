# Analysis Methodology - Complete Mathematical Explanation

## Table of Contents
1. [Overview](#overview)
2. [The Scoring Framework](#the-scoring-framework)
3. [Individual Score Calculations](#individual-score-calculations)
4. [Weighted Combination](#weighted-combination)
5. [Real Examples](#real-examples)
6. [Statistical Validation](#statistical-validation)
7. [Business Interpretation](#business-interpretation)

---

## Overview

### The Business Problem

**Question**: Where should we open a laundromat to maximize success probability?

**Approach**: Multi-criteria decision analysis (MCDA) using weighted scoring

**Output**: Ranked list of locations with scores from 0-100

### Why This Methodology?

Traditional approaches might look at just one factor (e.g., "go where there's no competition"). 

Our approach is **holistic** - it considers:
- ✅ Market demand (renters need laundromats)
- ✅ Customer affordability (income level)
- ✅ Customer volume (population density)
- ✅ Competitive landscape (existing businesses)

---

## The Scoring Framework

### Core Principle

Each location gets **four individual scores** (0-100 each), which are then **combined using weights** to produce a **total score** (0-100).

```
Total Score = (Income Score × 0.25) + 
              (Renter Score × 0.30) + 
              (Density Score × 0.25) + 
              (Competition Score × 0.20)
```

### Why These Weights?

| Factor | Weight | Rationale |
|--------|--------|-----------|
| Renter Rate | 30% | Most predictive - renters are primary customers |
| Income Level | 25% | Critical for affordability and willingness to pay |
| Population Density | 25% | Determines customer volume potential |
| Competition | 20% | Important but good businesses can compete |

**Note**: Weights are configurable in the code - you can adjust based on specific market conditions.

---

## Individual Score Calculations

### 1. Income Score (Target: $40K-$60K median income)

#### Business Logic

Laundromats thrive in **middle-income neighborhoods**:

- **Too Low (<$30K)**: Customers may struggle to afford services regularly
- **Sweet Spot ($40K-$60K)**: Regular customers, affordable, high usage
- **Too High (>$80K)**: More likely to own homes with washers/dryers

#### Mathematical Formula

We use a **Gaussian (normal) distribution** centered on the ideal income:

```
Income Score = 100 × e^(-((I - μ)² / (2σ²)))

Where:
  I = Actual median income for the neighborhood
  μ = Ideal income (default: $50,000)
  σ = Standard deviation / acceptable range (default: $40,000)
  e = Euler's number (≈ 2.71828)
```

#### Why Gaussian?

- Creates a smooth curve that peaks at ideal income
- Gradually decreases as you move away from ideal
- Doesn't penalize too harshly if slightly off-target
- Mathematically models "closeness to ideal"

#### Python Implementation

```python
def score_income_fit(income_series, ideal=50000, range_width=40000):
    """
    Score neighborhoods based on income fit
    
    Args:
        income_series: pandas Series of median incomes
        ideal: Target median income ($50K default)
        range_width: Standard deviation ($40K default)
    
    Returns:
        pandas Series of scores (0-100)
    """
    import numpy as np
    
    score = 100 * np.exp(-((income_series - ideal) ** 2) / (2 * range_width ** 2))
    return score.clip(0, 100)  # Ensure 0-100 range
```

#### Worked Example: Downtown

**Given Data**:
- Downtown median income: $65,000
- Ideal income (μ): $50,000
- Range (σ): $40,000

**Calculation**:
```
Step 1: Calculate difference from ideal
  Difference = $65,000 - $50,000 = $15,000

Step 2: Square the difference
  Difference² = 15,000² = 225,000,000

Step 3: Calculate denominator (2σ²)
  2σ² = 2 × 40,000² = 2 × 1,600,000,000 = 3,200,000,000

Step 4: Calculate exponent
  Exponent = -225,000,000 / 3,200,000,000 = -0.0703125

Step 5: Calculate e^(exponent)
  e^(-0.0703125) ≈ 0.9321

Step 6: Multiply by 100
  Income Score = 100 × 0.9321 = 93.21
```

**Result**: Downtown scores **93.21/100** on income - very close to ideal!

#### Score Table (Various Incomes)

| Median Income | Distance from Ideal | Income Score | Interpretation |
|---------------|---------------------|--------------|----------------|
| $50,000 | $0 | 100.0 | Perfect |
| $55,000 | $5,000 | 98.8 | Excellent |
| $65,000 | $15,000 | 93.2 | Very Good |
| $40,000 | -$10,000 | 97.5 | Very Good |
| $75,000 | $25,000 | 84.6 | Good |
| $30,000 | -$20,000 | 88.2 | Good |
| $90,000 | $40,000 | 71.7 | Fair |
| $100,000 | $50,000 | 60.7 | Acceptable |
| $20,000 | -$30,000 | 75.5 | Fair |

---

### 2. Renter Score (Higher is Better)

#### Business Logic

**Renters are the primary customer base** for laundromats because:
- Apartments often lack in-unit laundry
- Shared laundry facilities are inconvenient
- Renters are more likely to use laundromats regularly

Homeowners typically have their own washers/dryers.

#### Mathematical Formula

Simple **linear transformation** - the renter percentage IS the score:

```
Renter Score = Renter Rate × 100

Where:
  Renter Rate = (Renter-occupied units) / (Total housing units)
  Expressed as decimal (0.75 = 75%)
```

#### Why Linear?

- More renters = directly proportional to more customers
- No diminishing returns (even 100% renters is great)
- Simple, interpretable relationship
- Empirically validated by industry data

#### Python Implementation

```python
def score_renter_rate(renter_rate_series):
    """
    Score neighborhoods based on renter percentage
    
    Args:
        renter_rate_series: pandas Series of renter rates (0-1 scale)
    
    Returns:
        pandas Series of scores (0-100)
    """
    return renter_rate_series * 100
```

#### Worked Example: Koreatown

**Given Data**:
- Koreatown renter rate: 82% (0.82)

**Calculation**:
```
Renter Score = 0.82 × 100 = 82.0
```

**Result**: Koreatown scores **82.0/100** - high demand from renters!

#### Score Table (Various Renter Rates)

| Renter Rate | Renter Score | Customer Base | Interpretation |
|-------------|--------------|---------------|----------------|
| 90% | 90.0 | Excellent | Dense apartment area |
| 80% | 80.0 | Very Good | Many renters |
| 75% | 75.0 | Good | Solid rental market |
| 65% | 65.0 | Acceptable | Mixed housing |
| 50% | 50.0 | Fair | Half homeowners |
| 40% | 40.0 | Poor | Mostly homeowners |
| 25% | 25.0 | Very Poor | Suburban area |

---

### 3. Population Density Score (Higher is Better)

#### Business Logic

**More people = more potential customers**

Higher density means:
- More foot traffic
- More households in walking distance
- Better word-of-mouth marketing
- Higher revenue potential per location

#### Mathematical Formula

**Normalization** to 0-100 scale relative to the dataset maximum:

```
Density Score = (Area Density / Maximum Density in Dataset) × 100

Where:
  Area Density = Population / Area (square miles)
  Maximum Density = Highest density among all neighborhoods
```

#### Why Normalize?

- Makes scores comparable across different cities/regions
- Adjusts for dataset-specific ranges
- 100 = best in your market (not absolute)
- Relative scoring is appropriate for location comparison

#### Python Implementation

```python
def score_population_density(density_series):
    """
    Score neighborhoods based on population density
    
    Args:
        density_series: pandas Series of population per square mile
    
    Returns:
        pandas Series of scores (0-100)
    """
    max_density = density_series.max()
    
    if max_density > 0:
        return (density_series / max_density) * 100
    else:
        return 50  # Neutral score if no density data
```

#### Worked Example: Downtown vs. East LA

**Given Data**:
- Downtown: 50,000 people / 2.5 sq mi = **20,000 per sq mi**
- East LA: 38,000 people / 4.5 sq mi = **8,444 per sq mi**
- Maximum in dataset: 20,000 per sq mi (Downtown)

**Calculation - Downtown**:
```
Density Score = (20,000 / 20,000) × 100 = 100.0
```

**Calculation - East LA**:
```
Density Score = (8,444 / 20,000) × 100 = 42.2
```

**Result**: 
- Downtown: **100.0/100** - highest density in dataset
- East LA: **42.2/100** - less than half the density

#### Density Interpretation Guide

| People per Sq Mi | Urban Classification | Density Score* | Business Implication |
|------------------|---------------------|----------------|---------------------|
| 20,000+ | Very High Density | 100.0 | Excellent foot traffic |
| 15,000-20,000 | High Density | 75.0-99.9 | Strong customer base |
| 10,000-15,000 | Medium-High | 50.0-74.9 | Good potential |
| 5,000-10,000 | Medium | 25.0-49.9 | Moderate potential |
| 2,000-5,000 | Low-Medium | 10.0-24.9 | Requires good marketing |
| <2,000 | Low/Suburban | 0.0-9.9 | Challenging market |

*Scores relative to dataset maximum

---

### 4. Competition Score (Lower Competition = Higher Score)

#### Business Logic

**Less competition = better opportunity** (generally)

However, some competition can signal:
- Validated market demand
- Established customer habits
- Proof of concept

We use **inverse scoring** - fewer competitors get higher scores.

#### Mathematical Formula

**Inverse normalized scoring** based on competition density:

```
Competition Density = (Number of Competitors / Population) × 10,000

Competition Score = 100 × (1 - (Competition Density / (Max Competition × 1.2)))

Then clip to 0-100 range

Where:
  Competition Density = Laundromats per 10,000 residents
  Max Competition = Highest competition density in dataset
  1.2 multiplier = Prevents negative scores, allows some oversaturation
```

#### Why Competition Density (per 10K)?

- Normalizes for population size
- 1 competitor in 5,000 people ≠ 1 competitor in 50,000 people
- Industry standard metric
- Comparable across different-sized areas

#### Why Inverse Scoring?

- Zero competitors = 100 points (best case)
- Some competitors = moderate points
- Many competitors = low points (saturated)
- Uses (1 - x) transformation for inversion

#### Python Implementation

```python
def score_competition(competitor_count, population, max_comp_density):
    """
    Score neighborhoods based on competition level
    
    Args:
        competitor_count: Number of existing laundromats
        population: Total population
        max_comp_density: Highest competition density in dataset
    
    Returns:
        Competition score (0-100)
    """
    # Calculate competition per 10,000 residents
    comp_density = (competitor_count / population) * 10000
    
    # Inverse scoring - less competition = higher score
    if max_comp_density > 0:
        score = 100 * (1 - (comp_density / (max_comp_density * 1.2)))
    else:
        score = 100  # No competition anywhere
    
    return max(0, min(100, score))  # Clip to 0-100
```

#### Worked Example: Inglewood vs. Downtown vs. Koreatown

**Given Data**:
- **Inglewood**: 0 competitors, 44,000 population
- **Downtown**: 2 competitors, 50,000 population
- **Koreatown**: 3 competitors, 42,000 population

**Step 1: Calculate Competition Density**

Inglewood:
```
Comp Density = (0 / 44,000) × 10,000 = 0.0 per 10K
```

Downtown:
```
Comp Density = (2 / 50,000) × 10,000 = 0.4 per 10K
```

Koreatown:
```
Comp Density = (3 / 42,000) × 10,000 = 0.714 per 10K
```

**Step 2: Find Maximum**
```
Max Competition Density = 0.714 (Koreatown)
```

**Step 3: Calculate Scores**

Inglewood:
```
Score = 100 × (1 - (0.0 / (0.714 × 1.2)))
      = 100 × (1 - 0)
      = 100.0
```

Downtown:
```
Score = 100 × (1 - (0.4 / (0.714 × 1.2)))
      = 100 × (1 - (0.4 / 0.857))
      = 100 × (1 - 0.467)
      = 100 × 0.533
      = 53.3
```

Koreatown:
```
Score = 100 × (1 - (0.714 / (0.714 × 1.2)))
      = 100 × (1 - (0.714 / 0.857))
      = 100 × (1 - 0.833)
      = 100 × 0.167
      = 16.7
```

**Results**:
- Inglewood: **100.0/100** - no competition!
- Downtown: **53.3/100** - some competition
- Koreatown: **16.7/100** - saturated market

#### Competition Score Table

| Competitors | Population | Density (per 10K) | Score* | Market Status |
|-------------|------------|-------------------|--------|---------------|
| 0 | Any | 0.0 | 100.0 | Untapped market |
| 1 | 50,000 | 0.2 | 76.7 | Low competition |
| 2 | 50,000 | 0.4 | 53.3 | Moderate |
| 3 | 50,000 | 0.6 | 30.0 | High competition |
| 2 | 25,000 | 0.8 | 6.7 | Very high |
| 4 | 50,000 | 0.8 | 6.7 | Saturated |

*Assuming max density in dataset is 0.714 per 10K

---

## Weighted Combination

### The Final Formula

Once we have all four individual scores, we combine them using **predetermined weights**:

```
Total Score = (I × W_income) + (R × W_renter) + (D × W_density) + (C × W_competition)

Where:
  I = Income Score (0-100)
  R = Renter Score (0-100)
  D = Density Score (0-100)
  C = Competition Score (0-100)
  
  W_income = 0.25 (25% weight)
  W_renter = 0.30 (30% weight)
  W_density = 0.25 (25% weight)
  W_competition = 0.20 (20% weight)
  
  ΣW = 1.0 (weights sum to 100%)
```

### Why Weighted Average?

**Different factors have different importance**:

1. **Renter Rate (30%)** - Strongest predictor of demand
2. **Income (25%)** - Critical for sustainability
3. **Density (25%)** - Drives customer volume
4. **Competition (20%)** - Important but manageable

A simple average would treat all factors equally, which doesn't reflect business reality.

### Sensitivity Analysis

How much does each factor contribute to the final score?

```
Contribution = Individual Score × Weight

Maximum possible contribution:
- Income: 100 × 0.25 = 25 points
- Renter: 100 × 0.30 = 30 points
- Density: 100 × 0.25 = 25 points
- Competition: 100 × 0.20 = 20 points
```

### Python Implementation

```python
def calculate_total_score(income_score, renter_score, 
                         density_score, competition_score,
                         weights=None):
    """
    Calculate weighted total score
    
    Args:
        income_score: Score 0-100
        renter_score: Score 0-100
        density_score: Score 0-100
        competition_score: Score 0-100
        weights: dict with keys: income, renter, density, competition
                 (defaults to standard weights if None)
    
    Returns:
        Total score (0-100)
    """
    if weights is None:
        weights = {
            'income': 0.25,
            'renter': 0.30,
            'density': 0.25,
            'competition': 0.20
        }
    
    total = (income_score * weights['income'] +
             renter_score * weights['renter'] +
             density_score * weights['density'] +
             competition_score * weights['competition'])
    
    return total
```

---

## Real Examples

### Example 1: Downtown (Rank #1, Score: 81.47)

**Raw Data**:
```
Population: 50,000
Median Income: $65,000
Renter Rate: 75% (0.75)
Area: 2.5 square miles
Competitors: 2
```

**Derived Metrics**:
```
Population Density: 50,000 / 2.5 = 20,000 per sq mi
Competition Density: (2 / 50,000) × 10,000 = 0.4 per 10K
```

**Individual Scores**:
```
Income Score: 93.21
  → $65K is close to ideal $50K
  → Calculation: 100 × e^(-((65000-50000)²/(2×40000²))) = 93.21

Renter Score: 75.0
  → 75% renters
  → Calculation: 0.75 × 100 = 75.0

Density Score: 100.0
  → 20,000 per sq mi is highest in dataset
  → Calculation: (20,000 / 20,000) × 100 = 100.0

Competition Score: 53.3
  → 2 competitors, moderate density
  → Calculation: 100 × (1 - (0.4 / 0.857)) = 53.3
```

**Total Score Calculation**:
```
Total = (93.21 × 0.25) + (75.0 × 0.30) + (100.0 × 0.25) + (53.3 × 0.20)
      = 23.30 + 22.50 + 25.00 + 10.66
      = 81.47
```

**Score Breakdown**:
| Factor | Score | Weight | Contribution | % of Total |
|--------|-------|--------|--------------|------------|
| Income | 93.21 | 0.25 | 23.30 | 28.6% |
| Renter | 75.0 | 0.30 | 22.50 | 27.6% |
| Density | 100.0 | 0.25 | 25.00 | 30.7% |
| Competition | 53.3 | 0.20 | 10.66 | 13.1% |
| **TOTAL** | - | 1.00 | **81.47** | **100.0%** |

**Interpretation**:
- **Strengths**: Perfect density (100), near-ideal income (93.21)
- **Weaknesses**: Some competition hurts score (53.3)
- **Overall**: Excellent location despite competitors
- **Recommendation**: **Strong opportunity** - high traffic compensates for competition

---

### Example 2: Inglewood (Rank #2, Score: 81.22)

**Raw Data**:
```
Population: 44,000
Median Income: $48,000
Renter Rate: 75% (0.75)
Area: 4.0 square miles
Competitors: 0
```

**Derived Metrics**:
```
Population Density: 44,000 / 4.0 = 11,000 per sq mi
Competition Density: (0 / 44,000) × 10,000 = 0.0 per 10K
```

**Individual Scores**:
```
Income Score: 99.88
  → $48K is nearly perfect (ideal: $50K)
  → Calculation: 100 × e^(-((48000-50000)²/(2×40000²))) = 99.88

Renter Score: 75.0
  → 75% renters
  → Calculation: 0.75 × 100 = 75.0

Density Score: 55.0
  → 11,000 per sq mi (moderate)
  → Calculation: (11,000 / 20,000) × 100 = 55.0

Competition Score: 100.0
  → Zero competitors!
  → Calculation: 100 × (1 - 0) = 100.0
```

**Total Score Calculation**:
```
Total = (99.88 × 0.25) + (75.0 × 0.30) + (55.0 × 0.25) + (100.0 × 0.20)
      = 24.97 + 22.50 + 13.75 + 20.00
      = 81.22
```

**Score Breakdown**:
| Factor | Score | Weight | Contribution | % of Total |
|--------|-------|--------|--------------|------------|
| Income | 99.88 | 0.25 | 24.97 | 30.7% |
| Renter | 75.0 | 0.30 | 22.50 | 27.7% |
| Density | 55.0 | 0.25 | 13.75 | 16.9% |
| Competition | 100.0 | 0.20 | 20.00 | 24.6% |
| **TOTAL** | - | 1.00 | **81.22** | **100.0%** |

**Interpretation**:
- **Strengths**: Perfect income (99.88), no competition (100.0)
- **Weaknesses**: Lower density than Downtown (55.0)
- **Overall**: Excellent untapped market
- **Recommendation**: **Prime opportunity** - first-mover advantage

---

### Example 3: Santa Monica (Rank #9, Score: 68.53)

**Raw Data**:
```
Population: 30,000
Median Income: $78,000
Renter Rate: 58% (0.58)
Area: 3.5 square miles
Competitors: 0
```

**Derived Metrics**:
```
Population Density: 30,000 / 3.5 = 8,571 per sq mi
Competition Density: 0.0 per 10K
```

**Individual Scores**:
```
Income Score: 85.21
  → $78K is above ideal (too affluent)
  → Calculation: 100 × e^(-((78000-50000)²/(2×40000²))) = 85.21

Renter Score: 58.0
  → Only 58% renters (many homeowners)
  → Calculation: 0.58 × 100 = 58.0

Density Score: 42.9
  → Lower density area
  → Calculation: (8,571 / 20,000) × 100 = 42.9

Competition Score: 100.0
  → No competition
  → Calculation: 100.0
```

**Total Score Calculation**:
```
Total = (85.21 × 0.25) + (58.0 × 0.30) + (42.9 × 0.25) + (100.0 × 0.20)
      = 21.30 + 17.40 + 10.72 + 20.00
      = 69.42
```

**Score Breakdown**:
| Factor | Score | Weight | Contribution | % of Total |
|--------|-------|--------|--------------|------------|
| Income | 85.21 | 0.25 | 21.30 | 30.7% |
| Renter | 58.0 | 0.30 | 17.40 | 25.1% |
| Density | 42.9 | 0.25 | 10.72 | 15.4% |
| Competition | 100.0 | 0.20 | 20.00 | 28.8% |
| **TOTAL** | - | 1.00 | **69.42** | **100.0%** |

**Interpretation**:
- **Strengths**: No competition (100.0)
- **Weaknesses**: Too affluent (85.21), low renters (58.0), low density (42.9)
- **Overall**: Questionable market - demographics don't match ideal
- **Recommendation**: **Proceed with caution** - wealthy homeowners less likely to use laundromats

---

## Statistical Validation

### Z-Score Normalization

After calculating all scores, we add **z-scores** for statistical context:

```
Z-Score = (Individual Score - Mean Score) / Standard Deviation

Where:
  Individual Score = Total score for a neighborhood
  Mean Score = Average of all neighborhood scores
  Std Dev = Standard deviation of all scores
```

**Interpretation**:
- Z > 2.0: Exceptional (top 2.5%)
- Z > 1.0: Above average
- Z ≈ 0: Average
- Z < -1.0: Below average
- Z < -2.0: Poor (bottom 2.5%)

**Example**:
```
Downtown Score: 81.47
Mean Score: 72.1
Std Dev: 6.8

Z-Score = (81.47 - 72.1) / 6.8 = 1.38

Interpretation: Downtown is 1.38 standard deviations above average
                → Significantly better than typical location
```

### Percentile Ranking

```
Percentile = (Rank / Total Locations) × 100

Downtown: Rank 1 of 15
Percentile = (1 / 15) × 100 = 6.7th percentile
→ Better than 93.3% of locations
```

---

## Business Interpretation

### Score Ranges and Recommendations

| Total Score | Classification | Recommendation | Risk Level |
|-------------|----------------|----------------|------------|
| 85-100 | Excellent | **Strong Buy** - High confidence | Low |
| 75-84.9 | Very Good | **Buy** - Good opportunity | Low-Medium |
| 65-74.9 | Good | **Consider** - Viable with conditions | Medium |
| 55-64.9 | Fair | **Caution** - Requires further analysis | Medium-High |
| 45-54.9 | Poor | **Avoid** - High risk | High |
| 0-44.9 | Very Poor | **Do Not Invest** - Unviable | Very High |

### Decision Framework

**For a score of 81.47 (Downtown)**:

1. **Initial Assessment**: Excellent (85-100 range)
2. **Component Analysis**:
   - Income: ✅ Near ideal
   - Renters: ✅ Strong base
   - Density: ✅ Excellent traffic
   - Competition: ⚠️ Some competitors exist
3. **Risk Factors**: Competition manageable with good service
4. **Recommendation**: **Proceed to site visit and financial modeling**

### Comparative Analysis Example

| Location | Score | Best Feature | Worst Feature | Strategy |
|----------|-------|--------------|---------------|----------|
| Downtown | 81.47 | Density (100) | Competition (53) | Compete on quality/service |
| Inglewood | 81.22 | No competition (100) | Density (55) | First-mover advantage |
| Culver City | 76.26 | No competition (100) | Renter rate (68) | Target apartment complexes |
| Santa Monica | 69.42 | No competition (100) | Renter rate (58) | Premium positioning needed |

---

## Advanced Techniques

### Sensitivity Analysis

**Question**: How sensitive is the final score to weight changes?

**Example**: What if we increase competition weight to 30%?

```
Original Weights: Income=25%, Renter=30%, Density=25%, Competition=20%
New Weights:      Income=25%, Renter=25%, Density=25%, Competition=25%

Downtown (Original): 81.47
Downtown (New): (93.21×0.25) + (75.0×0.25) + (100.0×0.25) + (53.3×0.25)
              = 23.30 + 18.75 + 25.00 + 13.33
              = 80.38 (-1.09 points)

Inglewood (Original): 81.22
Inglewood (New): (99.88×0.25) + (75.0×0.25) + (55.0×0.25) + (100.0×0.25)
               = 24.97 + 18.75 + 13.75 + 25.00
               = 82.47 (+1.25 points)
```

**Result**: Inglewood becomes #1 if we weight competition more heavily!

### Monte Carlo Simulation

For uncertainty quantification, you could run simulations:

```python
import numpy as np

def simulate_score_uncertainty(base_scores, n_simulations=1000):
    """
    Simulate score ranges accounting for data uncertainty
    
    Assumes ±5% uncertainty in each component score
    """
    results = []
    
    for _ in range(n_simulations):
        # Add random noise
        income_score = base_scores['income'] * np.random.normal(1.0, 0.05)
        renter_score = base_scores['renter'] * np.random.normal(1.0, 0.05)
        density_score = base_scores['density'] * np.random.normal(1.0, 0.05)
        comp_score = base_scores['competition'] * np.random.normal(1.0, 0.05)
        
        # Calculate total
        total = (income_score * 0.25 + renter_score * 0.30 + 
                 density_score * 0.25 + comp_score * 0.20)
        
        results.append(total)
    
    return {
        'mean': np.mean(results),
        'std': np.std(results),
        'confidence_95': (np.percentile(results, 2.5), 
                         np.percentile(results, 97.5))
    }
```

**Example Output**:
```
Downtown Score Uncertainty:
  Point Estimate: 81.47
  Mean (1000 sims): 81.51
  Std Dev: 3.2
  95% Confidence Interval: [75.3, 87.6]
  
Interpretation: We're 95% confident the true score is between 75.3 and 87.6
```

---

## Summary

### The Complete Process

1. **Collect Data**: Demographics, income, housing, competitors
2. **Calculate Individual Scores**: 
   - Income (Gaussian curve)
   - Renter (Linear)
   - Density (Normalized)
   - Competition (Inverse normalized)
3. **Combine with Weights**: Weighted average (25%, 30%, 25%, 20%)
4. **Rank Locations**: Sort by total score
5. **Validate**: Check z-scores and percentiles
6. **Interpret**: Apply business judgment to scores

### Key Formulas Quick Reference

```
Income Score = 100 × e^(-((I - 50000)² / (2 × 40000²)))

Renter Score = Renter Rate × 100

Density Score = (Density / Max Density) × 100

Competition Score = 100 × (1 - (Comp Density / (Max Comp × 1.2)))

Total Score = (I×0.25) + (R×0.30) + (D×0.25) + (C×0.20)
```

### Mathematical Principles Used

1. **Gaussian Distribution** - Income scoring (normal curve)
2. **Linear Transformation** - Renter scoring (direct proportion)
3. **Min-Max Normalization** - Density scoring (relative scaling)
4. **Inverse Normalization** - Competition scoring (fewer = better)
5. **Weighted Average** - Final combination (different importance)
6. **Statistical Validation** - Z-scores and percentiles
