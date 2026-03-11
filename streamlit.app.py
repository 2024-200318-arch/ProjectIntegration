import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Pending Task Tracker", page_icon="📋", layout="wide")

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

st.title("My Pending Tracker")
st.caption("Keep track of all your pending school work and projects!")

t1, t2, t3, t4, t5 = st.tabs(["📊 Dashboard", "➕ Add Task", "📝 Pending Checklist", "✅ Completed", "❓ About"])

with t1:
    st.header("Quick Overview")
    
    pending_tasks = [t for t in st.session_state.tasks if t['Status'] == 'Pending']
    completed_tasks = [t for t in st.session_state.tasks if t['Status'] == 'Done']
    
    total_pending = len(pending_tasks)
    high_priority = sum(1 for t in pending_tasks if t['Priority'] >= 8)
    total_completed = len(completed_tasks)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pending Tasks", total_pending)
    c2.metric("High Priority", high_priority)
    c3.metric("Tasks Completed", total_completed)
    
    score = 0
    if (total_pending + total_completed) > 0:
        score = int((total_completed / (total_pending + total_completed)) * 100)
        
    c4.metric("Productivity Score", f"{score}%")
    
    st.divider()
    
    st.write("Weekly Progress")
    st.progress(score)
    
    if total_pending > 0:
        st.subheader("Tasks by Category")
        df_chart = pd.DataFrame(pending_tasks)
        category_counts = df_chart['Category'].value_counts()
        st.bar_chart(category_counts)
        
        st.subheader("Recent Pending Tasks")
        df_recent = pd.DataFrame(pending_tasks)[['Task', 'Category', 'Deadline', 'Priority']]
        st.dataframe(df_recent.head(5), use_container_width=True, hide_index=True)
    else:
        st.success("You have no pending tasks! Enjoy your free time or add a new task.")

with t2:
    st.header("Add a New Pending Task")
    with st.form("new_task_form", clear_on_submit=True):
        task_name = st.text_input("Task Name")
        
        col1, col2 = st.columns(2)
        with col1:
            deadline = st.date_input("Deadline", min_value=date.today())
            category = st.selectbox("Category", ["Homework", "Project", "Exam Study", "Personal Chores"])
        with col2:
            priority = st.slider("Priority Level (10 is highest)", 1, 10, 5)
            color = st.color_picker("Pick a color tag", "#00f900")
            
        desc = st.text_area("Task Description")
        is_urgent = st.toggle("Mark as URGENT")
        
        submit = st.form_submit_button("Save Task")
        
        if submit:
            if task_name == "":
                st.error("Please enter a task name!")
            else:
                st.session_state.tasks.append({
                    "id": len(st.session_state.tasks) + 1,
                    "Task": task_name,
                    "Category": category,
                    "Deadline": str(deadline),
                    "Priority": priority,
                    "Urgent": is_urgent,
                    "Color Tag": color,
                    "Description": desc,
                    "Status": "Pending"
                })
                st.success("Task added!")
                st.balloons()
                st.toast("Check your dashboard to see your new stats!")

with t3:
    st.header("Interactive Pending Checklist")
    st.info("Check the box next to a task to mark it as completed!")
    
    pending_list = [t for t in st.session_state.tasks if t['Status'] == 'Pending']
    
    if len(pending_list) == 0:
        st.write("No pending tasks.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            if task['Status'] == 'Pending':
                with st.container():
                    c1, c2 = st.columns([0.05, 0.95])
                    with c1:
                        if st.checkbox("", key=f"chk_{task['id']}"):
                            st.session_state.tasks[i]['Status'] = "Done"
                            st.rerun()
                    with c2:
                        if task['Urgent']:
                            st.markdown(f"🚨 **{task['Task']}** (Due: {task['Deadline']})")
                        else:
                            st.markdown(f"**{task['Task']}** (Due: {task['Deadline']})")
                        
                        with st.expander("View Details"):
                            st.write(f"Category: {task['Category']} | Priority: {task['Priority']}")
                            st.write(f"Notes: {task['Description']}")
                    st.divider()

with t4:
    st.header("Completed Tasks")
    completed_list = [t for t in st.session_state.tasks if t['Status'] == 'Done']
    
    if len(completed_list) == 0:
        st.write("You haven't completed any tasks yet. Get to work!")
    else:
        for task in completed_list:
            st.success(f"✅ {task['Task']} (Completed on {date.today()})")

with t5:
    st.header("About")
    st.markdown("""
    **What the app does (use-case):**
    This is a Pending Tracker application. It helps users list down things they need to do, set deadlines, and see a dashboard of their current workload to stay organized. It includes a dynamic checklist to mark items as done.
    
    **Who the target user is:**
    Students, freelancers, or anyone who has a lot of pending tasks and needs a simple, interactive way to track them instead of writing them on paper.
    
    **What inputs does the app collect:**
    Task name, deadline date, category, priority level, color tag, description, and an urgent status. It also collects checkbox inputs to update task statuses.
    
    **What output does it shows:**
    A dashboard showing calculated metrics, a progress bar, a bar chart of categories, and a recent tasks table. It also outputs an interactive checklist and a dedicated tab for finished tasks.
    """)