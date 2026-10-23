#!/usr/bin/env python3
"""Publish up to five substantial topic-specific guides per run; fail closed."""
import datetime as dt, hashlib, html, json, os, re, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"docs"
STATE=ROOT/"editorial-state.json"
BASE="https://aiautomationtactics.github.io/Ghostpages/"
from zoneinfo import ZoneInfo
ZONE=ZoneInfo("America/Vancouver")
START_DATE=dt.date(2026,10,23)
END_DATE=START_DATE+dt.timedelta(days=20)
LIMIT=100
# Curated links from previously supplied sites. Select by relevance, not link quotas.
RESOURCES=[
("Free affiliate guide","https://freeaffiliateguide.vercel.app/","beginner"),
("LeadForge learning","https://leadforge.wasmer.app/","leads"),
("LeadsLeap review","https://leadsleapreview.vercel.app/","leads"),
("Herculist review","https://herculistreview.vercel.app/","email"),
("ClickForge","https://clickforge.wasmer.app/","seo"),
("Affiliate SEO","https://affiliateseo.vercel.app/","seo"),
("SocialYou","https://socialyou.wasmer.app/","social"),
("ChatGPT marketing","https://chatgptmarketing.vercel.app/","ai"),
("Max Lead Gen","https://maxleadgen.wasmer.app/","leads"),
("ClickTraffic","https://clicktraffic.wasmer.app/","traffic"),
("Master Affiliate","https://masteraffiliate.wasmer.app/","beginner"),
("Make Money Online learning","https://makemoneyonline.wasmer.app/","beginner"),
("Social Traffic","https://socialtraffic.wasmer.app/","social"),
("Affiliate Machine","https://affiliatemachine.wasmer.app/","traffic"),
("1 Click Buyer Traffic","https://1clickbuyertraffic.vercel.app/","traffic"),
("LocalForge","https://localforgeaf.wasmer.app/","local"),
("ClickPath","https://clickpath.wasmer.app/","funnel"),
("TrafficGift","https://trafficgift.wasmer.app/","traffic"),
("Social Backlink Hack","https://backlinkhacksocial.wasmer.app/","seo"),
("Scalevora Traffic","https://scalevoratraffic.vercel.app/","traffic"),
("Affiliate Marketer Salary","https://affiliatemarketersalary.vercel.app/","beginner"),
("MMO Side Hustle","https://mmosidehustle.vercel.app/","beginner"),
("Safelist Traffic","https://safelisttraffic.wasmer.app/","email"),
("SuperIntelligence AI","https://superintelligenceai.wasmer.app/","ai"),
("Click Money AI","https://clickmoneyai.wasmer.app/","ai"),
("Web Traffic Affiliate","https://webtrafficaffiliate.wasmer.app/","traffic"),
("Buyer Clicks","https://getbuyerclicktraffic.vercel.app/","traffic"),
("Lead capture ideas","https://maxleadgen.wasmer.app/","funnel"),
("TopDogs Rotator referral","https://topdogsrotator.com/r/awanraheel0","traffic"),
("LeadsLeap referral","https://leadsleap.com/?r=awanraheel0","leads"),
("The Downliner referral","https://thedownliner.com/?ref=awanraheel0","email"),
("AI Traffic Learning","https://50000freeclicks.wasmer.app/","traffic"),
("YouTube channel","https://www.youtube.com/@makemoneyonlineaffiliatelink","social"),
("1Click Buyer Traffic","https://1clickbuyertrafficgalore.wasmer.app/","traffic"),
("Affiliate Marketing SEO","https://affiliatebuyerclicks.wasmer.app/","seo"),
("Affiliate Insta","https://affiliateinsta.wasmer.app/","social"),
("ClickForge archive","https://clickforge.wasmer.app/","beginner"),
("Traffic Planning","https://trafficgift.wasmer.app/","funnel"),
("Lead Generation Tools","https://leadg.wasmer.app/","leads"),
]
# Distinct topic+reader-intent inventory rather than near-duplicate page permutations.
TOPICS=[
("How to recognize qualified website visitors","traffic"),
("Clicks versus conversions: a practical measurement guide","traffic"),
("Designing a controlled paid-traffic test on a small budget","traffic"),
("Writing a clear opt-in promise without pressure","funnel"),
("Choosing search intent for an educational affiliate article","seo"),
("How to calculate a landing-page opt-in rate","leads"),
("What a bounce and an engaged visit can tell you","traffic"),
("Creating a UTM naming convention for campaigns","traffic"),
("Separating bot requests from real user behavior","traffic"),
("Reading a simple weekly traffic scorecard","traffic"),
("How to assess audience fit before buying clicks","traffic"),
("Comparing a referral placement against social discovery","traffic"),
("Establishing a stop rule for paid traffic","traffic"),
("Choosing one campaign variable to test","traffic"),
("Understanding attribution windows in plain language","traffic"),
("Auditing a landing page for clear intent","funnel"),
("Planning an honest call to action","funnel"),
("Designing a useful thank-you page after signup","funnel"),
("Setting expectations before an email opt-in","funnel"),
("Making a lead magnet that solves one problem","funnel"),
("Planning a three-email welcome sequence","email"),
("Understanding unsubscribe and consent principles","email"),
("Segmenting subscribers by the question they asked","email"),
("Comparing broadcast mail to an owned subscriber list","email"),
("Evaluating whether a safelist audience fits your offer","email"),
("Writing responsible subject lines for a newsletter","email"),
("Measuring email click quality beyond open rates","email"),
("Cleaning an outdated signup form","email"),
("Designing newsletter archives that help non-subscribers","email"),
("Helping unsubscribed visitors still find the resource","email"),
("Preparing a trustworthy review of an affiliate tool","beginner"),
("Disclosing referral compensation near recommendations","beginner"),
("Comparing products without inventing performance claims","beginner"),
("Deciding what not to promote to your readers","beginner"),
("Understanding commissions versus actual profit","beginner"),
("Keeping a simple affiliate expense ledger","beginner"),
("Researching audience questions before publishing","beginner"),
("Avoiding unrealistic earnings promises in marketing copy","beginner"),
("Creating a public about page with real editorial standards","beginner"),
("Checking a recommendation for hidden conditions","beginner"),
("Building an internal link map for an educational site","seo"),
("Writing a search snippet that matches the article","seo"),
("Understanding canonical tags for duplicate URLs","seo"),
("Creating a sitemap without trying to force indexing","seo"),
("Making a responsive page more readable on mobile","seo"),
("Checking headings and page hierarchy for accessibility","seo"),
("Recognizing thin pages before publication","seo"),
("Updating stale posts instead of multiplying pages","seo"),
("Writing descriptive link text for readers","seo"),
("Separating topical clusters by reader intent","seo"),
("Learning from Search Console queries without stuffing keywords","seo"),
("Choosing an article title that answers a real question","seo"),
("Adding worked examples to generic marketing advice","seo"),
("Knowing when to combine overlapping pages","seo"),
("Creating a simple editorial fact-check checklist","seo"),
("Making a practical YouTube description with source links","social"),
("Turning one community question into a useful video outline","social"),
("Choosing Pinterest pin titles without clickbait","social"),
("Answering Quora questions without dropping unwanted links","social"),
("Participating respectfully in Facebook group discussions","social"),
("Using Instagram captions for context instead of hype","social"),
("Teaching one marketing concept in a short-form video","social"),
("Repurposing a guide across channels without copying blindly","social"),
("Matching a social post to the promised landing page","social"),
("Measuring social referrals without vanity metrics","social"),
("Assessing when an AI draft needs a subject expert","ai"),
("Fact-checking AI-generated marketing explanations","ai"),
("Protecting reader data while experimenting with AI tools","ai"),
("Avoiding fabricated statistics in AI-assisted articles","ai"),
("Testing an AI headline against the actual page","ai"),
("Disclosing meaningful automation in an editorial workflow","ai"),
("Detecting repetitive AI phrasing in related articles","ai"),
("Reviewing AI-generated summaries for missing nuance","ai"),
("Creating a source log for factual claims","ai"),
("Separating idea generation from verified advice","ai"),
("Using a spreadsheet to compare lead-source quality","leads"),
("Planning a lead follow-up based on expressed interest","leads"),
("Designing a contact form with only necessary fields","leads"),
("Explaining what happens after someone signs up","leads"),
("Evaluating a lead-generation landing page for trust","leads"),
("Matching free traffic channels to a narrow audience","traffic"),
("Recognizing mismatched traffic offers","traffic"),
("Estimating the cost per meaningful action","traffic"),
("Using the same measurement period across two campaigns","traffic"),
("Learning from a campaign with no conversions","traffic"),
("Identifying a local-business customer's top question","local"),
("Creating a helpful local service comparison page","local"),
("Reviewing local marketing claims for accuracy","local"),
("Measuring qualified inquiries for a small local service","local"),
("Creating location-specific information without doorway pages","local"),
("Comparing newsletter growth to search growth for beginners","beginner"),
("Creating an editorial calendar that respects quality","beginner"),
("Deciding whether to publish or revise an article","beginner"),
("Understanding when an affiliate link helps the reader","beginner"),
("Designing a clear resource page without link clutter","beginner"),
("Running a usability check on a signup flow","funnel"),
("Writing a clear privacy note for a lead form","funnel"),
("Measuring the visitor journey from article to next step","funnel"),
("Planning a helpful FAQ based on actual reader questions","funnel"),
("Reducing distractions in an educational landing page","funnel"),
]
def slug(s): return re.sub("[^a-z0-9]+","-",s.lower()).strip("-")[:110]
def esc(s): return html.escape(str(s),quote=True)
def create_article(title,topic,audience):
    key=os.getenv("OPENAI_API_KEY","").strip()
    if not key: raise RuntimeError("OPENAI_API_KEY missing; publishing skipped safely.")
    prompt=f"""Create a completely original, truly useful evergreen guide titled '{title}', on '{topic}', {audience}. Do not repeat common boilerplate. Answer a clear reader question. Include a tangible example and a specific process.
Return a JSON object: description (115–155 characters), intro (100–160 words), sections (array of EXACTLY FIVE objects with heading and text, each 160–230 words), example (180–230 words realistic hypothetical, not fabricated actual results), checklist (array of EXACTLY SIX distinct actions), cautions (120–180 words). Minimum full article 1100 words. Realistic practical steps and context-specific tradeoffs, not waffle. Never invent statistics, platform policies, platform features, verified product claims, pricing, testimonials, or earned income. No guarantees of rankings, traffic, leads, or sales. No links, HTML, Markdown, or quotes attributed to unknown people. No keyword stuffing. All claims should be evergreen and qualify uncertain information; encourage readers to check platform documentation."""
    body=json.dumps({"model":"gpt-4.1-mini","temperature":0.6,"response_format":{"type":"json_object"},"messages":[{"role":"system","content":"You are a careful human-first educational editor. Produce factual substantive JSON with no markdown."},{"role":"user","content":prompt}]}).encode()
    req=urllib.request.Request("https://api.openai.com/v1/chat/completions",body,{"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=105) as response:
        result=json.load(response)
    return json.loads(result["choices"][0]["message"]["content"])
def verify(a,known):
    if not isinstance(a,dict): return None
    sections=a.get("sections")
    if not isinstance(sections,list) or len(sections)!=5: return None
    if not isinstance(a.get("checklist"),list) or len(a["checklist"])!=6: return None
    strings=[a.get("intro",""),a.get("example",""),a.get("cautions","")]+[s.get("text","") for s in sections]
    if not all(isinstance(x,str) for x in strings): return None
    words=sum(len(re.findall(r"\b[\w'-]+\b",s)) for s in strings)
    if words<1100: return None
    if not 95<=len(a.get("description",""))<=170: return None
    if any(not s.get("heading") for s in sections): return None
    corpus=" ".join(strings).lower()
    if any(b in corpus for b in ["guaranteed commissions","get rich quick","instant riches","100% guaranteed income"]): return None
    fingerprint=hashlib.sha256(corpus.encode()).hexdigest()
    return fingerprint if fingerprint not in known else None
def webpage(title,a,path,related):
    url=BASE+path
    schema=json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":a["description"],"mainEntityOfPage":url,"author":{"@type":"Organization","name":"Practical Traffic Lab"}}).replace("<","\\u003c")
    main="\n".join(f'<section><h2>{esc(s["heading"])}</h2><p>{esc(s["text"])}</p></section>' for s in a["sections"])
    actions="".join(f"<li>{esc(t)}</li>" for t in a["checklist"])
    refs="".join(f'<li><a rel="sponsored noopener noreferrer" target="_blank" href="{esc(u)}">{esc(n)}</a></li>' for n,u,_ in related)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | Practical Traffic Lab</title><meta name="description" content="{esc(a['description'])}"><link rel="canonical" href="{esc(url)}">
<script type="application/ld+json">{schema}</script>
<style>body{{font:17px/1.7 system-ui,Arial;color:#172437;background:#f3f6fa;margin:0}}header,footer{{padding:20px;background:#12223c;color:white}}header a,footer a{{color:#caeaff}}main{{max-width:860px;margin:24px auto;padding:clamp(20px,4vw,45px);background:white;border-radius:16px}}h1{{line-height:1.2}}h2{{color:#163a66;margin-top:2rem}}.disclosure{{background:#eef6fc;border-left:4px solid #2177ad;padding:15px}}a{{color:#0757a5}}li{{margin:10px 0}}</style></head>
<body><header><nav><a href="{BASE}">Practical Traffic Lab — Browse all guides</a></nav></header><main><article><h1>{esc(title)}</h1>
<p class="disclosure"><strong>Disclosure:</strong> Some recommended resources may use affiliate or referral links. We may receive compensation at no additional cost to you. This guide is educational and makes no income or ranking promises.</p>
<p>{esc(a['intro'])}</p>{main}<section><h2>Practical worked example</h2><p>{esc(a['example'])}</p></section>
<section><h2>Implementation checklist</h2><ol>{actions}</ol></section><section><h2>Limitations and cautions</h2><p>{esc(a['cautions'])}</p></section>
<section><h2>Relevant optional resources</h2><p>These are external websites for further comparison, not endorsements or guaranteed results. Review current terms and claims yourself.</p><ul>{refs}</ul></section></article>
<p><a href="{BASE}">Back to all guides</a></p></main><footer>Practical Traffic Lab — clear guidance for humans, not search engines.</footer></body></html>'''
def update_catalog(pages):
    DOCS.mkdir(exist_ok=True)
    links="".join(f'<li><a href="{esc(p["path"])}">{esc(p["title"])}</a></li>' for p in reversed(pages))
    (DOCS/"index.html").write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Practical Traffic Lab | Educational Affiliate Marketing</title><meta name="description" content="Beginner-friendly, honest guides to affiliate marketing, website traffic, lead generation, SEO and analytics."><link rel="canonical" href="{BASE}"><style>body{{font:18px/1.7 system-ui;color:#192638;background:#f5f7fb;margin:0}}header{{background:#162640;color:white;padding:30px}}main{{max-width:900px;margin:auto;padding:30px}}a{{color:#105da1}}li{{margin:10px 0}}</style></head><body><header><h1>Practical Traffic Lab</h1><p>Better educational content, clearer measurement, realistic expectations.</p></header><main><p>Explore practical ways to build useful content and find appropriate audiences. No guaranteed income, search rankings, or traffic outcomes.</p><p>Disclosure: Some external resources may include affiliate/referral links, and could earn commissions. We recommend comparing sources before making decisions.</p><h2>Browse guides</h2><ul>{links}</ul><p><a href="about.html">Editorial policy and affiliate disclosures</a></p></main></body></html>''',encoding="utf-8")
    sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+BASE+'</loc></url>'+''.join("<url><loc>"+esc(BASE+p["path"])+"</loc></url>" for p in pages)+"</urlset>"
    (DOCS/"sitemap.xml").write_text(sitemap,encoding="utf-8")
    (DOCS/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+BASE+"sitemap.xml\n",encoding="utf-8")
    (DOCS/".nojekyll").touch()
def main():
    local_day=dt.datetime.now(ZONE).date()
    if not START_DATE<=local_day<END_DATE:
        print("Outside 20-day window; no pages created."); return
    state=json.loads(STATE.read_text()) if STATE.exists() else {"pages":[],"hashes":[]}
    count=len(state["pages"])
    day_number=(local_day-START_DATE).days
    allowance=min(LIMIT,5*(day_number+1))
    if count>=allowance or count>=LIMIT:
        print("Daily or project cap already reached; no pages created."); return
    if not os.getenv("OPENAI_API_KEY"):
        print("Missing OPENAI_API_KEY secret; no pages created."); return
    new=[]
    for idx in range(count,min(count+5,allowance,LIMIT)):
        title,category=TOPICS[idx]
        topic=title
        audience="for a beginner reader seeking a specific practical answer"
        path="guides/"+slug(title)+".html"
        related=[r for r in RESOURCES if r[2]==category]
        if len(related)<2: related+=[r for r in RESOURCES if r[2]=="beginner"]
        chosen=[related[idx%len(related)],related[(idx+1)%len(related)]]
        print("Drafting",title)
        article=create_article(title,topic,audience)
        fingerprint=verify(article,set(state["hashes"])|{p[2] for p in new})
        if not fingerprint: raise RuntimeError("Quality gate rejected: "+title)
        new.append((path,title,fingerprint,webpage(title,article,path,chosen)))
    for path,title,fingerprint,markup in new:
        dest=DOCS/path
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(markup,encoding="utf-8")
        state["pages"].append({"title":title,"path":path})
        state["hashes"].append(fingerprint)
    update_catalog(state["pages"])
    STATE.write_text(json.dumps(state,indent=2)+"\n")
    print("Published",len(new),"pages; total",len(state["pages"]))
if __name__=="__main__": main()
