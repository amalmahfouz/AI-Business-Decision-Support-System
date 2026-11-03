from helper import (
    clean_json_response,
    create_procurement_record,
    evaluate_deterministic_rules,
    generate_request_id,
)
from llm import ask_llm
from prompts import build_procurement_policy_prompt

from database import save_request_to_db


def process_procurement_request(requester_name: str,department: str,item_name: str,cost: float,
    justification: str,existing_requests: list,) -> dict:
  if cost <= 0:
    return {
        "status": "error",
        "message": (
            "Sorry, the financial cost must be a positive number greater than zero."
        ),
    }

  if not item_name or len(item_name.strip()) < 3:
    return {
        "status": "error",
        "message": "Please clearly specify the name of the required item or device.",
    }

  rule_check = evaluate_deterministic_rules(
      department=department,
      item_name=item_name,
      cost=cost,
      justification=justification,
  )

  request_id = generate_request_id(existing_requests)

  system_prompt, user_prompt = build_procurement_policy_prompt(
      requester_name=requester_name,
      department=department,
      item_name=item_name,
      cost=cost,
      justification=justification,
      rule_check_results=rule_check,
  )

  raw_response = ask_llm(system_prompt, user_prompt)

  agent_eval = clean_json_response(raw_response)

  if rule_check["violations"] and agent_eval.get("action") == "send_for_review":
    agent_eval["action"] = "flag_policy_issue"
    agent_eval["status_label"] = "Policy Violation Flagged"

  record = create_procurement_record(
      request_id=request_id,
      requester_name=requester_name,
      department=department,
      item_name=item_name,
      cost=cost,
      justification=justification,
      agent_eval=agent_eval,
  )
  save_request_to_db(record)
  return {"status": "success", "record": record}