import sqlite3

def init_db():
    with sqlite3.connect("chat_history.db") as db:
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            positive_answers TEXT,
            known_facts TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            user_id INTEGER PRIMARY KEY,
            actual_question_number INTEGER DEFAULT 0,
            akinator_wins INTEGER DEFAULT 0,
            user_wins INTEGER DEFAULT 0,
            last_question TEXT DEFAULT '',
            is_final_state INTEGER DEFAULT 0
        )
        ''')


def get_session(user_id):
    with sqlite3.connect("chat_history.db") as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT actual_question_number, akinator_wins, user_wins, last_question, is_final_state FROM sessions WHERE user_id=?",
            (user_id,))
        row = cursor.fetchone()

        if row:
            return {
                "actual_question_number": row[0],
                "akinator_wins": row[1],
                "user_wins": row[2],
                "last_question": row[3],
                "is_final_state": bool(row[4])
            }
        else:

            cursor.execute("INSERT INTO sessions(user_id) VALUES (?)", (user_id,))
            return {"actual_question_number": 0, "akinator_wins": 0, "user_wins": 0, "last_question": "","is_final_state": False}
def clear_user_history(user_id):
    with sqlite3.connect("chat_history.db") as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM messages WHERE user_id=?", (user_id,))
        cursor.execute('''UPDATE sessions SET actual_question_number=?, last_question=?, is_final_state=? WHERE user_id=?''',(0, "", 0, user_id))
def update_session(user_id, question_number, akinator_wins, user_wins, last_question, is_final_state):
    with sqlite3.connect("chat_history.db") as db:
        cursor = db.cursor()
        cursor.execute('''
        UPDATE sessions 
        SET actual_question_number=?, akinator_wins=?, user_wins=?, last_question=?, is_final_state=? 
        WHERE user_id=?
        ''', (question_number, akinator_wins, user_wins, last_question, int(is_final_state), user_id))
def save_messages_positive(user_id, positive_answer):
    with sqlite3.connect("chat_history.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO messages(user_id,positive_answers) VALUES (?,?)", (user_id, positive_answer))
def save_messages_known_facts(user_id, last_question, user_answer):
    with sqlite3.connect("chat_history.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO messages(user_id,known_facts) VALUES (?,?)",(user_id, f"Q: {last_question} -> A: {user_answer}"))

def positive_answers_select(user_id):
    history = []
    with sqlite3.connect("chat_history.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT positive_answers FROM messages WHERE user_id=? ORDER BY id ASC", (user_id,))
        rows = cursor.fetchall()
        for row in rows:
            positive_answer = row
            history.append(positive_answer)
    return history
def known_facts_select(user_id):
    history = []
    with sqlite3.connect("chat_history.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT known_facts FROM messages WHERE user_id=? ORDER BY id ASC", (user_id,))
        rows = cursor.fetchall()
        for row in rows:
            known_fact = row
            history.append(known_fact)
    return history
init_db()