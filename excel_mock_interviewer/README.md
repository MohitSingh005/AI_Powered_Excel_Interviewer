# AI-Powered Excel Mock Interviewer

An intelligent web application that conducts automated Excel skill assessments using AI-powered conversation and evaluation. Perfect for companies looking to streamline their technical interview process for Finance, Operations, and Data Analytics roles.

![Demo](https://via.placeholder.com/800x400?text=AI+Excel+Mock+Interviewer+Demo)

## 🌟 Features

- **Conversational AI Interface**: Natural chat-based interview experience
- **Adaptive Questioning**: Dynamic difficulty adjustment based on performance
- **Intelligent Evaluation**: AI-powered answer assessment with detailed feedback
- **Comprehensive Reporting**: Detailed performance analysis with skill breakdowns
- **Multi-Role Support**: Tailored questions for different job roles
- **Real-time Feedback**: Immediate responses and progress tracking
- **Professional Reports**: Printable PDF-ready performance summaries

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend │    │  Flask Backend  │    │   Groq API      │
│                 │◄──►│                 │◄──►│                 │
│ - Chat UI       │    │ - Interview     │    │ - Evaluation    │
│ - Progress      │    │   Engine        │    │ - Question Gen  │
│ - Results       │    │ - State Mgmt    │    │ - Feedback      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Data Storage   │
                       │                 │
                       │ - Sessions      │
                       │ - Transcripts   │
                       │ - Results       │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Free Groq API key (sign up at [console.groq.com](https://console.groq.com))
- Internet connection

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd excel_mock_interviewer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the template
   cp .env.template .env
   
   # Edit .env and add your API key
   GROQ_API_KEY=your_groq_api_key_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Required: Get your free API key from https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Optional: Flask configuration
FLASK_DEBUG=True
FLASK_SECRET_KEY=your_secret_key_here
PORT=5000
```

### Getting a Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

**Note**: Groq offers generous free tier limits perfect for this application.

## 📖 How It Works

### Interview Flow

1. **Setup Phase**: Candidate enters name, target role, and experience level
2. **Introduction**: AI interviewer explains the process and expectations
3. **Assessment Phase**: Progressive questioning with real-time evaluation
4. **Conclusion**: Comprehensive performance report generation

### Evaluation Criteria

Each answer is evaluated on four dimensions:

- **Technical Accuracy (40%)**: Correctness of Excel concepts and syntax
- **Practical Application (30%)**: Real-world scenario handling
- **Communication (20%)**: Clarity and structure of explanations
- **Advanced Knowledge (10%)**: Best practices and optimization awareness

### Question Difficulty Levels

- **Basic**: Interface, basic formulas, cell references
- **Intermediate**: VLOOKUP, pivot tables, conditional formatting
- **Advanced**: Complex formulas, macros, data modeling

## 🎯 Supported Job Roles

- Financial Analyst
- Data Analyst
- Operations Analyst
- Business Analyst
- Accountant
- Other (customizable)

## 📊 Sample Interview Report

The system generates comprehensive reports including:

- Overall performance score and breakdown
- Skill area analysis (radar chart)
- Question-by-question review
- Detailed feedback and recommendations
- Hiring recommendation

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production Deployment

#### Option 1: Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
heroku config:set GROQ_API_KEY=your_key_here
```

#### Option 2: Railway
```bash
# Connect your GitHub repo to Railway
# Add environment variables in Railway dashboard
```

#### Option 3: Render
```bash
# Connect GitHub repo to Render
# Add environment variables in Render dashboard
```

## 🧪 Testing

### Manual Testing

1. Start the application
2. Fill out the interview form
3. Go through a complete interview
4. Check the generated report

### Sample Test Answers

**Question**: "What is the difference between relative and absolute cell references?"

**Good Answer**: "Relative references like A1 change when copied, while absolute references like $A$1 stay fixed. Mixed references like $A1 or A$1 fix either column or row."

**Poor Answer**: "One stays the same and one changes."

## 📁 Project Structure

```
excel_mock_interviewer/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.template         # Environment variables template
├── DESIGN.md            # System design document
├── README.md            # This file
├── app/
│   └── interview_agent.py # Core interview logic
├── templates/
│   ├── index.html       # Main interview interface
│   └── report.html      # Report display page
├── data/                # Interview data storage
├── sample_interviews/   # Example interview transcripts
└── static/             # CSS/JS assets (if needed)
```

## 🔌 API Endpoints

- `GET /` - Main interview interface
- `POST /api/interview/start` - Initialize interview session
- `POST /api/interview/message` - Send candidate message
- `GET /api/interview/status/<id>` - Get interview status
- `GET /api/interview/report/<id>` - Generate final report
- `GET /report/<id>` - View detailed report page

## 🤖 AI Model Configuration

The system uses Groq's Llama-3.1-70b-versatile model with the following configuration:

- **Temperature**: 0.3 (for consistent evaluations)
- **Max Tokens**: 1000-1500 depending on task
- **Model**: llama-3.1-70b-versatile
- **Rate Limits**: Generous free tier (check Groq documentation)

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Groq API key is correctly set in `.env`
2. **Module Not Found**: Make sure you've activated the virtual environment
3. **Port Already in Use**: Change the PORT in `.env` or kill the existing process
4. **Interview Not Loading**: Check browser console for JavaScript errors

### Debug Mode

Enable debug mode for detailed error messages:
```env
FLASK_DEBUG=True
```

## 🚦 Performance Considerations

- **Response Time**: Typically 2-5 seconds per AI evaluation
- **Concurrent Users**: Depends on your Groq API rate limits
- **Storage**: JSON files for simplicity (easily migrated to database)
- **Scalability**: Stateless design allows easy horizontal scaling

## 🔐 Security Notes

- API keys are stored in environment variables
- No sensitive data is logged
- Session data is stored locally
- HTTPS recommended for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: Create a GitHub issue
- **Questions**: Use GitHub Discussions
- **Email**: [Your contact email]

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Enhanced reporting and UI improvements
- **v1.2.0** - Additional question types and role support

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Video/audio interview capability
- [ ] Integration with ATS systems
- [ ] Advanced analytics dashboard
- [ ] Bulk candidate processing
- [ ] Custom question bank editor

---

**Built with ❤️ using Flask, Groq AI, and modern web technologies.**