"""
Support Case Automation Workflow System
Handles end-to-end support case processing with manufacturer communication
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# ============================================================================
# DATA MODELS
# ============================================================================

class CaseStatus(Enum):
    RECEIVED = "received"
    TRANSLATED = "translated"
    FORWARDED = "forwarded"
    AWAITING_REPLY = "awaiting_reply"
    REPLY_RECEIVED = "reply_received"
    TRANSLATED_BACK = "translated_back"
    PENDING_APPROVAL = "pending_approval"
    REMINDER_SENT = "reminder_sent"
    APPROVED = "approved"
    CLOSED = "closed"

@dataclass
class SupportCase:
    case_id: str
    original_text: str
    original_language: str
    translated_text: str = ""
    task_number: str = ""
    manufacturer_reply: str = ""
    reply_translated: str = ""
    status: str = CaseStatus.RECEIVED.value
    created_at: str = ""
    forwarded_at: str = ""
    reply_received_at: str = ""
    reminder_sent: bool = False
    needs_approval: bool = False
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

# ============================================================================
# TRANSLATION SERVICE (Mock)
# ============================================================================

class TranslationService:
    """Translation service with automatic language detection - production ready"""
    
    # Supported language codes mapping
    LANGUAGE_CODES = {
        'en': 'English',
        'da': 'Danish',
        'de': 'German',
        'fr': 'French',
        'es': 'Spanish',
        'sv': 'Swedish',
        'no': 'Norwegian',
        'nl': 'Dutch',
        'it': 'Italian',
        'pt': 'Portuguese'
    }
    
    @staticmethod
    def detect_language(text: str) -> tuple:
        """Detect language from text using langdetect library
        
        Returns:
            tuple: (language_code, language_name)
        """
        try:
            from langdetect import detect, DetectorFactory
            # Set seed for consistent results
            DetectorFactory.seed = 0
            
            # Detect language
            detected_code = detect(text)
            language_name = TranslationService.LANGUAGE_CODES.get(detected_code, 'English')
            
            print(f"[LANGUAGE DETECTION] Detected: {detected_code} ({language_name})")
            return detected_code, language_name
            
        except ImportError:
            print("[WARNING] langdetect not installed, defaulting to English")
            return 'en', 'English'
        except Exception as e:
            print(f"[WARNING] Language detection failed: {e}, defaulting to English")
            return 'en', 'English'
    
    @staticmethod
    def translate_to_english(text: str, source_lang_code: str = None) -> tuple:
        """Translate text to English with auto-detection
        
        Args:
            text: The text to translate
            source_lang_code: Optional source language code. If not provided, auto-detect.
        
        Returns:
            tuple: (translated_text, detected_lang_code, detected_lang_name)
        """
        # Auto-detect language if not provided
        if source_lang_code is None:
            source_lang_code, source_lang_name = TranslationService.detect_language(text)
        else:
            source_lang_name = TranslationService.LANGUAGE_CODES.get(source_lang_code, 'Unknown')
        
        print(f"[TRANSLATION] Translating from {source_lang_name} ({source_lang_code}) to English")
        
        # If already in English, no translation needed
        if source_lang_code == 'en':
            return text, source_lang_code, source_lang_name
        
        # Mock translation for development/testing
        # Replace with real API call: Google Translate, DeepL, etc.
        translated = f"[Translated from {source_lang_name} to English] {text}"
        return translated, source_lang_code, source_lang_name
    
    @staticmethod
    def translate_from_english(text: str, target_lang_code: str) -> str:
        """Translate text from English to target language
        
        Args:
            text: English text to translate
            target_lang_code: Target language code (e.g., 'da', 'de')
        
        Returns:
            str: Translated text
        """
        target_lang_name = TranslationService.LANGUAGE_CODES.get(target_lang_code, 'Unknown')
        print(f"[TRANSLATION] Translating from English to {target_lang_name}")
        
        # If target is English, no translation needed
        if target_lang_code == 'en':
            return text
        
        # Mock translation for development/testing
        # Replace with real API call: Google Translate, DeepL, etc.
        return f"[Translated to {target_lang_name}] {text}"

# ============================================================================
# MANUFACTURER API SERVICE (Mock)
# ============================================================================

class ManufacturerAPI:
    """Mock manufacturer API - replace with real implementation"""
    
    def __init__(self):
        self.task_counter = 1000
        self.submitted_tasks = {}
    
    def submit_case(self, case_description: str) -> str:
        """Submit case to manufacturer and receive task number"""
        self.task_counter += 1
        task_number = f"TASK-{self.task_counter}"
        
        print(f"[MANUFACTURER API] Submitting case to manufacturer")
        print(f"[MANUFACTURER API] Received task number: {task_number}")
        
        # Store for mock reply generation
        self.submitted_tasks[task_number] = {
            'description': case_description,
            'submitted_at': datetime.now()
        }
        
        return task_number
    
    def check_reply(self, task_number: str) -> Optional[str]:
        """Check if manufacturer has replied (mock implementation)"""
        if task_number not in self.submitted_tasks:
            return None
        
        # Mock: randomly decide if reply is available
        # In real implementation, check actual email or API
        print(f"[MANUFACTURER API] Checking for reply on {task_number}")
        return None  # No reply yet in this mock
    
    def send_reminder(self, task_number: str) -> bool:
        """Send reminder to manufacturer"""
        print(f"[MANUFACTURER API] Sending reminder for {task_number}")
        return True

# ============================================================================
# EMAIL SERVICE (Mock)
# ============================================================================

class EmailService:
    """Mock email service - replace with real SMTP/IMAP"""
    
    @staticmethod
    def send_email(to: str, subject: str, body: str) -> bool:
        """Send email (mock implementation)"""
        print(f"\n[EMAIL] Sending email:")
        print(f"  To: {to}")
        print(f"  Subject: {subject}")
        print(f"  Body: {body[:100]}...")
        return True
    
    @staticmethod
    def check_inbox() -> List[Dict]:
        """Check inbox for new emails (mock implementation)"""
        print("[EMAIL] Checking inbox for manufacturer replies")
        # Mock: return empty for now
        return []

# ============================================================================
# BUSINESS HOURS CALCULATOR
# ============================================================================

class BusinessHoursCalculator:
    """Calculate business hours excluding weekends"""
    
    @staticmethod
    def is_business_day(date: datetime) -> bool:
        """Check if date is a business day (Mon-Fri)"""
        return date.weekday() < 5  # 0-4 are Mon-Fri
    
    @staticmethod
    def add_business_hours(start_time: datetime, hours: int) -> datetime:
        """Add business hours to a datetime, skipping weekends"""
        current = start_time
        remaining_hours = hours
        
        while remaining_hours > 0:
            current += timedelta(hours=1)
            if BusinessHoursCalculator.is_business_day(current):
                remaining_hours -= 1
        
        return current
    
    @staticmethod
    def is_overdue(forwarded_at: str, hours_threshold: int = 24) -> bool:
        """Check if case is overdue for response"""
        forwarded_time = datetime.fromisoformat(forwarded_at)
        deadline = BusinessHoursCalculator.add_business_hours(
            forwarded_time, 
            hours_threshold
        )
        return datetime.now() > deadline

# ============================================================================
# MAIN WORKFLOW ORCHESTRATOR
# ============================================================================

class SupportWorkflow:
    """Main workflow orchestrator for support case automation"""
    
    def __init__(self):
        self.translator = TranslationService()
        self.manufacturer = ManufacturerAPI()
        self.email = EmailService()
        self.cases = {}  # In-memory storage (use database in production)
    
    def process_new_case(self, case_text: str) -> SupportCase:
        """
        Step 1-4: Process new support case through initial workflow
        1. Receive support case
        2. Auto-detect language and translate to English
        3. Forward to manufacturer
        4. Get task number
        """
        print("\n" + "="*70)
        print("PROCESSING NEW SUPPORT CASE")
        print("="*70)
        
        # Step 1: Receive case
        case_id = f"CASE-{len(self.cases) + 1001}"
        print(f"\n[STEP 1] Support case received: {case_id}")
        
        # Step 2: Auto-detect language and translate to English
        print(f"\n[STEP 2] Detecting language and translating to English")
        translated_text, lang_code, lang_name = self.translator.translate_to_english(case_text)
        
        case = SupportCase(
            case_id=case_id,
            original_text=case_text,
            original_language=lang_code,
            translated_text=translated_text,
            status=CaseStatus.TRANSLATED.value
        )
        
        # Step 3 & 4: Forward to manufacturer and get task number
        print(f"\n[STEP 3-4] Forwarding to manufacturer")
        task_number = self.manufacturer.submit_case(translated_text)
        
        case.task_number = task_number
        case.forwarded_at = datetime.now().isoformat()
        case.status = CaseStatus.AWAITING_REPLY.value
        
        # Store case
        self.cases[case_id] = case
        
        # Send confirmation email to internal team
        self.email.send_email(
            to="support@company.com",
            subject=f"Case {case_id} forwarded - Task {task_number}",
            body=f"Case has been forwarded to manufacturer.\n"
                 f"Task Number: {task_number}\n"
                 f"Original language: {original_language}"
        )
        
        print(f"\n✓ Case {case_id} processed successfully")
        print(f"  Task Number: {task_number}")
        print(f"  Status: {case.status}")
        
        return case
    
    def process_manufacturer_reply(self, task_number: str, reply_text: str) -> Optional[SupportCase]:
        """
        Step 5-6: Process manufacturer reply
        5. Receive reply from manufacturer
        6. Translate back to original language
        7. Mark for manual approval
        """
        print("\n" + "="*70)
        print("PROCESSING MANUFACTURER REPLY")
        print("="*70)
        
        # Find case by task number
        case = None
        for c in self.cases.values():
            if c.task_number == task_number:
                case = c
                break
        
        if not case:
            print(f"[ERROR] No case found for task number {task_number}")
            return None
        
        print(f"\n[STEP 5] Reply received for {case.case_id}")
        case.manufacturer_reply = reply_text
        case.reply_received_at = datetime.now().isoformat()
        case.status = CaseStatus.REPLY_RECEIVED.value
        
        # Step 6: Translate back to original language
        lang_name = TranslationService.LANGUAGE_CODES.get(case.original_language, 'Unknown')
        print(f"\n[STEP 6] Translating reply back to {lang_name} ({case.original_language})")
        case.reply_translated = self.translator.translate_from_english(
            reply_text,
            case.original_language
        )
        case.status = CaseStatus.TRANSLATED_BACK.value
        
        # Step 7: Mark for manual approval
        print(f"\n[STEP 7] Preparing for manual approval")
        case.needs_approval = True
        case.status = CaseStatus.PENDING_APPROVAL.value
        
        # Notify team for manual review
        self.email.send_email(
            to="support@company.com",
            subject=f"Case {case.case_id} - Ready for Approval",
            body=f"Manufacturer reply received and translated.\n\n"
                 f"Original Case: {case.original_text}\n\n"
                 f"Translated Reply: {case.reply_translated}\n\n"
                 f"Please review and approve."
        )
        
        print(f"\n✓ Reply processed for {case.case_id}")
        print(f"  Status: {case.status}")
        
        return case
    
    def check_and_send_reminders(self):
        """
        Addon: Check for cases needing reminders
        - No reply within 24 business hours
        - Excluding weekends
        - Only if no reply received since forwarding
        """
        print("\n" + "="*70)
        print("CHECKING FOR OVERDUE CASES")
        print("="*70)
        
        for case_id, case in self.cases.items():
            # Only check cases awaiting reply
            if case.status != CaseStatus.AWAITING_REPLY.value:
                continue
            
            # Skip if reminder already sent
            if case.reminder_sent:
                continue
            
            # Check if overdue (24 business hours)
            if BusinessHoursCalculator.is_overdue(case.forwarded_at, 24):
                print(f"\n[REMINDER] Case {case_id} is overdue")
                print(f"  Task Number: {case.task_number}")
                print(f"  Forwarded at: {case.forwarded_at}")
                
                # Send reminder to manufacturer
                self.manufacturer.send_reminder(case.task_number)
                
                # Send notification email
                self.email.send_email(
                    to="manufacturer@example.com",
                    subject=f"REMINDER: Task {case.task_number}",
                    body=f"This is a reminder for task {case.task_number}.\n"
                         f"We have not received a response within 24 business hours.\n"
                         f"Please provide an update."
                )
                
                case.reminder_sent = True
                case.status = CaseStatus.REMINDER_SENT.value
                
                print(f"  ✓ Reminder sent")
    
    def approve_case(self, case_id: str) -> bool:
        """Manual approval of translated reply"""
        if case_id not in self.cases:
            return False
        
        case = self.cases[case_id]
        case.status = CaseStatus.APPROVED.value
        
        # Send final response to customer
        self.email.send_email(
            to="customer@example.com",
            subject=f"Re: Your support case {case_id}",
            body=case.reply_translated
        )
        
        print(f"[APPROVAL] Case {case_id} approved and sent to customer")
        return True
    
    def get_case_status(self, case_id: str) -> Optional[Dict]:
        """Get current status of a case"""
        if case_id not in self.cases:
            return None
        return asdict(self.cases[case_id])
    
    def list_pending_approvals(self) -> List[Dict]:
        """Get all cases pending manual approval"""
        return [
            asdict(case) 
            for case in self.cases.values() 
            if case.needs_approval and case.status == CaseStatus.PENDING_APPROVAL.value
        ]

# ============================================================================
# DEMO USAGE
# ============================================================================

def demo_workflow():
    """Demonstrate the complete workflow"""
    
    workflow = SupportWorkflow()
    
    # Demo Case 1: Danish support request
    print("\n" + "#"*70)
    print("# DEMO: Complete Workflow")
    print("#"*70)
    
    case_text = """
    Jeg har et problem med mit produkt. 
    Det virker ikke korrekt og jeg har brug for hjælp.
    Model nummer: XYZ-123
    """
    
    # Process new case (Steps 1-4)
    case = workflow.process_new_case(case_text)
    
    print(f"\n{'='*70}")
    print("CASE PROCESSED - AWAITING MANUFACTURER REPLY")
    print(f"{'='*70}\n")
    
    # Simulate time passing and checking for reminders
    print("\n[SYSTEM] Checking for overdue cases...")
    workflow.check_and_send_reminders()
    
    # Simulate manufacturer reply (Steps 5-6)
    print("\n[SIMULATION] Manufacturer sends reply...")
    time.sleep(1)
    
    manufacturer_reply = """
    Thank you for contacting us. We have identified the issue with model XYZ-123.
    Please follow these steps:
    1. Reset the device
    2. Update firmware to version 2.1
    3. Contact us if problem persists
    """
    
    workflow.process_manufacturer_reply(case.task_number, manufacturer_reply)
    
    # Show pending approvals
    print("\n" + "="*70)
    print("PENDING APPROVALS")
    print("="*70)
    pending = workflow.list_pending_approvals()
    print(f"\nCases pending approval: {len(pending)}")
    for p in pending:
        print(f"  - {p['case_id']}: {p['original_language']}")
    
    # Approve case
    print("\n[MANUAL APPROVAL] Approving case...")
    workflow.approve_case(case.case_id)
    
    print("\n" + "#"*70)
    print("# WORKFLOW COMPLETE")
    print("#"*70)
    
    # Print final status
    status = workflow.get_case_status(case.case_id)
    print("\nFinal Case Status:")
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    demo_workflow()