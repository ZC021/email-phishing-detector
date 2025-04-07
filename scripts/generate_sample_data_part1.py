import pandas as pd
import numpy as np
import random
import os
import argparse
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake.seed_instance(42)

def generate_phishing_email():
    """Generate a fake phishing email"""
    # Choose a phishing type
    phishing_type = random.choice([
        'credential_harvest', 'financial_scam', 'malware_delivery', 
        'urgent_action', 'fake_invoice', 'false_security_alert'
    ])
    
    # Generate sender information
    if random.random() < 0.7:  # 70% chance to use deceptive sender
        legitimate_domains = ['paypal.com', 'amazon.com', 'microsoft.com', 'apple.com', 'google.com', 'facebook.com']
        company = random.choice(legitimate_domains).split('.')[0]
        sender_name = f"{company.capitalize()} Support"
        
        # Create a deceptive domain (similar but not identical)
        domain_variations = [
            f"{company}-support.com",
            f"{company}secure.net",
            f"{company}-team.org",
            f"{company}verify.com",
            f"{company}.security-check.com"
        ]
        sender_domain = random.choice(domain_variations)
        sender_email = f"security@{sender_domain}"
    else:
        sender_name = fake.name()
        sender_email = fake.email()
    
    # Generate recipient
    recipient_email = fake.email()
    
    # Generate date (within last 30 days)
    date = fake.date_time_between(start_date='-30d', end_date='now').strftime("%a, %d %b %Y %H:%M:%S %z")
    
    # Generate subject line based on phishing type
    subject_templates = {
        'credential_harvest': [
            "Urgent: Verify Your Account",
            "Security Alert: Unusual Login Attempt",
            "Your Account Access Has Been Limited",
            "Password Reset Required",
            "Suspicious Activity Detected"
        ],
        'financial_scam': [
            "Payment Confirmation #REF-{}",
            "Invoice #{} Due",
            "Your Refund of ${}",
            "Tax Refund Notification",
            "Unclaimed Funds in Your Name"
        ],
        'malware_delivery': [
            "Your Shipment Tracking Details",
            "Important Document Attached",
            "Receipt for Your Recent Purchase",
            "Your Requested Files",
            "Photo Shared With You"
        ],
        'urgent_action': [
            "URGENT: Action Required",
            "IMMEDIATE ATTENTION NEEDED",
            "Time Sensitive: Response Required",
            "FINAL WARNING: Account Termination",
            "Critical: Account Suspension Imminent"
        ],
        'fake_invoice': [
            "Invoice #{} from {}",
            "Your Recent Order #{}",
            "Receipt for Payment to {}",
            "Subscription Charge: ${}",
            "Order Confirmation #{}"
        ],
        'false_security_alert': [
            "Security Alert: New Device Login",
            "Suspicious Sign-in Blocked",
            "Your Account Access Has Changed",
            "Security Notification: Please Review",
            "Important Security Update Required"
        ]
    }
    
    subject_template = random.choice(subject_templates[phishing_type])
    
    # Format the subject with random data as needed
    if '{}' in subject_template:
        if 'Invoice' in subject_template or 'Order' in subject_template:
            subject = subject_template.format(random.randint(10000, 999999))
        elif 'Payment' in subject_template:
            subject = subject_template.format(random.randint(100000, 999999))
        elif 'Refund' in subject_template:
            subject = subject_template.format(random.randint(50, 999))
        elif '#REF' in subject_template:
            subject = subject_template.format(fake.bothify(text='???-######'))
        else:
            subject = subject_template.format(fake.company())
    else:
        subject = subject_template
    
    # Generate email body based on phishing type
    body = generate_phishing_body(phishing_type, recipient_email.split('@')[0])
    
    # Assemble the email
    email = f"From: {sender_name} <{sender_email}>\nTo: <{recipient_email}>\nDate: {date}\nSubject: {subject}\n\n{body}"
    
    return email

def generate_phishing_body(phishing_type, recipient_name):
    """Generate the body of a phishing email based on type"""
    
    if phishing_type == 'credential_harvest':
        company = random.choice(['PayPal', 'Amazon', 'Microsoft', 'Apple', 'Google', 'Facebook', 'Netflix'])
        greeting = random.choice([f"Dear {company} Customer", f"Dear Valued Customer", f"Dear User", f"Hello {recipient_name}"])
        
        body = f"{greeting},\n\n"
        body += random.choice([
            f"We have detected unusual activity on your {company} account. To secure your account, please verify your information immediately.",
            f"Your {company} account has been temporarily limited because we've noticed some unusual activity. We need your help resolving this issue.",
            f"We are updating our security measures. As part of this process, we need all users to verify their account information."
        ])
        
        body += "\n\n"
        body += random.choice([
            "Please click the link below to verify your information:\n",
            "To restore full access to your account, please update your details:\n",
            "To secure your account, please follow this link:\n"
        ])
        
        # Generate phishing URL
        domain_variations = [
            f"{company.lower()}-secure-verify.com",
            f"{company.lower()}-account-security.net",
            f"secure-{company.lower()}.com",
            f"{company.lower()}-verification.com"
        ]
        phishing_url = f"https://{random.choice(domain_variations)}/login"
        body += f"\n{phishing_url}\n\n"
        
        body += random.choice([
            f"If you do not verify your account within 24 hours, your {company} account will be suspended.",
            "Please complete this process as soon as possible to avoid account restrictions.",
            "This is an automated message. Please do not reply to this email."
        ])
        
        body += "\n\nThank you,\n"
        body += f"{company} Security Team"
        
    elif phishing_type == 'financial_scam':
        amount = random.randint(50, 5000)
        greeting = random.choice([f"Dear {recipient_name}", "Dear Sir/Madam", "Hello"])
        
        body = f"{greeting},\n\n"
        
        # Choose a random financial scam type
        scam_type = random.choice(['refund', 'lottery', 'inheritance', 'payment'])
        
        if scam_type == 'refund':
            body += f"Our records indicate that you are eligible for a refund of ${amount}.00 due to an overpayment on your recent tax filing."
            body += "\n\nTo process your refund, we need to verify your banking information. Please complete the secure form:"
        
        elif scam_type == 'lottery':
            body += f"Congratulations! Your email address has been randomly selected as the winner of our annual lottery draw."
            body += f"\n\nYou have won the grand prize of ${amount * 1000}.00. To claim your prize, you must complete the verification process:"
        
        elif scam_type == 'inheritance':
            body += f"I am contacting you regarding an unclaimed inheritance of ${amount * 10000}.00 from a distant relative."
            body += "\n\nAs the legal executor, I need your assistance to transfer these funds. Please complete the verification form:"
        
        else:  # payment
            body += f"We have processed a payment of ${amount}.00 to your account. The funds will be available within 3-5 business days."
            body += "\n\nTo check the status of your payment or expedite the process, please verify your information:"
        
        # Generate phishing URL
        phishing_url = f"https://secure-payment-{fake.domain_word()}.com/claim-funds"
        body += f"\n\n{phishing_url}\n\n"
        
        body += "This offer is valid for 48 hours only. Please respond promptly to avoid missing this opportunity."
        body += "\n\nRegards,\n"
        body += fake.name()
        body += f"\n{random.choice(['Financial Department', 'Claims Processing', 'Treasury Division'])}"
        
    else:
        # Other phishing types will be implemented in part 2
        body = "Generic phishing email content."
    
    return body

# Part 1 ends here, to be continued in part 2