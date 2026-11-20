"""Vitania Care website generator (v3, client-revised copy). Run: python3 build.py [--fragment-index]"""
import json, os, re, sys

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://naveenfreelancer2829-art.github.io/vitania-care-website/"

# ---- Contact details -------------------------------------------------------
# Official number shared by Prateeksha. It appears in the top bar, page headers,
# contact sections, footer and search data. Change both values and rebuild to update.
PHONE, PHONE_TEL = "+91 91806 06295", "+919180606295"
EMAILS = ["chairman@vitaniacare.com", "prateeksha@vitaniacare.com"]
FORM_TO, FORM_CC = "prateeksha@vitaniacare.com", "chairman@vitaniacare.com"
ADDRESS = ("No. 102, E Block, SLV Karnataka Splendour Apartment, Harinagar Cross, "
           "Kothanur, Konanakunte, Bengaluru – 560062, Karnataka")
GSTIN = "29AAMCV8593N1Z0"
FRAGMENT_INDEX = "--fragment-index" in sys.argv

# ---------- icons ----------
def ic(p):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + p + '</svg>')
I = {
 "check": ic('<path d="M9 3h6v3H9z"/><rect x="5" y="5" width="14" height="16" rx="2"/><path d="M9 13l2 2 4-4"/>'),
 "steth": ic('<path d="M6 3v6a5 5 0 0 0 10 0V3"/><path d="M11 14v2a4 4 0 0 0 8 0v-2"/><circle cx="19" cy="12" r="2"/>'),
 "mind": ic('<path d="M12 21c-4.5 0-8-3.5-8-8a8 8 0 0 1 16 0c0 1.5-.4 2.9-1.1 4.1L20 21h-8z"/><path d="M9.5 11.5a2.5 2.5 0 0 1 5 0c0 1.5-2.5 2-2.5 3.5"/>'),
 "home": ic('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M12 17s-3-1.8-3-3.8a1.6 1.6 0 0 1 3-.8 1.6 1.6 0 0 1 3 .8c0 2-3 3.8-3 3.8z"/>'),
 "video": ic('<rect x="2.5" y="6" width="13" height="12" rx="2.5"/><path d="M15.5 10.5l6-3.5v10l-6-3.5"/>'),
 "camp": ic('<path d="M3 20L12 4l9 16H3z"/><path d="M12 20v-6M9 17h6"/>'),
 "ohc": ic('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M12 7v6M9 10h6M9 21v-4h6v4"/>'),
 "building": ic('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 21v-4h6v4M8 7h2M14 7h2M8 11h2M14 11h2"/>'),
 "lab": ic('<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7.5 15h9"/>'),
 "pulse": ic('<path d="M3 12h4l2-5 4 10 2-5h6"/>'),
 "apple": ic('<path d="M12 7c-2-2-7-1.5-7 4 0 4 3 9 5 9 1 0 1.3-.6 2-.6s1 .6 2 .6c2 0 5-5 5-9 0-5.5-5-6-7-4z"/><path d="M12 7c0-2 1-3.5 3-4"/>'),
 "yoga": ic('<circle cx="12" cy="4.5" r="2"/><path d="M12 7v6M6 10l6 3 6-3M8 21l4-8 4 8"/>'),
 "talk": ic('<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>'),
 "shield": ic('<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6l8-3z"/><path d="M9 12l2 2 4-4"/>'),
 "users": ic('<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14c2.8 0 5 2.2 5 5"/>'),
 "chart": ic('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'),
 "rupee": ic('<path d="M7 5h10M7 9h10M7 5c4 0 6 1.5 6 4s-2 4-6 4l7 6"/>'),
 "nurse": ic('<path d="M6 8V5l6-2 6 2v3"/><path d="M11 5.5h2M12 4.5v2"/><circle cx="12" cy="11" r="3"/><path d="M6 21c0-3.5 2.7-6 6-6s6 2.5 6 6"/>'),
 "physio": ic('<circle cx="13" cy="4.5" r="2"/><path d="M9 21l2-6 3 2v4M7 12l3-4h4l3 3 3-1"/>'),
 "pill": ic('<rect x="3" y="8.5" width="18" height="7" rx="3.5" transform="rotate(-45 12 12)"/><path d="M9.5 9.5l5 5"/>'),
 "bed": ic('<path d="M3 7v12M3 15h18v4M21 15v-3a3 3 0 0 0-3-3h-7v6"/><circle cx="7" cy="11" r="2"/>'),
 "calendar": ic('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
 "lock": ic('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>'),
 "refill": ic('<path d="M20 12a8 8 0 1 1-2.3-5.6"/><path d="M20 4v5h-5"/><path d="M9 12h6M12 9v6"/>'),
}

def img(name, alt, sizes="(max-width:600px) 92vw, (max-width:980px) 46vw, 380px", lazy=True, w=800, h=500):
    srcset = ", ".join(f"assets/photos/{name}-{x}.webp {x}w" for x in (480, 800, 1200))
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return (f'<img src="assets/photos/{name}-800.webp" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{alt}" width="{w}" height="{h}" {load}>')

def mail(e, cls="link"):
    return f'<a class="{cls}" href="mailto:{e}">{e}</a>' if cls else f'<a href="mailto:{e}">{e}</a>'

def ticks(items):
    """Bulleted list in 'Label: description' style."""
    return '<ul class="ticks">' + "".join(f'<li><span><b>{t}:</b> {d}</span></li>' for t, d in items) + '</ul>'

def benefits(items):
    return '<ul class="benefits">' + "".join(
        f'<li><span class="ico">{I[k]}</span><span><b>{t}</b>{d}</span></li>' for k, t, d in items) + '</ul>'

# ---------- navigation ----------
SOLUTIONS = [
 ("employee-wellness.html", "Employee Wellness Program", "OHC, Teleconsultation and year-round wellness"),
 ("health-checkups.html", "Health Check-ups", "Onsite check-ups, camps and lab tests"),
 ("mental-wellbeing.html", "Mental Wellbeing (EAP)", "Confidential counselling for employees"),
 ("home-care.html", "Home Care", "Doctors, nurses and caregivers at home"),
]
SOL_FILES = [s[0] for s in SOLUTIONS]

def header(active):
    sub = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}<small>{d}</small></a></li>' for h, t, d in SOLUTIONS)
    def a(h, t):
        cur = ' aria-current="page"' if h == active else ""
        return f'<a href="{h}"{cur}>{t}</a>'
    sol_cur = ' aria-current="page"' if active in SOL_FILES else ""
    contacts = ([f'<a href="tel:{PHONE_TEL}">{PHONE}</a>'] if PHONE else []) + [mail(e, "") for e in EMAILS]
    return f'''<div class="topbar"><div class="wrap">
  <span>Corporate Health &amp; Wellness Partner, Serving Across India</span>
  <span>{" &nbsp;·&nbsp; ".join(contacts)}</span>
</div></div>
<header class="site"><div class="wrap bar">
  <a class="brand" href="index.html" aria-label="Vitania Care home"><img src="assets/logo.webp" alt="Vitania Care" width="300" height="191"></a>
  <nav class="main" id="nav" aria-label="Main"><ul>
    <li>{a("index.html", "Home")}</li>
    <li class="dd"><a href="employee-wellness.html"{sol_cur}>Solutions</a><ul>{sub}</ul></li>
    <li>{a("about.html", "About Us")}</li>
    <li>{a("contact.html", "Contact Us")}</li>
  </ul></nav>
  <a class="btn btn-primary" href="contact.html">Request a Proposal</a>
  <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
</div></header>'''

def footer():
    contact = ([f'<li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>'] if PHONE else []) + [f'<li>{mail(e, "")}</li>' for e in EMAILS] + [f'<li>{ADDRESS}</li>']
    return f'''<footer class="site"><div class="wrap">
  <div class="foot">
    <div style="display:grid;gap:14px;align-content:start">
      <img src="assets/logo-white.webp" alt="Vitania Care" width="300" height="191" loading="lazy">
      <p>Healthier People, Brighter Workplaces. Occupational health, Employee Wellness Programs and Home Care services for organisations and families across India.</p>
    </div>
    <div><h4>Solutions</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in SOLUTIONS)}</ul></div>
    <div><h4>Company</h4><ul><li><a href="about.html">About Us</a></li><li><a href="contact.html">Contact Us</a></li><li><a href="contact.html">Request a Proposal</a></li></ul></div>
    <div><h4>Contact</h4><ul>{"".join(contact)}</ul></div>
  </div>
  <div class="legal"><span>© 2026 Vitania Care Private Limited. All rights reserved.</span><span>GSTIN: {GSTIN}</span></div>
</div></footer>'''

# ---------- shared blocks ----------
def faq(items, soft=False, intro=""):
    FAQS.extend(items)
    d = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(items))
    return f'''<section{' class="soft"' if soft else ''}><div class="wrap">
  <div class="head"><span class="eyebrow">FAQs</span><h2>Frequently Asked Questions</h2>{f'<p class="lede">{intro}</p>' if intro else ''}</div>
  <div class="faq">{d}</div></div></section>'''

def features(items):
    return '<div class="features">' + "".join(
        f'<div class="feature"><div class="ico">{I[k]}</div><h3>{t}</h3><p>{d}</p></div>' for k, t, d in items) + '</div>'

def steps(items):
    return '<ol class="steps">' + "".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in items) + '</ol>'

def cta(title, text, label="Request a Proposal", href="contact.html"):
    return f'''<section><div class="wrap"><div class="cta"><div><h2>{title}</h2><p>{text}</p></div>
  <a class="btn btn-white" href="{href}">{label}</a></div></div></section>'''

def second_button():
    if PHONE:
        return f'<a class="btn btn-outline" href="tel:{PHONE_TEL}">Call {PHONE}</a>'
    return f'<a class="btn btn-outline" href="mailto:{EMAILS[0]}">Email Us</a>'

def page_hero(crumb, eyebrow, title, lede, photo, alt, cta_label="Request a Proposal", cta_href="#enquire"):
    return f'''<section class="page-hero"><div class="wrap">
  <div class="copy">
    <p class="crumbs"><a href="index.html">Home</a> / {crumb}</p>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
    <div class="cta-row"><a class="btn btn-primary" href="{cta_href}">{cta_label}</a>{second_button()}</div>
  </div>
  <div>{img(photo, alt, "(max-width:900px) 92vw, 520px", lazy=False, w=800, h=600)}</div>
</div></section>'''

PROGRAMS = ["Occupational Health Centre (OHC)", "Annual Health Check-ups", "Onsite Health Check-ups", "Onsite Camps",
            "Teleconsultation", "Lab Tests", "Mental Wellbeing (EAP)", "Webinars &amp; Seminars",
            "Fitness &amp; Yoga", "Nutrition Coaching", "Chronic Care Programs", "Home Care",
            "Caregiver Services", "Medicines &amp; Medical Equipment"]

def form(title, preselect=None, fid="enq"):
    sizes = ["1–50 Employees", "51–200 Employees", "201–500 Employees", "501–1,000 Employees", "More than 1,000 Employees", "Individual or Family"]
    so = "".join(f"<option>{s}</option>" for s in sizes)
    checks = "".join(f'<label><input type="checkbox" name="programs" value="{p.replace("&amp;", "and")}"{" checked" if p == preselect else ""}> {p}</label>' for p in PROGRAMS)
    return f'''<form class="enquiry" id="{fid}" action="https://formsubmit.co/{FORM_TO}" method="POST">
  <div><h3>{title}</h3><p class="note" style="margin-top:6px">Please share your details, and our team will get back to you within one working day.</p></div>
  <input type="hidden" name="_subject" value="New Enquiry from the Vitania Care Website">
  <input type="hidden" name="_cc" value="{FORM_CC}">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_next" value="">
  <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
  <div class="row2">
    <label for="{fid}-name"><span>Full Name <span class="req">*</span></span><input id="{fid}-name" name="name" autocomplete="name" required></label>
    <label for="{fid}-company">Company Name<input id="{fid}-company" name="company" autocomplete="organization"></label>
  </div>
  <div class="row2">
    <label for="{fid}-email"><span>Work Email <span class="req">*</span></span><input id="{fid}-email" name="email" type="email" autocomplete="email" required></label>
    <label for="{fid}-phone"><span>Phone Number <span class="req">*</span></span><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required pattern="[0-9+ ()-]{{8,}}"></label>
  </div>
  <label for="{fid}-size">Number of Employees<select id="{fid}-size" name="employees">{so}</select></label>
  <fieldset><legend>Programs of Interest</legend><div class="checks">{checks}</div></fieldset>
  <label for="{fid}-msg">Message<textarea id="{fid}-msg" name="message" placeholder="Tell us about your team, locations or the support you require."></textarea></label>
  <button class="btn btn-primary" type="submit" style="justify-self:start">Submit Enquiry</button>
  <p class="note form-note">By submitting this form, you agree to be contacted by Vitania Care regarding your enquiry.</p>
</form>'''

def contact_list():
    rows = []
    if PHONE:
        rows.append(f'<div><dt>Phone</dt><dd><a class="link" href="tel:{PHONE_TEL}">{PHONE}</a></dd></div>')
    rows.append('<div><dt>Email</dt><dd>' + "<br>".join(mail(e) for e in EMAILS) + '</dd></div>')
    return rows

def enquire(title, preselect, blurb="Share a few details, and we will recommend a plan that suits your team size, locations and budget."):
    rows = contact_list() + [f'<div><dt>Registered Office</dt><dd>{ADDRESS}</dd></div>']
    return f'''<section id="enquire" class="soft"><div class="wrap contact-grid">
  <div class="info">
    <div class="head" style="margin:0"><span class="eyebrow">Get Started</span><h2>{title}</h2>
      <p class="lede">{blurb}</p></div>
    <dl>{"".join(rows)}</dl>
  </div>
  {form("Request a Proposal", preselect)}
</div></section>'''

# ---------- SEO ----------
FAQS = []
def head(fname, title, desc, crumbs=None, service=None):
    url = SITE + ("" if fname == "index.html" else fname)
    org = {"@type": "MedicalBusiness", "@id": SITE + "#org", "name": "Vitania Care", "legalName": "Vitania Care Private Limited",
           "slogan": "Healthier People, Brighter Workplaces", "url": SITE, "logo": SITE + "assets/logo.png", "image": SITE + "assets/og-image.jpg",
           "email": EMAILS[0], "taxID": GSTIN,
           "address": {"@type": "PostalAddress", "streetAddress": "No. 102, E Block, SLV Karnataka Splendour Apartment, Harinagar Cross, Kothanur, Konanakunte",
                       "addressLocality": "Bengaluru", "addressRegion": "Karnataka", "postalCode": "560062", "addressCountry": "IN"},
           "areaServed": {"@type": "Country", "name": "India"},
           "founder": [{"@type": "Person", "name": "Sanjeet Kumar", "jobTitle": "Founder & CEO"},
                       {"@type": "Person", "name": "Prateeksha Devadiga", "jobTitle": "Co-Founder & Head of Operations"}]}
    if PHONE:
        org["telephone"] = PHONE
    graph = [org, {"@type": "WebPage", "url": url, "name": title, "description": desc, "inLanguage": "en-IN", "about": {"@id": SITE + "#org"}}]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h} for i, (n, h) in enumerate(crumbs)]})
    if service:
        graph.append({"@type": "Service", "name": service, "provider": {"@id": SITE + "#org"}, "areaServed": "India", "url": url})
    if FAQS:
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in FAQS]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    return f'''<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0B3D6B">
<meta property="og:type" content="website"><meta property="og:site_name" content="Vitania Care"><meta property="og:locale" content="en_IN">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300;12..96,400;12..96,500;12..96,600;12..96,700&display=swap">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{ld}</script>'''

def write(fname, title, desc, body, crumbs=None, service=None):
    h = head(fname, title, desc, crumbs, service)
    FAQS.clear()
    content = f'{header(fname)}\n<main>\n{body}\n</main>\n{footer()}\n<script src="site.js" defer></script>'
    if fname == "index.html" and FRAGMENT_INDEX:
        html = h + "\n" + content
    else:
        html = f'<!doctype html>\n<html lang="en-IN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{h}\n</head>\n<body>\n{content}\n</body>\n</html>\n'
    open(os.path.join(OUT, fname), "w").write(html)

WIDE = "(max-width:900px) 92vw, 560px"

# ================= HOME =================
home_faq = [
 ("What does Vitania Care offer?", "For organisations, we offer Occupational Health Centres (OHC), Onsite Health Check-ups, Onsite Camps, Teleconsultation, Lab Tests, Mental Wellbeing support and Employee Wellness Programs. For individuals and families, we provide Home Care and Caregiver Services. Organisations can choose individual services or a comprehensive year-round program."),
 ("Can individuals and families use your services?", "Yes. Individuals and families can book Home Care, Caregiver Services, physiotherapy, lab tests at home, and medicines and medical equipment directly with us."),
 ("Can the program be customised for our organisation?", "Yes. Every program is planned around your team size, office locations, work shifts, health priorities and budget."),
 ("Do you work with small companies and start-ups?", "Yes. We work with organisations of all sizes, from early-stage start-ups to large enterprises with multiple offices."),
 ("Is employee health data kept confidential?", "Yes. Individual health records are shared only with the employee concerned. Employers receive anonymised, summary-level reports."),
 ("Which locations do you cover?", "We cover locations across India. Onsite services, such as Occupational Health Centres, Onsite Health Check-ups and Onsite Camps, are arranged at your office locations, while Teleconsultation, counselling, webinars and seminars are available nationwide."),
]
cards = [
 ("employee-wellness.html#ohc", "ohc-clinic", "Doctor consulting an employee at an Occupational Health Centre", "Occupational Health Centre (OHC)", "A comprehensive, professionally managed healthcare facility at your workplace, staffed by qualified doctors and nurses to provide accessible medical care, employee health monitoring and occupational health support."),
 ("health-checkups.html", "bp-check", "Doctor measuring an employee's blood pressure during a health check-up", "Onsite Health Check-ups", "Workplace health screenings, annual and pre-employment check-ups, with doctor-reviewed reports."),
 ("health-checkups.html#camps", "medical-camp", "Doctors attending to employees at an onsite health camp", "Onsite Medical Camps", "Onsite deployment of qualified MBBS and specialist doctors for workplace health camps."),
 ("employee-wellness.html#teleconsultation", "online-doctor", "Doctor greeting a patient during a video consultation", "Teleconsultation", "Convenient phone and video consultations with general physicians and specialists."),
 ("health-checkups.html#lab-tests", "lab-test", "Laboratory technician examining a blood sample", "Laboratory &amp; Diagnostic Services", "Pathology and radiology services with convenient onsite and home sample collection."),
 ("mental-wellbeing.html", None, "", "Mental Wellbeing (EAP)", "Confidential counselling and wellness workshops for employees and their families."),
 ("employee-wellness.html", "nutrition-guidance", "Nutritionist explaining a balanced diet plan to a client", "Employee Wellness Programs", "Year-round wellness initiatives covering fitness, yoga, nutrition, webinars and chronic care management."),
 ("home-care.html", "doctor-home-visit", "Doctor examining an elderly man at home", "Home Healthcare", "Doctor and nursing visits, physiotherapy, lab tests and medicine delivery at home."),
 ("home-care.html#caregivers", "nurse-elderly-care", "Caregiver holding the hand of an elderly woman", "Caregiver Services", "Trained caregivers providing personal care, mobility assistance and daily living support at home."),
]
def card_media(p, a):
    return img(p, a) if p else f'<div class="card-art">{I["mind"]}</div>'
card_html = '<div class="cards">' + "".join(
    f'<article class="card">{card_media(p, a)}<div class="body"><h3>{t}</h3><p>{d}</p><a class="link" href="{h}">Learn More →</a></div></article>'
    for h, p, a, t, d in cards) + '</div>'

home = f'''<section class="hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <span class="eyebrow">Corporate Health &amp; Wellness Partner Across India</span>
    <h1>Your Trusted Partner for <span class="accent">Employee Health and Wellness</span></h1>
    <p class="lede">Vitania Care delivers comprehensive healthcare solutions to organisations across India, including Occupational Health Centres (OHCs), Onsite Health Check-ups, Doctor Teleconsultation, Laboratory Testing, Vaccination Drives, Food Handler Health Checks and Employee Wellness Programs.</p>
    {ticks([("Pan-India Coverage", "Seamless delivery of onsite and digital healthcare services for organisations across India."),
            ("Qualified Healthcare Professionals", "Access to a multidisciplinary team of MBBS and specialist doctors, nurses, counsellors, physiotherapists and nutritionists."),
            ("Single Point of Contact", "A dedicated team to manage coordination, planning, scheduling, service delivery and reporting, ensuring a smooth and hassle-free healthcare experience.")])}
    <div class="cta-row"><a class="btn btn-primary" href="contact.html">Request a Proposal</a><a class="btn btn-outline" href="#solutions">Explore Our Solutions</a></div>
  </div>
  <div class="hero-media">
    {img("doctor-bp-check", "Doctor checking a patient's blood pressure during a health check-up", "(max-width:900px) 92vw, 560px", lazy=False, w=800, h=640)}
  </div>
</div></section>

<div class="pillars"><div class="wrap"><ul>
  <li><span class="ico">{I["ohc"]}</span><span><b>Occupational Health Centre (OHC)</b><small>Medical care at your workplace</small></span></li>
  <li><span class="ico">{I["video"]}</span><span><b>Teleconsultation</b><small>General physicians and specialist doctors</small></span></li>
  <li><span class="ico">{I["mind"]}</span><span><b>Mental Wellbeing</b><small>Confidential counselling support</small></span></li>
  <li><span class="ico">{I["home"]}</span><span><b>Home Care</b><small>Medical care at your doorstep</small></span></li>
</ul></div></div>

<section class="soft"><div class="wrap">
  <div class="head center"><span class="eyebrow">Who We Serve</span><h2>Comprehensive Healthcare for Businesses and Families</h2>
    <p class="lede">Whether you are an organisation seeking integrated employee healthcare solutions or a family looking for personalised care at home, Vitania Care offers dependable, end-to-end healthcare services designed around your needs — delivered with expertise, convenience and compassion.</p></div>
  <div class="audience">
    <div class="aud aud-org">
      <span class="ico">{I["building"]}</span>
      <h3>For Organisations</h3>
      <p><b>Comprehensive Corporate Healthcare &amp; Employee Wellness Solutions</b></p>
      <p>Empowering organisations to build healthier, safer and more productive workplaces through integrated healthcare services, preventive health initiatives and employee wellbeing programs. Our tailored solutions are designed to support workforce health, enhance employee engagement and simplify healthcare management.</p>
      {ticks([("Occupational Health Centre (OHC) Management", "End-to-end setup, management and staffing of workplace healthcare centres to support occupational health and employee medical needs."),
              ("Onsite Health Check-ups &amp; Doctor Deployment", "Workplace health screenings, medical assessments and deployment of qualified doctors to ensure convenient and accessible healthcare for employees."),
              ("Teleconsultation &amp; Laboratory Services", "Convenient access to medical consultations and reliable diagnostic testing through integrated healthcare solutions."),
              ("Employee Wellness &amp; Mental Wellbeing (EAP)", "Holistic wellness initiatives encompassing physical fitness, nutrition, stress management, counselling and employee assistance programs to promote overall wellbeing.")])}
      <a class="btn btn-white" href="contact.html">Request a Proposal</a>
    </div>
    <div class="aud aud-family">
      <span class="ico">{I["home"]}</span>
      <h3>For Individuals &amp; Families</h3>
      <p><b>Personalised Home Healthcare &amp; Compassionate Care Services</b></p>
      <p>Access professional medical care, personalised assistance and reliable healthcare support in the comfort of your home. Vitania Care connects individuals, senior citizens, patients and families with trusted healthcare professionals and essential healthcare services, making home-based care convenient, comfortable and dependable.</p>
      {ticks([("Doctor &amp; Nursing Care at Home", "Professional medical consultations, nursing assistance and clinical care delivered at home by qualified healthcare professionals."),
              ("Caregiver Services", "Compassionate and dependable caregivers to support senior citizens, patients and individuals who require assistance with daily activities and personal care."),
              ("Physiotherapy at Home", "Personalised physiotherapy and rehabilitation services to support recovery, improve mobility, restore strength and enhance overall wellbeing."),
              ("Lab Tests, Medicines &amp; Medical Equipment", "Convenient access to diagnostic tests, prescribed medicines and essential medical equipment, delivered or arranged to support your healthcare needs at home.")])}
      <a class="btn btn-primary" href="home-care.html#enquire">Arrange Home Care</a>
    </div>
  </div>
</div></section>

<section id="solutions"><div class="wrap">
  <div class="head"><span class="eyebrow">Our Solutions</span><h2>Comprehensive Healthcare Solutions for Your Workforce and Their Families</h2>
    <p class="lede">Vitania Care delivers tailored healthcare solutions to support your workforce and their families. Choose individual services or integrated healthcare programs, seamlessly managed end to end by our team.</p></div>
  {card_html}
</div></section>

<section class="soft"><div class="wrap split">
  <div class="media">{img("bp-monitor", "Doctor measuring a patient's blood pressure", WIDE, w=800, h=600)}</div>
  <div class="copy">
    <span class="eyebrow">Why Vitania Care?</span>
    <h2>Healthcare Made Simple. Workforce Wellbeing Made Better.</h2>
    <p class="lede">We manage healthcare planning, professional deployment and ongoing coordination, enabling your HR team to focus on employee engagement while we take care of workforce wellbeing.</p>
    {benefits([("rupee", "Optimised Healthcare Costs", "Preventive screenings and timely interventions help manage long-term healthcare expenses."),
                ("chart", "Improved Workforce Productivity", "Proactive healthcare promotes employee wellbeing, reduces avoidable absenteeism and enhances productivity."),
                ("users", "Enhanced Employee Benefits", "Comprehensive healthcare support for employees and their families strengthens employee satisfaction and retention."),
                ("lock", "Confidential &amp; Secure", "Employee health information is treated with strict confidentiality, with employers receiving anonymised health reports.")])}
  </div>
</div></section>

<section><div class="wrap">
  <div class="head"><span class="eyebrow">How It Works</span><h2>A Seamless Journey from Planning to Healthcare Delivery</h2></div>
  {steps([("Understand Your Needs", "We assess your workforce, locations, operational requirements and healthcare priorities."),
          ("Design Your Program", "We develop a customised healthcare plan with defined services, schedules and transparent pricing."),
          ("Deliver Healthcare Services", "Our qualified doctors, nurses and wellness professionals ensure seamless service execution."),
          ("Monitor &amp; Improve", "Periodic reports and performance reviews help track engagement, assess outcomes and improve program effectiveness.")])}
</div></section>

<section class="band"><div class="wrap">
  <div class="head"><span class="eyebrow">Industries We Serve</span><h2>Healthcare Solutions Across Diverse Industries</h2>
    <p class="lede">We deliver customised healthcare solutions designed to meet the unique workforce requirements of diverse industries across India.</p></div>
  {features([("building", "IT &amp; Technology", "Employee wellness, stress management, posture care and lifestyle health support."),
             ("users", "Manufacturing &amp; Operations", "Occupational Health Centres, onsite medical support, health screenings and first-aid services."),
             ("chart", "Banking, Finance &amp; Corporate Services", "Preventive health check-ups, mental wellbeing and employee wellness programs."),
             ("pulse", "Start-ups &amp; Growing Businesses", "Flexible and scalable healthcare solutions aligned with workforce growth and business needs."),
             ("calendar", "Hospitality &amp; Retail", "Pre-employment medical check-ups, food handler health assessments and periodic employee screenings."),
             ("home", "Employee Families", "Accessible home healthcare, nursing, physiotherapy and caregiver services for employees' families.")])}
</div></section>
{faq(home_faq, intro="Find answers to common questions about our corporate healthcare solutions, service delivery, employee wellness programs and home healthcare services.")}
{cta("Ready to Build a Healthier Workforce?", "Tell us about your organisation, and we will share a wellness plan and proposal tailored to your requirements.")}'''
write("index.html", "Vitania Care | Corporate Health & Wellness Partner Across India",
      "Corporate health and wellness services across India: Occupational Health Centres, Onsite Health Check-ups, Onsite Camps, Teleconsultation, Lab Tests, Mental Wellbeing support and Home Care.", home)

# ================= EMPLOYEE WELLNESS PROGRAM =================
ew_faq = [
 ("What does a typical corporate wellness programme include?", "Our programmes may include Occupational Health Centres, Onsite Health Check-ups, Teleconsultations, health webinars, fitness and nutrition sessions, and chronic disease management. Each programme is customised to your workforce's healthcare requirements."),
 ("Can the programme support remote and hybrid employees?", "Yes. Teleconsultations, webinars, counselling, and nutrition coaching can be delivered virtually, ensuring healthcare access for remote and hybrid employees across India."),
 ("How do you measure programme effectiveness?", "We monitor employee participation, health screening outcomes, and follow-up activities, providing quarterly anonymised reports to help HR teams assess programme performance."),
 ("How soon can we launch the programme?", "Implementation timelines depend on the services selected and operational requirements. Most standard programmes can be initiated within a few weeks of confirmation."),
]
ew = f'''{page_hero("Employee Wellness Program", "Employee Wellness Program", "Comprehensive Workplace Wellness Programs", "We deliver integrated, year-round employee wellness solutions encompassing Occupational Health Centres, Onsite Health Check-ups, Teleconsultations, fitness, nutrition, and mental wellbeing initiatives. From programme planning to execution and performance reporting, we manage every aspect to promote a healthier, more productive workforce.", "nutrition-guidance", "Nutritionist explaining a balanced diet chart to a client")}
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Program Inclusions</span><h2>Integrated Healthcare &amp; Wellness Solutions for Your Workforce</h2>
    <p class="lede">Choose individual services or combine them into a customised annual employee wellness programme.</p></div>
  {features([("ohc", "Occupational Health Centre (OHC)", "End-to-end management of workplace medical centres with qualified doctors and nursing staff."),
             ("check", "Onsite Health Check-ups", "Workplace health screenings covering blood pressure, blood sugar, BMI, vision, and dental assessments."),
             ("camp", "Onsite Medical Camps", "Deployment of MBBS and specialist doctors to provide workplace medical services."),
             ("video", "Teleconsultation", "Convenient phone and video consultations with general physicians and specialists."),
             ("lab", "Pathology &amp; Radiology", "Comprehensive diagnostic services with onsite and home sample collection."),
             ("talk", "Health Webinars &amp; Seminars", "Expert-led sessions on preventive healthcare, lifestyle diseases, sleep, and workplace wellness."),
             ("yoga", "Fitness &amp; Yoga", "Workplace and virtual fitness, yoga, and guided stretching sessions."),
             ("apple", "Nutrition Coaching", "Personalised dietary guidance and nutrition consultations by qualified nutritionists."),
             ("pulse", "Chronic Disease Management", "Ongoing healthcare support for diabetes, hypertension, thyroid disorders, and weight management.")])}
</div></section>
<section id="ohc" class="soft"><div class="wrap split">
  <div class="media">{img("ohc-clinic", "Doctor consulting an employee at an Occupational Health Centre", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Occupational Health Centre (OHC)</span><h2>Comprehensive Medical Facilities at Your Workplace</h2>
    <p class="lede">We provide end-to-end setup and management of Occupational Health Centres at your premises, ensuring employees have convenient access to timely medical care, preventive health services, and emergency support without leaving the workplace.</p>
    {ticks([("Qualified Medical Professionals", "Deployment of experienced MBBS doctors and trained nursing staff, with schedules aligned to your operational hours and shift requirements."),
            ("First Aid &amp; Emergency Response", "Immediate medical assistance, first aid management, and coordination with nearby hospitals during medical emergencies."),
            ("Medical Examinations &amp; Health Records", "Pre-employment and periodic medical assessments, along with secure and confidential employee health record management.")])}</div>
</div></section>
<section id="teleconsultation"><div class="wrap split rev">
  <div class="media">{img("online-doctor", "Doctor greeting a patient during a video consultation", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Teleconsultation Services</span><h2>Convenient Access to General Physicians &amp; Specialist Doctors</h2>
    <p class="lede">We provide seamless access to qualified general physicians and specialist doctors through phone and video consultations, enabling employees to receive timely medical advice without disrupting their work schedules or visiting hospitals.</p>
    {benefits([("steth", "General Physician Consultations", "Medical consultations for common illnesses, infections, lifestyle-related conditions, and routine health concerns."),
               ("users", "Specialist Consultations", "Access to experienced specialists for further evaluation, expert medical opinions, and condition-specific guidance."),
               ("pill", "Digital Prescriptions &amp; Follow-ups", "Online prescriptions, medicine delivery support, and follow-up consultations to ensure continuity of care.")])}</div>
</div></section>
<section id="fitness" class="soft"><div class="wrap split">
  <div class="media">{img("physiotherapy", "Physiotherapist guiding a man through a resistance-band exercise", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Fitness &amp; Recovery</span><h2>Promoting Movement, Fitness &amp; Workplace Wellbeing</h2>
    <p class="lede">We offer professionally guided fitness and recovery programmes to reduce work-related physical discomfort, improve mobility, and encourage healthier workplace habits.</p>
    {ticks([("Ergonomic Assessments", "Workstation evaluations and posture improvement guidance."),
            ("Physiotherapy Support", "Professional care for back, neck, and joint-related concerns."),
            ("Fitness Initiatives", "Engaging fitness challenges and wellness activities to promote an active workforce.")])}</div>
</div></section>
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Our Approach</span><h2>A Structured, End-to-End Wellness Management Approach</h2></div>
  {steps([("Assess", "Evaluate workforce health requirements, organisational priorities, and existing healthcare benefits."),
          ("Plan", "Develop a customised 12-month wellness calendar with defined activities, timelines, and transparent pricing."),
          ("Deliver", "Seamlessly coordinate and execute all wellness initiatives, medical camps, consultations, and employee engagement activities."),
          ("Report", "Provide quarterly, anonymised performance and wellness reports to track programme effectiveness and employee engagement.")])}
</div></section>
{faq(ew_faq, soft=True)}
{enquire("Plan a Wellness Program for Your Team", "Occupational Health Centre (OHC)")}'''
write("employee-wellness.html", "Employee Wellness Program | Vitania Care",
      "Employee Wellness Programs across India: Occupational Health Centres, Onsite Health Check-ups, Onsite Camps, Teleconsultation, lab tests, webinars and seminars, fitness, nutrition and chronic care.", ew,
      [("Home", ""), ("Employee Wellness Program", "employee-wellness.html")], "Employee Wellness Program")

# ================= HEALTH CHECK-UPS =================
hc_faq = [
 ("Where can employees undergo health check-ups?", "Health check-ups can be organised at your corporate premises through onsite screening programmes, at our partnered diagnostic centres, or through convenient home-based sample collection services."),
 ("Will employees receive their medical reports and consultation?", "Yes. Every employee receives a digital copy of their medical report. Qualified doctors review the reports, explain the findings, and provide appropriate medical guidance and follow-up recommendations wherever required."),
 ("Can you accommodate urgent pre-employment medical examinations?", "Absolutely. We facilitate timely scheduling and completion of pre-employment medical examinations to support smooth employee onboarding and minimise delays in joining formalities."),
 ("Is fasting required before health check-ups?", "Certain blood investigations may require 8–12 hours of fasting. Employees are provided with the necessary test preparation guidelines and instructions in advance to ensure accurate results."),
]
hc = f'''{page_hero("Health Check-ups", "Health Check-ups", "Preventive Healthcare Services for Early Detection and Proactive Care", "We offer comprehensive preventive healthcare solutions, including Annual Health Check-ups, Pre-employment Medical Examinations, Food Handler Medical Tests, Onsite Health Screenings, and Pathology and Radiology Services. All medical reports are reviewed by qualified doctors, with consultations and clinical guidance provided whenever required.", "bp-check", "Doctor measuring an employee's blood pressure during a health check-up")}
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Our Check-up Services</span><h2>Comprehensive Health Screening Across Every Stage of Employment</h2></div>
  {features([("check", "Annual Health Check-ups", "Comprehensive preventive health packages covering essential blood investigations, ECG, vision screening, and doctor consultations to support early detection and overall health monitoring."),
             ("users", "Pre-employment Medical Examinations", "Structured medical assessments to evaluate candidates' fitness for employment, ensuring timely completion and efficient onboarding."),
             ("building", "Onsite Health Screenings", "Workplace-based health assessments, including blood pressure, blood glucose, BMI, vision, and dental screenings, for convenient employee health monitoring."),
             ("camp", "Onsite Medical Camps", "Deployment of qualified MBBS and specialist doctors at corporate premises to conduct medical camps and provide accessible healthcare services."),
             ("lab", "Pathology &amp; Radiology Services", "Comprehensive diagnostic services, including pathology investigations and radiology tests, with convenient onsite and home-based sample collection facilities."),
             ("steth", "Doctor-Reviewed Reports &amp; Consultations", "Medical reports reviewed by qualified doctors, with professional interpretation, consultations, and appropriate follow-up recommendations wherever required.")])}
</div></section>
<section id="camps" class="soft"><div class="wrap split">
  <div class="media">{img("medical-camp", "Doctors attending to employees at an onsite health camp", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Onsite Medical Camps</span><h2>Expert Medical Care, Delivered to Your Workplace</h2>
    <p class="lede">We provide comprehensive onsite healthcare services by deploying qualified MBBS and specialist doctors, along with trained medical technicians and the necessary equipment. Our camps are scheduled around your organisation’s working hours to ensure seamless healthcare access with minimal disruption to business operations.</p>
    {ticks([("Specialist Medical Support", "Deployment of experienced specialists based on your employees’ healthcare requirements."),
            ("Flexible Deployment", "Customised medical camps designed to accommodate individual teams, departments, or the entire workforce."),
            ("Convenient Scheduling", "Flexible appointment slots aligned with workplace schedules to ensure smooth operations."),
            ("Medical Consultations &amp; Follow-ups", "Professional consultations and appropriate follow-up guidance for employees requiring further medical attention.")])}</div>
</div></section>
<section id="lab-tests"><div class="wrap split rev">
  <div class="media">{img("lab-test", "Laboratory technician examining a blood sample beside a microscope", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Diagnostic Services – Pathology &amp; Radiology</span><h2>Comprehensive Diagnostic Solutions at Your Convenience</h2>
    <p class="lede">We facilitate a wide range of pathology and radiology services through our network of trusted laboratory and diagnostic partners, ensuring reliable testing, convenient sample collection, and timely delivery of reports. Services are available at corporate premises and employees’ homes for greater accessibility and convenience.</p>
    {ticks([("Pathology Services", "Comprehensive blood, urine, and other laboratory investigations, with reports delivered digitally."),
            ("Radiology Services", "Access to diagnostic imaging services, including X-rays, ultrasound, and other radiological investigations through our partner diagnostic centres."),
            ("Onsite &amp; Home Sample Collection", "Convenient sample collection at workplaces and residences by trained healthcare professionals."),
            ("Timely Reporting", "Efficient coordination with diagnostic partners to facilitate timely report delivery and seamless access to diagnostic results.")])}</div>
</div></section>
<section class="soft"><div class="wrap">
  <div class="head"><span class="eyebrow">How It Works</span><h2>A Seamless Healthcare Experience for HR Teams and Employees</h2>
    <p class="lede">Our streamlined process ensures convenient coordination, efficient service delivery, and professional medical support at every stage.</p></div>
  {steps([("Package Selection", "We recommend customised health check-up packages based on employees’ age groups, job roles, medical requirements, and occupational health risks."),
          ("Scheduling &amp; Coordination", "We coordinate appointments and testing schedules, offering employees the flexibility to access services at their workplace, designated diagnostic centres, or their homes."),
          ("Health Screening &amp; Diagnostics", "All medical examinations, diagnostic tests, and sample collections are conducted by qualified healthcare professionals using appropriate equipment and established protocols."),
          ("Medical Review &amp; Follow-up", "Medical reports are reviewed by qualified doctors, with professional consultations, interpretation of results, and follow-up recommendations provided wherever necessary.")])}
</div></section>
{faq(hc_faq)}
{enquire("Comprehensive Healthcare Solutions for Your Workforce", "Annual Health Check-ups", "Partner with us to provide accessible, reliable, and professionally managed healthcare services for your employees. Share your organisation's requirements, and our team will recommend a customised healthcare programme based on your workforce size, locations, medical requirements, and budget. Connect with us to design the right healthcare solution for your organisation.")}'''
write("health-checkups.html", "Preventive Health Check-ups for Employees | Vitania Care",
      "Comprehensive preventive healthcare solutions, including annual and pre-employment health check-ups, onsite medical camps with MBBS and specialist doctors, and pathology and radiology services with convenient onsite and home sample collection.", hc,
      [("Home", ""), ("Health Check-ups", "health-checkups.html")], "Employee Health Check-ups")

# ================= MENTAL WELLBEING =================
mw_faq = [
 ("Are counselling sessions confidential?", "Yes. All sessions are strictly confidential. Employee participation and personal discussions are not disclosed to employers."),
 ("Who can access the service?", "All employees covered under the programme are eligible. Family members can also be included based on the selected plan."),
 ("How can employees book a session?", "Employees can contact our support team to schedule phone, video, or in-person counselling at their convenience."),
 ("What concerns can counsellors address?", "Counselling support covers stress, anxiety, emotional wellbeing, relationship challenges, parenting, grief, workplace pressure, and work–life balance."),
]
mw = f'''{page_hero("Mental Wellbeing", "Employee Assistance Program (EAP)", "Confidential Counselling for a Healthier, More Resilient Workforce", "We provide confidential mental health and emotional wellbeing support through qualified counsellors, helping employees navigate workplace stress, anxiety, personal challenges, and emotional concerns. Employees can access professional counselling through flexible phone, video, or in-person sessions, ensuring convenient, compassionate, and personalised support.", "online-doctor", "Counsellor smiling and waving during a video session")}
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Program Inclusions</span><h2>Comprehensive Mental Health &amp; Wellbeing Support</h2></div>
  {features([("talk", "One-to-One Counselling", "Confidential counselling sessions with qualified psychologists and mental health professionals."),
             ("users", "Family Counselling", "Wellbeing support extended to employees and their immediate family members."),
             ("mind", "Stress Management Workshops", "Interactive sessions on stress management, burnout prevention, sleep, and emotional wellbeing."),
             ("users", "Manager Training", "Equipping managers to identify early signs of distress and provide appropriate support."),
             ("shield", "Critical Incident Support", "Timely psychological support for employees and teams following critical or traumatic events."),
             ("chart", "Anonymised Wellbeing Insights", "Confidential, aggregated insights to help HR teams strengthen workplace wellbeing initiatives.")])}
</div></section>
<section class="soft"><div class="wrap">
  <div class="head"><span class="eyebrow">Why It Matters</span><h2>Supporting Employee Wellbeing, Strengthening Workplace Performance</h2>
    <p class="lede">Proactive mental health support helps reduce workplace stress, improve employee engagement, and enhance productivity, wellbeing, and retention.</p></div>
  {features([("video", "Flexible Access", "Confidential counselling through phone, video, or in-person sessions at convenient times."),
             ("calendar", "Easy Scheduling", "A simple and hassle-free appointment booking process for employees."),
             ("lock", "Strict Confidentiality", "All counselling sessions and personal information are handled with the utmost privacy and confidentiality.")])}
</div></section>
{faq(mw_faq)}
{enquire("Set Up an Employee Assistance Program", "Mental Wellbeing (EAP)")}'''
write("mental-wellbeing.html", "Employee Assistance Program (EAP) | Vitania Care",
      "Confidential employee counselling, stress and resilience workshops, manager training and family support through the Vitania Care Employee Assistance Program.", mw,
      [("Home", ""), ("Mental Wellbeing", "mental-wellbeing.html")], "Employee Assistance Program")

# ================= HOME CARE =================
hm_faq = [
 ("How quickly can home care services be arranged?", "Visits can often be scheduled within 24 hours, subject to availability and location."),
 ("Do home care services cover medical emergencies?", "No. In an emergency, please contact ambulance services or visit the nearest hospital."),
 ("What support do caregivers provide?", "Caregivers assist with personal care, mobility, feeding, medication reminders and companionship."),
 ("Can I rent medical equipment?", "Yes. Wheelchairs, walkers, hospital beds and oxygen concentrators are available on rent."),
 ("Can organisations offer home care to employees and their families?", "Yes. Organisations can include our home healthcare services as part of their employee wellness benefits."),
]
hm = f'''{page_hero("Home Care", "Home Care", "Professional Medical Care in the Comfort of Your Home", "We deliver comprehensive home healthcare, including doctor and nursing visits, caregiver support, physiotherapy, lab tests and medicine delivery, ensuring convenient and personalised care at home.", "doctor-home-visit", "Doctor checking an elderly man's heartbeat at home while his wife looks on")}
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Home Healthcare Services</span><h2>Professional Medical Care, Delivered to Your Doorstep</h2>
    <p class="lede">Access reliable medical care and personalised support in the comfort of your home.</p></div>
  {features([("steth", "Doctor Visits at Home", "Qualified physicians providing home consultations, medical assessments and prescriptions."),
             ("nurse", "Nursing Care", "Professional nursing support for injections, wound dressing, IV therapy and post-operative care."),
             ("users", "Caregiver Services", "Trained caregivers assisting with personal care, mobility and daily activities."),
             ("physio", "Physiotherapy at Home", "Personalised rehabilitation for post-surgical, post-injury and post-stroke recovery."),
             ("lab", "Lab Tests at Home", "Home sample collection for laboratory tests, with reports shared digitally."),
             ("bed", "Medical Equipment on Rent", "Hospital beds, wheelchairs and oxygen concentrators provided on a rental basis.")])}
</div></section>
<section id="caregivers" class="soft"><div class="wrap split">
  <div class="media">{img("nurse-elderly-care", "Caregiver holding the hand of an elderly woman resting in bed", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Caregiver Services</span><h2>Compassionate, Professional Care at Home</h2>
    <p class="lede">Our trained caregivers provide personalised assistance to senior citizens and patients, ensuring comfort, dignity, safety and support in their daily lives.</p>
    {benefits([("users", "Personal Care", "Assistance with bathing, grooming, dressing and hygiene."),
               ("physio", "Mobility &amp; Daily Support", "Help with walking, transfers, feeding and everyday activities."),
               ("pill", "Medication Reminders &amp; Companionship", "Timely reminders, routine support and compassionate companionship."),
               ("calendar", "Flexible Care Plans", "Customised short-term and long-term caregiving services to suit individual needs.")])}</div>
</div></section>
<section><div class="wrap split rev">
  <div class="media">{img("medicine-delivery", "Delivery executive handing a bag of medicines to a customer at his door", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Medicines &amp; Medical Equipment</span><h2>Essential Healthcare, Delivered to Your Doorstep</h2>
    <p class="lede">Convenient access to prescribed medicines, medical equipment and personalised nutrition support for better health management at home.</p>
    {benefits([("refill", "Monthly Medicine Refills", "Timely medicine delivery and refill support for uninterrupted care."),
               ("bed", "Medical Equipment on Rent", "Wheelchairs, walkers, hospital beds and oxygen concentrators available for rent."),
               ("apple", "Personalised Nutrition Plans", "Tailored dietary guidance to support recovery, wellness and healthy ageing.")])}</div>
</div></section>
<section class="soft"><div class="wrap">
  <div class="head"><span class="eyebrow">How It Works</span><h2>Seamless Healthcare, Delivered at Home</h2></div>
  {steps([("Share Your Requirements", "Tell us your healthcare needs, location and preferred support."),
          ("Clinical Assessment", "Our medical professionals assess your needs and recommend suitable care."),
          ("Care at Home", "We schedule the required healthcare services at your convenience."),
          ("Ongoing Support &amp; Updates", "We monitor progress and keep you and your family informed.")])}
</div></section>
{faq(hm_faq)}
{enquire("Arrange Home Care", "Home Care", "Share your care requirements and location, and our team will recommend the right healthcare solutions.")}'''
write("home-care.html", "Home Care Services | Vitania Care",
      "Vitania Care offers comprehensive home healthcare, including doctor and nursing visits, caregiver support, physiotherapy, lab tests, medicine delivery and medical equipment rentals.", hm,
      [("Home", ""), ("Home Care", "home-care.html")], "Home Care")

# ================= ABOUT =================
about = f'''{page_hero("About Us", "About Vitania Care", "Healthier People, Brighter Workplaces", "Vitania Care Private Limited is a Bengaluru-based healthcare organisation committed to delivering comprehensive, accessible and personalised healthcare solutions across India. We partner with corporates, institutions and families to promote better health outcomes through preventive healthcare, Employee Wellness Programs and comprehensive home healthcare services. Our focus is on making quality healthcare more accessible, convenient and patient-centric at every stage of life.", "family-consultation", "Vitania Care doctor speaking with a family", "Contact Us", "contact.html")}
<section><div class="wrap split">
  <div class="copy"><span class="eyebrow">Our Story</span><h2>Making Quality Healthcare Easy to Access</h2>
    <p class="lede">Most people visit a doctor only when something goes wrong. We founded Vitania Care to change this by bringing regular Health Check-ups, expert medical advice and timely care to the places where people spend most of their time: at work and at home.</p>
    <p>Today, we partner with organisations to look after their employees and with families to care for their loved ones. Every program is led by qualified professionals and coordinated by a dedicated team.</p></div>
  <div class="media">{img("bp-monitor", "Doctor measuring a patient's blood pressure", WIDE, w=800, h=600)}</div>
</div></section>
<section class="soft"><div class="wrap vm">
  <div class="vision"><span class="eyebrow">Our Vision</span><p>To ensure that every employee and every family has easy access to preventive, coordinated healthcare.</p></div>
  <div><span class="eyebrow">Our Mission</span><h3>What We Work Towards Every Day</h3>
    <ul class="ticks"><li>Help people identify health risks early and take timely action.</li><li>Make doctors, counsellors and nurses easily accessible.</li><li>Coordinate care so that nothing is overlooked.</li><li>Provide employers with clear, confidential insights into workforce health.</li></ul></div>
</div></section>
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Our Values</span><h2>The Principles That Define Our Care</h2></div>
  {features([("shield", "Integrity", "Transparency, trust and confidentiality in everything we do."),
             ("users", "Compassion", "Delivering every service with empathy, dignity and respect."),
             ("chart", "Accountability", "Taking ownership of service quality, commitments and measurable outcomes.")])}
</div></section>
<section style="background:#fff"><div class="wrap">
  <div class="lead-head"><h2><span class="ln"></span>Meet Our <em>Leadership Team</em><span class="ln"></span></h2><p>Driven by a shared vision to build a healthier, happier and more productive tomorrow.</p></div>
  <div class="leads">
    <div class="lead"><div class="lead-photo"><img src="assets/sanjeet-kumar-cut.webp" alt="Sanjeet Kumar" loading="lazy"></div><div class="lead-info"><h3>Sanjeet Kumar</h3><span class="lead-line"></span><p class="role">Founder &amp; Chief Executive Officer</p><a class="lead-mail" href="mailto:chairman@vitaniacare.com"><i><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fff" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg></i>chairman@vitaniacare.com</a></div></div>
    <div class="lead"><div class="lead-photo"><img src="assets/prateeksha-devadiga-cut.webp" alt="Prateeksha Devadiga" loading="lazy"></div><div class="lead-info"><h3>Prateeksha Devadiga</h3><span class="lead-line"></span><p class="role">Co-Founder &amp; Head of Operations</p><a class="lead-mail" href="mailto:prateeksha@vitaniacare.com"><i><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fff" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg></i>prateeksha@vitaniacare.com</a></div></div>
  </div>
</div></section>
{cta("Partner with Vitania Care", "Let's build healthier workplaces and deliver quality healthcare with care, trust and expertise. Connect with our team to explore tailored healthcare solutions for your organisation and family.")}'''
write("about.html", "About Us | Vitania Care Private Limited",
      "Vitania Care Private Limited is a Bengaluru-based healthcare organisation delivering Employee Wellness Programs, preventive healthcare and home healthcare services across India.", about,
      [("Home", ""), ("About Us", "about.html")])

# ================= CONTACT =================
contact_rows = contact_list() + [
    f'<div><dt>Registered Office</dt><dd>{ADDRESS}<br><a class="link" href="https://www.google.com/maps/search/?api=1&amp;query=SLV+Karnataka+Splendour+Apartment+Konanakunte+Bengaluru+560062" target="_blank" rel="noopener">Get Directions →</a></dd></div>']
contact = f'''{page_hero("Contact Us", "Contact Us", "Let Us Help You Build a Healthier Workforce", "Request a proposal for your organisation or enquire about Home Care for your family. Our team will respond within one working day.", "online-doctor", "Vitania Care doctor greeting a patient on a video call", "Send an Enquiry", "#enquire")}
<section id="enquire"><div class="wrap contact-grid">
  <div class="info">
    <div class="head" style="margin:0"><span class="eyebrow">Get in Touch</span><h2>We Are Here to Help</h2></div>
    <dl>{"".join(contact_rows)}</dl>
  </div>
  {form("Send Us an Enquiry", None, "contact")}
</div></section>'''
write("contact.html", "Contact Us | Vitania Care",
      "Contact Vitania Care to request an Employee Wellness Program proposal, book Health Check-ups or arrange Home Care services.", contact,
      [("Home", ""), ("Contact Us", "contact.html")])

# ================= THANK YOU =================
ty = f'''<section class="page-hero"><div class="wrap"><div class="copy">
  <span class="eyebrow">Enquiry Received</span><h1>Thank You for Contacting Vitania Care</h1>
  <p class="lede">Our team will review your enquiry and respond within one working day. For urgent queries, please write to {mail(EMAILS[0])}.</p>
  <div class="cta-row"><a class="btn btn-primary" href="index.html">Back to Home</a><a class="btn btn-outline" href="employee-wellness.html">Explore Our Solutions</a></div>
</div></div></section>'''
write("thank-you.html", "Thank You | Vitania Care", "Thank you for contacting Vitania Care.", ty)

# ---------- sitemap / robots ----------
pages = ["", "employee-wellness.html", "health-checkups.html", "mental-wellbeing.html", "home-care.html", "about.html", "contact.html"]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>2026-11-08</lastmod></url>\n" for p in pages) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you.html\n\nSitemap: {SITE}sitemap.xml\n")
print("built", "(index as fragment)" if FRAGMENT_INDEX else "")
