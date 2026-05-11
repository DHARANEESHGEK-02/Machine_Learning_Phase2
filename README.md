<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Machine Learning Phase 2 - Project Portfolio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            animation: fadeInDown 0.8s ease;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.95;
            animation: fadeInUp 0.8s ease;
        }
        
        .badges {
            margin-top: 20px;
            animation: fadeIn 1s ease;
        }
        
        .badge {
            display: inline-block;
            padding: 8px 16px;
            margin: 5px;
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            font-size: 0.9em;
            text-decoration: none;
            color: white;
            transition: transform 0.3s ease;
        }
        
        .badge:hover {
            transform: translateY(-2px);
            background: rgba(255,255,255,0.3);
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 50px;
        }
        
        .section-title {
            font-size: 2em;
            margin-bottom: 20px;
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            display: inline-block;
        }
        
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }
        
        .project-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }
        
        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        
        .project-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .project-title {
            font-size: 1.5em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .project-description {
            color: #586069;
            margin-bottom: 15px;
        }
        
        .feature-list {
            list-style: none;
            padding-left: 0;
        }
        
        .feature-list li {
            padding: 5px 0;
            padding-left: 25px;
            position: relative;
        }
        
        .feature-list li:before {
            content: "✅";
            position: absolute;
            left: 0;
        }
        
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }
        
        .tech-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
        }
        
        .code-block {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            margin: 15px 0;
        }
        
        .code-block pre {
            margin: 0;
        }
        
        .metrics-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        .metrics-table th,
        .metrics-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e1e4e8;
        }
        
        .metrics-table th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        
        .metrics-table tr:hover {
            background: #f8f9fa;
        }
        
        .button {
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            margin: 10px 5px;
            transition: transform 0.3s ease;
            border: none;
            cursor: pointer;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .demo-link {
            display: inline-block;
            padding: 10px 20px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            margin: 10px 5px;
            transition: transform 0.3s ease;
        }
        
        .demo-link:hover {
            transform: translateY(-2px);
            background: #218838;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-left: 10px;
            background: #28a745;
            color: white;
        }
        
        .footer {
            background: #2d3748;
            color: white;
            text-align: center;
            padding: 30px;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }
            .projects-grid {
                grid-template-columns: 1fr;
            }
            .content {
                padding: 20px;
            }
            .button, .demo-link {
                display: block;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🚀 Machine Learning Phase 2</h1>
            <p><em>Data Science Project Portfolio</em></p>
            <div class="badges">
                <a href="https://github.com/DHARANEESHGEK-02/machine_learning_phase2" class="badge">⭐ GitHub Stars</a>
                <a href="https://github.com/DHARANEESHGEK-02/machine_learning_phase2/network/members" class="badge">🍴 Forks</a>
                <a href="#" class="badge">🐍 Python 3.12</a>
                <a href="#" class="badge">📄 MIT License</a>
            </div>
        </div>
        
        <!-- Content -->
        <div class="content">
            <!-- Overview Section -->
            <div class="section">
                <h2 class="section-title">📊 Overview</h2>
                <p>This repository contains two complete <strong>end-to-end Machine Learning projects</strong> with interactive <strong>Streamlit</strong> web applications. The projects demonstrate real-world applications of <strong>Logistic Regression</strong> for prediction tasks.</p>
                <br>
                <div class="tech-stack">
                    <span class="tech-item">🐍 Python</span>
                    <span class="tech-item">🎨 Streamlit</span>
                    <span class="tech-item">🤖 scikit-learn</span>
                    <span class="tech-item">📊 Pandas</span>
                    <span class="tech-item">📈 Matplotlib</span>
                    <span class="tech-item">🎨 Seaborn</span>
                </div>
            </div>
            
            <!-- Projects Grid -->
            <div class="section">
                <h2 class="section-title">🎯 Live Demos</h2>
                <div class="projects-grid">
                    <!-- Project 1 -->
                    <div class="project-card">
                        <div class="project-icon">🏦</div>
                        <div class="project-title">
                            Insurance Purchase Prediction
                            <span class="status-badge">● Live</span>
                        </div>
                        <div class="project-description">
                            Predicts whether a person will purchase travel insurance based on their age using Logistic Regression.
                        </div>
                        <ul class="feature-list">
                            <li>Real-time age-based predictions</li>
                            <li>Probability scores (0-100%)</li>
                            <li>Custom CSV upload support</li>
                            <li>Adjustable decision threshold</li>
                        </ul>
                        <div style="margin-top: 15px;">
                            <a href="https://dharanees-qdcgwgrxojd27aw9tjw64v.streamlit.app/" target="_blank" class="demo-link">🚀 Launch Live Demo</a>
                            <a href="https://github.com/DHARANEESHGEK-02/machine_learning_phase2/tree/main/Insurance" target="_blank" class="button">📁 View Code</a>
                        </div>
                    </div>
                    
                    <!-- Project 2 -->
                    <div class="project-card">
                        <div class="project-icon">👥</div>
                        <div class="project-title">
                            HR Employee Retention Analytics
                            <span class="status-badge">● Live</span>
                        </div>
                        <div class="project-description">
                            Analyzes employee attrition patterns and predicts which employees are at risk of leaving the company.
                        </div>
                        <ul class="feature-list">
                            <li>Interactive EDA visualizations</li>
                            <li>Custom feature selection</li>
                            <li>Batch predictions for all employees</li>
                            <li>Comprehensive model metrics</li>
                        </ul>
                        <div style="margin-top: 15px;">
                            <a href="https://dharaneesh-xah29pvunn2mzoi5skw8ta.streamlit.app/" target="_blank" class="demo-link">🚀 Launch Live Demo</a>
                            <a href="https://github.com/DHARANEESHGEK-02/machine_learning_phase2/tree/main/HR_Analysis" target="_blank" class="button">📁 View Code</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Model Performance -->
            <div class="section">
                <h2 class="section-title">📈 Model Performance</h2>
                <table class="metrics-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Insurance Model</th>
                            <th>HR Analytics Model</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Algorithm</td><td>Logistic Regression</td><td>Logistic Regression</td></tr>
                        <tr><td>Features</td><td>1 (age)</td><td>3-7 (selectable)</td></tr>
                        <tr><td>Accuracy</td><td>75-85%</td><td>75-80%</td></tr>
                        <tr><td>Precision</td><td>0.82</td><td>0.78</td></tr>
                        <tr><td>Recall</td><td>0.78</td><td>0.76</td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Quick Start -->
            <div class="section">
                <h2 class="section-title">🚀 Quick Start Guide</h2>
                <div class="code-block">
                    <pre># Clone the repository
git clone https://github.com/DHARANEESHGEK-02/machine_learning_phase2.git
cd machine_learning_phase2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies for Insurance App
cd Insurance
pip install -r requirements.txt

# Run the Insurance app
streamlit run insurance.py

# Open new terminal for HR App
cd ../HR_Analysis
pip install -r requirements.txt

# Run the HR Analytics app
streamlit run Hr_analysis.py</pre>
                </div>
            </div>
            
            <!-- Project Structure -->
            <div class="section">
                <h2 class="section-title">📁 Project Structure</h2>
                <div class="code-block">
                    <pre>machine_learning_phase2/
│
├── 📁 Insurance/
│   ├── 📄 insurance.py              # Streamlit app
│   ├── 📓 insurance.ipynb           # Jupyter notebook
│   ├── 📊 insurance_data.csv        # Sample dataset
│   └── 📦 requirements.txt          # Dependencies
│
├── 📁 HR_Analysis/
│   ├── 📄 Hr_analysis.py            # Streamlit app
│   └── 📦 requirements.txt          # Dependencies
│
├── 📁 WorkSpace/                     # Development workspace
├── 📄 README.md                      # Documentation
└── 📄 .gitignore                     # Git ignore rules</pre>
                </div>
            </div>
            
            <!-- App URLs Section -->
            <div class="section">
                <h2 class="section-title">🌐 Application URLs</h2>
                <table class="metrics-table">
                    <thead>
                        <tr><th>Application</th><th>Live Demo URL</th><th>Status</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>🏦 Insurance Prediction App</strong></td>
                            <td><a href="https://dharanees-qdcgwgrxojd27aw9tjw64v.streamlit.app/" target="_blank">https://dharanees-qdcgwgrxojd27aw9tjw64v.streamlit.app/</a></td>
                            <td><span style="color: #28a745;">✅ Active</span></td>
                        </tr>
                        <tr>
                            <td><strong>👥 HR Analytics App</strong></td>
                            <td><a href="https://dharaneesh-xah29pvunn2mzoi5skw8ta.streamlit.app/" target="_blank">https://dharaneesh-xah29pvunn2mzoi5skw8ta.streamlit.app/</a></td>
                            <td><span style="color: #28a745;">✅ Active</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Installation Commands -->
            <div class="section">
                <h2 class="section-title">💻 Installation Commands</h2>
                <div class="code-block">
                    <pre># Insurance App
cd Insurance
pip install -r requirements.txt
streamlit run insurance.py

# HR Analytics App (in another terminal)
cd HR_Analysis
pip install -r requirements.txt
streamlit run Hr_analysis.py</pre>
                </div>
            </div>
            
            <!-- Troubleshooting -->
            <div class="section">
                <h2 class="section-title">🔧 Troubleshooting</h2>
                <table class="metrics-table">
                    <thead>
                        <tr><th>Issue</th><th>Solution</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>❌ ModuleNotFoundError</td><td>Run <code>pip install -r requirements.txt</code></td></tr>
                        <tr><td>❌ File not found</td><td>Ensure CSV file is in correct directory</td></tr>
                        <tr><td>❌ Port already in use</td><td>Use <code>streamlit run app.py --server.port 8502</code></td></tr>
                        <tr><td>❌ Deployment error</td><td>Check logs in Streamlit Cloud dashboard</td></tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Contributing -->
            <div class="section">
                <h2 class="section-title">🤝 Contributing</h2>
                <ol style="margin-left: 20px; line-height: 1.8;">
                    <li>🍴 Fork the repository</li>
                    <li>🌿 Create a feature branch (<code>git checkout -b feature/AmazingFeature</code>)</li>
                    <li>💾 Commit your changes (<code>git commit -m 'Add AmazingFeature'</code>)</li>
                    <li>📤 Push to the branch (<code>git push origin feature/AmazingFeature</code>)</li>
                    <li>🔄 Open a Pull Request</li>
                </ol>
            </div>
            
            <!-- Support -->
            <div class="section">
                <h2 class="section-title">⭐ Support</h2>
                <p>If you find this project useful, please consider giving it a ⭐ on GitHub! Your support helps keep the project maintained and improved.</p>
                <br>
                <a href="https://github.com/DHARANEESHGEK-02/machine_learning_phase2" class="button" style="background: #28a745;">⭐ Star this Repository</a>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Built with ❤️ using Python & Streamlit</p>
            <p>© 2025 Dharaneesh G E K | MIT License</p>
            <div style="margin-top: 15px;">
                <a href="https://github.com/DHARANEESHGEK-02" target="_blank" style="color: white; text-decoration: none; margin: 0 10px;">🐙 GitHub</a>
                <a href="#" style="color: white; text-decoration: none; margin: 0 10px;">💼 LinkedIn</a>
                <a href="#" style="color: white; text-decoration: none; margin: 0 10px;">📧 Email</a>
            </div>
        </div>
    </div>
</body>
</html>
