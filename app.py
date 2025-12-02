import streamlit as st
import os
from dotenv import load_dotenv
from sustainable_planner import create_sustainable_life_plan

load_dotenv()

# Page config
st.set_page_config(
    page_title="🌱 Sustainable Life Planner",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: transparent;
    }
    div[data-testid="stForm"] {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .agent-box {
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .agent-active {
        background: #e8f5e9;
        border-left-color: #4caf50;
    }
    .agent-complete {
        background: #e3f2fd;
        border-left-color: #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; color: white;'>🌱 Sustainable Life Planner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; font-size: 1.2em;'>AI-Powered Multi-Agent System for Sustainable Living</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Your Profile")
    
    with st.form("profile_form"):
        transportation = st.text_input(
            "🚗 Transportation",
            value="gasoline car, 20 km daily commute",
            placeholder="e.g., gasoline car, 20 km daily commute"
        )
        
        diet = st.text_input(
            "🍽️ Diet",
            value="meat-eating, occasional fast food",
            placeholder="e.g., meat-eating, occasional fast food"
        )
        
        energy_usage = st.text_input(
            "⚡ Energy Usage",
            value="standard home, no solar, AC usage high",
            placeholder="e.g., standard home, no solar, AC usage high"
        )
        
        goals = st.text_area(
            "🎯 Goals",
            value="reduce carbon footprint by 30% in 6 months",
            placeholder="e.g., reduce carbon footprint by 30% in 6 months"
        )
        
        submit = st.form_submit_button("🚀 Generate My Sustainable Plan", use_container_width=True)

with col2:
    st.markdown("### 🤖 AI Agents Working")
    
    agent1 = st.empty()
    agent2 = st.empty()
    agent3 = st.empty()
    agent4 = st.empty()
    
    agent1.markdown("""
    <div class="agent-box">
        <strong>📚 Agent 1: Knowledge Expert</strong><br>
        <small>Retrieving sustainability data (RAG)</small>
    </div>
    """, unsafe_allow_html=True)
    
    agent2.markdown("""
    <div class="agent-box">
        <strong>📊 Agent 2: Carbon Analyzer</strong><br>
        <small>Calculating your carbon footprint</small>
    </div>
    """, unsafe_allow_html=True)
    
    agent3.markdown("""
    <div class="agent-box">
        <strong>📅 Agent 3: Habit Coach</strong><br>
        <small>Creating weekly sustainable routine</small>
    </div>
    """, unsafe_allow_html=True)
    
    agent4.markdown("""
    <div class="agent-box">
        <strong>💡 Agent 4: Recommendation Engine</strong><br>
        <small>Generating personalized recommendations</small>
    </div>
    """, unsafe_allow_html=True)

# Process form submission
if submit:
    if not os.getenv('OPENAI_API_KEY'):
        st.error("⚠️ Please set OPENAI_API_KEY in .env file")
    else:
        user_profile = {
            'transportation': transportation,
            'diet': diet,
            'energy_usage': energy_usage,
            'goals': goals
        }
        
        # Show agent progress
        with col2:
            agent1.markdown("""
            <div class="agent-box agent-active">
                <strong>📚 Agent 1: Knowledge Expert</strong><br>
                <small>🔄 Working...</small>
            </div>
            """, unsafe_allow_html=True)
        
        with st.spinner("🤖 AI Agents are analyzing your profile..."):
            try:
                result = create_sustainable_life_plan(user_profile)
                
                # Mark all agents complete
                with col2:
                    agent1.markdown("""
                    <div class="agent-box agent-complete">
                        <strong>📚 Agent 1: Knowledge Expert</strong><br>
                        <small>✅ Complete</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    agent2.markdown("""
                    <div class="agent-box agent-complete">
                        <strong>📊 Agent 2: Carbon Analyzer</strong><br>
                        <small>✅ Complete</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    agent3.markdown("""
                    <div class="agent-box agent-complete">
                        <strong>📅 Agent 3: Habit Coach</strong><br>
                        <small>✅ Complete</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    agent4.markdown("""
                    <div class="agent-box agent-complete">
                        <strong>💡 Agent 4: Recommendation Engine</strong><br>
                        <small>✅ Complete</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display results
                st.markdown("---")
                st.markdown("## 📋 Your Sustainable Life Plan")
                st.success("✅ Plan generated successfully!")
                st.text_area("Results", value=str(result), height=400)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure your OpenAI API key is set correctly in .env file")

