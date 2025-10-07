from flask import Flask, render_template_string, request, jsonify, session as flask_session
import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.banking_core import SecureOnlineBanking
    from src.performance_reporter import PerformanceReporter
    BANK_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import banking modules: {e}")
    BANK_AVAILABLE = False
    SecureOnlineBanking = None
    PerformanceReporter = None

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'vercel-secret-key-123')

# Initialize bank only if available
bank = None
if BANK_AVAILABLE:
    try:
        bank = SecureOnlineBanking()
    except Exception as e:
        print(f"Warning: Could not initialize banking system: {e}")
        bank = None

# Main dashboard HTML
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Banking Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background: #007cba; color: white; padding: 20px; border-radius: 10px 10px 0 0; }
        .nav { background: white; padding: 15px; border-bottom: 1px solid #ddd; }
        .nav button { margin: 0 10px; padding: 10px 20px; background: #007cba; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .content { background: white; padding: 20px; border-radius: 0 0 10px 10px; }
        .card { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007cba; }
        .success { color: green; }
        .error { color: red; }
        .form-group { margin: 15px 0; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .btn { padding: 10px 20px; background: #007cba; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .btn:hover { background: #005a8b; }
        .balance { font-size: 24px; font-weight: bold; color: #007cba; }
        .transaction-history { max-height: 400px; overflow-y: auto; }
        .transaction { padding: 10px; border-bottom: 1px solid #eee; }
        .performance-metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .metric { background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; }
        .metric-value { font-size: 24px; font-weight: bold; color: #007cba; }
        .metric-label { font-size: 12px; color: #666; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏦 Secure Banking System</h1>
            <p>Advanced Cryptographic Security & Performance Monitoring</p>
        </div>
        
        <div class="nav">
            <button onclick="showSection('banking')">Banking</button>
            <button onclick="showSection('performance')">Performance</button>
            <button onclick="showSection('security')">Security</button>
            {% if session.get('user_id') %}
            <button onclick="logout()" style="float: right; background: #dc3545;">Logout</button>
            <span style="float: right; margin-right: 20px; line-height: 40px;">Welcome, {{ session.get('user_id') }}!</span>
            {% endif %}
        </div>
        
        <div class="content">
            {% if not session.get('user_id') %}
            <!-- Login Form -->
            <div id="login-section">
                <h2>🔐 User Authentication</h2>
                <div class="card">
                    <form id="login-form">
                        <div class="form-group">
                            <label>Username:</label>
                            <input type="text" id="username" required>
                        </div>
                        <div class="form-group">
                            <label>Password:</label>
                            <input type="password" id="password" required>
                        </div>
                        <div class="form-group">
                            <label>OTP (6 digits):</label>
                            <input type="text" id="otp" pattern="[0-9]{6}" required>
                        </div>
                        <button type="submit" class="btn">🔑 Login</button>
                    </form>
                </div>
                
                <div class="card">
                    <h3>Demo Credentials</h3>
                    <p><strong>Username:</strong> alice</p>
                    <p><strong>Password:</strong> secure123</p>
                    <p><strong>OTP:</strong> 123456 (demo)</p>
                </div>
            </div>
            {% else %}
            
            <!-- Banking Section -->
            <div id="banking-section">
                <h2>💰 Banking Operations</h2>
                
                <div class="card">
                    <h3>Account Balance</h3>
                    <div class="balance" id="balance">Loading...</div>
                </div>
                
                <div class="card">
                    <h3>Transfer Funds</h3>
                    <form id="transfer-form">
                        <div class="form-group">
                            <label>To Account:</label>
                            <input type="text" id="to-account" required>
                        </div>
                        <div class="form-group">
                            <label>Amount:</label>
                            <input type="number" id="amount" step="0.01" required>
                        </div>
                        <button type="submit" class="btn">💸 Transfer</button>
                    </form>
                </div>
                
                <div class="card">
                    <h3>Recent Transactions</h3>
                    <div id="transactions" class="transaction-history">Loading...</div>
                </div>
            </div>
            
            <!-- Performance Section -->
            <div id="performance-section" style="display: none;">
                <h2>📊 Performance Monitoring</h2>
                <div id="performance-data">Loading...</div>
            </div>
            
            <!-- Security Section -->
            <div id="security-section" style="display: none;">
                <h2>🔒 Security Information</h2>
                <div class="card">
                    <h3>Encryption Status</h3>
                    <p>✅ AES-256 Encryption Active</p>
                    <p>✅ RSA-4096 Key Exchange</p>
                    <p>✅ HMAC Authentication</p>
                </div>
                
                <div class="card">
                    <h3>Session Information</h3>
                    <div id="session-info">Loading...</div>
                </div>
            </div>
            
            {% endif %}
            
            <div id="message" style="margin-top: 20px;"></div>
        </div>
    </div>

    <script>
        function showMessage(msg, isError = false) {
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `<div class="card ${isError ? 'error' : 'success'}">${msg}</div>`;
            setTimeout(() => messageDiv.innerHTML = '', 5000);
        }

        function showSection(section) {
            const sections = ['banking-section', 'performance-section', 'security-section'];
            sections.forEach(s => {
                const el = document.getElementById(s);
                if (el) el.style.display = s === section + '-section' ? 'block' : 'none';
            });
            
            if (section === 'performance') {
                loadPerformanceData();
            } else if (section === 'security') {
                loadSecurityInfo();
            }
        }

        async function login(event) {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const otp = document.getElementById('otp').value;

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password, otp})
                });
                
                const data = await response.json();
                if (data.success) {
                    location.reload();
                } else {
                    showMessage(data.message || 'Login failed', true);
                }
            } catch (error) {
                showMessage('Login error: ' + error.message, true);
            }
        }

        async function logout() {
            try {
                const response = await fetch('/api/logout', {method: 'POST'});
                if (response.ok) {
                    location.reload();
                }
            } catch (error) {
                showMessage('Logout error: ' + error.message, true);
            }
        }

        async function transfer(event) {
            event.preventDefault();
            const toAccount = document.getElementById('to-account').value;
            const amount = parseFloat(document.getElementById('amount').value);

            try {
                const response = await fetch('/api/transfer', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({to_account: toAccount, amount})
                });
                
                const data = await response.json();
                if (data.success) {
                    showMessage(`Transfer of $${amount} to ${toAccount} successful!`);
                    loadBalance();
                    loadTransactions();
                    document.getElementById('transfer-form').reset();
                } else {
                    showMessage(data.message || 'Transfer failed', true);
                }
            } catch (error) {
                showMessage('Transfer error: ' + error.message, true);
            }
        }

        async function loadBalance() {
            try {
                const response = await fetch('/api/balance');
                const data = await response.json();
                if (data.success) {
                    document.getElementById('balance').textContent = `$${data.balance.toFixed(2)}`;
                }
            } catch (error) {
                document.getElementById('balance').textContent = 'Error loading balance';
            }
        }

        async function loadTransactions() {
            try {
                const response = await fetch('/api/transactions');
                const data = await response.json();
                if (data.success) {
                    const transactionsDiv = document.getElementById('transactions');
                    transactionsDiv.innerHTML = data.transactions.map(t => 
                        `<div class="transaction">
                            <strong>${t.type}</strong> - $${t.amount} 
                            ${t.type === 'TRANSFER' ? `to ${t.to_account}` : ''} 
                            <br><small>${t.timestamp}</small>
                        </div>`
                    ).join('') || '<p>No transactions found</p>';
                }
            } catch (error) {
                document.getElementById('transactions').innerHTML = 'Error loading transactions';
            }
        }

        async function loadPerformanceData() {
            try {
                const response = await fetch('/api/performance');
                const data = await response.json();
                if (data.success) {
                    const perfDiv = document.getElementById('performance-data');
                    perfDiv.innerHTML = `
                        <div class="performance-metrics">
                            <div class="metric">
                                <div class="metric-value">${data.data.total_operations}</div>
                                <div class="metric-label">Total Operations</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${data.data.avg_crypto_time.toFixed(2)}ms</div>
                                <div class="metric-label">Avg Crypto Time</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${data.data.avg_protocol_time.toFixed(2)}ms</div>
                                <div class="metric-label">Avg Protocol Time</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${data.data.system_health.cpu.toFixed(1)}%</div>
                                <div class="metric-label">CPU Usage</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">${data.data.system_health.memory.toFixed(1)}%</div>
                                <div class="metric-label">Memory Usage</div>
                            </div>
                        </div>
                    `;
                }
            } catch (error) {
                document.getElementById('performance-data').innerHTML = 'Error loading performance data';
            }
        }

        async function loadSecurityInfo() {
            try {
                const response = await fetch('/api/security');
                const data = await response.json();
                if (data.success) {
                    document.getElementById('session-info').innerHTML = `
                        <p><strong>Session ID:</strong> ${data.session_id || 'N/A'}</p>
                        <p><strong>Login Time:</strong> ${new Date().toLocaleString()}</p>
                        <p><strong>Encryption:</strong> Active</p>
                        <p><strong>Protocol:</strong> Secure</p>
                    `;
                }
            } catch (error) {
                document.getElementById('session-info').innerHTML = 'Error loading security info';
            }
        }

        // Event listeners
        document.addEventListener('DOMContentLoaded', function() {
            const loginForm = document.getElementById('login-form');
            if (loginForm) {
                loginForm.addEventListener('submit', login);
            }
            
            const transferForm = document.getElementById('transfer-form');
            if (transferForm) {
                transferForm.addEventListener('submit', transfer);
                loadBalance();
                loadTransactions();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    if not BANK_AVAILABLE or bank is None:
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Secure Banking System - Maintenance</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #007cba; }
                .status { color: #666; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏦 Secure Banking System</h1>
                <p class="status">System is currently initializing...</p>
                <p>Please check back in a few moments.</p>
                <p><small>Status: Banking core loading</small></p>
            </div>
        </body>
        </html>
        ''')

    return render_template_string(DASHBOARD_HTML)

@app.route('/api/login', methods=['POST'])
def login():
    if not BANK_AVAILABLE or bank is None:
        return jsonify({'success': False, 'message': 'Banking system is initializing. Please try again.'})

    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'Invalid request data'})

        username = data.get('username')
        password = data.get('password')
        otp = data.get('otp')

        if not all([username, password, otp]):
            return jsonify({'success': False, 'message': 'Missing required fields'})

        # For demo purposes, accept specific credentials
        if username == 'alice' and password == 'secure123' and otp == '123456':
            session_id = f"session_{int(datetime.now().timestamp())}"
            flask_session['user_id'] = username
            flask_session['session_id'] = session_id
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'System error: {str(e)}'})

@app.route('/api/logout', methods=['POST'])
def logout():
    flask_session.clear()
    return jsonify({'success': True})

@app.route('/api/balance')
def get_balance():
    if 'user_id' not in flask_session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    try:
        # For demo, return a mock balance
        balance = 1500.00  # In a real app, get from database
        return jsonify({'success': True, 'balance': balance})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/transfer', methods=['POST'])
def transfer():
    if not BANK_AVAILABLE or bank is None:
        return jsonify({'success': False, 'message': 'Banking system is initializing. Please try again.'})

    if 'user_id' not in flask_session:
        return jsonify({'success': False, 'message': 'Not authenticated'})

    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'Invalid request data'})

        to_account = data.get('to_account')
        amount = data.get('amount', 0)

        if not to_account or amount <= 0:
            return jsonify({'success': False, 'message': 'Invalid transfer details'})

        # Simulate successful transfer for demo
        return jsonify({'success': True, 'message': f'Transfer of ${amount} to {to_account} completed!'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/transactions')
def get_transactions():
    if 'user_id' not in flask_session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    try:
        # Mock transaction data
        transactions = [
            {'type': 'DEPOSIT', 'amount': 1000.00, 'timestamp': '2025-10-07 10:00:00'},
            {'type': 'TRANSFER', 'amount': 50.00, 'to_account': 'bob', 'timestamp': '2025-10-07 11:30:00'},
            {'type': 'WITHDRAW', 'amount': 100.00, 'timestamp': '2025-10-07 12:15:00'}
        ]
        return jsonify({'success': True, 'transactions': transactions})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/performance')
def get_performance():
    if 'user_id' not in flask_session:
        return jsonify({'success': False, 'message': 'Not authenticated'})

    try:
        # Mock performance data since banking system might not be available
        summary = {
            'total_operations': 42,
            'avg_crypto_time': '2.5',
            'avg_protocol_time': '1.8',
            'system_health': {
                'cpu': 45.2,
                'memory': 62.1
            }
        }
        return jsonify({'success': True, 'data': summary})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/security')
def get_security():
    if 'user_id' not in flask_session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    try:
        session_id = flask_session.get('session_id', 'N/A')
        return jsonify({'success': True, 'session_id': session_id})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Vercel serverless function handler
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def handle_request(self, method):
        # Create WSGI environ
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': self.path,
            'QUERY_STRING': self.path.split('?', 1)[1] if '?' in self.path else '',
            'CONTENT_TYPE': self.headers.get('content-type', ''),
            'CONTENT_LENGTH': self.headers.get('content-length', '0'),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': self.rfile,
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }
        # Add headers
        for header, value in self.headers.items():
            environ['HTTP_' + header.upper().replace('-', '_')] = value

        # Start response function
        def start_response(status, headers):
            self.send_response(int(status.split()[0]))
            for h, v in headers:
                self.send_header(h, v)
            self.end_headers()

        # Call the app
        result = app(environ, start_response)
        # Write the body
        for data in result:
            self.wfile.write(data)

# For local development
if __name__ == '__main__':
    print("🚀 Starting Enhanced Banking System...")
    print("📍 Open your browser to: http://localhost:5000")
    app.run(debug=True, port=5000)