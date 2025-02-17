# A python code for scanning the phishing links 

import re
import string
from urllib.parse import urlparse
from collections import Counter
import math
from difflib import SequenceMatcher

# phishing keywords and suspicious TLD
phishing_keywords = ["login", "logon", "signin", "verify", "verification",
                      "account", "acct", "update", "secure", "upgrade",
                      "security", "safe", "web", "webaccess", "webmail",
                      "confirm", "confirmation", "payment", "pay",
                      "checkout", "bank", "banking", "securebank",
                      "service", "customer-service", "alert", "warning",
                      "support", "helpdesk", "password", "pass", "pwd",
                      "unlock", "reactivate", "validate", "validation",
                      "reset", "recovery", "activity", "suspicious-activity",
                      "online", "onlinebanking", "notice", "notification",
                      "limited", "limitedtime", "expiring", "access",
                      "restricted-access", "funds", "fundtransfer",
                      "statement", "billing", "updateinfo", "info-update",
                      "checkout", "purchase", "reward", "bonus", "prize",
                      "gift", "giftcard", "giveaway", "promo", "promotion"]
suspicious_tlds = [
    ".biz", ".info", ".ru", ".cn", ".pw", ".top", ".work", ".club", ".link",
    ".click", ".xyz", ".online", ".party", ".gq", ".ml", ".ga", ".cf", ".tk",
    ".men", ".stream", ".download", ".racing", ".win", ".bid", ".loan", ".trade",
    ".science", ".accountants", ".date", ".faith", ".press", ".review", ".space",
    ".host", ".website"
]
# Known popular domains to check for typosquatting
popular_domains = ["google.com", "paypal.com", "facebook.com", "amazon.com",
                   "daraz.com", "rokomari.com","bkash.com"]


#calculation of entrophy for randomness detection
def calculate_entrophy(string):
  p = Counter(string)
  lns = float(len(string))
  return -sum(count/lns * math.log2(count/lns) for count in p.values())

# Check the domain is a close match to popular domain using SuquencerMatcher
def is_typosquatting(domain):
    for known_domain in popular_domains:
      ## Compare the domain with the known domains and return True if the ratio is high
        similarity = SequenceMatcher(None, domain, known_domain).ratio()
        if similarity > 0.8 and domain != known_domain:
            return True
    return False

#Main function for analyzing the url
def check_phishing_url(url):
   # breaks down the URL into different parts, like the domain, path, scheme using urlparse
  parsed_url = urlparse(url)
  domain = parsed_url.netloc
  path = parsed_url.path
  warnings = []

  #check for phishing keywords in directory list
  if any(keyword in path.lower() for keyword in phishing_keywords):
    warnings.append("Suspicious keyword found in URL path.")

  #check for suspicious tld
  if any(domain.endswith(tld) for tld in suspicious_tlds):
    warnings.append("Suspicious TLD found in URL")

  #check for IP address in domain
  ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"
  if re.search(ip_pattern, domain):
    warnings.append("URL contains an IP address which is unusual for legitimate sites.")


  #check for unusual characters
  if "@" in url or domain.count('-') >1:
    warnings.append("URL contains unusual characters or multiple hypens.")
  if domain.count('.') > 2:
    warnings.append("Domain has multiple subdomain which is suspicious.")


  #check if url is too long
  if len(url) > 75:
    warnings.append("URL is unusually long which may be suspicious.")

  #check if URL entrophy is high
  if calculate_entrophy(url) > 4.0:
    warnings.append("URL entrophy is very high which means it has include randomness.")

  #check for typosquatting
  if is_typosquatting(domain):
    warnings.append("It is assumed that your domain is very near to close with a popular domain.")

  #check for the url containing secured http(HTTPS) or not
  if not url.startswith("https://"):
    warnings.append("URL does not use HTTPS which can cause security issue")


  #Display result
  if warnings:
    print("URL is not safe for further visit and contains phishing indicators.")
    for warning in warnings:
     print(f" - {warning}")
  else:
    print("URL is safe for further visit.")


#url input
url = input("Enter a url for phishing link scanning:")
check_phishing_url(url)
