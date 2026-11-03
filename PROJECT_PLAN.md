AI Business Decision Support System (Procurement)

Project Name:
   - Smart Procurement Decision Support System (ProcureGuard AI)

Problem Statement: 
   - Companies spend significant administrative time manually checking employee procurement requests against internal finance policies. Manual checks lead to delays, inconsistent policy enforcement, and accidental approval of out-of-budget or non-compliant purchases.


Realistic Example:
    - An IT employee submits a request for a $3,500 specialized server monitor without specifying a business justification or checking if it exceeds the department's single-item threshold.


Target User:
    - Procurement Managers, Finance Approvers, and Department Heads.


Goal:
     - Automatically evaluate incoming purchase requests against a written corporate procurement policy, identify missing fields, flag rule violations, generate a structured recommendation, and route requests for human approval.



Scope
WILL DO:
  -  Provide a structured purchase request submission form with validation for negative costs and missing fields.

  - Evaluate requests against explicit written policy rules (department budgets, item restrictions, required approvals).

  - Classify requests into decision paths: "Ask for More Information", "Flag Policy Issue", or "Send for Human Review".

  - Display a detailed decision-support breakdown highlighting passed checks, missing fields, and specific policy violations.

  - Provide a Human Reviewer Dashboard where managers can inspect request history and render final 'Approved' or 'Rejected' decisions.


WILL NOT DO:
   - Automatically approve purchases or disburse funds without human review.
   - Handle employee training requests (focusing strictly on Procurement ).


Example Out-of-Scope Request:
  - Automatically charge the company credit card and buy 5 laptops from Amazon right now."



Input Contract

| Input Field | Required? | Type | Example Value | Handling Missing/Invalid Input |

Requester Name  Yes, String , "Amal Mahfouz" , Blocked if blank, prompts for user name. 

Department      Yes, Select , "IT" , Selection restricted to valid company departments (IT, Marketing, HR, Sales,Operations`). 

Equipment       Yes , String , "Development Laptop" , Blocked if blank or under 3 characters. 

Cost ($)        Yes , Float , 2400.00 , Rejects negative or zero values with an error message. 

Business Justification  Yes , String , "Required for AI software development" , If missing/blank, flags status as Pending Missing Info and prompts specifically for justification. 



Output Contract
  1. Structured Request Record with timestamp and Request ID (PR-1001).
  2. Policy Compliance Report listing passed checks and triggered violations.
  3. Decision Recommendation (Ask for Info, Flag Policy Issue, Send for Review).
  4. Actionable Approval Dashboard with buttons for human managers (Approve, Reject, Request Revision).

Sample Output :
  Request ID: PR-1001
  Requester: Amal Mahfouz (IT Dept)
  Item: Server Rack ($4,200)
  Policy Check Result:
    Mandatory fields present
    Valid non-negative cost
    Exceeds standard $3,000 threshold -> Requires Department Head + Finance Approval.
  System Recommendation: Send for Human Review (Requires Finance Approval)


Workflow
Requester Submits Form -> Validate Input Types & Ranges -> Extract Fields to Structured JSON -> Evaluate Rule Engine & LLM Agent.

  - Path A (Missing Input): Action: ask_for_info -> Status: Pending Missing Info -> Form remains prepopulated for easy user correction.

  - Path B (Policy Violation): Action: flag_policy_issue -> Status: Policy Violation Flagged -> Specific violated rule highlighted.

  - Path C (Compliant Request): Action: send_for_review -> Status: Pending Human Approval -> Routed to Approver Dashboard.



Agent Specification
Goal:
   - Evaluate procurement requests against company financial rules, enforce policy boundaries, and prepare decision summaries for human approvers.

Allowed Actions:
  - ask_for_info.  
  - flag_policy_issue.
  - send_for_review
  - finish.


Decision Rules:
  - If any mandatory field (Requester, Department, Item, Cost, Justification) is empty or cost <= 0 -> Trigger ask_for_info.

  - If requested item is a restricted personal item (e.g., gaming consoles, personal subscriptions) OR exceeds department max budget limit -> Trigger flag_policy_issue.

  - If all mandatory fields are valid and within policy limits -> Trigger send_for_review.

Permissions: Restricted to structured decision summaries; no autonomous purchase authorization permitted.



Company Procurement Policy (Rules)

Rule 1 (Department Spending Limits):
   IT: Max $5,000 per request.
   Marketing: Max $3,000 per request.
   HR / Sales / Operations: Max $1,500 per request.


Rule 2 (Approval Tier Requirements):
   Cost < $500: Line Manager Approval required.
   Cost $500 to Department Limit: Department Head + Finance Approval required.
   Cost > Department Limit: Triggers Policy Violation (Requires Executive Exception).


Rule 3 (Restricted Items):
  Gaming hardware, gift cards, personal entertainment subscriptions, and unapproved personal electronics are strictly prohibited.


Interface Sketch
Tab 1: Request Submission Portal
   Sidebar: Summary of written Company Procurement Policy.
   Form fields: Requester Name, Department, Item Name, Cost, Business Justification.
   Submit Button & Instant Evaluation Card showing passed/failed rules.

Tab 2: Manager Review Dashboard (Human-in-the-Loop)
  Status Metrics (Total Requests, Pending Info, Policy Issues, Pending Review, Approved, Rejected).
  Request History Table with detailed evaluation expanders.
  Action controls: Approve Request, Reject Request, Request Revision.

Success Tests
 T1 (Compliant Request): Valid request within budget is routed to human review -> send_for_review.

 T2 (Missing Information): Missing justification prompts specifically for missing details without clearing the form -> ask_for_info.

 T3 (Policy Violation): Request exceeding department budget highlights the specific rule violated -> flag_policy_issue.

 T4 (Boundary Test): Request exactly at the $3,000 limit follows correct tier approval rules.

 T5 (Invalid Data Handling): Negative cost value (-$500) is rejected by input validation.


Technology Plan

Known Concepts: Python, System Prompts, JSON Parsing, Rule-Based Validation.
Self-Learned Tools:
  Streamlit: Forms (st.form), Tabs (st.tabs), Status Badges, Session State (st.session_state).




