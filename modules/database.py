import sqlite3, json
from pathlib import Path
from config import DB_PATH
from modules.report_generator import report_text
def get_conn(): Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True); return sqlite3.connect(DB_PATH)
def init_db():
    with get_conn() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS scan_history (id INTEGER PRIMARY KEY AUTOINCREMENT,timestamp TEXT,input_type TEXT,sender TEXT,subject TEXT,message_preview TEXT,full_message TEXT,urls_found TEXT,attachments_found TEXT,threat_score INTEGER,risk_level TEXT,threat_category TEXT,detected_signals TEXT,reasoning_summary TEXT,recommendation TEXT,report_text TEXT)'''); conn.commit()
def save_scan(result):
    init_db()
    with get_conn() as conn:
        cur=conn.execute('''INSERT INTO scan_history (timestamp,input_type,sender,subject,message_preview,full_message,urls_found,attachments_found,threat_score,risk_level,threat_category,detected_signals,reasoning_summary,recommendation,report_text) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(result.get('timestamp'),result.get('input_type'),result.get('sender'),result.get('subject'),result.get('message_preview'),result.get('full_message'),json.dumps(result.get('urls_found',[])),json.dumps(result.get('attachments_found',[])),result.get('threat_score'),result.get('risk_level'),result.get('threat_category'),json.dumps(result.get('detected_signals',[])),result.get('reasoning_summary'),result.get('recommended_action'),report_text(result)))
        conn.commit(); return cur.lastrowid
def fetch_history(limit=500):
    init_db()
    with get_conn() as conn:
        conn.row_factory=sqlite3.Row; return [dict(r) for r in conn.execute('SELECT * FROM scan_history ORDER BY id DESC LIMIT ?',(limit,)).fetchall()]
def clear_history():
    init_db()
    with get_conn() as conn: conn.execute('DELETE FROM scan_history'); conn.commit()
