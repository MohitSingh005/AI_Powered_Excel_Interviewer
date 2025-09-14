"""
Core Interview Agent for Excel Mock Interviewer
Handles conversation flow, state management, and question progression
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import os
from groq import Groq

class InterviewAgent:
    """Main interview agent that manages the entire interview process"""
    
    def __init__(self, groq_api_key: str):
        self.groq_client = Groq(api_key=groq_api_key)
        self.question_bank = self._load_question_bank()
        
    def _load_question_bank(self) -> Dict:
        """Load predefined questions organized by difficulty level"""
        return {
            "basic": [
                "What is the difference between a relative and absolute cell reference in Excel?",
                "How would you use the SUM function to calculate the total of cells A1 through A10?",
                "Explain the purpose of Excel's AutoSum feature and how to use it.",
                "What is the shortcut to copy a cell in Excel?",
                "How do you format a cell to display numbers as currency?"
            ],
            "intermediate": [
                "Explain how VLOOKUP works and provide an example scenario where you'd use it.",
                "What's the difference between VLOOKUP and INDEX-MATCH? When would you use each?",
                "How would you create a pivot table to analyze sales data by region and product?",
                "Describe how to use conditional formatting to highlight cells based on their values.",
                "What is the COUNTIF function and how would you use it to count cells meeting specific criteria?"
            ],
            "advanced": [
                "How would you create a nested IF statement with multiple conditions?",
                "Explain array formulas in Excel and provide an example of when you'd use them.",
                "How would you use Excel's Goal Seek feature for what-if analysis?",
                "Describe how to create and use named ranges in formulas.",
                "What are Excel macros and how would you create a simple macro to automate a task?"
            ]
        }
    
    def start_interview(self, candidate_name: str, target_role: str, experience_level: str) -> Dict:
        """Initialize a new interview session"""
        interview_id = str(uuid.uuid4())
        
        interview_data = {
            "id": interview_id,
            "candidate_name": candidate_name,
            "target_role": target_role,
            "experience_level": experience_level,
            "status": "started",
            "current_phase": "introduction",
            "current_difficulty": "basic",
            "question_count": 0,
            "score": 0,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "end_time": None,
            "messages": [],
            "evaluations": []
        }
        
        # Save interview data
        self._save_interview_data(interview_data)
        
        # Generate welcome message
        welcome_message = self._generate_welcome_message(candidate_name, target_role)
        
        return {
            "interview_id": interview_id,
            "message": welcome_message,
            "status": "started"
        }
    
    def _generate_welcome_message(self, candidate_name: str, target_role: str) -> str:
        """Generate personalized welcome message"""
        return f"""Hello {candidate_name}! 👋

Welcome to the AI-Powered Excel Mock Interviewer. I'm here to assess your Excel skills for the {target_role} position.

**How this works:**
• I'll ask you a series of Excel-related questions
• Questions will progress from basic to advanced based on your performance
• Please explain your answers thoroughly - I'm evaluating both technical knowledge and communication
• The interview will take about 15-20 minutes

**What I'm looking for:**
• Technical accuracy of Excel concepts
• Practical application knowledge
• Clear communication of your thought process
• Best practices awareness

Are you ready to begin? Just type "yes" or "ready" when you're set to start!"""

    def process_message(self, interview_id: str, user_message: str) -> Dict:
        """Process user message and generate appropriate response"""
        interview_data = self._load_interview_data(interview_id)
        
        if not interview_data:
            return {"error": "Interview not found"}
        
        # Add user message to conversation
        interview_data["messages"].append({
            "role": "candidate",
            "content": user_message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        # Process based on current phase
        if interview_data["current_phase"] == "introduction":
            response = self._handle_introduction(interview_data, user_message)
        elif interview_data["current_phase"] == "assessment":
            response = self._handle_assessment(interview_data, user_message)
        else:
            response = self._handle_conclusion(interview_data)
        
        # Add response to conversation
        interview_data["messages"].append({
            "role": "interviewer",
            "content": response["message"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        # Update interview data
        interview_data.update(response.get("interview_updates", {}))
        self._save_interview_data(interview_data)
        
        return response
    
    def _handle_introduction(self, interview_data: Dict, user_message: str) -> Dict:
        """Handle introduction phase responses"""
        if any(word in user_message.lower() for word in ["yes", "ready", "start", "begin"]):
            # Move to assessment phase
            question = self._get_next_question(interview_data)
            
            return {
                "message": f"Perfect! Let's start with our first question:\n\n**Question 1:** {question}",
                "interview_updates": {
                    "current_phase": "assessment",
                    "question_count": 1
                }
            }
        else:
            return {
                "message": "No worries! Take your time. When you're ready to begin the Excel assessment, just let me know by typing 'ready' or 'yes'."
            }
    
    def _handle_assessment(self, interview_data: Dict, user_message: str) -> Dict:
        """Handle assessment phase - evaluate answer and ask next question"""
        # Evaluate the current answer
        evaluation = self._evaluate_answer(interview_data, user_message)
        interview_data["evaluations"].append(evaluation)
        
        # Update score
        interview_data["score"] += evaluation["points"]
        
        # Determine if we should continue or conclude
        question_count = interview_data["question_count"]
        
        if question_count >= 8 or self._should_conclude_interview(interview_data):
            # Move to conclusion
            return {
                "message": f"Thank you for that answer! I have enough information to provide you with feedback.\n\nLet me generate your performance report...",
                "interview_updates": {
                    "current_phase": "conclusion",
                    "end_time": datetime.now(timezone.utc).isoformat(),
                    "status": "completed"
                }
            }
        else:
            # Ask next question
            next_question = self._get_next_question(interview_data)
            feedback = self._generate_brief_feedback(evaluation)
            
            return {
                "message": f"{feedback}\n\n**Question {question_count + 1}:** {next_question}",
                "interview_updates": {
                    "question_count": question_count + 1
                }
            }
    
    def _evaluate_answer(self, interview_data: Dict, answer: str) -> Dict:
        """Use AI to evaluate the candidate's answer"""
        current_question = self._get_current_question(interview_data)
        difficulty = interview_data["current_difficulty"]
        
        evaluation_prompt = f"""
        You are an expert Excel interviewer evaluating a candidate's response. 
        
        Question: {current_question}
        Difficulty Level: {difficulty}
        Candidate's Answer: {answer}
        
        Evaluate this answer on a scale of 0-10 based on:
        1. Technical Accuracy (40%)
        2. Practical Application (30%) 
        3. Communication Clarity (20%)
        4. Advanced Knowledge (10%)
        
        Respond with JSON format:
        {{
            "score": <0-10>,
            "points": <0-15>,
            "technical_accuracy": <0-10>,
            "practical_application": <0-10>,
            "communication": <0-10>,
            "advanced_knowledge": <0-10>,
            "feedback": "<detailed feedback>",
            "strengths": ["<strength1>", "<strength2>"],
            "improvements": ["<improvement1>", "<improvement2>"]
        }}
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": evaluation_prompt}],
                model="llama-3.1-70b-versatile",
                temperature=0.3,
                max_tokens=1000
            )
            
            evaluation_text = response.choices[0].message.content
            # Extract JSON from response
            json_start = evaluation_text.find('{')
            json_end = evaluation_text.rfind('}') + 1
            evaluation_json = evaluation_text[json_start:json_end]
            
            evaluation = json.loads(evaluation_json)
            evaluation["question"] = current_question
            evaluation["answer"] = answer
            
            return evaluation
            
        except Exception as e:
            # Fallback evaluation if AI fails
            return {
                "score": 5,
                "points": 7,
                "technical_accuracy": 5,
                "practical_application": 5,
                "communication": 5,
                "advanced_knowledge": 5,
                "feedback": "Unable to provide detailed feedback due to technical issue.",
                "strengths": ["Provided a response"],
                "improvements": ["Could provide more detail"],
                "question": current_question,
                "answer": answer,
                "error": str(e)
            }
    
    def _get_current_question(self, interview_data: Dict) -> str:
        """Get the current question being asked"""
        messages = interview_data["messages"]
        for message in reversed(messages):
            if message["role"] == "interviewer" and "Question" in message["content"]:
                # Extract question from message
                content = message["content"]
                if "**Question" in content:
                    question_part = content.split("**Question")[1]
                    if "**" in question_part:
                        return question_part.split("**")[0].split(":", 1)[1].strip()
        return "Previous question not found"
    
    def _get_next_question(self, interview_data: Dict) -> str:
        """Get the next question based on performance"""
        difficulty = self._determine_next_difficulty(interview_data)
        interview_data["current_difficulty"] = difficulty
        
        questions = self.question_bank[difficulty]
        question_count = interview_data["question_count"]
        
        # Cycle through questions or use AI to generate new ones
        if question_count < len(questions):
            return questions[question_count % len(questions)]
        else:
            return self._generate_adaptive_question(interview_data, difficulty)
    
    def _determine_next_difficulty(self, interview_data: Dict) -> str:
        """Determine the next question difficulty based on performance"""
        if not interview_data["evaluations"]:
            return "basic"
        
        recent_scores = [eval["score"] for eval in interview_data["evaluations"][-3:]]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        if avg_score >= 8:
            return "advanced"
        elif avg_score >= 6:
            return "intermediate"
        else:
            return "basic"
    
    def _generate_adaptive_question(self, interview_data: Dict, difficulty: str) -> str:
        """Generate a new question using AI based on previous performance"""
        previous_questions = [eval["question"] for eval in interview_data["evaluations"]]
        
        prompt = f"""
        Generate a {difficulty}-level Excel interview question. 
        
        Difficulty: {difficulty}
        Previous questions asked: {previous_questions}
        
        Requirements:
        - Focus on practical Excel skills for {interview_data["target_role"]}
        - Don't repeat previous questions
        - Should be answerable in 2-3 sentences
        - Be specific and actionable
        
        Return only the question, no additional text.
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-70b-versatile",
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except:
            # Fallback to predefined questions
            return self.question_bank[difficulty][0]
    
    def _generate_brief_feedback(self, evaluation: Dict) -> str:
        """Generate brief feedback for the candidate"""
        score = evaluation["score"]
        if score >= 8:
            return "✅ Excellent answer! You demonstrate strong Excel knowledge."
        elif score >= 6:
            return "👍 Good answer! You show solid understanding."
        elif score >= 4:
            return "👌 Decent answer, but there's room for improvement."
        else:
            return "💡 I see some gaps we can work on. Let's continue."
    
    def _should_conclude_interview(self, interview_data: Dict) -> bool:
        """Determine if the interview should be concluded"""
        # Conclude after 8 questions or if performance is consistently very low/high
        evaluations = interview_data["evaluations"]
        if len(evaluations) >= 5:
            recent_scores = [eval["score"] for eval in evaluations[-3:]]
            avg_score = sum(recent_scores) / len(recent_scores)
            
            # If consistently scoring very high or very low, can conclude early
            if avg_score >= 9 or avg_score <= 3:
                return True
        
        return False
    
    def generate_final_report(self, interview_id: str) -> Dict:
        """Generate comprehensive final performance report"""
        interview_data = self._load_interview_data(interview_id)
        
        if not interview_data or not interview_data["evaluations"]:
            return {"error": "No evaluation data found"}
        
        # Calculate overall metrics
        evaluations = interview_data["evaluations"]
        total_score = sum(eval["score"] for eval in evaluations)
        avg_score = total_score / len(evaluations)
        total_points = interview_data["score"]
        max_possible_points = len(evaluations) * 10
        percentage_score = (total_points / max_possible_points) * 100 if max_possible_points > 0 else 0
        
        # Generate detailed report using AI
        report_prompt = f"""
        Generate a comprehensive Excel interview performance report.
        
        Candidate: {interview_data["candidate_name"]}
        Role: {interview_data["target_role"]}
        Questions Asked: {len(evaluations)}
        Average Score: {avg_score:.1f}/10
        Total Points: {total_points}/{max_possible_points}
        Percentage: {percentage_score:.1f}%
        
        Detailed Evaluations:
        {json.dumps([{"question": e["question"], "answer": e["answer"], "score": e["score"], "feedback": e["feedback"]} for e in evaluations], indent=2)}
        
        Create a professional report with:
        1. Overall Performance Summary
        2. Skill Level Assessment (Basic/Intermediate/Advanced)
        3. Strengths and Areas for Improvement
        4. Specific Recommendations
        5. Hiring Recommendation (Strong Hire/Hire/No Hire)
        
        Format as structured text, not JSON.
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": report_prompt}],
                model="llama-3.1-70b-versatile",
                temperature=0.3,
                max_tokens=1500
            )
            
            detailed_report = response.choices[0].message.content
            
        except Exception as e:
            detailed_report = f"Unable to generate detailed report due to technical issue: {str(e)}"
        
        return {
            "interview_id": interview_id,
            "candidate_name": interview_data["candidate_name"],
            "target_role": interview_data["target_role"],
            "overall_score": avg_score,
            "percentage_score": percentage_score,
            "total_points": total_points,
            "max_points": max_possible_points,
            "questions_answered": len(evaluations),
            "interview_duration": self._calculate_duration(interview_data),
            "detailed_report": detailed_report,
            "skill_breakdown": self._calculate_skill_breakdown(evaluations),
            "evaluations": evaluations
        }
    
    def _calculate_skill_breakdown(self, evaluations: List[Dict]) -> Dict:
        """Calculate breakdown of different skill areas"""
        if not evaluations:
            return {}
        
        skill_totals = {
            "technical_accuracy": sum(e.get("technical_accuracy", 0) for e in evaluations) / len(evaluations),
            "practical_application": sum(e.get("practical_application", 0) for e in evaluations) / len(evaluations),
            "communication": sum(e.get("communication", 0) for e in evaluations) / len(evaluations),
            "advanced_knowledge": sum(e.get("advanced_knowledge", 0) for e in evaluations) / len(evaluations)
        }
        
        return skill_totals
    
    def _calculate_duration(self, interview_data: Dict) -> str:
        """Calculate interview duration"""
        try:
            start_time = datetime.fromisoformat(interview_data["start_time"])
            end_time = datetime.fromisoformat(interview_data["end_time"]) if interview_data["end_time"] else datetime.now(timezone.utc)
            duration = end_time - start_time
            
            minutes = int(duration.total_seconds() / 60)
            seconds = int(duration.total_seconds() % 60)
            
            return f"{minutes}m {seconds}s"
        except:
            return "Unknown"
    
    def _save_interview_data(self, interview_data: Dict):
        """Save interview data to file"""
        os.makedirs("data", exist_ok=True)
        filepath = f"data/interview_{interview_data['id']}.json"
        with open(filepath, 'w') as f:
            json.dump(interview_data, f, indent=2)
    
    def _load_interview_data(self, interview_id: str) -> Optional[Dict]:
        """Load interview data from file"""
        filepath = f"data/interview_{interview_id}.json"
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None