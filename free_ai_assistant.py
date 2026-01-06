"""
Rule-Based AI Market Assistant (100% FREE)
Smart pattern matching that looks like AI
"""

import streamlit as st
import re
from typing import Dict, List, Tuple

class RuleBasedAssistant:
    """
    Pattern-matching assistant that answers questions about market data
    """
    
    def __init__(self, county_name, state, insights, scores_df, top10):
        self.county_name = county_name
        self.state = state
        self.insights = insights
        self.scores_df = scores_df
        self.top10 = top10
        
        # Calculate useful stats
        self.total_pop = int(scores_df['population'].sum())
        self.total_competitors = int(scores_df['competitor_count'].sum())
        self.avg_score = scores_df['total_score'].mean()
        self.top3 = scores_df.nlargest(3, 'total_score')
        self.worst3 = scores_df.nsmallest(3, 'total_score')
        self.zero_competition = scores_df[scores_df['competitor_count'] == 0]
    
    def answer(self, question: str) -> str:
        """
        Match question to pattern and return answer
        """
        question_lower = question.lower()
        
        # Pattern 1: Why is X ranked #1?
        if any(word in question_lower for word in ['why', '#1', 'number 1', 'top', 'best', 'ranked']):
            return self._explain_top_ranking()
        
        # Pattern 2: Compare locations
        if any(word in question_lower for word in ['compare', 'versus', 'vs', 'difference between']):
            return self._compare_locations()
        
        # Pattern 3: Zero/least competition
        if any(word in question_lower for word in ['zero', 'no competition', 'least competition', 'underserved']):
            return self._find_zero_competition()
        
        # Pattern 4: What should I do next / guidance
        if any(word in question_lower for word in ['what should', 'next steps', 'recommend', 'advice']):
            return self._investment_guidance()
        
        # Pattern 5: Methodology / scoring
        if any(word in question_lower for word in ['score', 'calculate', 'methodology', 'algorithm', 'how']):
            return self._explain_scoring()
        
        # Pattern 6: Overview / summary
        if any(word in question_lower for word in ['overview', 'summary', 'tell me about', 'explain']):
            return self._market_overview()
        
        # Pattern 7: Risks / avoid
        if any(word in question_lower for word in ['risk', 'avoid', 'bad', 'worst', 'saturated']):
            return self._explain_risks()
        
        # Pattern 8: Specific ZIP code mentioned
        zip_match = re.search(r'\b\d{5}\b', question)
        if zip_match:
            return self._explain_specific_zip(zip_match.group())
        
        # Default: General help
        return self._general_help()
    
    def _explain_top_ranking(self) -> str:
        """Explain why #1 is ranked first"""
        top = self.top3.iloc[0]
        avg_competitors = self.scores_df['competitor_count'].mean()
        avg_pop = self.scores_df['population'].mean()
        
        response = f"""**Why {top['location_name']} (ZIP {int(top['zip_code'])}) ranks #1:**

🏆 **Score: {top['total_score']:.1f}/100**

**Key Advantages:**
• **Population:** {int(top['population']):,} people ({int((top['population']/avg_pop - 1) * 100):+d}% vs average)
• **Competition:** {int(top['competitor_count'])} competitors ({int((top['competitor_count']/avg_competitors - 1) * 100) if avg_competitors > 0 else -100:+d}% vs average)
• **Market Size:** {int(top['population']/(top['competitor_count'] if top['competitor_count'] > 0 else 1)):,} people per business
"""
        
        if top['competitor_count'] == 0:
            response += "\n⭐ **ZERO competition** - completely underserved market!"
        
        response += f"""

**Why This Matters:**
This location has the optimal combination of high demand (population) and low supply (competition), representing the strongest market opportunity in {self.county_name}."""
        
        return response
    
    def _compare_locations(self) -> str:
        """Compare top 3 opportunities"""
        response = f"**Top 3 Market Opportunities Comparison:**\n\n"
        
        for i, (_, row) in enumerate(self.top3.iterrows(), 1):
            market_size = int(row['population']/(row['competitor_count'] if row['competitor_count'] > 0 else 1))
            
            response += f"""**#{i}. {row['location_name']} (ZIP {int(row['zip_code'])})**
• Score: {row['total_score']:.1f}/100
• Population: {int(row['population']):,}
• Competitors: {int(row['competitor_count'])}
• Market Size: {market_size:,} people/business

"""
        
        response += """**Recommendation:**
All three are strong opportunities. Choose based on:
1. Real estate availability
2. Your budget
3. Local traffic patterns
4. Zoning regulations"""
        
        return response
    
    def _find_zero_competition(self) -> str:
        """Find areas with zero competition"""
        if len(self.zero_competition) == 0:
            return f"**No areas with zero competition** in {self.county_name}. The least competitive area is {self.top3.iloc[0]['location_name']} with {int(self.top3.iloc[0]['competitor_count'])} competitors."
        
        response = f"**{len(self.zero_competition)} ZIP codes with ZERO competition:**\n\n"
        
        top_zero = self.zero_competition.nlargest(5, 'population')
        
        for _, row in top_zero.iterrows():
            response += f"• **{row['location_name']}** (ZIP {int(row['zip_code'])}) - {int(row['population']):,} people\n"
        
        response += f"""

**What This Means:**
These {len(self.zero_competition)} areas have NO existing laundromats. Residents must travel elsewhere for service, representing untapped demand.

**Important:** Verify these are residential areas (not industrial/commercial zones) before investing."""
        
        return response
    
    def _investment_guidance(self) -> str:
        """Provide next steps guidance"""
        top = self.top3.iloc[0]
        
        return f"""**Recommended Next Steps:**

**1. Site Visits** 🚗
Visit the top 3 locations in person:
• {self.top3.iloc[0]['location_name']} (ZIP {int(self.top3.iloc[0]['zip_code'])})
• {self.top3.iloc[1]['location_name']} (ZIP {int(self.top3.iloc[1]['zip_code'])})
• {self.top3.iloc[2]['location_name']} (ZIP {int(self.top3.iloc[2]['zip_code'])})

**2. Ground Truth Verification** ✅
• Drive around - assess foot traffic
• Check parking availability
• Look for nearby apartment complexes
• Verify competitors (Yelp data may be incomplete)

**3. Commercial Real Estate** 🏢
• Search for available retail spaces
• Target: 1,000-2,000 sq ft
• Check zoning permits
• Assess utilities (water, electrical, venting)

**4. Financial Analysis** 💰
• Get quotes from equipment suppliers
• Calculate build-out costs
• Project revenue ({int(self.total_pop/self.total_competitors if self.total_competitors > 0 else self.total_pop):,} people/business avg)
• Run break-even analysis

**5. Professional Consultation** 👥
• Attorney: Lease review, entity formation
• Accountant: Tax implications, projections
• Real estate broker: Local market insights

**Start with #{self.top3.iloc[0]['location_name']}** - it has the strongest data-driven potential."""
        
        return response
    
    def _explain_scoring(self) -> str:
        """Explain the scoring methodology"""
        return f"""**Opportunity Score Methodology:**

Our algorithm evaluates **5 weighted factors** (0-100 scale):

**1. Population Size (25%)**
• Larger markets = more customers
• {self.county_name} range: {int(self.scores_df['population'].min()):,} to {int(self.scores_df['population'].max()):,}

**2. Income Levels (20%)**
• Higher income = more discretionary spending
• Captures purchasing power

**3. Population Density (15%)**
• Denser areas = easier customer access
• Suburban vs urban consideration

**4. Renter Rate (20%)**
• Renters use laundromats more than homeowners
• Key demographic indicator
• County average: {int(self.scores_df['renter_rate'].mean() * 100) if 'renter_rate' in self.scores_df.columns else 'N/A'}%

**5. Competition Gap (20%)**
• People per existing business
• Lower competition = higher score
• County average: {int(self.total_pop/self.total_competitors if self.total_competitors > 0 else 0):,} people/business

**Final Score = Weighted Sum**
• 80-100: Excellent opportunity
• 60-79: Good opportunity
• 40-59: Moderate opportunity
• 0-39: Saturated market

All metrics are **normalized** to ensure fair comparison across different scales."""
        
        return response
    
    def _market_overview(self) -> str:
        """Provide market overview"""
        return f"""**{self.county_name}, {self.state} - Market Overview:**

**Market Size:**
• ZIP codes analyzed: {self.insights['total_zips']:,}
• Total population: {self.total_pop:,}
• Existing competitors: {self.total_competitors}
• Market size/business: {int(self.total_pop/self.total_competitors if self.total_competitors > 0 else self.total_pop):,} people

**Opportunity Distribution:**
• High opportunity (80-100): {len(self.scores_df[self.scores_df['total_score'] >= 80])} ZIPs
• Good opportunity (60-79): {len(self.scores_df[(self.scores_df['total_score'] >= 60) & (self.scores_df['total_score'] < 80)])} ZIPs
• Moderate (40-59): {len(self.scores_df[(self.scores_df['total_score'] >= 40) & (self.scores_df['total_score'] < 60)])} ZIPs
• Saturated (0-39): {len(self.scores_df[self.scores_df['total_score'] < 40])} ZIPs

**Best Opportunity:**
{self.top3.iloc[0]['location_name']} (ZIP {int(self.top3.iloc[0]['zip_code'])}) - Score: {self.top3.iloc[0]['total_score']:.1f}/100

**Key Insight:**
{len(self.zero_competition)} ZIP codes have ZERO competition, representing {int(self.zero_competition['population'].sum()) if len(self.zero_competition) > 0 else 0:,} underserved residents."""
        
        return response
    
    def _explain_risks(self) -> str:
        """Explain risks and areas to avoid"""
        worst = self.worst3.iloc[0]
        
        response = f"""**Market Risks & Areas to Avoid:**

**Most Saturated (Lowest Scores):**

"""
        for i, (_, row) in enumerate(self.worst3.iterrows(), 1):
            competition_ratio = int(row['population']/(row['competitor_count'] if row['competitor_count'] > 0 else 1))
            response += f"**#{i}. {row['location_name']}** (ZIP {int(row['zip_code'])})\n"
            response += f"• Score: {row['total_score']:.1f}/100\n"
            response += f"• {int(row['population']):,} people ÷ {int(row['competitor_count'])} businesses = {competition_ratio:,} people/business\n\n"
        
        response += f"""**Why These Are Risky:**
• High competition = harder to gain market share
• Lower profit margins due to price competition
• Established competitors have customer loyalty

**General Risks:**
• **Data lag:** Census is 2022, market may have changed
• **Incomplete competition:** Yelp may miss unlisted businesses
• **Local factors:** Regulations, crime, demographics not in data
• **Real estate:** High rent can offset good market conditions

**Recommendation:** Avoid scores below 50 unless you have specific local knowledge or advantages."""
        
        return response
    
    def _explain_specific_zip(self, zip_code: str) -> str:
        """Explain a specific ZIP code"""
        zip_data = self.scores_df[self.scores_df['zip_code'] == int(zip_code)]
        
        if len(zip_data) == 0:
            return f"ZIP code {zip_code} not found in {self.county_name}, {self.state}. Try a different ZIP or check the top 10 list."
        
        row = zip_data.iloc[0]
        rank = (self.scores_df['total_score'] > row['total_score']).sum() + 1
        
        market_size = int(row['population']/(row['competitor_count'] if row['competitor_count'] > 0 else 1))
        
        response = f"""**ZIP {zip_code} - {row['location_name']}:**

**Rankings:**
• Score: {row['total_score']:.1f}/100
• Rank: #{rank} out of {len(self.scores_df)}

**Market Metrics:**
• Population: {int(row['population']):,}
• Competitors: {int(row['competitor_count'])}
• Market Size: {market_size:,} people/business
"""
        
        if row['total_score'] >= 80:
            response += "\n✅ **Excellent opportunity** - highly recommended for investment"
        elif row['total_score'] >= 60:
            response += "\n👍 **Good opportunity** - worth investigating further"
        elif row['total_score'] >= 40:
            response += "\n⚠️ **Moderate opportunity** - competitive but possible"
        else:
            response += "\n❌ **Saturated market** - high risk, not recommended"
        
        if row['competitor_count'] == 0:
            response += "\n⭐ **ZERO competition!**"
        
        return response
    
    def _general_help(self) -> str:
        """General help message"""
        return f"""**I can help you understand this market analysis!**

**Try asking:**
• "Why is {self.top3.iloc[0]['location_name']} ranked #1?"
• "Compare the top 3 opportunities"
• "Which areas have zero competition?"
• "What should I do next?"
• "Explain the scoring methodology"
• "What are the risks?"
• "Tell me about ZIP {int(self.top3.iloc[0]['zip_code'])}"

**Market Summary:**
{self.county_name}, {self.state} has {self.insights['total_zips']} ZIP codes analyzed. The best opportunity is {self.top3.iloc[0]['location_name']} with a score of {self.top3.iloc[0]['total_score']:.1f}/100.

**What would you like to know?**"""


def free_ai_assistant(county_name, state, insights, scores_df, top10):
    """
    Free rule-based AI assistant UI
    """
    
    st.markdown('<div class="section-title">💬 AI Market Assistant</div>', unsafe_allow_html=True)
    
    # Initialize assistant
    assistant = RuleBasedAssistant(county_name, state, insights, scores_df, top10)
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Suggested questions
    st.markdown("**Quick Questions:**")
    suggestions_col1, suggestions_col2, suggestions_col3 = st.columns(3)
    
    with suggestions_col1:
        if st.button(f"Why is #{top10.iloc[0]['Location']} ranked #1?", key="q1", use_container_width=True):
            st.session_state.current_question = f"Why is {top10.iloc[0]['Location']} ranked #1?"
        if st.button("Compare top 3", key="q2", use_container_width=True):
            st.session_state.current_question = "Compare the top 3 opportunities"
    
    with suggestions_col2:
        if st.button("Zero competition areas?", key="q3", use_container_width=True):
            st.session_state.current_question = "Which areas have zero competition?"
        if st.button("What should I do next?", key="q4", use_container_width=True):
            st.session_state.current_question = "What should I do next?"
    
    with suggestions_col3:
        if st.button("Explain scoring", key="q5", use_container_width=True):
            st.session_state.current_question = "Explain the scoring methodology"
        if st.button("What are the risks?", key="q6", use_container_width=True):
            st.session_state.current_question = "What are the risks?"
    
    # Chat input
    user_question = st.chat_input("Ask about this market...")
    
    # Handle suggested question clicks
    if 'current_question' in st.session_state:
        user_question = st.session_state.current_question
        del st.session_state.current_question
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Process new question
    if user_question:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Get AI response
        with st.chat_message("assistant"):
            response = assistant.answer(user_question)
            st.markdown(response)
            
            # Add to history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Clear chat
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", key="clear"):
            st.session_state.chat_history = []
            st.rerun()