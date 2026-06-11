import re
from urllib.parse import urlparse
URL_RE = re.compile(r"(?i)\b((?:https?://|www\.)[^\s<>\"]+|[a-z0-9.-]+\.[a-z]{2,}(?:/[^\s<>\"]*)?)")
SHORTENERS={"bit.ly","tinyurl.com","t.co","goo.gl","ow.ly","is.gd","buff.ly","cutt.ly","rebrand.ly"}
SUSPICIOUS_TLDS={"xyz","top","ru","click","zip","mov","country","gq","tk","work","support"}
BRANDS={"microsoft":["microsoft.com","office.com","live.com","outlook.com"],"google":["google.com","gmail.com"],"paypal":["paypal.com"],"apple":["apple.com"],"amazon":["amazon.com"],"facebook":["facebook.com"],"netflix":["netflix.com"]}
KEYWORDS=["login","security","account","verify","password","reset","update","support","billing","unlock","mfa","signin","secure"]
def extract_urls(text):
    found=[]
    for m in URL_RE.finditer(text or ""):
        url=m.group(1).rstrip('.,);]')
        if '@' in url and not url.startswith(('http','www.')): continue
        found.append(url)
    return list(dict.fromkeys(found))
def _domain(url):
    normalized=url if re.match(r"(?i)^https?://", url) else "http://"+url
    parsed=urlparse(normalized)
    return parsed.netloc.lower().split('@')[-1].split(':')[0]
def analyze_url(url):
    signals=[]; score=0; normalized=url if re.match(r"(?i)^https?://", url) else "http://"+url; parsed=urlparse(normalized); domain=_domain(url); path=(parsed.path or "")+("?"+parsed.query if parsed.query else "")
    if parsed.scheme=="http": signals.append({"name":"HTTP link","weight":10,"detail":"The URL does not use HTTPS."}); score+=10
    if domain in SHORTENERS: signals.append({"name":"Shortened URL","weight":15,"detail":"Shortened links hide the final destination."}); score+=15
    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}",domain): signals.append({"name":"IP-based URL","weight":20,"detail":"The URL uses an IP address instead of a normal domain."}); score+=20
    tld=domain.split('.')[-1] if domain else ''
    if tld in SUSPICIOUS_TLDS: signals.append({"name":"Suspicious TLD","weight":15,"detail":f"Domain uses .{tld}, which is often abused in scams."}); score+=15
    if len(domain)>45: signals.append({"name":"Long domain","weight":10,"detail":"The domain is unusually long."}); score+=10
    if domain.count('-')>=2: signals.append({"name":"Hyphen-heavy domain","weight":10,"detail":"Multiple hyphens can be used in impersonation domains."}); score+=10
    lower=(domain+path).lower(); kws=[k for k in KEYWORDS if k in lower]
    if kws: signals.append({"name":"Account/security keywords","weight":15,"detail":"URL contains: "+", ".join(kws)}); score+=15
    for brand,official in BRANDS.items():
        if brand in domain and not any(domain==od or domain.endswith('.'+od) for od in official): signals.append({"name":"Possible brand impersonation","weight":15,"detail":f"'{brand}' appears in a non-official domain."}); score+=15
    if parsed.query and len(parsed.query)>60: signals.append({"name":"Complex query string","weight":10,"detail":"The URL contains a long query string."}); score+=10
    return {"url":url,"domain":domain,"scheme":parsed.scheme,"path":path,"score":min(score,100),"signals":signals}
def analyze_urls(text_or_urls): return [analyze_url(u) for u in extract_urls(text_or_urls)]
