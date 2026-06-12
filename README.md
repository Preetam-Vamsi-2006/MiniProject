# 🚀 Career Roadmap AI

An intelligent, all-in-one career development platform powered by Google's Gemini API. Generate personalized learning roadmaps, analyze resumes, and practice mock interviews—all in one beautiful application.

## ✨ Features

### 🎯 Career Roadmap Generator
- Select from 12+ career roles
- Customize learning timeline (4-52 weeks)
- Choose experience level (Beginner/Intermediate/Advanced)
- Select learning style (mixed/video/reading/hands-on/interactive)
- Get detailed week-by-week roadmap with:
  - Prerequisites and milestones
  - Resources and tutorials
  - Real-world projects
  - Skills to gain
  - Estimated salary range
- Download roadmap as text file

### 📄 Resume Analyzer
- Upload PDF or DOCX resume files
- Or paste resume text directly
- Optional target job role selection
- Get comprehensive AI analysis:
  - Overall assessment
  - ATS compatibility score (0-100%)
  - Key skills identified
  - Missing skills or experience
  - Specific improvement recommendations
  - Interview readiness score

### 🎤 Mock Interview Tool
- Select job role and difficulty level
- Three difficulty levels: Easy, Medium, Hard
- Upload resume (PDF/DOCX) or paste text
- Get 5 AI-generated interview questions based on your resume
- Answer questions and receive detailed AI feedback
- Get rating and specific improvement suggestions

### 🎨 Attractive UI
- Beautiful gradient background with animated particles
- Smooth animations and transitions
- Responsive design for all devices
- Hamburger menu for mobile navigation
- Modern glass-morphism effects
- 3D particle system (optimized for mobile)

## 🛠️ Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Beautiful styling with gradients and animations
- **Vanilla JavaScript** - No frameworks, pure performance
- **Canvas API** - 3D particle effects
- **Responsive Design** - Mobile-first approach

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.9+** - Language
- **Google Gemini API** - Advanced AI capabilities
- **PyPDF2** - PDF processing
- **python-docx** - DOCX file processing

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js (optional, for local development)
- Google Gemini API key
- Modern web browser

## 🚀 Quick Start

### Local Development

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/career-roadmap-ai.git
cd career-roadmap-ai
```

#### 2. Setup Backend

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
```

#### 3. Run Backend
```bash
python backend_main.py
```
Backend will run on `http://localhost:8000`

#### 4. Open Frontend

**Option A: Direct**
- Open `index.html` in your browser

**Option B: Local Server**
```bash
# Python
python -m http.server 8001

# Or Node.js
npx http-server
```
Then navigate to `http://localhost:8001`

## 📁 Project Structure

```
career-roadmap-ai/
├── backend_main.py           # FastAPI backend
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not pushed to Git)
├── .env.example              # Example env variables
├── .gitignore                # Git ignore rules
│
├── index.html                # Main HTML file
├── style.css                 # CSS styling
├── script.js                 # Frontend JavaScript
├── particle.js               # 3D particle system
│
├── README.md                 # This file
├── DEPLOYMENT_GUIDE.md       # Deployment instructions
└── COMPLETE_SETUP.md         # Detailed setup guide
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

Get your Gemini API key from: https://aistudio.google.com/app/apikey

### API URL Configuration

In `script.js`, update the API URL:

```javascript
// For local development
const API_URL = "http://localhost:8000/api";

// For production (Render)
const API_URL = "https://your-backend-url.onrender.com/api";
```

## 📚 API Endpoints

### Health Check
- `GET /health` - Check if backend is running
- `GET /` - Welcome message

### Career Roadmap
- `POST /api/roadmap/generate` - Generate career roadmap

**Request:**
```json
{
  "role": "Data Scientist",
  "experience_level": "Beginner",
  "timeline_weeks": 12,
  "learning_style": "mixed"
}
```

### Resume Analysis
- `POST /api/resume/analyze` - Analyze resume
- `POST /api/resume/upload` - Upload and extract resume (PDF/DOCX)

**Request:**
```json
{
  "resume_text": "Your resume content...",
  "job_role": "Data Scientist"
}
```

### Mock Interview
- `POST /api/interview/generate` - Generate interview questions
- `POST /api/interview/feedback` - Get feedback on answer

**Request:**
```json
{
  "resume_text": "Your resume content...",
  "job_role": "Data Scientist",
  "difficulty": "Medium"
}
```

## 🌐 Deployment

### Backend on Render
1. Push code to GitHub
2. Create Web Service on Render
3. Connect repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python backend_main.py`
6. Add environment variable: `GEMINI_API_KEY=your_key`
7. Deploy!

### Frontend on Vercel
1. Push code to GitHub
2. Import project on Vercel
3. Configure root directory (if needed)
4. Deploy!

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed instructions.

## 🎯 Supported Career Roles

- Data Scientist
- AI Engineer
- DevOps Engineer
- Full Stack Python Developer
- Full Stack Java Developer
- Data Analyst
- Machine Learning Engineer
- Cloud Architect
- Backend Developer
- Frontend Developer
- Mobile Developer
- Security Engineer

## 🔒 Security

- ✅ API keys stored in environment variables
- ✅ `.env` file excluded from Git
- ✅ No sensitive data in frontend
- ✅ CORS enabled for safe cross-origin requests
- ✅ Input validation on all endpoints

## 🐛 Troubleshooting

### Backend Issues

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"GEMINI_API_KEY not found"**
- Ensure `.env` file exists with your API key
- Check file name is exactly `.env`

**"Connection refused"**
- Verify backend is running: `python backend_main.py`
- Check port 8000 is available

### Frontend Issues

**"API calls failing"**
- Verify backend URL in `script.js`
- Check browser console for errors
- Ensure CORS is enabled

**"Particles not visible"**
- Check browser console
- Ensure JavaScript is enabled
- Try refreshing page

**"Resume upload fails"**
- Ensure file is PDF or DOCX
- Check file size (under 10MB recommended)
- Verify backend is running

## 📊 Performance

- **Career Roadmap Generation**: 15-30 seconds
- **Resume Analysis**: 10-20 seconds
- **Interview Questions**: 15-30 seconds
- **Feedback on Answer**: 10-15 seconds
- **App Load Time**: < 1 second
- **Memory Usage**: ~50MB

## 🎓 Learning Resources

This project demonstrates:
- ✅ FastAPI backend development
- ✅ RESTful API design
- ✅ Frontend-backend integration
- ✅ File upload processing
- ✅ AI API integration (Gemini)
- ✅ Responsive web design
- ✅ Canvas animations
- ✅ Environment variable management

## 🚀 Future Enhancements

- [ ] User authentication and profiles
- [ ] Save roadmaps and progress
- [ ] Real job board integration
- [ ] Video tutorials
- [ ] Salary negotiation guides
- [ ] Community features
- [ ] Mobile app version
- [ ] Multiple language support
- [ ] Certificate generation
- [ ] Progress tracking

## 📝 License

MIT License - feel free to use this project for personal or commercial use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💬 Support

If you encounter any issues:
1. Check the [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
2. Check the [COMPLETE_SETUP.md](./COMPLETE_SETUP.md)
3. Review the troubleshooting section above
4. Create an issue on GitHub

## 👨‍💻 Author

Created with ❤️ for career builders everywhere

## 🙏 Acknowledgments

- **Google Gemini API** - For powerful AI capabilities
- **FastAPI** - For amazing web framework
- **Vercel** - For frontend hosting
- **Render** - For backend hosting

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2024

**Start your career journey today!** 🚀

[Live Demo](https://career-roadmap-ai.vercel.app) | [Backend API](https://your-backend-url.onrender.com)
