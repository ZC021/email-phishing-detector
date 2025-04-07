import re
import email
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import base64
import quopri

def parse_email_content(raw_email):
    """Parse raw email content and extract features for phishing detection"""
    # Parse the email
    try:
        parsed_email = email.message_from_string(raw_email)
    except:
        # If parsing fails, use the raw content
        return raw_email
    
    # Extract text content
    body = ""
    
    if parsed_email.is_multipart():
        for part in parsed_email.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            
            # Skip attachments
            if 'attachment' in content_disposition:
                continue
            
            if content_type == 'text/plain' or content_type == 'text/html':
                try:
                    payload = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    
                    # If HTML, extract text
                    if content_type == 'text/html':
                        soup = BeautifulSoup(payload, 'html.parser')
                        payload = soup.get_text(separator=' ', strip=True)
                    
                    body += payload + '\n'
                except:
                    # If decoding fails, try to use the encoded content
                    try:
                        payload = part.get_payload()
                        body += payload + '\n'
                    except:
                        pass
    else:
        # Not multipart - get the content directly
        try:
            payload = parsed_email.get_payload(decode=True)
            if payload:
                body = payload.decode('utf-8', errors='ignore')
            else:
                body = parsed_email.get_payload()
        except:
            body = parsed_email.get_payload()
    
    # Extract headers that might be useful for phishing detection
    headers = {
        'From': parsed_email.get('From', ''),
        'To': parsed_email.get('To', ''),
        'Subject': parsed_email.get('Subject', ''),
        'Return-Path': parsed_email.get('Return-Path', ''),
        'X-Mailer': parsed_email.get('X-Mailer', ''),
        'Message-ID': parsed_email.get('Message-ID', '')
    }
    
    # Combine headers with body for feature extraction
    combined_text = f"Subject: {headers['Subject']}\nFrom: {headers['From']}\nTo: {headers['To']}\n\n{body}"
    
    return combined_text

def extract_links(html_content):
    """Extract all links from HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return links

def analyze_urls(urls):
    """Analyze URLs for suspicious patterns"""
    suspicious_count = 0
    suspicious_domains = []
    
    for url in urls:
        if not url:
            continue
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Check for suspicious patterns
            suspicious = False
            
            # IP address instead of domain name
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
                suspicious = True
            
            # Unusual TLDs
            unusual_tlds = ['.xyz', '.top', '.tk', '.ml', '.ga', '.cf']
            if any(domain.endswith(tld) for tld in unusual_tlds):
                suspicious = True
            
            # URL shorteners
            shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd']
            if any(domain == shortener for shortener in shorteners):
                suspicious = True
            
            # Deceptive subdomains
            trusted_domains = ['paypal.com', 'google.com', 'apple.com', 'microsoft.com', 'amazon.com']
            if any(trusted in domain and not domain.endswith(trusted) for trusted in trusted_domains):
                suspicious = True
            
            if suspicious:
                suspicious_count += 1
                suspicious_domains.append(domain)
        except:
            pass
    
    return {
        'total_urls': len(urls),
        'suspicious_urls': suspicious_count,
        'suspicious_domains': suspicious_domains
    }