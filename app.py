import streamlit as st
from datetime import date, timedelta
# Import the custom database functions including the new execute_transaction
from db.connect_mysql import get_db_connection, run_query, execute_query, execute_transaction

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="Library Management System", layout="wide")
st.title("📚 Library Management System")

# Sidebar Navigation
menu = ["Books", "Members", "Issue/Return", "Reports"]
choice = st.sidebar.selectbox("Navigation", menu)

# ==================== BOOKS PAGE ====================
if choice == "Books":
    st.header("Manage Books")
    
    with st.expander("Add a New Book"):
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            category = st.text_input("Category")
            copies = st.number_input("Total Copies", min_value=1, step=1)
            submit_book = st.form_submit_button("Add Book")
            
            if submit_book:
                query = """
                INSERT INTO books (title, author, category, total_copies, available_copies) 
                VALUES (%s, %s, %s, %s, %s)
                """
                if execute_query(query, (title, author, category, copies, copies)):
                    st.success(f"'{title}' added successfully!")
                    
    st.subheader("Current Book Inventory")
    books_df = run_query("SELECT * FROM books")
    st.dataframe(books_df, use_container_width=True)

# ==================== MEMBERS PAGE ====================
elif choice == "Members":
    st.header("Manage Members")
    
    with st.expander("Add a New Member"):
        with st.form("add_member_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            join_date = st.date_input("Join Date", date.today())
            status = st.selectbox("Status", ["active", "inactive"])
            submit_member = st.form_submit_button("Add Member")
            
            if submit_member:
                query = "INSERT INTO members (name, email, join_date, status) VALUES (%s, %s, %s, %s)"
                if execute_query(query, (name, email, join_date, status)):
                    st.success(f"Member '{name}' added successfully!")

    st.subheader("Member List")
    members_df = run_query("SELECT * FROM members")
    st.dataframe(members_df, use_container_width=True)

# ==================== ISSUE / RETURN PAGE ====================
elif choice == "Issue/Return":
    st.header("Issue or Return a Book")
    
    col1, col2 = st.columns(2)
    
    # ISSUE BOOK LOGIC
    with col1:
        st.subheader("Issue Book")
        # Ensure available_copies > 0 before issue
        books_list = run_query("SELECT book_id, title, available_copies FROM books WHERE available_copies > 0")
        members_list = run_query("SELECT member_id, name FROM members WHERE status = 'active'")
        
        if not books_list.empty and not members_list.empty:
            book_options = {row['title']: row['book_id'] for _, row in books_list.iterrows()}
            member_options = {row['name']: row['member_id'] for _, row in members_list.iterrows()}
            
            sel_book = st.selectbox("Select Book", options=book_options.keys())
            sel_member = st.selectbox("Select Member", options=member_options.keys())
            issue_date = date.today()
            due_date = issue_date + timedelta(days=14) 
            
            if st.button("Issue Book"):
                b_id = book_options[sel_book]
                m_id = member_options[sel_member]
                
                # Group queries for the transaction helper
                issue_queries = [
                    ("INSERT INTO book_issues (book_id, member_id, issue_date, due_date) VALUES (%s, %s, %s, %s)", (b_id, m_id, issue_date, due_date)),
                    ("UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s", (b_id,))
                ]
                
                success, error = execute_transaction(issue_queries)
                
                if success:
                    st.success(f"Book issued to {sel_member}. Due back on {due_date}.")
                else:
                    st.error(f"Transaction failed: {error}")
        else:
            st.warning("No books available or no active members.")

    # RETURN BOOK LOGIC
    with col2:
        st.subheader("Return Book")
        active_issues = run_query("""
            SELECT bi.issue_id, b.title, m.name 
            FROM book_issues bi
            JOIN books b ON bi.book_id = b.book_id
            JOIN members m ON bi.member_id = m.member_id
            WHERE bi.return_date IS NULL
        """)
        
        if not active_issues.empty:
            issue_options = {f"{row['title']} (Borrowed by {row['name']})": row['issue_id'] for _, row in active_issues.iterrows()}
            sel_return = st.selectbox("Select Record to Return", options=issue_options.keys())
            return_date = date.today()
            
            if st.button("Process Return"):
                i_id = issue_options[sel_return]
                
                b_id_df = run_query("SELECT book_id FROM book_issues WHERE issue_id = %s", (i_id,))
                b_id = int(b_id_df.iloc[0]['book_id'])
                
                # Group queries for the transaction helper
                return_queries = [
                    ("UPDATE book_issues SET return_date = %s WHERE issue_id = %s", (return_date, i_id)),
                    ("UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s", (b_id,))
                ]
                
                success, error = execute_transaction(return_queries)
                
                if success:
                    st.success("Book returned successfully!")
                else:
                    st.error(f"Transaction failed: {error}")
        else:
            st.info("No pending book returns.")

# ==================== REPORTS PAGE ====================
elif choice == "Reports":
    st.header("Library Analytics & Reports")
    
    tab1, tab2, tab3 = st.tabs(["Active Borrowers", "Overdue Books", "Top 5 Popular Books"])
    
    with tab1:
        st.subheader("Who has borrowed which book?")
        query_borrowers = """
            SELECT m.name AS Member, b.title AS Book, bi.issue_date, bi.due_date 
            FROM book_issues bi
            JOIN members m ON bi.member_id = m.member_id
            JOIN books b ON bi.book_id = b.book_id
            WHERE bi.return_date IS NULL
            ORDER BY bi.issue_date DESC;
        """
        st.dataframe(run_query(query_borrowers), width="stretch")

    with tab2:
        st.subheader("Overdue Books")
        query_overdue = """
            SELECT m.name AS Member, m.email, b.title AS Book, bi.due_date, DATEDIFF(CURDATE(), bi.due_date) as Days_Overdue
            FROM book_issues bi
            JOIN members m ON bi.member_id = m.member_id
            JOIN books b ON bi.book_id = b.book_id
            WHERE bi.return_date IS NULL AND bi.due_date < CURDATE()
            ORDER BY Days_Overdue DESC;
        """
        df_overdue = run_query(query_overdue)
        if df_overdue.empty:
            st.success("No overdue books at the moment!")
        else:
            st.dataframe(df_overdue, width="stretch")

    with tab3:
        st.subheader("Top 5 Most Borrowed Books")
        query_top5 = """
            SELECT b.title, b.author, COUNT(bi.issue_id) AS times_borrowed
            FROM books b
            LEFT JOIN book_issues bi ON b.book_id = bi.book_id
            GROUP BY b.book_id
            ORDER BY times_borrowed DESC
            LIMIT 5;
        """
        df_top5 = run_query(query_top5)
        st.bar_chart(df_top5.set_index('title')['times_borrowed'])