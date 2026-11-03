import streamlit as st
from helper import DEPARTMENT_BUDGETS, calculate_procurement_metrics
from full_system import process_procurement_request
import database as db 


db.init_db()

st.set_page_config(
    page_title="Decision Support System",
    layout="wide"
)

with st.sidebar:
    st.header("Approved Procurement Policy")
    st.caption("Permitted financial limits per request, by department:")
    for dept, budget in DEPARTMENT_BUDGETS.items():
        st.write(f"**{dept}:** {budget:,.0f}$")
        
    st.divider()
    st.markdown("Prohibited Items")
    st.caption("Gaming consoles, personal subscriptions, gift cards, and non-certified devices.")


st.title("Procurement and Policy Decision Support System ")
st.caption("An intelligent assistant evaluates purchase requests against the company's financial policies and routes them for human approval.")

# Tabs
tab_submit, tab_manager = st.tabs(["Submit a new purchase request", " Manager Review and Approval Dashboard | Human Approval"])


# Requester tab
with tab_submit:
    st.subheader("New Purchase Request Form")
    st.write("Please enter the details of the requested item so that it can be automatically checked against the approved company policy.")
    
    with st.form(key="procurement_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            req_name = st.text_input("Employee Name : *", placeholder="e.g. Amal Mahfouz ")
            item_name = st.text_input(" Name of the required device *", placeholder="e.g. msi Laptop for design")
        with col2:
            department = st.selectbox("The department :*", list(DEPARTMENT_BUDGETS.keys()))
            cost = st.number_input(" Estimated total cost $ *", min_value=0.0, step=50.0, value=250.0)
            
        justification = st.text_area("Business Justification*", placeholder="Write a clear justification for purchasing this item and explain how it supports the work...", height=100)
        
        submit_btn = st.form_submit_button(label="Review and evaluation of the application")
        
    if submit_btn:
        with st.spinner("The request is being checked against the rules engine and company policy..."):
            existing_requests_db = db.get_all_requests()
            
            result = process_procurement_request(
                requester_name=req_name,
                department=department,
                item_name=item_name,
                cost=cost,
                justification=justification,
                existing_requests=existing_requests_db
            )
            
            if result["status"] == "error":
                st.error(f" {result['message']}")
            else:
                record = result["record"]
                
                st.success(f"The application has been successfully registered and reviewed! Application number: **{record['request_id']}**")
                
                with st.expander("Application evaluation results and initial status", expanded=True):
                    st.write(f"**Evaluation Status:** {record['status_label']}")
                    st.write(f"**Summary:** {record['summary']}")
                    
                    if record['passed_checks']:
                        st.markdown("**Obligatory conditions:**")
                        for check in record['passed_checks']:
                            st.write(f"  - ✅ {check}")
                            
                    if record['violations']:
                        st.markdown("**Violations or deficiencies discovered:**")
                        for v in record['violations']:
                            st.write(f"  - ⚠️ {v}")


# Approval Dashboard tab2
with tab_manager:
    st.subheader("Manager's Dashboard and Decision Review")
    
    all_db_requests = db.get_all_requests()
    
    metrics = calculate_procurement_metrics(all_db_requests)
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    
    m1.metric("**Total Request**", metrics["total"])
    m2.metric("**Missing data**", metrics["pending_info"])
    m3.metric("**Policy Violations**", metrics["policy_issues"])
    m4.metric("**Pending approval**", metrics["pending_approval"])
    m5.metric("**Approved **", metrics["approved"])
    m6.metric("**Rejected **", metrics["rejected"])
    
    st.divider()
    
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        action_filter = st.selectbox("Filter by recommendation type:", ["All", "send_for_review", "flag_policy_issue", "ask_for_info"])
    with f_col2:
        decision_filter = st.selectbox("Filter by decision:", ["All", "Pending Review", "Approved", "Rejected"])
        
    filtered = all_db_requests
    if action_filter != "All":
        filtered = [r for r in filtered if r.get("action") == action_filter]
    if decision_filter != "All":
        filtered = [r for r in filtered if r.get("decision") == decision_filter]
        
    st.write(f"View **{len(filtered)}** Purchase Order :")
    
    if not filtered:
        st.info("No requests match the current filter options.")
    else:
        for idx, req in enumerate(reversed(filtered)):
            req_id = req["request_id"]
            
            
            with st.expander(f"{req_id} | decision: {req['decision']} | Purchase Requisitioner: {req['requester_name']} ({req['department']}) | Price: ${req['cost']:,.2f}"):
                c1, c2 = st.columns([1, 1])
                
                with c1:
                    st.markdown("### Details of the submitted request")
                    st.write(f"**Required material:** {req['item_name']}")
                    st.write(f"**Cost:** ${req['cost']:,.2f}")
                    st.write(f"**Justification:** \"{req['justification']}\"")
                    st.write(f"**Order Date:** {req['created_at']}")
                    st.write(f"**Approvals required under the policy:** {', '.join(req['required_approvers'])}")
                    
                with c2:
                    st.markdown("### AI Recommendation and Evaluation ")
                    st.info(f"**Recommendation:** {req['recommendation']}")
                    
                    if req['passed_checks']:
                        st.caption("✅ Successful tests:")
                        for p in req['passed_checks']:
                            st.caption(f"- {p}")
                            
                    if req['violations']:
                        st.error("⚠️ Resulting violations:")
                        for v in req['violations']:
                            st.write(f"- {v}")
                            
                    st.divider()
                    st.markdown("### The final human decision")
                    
                    b1, b2, b3 = st.columns(3)
                    with b1:
                        if st.button("Approval Request", key=f"app_{req_id}_{idx}"):
                            db.update_request_decision(req_id, "Approved") 
                            st.success("The request has been approved and financially authorized!")
                            st.rerun()
                    with b2:
                        if st.button("Rejected Request", key=f"rej_{req_id}_{idx}"):
                            db.update_request_decision(req_id, "Rejected") 
                            st.error("The request was rejected.")
                            st.rerun()
                    with b3:
                        if st.button("Delete", key=f"del_{req_id}_{idx}"):
                            db.delete_request_from_db(req_id)
                            st.success("The request has been deleted.")
                            st.rerun()