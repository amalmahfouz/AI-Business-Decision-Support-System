import json
import re
from datetime import datetime


DEPARTMENT_BUDGETS = {
    "IT": 5000.0,
    "Marketing": 3000.0,
    "HR": 1500.0,
    "Sales": 1500.0,
    "Operations": 1500.0
}

RESTRICTED_KEYWORDS = [
    "gaming", "game", "playstation", "xbox", "nintendo", 
    "netflix", "spotify", "gift card", "personal subscription","اللعب","الترفيه"
]

def clean_json_response(response_str: str) -> dict:
    if not response_str:
        return {}
    
    cleaned = re.sub(r"```(?:json)?", "", response_str, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "").strip()
    
    try:
        return json.loads(cleaned)
    except Exception as e:
        print(f"failed while analysis JSON: {e}")
        return {
            "action": "flag_policy_issue",
            "status_label": "Policy Violation Flagged",
            "summary": "error with policy analysis  .",
            "passed_checks": [],
            "violations": [" error with ai analysis ."],
            "required_approvers": ["Finance"],
            "recommendation": "Error in the system."
        }

def evaluate_deterministic_rules(department: str, item_name: str, cost: float, justification: str) -> dict:
   
    passed_checks = []
    violations = []
    
    if cost <= 0:
        violations.append(" cost should be more than  zero.")
    else:
        passed_checks.append(" Cost is positive.")
        
    
    max_budget = DEPARTMENT_BUDGETS.get(department, 1500.0)
    if cost > max_budget:
        violations.append(f" cost needed (${cost:,.2f})  و  it exceeded exceeded the maximum limit allowed for the section {department} ,which (${max_budget:,.2f}).")
    else:
        passed_checks.append(f"Cost within the allowed budget for the department{department} (${max_budget:,.2f}).")
        
  
    item_lower = item_name.lower()
    for kw in RESTRICTED_KEYWORDS:
        if kw in item_lower:
            violations.append(f" The requested item contains a prohibited element under the financial policy ('{kw}').")
            break
    else:
        passed_checks.append("The requested item is not included in the prohibited list. .")
        
  
    if not justification or len(justification.strip()) < 10:
        violations.append("The business justification is incomplete or less than 10 characters long.")
    else:
        passed_checks.append("The business justification is complete.")

 
    required_approvers = []
    if cost < 500:
        required_approvers.append("Line Manager")
    elif cost <= max_budget:
        required_approvers.extend(["Department Head", "Finance"])
    else:
        required_approvers.extend(["Department Head", "Finance", "Executive Board Exception"])

    return {
        "is_valid": len(violations) == 0,
        "max_department_budget": max_budget,
        "passed_checks": passed_checks,
        "violations": violations,
        "required_approvers": required_approvers
    }

def generate_request_id(existing_requests: list) -> str:
    base_number = 1001
    if not existing_requests:
        return f"PR-{base_number}"
        
    existing_ids = []
    for req in existing_requests:
        rid = req.get("request_id", "")
        if rid.startswith("PR-"):
            try:
                num = int(rid.split("-")[1])
                existing_ids.append(num)
            except ValueError:
                pass
                
    if existing_ids:
        next_number = max(existing_ids) + 1
    else:
        next_number = base_number + len(existing_requests)
        
    return f"PR-{next_number}"

def create_procurement_record(request_id: str,requester_name: str,department: str,item_name: str,
    cost: float,justification: str,agent_eval: dict) -> dict:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "request_id": request_id,
        "created_at": now_str,
        "requester_name": requester_name if requester_name else "Anonymous",
        "department": department,
        "item_name": item_name,
        "cost": cost,
        "justification": justification,
        "action": agent_eval.get("action", "send_for_review"),
        "status_label": agent_eval.get("status_label", "Pending Human Approval"),
        "summary": agent_eval.get("summary", ""),
        "passed_checks": agent_eval.get("passed_checks", []),
        "violations": agent_eval.get("violations", []),
        "required_approvers": agent_eval.get("required_approvers", []),
        "recommendation": agent_eval.get("recommendation", ""),
        "decision": "Pending Review"  
    }

def calculate_procurement_metrics(requests: list) -> dict:
    total = len(requests)
    pending_info = sum(1 for r in requests if r.get("action") == "ask_for_info")
    policy_issues = sum(1 for r in requests if r.get("action") == "flag_policy_issue")
    pending_approval = sum(1 for r in requests if r.get("decision") == "Pending Review" and r.get("action") == "send_for_review")
    approved = sum(1 for r in requests if r.get("decision") == "Approved")
    rejected = sum(1 for r in requests if r.get("decision") == "Rejected")
    
    return {
        "total": total,
        "pending_info": pending_info,
        "policy_issues": policy_issues,
        "pending_approval": pending_approval,
        "approved": approved,
        "rejected": rejected
    }