import sqlite3
import json

DB_NAME = "procurement.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                request_id TEXT PRIMARY KEY,
                created_at TEXT,
                requester_name TEXT,
                department TEXT,
                item_name TEXT,
                cost REAL,
                justification TEXT,
                action TEXT,
                status_label TEXT,
                summary TEXT,
                passed_checks TEXT,
                violations TEXT,
                required_approvers TEXT,
                recommendation TEXT,
                decision TEXT
            )
        ''')
        conn.commit()

def save_request_to_db(record: dict):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO requests (
                request_id, created_at, requester_name, department, item_name, 
                cost, justification, action, status_label, summary, 
                passed_checks, violations, required_approvers, recommendation, decision
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['request_id'],
            record['created_at'],
            record['requester_name'],
            record['department'],
            record['item_name'],
            record['cost'],
            record['justification'],
            record['action'],
            record['status_label'],
            record['summary'],
            json.dumps(record['passed_checks']),
            json.dumps(record['violations']),
            json.dumps(record['required_approvers']),
            record['recommendation'],
            record['decision']
        ))
        conn.commit()

def get_all_requests() -> list:
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests ORDER BY created_at ASC")
        rows = cursor.fetchall()
        
        requests_list = []
        for row in rows:
            req_dict = dict(row)
            req_dict['passed_checks'] = json.loads(req_dict['passed_checks']) if req_dict['passed_checks'] else []
            req_dict['violations'] = json.loads(req_dict['violations']) if req_dict['violations'] else []
            req_dict['required_approvers'] = json.loads(req_dict['required_approvers']) if req_dict['required_approvers'] else []
            requests_list.append(req_dict)
            
        return requests_list

def update_request_decision(request_id: str, new_decision: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE requests 
            SET decision = ?
            WHERE request_id = ?
        ''', (new_decision, request_id))
        conn.commit()

def delete_request_from_db(request_id: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM requests WHERE request_id = ?", (request_id,))
        conn.commit()