import pandas as pd
import numpy as np
import random
import os
import argparse
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# This is part 2 of the sample data generation script
# It completes the remaining phishing body generators and adds functions to generate legitimate emails

def generate_malware_delivery_body(recipient_name):
    """Generate a phishing email body for malware delivery"""
    greeting = random.choice([f"Hi {recipient_name}", "Hello", "Good day"])
    
    body = f"{greeting},\n\n"
    
    # Choose a random malware delivery pretense
    delivery_type = random.choice(['invoice', 'shipment', 'shared_document', 'photo', 'voice_message'])
    
    if delivery_type == 'invoice':
        body += "Please find attached the invoice for your recent purchase.\n"
        body += "Review the details and let us know if you have any questions.\n\n"
        body += "The invoice is password protected for security reasons.\n"
        body += f"Password: Invoice{random.randint(1000, 9999)}"
    
    elif delivery_type == 'shipment':
        body += "Your shipment is on its way!\n"
        body += f"Tracking Number: {fake.bothify(text='??######??')}\n\n"
        body += "Please see the attached shipping label and receipt.\n"
        body += "You can also track your package by clicking this link:\n"
        body += f"https://tracking-{fake.domain_word()}.com/track?id={fake.bothify(text='###???###')}"
    
    elif delivery_type == 'shared_document':
        body += f"{fake.name()} has shared a document with you.\n\n"
        body += "To view this document, please download the attachment and enable macros when prompted.\n"
        body += "This document requires Microsoft Office to view properly."
    
    elif delivery_type == 'photo':
        body += "Check out these photos from our recent event!\n\n"
        body += "I've attached them for you to see. Some great memories here.\n"
        body += "The file is a self-extracting archive to preserve the original quality."
    
    else:  # voice_message
        body += "You have received a new voice message.\n\n"
        body += f"Duration: {random.randint(1, 5)}:{random.randint(10, 59)} minutes\n"
        body += "To listen to this message, please open the attached audio file.\n"
        body += "If you cannot open the attachment, use the backup link below:\n"
        body += f"https://voicemail-{fake.domain_word()}.com/listen?id={fake.bothify(text='###???###')}"
    
    body += "\n\nRegards,\n"
    body += fake.name()
    
    return body

def generate_urgent_action_body(recipient_name):
    """Generate a phishing email body with urgent action required"""
    greeting = random.choice(["ATTENTION", f"URGENT: {recipient_name}", "IMPORTANT NOTICE", "ACTION REQUIRED"])
    
    body = f"{greeting}\n\n"
    body += random.choice([
        "Your account will be SUSPENDED within 24 HOURS unless you take immediate action.",
        "We have detected UNAUTHORIZED access to your account. Immediate verification required.",
        "FINAL NOTICE: Your service will be terminated unless you update your information TODAY."
    ])
    
    body += "\n\n"
    body += "To prevent this action, you MUST verify your account immediately:\n"
    
    # Generate phishing URL
    phishing_url = f"https://urgent-verify-{fake.domain_word()}.com/secure-action"
    body += f"\n{phishing_url}\n\n"
    
    body += random.choice([
        "Failure to respond will result in PERMANENT account closure.",
        "This is your FINAL WARNING. No further notices will be sent.",
        "Your immediate action is REQUIRED to prevent service interruption."
    ])
    
    body += "\n\nSecurity Department"
    return body

def generate_fake_invoice_body(recipient_name):
    """Generate a phishing email body with a fake invoice"""
    company = random.choice(['Amazon', 'Apple', 'Netflix', 'Spotify', 'Microsoft Office', 'Adobe', 'Dropbox'])
    amount = random.randint(29, 599)
    greeting = random.choice([f"Dear {recipient_name}", "Hello", f"Dear {company} Customer"])
    
    body = f"{greeting},\n\n"
    body += f"Thank you for your recent purchase from {company}.\n\n"
    body += f"Invoice Number: INV-{fake.bothify(text='######')}\n"
    body += f"Date: {fake.date_this_month().strftime('%Y-%m-%d')}\n"
    body += f"Amount: ${amount}.{random.randint(0, 99):02d}\n\n"
    
    body += random.choice([
        "Your account has been charged for this purchase. Please find the invoice details attached.",
        f"Your subscription to {company} has been renewed for another year.",
        f"We have processed your payment for {company} services."
    ])
    
    body += "\n\n"
    body += random.choice([
        "If you did not authorize this charge, please click below to dispute the transaction:\n",
        "To view your invoice details or manage your subscription, please click here:\n",
        "For any questions about this charge, please contact us through the secure customer portal:\n"
    ])
    
    # Generate phishing URL
    phishing_url = f"https://{company.lower().replace(' ', '')}-billing.{fake.domain_word()}.com/invoice"
    body += f"\n{phishing_url}\n\n"
    
    body += "Thank you for your business.\n\n"
    body += f"{company} Billing Team"
    return body

def generate_false_security_alert_body(recipient_name):
    """Generate a phishing email body with a false security alert"""
    platform = random.choice(['Google', 'Microsoft', 'Apple', 'Facebook', 'Amazon', 'PayPal', 'Twitter'])
    greeting = random.choice([f"Dear {recipient_name}", f"Hi {recipient_name}", f"Hello {recipient_name}", "Dear User"])
    
    body = f"{greeting},\n\n"
    body += random.choice([
        f"We detected a new sign-in to your {platform} account from an unknown device.",
        f"Your {platform} account password was recently changed.",
        f"Unusual activity was detected on your {platform} account."
    ])
    
    body += "\n\n"
    body += random.choice([
        f"Device: {random.choice(['Windows PC', 'Mac', 'iPhone', 'Android', 'Linux'])}",
        f"Location: {fake.city()}, {fake.country()}",
        f"IP Address: {fake.ipv4()}"
    ])
    body += f"\nTime: {fake.date_time_this_month().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    body += "If this wasn't you, your account may have been compromised.\n"
    body += "Secure your account immediately by clicking the link below:\n"
    
    # Generate phishing URL
    phishing_url = f"https://{platform.lower()}-account-security.{fake.domain_word()}.com/verify"
    body += f"\n{phishing_url}\n\n"
    
    body += random.choice([
        "This security alert was sent to you automatically. Please do not reply to this email.",
        "For your protection, we recommend changing your password immediately.",
        "If you don't recognize this activity, someone else may be using your account."
    ])
    
    body += "\n\nSincerely,\n"
    body += f"The {platform} Security Team"
    return body

def generate_complete_phishing_body(phishing_type, recipient_name):
    """Generate a complete phishing email body based on type"""
    if phishing_type == 'malware_delivery':
        return generate_malware_delivery_body(recipient_name)
    elif phishing_type == 'urgent_action':
        return generate_urgent_action_body(recipient_name)
    elif phishing_type == 'fake_invoice':
        return generate_fake_invoice_body(recipient_name)
    elif phishing_type == 'false_security_alert':
        return generate_false_security_alert_body(recipient_name)
    else:
        # For types implemented in part 1
        return "Body would be generated in part 1."

def generate_legitimate_email():
    """Generate a fake legitimate email"""
    # Choose an email type
    email_type = random.choice([
        'newsletter', 'order_confirmation', 'subscription', 'personal', 
        'business', 'notification', 'receipt'
    ])
    
    # Generate sender information
    if email_type in ['newsletter', 'order_confirmation', 'subscription', 'notification', 'receipt']:
        companies = [
            ('Amazon', 'amazon.com'),
            ('Netflix', 'netflix.com'),
            ('Microsoft', 'microsoft.com'),
            ('Apple', 'apple.com'),
            ('Google', 'google.com'),
            ('Spotify', 'spotify.com'),
            ('LinkedIn', 'linkedin.com'),
            ('Twitter', 'twitter.com'),
            ('GitHub', 'github.com'),
            ('Dropbox', 'dropbox.com')
        ]
        company, domain = random.choice(companies)
        sender_name = company
        sender_email = f"{random.choice(['info', 'support', 'noreply', 'help', 'service'])}@{domain}"
    else:
        sender_name = fake.name()
        sender_email = fake.email()
    
    # Generate recipient
    recipient_email = fake.email()
    recipient_name = recipient_email.split('@')[0]
    
    # Generate date (within last 30 days)
    date = fake.date_time_between(start_date='-30d', end_date='now').strftime("%a, %d %b %Y %H:%M:%S %z")
    
    # Generate subject line based on email type
    if email_type == 'newsletter':
        subject = random.choice([
            f"{sender_name} Newsletter - {fake.date_this_month().strftime('%B %Y')}",
            f"Your Weekly Update from {sender_name}",
            f"What's New at {sender_name} This Month",
            f"{sender_name} Insider: Tips, News, and Updates"
        ])
    
    elif email_type == 'order_confirmation':
        subject = random.choice([
            f"Your {sender_name} Order Confirmation #{fake.bothify(text='##-######')}",
            f"Thank you for your order from {sender_name}",
            f"Order Confirmation: #{fake.bothify(text='###-####-###')}",
            f"Your order has shipped! Tracking #{fake.bothify(text='??######??')}"
        ])
    
    elif email_type == 'subscription':
        subject = random.choice([
            f"Your {sender_name} subscription has been renewed",
            f"Subscription Confirmation - {sender_name}",
            f"{sender_name} - Payment Receipt",
            f"Your {sender_name} subscription details"
        ])
    
    elif email_type == 'personal':
        subject = random.choice([
            "Hello! How have you been?",
            "Plans for this weekend?",
            "Catching up",
            "Quick question for you",
            "Thought you might find this interesting"
        ])
    
    elif email_type == 'business':
        subject = random.choice([
            "Meeting tomorrow at 10am",
            "Project Update - Q2 Progress",
            "Follow-up on our discussion",
            "New business opportunity",
            "Upcoming team event"
        ])
    
    elif email_type == 'notification':
        subject = random.choice([
            "Your account has been updated",
            f"New sign-in to {sender_name}",
            "Your feedback is important to us",
            "Security update for your account",
            "Important information about your account"
        ])
    
    elif email_type == 'receipt':
        amount = random.randint(5, 200)
        subject = random.choice([
            f"Receipt for your payment of ${amount}.{random.randint(0, 99):02d}",
            f"{sender_name} - Your purchase receipt",
            f"Your receipt from {sender_name}",
            f"Thank you for your purchase of ${amount}.{random.randint(0, 99):02d}"
        ])
    
    # Generate email body based on type
    body = generate_legitimate_body(email_type, recipient_name, sender_name)
    
    # Assemble the email
    email = f"From: {sender_name} <{sender_email}>\nTo: <{recipient_email}>\nDate: {date}\nSubject: {subject}\n\n{body}"
    
    return email, email_type

def generate_legitimate_body(email_type, recipient_name, sender_name):
    """Generate the body of a legitimate email based on type"""
    # Select the appropriate generator based on the email type
    if email_type == 'newsletter':
        return generate_newsletter_body(recipient_name, sender_name)
    elif email_type == 'order_confirmation':
        return generate_order_confirmation_body(recipient_name, sender_name)
    elif email_type == 'subscription':
        return generate_subscription_body(recipient_name, sender_name)
    elif email_type == 'personal':
        return generate_personal_email_body(recipient_name, sender_name)
    elif email_type == 'business':
        return generate_business_email_body(recipient_name, sender_name)
    elif email_type == 'notification':
        return generate_notification_body(recipient_name, sender_name)
    elif email_type == 'receipt':
        return generate_receipt_body(recipient_name, sender_name)
    else:
        return "Generic legitimate email content."

def generate_newsletter_body(recipient_name, sender_name):
    """Generate a newsletter email body"""
    greeting = random.choice([f"Hi {recipient_name}", "Hello", "Hi there", f"Hello {recipient_name}"])
    
    body = f"{greeting},\n\n"
    body += f"Welcome to our {fake.date_this_month().strftime('%B %Y')} newsletter!\n\n"
    
    # Add 2-3 newsletter sections
    for _ in range(random.randint(2, 3)):
        section_title = random.choice([
            "Latest Updates", "What's New", "Featured Products", "Upcoming Events", 
            "Tips & Tricks", "Community Spotlight", "Industry News"
        ])
        body += f"**{section_title}**\n\n"
        
        # Add 1-3 paragraphs for this section
        for _ in range(random.randint(1, 3)):
            body += fake.paragraph() + "\n\n"
    
    body += random.choice([
        "Read more on our website.",
        "Visit our blog for more articles.",
        "Follow us on social media for daily updates."
    ])
    
    body += "\n\nBest regards,\n"
    body += f"The {sender_name} Team\n\n"
    
    # Add unsubscribe information
    body += "---\n"
    body += "You're receiving this email because you signed up for our newsletter.\n"
    body += "To unsubscribe, click here: [Unsubscribe]\n"
    
    return body

def generate_order_confirmation_body(recipient_name, sender_name):
    """Generate an order confirmation email body"""
    greeting = random.choice([f"Hi {recipient_name}", f"Hello {recipient_name}", "Thank you for your order"])
    
    order_number = fake.bothify(text='##-######')
    order_date = fake.date_this_month().strftime('%B %d, %Y')
    
    body = f"{greeting},\n\n"
    body += f"We're writing to confirm your order (#{order_number}).\n\n"
    
    body += "Order Summary:\n"
    body += f"Order Date: {order_date}\n"
    
    # Generate random items
    total = 0
    for _ in range(random.randint(1, 3)):
        item = random.choice([
            "Wireless Headphones", "Smartphone Case", "USB Cable", "Power Bank",
            "Fitness Tracker", "Bluetooth Speaker", "Laptop Sleeve", "Wireless Mouse",
            "Coffee Mug", "T-shirt", "Book", "Subscription Renewal"
        ])
        quantity = random.randint(1, 2)
        price = random.randint(10, 100) + random.randint(0, 99) / 100
        item_total = quantity * price
        total += item_total
        
        body += f"- {item} (Qty: {quantity}) - ${price:.2f}\n"
    
    # Add shipping, tax, and total
    shipping = random.randint(5, 15) + random.randint(0, 99) / 100
    tax = total * 0.08  # 8% tax
    grand_total = total + shipping + tax
    
    body += f"Subtotal: ${total:.2f}\n"
    body += f"Shipping & Handling: ${shipping:.2f}\n"
    body += f"Tax: ${tax:.2f}\n"
    body += f"Total: ${grand_total:.2f}\n\n"
    
    # Add shipping information
    body += "Your order will be shipped to:\n"
    body += f"{fake.name()}\n"
    body += f"{fake.street_address()}\n"
    body += f"{fake.city()}, {fake.state_abbr()} {fake.zipcode()}\n\n"
    
    body += random.choice([
        f"Your order will be delivered within {random.randint(3, 7)} business days.",
        "Thank you for shopping with us!",
        "We appreciate your business."
    ])
    
    body += "\n\nRegards,\n"
    body += f"{sender_name} Customer Service\n"
    body += "For any questions, please contact our support team."
    
    return body

# Helper functions for other email types would follow here
# To keep the file size manageable, we'll implement just the main function

def main():
    """Main function to generate sample data"""
    parser = argparse.ArgumentParser(description='Generate sample phishing and legitimate email data')
    parser.add_argument('--output', type=str, default='data/sample/generated_emails.csv', 
                        help='Output CSV file path')
    parser.add_argument('--count', type=int, default=100, 
                        help='Number of emails to generate (50% phishing, 50% legitimate)')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # For demonstration in this part 2, we'll just print some sample outputs
    print("Sample phishing email (malware delivery):")
    print(generate_malware_delivery_body("user123"))
    print("\n---\n")
    
    print("Sample phishing email (urgent action):")
    print(generate_urgent_action_body("user123"))
    print("\n---\n")
    
    print("Sample legitimate email (newsletter):")
    body = generate_newsletter_body("user123", "TestCompany")
    print(body[:500] + "..." if len(body) > 500 else body)
    
    print("\nTo generate a full dataset, run the complete script.")

if __name__ == "__main__":
    main()