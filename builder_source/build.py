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
def faq(items, soft=False):
    FAQS.extend(items)
    d = "".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(items))
    return f'''<section{' class="soft"' if soft else ''}><div class="wrap">
  <div class="head"><span class="eyebrow">FAQs</span><h2>Frequently Asked Questions</h2></div>
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
<link rel="preload" href="assets/fonts/interdisplay-700.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="assets/fonts/inter-400.woff" as="font" type="font/woff" crossorigin>
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
 ("employee-wellness.html#ohc", "ohc-clinic", "Doctor consulting an employee at an Occupational Health Centre", "Occupational Health Centre (OHC)", "A fully managed medical centre at your premises, staffed by qualified doctors and nurses."),
 ("health-checkups.html", "bp-check", "Doctor measuring an employee's blood pressure during a health check-up", "Onsite Health Check-ups", "Annual, pre-employment and Onsite Health Check-ups at your workplace, with every report reviewed by a doctor."),
 ("health-checkups.html#camps", "medical-camp", "Doctors attending to employees at an onsite health camp", "Onsite Camps", "Deployment of MBBS and specialist doctors at your workplace for health camps."),
 ("employee-wellness.html#teleconsultation", "online-doctor", "Doctor greeting a patient during a video consultation", "Teleconsultation", "Teleconsultation by general physicians and specialist doctors, by phone or video."),
 ("health-checkups.html#lab-tests", "lab-test", "Laboratory technician examining a blood sample", "Lab Tests", "Pathology and radiology services, with onsite and home sample collection."),
 ("mental-wellbeing.html", None, "", "Mental Wellbeing (EAP)", "Confidential counselling for employees and their families, along with workshops on stress, sleep and resilience."),
 ("employee-wellness.html", "nutrition-guidance", "Nutritionist explaining a balanced diet plan to a client", "Employee Wellness Program", "Webinars and seminars, fitness and yoga, nutrition coaching and chronic care programs throughout the year."),
 ("home-care.html", "doctor-home-visit", "Doctor examining an elderly man at home", "Home Care", "Doctor and nurse visits, physiotherapy, lab tests and medicine delivery in the comfort of home."),
 ("home-care.html#caregivers", "nurse-elderly-care", "Caregiver holding the hand of an elderly woman", "Caregiver Services", "Trained caregivers who assist with personal care, mobility and daily living at home."),
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
    <p class="lede">Vitania Care serves organisations across India with Occupational Health Centres, Onsite Health Check-ups, Teleconsultation, Lab Tests and Employee Wellness Programs. For individuals and families, we provide Home Care and Caregiver Services at your doorstep.</p>
    {ticks([("Pan-India Coverage", "Onsite and online services for your offices across India."),
            ("Qualified Professionals", "MBBS and specialist doctors, nurses, counsellors and nutritionists."),
            ("Single Point of Contact", "One dedicated team for planning, scheduling and reporting.")])}
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
  <div class="head center"><span class="eyebrow">Who We Serve</span><h2>Healthcare Solutions for Organisations and Families</h2>
    <p class="lede">Whether you are an HR leader planning employee benefits or a family arranging care at home, we make it simple to find the right support.</p></div>
  <div class="audience">
    <div class="aud aud-org">
      <span class="ico">{I["building"]}</span>
      <h3>For Organisations</h3>
      <p>Comprehensive programs that keep your workforce healthy, engaged and productive.</p>
      <ul class="ticks"><li>Occupational Health Centre (OHC)</li><li>Onsite Health Check-ups &amp; Onsite Camps</li><li>Teleconsultation &amp; Lab Tests</li><li>Employee Wellness Program &amp; Mental Wellbeing (EAP)</li></ul>
      <a class="btn btn-white" href="contact.html">Request a Proposal</a>
    </div>
    <div class="aud aud-family">
      <span class="ico">{I["home"]}</span>
      <h3>For Individuals &amp; Families</h3>
      <p>Professional medical care and dependable support, delivered to your home.</p>
      <ul class="ticks"><li>Doctor &amp; Nursing Visits at Home</li><li>Caregiver Services</li><li>Physiotherapy at Home</li><li>Lab Tests, Medicines &amp; Medical Equipment</li></ul>
      <a class="btn btn-primary" href="home-care.html#enquire">Arrange Home Care</a>
    </div>
  </div>
</div></section>

<section id="solutions"><div class="wrap">
  <div class="head"><span class="eyebrow">Our Solutions</span><h2>Comprehensive Health Services for Your Workforce and Their Families</h2>
    <p class="lede">Choose a single service or combine several into one integrated program, managed end to end by our team.</p></div>
  {card_html}
</div></section>

<section class="soft"><div class="wrap split">
  <div class="media">{img("bp-monitor", "Doctor measuring a patient's blood pressure", WIDE, w=800, h=600)}</div>
  <div class="copy">
    <span class="eyebrow">Why Vitania Care</span>
    <h2>Healthier Teams, Simplified for HR</h2>
    <p class="lede">We manage the planning, the medical professionals and the follow-up, allowing your HR team to focus on people rather than logistics.</p>
    {benefits([("rupee", "Reduced Healthcare Costs", "Early screening and regular follow-up help reduce the need for expensive treatment and lower insurance claims over time."),
                ("chart", "Fewer Sick Days", "Healthier employees tend to take less time off and remain more engaged at work."),
                ("users", "A Valued Employee Benefit", "Health support that extends to families makes your organisation a more attractive place to work."),
                ("lock", "Confidential by Design", "Personal health information remains private. Employers receive anonymised reports only.")])}
  </div>
</div></section>

<section><div class="wrap">
  <div class="head"><span class="eyebrow">How It Works</span><h2>From Initial Consultation to Measurable Results</h2></div>
  {steps([("Understand Your Needs", "We meet your HR team to understand your team size, locations, work shifts and health priorities."),
          ("Design the Program", "You receive a clear annual plan with services, schedules and a transparent quotation."),
          ("Deliver on the Ground", "Our doctors, nurses and wellness experts conduct every session, camp and consultation."),
          ("Review and Improve", "Quarterly reports show participation and health trends, helping us refine the program.")])}
</div></section>

<section class="band"><div class="wrap">
  <div class="head"><span class="eyebrow">Industries We Serve</span><h2>Built for Workplaces</h2>
    <p class="lede">Our programs adapt to office-based teams, shift workers and distributed teams across India.</p></div>
  {features([("building", "IT &amp; Technology Companies", "Desk-based teams that need support with stress, posture, sleep and lifestyle-related conditions."),
             ("users", "Manufacturing &amp; Operations", "Shift workers who benefit from Occupational Health Centres, Onsite Health Check-ups and first-aid training."),
             ("chart", "Banking, Finance &amp; Services", "High-pressure roles where mental wellbeing and regular health check-ups matter most."),
             ("pulse", "Start-ups &amp; Growing Teams", "Flexible, cost-effective plans that grow with your headcount."),
             ("calendar", "Hospitality &amp; Retail", "Pre-employment health checks and regular screening for customer-facing staff."),
             ("home", "Employee Families", "We also provide medical care at home for the families of employees through Home Care and Caregiver Services.")])}
</div></section>
{faq(home_faq)}
{cta("Ready to Build a Healthier Workforce?", "Tell us about your organisation, and we will share a wellness plan and proposal tailored to your requirements.")}'''
write("index.html", "Vitania Care | Corporate Health & Wellness Partner Across India",
      "Corporate health and wellness services across India: Occupational Health Centres, Onsite Health Check-ups, Onsite Camps, Teleconsultation, Lab Tests, Mental Wellbeing support and Home Care.", home)

# ================= EMPLOYEE WELLNESS PROGRAM =================
ew_faq = [
 ("What does an Employee Wellness Program include?", "A typical program combines an Occupational Health Centre, Onsite Health Check-ups, Teleconsultation, webinars and seminars, fitness and nutrition sessions, and support for chronic conditions. We tailor the combination to your workforce."),
 ("Can sessions be conducted online?", "Yes. Teleconsultation, webinars, counselling and nutrition coaching can all be delivered online for remote and hybrid teams across India."),
 ("How do you measure the impact of the program?", "We track participation, screening results and follow-up outcomes, and share anonymised quarterly reports with your HR team."),
 ("How long does it take to launch a program?", "Launch timelines depend on the services selected. Most standard programs can begin within a few weeks of confirmation."),
]
ew = f'''{page_hero("Employee Wellness Program", "Employee Wellness Program", "Wellness Programs That Keep Your Workforce Healthy", "Our year-round programs bring together Occupational Health Centres, Onsite Health Check-ups, Teleconsultation, fitness, nutrition and mental wellbeing support. We plan and manage every element and share regular progress reports with you.", "nutrition-guidance", "Nutritionist explaining a balanced diet chart to a client")}
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Program Inclusions</span><h2>Everything Your Team Needs to Stay Well</h2>
    <p class="lede">Choose individual services or combine them into one annual program.</p></div>
  {features([("ohc", "Occupational Health Centre (OHC)", "A fully managed medical centre at your premises, staffed by qualified doctors and nurses."),
             ("check", "Onsite Health Check-ups", "Health check-ups at your workplace, including blood pressure, blood sugar, BMI, eye and dental checks."),
             ("camp", "Onsite Camps", "Deployment of MBBS and specialist doctors at your workplace for health camps."),
             ("video", "Teleconsultation", "Teleconsultation by general physicians and specialist doctors, by phone or video."),
             ("lab", "Lab Tests", "Pathology and radiology services, with onsite and home sample collection."),
             ("talk", "Webinars &amp; Seminars", "Expert-led webinars and seminars by doctors on topics such as heart health, diabetes, sleep and posture."),
             ("yoga", "Fitness &amp; Yoga Sessions", "Group yoga, stretching and fitness sessions conducted at your office or online."),
             ("apple", "Nutrition Coaching", "Personalised diet plans and one-to-one guidance from qualified nutritionists."),
             ("pulse", "Chronic Care Programs", "Ongoing support for diabetes, hypertension, thyroid disorders and weight management.")])}
</div></section>
<section id="ohc" class="soft"><div class="wrap split">
  <div class="media">{img("ohc-clinic", "Doctor consulting an employee at an Occupational Health Centre", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Occupational Health Centre (OHC)</span><h2>A Fully Managed Medical Centre at Your Workplace</h2>
    <p class="lede">We set up and run Occupational Health Centres at your premises, so that employees receive prompt medical attention without leaving the workplace.</p>
    {ticks([("Qualified Medical Team", "MBBS doctors and trained nurses, scheduled to suit your working hours and shifts."),
            ("First Aid &amp; Emergency Response", "Immediate first aid and coordination with nearby hospitals when required."),
            ("Medical Examinations &amp; Records", "Pre-employment and periodic medical examinations, with confidential health records.")])}</div>
</div></section>
<section id="teleconsultation"><div class="wrap split rev">
  <div class="media">{img("online-doctor", "Doctor greeting a patient during a video consultation", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Teleconsultation</span><h2>Teleconsultation with General Physicians and Specialist Doctors</h2>
    <p class="lede">Employees can consult a doctor by phone or video, without leaving work or waiting in a hospital queue.</p>
    {benefits([("steth", "General Physicians", "Consultations for everyday health concerns such as fever, infections and lifestyle conditions."),
               ("users", "Specialist Doctors", "Access to specialist doctors for further evaluation and expert opinion."),
               ("pill", "Prescriptions &amp; Follow-up", "Digital prescriptions, medicine delivery and follow-up reminders.")])}</div>
</div></section>
<section id="fitness" class="soft"><div class="wrap split">
  <div class="media">{img("physiotherapy", "Physiotherapist guiding a man through a resistance-band exercise", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Fitness &amp; Recovery</span><h2>Building Healthy Habits That Last</h2>
    <p class="lede">Long hours at a desk can lead to back pain, stiffness and fatigue. Our physiotherapists and fitness coaches help employees move better and feel better.</p>
    {ticks([("Ergonomic Assessments", "Workstation reviews and posture correction."),
            ("Physiotherapy Support", "Treatment for back, neck and joint pain."),
            ("Fitness Challenges", "Monthly activities that keep teams active and engaged.")])}</div>
</div></section>
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Our Approach</span><h2>A Seamless, Fully Managed Program</h2></div>
  {steps([("Assess", "We review the needs of your team and your existing health benefits."),
          ("Plan", "We create a 12-month wellness calendar with clear, transparent costs."),
          ("Deliver", "Our team conducts every session, camp and consultation."),
          ("Report", "You receive quarterly, anonymised impact reports.")])}
</div></section>
{faq(ew_faq, soft=True)}
{enquire("Plan a Wellness Program for Your Team", "Occupational Health Centre (OHC)")}'''
write("employee-wellness.html", "Employee Wellness Program | Vitania Care",
      "Employee Wellness Programs across India: Occupational Health Centres, Onsite Health Check-ups, Onsite Camps, Teleconsultation, lab tests, webinars and seminars, fitness, nutrition and chronic care.", ew,
      [("Home", ""), ("Employee Wellness Program", "employee-wellness.html")], "Employee Wellness Program")

# ================= HEALTH CHECK-UPS =================
hc_faq = [
 ("Where are the check-ups conducted?", "Check-ups can be conducted at your office through Onsite Health Check-ups, at a partner diagnostic centre, or through home sample collection."),
 ("How are reports shared?", "Each employee receives a digital report, and a doctor explains the results and recommends the next steps where required."),
 ("Can you conduct pre-employment medical examinations at short notice?", "Yes. We schedule pre-employment check-ups promptly so that joining dates are not delayed."),
 ("Do employees need to fast before the tests?", "Some blood tests require 8–12 hours of fasting. We share preparation instructions with every employee before the test."),
]
hc = f'''{page_hero("Health Check-ups", "Health Check-ups", "Preventive Health Check-ups for Early Detection and Timely Care", "We offer Annual Health Check-ups, Pre-employment Medical Examinations, Onsite Health Check-ups and Lab Tests, with every report reviewed by a doctor and a Doctor Consultation provided as needed.", "bp-check", "Doctor measuring an employee's blood pressure during a health check-up")}
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Our Check-up Services</span><h2>Screening for Every Stage of Employment</h2></div>
  {features([("check", "Annual Health Check-ups", "Comprehensive packages that include blood tests, an ECG, eye tests and a Doctor Consultation."),
             ("users", "Pre-employment Check-ups", "Fitness-for-work medical examinations for new joiners, completed promptly and on schedule."),
             ("building", "Onsite Health Check-ups", "Blood pressure, blood sugar, BMI, eye and dental checks conducted at your workplace."),
             ("camp", "Onsite Camps", "Deployment of MBBS and specialist doctors at your workplace for health camps."),
             ("lab", "Lab Tests", "Pathology and radiology services, with onsite and home sample collection."),
             ("steth", "Doctor Review of Reports", "A doctor explains every report and recommends follow-up care where required.")])}
</div></section>
<section id="camps" class="soft"><div class="wrap split">
  <div class="media">{img("medical-camp", "Doctors attending to employees at an onsite health camp", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Onsite Camps</span><h2>MBBS and Specialist Doctors at Your Workplace</h2>
    <p class="lede">We deploy MBBS and specialist doctors, along with technicians and equipment, at your workplace, and schedule slots around working hours to avoid disruption.</p>
    {ticks([("Specialist Doctors", "Specialists deployed according to the health needs of your workforce."),
            ("Flexible Scale", "Camps for a single team or an entire office."),
            ("Follow-up Care", "Doctor Consultations for employees who need further advice.")])}</div>
</div></section>
<section id="lab-tests"><div class="wrap split rev">
  <div class="media">{img("lab-test", "Laboratory technician examining a blood sample beside a microscope", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Lab Tests</span><h2>Pathology and Radiology Services</h2>
    <p class="lede">We arrange accurate diagnostic tests through trusted partner laboratories and diagnostic centres, with convenient sample collection at your workplace or at home.</p>
    {ticks([("Pathology", "Blood, urine and other laboratory tests, with reports shared digitally."),
            ("Radiology", "X-ray, ultrasound and other imaging through partner diagnostic centres."),
            ("Onsite &amp; Home Sample Collection", "Trained technicians collect samples at your workplace or at home.")])}</div>
</div></section>
<section class="soft"><div class="wrap">
  <div class="head"><span class="eyebrow">How It Works</span><h2>Simple for HR and Employees</h2></div>
  {steps([("Choose a Package", "We recommend packages based on age, role and health risk."),
          ("Schedule", "Employees book slots at the office, a diagnostic centre or at home."),
          ("Test", "Samples and checks are completed by trained professionals."),
          ("Review", "A doctor explains the results and plans follow-up care.")])}
</div></section>
{faq(hc_faq)}
{enquire("Book Health Check-ups for Your Team", "Annual Health Check-ups")}'''
write("health-checkups.html", "Preventive Health Check-ups for Employees | Vitania Care",
      "Annual, pre-employment and onsite health check-ups, onsite camps with MBBS and specialist doctors, and pathology and radiology lab tests with onsite and home sample collection.", hc,
      [("Home", ""), ("Health Check-ups", "health-checkups.html")], "Employee Health Check-ups")

# ================= MENTAL WELLBEING =================
mw_faq = [
 ("Is counselling confidential?", "Yes. All sessions are completely confidential. Employers are never informed about who used the service or what was discussed."),
 ("Who can use the Employee Assistance Program?", "All employees covered under your plan can use the service, and family members can be included if you choose."),
 ("How do employees book a session?", "Employees can call or message our team to book a phone, video or in-person session at a convenient time."),
 ("What concerns can counsellors help with?", "Counsellors can help with stress, anxiety, low mood, relationships, parenting, grief, work pressure and work–life balance, among other concerns."),
]
mw = f'''{page_hero("Mental Wellbeing", "Employee Assistance Program (EAP)", "Confidential Support for Employee Mental Wellbeing", "Qualified counsellors help employees manage stress, anxiety and personal challenges through phone, video or in-person sessions.", "online-doctor", "Counsellor smiling and waving during a video session")}
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Program Inclusions</span><h2>Support for Everyday and Difficult Moments</h2></div>
  {features([("talk", "One-to-One Counselling", "Confidential sessions with qualified counsellors and psychologists."),
             ("users", "Family Support", "Counselling that can be extended to spouses, children and parents."),
             ("mind", "Stress &amp; Resilience Workshops", "Group sessions on stress, burnout, sleep and emotional wellbeing."),
             ("users", "Manager Training", "Training that helps team leaders recognise signs of distress and respond with care."),
             ("shield", "Critical Incident Support", "Prompt support for teams after a crisis or traumatic event."),
             ("chart", "Anonymised Insights", "Usage and wellbeing trends that help guide your HR policies.")])}
</div></section>
<section class="soft"><div class="wrap">
  <div class="head"><span class="eyebrow">Why It Matters</span><h2>A Supported Team Is a Productive Team</h2>
    <p class="lede">Unaddressed stress affects focus, attendance and retention. Early, confidential support helps employees stay well and perform at their best.</p></div>
  {features([("video", "Flexible Sessions", "Counselling available by phone, video or in person, at a time that suits the employee."),
             ("calendar", "Easy Booking", "A simple booking process with no paperwork required for employees."),
             ("lock", "Complete Privacy", "Every conversation remains strictly confidential.")])}
</div></section>
{faq(mw_faq)}
{enquire("Set Up an Employee Assistance Program", "Mental Wellbeing (EAP)")}'''
write("mental-wellbeing.html", "Employee Assistance Program (EAP) | Vitania Care",
      "Confidential employee counselling, stress and resilience workshops, manager training and family support through the Vitania Care Employee Assistance Program.", mw,
      [("Home", ""), ("Mental Wellbeing", "mental-wellbeing.html")], "Employee Assistance Program")

# ================= HOME CARE =================
hm_faq = [
 ("How soon can a doctor or nurse visit?", "Visits can often be arranged within a day. Please let us know how urgent the requirement is when you contact us."),
 ("Is Home Care suitable for medical emergencies?", "No. Home Care is not a substitute for emergency services. In a medical emergency, please call an ambulance or visit the nearest hospital."),
 ("What support do your caregivers provide?", "Our caregivers assist with personal care, mobility, feeding, medication reminders and companionship. We recommend a care plan after understanding the needs of the patient."),
 ("Do you provide medical equipment on rent?", "Yes. We arrange wheelchairs, walkers, hospital beds and oxygen concentrators on rent, delivered to your home."),
 ("Can organisations offer Home Care as an employee benefit?", "Yes. Organisations can extend Home Care services to employees and their families as part of their Employee Wellness Program."),
]
hm = f'''{page_hero("Home Care", "Home Care", "Professional Medical Care in the Comfort of Your Home", "We provide doctor and nurse visits, Caregiver Services, physiotherapy, lab tests and medicine delivery at home, helping patients recover and manage their health with ease.", "doctor-home-visit", "Doctor checking an elderly man's heartbeat at home while his wife looks on")}
<section><div class="wrap">
  <div class="head"><span class="eyebrow">Home Care Services</span><h2>Quality Medical Care Without the Hospital Visit</h2></div>
  {features([("steth", "Doctor Visits at Home", "General physicians who examine, diagnose and prescribe at home."),
             ("nurse", "Nursing Care", "Injections, wound dressing, IV care and post-operative care by trained nurses."),
             ("users", "Caregiver Services", "Trained caregivers who assist with personal care, mobility and daily living at home."),
             ("physio", "Physiotherapy", "Post-surgery, post-injury and post-stroke rehabilitation sessions at home."),
             ("lab", "Lab Tests at Home", "Home sample collection for laboratory tests, with reports shared digitally."),
             ("bed", "Medical Equipment on Rent", "Hospital beds, wheelchairs and oxygen concentrators provided on a rental basis.")])}
</div></section>
<section id="caregivers" class="soft"><div class="wrap split">
  <div class="media">{img("nurse-elderly-care", "Caregiver holding the hand of an elderly woman resting in bed", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Caregiver Services</span><h2>Trained Caregivers for Everyday Support at Home</h2>
    <p class="lede">Our caregivers provide compassionate and reliable assistance with daily activities, helping patients and elderly family members live safely and comfortably at home.</p>
    {benefits([("users", "Personal Care Assistance", "Support with bathing, grooming, dressing and toileting, delivered with dignity and respect."),
               ("physio", "Mobility &amp; Daily Living Support", "Help with walking, transfers, feeding and everyday routines."),
               ("pill", "Medication Reminders &amp; Companionship", "Timely medication reminders, regular monitoring and attentive companionship."),
               ("calendar", "Flexible Care Plans", "Short-term or long-term support, scheduled according to your requirements.")])}</div>
</div></section>
<section><div class="wrap split rev">
  <div class="media">{img("medicine-delivery", "Delivery executive handing a bag of medicines to a customer at his door", WIDE, w=800, h=600)}</div>
  <div class="copy"><span class="eyebrow">Everyday Support</span><h2>Medicines &amp; Medical Equipment, Delivered to Your Doorstep</h2>
    <p class="lede">We make healthcare management easier by arranging prescribed medications, timely refills and essential medical equipment, helping individuals and families access the care and support they need.</p>
    {benefits([("refill", "Monthly Medicine Refills", "Convenient monthly medicine replenishment with timely reminders to ensure continuity of medication."),
               ("bed", "Medical Equipment on Rent", "Access to essential medical equipment, including wheelchairs, walkers, hospital beds and oxygen concentrators, available for rent."),
               ("apple", "Personalised Nutrition Plans", "Tailored nutrition plans to support recovery, improve overall wellbeing and promote healthy ageing.")])}</div>
</div></section>
<section class="soft"><div class="wrap">
  <div class="head"><span class="eyebrow">How It Works</span><h2>Arranging Care at Home</h2></div>
  {steps([("Share Your Requirement", "Tell us who needs care, where and what kind of support is required."),
          ("Clinical Assessment", "A doctor or nurse assesses the condition and recommends a care plan."),
          ("Care at Home", "Visits, nursing, caregiving, therapy or tests are scheduled at a time that suits you."),
          ("Regular Updates", "We monitor progress and keep you and your doctor informed.")])}
</div></section>
{faq(hm_faq)}
{enquire("Arrange Home Care", "Home Care", "Tell us who needs care and where, and our team will recommend the right services for you and your family.")}'''
write("home-care.html", "Home Care Services | Vitania Care",
      "Doctor and nurse visits, Caregiver Services, physiotherapy, lab tests, medicine delivery and medical equipment on rent, delivered at home by Vitania Care.", hm,
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
  <div class="head"><span class="eyebrow">Our Values</span><h2>The Principles That Guide Our Work</h2></div>
  {features([("shield", "Integrity", "We are transparent about our services and protect the privacy of every individual."),
             ("users", "Care", "We treat every employee and family member with patience, empathy and respect."),
             ("chart", "Accountability", "We measure our work and report results openly to our clients.")])}
</div></section>
<section class="soft"><div class="wrap">
  <div class="head"><span class="eyebrow">Leadership</span><h2>Meet Our Founders</h2></div>
  <div class="team">
    <div class="person"><img src="assets/sanjeet-kumar.webp" alt="Sanjeet Kumar" width="192" height="192" loading="lazy"><h3>Sanjeet Kumar</h3><p class="role">Founder &amp; CEO</p><p class="meta">chairman@vitaniacare.com</p></div>
    <div class="person"><img src="assets/prateeksha-devadiga.webp" alt="Prateeksha Devadiga" width="192" height="192" loading="lazy"><h3>Prateeksha Devadiga</h3><p class="role">Co-Founder &amp; Head of Operations</p><p class="meta">prateeksha@vitaniacare.com</p></div>
  </div>
</div></section>
{cta("Partner with Us for a Healthier Workplace", "Speak with our team about a wellness program for your organisation or Home Care for your family.")}'''
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
