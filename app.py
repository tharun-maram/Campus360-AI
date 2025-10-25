# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
import datetime
import json
import random
import requests # Needed for Compiler

# --- PHASE 9 IMPORTS: AI Logic and Customization ---
from interview_data import (
    INTERVIEW_QUESTIONS_BY_ROLE, REMEDIAL_RESOURCES, 
    LEVEL_CATEGORIES, BRANCH_CATEGORIES, ROLE_CATEGORIES, 
    PHASE_INTRODUCTION_Q, PHASE_SOFT_SKILL_Q
)

# --- CONFIGURATION ---
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  

# --- MONGODB CONNECTION ---
MONGO_URI = os.getenv('MONGO_URI')
try:
    client = MongoClient(MONGO_URI)
    db = client.campus360db 
except Exception as e:
    print(f"!!! CRITICAL MONGODB CONNECTION FAILURE: {e} !!!")
    exit()

# Define your collections 
users_collection = db.students 
interview_results_collection = db.interview_results
coding_activity_collection = db.coding_activity


# ----------------------------------------------------
# HELPER FUNCTIONS 
# ----------------------------------------------------

def create_sample_users():
    """Inserts sample users into the students collection."""
    hashed_student_pass = generate_password_hash("Student@123", method='pbkdf2:sha256')
    hashed_faculty_pass = generate_password_hash("Faculty@123", method='pbkdf2:sha256')

    sample_users = [
        {"username": "student1@gmail.com", "password": hashed_student_pass, "role": "student"},
        {"username": "faculty@gmail.com", "password": hashed_faculty_pass, "role": "faculty"},
        {"username": "student2@gmail.com", "password": hashed_student_pass, "role": "student"},
    ]
    users_collection.insert_many(sample_users)
    print("--- Sample users created in MongoDB (3 users)! ---")


def analyze_response(question_text, student_answer, concept_key):
    """
    PHASE 3: MOCK LLM ANALYSIS FUNCTION - Used for demonstration.
    """
    mock_score = random.randint(30, 95)
    mock_category = random.choice(list(REMEDIAL_RESOURCES.keys()))

    mock_analysis = {
        "score": mock_score,
        "communication_feedback": f"MOCK: Your structure needs polish. Focus on organizing thoughts for {concept_key}.",
        "technical_feedback": f"MOCK: Concept {concept_key} explanation was {mock_score//10 * 10}% accurate.",
        "improvement_category": mock_category 
    }
    return mock_analysis


# ----------------------------------------------------
# AUTHENTICATION & DASHBOARD ROUTES
# ----------------------------------------------------

@app.route('/')
def landing_page():
    if 'role' in session:
        return redirect(url_for('student_dashboard' if session['role'] == 'student' else 'faculty_dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users_collection.find_one({"username": username})

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['role'] = user['role']
            session['username'] = user['username']
            return redirect(url_for('student_dashboard' if user['role'] == 'student' else 'faculty_dashboard'))
        else:
            flash("Invalid username or password.", 'danger')
            return redirect(url_for('login'))
    
    return render_template('auth_form.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if users_collection.find_one({"username": username}):
            flash("Account already exists with this email.", 'danger')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        result = users_collection.insert_one({
            "username": username,
            "password": hashed_password,
            "role": "student"
        })

        # Automatic Login Logic
        session['user_id'] = str(result.inserted_id)
        session['role'] = "student"
        session['username'] = username
        
        flash("Account created successfully! Welcome aboard.", 'success')
        return redirect(url_for('student_dashboard')) 
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    # This clears all session data, preventing confusion
    session.clear() 
    return redirect(url_for('login'))


@app.route('/student_dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student': return redirect(url_for('login'))
    
    user_id = ObjectId(session['user_id'])
    
    # Fetch recent activity
    recent_interviews = interview_results_collection.find({"student_id": user_id}).sort("timestamp", -1).limit(5)
    recent_coding = coding_activity_collection.find({"student_id": user_id}).sort("timestamp", -1).limit(5)

    return render_template(
        'student.html', 
        username=session['username'].split('@')[0],
        interviews=list(recent_interviews),
        coding_activity=list(recent_coding)
    )

@app.route('/faculty_dashboard')
def faculty_dashboard():
    if 'role' not in session or session['role'] != 'faculty': return redirect(url_for('login'))
    
    all_students = users_collection.find({"role": "student"})
    student_data = []

    one_week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    for student in all_students:
        student_id = student['_id']
        
        interview_stats = list(interview_results_collection.aggregate([
            {"$match": {"student_id": student_id}},
            {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
        ]))
        
        avg_score = round(interview_stats[0]['avg_score'], 1) if interview_stats else 0
        
        recent_interview_count = interview_results_collection.count_documents({"student_id": student_id, "timestamp": {"$gte": one_week_ago}})
        recent_coding_count = coding_activity_collection.count_documents({"student_id": student_id, "timestamp": {"$gte": one_week_ago}})
        
        total_recent_activity = recent_interview_count + recent_coding_count
        
        intervention = (avg_score < 60 and avg_score > 0) or (total_recent_activity == 0)

        student_data.append({
            "id": str(student_id),
            "username": student['username'].split('@')[0],
            "last_score": avg_score,
            "total_activity": total_recent_activity,
            "intervention_needed": intervention,
        })

    return render_template(
        'faculty.html', 
        username=session['username'].split('@')[0],
        student_data=student_data
    )


# ----------------------------------------------------
# DYNAMIC INTERVIEW ROUTES (Structured 10-Question Flow)
# ----------------------------------------------------

@app.route('/start_interview', methods=['GET', 'POST'])
def start_interview():
    if 'role' not in session or session['role'] != 'student': return redirect(url_for('login'))
    
    if request.method == 'POST':
        role = request.form.get('target_role')
        
        if not role or role not in INTERVIEW_QUESTIONS_BY_ROLE:
            flash("Please select your target job role.", 'danger')
            return redirect(url_for('start_interview'))

        tech_pool = INTERVIEW_QUESTIONS_BY_ROLE.get(role, [])
        
        # --- BUILD THE 10-QUESTION FINAL LIST ---
        final_q_list = PHASE_INTRODUCTION_Q[:] 
        
        # 2. Technical (5 questions: 2 easy/medium, 3 medium/hard)
        easy_med_tech = [q for q in tech_pool if q['difficulty'] in ['easy', 'medium']]
        hard_tech = [q for q in tech_pool if q['difficulty'] in ['medium', 'hard']]
        
        random.shuffle(easy_med_tech)
        random.shuffle(hard_tech)
        final_q_list.extend(easy_med_tech[:2])
        final_q_list.extend(hard_tech[:3])

        # 3. Soft Skills (3 random questions)
        random.shuffle(PHASE_SOFT_SKILL_Q)
        final_q_list.extend(PHASE_SOFT_SKILL_Q[:3])
        
        # Initialize session state
        session['interview_state'] = {
            'role': role,
            'current_index': 0,
            'question_list': final_q_list, 
            'total_questions': len(final_q_list),
        }
        
        return redirect(url_for('next_question'))

    # Mode 1: Show Selection Form (GET Request)
    return render_template(
        'interview_select.html', 
        levels=LEVEL_CATEGORIES, 
        branches=BRANCH_CATEGORIES,
        roles=ROLE_CATEGORIES 
    )

@app.route('/next_question', methods=['GET'])
def next_question():
    state = session.get('interview_state')
    if not state:
        flash("Interview session expired. Please restart.", 'danger')
        return redirect(url_for('start_interview'))
    
    current_index = state['current_index']
    
    if current_index >= state['total_questions']:
        # Interview is complete
        session.pop('interview_state', None) 
        flash(f"Congratulations! Your systematic interview for {state['role']} is complete. View your full report.", 'success')
        return redirect(url_for('student_dashboard'))
    
    # GET CURRENT QUESTION
    question_data = state['question_list'][current_index]
    
    q_key = f"{state['role']}_Q{current_index}_{question_data['concept']}"
    
    # RENDER THE QUESTION
    return render_template('interview.html', question=question_data, question_key=q_key, current_q_num=current_index + 1, total_q_num=state['total_questions'])

@app.route('/process_interview', methods=['POST'])
def process_interview():
    if 'role' not in session or not session.get('interview_state'):
        flash("Session error. Please restart the interview.", 'danger')
        return redirect(url_for('start_interview'))
    
    state = session['interview_state']
    
    # PROCESS AND LOG ANSWER
    full_q_key = request.form.get('question_key')
    student_answer = request.form.get('student_answer')
    question_text = request.form.get('question_text')

    concept_key = full_q_key.split('_')[-1]
    
    analysis = analyze_response(question_text, student_answer, concept_key)
    
    if analysis is None:
        flash("Error processing answer with AI. Logging stopped.", 'danger')
    else:
        remedy_key = analysis.get('improvement_category', 'communication_structure')
        resource = REMEDIAL_RESOURCES.get(remedy_key)
        
        interview_results_collection.insert_one({
            "student_id": ObjectId(session['user_id']),
            "timestamp": datetime.datetime.utcnow(),
            "question": question_text,
            "score": analysis['score'],
            "communication_feedback": analysis['communication_feedback'],
            "technical_feedback": analysis['technical_feedback'],
            "improvement_category": remedy_key,
            "remedial_resource": resource,
        })
        
        flash(f"Answer received and analyzed! Score: {analysis['score']}%.", 'info')

    # ADVANCE THE INTERVIEW STATE
    state['current_index'] += 1
    session['interview_state'] = state
    
    # REDIRECT TO NEXT QUESTION
    return redirect(url_for('next_question'))


# ----------------------------------------------------
# COMPILER & ROADMAP ROUTES
# ----------------------------------------------------

COMPILER_LANGUAGES = {"python": "3.10", "c": "10.2.0", "cpp": "10.2.0", "java": "15.0.2"}

@app.route('/compiler', methods=['GET', 'POST'])
def compiler():
    if 'role' not in session or session['role'] != 'student': return redirect(url_for('login'))
    
    output = None
    code = "print('Hello World')" 
    lang = "python"
    
    if request.method == 'POST':
        code = request.form.get('code_input')
        lang = request.form.get('language')
        api_url = "https://emkc.org/api/v2/piston/execute"
        payload = {"language": lang, "version": COMPILER_LANGUAGES.get(lang), "files": [{"content": code}]}
        status = "Execution Success"
        
        try:
            response = requests.post(api_url, json=payload, timeout=15)
            result = response.json()
            if result.get('run', {}).get('output'):
                output = result['run']['output']
                status = "Success" if result['run']['code'] == 0 else "Runtime Error"
            else:
                output = result.get('compile', {}).get('output') or "Execution failed or timed out."
                status = "Compile Error"
                
            coding_activity_collection.insert_one({"student_id": ObjectId(session['user_id']), "timestamp": datetime.datetime.utcnow(), "language": lang, "status": status, "code_snippet": code[:100]})
        except requests.exceptions.RequestException as e:
            output = f"API Connection Error: ({e})"
            
    return render_template('compiler.html', output=output, code=code, selected_lang=lang, languages=COMPILER_LANGUAGES)

@app.route('/roadmap', methods=['GET'])
def roadmap():
    if 'role' not in session or session['role'] != 'student': 
        return redirect(url_for('login'))
    
    # Base URL for the roadmap website
    base_url = "https://roadmap.sh"
    
    # Get the search query (profession) from the URL parameter
    search_query = request.args.get('search', '').strip()
    
    # Comprehensive list of roles for the dropdown
    roles = [
        "Frontend", "Backend", "DevOps", "Data Science", 
        "AI/ML", "Java", "Python", "Full Stack", "Cyber Security", 
        "Product Manager", "UX Design"
    ]
    
    # Construct the URL based on the user's selection
    # Example: If user selects 'Data Science', the URL will be roadmap.sh/data-science
    roadmap_path = "frontend" # Default path
    if search_query:
        # Normalize the query to match roadmap.sh's URL format (lowercase, hyphens)
        roadmap_path = search_query.lower().replace(" ", "-").replace("/", "")
        
    roadmap_url = f"{base_url}/{roadmap_path}"
        
    return render_template('roadmap.html', roadmap_url=roadmap_url, roles=roles, selected_path=roadmap_path)


# ----------------------------------------------------
# STARTUP LOGIC
# ----------------------------------------------------

if __name__ == '__main__':
    try:
        if users_collection.count_documents({}) == 0:
            create_sample_users()
        else:
            print("--- Sample users already exist in MongoDB. Skipping creation. ---")
    except Exception as e:
        print(f"!!! CRITICAL MONGODB CONNECTION ERROR: {e} !!!")
        exit() 

    app.run(debug=True)