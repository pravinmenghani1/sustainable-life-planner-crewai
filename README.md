# Sustainable Life Planner - AI Agent Demo

A prototype AI agent system for sustainable living planning, built with CrewAI for testing before migrating to Amazon Bedrock.

## Features

- **RAG Knowledge Base**: Grounded sustainability information
- **Carbon Footprint Analyzer**: Calculate emissions from daily activities
- **Habit Tracker**: Personalized weekly sustainable routines
- **Eco-Friendly Recommendations**: Actionable suggestions based on user profile
- **Web UI**: Interactive browser-based interface

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...
```

### 3. Run the Demo

**Option A: Command Line**
```bash
python sustainable_planner.py
```

**Option B: Web Interface (Streamlit)**
```bash
streamlit run app.py
# Opens automatically in browser at http://localhost:8501
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed explanation of how the system works.

View [architecture_diagram.svg](architecture_diagram.svg) for visual representation.

### CrewAI Version (Current)
- **4 Specialized Agents**:
  1. Sustainability Knowledge Expert (with RAG)
  2. Carbon Footprint Analyzer
  3. Sustainable Habit Coach
  4. Eco-Friendly Advisor
- **Sequential Task Processing**
- **File-based Knowledge Base**
- **Web UI with real-time agent status**

### How It Works

```
User Input → CrewAI Orchestrator → Agent 1 (RAG) → Agent 2 (Calculate) 
→ Agent 3 (Plan) → Agent 4 (Recommend) → Final Plan
```

Each agent:
1. Receives a specific task
2. Uses tools (Agent 1) or LLM reasoning (Agents 2-4)
3. Passes context to the next agent
4. Contributes to the final output

### Future: Amazon Bedrock Migration

This prototype validates the workflow. Migration path:

| CrewAI Component | Amazon Bedrock Equivalent |
|------------------|---------------------------|
| CrewAI Agents | Bedrock Agents |
| DirectoryReadTool/FileReadTool | Bedrock Knowledge Bases |
| OpenAI LLM | Bedrock Foundation Models (Claude, Titan) |
| Sequential Process | Agent Orchestration |

## Customization

Edit `sustainable_planner.py` to modify:
- User profile parameters
- Agent roles and goals
- Task descriptions
- Knowledge base content in `knowledge_base/`

## Testing Checklist

- [ ] RAG retrieval from knowledge base works
- [ ] Agents collaborate sequentially
- [ ] Carbon footprint calculations are accurate
- [ ] Weekly habits are actionable
- [ ] Recommendations are personalized
- [ ] Output is coherent and useful
- [ ] Web UI displays agent progress
- [ ] Results are formatted properly

Once validated, proceed with Bedrock implementation.

## Workshop Flow

1. **Introduction** (5 min): Agentic AI concepts
2. **Demo** (10 min): Run this CrewAI prototype (Web UI)
3. **Architecture** (10 min): Explain agent design with diagrams
4. **Bedrock Migration** (20 min): Live coding with Bedrock
5. **Hands-on** (15 min): Participants customize agents

## Project Structure

```
sustainablelifeplanner/
├── app.py                      # Flask web application
├── sustainable_planner.py      # Core agent system
├── requirements.txt            # Python dependencies
├── .env.example               # API key template
├── README.md                  # This file
├── ARCHITECTURE.md            # Detailed architecture docs
├── architecture_diagram.svg   # Visual architecture
├── knowledge_base/
│   └── sustainability_guide.txt  # RAG data source
└── templates/
    └── index.html             # Web UI
```

## Next Steps

After validating this prototype:
1. Set up AWS account and Bedrock access
2. Create Bedrock Knowledge Base with S3 bucket
3. Configure Bedrock Agents with action groups
4. Implement Lambda functions for calculations
5. Deploy and test Bedrock version
