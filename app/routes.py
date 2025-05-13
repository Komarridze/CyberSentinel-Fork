from flask import Blueprint, request, jsonify, send_file, make_response, current_app, render_template
from flask_socketio import emit
import csv, io
from datetime import datetime
from app import socketio
from app.models import LogEntry
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    query = request.args.get("q")
    if query:
        logs = LogEntry.query.filter(LogEntry.message.ilike(f"%{query}%")).order_by(LogEntry.timestamp.desc()).all()
    else:
        logs = LogEntry.query.order_by(LogEntry.timestamp.desc()).all()
    return render_template("dashboard.html", logs=logs)

@main_bp.route('/base')
def base():
    return render_template("base.html")

@main_bp.route('/about')
def about():
    return render_template("about.html")

@main_bp.route('/login')
def login():
    return render_template("login.html")

@main_bp.route('/api/logs', methods=['GET'])
@login_required
def get_logs():
    """Return logs with optional filtering: level, keyword, agent, date range, pagination parameters."""
    # Parse query parameters
    level = request.args.get("level")
    keyword = request.args.get("keyword")
    agent = request.args.get("agent")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 100))
    
    # Query LogEntry model
    query = LogEntry.query  # customize with filtering logic
    if level:
        query = query.filter(LogEntry.level==level)
    if keyword:
        query = query.filter(LogEntry.message.ilike(f"%{keyword}%"))
    if agent:
        query = query.filter(LogEntry.agent==agent)
    if start_date:
        query = query.filter(LogEntry.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(LogEntry.timestamp <= datetime.fromisoformat(end_date))

    logs = query.order_by(LogEntry.timestamp.desc()).paginate(page, per_page, False)
    
    return jsonify({
        "logs": [log.to_dict() for log in logs.items],
        "page": page,
        "per_page": per_page,
        "total": logs.total
    })
    
@main_bp.route('/api/export_logs', methods=['GET'])
@login_required
def export_logs():
    """Exports filtered logs as CSV"""
    # Same filter logic as the get_logs endpoint
    # For brevity, assume we fetch all filtered logs into 'logs'
    logs = LogEntry.query.order_by(LogEntry.timestamp.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp", "Level", "Agent", "Message"])
    for log in logs:
        writer.writerow([log.timestamp, log.level, log.agent, log.message])
    
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=logs.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

# SocketIO event to push new log entries
@socketio.on('connect')
def handle_connect():
    print("Client Connected")
    
def push_log_update(log_data):
    # Called by your Logger/Monitor Agent when a new long entry arrives
    socketio.emit("new_log", log_data)
    
# This push_log_update function would be called from agent integrations or a background thread.