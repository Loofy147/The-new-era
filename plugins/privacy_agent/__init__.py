from core.plugin_interface import PluginInterface
import json
import os
import re
from datetime import datetime, timedelta

class PrivacyGuardAgent(PluginInterface):
    def __init__(self):
        self.name = "PrivacyGuard"
        self.role = "Data Privacy Agent"
        self.description = "Ensures datasets and flows comply with privacy laws (GDPR, CCPA, etc.)"
        self.privacy_frameworks = ["GDPR", "CCPA", "PIPEDA", "LGPD"]
        self.pii_patterns = self.load_pii_patterns()
        self.scan_results = []
    
    def run(self):
        print(f"🤖 {self.name} ({self.role}) is starting privacy compliance scan...")
        
        # Perform comprehensive privacy scan
        privacy_analysis = self.perform_privacy_scan()
        self.generate_privacy_report(privacy_analysis)
        
        print(f"✅ {self.name} completed privacy compliance analysis")
        return privacy_analysis
    
    def load_pii_patterns(self):
        """Load patterns for detecting personally identifiable information"""
        return {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            "ssn": r'\b\d{3}-?\d{2}-?\d{4}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            "ip_address": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            "date_of_birth": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            "passport": r'\b[A-Z]{1,2}\d{6,9}\b',
            "driver_license": r'\b[A-Z]{1,2}\d{6,8}\b'
        }
    
    def perform_privacy_scan(self):
        """Perform comprehensive privacy compliance scanning"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "scan_type": "privacy_compliance",
            "frameworks_checked": self.privacy_frameworks,
            "pii_findings": [],
            "data_flow_analysis": {},
            "consent_management": {},
            "data_retention": {},
            "privacy_score": 0,
            "compliance_gaps": []
        }
        
        # Scan for PII in codebase
        pii_findings = self.scan_for_pii()
        results["pii_findings"] = pii_findings
        
        # Analyze data flows
        results["data_flow_analysis"] = self.analyze_data_flows()
        
        # Check consent management
        results["consent_management"] = self.check_consent_management()
        
        # Check data retention policies
        results["data_retention"] = self.check_data_retention()
        
        # Check privacy policy compliance
        results["privacy_policy"] = self.check_privacy_policy()
        
        # Generate compliance gaps
        results["compliance_gaps"] = self.identify_compliance_gaps(results)
        
        # Calculate privacy score
        results["privacy_score"] = self.calculate_privacy_score(results)
        
        print(f"🔍 Privacy scan completed:")
        print(f"   Privacy score: {results['privacy_score']}/100")
        print(f"   PII findings: {len(results['pii_findings'])}")
        print(f"   Compliance gaps: {len(results['compliance_gaps'])}")
        
        return results
    
    def scan_for_pii(self):
        """Scan codebase and data files for personally identifiable information"""
        pii_findings = []
        
        # Scan source code files
        for root, dirs, files in os.walk('.'):
            # Skip virtual environment and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.endswith(('.py', '.json', '.txt', '.csv', '.log')):
                    file_path = os.path.join(root, file)
                    file_findings = self.scan_file_for_pii(file_path)
                    pii_findings.extend(file_findings)
        
        print(f"🔍 PII scan found {len(pii_findings)} potential exposures")
        return pii_findings
    
    def scan_file_for_pii(self, file_path):
        """Scan individual file for PII"""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            for pii_type, pattern in self.pii_patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    # Mask the actual PII data for security
                    masked_data = self.mask_pii_data(match.group(), pii_type)
                    
                    findings.append({
                        "type": pii_type,
                        "file": file_path,
                        "line": line_num,
                        "severity": self.get_pii_severity(pii_type),
                        "description": f"Potential {pii_type.replace('_', ' ')} detected",
                        "masked_data": masked_data,
                        "context": lines[line_num - 1].strip()[:100]
                    })
        
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
        
        return findings
    
    def mask_pii_data(self, data, pii_type):
        """Mask PII data for reporting"""
        if pii_type == "email":
            parts = data.split('@')
            if len(parts) == 2:
                return f"{parts[0][:2]}***@{parts[1]}"
        elif pii_type == "phone":
            return f"***-***-{data[-4:]}"
        elif pii_type == "ssn":
            return f"***-**-{data[-4:]}"
        elif pii_type == "credit_card":
            return f"****-****-****-{data[-4:]}"
        else:
            return f"{data[:2]}***{data[-2:] if len(data) > 4 else ''}"
    
    def get_pii_severity(self, pii_type):
        """Get severity level for different types of PII"""
        high_risk = ["ssn", "credit_card", "passport", "driver_license"]
        medium_risk = ["email", "phone", "date_of_birth"]
        
        if pii_type in high_risk:
            return "high"
        elif pii_type in medium_risk:
            return "medium"
        else:
            return "low"
    
    def analyze_data_flows(self):
        """Analyze how data flows through the system"""
        analysis = {
            "data_collection_points": [],
            "data_storage_locations": [],
            "data_transmission_paths": [],
            "third_party_integrations": []
        }
        
        # Check Flask app for data collection
        flask_app_path = 'services/prompt_memory/app.py'
        if os.path.exists(flask_app_path):
            with open(flask_app_path, 'r') as f:
                content = f.read()
                
                # Look for data collection endpoints
                if '@app.route' in content and 'POST' in content:
                    analysis["data_collection_points"].append({
                        "location": flask_app_path,
                        "type": "API endpoint",
                        "description": "Flask app collects data via POST requests"
                    })
        
        # Check for data storage
        if os.path.exists('services/prompt_memory/prompts.json'):
            analysis["data_storage_locations"].append({
                "location": "services/prompt_memory/prompts.json",
                "type": "Local file storage",
                "description": "Prompts stored in JSON file"
            })
        
        print(f"📊 Data flow analysis completed")
        return analysis
    
    def check_consent_management(self):
        """Check for consent management implementation"""
        consent_status = {
            "consent_mechanism_exists": False,
            "consent_tracking": False,
            "consent_withdrawal": False,
            "granular_consent": False,
            "findings": []
        }
        
        # Check for consent-related code
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read().lower()
                            
                            if 'consent' in content:
                                consent_status["findings"].append({
                                    "file": file_path,
                                    "note": "Consent-related code found"
                                })
                    except:
                        continue
        
        if not consent_status["findings"]:
            consent_status["findings"].append({
                "issue": "No consent management mechanism found",
                "recommendation": "Implement GDPR-compliant consent management"
            })
        
        print(f"📋 Consent management check completed")
        return consent_status
    
    def check_data_retention(self):
        """Check data retention policies and implementation"""
        retention_status = {
            "retention_policy_exists": False,
            "automated_deletion": False,
            "retention_periods_defined": False,
            "findings": []
        }
        
        # Check for retention-related code or configuration
        retention_keywords = ['delete', 'retention', 'expire', 'cleanup', 'purge']
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.endswith(('.py', '.json', '.yaml', '.yml')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read().lower()
                            
                            for keyword in retention_keywords:
                                if keyword in content:
                                    retention_status["findings"].append({
                                        "file": file_path,
                                        "keyword": keyword,
                                        "note": f"Potential retention-related code found"
                                    })
                                    break
                    except:
                        continue
        
        if not retention_status["findings"]:
            retention_status["findings"].append({
                "issue": "No data retention policies implemented",
                "recommendation": "Implement automated data retention and deletion"
            })
        
        print(f"🗂️ Data retention check completed")
        return retention_status
    
    def check_privacy_policy(self):
        """Check for privacy policy and data processing documentation"""
        policy_status = {
            "privacy_policy_exists": False,
            "data_processing_documented": False,
            "user_rights_documented": False,
            "findings": []
        }
        
        # Check for privacy policy files
        policy_files = ['privacy_policy.md', 'PRIVACY.md', 'privacy.txt', 'data_processing.md']
        
        for policy_file in policy_files:
            if os.path.exists(policy_file):
                policy_status["privacy_policy_exists"] = True
                policy_status["findings"].append({
                    "file": policy_file,
                    "note": "Privacy policy found"
                })
        
        if not policy_status["privacy_policy_exists"]:
            policy_status["findings"].append({
                "issue": "No privacy policy found",
                "recommendation": "Create comprehensive privacy policy documenting data processing"
            })
        
        print(f"📜 Privacy policy check completed")
        return policy_status
    
    def identify_compliance_gaps(self, results):
        """Identify specific compliance gaps based on scan results"""
        gaps = []
        
        # GDPR compliance gaps
        if len(results["pii_findings"]) > 0:
            gaps.append({
                "framework": "GDPR",
                "article": "Article 32 - Security of processing",
                "gap": "PII found in code/data files",
                "severity": "high",
                "recommendation": "Remove or encrypt PII, implement data minimization"
            })
        
        if not results["consent_management"]["consent_mechanism_exists"]:
            gaps.append({
                "framework": "GDPR",
                "article": "Article 7 - Conditions for consent",
                "gap": "No consent management mechanism",
                "severity": "critical",
                "recommendation": "Implement consent collection and tracking system"
            })
        
        if not results["data_retention"]["retention_policy_exists"]:
            gaps.append({
                "framework": "GDPR",
                "article": "Article 5(1)(e) - Storage limitation",
                "gap": "No data retention policy",
                "severity": "high",
                "recommendation": "Define and implement data retention periods"
            })
        
        if not results["privacy_policy"]["privacy_policy_exists"]:
            gaps.append({
                "framework": "GDPR",
                "article": "Article 13 - Information to be provided",
                "gap": "No privacy policy found",
                "severity": "high",
                "recommendation": "Create comprehensive privacy notice"
            })
        
        # CCPA compliance gaps
        gaps.append({
            "framework": "CCPA",
            "section": "Section 1798.100",
            "gap": "Consumer rights not implemented",
            "severity": "medium",
            "recommendation": "Implement consumer data access and deletion rights"
        })
        
        return gaps
    
    def calculate_privacy_score(self, results):
        """Calculate overall privacy compliance score"""
        base_score = 100
        
        # Deduct points for PII findings
        pii_deduction = min(len(results["pii_findings"]) * 5, 30)
        base_score -= pii_deduction
        
        # Deduct points for compliance gaps
        for gap in results["compliance_gaps"]:
            severity = gap.get("severity", "low")
            if severity == "critical":
                base_score -= 15
            elif severity == "high":
                base_score -= 10
            elif severity == "medium":
                base_score -= 5
        
        # Add points for good practices
        if results["consent_management"]["consent_mechanism_exists"]:
            base_score += 5
        
        if results["data_retention"]["retention_policy_exists"]:
            base_score += 5
        
        if results["privacy_policy"]["privacy_policy_exists"]:
            base_score += 5
        
        return max(0, min(100, base_score))
    
    def generate_privacy_report(self, results):
        """Generate comprehensive privacy compliance report"""
        report_path = "reports/privacy_compliance_report.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Privacy compliance report saved to: {report_path}")
        
        # Generate privacy action plan
        self.generate_privacy_action_plan(results)
        
        # Generate GDPR compliance checklist
        self.generate_gdpr_checklist()
    
    def generate_privacy_action_plan(self, results):
        """Generate detailed privacy action plan"""
        plan_path = "reports/privacy_action_plan.md"
        
        with open(plan_path, 'w') as f:
            f.write("# Privacy Compliance Action Plan\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Privacy Score: {results['privacy_score']}/100\n\n")
            
            # Immediate actions for critical gaps
            critical_gaps = [g for g in results["compliance_gaps"] if g.get("severity") == "critical"]
            if critical_gaps:
                f.write("## 🚨 Immediate Actions Required\n\n")
                for gap in critical_gaps:
                    f.write(f"### {gap['gap']}\n")
                    f.write(f"- **Framework**: {gap['framework']}\n")
                    f.write(f"- **Reference**: {gap.get('article', gap.get('section', 'N/A'))}\n")
                    f.write(f"- **Action**: {gap['recommendation']}\n\n")
            
            # High priority actions
            high_gaps = [g for g in results["compliance_gaps"] if g.get("severity") == "high"]
            if high_gaps:
                f.write("## ⚠️ High Priority Actions (30 days)\n\n")
                for gap in high_gaps:
                    f.write(f"### {gap['gap']}\n")
                    f.write(f"- **Framework**: {gap['framework']}\n")
                    f.write(f"- **Action**: {gap['recommendation']}\n\n")
            
            # PII remediation
            if results["pii_findings"]:
                f.write("## 🔒 PII Remediation\n\n")
                high_risk_pii = [p for p in results["pii_findings"] if p["severity"] == "high"]
                if high_risk_pii:
                    f.write("### High Risk PII (Remove Immediately)\n\n")
                    for pii in high_risk_pii:
                        f.write(f"- **File**: {pii['file']} (Line {pii['line']})\n")
                        f.write(f"  - **Type**: {pii['type']}\n")
                        f.write(f"  - **Data**: {pii['masked_data']}\n\n")
            
            # Implementation roadmap
            f.write("## 📅 Implementation Roadmap\n\n")
            f.write("### Phase 1 (0-30 days): Critical Compliance\n")
            f.write("- [ ] Remove all PII from code and logs\n")
            f.write("- [ ] Implement consent management system\n")
            f.write("- [ ] Create privacy policy\n\n")
            
            f.write("### Phase 2 (30-90 days): Process Implementation\n")
            f.write("- [ ] Implement data retention policies\n")
            f.write("- [ ] Set up user rights fulfillment process\n")
            f.write("- [ ] Implement data breach notification procedures\n\n")
            
            f.write("### Phase 3 (90+ days): Continuous Improvement\n")
            f.write("- [ ] Regular privacy audits\n")
            f.write("- [ ] Staff privacy training\n")
            f.write("- [ ] Privacy impact assessments for new features\n\n")
        
        print(f"📋 Privacy action plan saved to: {plan_path}")
    
    def generate_gdpr_checklist(self):
        """Generate GDPR compliance checklist"""
        checklist_path = "docs/gdpr_compliance_checklist.md"
        os.makedirs(os.path.dirname(checklist_path), exist_ok=True)
        
        content = f"""# GDPR Compliance Checklist

Generated by PrivacyGuard on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Lawful Basis and Consent (Articles 6 & 7)
- [ ] Lawful basis identified for all data processing
- [ ] Consent mechanisms implemented where required
- [ ] Consent is freely given, specific, informed, and unambiguous
- [ ] Easy withdrawal of consent available

## Transparency and Information (Articles 13 & 14)
- [ ] Privacy notice provided at data collection
- [ ] Clear information about data processing purposes
- [ ] Data retention periods specified
- [ ] Contact details for Data Protection Officer provided

## Individual Rights (Articles 15-22)
- [ ] Right of access implemented
- [ ] Right to rectification available
- [ ] Right to erasure (right to be forgotten) implemented
- [ ] Right to restrict processing available
- [ ] Right to data portability implemented
- [ ] Right to object to processing available

## Data Protection by Design and Default (Article 25)
- [ ] Privacy considerations in system design
- [ ] Data minimization principles applied
- [ ] Pseudonymization techniques used where appropriate
- [ ] Encryption implemented for sensitive data

## Data Security (Article 32)
- [ ] Appropriate technical measures implemented
- [ ] Organizational measures in place
- [ ] Regular security assessments conducted
- [ ] Incident response procedures defined

## Data Protection Impact Assessment (Article 35)
- [ ] DPIA process established
- [ ] High-risk processing activities identified
- [ ] Privacy risks assessed and mitigated

## Records of Processing (Article 30)
- [ ] Processing activities documented
- [ ] Legal basis for processing recorded
- [ ] Data categories and retention periods documented
- [ ] Third-party data sharing documented

## Data Breach Notification (Articles 33 & 34)
- [ ] Breach detection procedures in place
- [ ] 72-hour notification process to supervisory authority
- [ ] Individual notification process for high-risk breaches
- [ ] Breach register maintained

## International Data Transfers (Chapter V)
- [ ] Adequacy decisions considered
- [ ] Appropriate safeguards in place for transfers
- [ ] Standard contractual clauses used where applicable

## Accountability (Article 5)
- [ ] Compliance monitoring procedures
- [ ] Staff training on data protection
- [ ] Regular policy reviews
- [ ] Evidence of compliance maintained

---

Use this checklist to track GDPR compliance progress.
Run PrivacyGuard regularly to maintain compliance.
"""
        
        with open(checklist_path, 'w') as f:
            f.write(content)
        
        print(f"✅ GDPR checklist saved to: {checklist_path}")
    
    def get_metrics(self):
        """Return performance metrics for this agent"""
        return {
            "scans_completed": len(self.scan_results),
            "frameworks_supported": len(self.privacy_frameworks),
            "pii_patterns": len(self.pii_patterns),
            "last_run": datetime.now().isoformat()
        }

def get_plugin():
    return PrivacyGuardAgent()
