const API_URL = "https://miniproject-3-u7zr.onrender.com/api";

// Hamburger Menu Functionality
function toggleMenu() {
    const navMenu = document.getElementById('navMenu');
    const hamburger = document.querySelector('.hamburger');
    
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
    if (hamburger) {
        hamburger.classList.toggle('active');
    }
}

function closeMenu() {
    const navMenu = document.getElementById('navMenu');
    const hamburger = document.querySelector('.hamburger');
    
    if (navMenu) {
        navMenu.classList.remove('active');
    }
    if (hamburger) {
        hamburger.classList.remove('active');
    }
}

// Close menu when clicking outside
document.addEventListener('click', (event) => {
    const navbar = document.querySelector('.navbar');
    if (navbar && !navbar.contains(event.target)) {
        closeMenu();
    }
});

// Close menu on window resize (for desktop view)
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        closeMenu();
    }
});

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.nav-link').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
    
    // Find and mark the clicked button as active
    const clickedBtn = document.querySelector(`.nav-link[onclick*="${tabName}"]`);
    if (clickedBtn) {
        clickedBtn.classList.add('active');
    }
    
    // Close menu on mobile
    if (window.innerWidth <= 768) {
        closeMenu();
    }
}

function showLoading(elementId, show) {
    const element = document.getElementById(elementId);
    if (show) {
        element.classList.add('show');
        element.innerHTML = '<div class="spinner"></div><p>⏳ Processing (10-20 seconds)...</p>';
    } else {
        element.classList.remove('show');
    }
}

function showAlert(elementId, message) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.classList.add('show');
}

function hideAlerts(tabName) {
    document.getElementById(tabName + 'Success').classList.remove('show');
    document.getElementById(tabName + 'Error').classList.remove('show');
}

function displayResult(elementId, data, role = '') {
    const resultElement = document.getElementById(elementId);
    resultElement.innerHTML = '<div class="result">' + data + '</div>';
    
    if (role) {
        const downloadBtn = document.createElement('button');
        downloadBtn.className = 'download-btn';
        downloadBtn.textContent = '📥 Download as Text';
        downloadBtn.onclick = () => downloadAsText(data, role);
        resultElement.appendChild(downloadBtn);
    }
}

function downloadAsText(data, role) {
    const element = document.createElement("a");
    element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(data));
    element.setAttribute("download", `roadmap_${role.replace(/ /g, '_')}.txt`);
    element.style.display = "none";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

async function generateRoadmap(e) {
    e.preventDefault();
    const role = document.getElementById('role').value;
    const experience = document.getElementById('experience').value;
    const timeline = parseInt(document.getElementById('timeline').value);
    const learning = document.getElementById('learning').value;

    if (!role) {
        showAlert('roadmapError', '❌ Please select a role');
        return;
    }

    showLoading('roadmapLoading', true);
    hideAlerts('roadmap');

    try {
        const response = await fetch(`${API_URL}/roadmap/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                role: role,
                experience_level: experience,
                timeline_weeks: timeline,
                learning_style: learning
            })
        });

        if (!response.ok) throw new Error('Failed to generate roadmap');
        const data = await response.json();

        showLoading('roadmapLoading', false);
        showAlert('roadmapSuccess', '✅ Roadmap generated successfully!');
        displayResult('roadmapResult', data.data, role);
    } catch (error) {
        showLoading('roadmapLoading', false);
        showAlert('roadmapError', '❌ Error: ' + error.message);
    }
}

async function analyzeResume(e) {
    e.preventDefault();
    const resumeFile = document.getElementById('resumeFile').files[0];
    const resumeText = document.getElementById('resumeText').value;
    const jobRole = document.getElementById('jobRole').value;

    if (!resumeFile && !resumeText) {
        showAlert('resumeError', '❌ Please upload or paste a resume');
        return;
    }

    showLoading('resumeLoading', true);
    hideAlerts('resume');

    try {
        let finalText = resumeText;

        if (resumeFile) {
            const formData = new FormData();
            formData.append('file', resumeFile);
            const uploadResponse = await fetch(`${API_URL}/resume/upload`, {
                method: 'POST',
                body: formData
            });

            if (!uploadResponse.ok) throw new Error('Failed to upload resume');
            const uploadData = await uploadResponse.json();
            finalText = uploadData.data;
        }

        const response = await fetch(`${API_URL}/resume/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_text: finalText,
                job_role: jobRole
            })
        });

        if (!response.ok) throw new Error('Failed to analyze resume');
        const data = await response.json();

        showLoading('resumeLoading', false);
        showAlert('resumeSuccess', '✅ Analysis complete!');
        displayResult('resumeResult', data.data);
    } catch (error) {
        showLoading('resumeLoading', false);
        showAlert('resumeError', '❌ Error: ' + error.message);
    }
}

async function generateInterview(e) {
    e.preventDefault();
    const resumeFile = document.getElementById('interviewResume').files[0];
    const resumeText = document.getElementById('interviewText').value;
    const role = document.getElementById('interviewRole').value;
    const difficulty = document.getElementById('difficulty').value;

    if (!resumeFile && !resumeText) {
        showAlert('interviewError', '❌ Please upload or paste a resume');
        return;
    }

    showLoading('interviewLoading', true);
    hideAlerts('interview');

    try {
        let finalText = resumeText;

        if (resumeFile) {
            const formData = new FormData();
            formData.append('file', resumeFile);
            const uploadResponse = await fetch(`${API_URL}/resume/upload`, {
                method: 'POST',
                body: formData
            });

            if (!uploadResponse.ok) throw new Error('Failed to upload resume');
            const uploadData = await uploadResponse.json();
            finalText = uploadData.data;
        }

        const response = await fetch(`${API_URL}/interview/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_text: finalText,
                job_role: role,
                difficulty: difficulty
            })
        });

        if (!response.ok) throw new Error('Failed to generate interview');
        const data = await response.json();

        showLoading('interviewLoading', false);
        showAlert('interviewSuccess', '✅ Interview questions generated!');
        displayResult('interviewResult', data.data);
        document.getElementById('feedbackSection').style.display = 'block';
    } catch (error) {
        showLoading('interviewLoading', false);
        showAlert('interviewError', '❌ Error: ' + error.message);
    }
}

async function getFeedback() {
    const answer = document.getElementById('userAnswer').value;

    if (!answer) {
        showAlert('interviewError', '❌ Please provide an answer');
        return;
    }

    showLoading('feedbackLoading', true);

    try {
        const response = await fetch(`${API_URL}/interview/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                answer: answer
            })
        });

        if (!response.ok) throw new Error('Failed to get feedback');
        const data = await response.json();

        showLoading('feedbackLoading', false);
        displayResult('feedbackResult', data.data);
    } catch (error) {
        showLoading('feedbackLoading', false);
        showAlert('interviewError', '❌ Error: ' + error.message);
    }
}
