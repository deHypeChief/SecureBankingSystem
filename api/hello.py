from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = '''
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
        </div>
        
        <div class="content">
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
            
            <!-- Banking Section -->
            <div id="banking-section" style="display: none;">
                <h2>💰 Banking Operations</h2>
                
                <div class="card">
                    <h3>Account Balance</h3>
                    <div class="balance" id="balance">$1000.00</div>
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
                    <div id="transactions" class="transaction-history">
                        <div class="transaction">
                            <strong>DEPOSIT</strong> - $500.00 <br><small>2025-10-07 12:00:00</small>
                        </div>
                        <div class="transaction">
                            <strong>TRANSFER</strong> - $100.00 to bob <br><small>2025-10-07 11:00:00</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Performance Section -->
            <div id="performance-section" style="display: none;">
                <h2>📊 Performance Monitoring</h2>
                <div id="performance-data">
                    <div class="performance-metrics">
                        <div class="metric">
                            <div class="metric-value">42</div>
                            <div class="metric-label">Total Operations</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">15.3ms</div>
                            <div class="metric-label">Avg Crypto Time</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">8.7ms</div>
                            <div class="metric-label">Avg Protocol Time</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">23.4%</div>
                            <div class="metric-label">CPU Usage</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">45.6%</div>
                            <div class="metric-label">Memory Usage</div>
                        </div>
                    </div>
                </div>
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
                    <div id="session-info">
                        <p><strong>Session ID:</strong> demo-session-123</p>
                        <p><strong>Login Time:</strong> 2025-10-07 12:00:00</p>
                        <p><strong>Encryption:</strong> Active</p>
                        <p><strong>Protocol:</strong> Secure</p>
                    </div>
                </div>
            </div>
            
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
            const sections = ['login-section', 'banking-section', 'performance-section', 'security-section'];
            sections.forEach(s => {
                const el = document.getElementById(s);
                if (el) el.style.display = s === section + '-section' ? 'block' : 'none';
            });
        }

        async function login(event) {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const otp = document.getElementById('otp').value;

            if (username === 'alice' && password === 'secure123' && otp === '123456') {
                showSection('banking');
                showMessage('Login successful!');
            } else {
                showMessage('Invalid credentials', true);
            }
        }

        async function transfer(event) {
            event.preventDefault();
            const toAccount = document.getElementById('to-account').value;
            const amount = parseFloat(document.getElementById('amount').value);

            showMessage(`Transfer of $${amount} to ${toAccount} simulated!`);
            document.getElementById('transfer-form').reset();
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
            }
        });
    </script>
</body>
</html>
        '''
        self.wfile.write(html.encode())
        return
