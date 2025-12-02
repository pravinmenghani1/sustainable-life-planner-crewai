import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import DirectoryReadTool, FileReadTool
from langchain_openai import ChatOpenAI

load_dotenv()

# Initialize tools for RAG
docs_tool = DirectoryReadTool(directory='./knowledge_base')
file_tool = FileReadTool()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Agent 1: Sustainability Knowledge Expert (RAG)
knowledge_agent = Agent(
    role='Sustainability Knowledge Expert',
    goal='Provide accurate information about sustainable living practices using the knowledge base',
    backstory='Expert in environmental science with access to comprehensive sustainability data',
    tools=[docs_tool, file_tool],
    llm=llm,
    verbose=True
)

# Agent 2: Carbon Footprint Analyzer
carbon_agent = Agent(
    role='Carbon Footprint Analyzer',
    goal='Calculate and analyze carbon footprint based on user activities',
    backstory='Environmental data scientist specializing in carbon emission calculations',
    llm=llm,
    verbose=True
)

# Agent 3: Habit Tracker & Routine Planner
habit_agent = Agent(
    role='Sustainable Habit Coach',
    goal='Create personalized sustainable habits and weekly routines',
    backstory='Behavioral psychologist focused on building sustainable lifestyle habits',
    llm=llm,
    verbose=True
)

# Agent 4: Eco-Friendly Recommendation Engine
recommendation_agent = Agent(
    role='Eco-Friendly Advisor',
    goal='Provide actionable eco-friendly recommendations tailored to user lifestyle',
    backstory='Sustainability consultant with expertise in practical green living solutions',
    llm=llm,
    verbose=True
)

def create_sustainable_life_plan(user_profile):
    """
    Main function to create a sustainable life plan
    user_profile: dict with keys like 'transportation', 'diet', 'energy_usage', 'goals'
    """
    
    # Task 1: Gather sustainability knowledge
    knowledge_task = Task(
        description=f"""Research and compile relevant sustainability information for:
        - Transportation: {user_profile.get('transportation', 'car')}
        - Diet: {user_profile.get('diet', 'mixed')}
        - Energy usage: {user_profile.get('energy_usage', 'standard')}
        Use the knowledge base to provide accurate data.""",
        agent=knowledge_agent,
        expected_output='Comprehensive sustainability information relevant to user profile'
    )
    
    # Task 2: Calculate carbon footprint
    carbon_task = Task(
        description=f"""Calculate the estimated annual carbon footprint based on:
        - Transportation: {user_profile.get('transportation', 'car')}
        - Diet: {user_profile.get('diet', 'mixed')}
        - Energy usage: {user_profile.get('energy_usage', 'standard')}
        Provide breakdown by category and total CO2 tons per year.""",
        agent=carbon_agent,
        expected_output='Detailed carbon footprint calculation with breakdown',
        context=[knowledge_task]
    )
    
    # Task 3: Create habit tracking plan
    habit_task = Task(
        description=f"""Design a weekly sustainable routine with daily habits to achieve:
        Goals: {user_profile.get('goals', 'reduce carbon footprint')}
        Include specific, measurable habits for each day of the week.""",
        agent=habit_agent,
        expected_output='7-day sustainable routine with daily actionable habits',
        context=[knowledge_task, carbon_task]
    )
    
    # Task 4: Generate recommendations
    recommendation_task = Task(
        description=f"""Provide top 5 personalized eco-friendly recommendations based on:
        - Current carbon footprint analysis
        - User goals: {user_profile.get('goals', 'reduce carbon footprint')}
        Prioritize high-impact, practical changes.""",
        agent=recommendation_agent,
        expected_output='Top 5 prioritized eco-friendly recommendations with expected impact',
        context=[knowledge_task, carbon_task, habit_task]
    )
    
    # Create crew
    crew = Crew(
        agents=[knowledge_agent, carbon_agent, habit_agent, recommendation_agent],
        tasks=[knowledge_task, carbon_task, habit_task, recommendation_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    # Example user profile
    user_profile = {
        'transportation': 'gasoline car, 20 km daily commute',
        'diet': 'meat-eating, occasional fast food',
        'energy_usage': 'standard home, no solar, AC usage high',
        'goals': 'reduce carbon footprint by 30% in 6 months'
    }
    
    print("🌱 Sustainable Life Planner - CrewAI Demo\n")
    print("=" * 60)
    print("User Profile:")
    for key, value in user_profile.items():
        print(f"  {key}: {value}")
    print("=" * 60)
    print("\n🤖 AI Agents are working on your sustainable life plan...\n")
    
    result = create_sustainable_life_plan(user_profile)
    
    print("\n" + "=" * 60)
    print("📋 YOUR SUSTAINABLE LIFE PLAN")
    print("=" * 60)
    print(result)
