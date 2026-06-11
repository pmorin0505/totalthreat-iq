from modules.url_analyzer import analyze_urls, extract_urls
from modules.attachment_analyzer import analyze_attachments
from modules.scoring import cap_score, risk_level, confidence_from_signals
from modules.utils import preview, now_iso
RULES=[("Urgency or pressure",15,["urgent","immediately","right now","act now","final notice","within 24 hours","today only","asap"]),("Credential request",25,["password","login","sign in","verify your account","credentials","username","reset your password"]),("MFA code request",25,["mfa","multi-factor","verification code","one-time code","otp","authenticator code"]),("Account shutdown threat",20,["suspended","locked","closed","disabled","terminated","account will be deleted"]),("Payment or banking request",20,["payment","wire","bank","routing","invoice","ach","payroll","direct deposit"]),("Gift card request",20,["gift card","itunes card","apple card","steam card","google play card"]),("Too-good-to-be-true offer",15,["selected","winner","free","guaranteed","no experience needed","earn $","prize"]),("Social engineering language",15,["do not tell","confidential","keep this between us","are you available","quick favor"]),("Attachment mention",10,["attached","attachment","open the file","see invoice","review document"])]
BRANDS=["microsoft","office 365","paypal","amazon","apple","google","docusign","netflix","facebook","bank of america","chase","wells fargo"]
def detect_message_signals(text):
    low=(text or '').lower(); signals=[]; score=0
    for name,weight,keywords in RULES:
        hits=[k for k in keywords if k in low]
        if hits: signals.append({"name":name,"weight":weight,"detail":"Matched: "+", ".join(hits[:4])}); score+=weight
    brand_hits=[b for b in BRANDS if b in low]
    if brand_hits: signals.append({"name":"Brand reference / possible impersonation","weight":15,"detail":"Brand words found: "+", ".join(brand_hits[:5])}); score+=15
    urls=extract_urls(text)
    if urls: signals.append({"name":"Suspicious link present","weight":20,"detail":f"Found {len(urls)} URL/domain value(s)."}); score+=20
    return signals,score
def classify_category(text,signals,url_results,attachment_results):
    low=(text or '').lower(); names=" ".join(s['name'].lower() for s in signals)
    if any("mfa" in s['name'].lower() for s in signals) or "verification code" in low or "otp" in low: return "MFA code theft"
    if ("password" in low or "login" in low or "verify" in low) and url_results: return "Credential phishing"
    if "gift card" in low: return "Gift card scam"
    if any(x in low for x in ["invoice","payment","wire","ach"]): return "Invoice/payment scam"
    if "payroll" in low or "direct deposit" in low: return "Payroll scam"
    if any(a['score']>=25 for a in attachment_results): return "Malware delivery attempt"
    if "job" in low and any(x in low for x in ["offer","selected","interview","remote"]): return "Fake job scam"
    if any(x in low for x in ["package","delivery","shipment"]): return "Package delivery scam"
    if "brand" in names or "impersonation" in names: return "Brand impersonation"
    if signals: return "General social engineering"
    return "Low-confidence suspicious message"
def recommendation_for(risk,category):
    if risk in ["Critical","High"]: return "Do not click links, open attachments, reply, or provide information. Report the message to IT/security and verify through an official channel."
    if risk=="Medium": return "Use caution. Verify the sender and destination through official channels before taking action. Do not provide credentials or payment information."
    return "No major indicators detected, but verify unexpected messages through official channels."
def build_reasoning(result):
    names=[s['name'] for s in result['detected_signals']]
    if names:
        main=', '.join(names[:5]); return f"This communication may be suspicious because it contains {main}. These indicators can work together to pressure a user into clicking a link, opening a file, sending money, or providing account information. The likely threat category is {result['threat_category']}.", "Simple Explanation: The message has warning signs that attackers commonly use to rush people into unsafe actions. Verify it through a trusted official channel before responding."
    return "No major phishing or social engineering indicators were detected by the current pattern-based rules. This does not prove the message is safe.", "Simple Explanation: Nothing obvious stood out, but unexpected messages should still be verified."
def analyze_message(input_type="Mixed content",sender="",subject="",body="",attachment_names=""):
    combined="\n".join([sender or '',subject or '',body or '',attachment_names or '']); msg_signals,msg_score=detect_message_signals(combined); url_results=analyze_urls(combined); attachment_results=analyze_attachments(attachment_names); signals=list(msg_signals); score=msg_score
    for u in url_results:
        for s in u['signals']: signals.append({**s,"source":u['url']}); score+=s['weight']
    for a in attachment_results:
        for s in a['signals']: signals.append({**s,"source":a['filename']}); score+=s['weight']
    score=cap_score(score); risk=risk_level(score); category=classify_category(combined,signals,url_results,attachment_results)
    result={"timestamp":now_iso(),"input_type":input_type,"sender":sender,"subject":subject,"message_preview":preview(body),"full_message":body,"urls_found":[u['url'] for u in url_results],"attachments_found":[a['filename'] for a in attachment_results],"threat_score":score,"risk_level":risk,"threat_category":category,"detected_signals":signals,"url_results":url_results,"attachment_results":attachment_results,"confidence_level":confidence_from_signals(signals),"recommended_action":recommendation_for(risk,category)}
    result['reasoning_summary'],result['plain_english_explanation']=build_reasoning(result); return result
