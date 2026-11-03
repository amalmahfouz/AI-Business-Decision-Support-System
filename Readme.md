Decision Support System 

An intelligent procurement and policy decision support system built with Streamlit, Python, SQLite, and the Qwen3-Coder LLM. The system automatically evaluates employee purchase requests against corporate financial policies, enforces departmental budget limits, detects prohibited items, and routes requests for human approval.



 Key Features
1. Automated Policy Enforcement: Validates requests against explicit departmental budget limits 
     (IT: $5,000, Marketing: $3,000, HR/Sales/Operations: $1,500).

2. Prohibited Item Detection: Automatically flags restricted personal hardware, gaming equipment, or unauthorized entertainment subscriptions.

3. Missing Information Detection: Identifies incomplete justifications and requests missing context (ask_for_info).

4. SQLite Data Persistence: Permanently stores purchase requests, rule-engine evaluations, and manager approval decisions in a local SQLite database (procurement.db).


5. Human-In-The-Loop Approval Dashboard: Gives procurement managers dynamic status metrics and full decision control (Approved, Rejected, Deleted).

---

Architecture & Project Structure


AI Business Decision Support System/

.env                # API keys and environment variables
config.py           # Model settings and runtime parameters
prompts.py          # Structured JSON prompts for policy Company evaluation
llm.py              # OpenAI API client wrapper for Qwen3-Coder
database.py         # SQLite CRUD operations and persistence layer
helper.py           # Deterministic rule engine and metrics calculation
full_system.py      # Core agent orchestration logic
app.py              # Dual-tab Streamlit UI (Requester Portal + Manager Dashboard)
PROJECT_PLAN.md     # Design specification document
README.md           # Instructions and documentation


Setup & Execution Guide
1. Prerequisites
Python 3.8 or higher.
A valid Hugging Face / Novita API Key for LLM access.

2. Installation
Install the required dependencies:
pip install streamlit openai python-dotenv


3. Environment Configuration
Create a .env file in the root folder and add your API key:
HF_API_KEY=your_huggingface_api_key_here


4. Running the Application
Launch the Streamlit web server:
streamlit run app.py


Usage Workflow
Submit a New Purchase Request (Tab 1):
 - Requisitioners fill out the purchase form (Employee Name, Department, Item Name, Estimated Cost, Business Justification). 
 - The system performs deterministic rule checks and displays initial status evaluation.

Manager Review and Approval Dashboard (Tab 2):
 - Approvers review metric cards, filter orders, inspect AI policy recommendations, and render final human decisions (Approval Request or Rejected Request).