import os, re
DANGEROUS={".exe",".bat",".cmd",".scr",".js",".vbs",".ps1",".hta",".jar",".msi"}; MACRO={".docm",".xlsm",".pptm"}; ARCHIVE={".zip",".rar",".7z",".gz"}; DISK={".iso",".img"}; SUSPICIOUS_WORDS=["payroll","urgent","invoice","password","reset","benefits","tax","statement","security","update","wire","payment"]
def split_names(text): return [p.strip() for p in re.split(r"[,;\n]+", text or "") if p.strip()]
def analyze_attachment_name(name):
    n=(name or '').strip(); low=n.lower(); signals=[]; score=0; _,ext=os.path.splitext(low); all_exts=re.findall(r"\.[a-z0-9]{2,5}",low)
    if ext in DANGEROUS: signals.append({"name":"Dangerous attachment extension","weight":25,"detail":f"{ext} files can execute code."}); score+=25
    if ext in MACRO: signals.append({"name":"Macro-enabled Office file","weight":20,"detail":f"{ext} files can contain macros."}); score+=20
    if ext in ARCHIVE: signals.append({"name":"Compressed archive","weight":10,"detail":"Archives can hide risky contents."}); score+=10
    if ext in DISK: signals.append({"name":"Disk image file","weight":20,"detail":"Disk image files are commonly abused for malware delivery."}); score+=20
    if len(all_exts)>=2: signals.append({"name":"Double extension","weight":25,"detail":"The filename appears to use multiple extensions."}); score+=25
    words=[wrd for wrd in SUSPICIOUS_WORDS if wrd in low]
    if words: signals.append({"name":"Suspicious filename wording","weight":10,"detail":"Filename contains: "+", ".join(words)}); score+=10
    risk="Critical" if score>=75 else "High" if score>=50 else "Medium" if score>=25 else "Low"
    return {"filename":n,"extension":ext or "None","score":min(score,100),"risk_level":risk,"signals":signals}
def analyze_attachments(text): return [analyze_attachment_name(n) for n in split_names(text)]
