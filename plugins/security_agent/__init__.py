from core.plugin_interface import PluginInterface
import json
import os
import re
import hashlib
from datetime import datetime

class SecurityHardeningAgent(PluginInterface):
    def __init__(self):
        self.name = "SecuBot"
        self.role = "Security Hardening Agent"
        self.description = "Inspects the system for vulnerabilities and provides security recommendations"
        self.vulnerability_db = self.load_vulnerability_patterns()
        self.scan_results = []
    
    def run(self):
        print(f"🤖 {self.name} ({self.role}) is starting security scan...")
        
        # Perform comprehensive security scan
        scan_results = self.perform_security_scan()
        self.generate_security_report(scan_results)
        
        print(f"✅ {self.name} completed security analysis")
        return scan_results
    
    def load_vulnerability_patterns(self):
        """Load known vulnerability patterns and signatures"""
        return {
            "hardcoded_secrets": [
                r'password\s*=\s*["\'][^"\']{1,}["\']',
                r'api_key\s*=\s*["\'][^"\']{10,}["\']',
                r'secret\s*=\s*["\'][^"\']{1,}["\']',
                r'token\s*=\s*["\'][^"\']{10,}["\']'
            ],
            "insecure_functions": [
                r'eval\s*\(',
                r'exec\s*\(',
                r'os\.system\s*\(',
                r'subprocess\.call\s*\([^)]*shell\s*=\s*True'
            ],
            "weak_crypto": [
                r'md5\s*\(',
                r'sha1\s*\(',
                r'DES\s*\(',
                r'RC4\s*\('
            ],
            "sql_injection": [
                r'execute\s*\(\s*["\'][^"\']*%[sd][^"\']*["\']',
                r'query\s*\(\s*["\'][^"\']*\+[^"\']*["\']'
            ]
        }
    
    def perform_security_scan(self):
        """Perform comprehensive security scanning"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "scan_type": "comprehensive",
            "vulnerabilities": [],
            "security_score": 0,
            "recommendations": []
        }
        
        # Scan source code for vulnerabilities
        code_vulns = self.scan_source_code()
        results["vulnerabilities"].extend(code_vulns)
        
        # Check file permissions
        permission_issues = self.check_file_permissions()
        results["vulnerabilities"].extend(permission_issues)
        
        # Check configuration security
        config_issues = self.check_configuration_security()
        results["vulnerabilities"].extend(config_issues)
        
        # Check dependencies for known vulnerabilities
        dependency_issues = self.scan_dependencies()
        results["vulnerabilities"].extend(dependency_issues)
        
        # Generate security recommendations
        results["recommendations"] = self.generate_security_recommendations(results["vulnerabilities"])
        
        # Calculate security score
        results["security_score"] = self.calculate_security_score(results["vulnerabilities"])
        
        print(f"🔍 Security scan completed:")
        print(f"   Security score: {results['security_score']}/100")
        print(f"   Vulnerabilities found: {len(results['vulnerabilities'])}")
        print(f"   Recommendations: {len(results['recommendations'])}")
        
        return results
    
    def scan_source_code(self):
        """Scan source code for security vulnerabilities"""
        vulnerabilities = []
        
        # Scan Python files
        for root, dirs, files in os.walk('.'):
            # Skip virtual environment and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    file_vulns = self.scan_python_file(file_path)
                    vulnerabilities.extend(file_vulns)
        
        print(f"🔍 Source code scan found {len(vulnerabilities)} potential issues")
        return vulnerabilities
    
    def scan_python_file(self, file_path):
        """Scan a Python file for security vulnerabilities"""
        vulnerabilities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Check for hardcoded secrets
            for pattern in self.vulnerability_db["hardcoded_secrets"]:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    vulnerabilities.append({
                        "type": "hardcoded_secret",
                        "severity": "high",
                        "file": file_path,
                        "line": line_num,
                        "description": "Potential hardcoded secret detected",
                        "code_snippet": lines[line_num - 1].strip()
                    })
            
            # Check for insecure functions
            for pattern in self.vulnerability_db["insecure_functions"]:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    vulnerabilities.append({
                        "type": "insecure_function",
                        "severity": "high",
                        "file": file_path,
                        "line": line_num,
                        "description": "Potentially insecure function usage",
                        "code_snippet": lines[line_num - 1].strip()
                    })
            
            # Check for weak cryptography
            for pattern in self.vulnerability_db["weak_crypto"]:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    vulnerabilities.append({
                        "type": "weak_crypto",
                        "severity": "medium",
                        "file": file_path,
                        "line": line_num,
                        "description": "Weak cryptographic algorithm detected",
                        "code_snippet": lines[line_num - 1].strip()
                    })
            
            # Check for SQL injection patterns
            for pattern in self.vulnerability_db["sql_injection"]:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    vulnerabilities.append({
                        "type": "sql_injection",
                        "severity": "critical",
                        "file": file_path,
                        "line": line_num,
                        "description": "Potential SQL injection vulnerability",
                        "code_snippet": lines[line_num - 1].strip()
                    })
        
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
        
        return vulnerabilities
    
    def check_file_permissions(self):
        """Check for insecure file permissions"""
        issues = []
        
        # Check for world-writable files
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    stat_info = os.stat(file_path)
                    mode = stat_info.st_mode
                    
                    # Check if world-writable
                    if mode & 0o002:
                        issues.append({
                            "type": "insecure_permissions",
                            "severity": "medium",
                            "file": file_path,
                            "description": "File is world-writable",
                            "current_permissions": oct(mode)[-3:]
                        })
                    
                    # Check for overly permissive script files
                    if file.endswith(('.py', '.sh', '.bash')) and (mode & 0o777) == 0o777:
                        issues.append({
                            "type": "overly_permissive",
                            "severity": "high",
                            "file": file_path,
                            "description": "Script file has overly permissive permissions",
                            "current_permissions": oct(mode)[-3:]
                        })
                
                except OSError:
                    continue
        
        print(f"🔒 Permission check found {len(issues)} issues")
        return issues
    
    def check_configuration_security(self):
        """Check configuration files for security issues"""
        issues = []
        
        # Check Flask app configuration
        flask_app_path = 'services/prompt_memory/app.py'
        if os.path.exists(flask_app_path):
            with open(flask_app_path, 'r') as f:
                content = f.read()
                
                # Check for debug mode in production
                if 'debug=True' in content:
                    issues.append({
                        "type": "debug_mode",
                        "severity": "high",
                        "file": flask_app_path,
                        "description": "Flask debug mode enabled (potential information disclosure)",
                        "recommendation": "Disable debug mode in production"
                    })
                
                # Check for default secret key
                if 'SECRET_KEY' not in content:
                    issues.append({
                        "type": "missing_secret_key",
                        "severity": "high",
                        "file": flask_app_path,
                        "description": "Flask app missing SECRET_KEY configuration",
                        "recommendation": "Add a strong, random SECRET_KEY"
                    })
        
        # Check for environment files with secrets
        env_files = ['.env', '.env.local', '.env.production']
        for env_file in env_files:
            if os.path.exists(env_file):
                issues.append({
                    "type": "env_file_exposure",
                    "severity": "medium",
                    "file": env_file,
                    "description": "Environment file may contain secrets",
                    "recommendation": "Ensure environment files are not committed to version control"
                })
        
        print(f"⚙️ Configuration check found {len(issues)} issues")
        return issues
    
    def scan_dependencies(self):
        """Scan dependencies for known vulnerabilities"""
        issues = []
        
        # Check requirements.txt for known vulnerable packages
        if os.path.exists('requirements.txt'):
            with open('requirements.txt', 'r') as f:
                requirements = f.read()
            
            # Common vulnerable patterns (simplified check)
            vulnerable_patterns = {
                'flask==2.0.0': 'Known XSS vulnerability in Flask 2.0.0',
                'requests<2.20.0': 'Vulnerable to URL parsing issues',
                'pyyaml<5.1': 'Arbitrary code execution vulnerability'
            }
            
            for pattern, description in vulnerable_patterns.items():
                if pattern in requirements:
                    issues.append({
                        "type": "vulnerable_dependency",
                        "severity": "high",
                        "file": "requirements.txt",
                        "description": description,
                        "recommendation": f"Update package to latest secure version"
                    })
        
        print(f"📦 Dependency scan found {len(issues)} issues")
        return issues
    
    def generate_security_recommendations(self, vulnerabilities):
        """Generate actionable security recommendations"""
        recommendations = []
        
        # General security hardening
        recommendations.extend([
            {
                "category": "Authentication",
                "priority": "high",
                "action": "Implement multi-factor authentication for admin accounts",
                "implementation": "Use libraries like PyOTP for TOTP implementation"
            },
            {
                "category": "Encryption",
                "priority": "high",
                "action": "Encrypt sensitive data at rest",
                "implementation": "Use cryptography library with AES-256-GCM"
            },
            {
                "category": "Logging",
                "priority": "medium",
                "action": "Implement comprehensive security logging",
                "implementation": "Log authentication attempts, data access, and configuration changes"
            },
            {
                "category": "Network Security",
                "priority": "medium",
                "action": "Implement rate limiting and CORS policies",
                "implementation": "Use Flask-Limiter for rate limiting"
            }
        ])
        
        # Specific recommendations based on vulnerabilities
        vuln_types = [v["type"] for v in vulnerabilities]
        
        if "hardcoded_secret" in vuln_types:
            recommendations.append({
                "category": "Secret Management",
                "priority": "critical",
                "action": "Remove hardcoded secrets and use environment variables",
                "implementation": "Use python-dotenv or HashiCorp Vault for secret management"
            })
        
        if "insecure_function" in vuln_types:
            recommendations.append({
                "category": "Code Security",
                "priority": "high",
                "action": "Replace insecure functions with safer alternatives",
                "implementation": "Use subprocess with shell=False, avoid eval/exec"
            })
        
        return recommendations
    
    def calculate_security_score(self, vulnerabilities):
        """Calculate overall security score based on vulnerabilities"""
        base_score = 100
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "low")
            if severity == "critical":
                base_score -= 20
            elif severity == "high":
                base_score -= 10
            elif severity == "medium":
                base_score -= 5
            elif severity == "low":
                base_score -= 2
        
        return max(0, base_score)
    
    def generate_security_report(self, results):
        """Generate comprehensive security report"""
        report_path = "reports/security_report.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Security report saved to: {report_path}")
        
        # Generate security remediation plan
        self.generate_remediation_plan(results)
        
        # Generate security checklist
        self.generate_security_checklist()
    
    def generate_remediation_plan(self, results):
        """Generate detailed security remediation plan"""
        plan_path = "reports/security_remediation_plan.md"
        
        with open(plan_path, 'w') as f:
            f.write("# Security Remediation Plan\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Security Score: {results['security_score']}/100\n\n")
            
            # Group vulnerabilities by severity
            critical = [v for v in results["vulnerabilities"] if v.get("severity") == "critical"]
            high = [v for v in results["vulnerabilities"] if v.get("severity") == "high"]
            medium = [v for v in results["vulnerabilities"] if v.get("severity") == "medium"]
            
            if critical:
                f.write("## 🚨 Critical Priority (Fix Immediately)\n\n")
                for i, vuln in enumerate(critical, 1):
                    f.write(f"### {i}. {vuln['description']}\n")
                    f.write(f"- **File**: {vuln.get('file', 'N/A')}\n")
                    f.write(f"- **Type**: {vuln['type']}\n")
                    if 'code_snippet' in vuln:
                        f.write(f"- **Code**: `{vuln['code_snippet']}`\n")
                    f.write("\n")
            
            if high:
                f.write("## ⚠️ High Priority (Fix Within 7 Days)\n\n")
                for i, vuln in enumerate(high, 1):
                    f.write(f"### {i}. {vuln['description']}\n")
                    f.write(f"- **File**: {vuln.get('file', 'N/A')}\n")
                    f.write(f"- **Type**: {vuln['type']}\n")
                    if 'recommendation' in vuln:
                        f.write(f"- **Fix**: {vuln['recommendation']}\n")
                    f.write("\n")
            
            if medium:
                f.write("## 📋 Medium Priority (Fix Within 30 Days)\n\n")
                for i, vuln in enumerate(medium, 1):
                    f.write(f"### {i}. {vuln['description']}\n")
                    f.write(f"- **File**: {vuln.get('file', 'N/A')}\n")
                    f.write(f"- **Type**: {vuln['type']}\n")
                    f.write("\n")
            
            # Add recommendations
            f.write("## 🛡️ Security Recommendations\n\n")
            for rec in results["recommendations"]:
                f.write(f"### {rec['action']}\n")
                f.write(f"- **Priority**: {rec['priority'].upper()}\n")
                f.write(f"- **Category**: {rec['category']}\n")
                f.write(f"- **Implementation**: {rec['implementation']}\n\n")
        
        print(f"📋 Remediation plan saved to: {plan_path}")
    
    def generate_security_checklist(self):
        """Generate security hardening checklist"""
        checklist_path = "docs/security_checklist.md"
        os.makedirs(os.path.dirname(checklist_path), exist_ok=True)
        
        content = f"""# Security Hardening Checklist

Generated by SecuBot on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Application Security

### Authentication & Authorization
- [ ] Multi-factor authentication implemented
- [ ] Strong password policies enforced
- [ ] Session management secure
- [ ] Role-based access control implemented

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Secure communication (HTTPS/TLS)
- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS

### Code Security
- [ ] No hardcoded secrets in source code
- [ ] Secure coding practices followed
- [ ] Dependencies regularly updated
- [ ] Code reviews include security considerations

### Infrastructure Security
- [ ] File permissions properly configured
- [ ] Debug mode disabled in production
- [ ] Error messages don't expose sensitive information
- [ ] Security headers implemented

### Monitoring & Logging
- [ ] Security events logged
- [ ] Log integrity protected
- [ ] Anomaly detection implemented
- [ ] Incident response plan in place

### Compliance
- [ ] OWASP Top 10 vulnerabilities addressed
- [ ] Security policies documented
- [ ] Regular security assessments conducted
- [ ] Vulnerability management process in place

---

Run SecuBot regularly to maintain security posture.
"""
        
        with open(checklist_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Security checklist saved to: {checklist_path}")
    
    def get_metrics(self):
        """Return performance metrics for this agent"""
        return {
            "scans_completed": len(self.scan_results),
            "vulnerability_patterns": len(self.vulnerability_db),
            "last_run": datetime.now().isoformat()
        }

def get_plugin():
    return SecurityHardeningAgent()
