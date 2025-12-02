# Sustainable Life Planner - Architecture Deep Dive

## Overview

This system uses **4 specialized AI agents** that work together sequentially to create a personalized sustainable living plan. Each agent has a specific role, tools, and outputs that feed into the next agent.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                                │
│  (Transportation, Diet, Energy Usage, Goals)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CREWAI ORCHESTRATOR                           │
│              (Sequential Task Processing)                        │
└─────────────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┬────────────────┐
        │                │                │                │
        ▼                ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   AGENT 1    │ │   AGENT 2    │ │   AGENT 3    │ │   AGENT 4    │
│  Knowledge   │ │   Carbon     │ │    Habit     │ │Recommenda-   │
│   Expert     │ │  Analyzer    │ │   Coach      │ │   tion       │
│              │ │              │ │              │ │   Engine     │
│  [RAG Tool]  │ │              │ │              │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │                │
       │    Context     │    Context     │    Context     │
       └────────────────┴────────────────┴────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FINAL OUTPUT                                   │
│  • Sustainability Facts                                          │
│  • Carbon Footprint Breakdown                                    │
│  • 7-Day Habit Plan                                              │
│  • Top 5 Recommendations                                         │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Workflow (Sequential Process)

```
START
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ AGENT 1: Sustainability Knowledge Expert                        │
│                                                                  │
│ Role: Research sustainability data from knowledge base          │
│ Tools: DirectoryReadTool, FileReadTool (RAG)                    │
│ Input: User profile (transportation, diet, energy)              │
│ Process:                                                         │
│   1. Reads knowledge_base/sustainability_guide.txt              │
│   2. Extracts relevant facts about user's lifestyle             │
│   3. Compiles baseline sustainability information               │
│ Output: Comprehensive sustainability facts                      │
└────────────────────────┬────────────────────────────────────────┘
                         │ Context passed to Agent 2
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ AGENT 2: Carbon Footprint Analyzer                              │
│                                                                  │
│ Role: Calculate CO2 emissions                                   │
│ Tools: None (uses LLM reasoning + Agent 1's data)               │
│ Input: User profile + Agent 1's sustainability facts            │
│ Process:                                                         │
│   1. Uses emission factors from knowledge base                  │
│   2. Calculates transportation emissions                        │
│   3. Calculates diet emissions                                  │
│   4. Calculates energy emissions                                │
│   5. Sums total annual CO2 (tons/year)                          │
│ Output: Carbon footprint breakdown by category                  │
└────────────────────────┬────────────────────────────────────────┘
                         │ Context passed to Agent 3
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ AGENT 3: Sustainable Habit Coach                                │
│                                                                  │
│ Role: Design weekly sustainable routine                         │
│ Tools: None (uses LLM reasoning)                                │
│ Input: User goals + Agent 1 & 2's outputs                       │
│ Process:                                                         │
│   1. Analyzes user's current footprint                          │
│   2. Identifies high-impact behavior changes                    │
│   3. Creates 7-day habit plan (Monday-Sunday)                   │
│   4. Ensures habits are specific and measurable                 │
│ Output: Weekly routine with daily actionable habits             │
└────────────────────────┬────────────────────────────────────────┘
                         │ Context passed to Agent 4
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ AGENT 4: Eco-Friendly Recommendation Engine                     │
│                                                                  │
│ Role: Provide prioritized recommendations                       │
│ Tools: None (uses LLM reasoning)                                │
│ Input: All previous agents' outputs                             │
│ Process:                                                         │
│   1. Reviews carbon footprint analysis                          │
│   2. Considers user's stated goals                              │
│   3. Prioritizes high-impact, practical changes                 │
│   4. Estimates CO2 reduction for each recommendation            │
│   5. Ranks top 5 recommendations                                │
│ Output: Top 5 eco-friendly recommendations with impact          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
                    FINAL PLAN
```

## How RAG (Retrieval Augmented Generation) Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAG WORKFLOW                                  │
└─────────────────────────────────────────────────────────────────┘

User Query: "Calculate carbon footprint for gasoline car commute"
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Agent 1 receives task                                   │
│ "Research sustainability information for gasoline car"          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: DirectoryReadTool scans knowledge_base/                 │
│ Finds: sustainability_guide.txt                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: FileReadTool reads sustainability_guide.txt             │
│ Extracts relevant sections:                                     │
│ "Gasoline car: 0.19 kg CO2 per km"                              │
│ "Transportation accounts for 29% of emissions"                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: LLM (GPT-4) processes retrieved data                    │
│ Combines knowledge base facts with reasoning                    │
│ Generates grounded, accurate response                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ OUTPUT: "Gasoline cars emit 0.19 kg CO2/km. For a 20km daily   │
│ commute, that's 3.8 kg/day or 1,387 kg (1.4 tons) per year."   │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components Explained

### 1. **CrewAI Framework**
- **Crew**: Orchestrates multiple agents
- **Agent**: Autonomous AI with specific role, goal, and tools
- **Task**: Specific job assigned to an agent
- **Process.sequential**: Agents execute one after another, passing context

### 2. **LLM (Large Language Model)**
- Uses OpenAI's GPT-4o-mini
- Provides reasoning and language generation
- Each agent has its own LLM instance

### 3. **Tools (RAG Implementation)**
- **DirectoryReadTool**: Scans folders for relevant files
- **FileReadTool**: Reads file contents
- Only Agent 1 has tools (knowledge retrieval)
- Other agents use pure LLM reasoning

### 4. **Context Passing**
```python
carbon_task = Task(
    description="Calculate carbon footprint...",
    agent=carbon_agent,
    context=[knowledge_task]  # ← Receives Agent 1's output
)
```

## Data Flow Example

**User Input:**
```python
{
    'transportation': 'gasoline car, 20 km daily commute',
    'diet': 'meat-eating, occasional fast food',
    'energy_usage': 'standard home, no solar, AC usage high',
    'goals': 'reduce carbon footprint by 30% in 6 months'
}
```

**Agent 1 Output:**
```
Transportation: Gasoline cars emit 0.19 kg CO2/km
Diet: Meat-eating diet produces 2.5 tons CO2/year
Energy: Standard home energy contributes 20% of footprint
```

**Agent 2 Output:**
```
Carbon Footprint Breakdown:
- Transportation: 1.4 tons CO2/year (20km × 0.19kg × 365 days)
- Diet: 2.5 tons CO2/year
- Energy: 2.0 tons CO2/year (estimated)
Total: 5.9 tons CO2/year
```

**Agent 3 Output:**
```
Weekly Habit Plan:
Monday: Carpool to work (save 50% transport emissions)
Tuesday: Meatless meal day
Wednesday: Reduce AC by 2°C
Thursday: Bike to work if possible
Friday: Meal prep with local produce
Saturday: Energy audit at home
Sunday: Plan next week's sustainable meals
```

**Agent 4 Output:**
```
Top 5 Recommendations:
1. Switch to hybrid/EV → Save 1.0 tons CO2/year
2. Reduce meat consumption 50% → Save 0.5 tons CO2/year
3. Install smart thermostat → Save 0.4 tons CO2/year
4. Carpool 3x/week → Save 0.3 tons CO2/year
5. Switch to renewable energy → Save 0.8 tons CO2/year
Total potential reduction: 3.0 tons (51% reduction)
```

## Migration to Amazon Bedrock

### Component Mapping

| CrewAI Component | Bedrock Equivalent | How It Works |
|------------------|-------------------|--------------|
| **CrewAI Agent** | **Bedrock Agent** | Managed agent service with built-in orchestration |
| **DirectoryReadTool/FileReadTool** | **Bedrock Knowledge Base** | S3 + Vector DB (OpenSearch) for RAG |
| **OpenAI GPT-4** | **Claude 3 / Titan** | Foundation models via Bedrock API |
| **Sequential Process** | **Agent Orchestration** | Built-in multi-agent coordination |
| **Task Context** | **Session State** | Maintains conversation context |
| **Python Functions** | **Lambda Action Groups** | Serverless functions for calculations |

### Bedrock Architecture (Future)

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BEDROCK AGENT                                  │
│              (Orchestrates all sub-agents)                       │
└─────────────────────────────────────────────────────────────────┘
         │                │                │                │
         ▼                ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Bedrock    │ │   Lambda     │ │   Lambda     │ │   Bedrock    │
│  Knowledge   │ │  Function    │ │  Function    │ │    Agent     │
│    Base      │ │  (Carbon     │ │  (Habit      │ │ (Recommend)  │
│              │ │   Calc)      │ │   Plan)      │ │              │
│  [S3 +       │ │              │ │              │ │              │
│   Vector DB] │ │              │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
         │                │                │                │
         └────────────────┴────────────────┴────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CLAUDE 3 / TITAN                               │
│              (Foundation Model via Bedrock)                      │
└─────────────────────────────────────────────────────────────────┘
```

## Why This Architecture?

1. **Separation of Concerns**: Each agent has one job
2. **Grounded AI**: RAG ensures factual accuracy
3. **Scalability**: Easy to add more agents
4. **Testability**: Can test each agent independently
5. **Context Awareness**: Agents build on previous outputs
6. **Cloud-Ready**: Direct path to AWS Bedrock
