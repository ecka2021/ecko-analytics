#!/usr/bin/env python3
"""
Market Analysis with ZIP-Level Data (SCALABLE VERSION)
Works for any city - no hardcoded neighborhoods
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """Analyzes laundromat market opportunities using ZIP-level data"""
    
    def __init__(self, data_dir=Path('data'), output_dir=Path('outputs')):
        self.demographics = None
        self.analysis = None
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        
    def load_data(self) -> None:
        """Load ZIP-level demographics"""
        logger.info("Loading ZIP-level demographics...")
        
        demographics_file = self.data_dir / 'zip_demographics.csv'
        
        if not demographics_file.exists():
            raise FileNotFoundError(
                "ZIP demographics not found. Run create_zip_demographics.py first!"
            )
        
        self.demographics = pd.read_csv(demographics_file)
        
        logger.info(f"✓ Loaded demographics for {len(self.demographics)} ZIP codes")
        logger.info(f"  Total population: {self.demographics['population'].sum():,.0f}")
        logger.info(f"  Total competitors: {int(self.demographics['competitor_count'].sum())}")
        
    def calculate_scores(self) -> pd.DataFrame:
        """Calculate opportunity scores for each ZIP code"""
        logger.info("Calculating opportunity scores...")
        
        analysis = self.demographics.copy()
        
        # Income Score (0-100): Gaussian centered at $50k
        target_income = 50000
        income_std = 25000
        analysis['income_score'] = 100 * np.exp(
            -((analysis['median_income'] - target_income) ** 2) / (2 * income_std ** 2)
        )
        
        # Renter Score (0-100): Higher is better
        analysis['renter_score'] = analysis['renter_rate'] * 100
        
        # Density Score (0-100): Normalized population density
        max_density = analysis['population_density'].max()
        analysis['density_score'] = (analysis['population_density'] / max_density) * 100
        
        # Competition Score (0-100): Inverse of competition density
        analysis['competition_density'] = (
            analysis['competitor_count'] / analysis['population']
        ) * 10000
        
        max_comp = analysis['competition_density'].max()
        if max_comp > 0:
            analysis['competition_score'] = 100 * (
                1 - (analysis['competition_density'] / max_comp)
            )
        else:
            analysis['competition_score'] = 100
        
        # Total Score: Weighted combination
        analysis['total_score'] = (
            analysis['income_score'] * 0.25 +
            analysis['renter_score'] * 0.30 +
            analysis['density_score'] * 0.25 +
            analysis['competition_score'] * 0.20
        )
        
        # Calculate z-scores and percentiles
        analysis['score_zscore'] = (
            (analysis['total_score'] - analysis['total_score'].mean()) /
            analysis['total_score'].std()
        )
        
        analysis['score_percentile'] = analysis['total_score'].rank(pct=True) * 100
        
        # Rank ZIP codes
        analysis = analysis.sort_values('total_score', ascending=False)
        analysis['rank'] = range(1, len(analysis) + 1)
        
        self.analysis = analysis
        
        logger.info(f"✓ Scoring complete. Top score: {analysis['total_score'].max():.1f}")
        
        return analysis
    
    def export_results(self) -> None:
        """Export analysis results"""
        logger.info("\nExporting results...")
        
        # Save full scored data
        scores_file = self.output_dir / 'zip_scores.csv'
        self.analysis.to_csv(scores_file, index=False)
        logger.info(f"✓ Saved scored data to {scores_file}")
        
        # Create insights JSON
        insights = {
            'analysis_date': pd.Timestamp.now().isoformat(),
            'total_zips': len(self.analysis),
            'underserved_markets': int((self.analysis['competitor_count'] < 3).sum()),
            'high_opportunity': int((self.analysis['total_score'] > 75).sum()),
            'avg_score': float(self.analysis['total_score'].mean()),
            'top_zips': self.analysis.nlargest(5, 'total_score')[[
                'zip_code', 'total_score', 'competitor_count', 'population'
            ]].to_dict('records')
        }
        
        import json
        insights_file = self.output_dir / 'analysis_insights.json'
        with open(insights_file, 'w') as f:
            json.dump(insights, f, indent=2)
        logger.info(f"✓ Saved insights to {insights_file}")
        
        # Create summary text
        summary_file = self.output_dir / 'analysis_summary.txt'
        with open(summary_file, 'w') as f:
            f.write("LAUNDROMAT MARKET ANALYSIS SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Based on ZIP-level census data\n\n")
            f.write(f"ZIP codes analyzed: {insights['total_zips']}\n")
            f.write(f"Underserved markets: {insights['underserved_markets']}\n")
            f.write(f"High-opportunity zones: {insights['high_opportunity']}\n")
            f.write(f"Avg score: {insights['avg_score']:.1f}\n")
        logger.info(f"✓ Saved summary to {summary_file}")
        

def main():
    """Main analysis workflow"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run market analysis')
    parser.add_argument('--data-dir', default='data', help='Input data directory')
    parser.add_argument('--output-dir', default='outputs', help='Output directory')
    args = parser.parse_args()
    
    from pathlib import Path
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Starting ZIP-level market analysis...")
    
    analyzer = MarketAnalyzer(data_dir=data_dir, output_dir=output_dir)
    
    # Load data
    analyzer.load_data()
    
    # Calculate scores
    logger.info("\nScoring ZIP codes...")
    results = analyzer.calculate_scores()
    
    # Display top results
    print("\n" + "=" * 60)
    print("TOP 5 ZIP CODES BY SCORE:")
    print("=" * 60)
    top5 = results.head(5)[['zip_code', 'total_score', 'competitor_count', 'population', 'rank']]
    print(top5.to_string(index=False))
    
    # Export
    analyzer.export_results()
    
    logger.info("\n" + "=" * 60)
    logger.info("ANALYSIS COMPLETE - All outputs saved")
    logger.info("=" * 60)
    
    # Print insights
    print("\n" + "=" * 60)
    print("KEY INSIGHTS:")
    print("=" * 60)
    print(f"ZIP codes analyzed: {len(results)}")
    print(f"Underserved markets: {(results['competitor_count'] < 3).sum()}")
    print(f"High-opportunity zones: {(results['total_score'] > 75).sum()}")
    print(f"Avg score: {results['total_score'].mean():.1f}")
    

if __name__ == "__main__":
    main()