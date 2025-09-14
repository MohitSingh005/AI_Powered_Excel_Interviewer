"""
Flask Web Application for Excel Mock Interviewer
Main entry point with API endpoints
"""

from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
import os
from app.interview_agent import InterviewAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize the interview agent
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is required")

interview_agent = InterviewAgent(groq_api_key)

@app.route('/')
def index():
    """Main interview interface"""
    return render_template('index.html')

@app.route('/api/interview/start', methods=['POST'])
def start_interview():
    """Start a new interview session"""
    try:
        data = request.get_json()
        
        candidate_name = data.get('candidate_name', '').strip()
        target_role = data.get('target_role', '').strip()
        experience_level = data.get('experience_level', 'intermediate').strip()
        
        if not candidate_name or not target_role:
            return jsonify({
                'error': 'Missing required fields: candidate_name and target_role'
            }), 400
        
        result = interview_agent.start_interview(
            candidate_name=candidate_name,
            target_role=target_role,
            experience_level=experience_level
        )
        
        # Store interview ID in session
        session['current_interview_id'] = result['interview_id']
        
        return jsonify({
            'success': True,
            'interview_id': result['interview_id'],
            'message': result['message'],
            'status': result['status']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to start interview: {str(e)}'
        }), 500

@app.route('/api/interview/message', methods=['POST'])
def send_message():
    """Send a message in the current interview"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        interview_id = data.get('interview_id') or session.get('current_interview_id')
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        if not interview_id:
            return jsonify({'error': 'No active interview session'}), 400
        
        result = interview_agent.process_message(interview_id, message)
        
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify({
            'success': True,
            'message': result['message'],
            'interview_id': interview_id
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to process message: {str(e)}'
        }), 500

@app.route('/api/interview/status/<interview_id>')
def get_interview_status(interview_id):
    """Get the current status of an interview"""
    try:
        interview_data = interview_agent._load_interview_data(interview_id)
        
        if not interview_data:
            return jsonify({'error': 'Interview not found'}), 404
        
        return jsonify({
            'success': True,
            'interview_id': interview_id,
            'status': interview_data['status'],
            'current_phase': interview_data['current_phase'],
            'question_count': interview_data['question_count'],
            'score': interview_data['score'],
            'candidate_name': interview_data['candidate_name'],
            'target_role': interview_data['target_role']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get interview status: {str(e)}'
        }), 500

@app.route('/api/interview/report/<interview_id>')
def get_final_report(interview_id):
    """Generate and return the final interview report"""
    try:
        report = interview_agent.generate_final_report(interview_id)
        
        if 'error' in report:
            return jsonify(report), 404
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to generate report: {str(e)}'
        }), 500

@app.route('/report/<interview_id>')
def view_report(interview_id):
    """View the detailed report page"""
    return render_template('report.html', interview_id=interview_id)

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )
