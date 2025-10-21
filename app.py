from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
import datetime
import json
import random
import requests # Needed for Phase 4: Compiler

# --- PHASE 3 IMPORTS: AI Logic ---
# You must create 'interview_data.py' and install 'google-genai'
from interview_data import INTERVIEW_QUESTIONS, REMEDIAL_RESOURCES 
# Uncomment the following lines when you are ready to integrate the REAL AI
# from google import genai 


# --- CONFIGURATION ---
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  

# --- MONGODB CONNECTION ---
MONGO_URI = os.getenv('MONGO_URI')
try:
    client = MongoClient(MONGO_URI)
    # FIX: Using 'campus360db' to match your Atlas screenshot
    db = client.campus360db 
except Exception as e:
    print(f"!!! CRITICAL MONGODB CONNECTION FAILURE: {e} !!!")
    print("!!! Please check your MONGO_URI in the .env file. !!!")
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
    PHASE 3: MOCK LLM ANALYSIS FUNCTION
    Mocks the AI response structure for local testing continuity.
    REPLACE this entire body with the REAL Gemini API call when ready (as previously detailed).
    """
    mock_score = random.randint(30, 95)
    mock_category = random.choice(list(REMEDIAL_RESOURCES.keys()))

    mock_analysis = {
        "score": mock_score,
        "communication_feedback": f"MOCK: Your structure needs polish. Focus on organizing your thoughts before speaking. (Score: {mock_score})",
        "technical_feedback": f"MOCK: Concept {concept_key} explanation was {mock_score//10 * 10}% accurate. Needs deeper understanding.",
        "improvement_category": mock_category 
    }
    return mock_analysis


# ----------------------------------------------------
# AUTHENTICATION ROUTES (FINAL CORRECTED)
# ----------------------------------------------------

# app.py (Replace the landing_page function)

@app.route('/')
def landing_page():
    # Check if the user is already logged in (Role exists in session)
    if 'role' in session:
        if session['role'] == 'student':
            return redirect(url_for('student_dashboard'))
        elif session['role'] == 'faculty':
            return redirect(url_for('faculty_dashboard'))
    
    # If the user is NOT logged in, show the landing page (index.html)
    return render_template('index.html')

# Note: The login function mapped to /login remains the same.


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # --- PROCESS LOGIN CREDENTIALS ---
        username = request.form.get('username')
        password = request.form.get('password')

        user = users_collection.find_one({"username": username})

        if user and check_password_hash(user['password'], password):
            # Authentication Success
            session['user_id'] = str(user['_id'])
            session['role'] = user['role']
            session['username'] = user['username']
            
            if user['role'] == 'student':
                return redirect(url_for('student_dashboard'))
            elif user['role'] == 'faculty':
                return redirect(url_for('faculty_dashboard'))
        else:
            # Authentication Failure
            flash("Invalid username or password.", 'danger')
            return redirect(url_for('login')) # Redirect back to the GET view
    
    # --- SHOW LOGIN FORM (GET REQUEST) ---
    return render_template('auth_form.html')
# app.py (Add this route after the existing login function)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1. Check if user already exists
        if users_collection.find_one({"username": username}):
            flash("Account already exists with this email.", 'danger')
            return redirect(url_for('signup'))
        
        # 2. Re-validate password constraints (Backend check)
        # We assume the user signing up is a 'student' by default for the hackathon MVP
        if not (len(password) >= 8 and any(c.isupper() for c in password) and 
                any(c.islower() for c in password) and any(c.isdigit() for c in password) and 
                any(c in "!@#$%^&*()_+-=" for c in password)):
            # This should ideally be handled by the frontend, but is a good security fallback
            flash("Password does not meet complexity requirements.", 'danger')
            return redirect(url_for('signup'))

        # 3. Hash password and insert new user into MongoDB
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # app.py (Inside the signup function, replace the insertion block and return)

        # 3. Hash password and insert new user into MongoDB
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Insert the new user and capture the result, which contains the unique MongoDB ID (_id)
        result = users_collection.insert_one({
            "username": username,
            "password": hashed_password,
            "role": "student"
        })

        # --- Automatic Login Logic ---
        user_id = str(result.inserted_id)
        
        # 4. Set Session variables to log the user in instantly
        session['user_id'] = user_id
        session['role'] = "student"
        session['username'] = username
        
        # 5. Redirect the user directly to their dashboard
        flash("Account created successfully! Welcome aboard.", 'success')
        return redirect(url_for('student_dashboard')) 
    
    # Show the sign-up form template (GET request)
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ----------------------------------------------------
# DASHBOARD ROUTES
# ----------------------------------------------------

@app.route('/student_dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student': return redirect(url_for('login'))
    
    user_id = ObjectId(session['user_id'])
    
    # Fetch recent interview results 
    recent_interviews = interview_results_collection.find(
        {"student_id": user_id}
    ).sort("timestamp", -1).limit(5)
    
    # Fetch coding activity
    recent_coding = coding_activity_collection.find(
        {"student_id": user_id}
    ).sort("timestamp", -1).limit(5)

    return render_template(
        'student.html', 
        username=session['username'].split('@')[0],
        interviews=list(recent_interviews),
        coding_activity=list(recent_coding)
    )

# app.py (Replace the entire faculty_dashboard route)

@app.route('/faculty_dashboard')
def faculty_dashboard():
    if 'role' not in session or session['role'] != 'faculty': return redirect(url_for('login'))
    
    # Fetch all student accounts
    all_students = users_collection.find({"role": "student"})
    student_data = []

    # Define a cutoff date for "recent" activity (e.g., last 7 days)
    one_week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    for student in all_students:
        student_id = student['_id']
        
        # --- 1. Calculate Average Interview Score ---
        # MongoDB aggregation pipeline calculates the average score for this student
        interview_stats = list(interview_results_collection.aggregate([
            {"$match": {"student_id": student_id}},
            {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
        ]))
        
        # Get score or default to 0 if no interviews exist
        avg_score = round(interview_stats[0]['avg_score'], 1) if interview_stats else 0
        
        # --- 2. Count Recent Activity (Interviews + Coding) ---
        recent_interview_count = interview_results_collection.count_documents({
            "student_id": student_id,
            "timestamp": {"$gte": one_week_ago}
        })
        recent_coding_count = coding_activity_collection.count_documents({
            "student_id": student_id,
            "timestamp": {"$gte": one_week_ago}
        })
        
        total_recent_activity = recent_interview_count + recent_coding_count
        
        # --- 3. Determine Intervention Need (Low Score OR Inactive) ---
        # Flag if score is low (e.g., < 60%) AND they have taken at least one interview, 
        # OR if they have done zero activity this week.
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
# PHASE 3: AI INTERVIEWER ROUTES
# ----------------------------------------------------

@app.route('/start_interview/<q_key>')
def start_interview(q_key):
    if 'role' not in session or session['role'] != 'student': return redirect(url_for('login'))
    
    if q_key not in INTERVIEW_QUESTIONS:
        flash("Invalid question selected.", 'danger')
        return redirect(url_for('student_dashboard')) 

    question = INTERVIEW_QUESTIONS[q_key]
    return render_template('interview.html', question=question, question_key=q_key)


@app.route('/process_interview', methods=['POST'])
def process_interview():
    if 'role' not in session or session['role'] != 'student': return redirect(url_for('login'))
    
    q_key = request.form.get('question_key')
    student_answer = request.form.get('student_answer')

    question = INTERVIEW_QUESTIONS.get(q_key)

    if not question or not student_answer:
        flash("Missing question or answer.", 'danger')
        return redirect(url_for('student_dashboard'))

    # --- CORE AI ANALYSIS ---
    analysis = analyze_response(question['text'], student_answer, question['concept'])
    
    if analysis is None:
        flash("Error processing interview with AI. Please check server logs.", 'danger')
        return redirect(url_for('student_dashboard'))

    # Find the specific remedial resource based on the AI's category
    remedy_key = analysis.get('improvement_category', 'communication_structure')
    resource = REMEDIAL_RESOURCES.get(remedy_key)

    # Log the result to MongoDB
    interview_results_collection.insert_one({
        "student_id": ObjectId(session['user_id']),
        "timestamp": datetime.datetime.utcnow(),
        "question": question['text'],
        "score": analysis['score'],
        "communication_feedback": analysis['communication_feedback'],
        "technical_feedback": analysis['technical_feedback'],
        "improvement_category": remedy_key,
        "remedial_resource": resource,
    })

    flash(f"Interview Complete! Your score is {analysis['score']}%. Review your latest results below.", 'success')
    return redirect(url_for('student_dashboard'))


# ----------------------------------------------------
# PHASE 4: COMPILER ROUTE
# ----------------------------------------------------

# PHASE 4: COMPILER SETUP
COMPILER_LANGUAGES = {
    "python": "3.10", 
    "c": "10.2.0",    
    "cpp": "10.2.0",  
    "java": "15.0.2", 
}

@app.route('/compiler', methods=['GET', 'POST'])
def compiler():
    if 'role' not in session or session['role'] != 'student': 
        return redirect(url_for('login'))
    
    output = None
    code = "print('Hello World')" # Default code for Python
    lang = "python" # Default language
    
    if request.method == 'POST':
        code = request.form.get('code_input')
        lang = request.form.get('language')
        
        if lang not in COMPILER_LANGUAGES:
            output = "Error: Unsupported language selected."
        
        # --- API CALL: Piston API (Free Compiler Service) ---
        api_url = "https://emkc.org/api/v2/piston/execute"
        
        payload = {
            "language": lang,
            "version": COMPILER_LANGUAGES[lang],
            "files": [{"content": code}]
        }
        
        status = "Execution Success"
        
        try:
            # Send the code to the external execution API
            response = requests.post(api_url, json=payload, timeout=15)
            result = response.json()
            
            # Check for execution output or errors
            if result.get('run', {}).get('output'):
                output = result['run']['output']
                status = "Success" if result['run']['code'] == 0 else "Runtime Error"
            else:
                # Capture compilation errors or API failure
                output = result.get('compile', {}).get('output') or "Execution failed or timed out."
                status = "Compile Error"
                
            # Log the activity to MongoDB
            coding_activity_collection.insert_one({
                "student_id": ObjectId(session['user_id']),
                "timestamp": datetime.datetime.utcnow(),
                "language": lang,
                "status": status,
                "code_snippet": code[:100] # Log first 100 characters for analysis
            })

        except requests.exceptions.RequestException as e:
            output = f"API Connection Error: Cannot reach compiler service. ({e})"
            status = "API Error"
            
    return render_template('compiler.html', output=output, code=code, selected_lang=lang, languages=COMPILER_LANGUAGES)


# ----------------------------------------------------
# STARTUP LOGIC
# ----------------------------------------------------

if __name__ == '__main__':
    # CRITICAL: This block ensures the sample users are created ONCE 
    # if the database is empty, and catches connection errors.
    try:
        # Check if the students collection is empty.
        if users_collection.count_documents({}) == 0:
            create_sample_users()
        else:
            print("--- Sample users already exist in MongoDB. Skipping creation. ---")
    except Exception as e:
        print(f"!!! CRITICAL MONGODB CONNECTION ERROR: {e} !!!")
        print("!!! Please check your MONGO_URI in the .env file. Shutting down. !!!")
        # Exit the program if database connection failed
        exit() 

    app.run(debug=True)