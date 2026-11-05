"""Builds every HTML page of the AudioSplitAI site into ../web. Run: python3 gen/gen.py"""
import os, re, sys, math, json, html
sys.path.insert(0, os.path.dirname(__file__))
from guides_content import GUIDES as OLD

OUT = os.path.join(os.path.dirname(__file__), "..", "web")
BASE = "https://audiosplitai.si"
BRAND = "AudioSplitAI"
EMAIL = "lousdias0@gmail.com"
PLAY = "https://play.google.com/store/apps/details?id=com.black.tradictuin&referrer=utm_source%3Dweb"
UPDATED = "November 4, 2026"
ISO = "2026-11-04"
esc = html.escape

# ------------------------------------------------------------------ guide metadata
META = {
 "guide-remove-vocals.html": dict(
   seo="Remove Vocals from a Song Online with AI: Step-by-Step",
   desc="Learn how to remove vocals from a song with a free AI vocal remover. Step-by-step instructions, what to expect and tips for a clean instrumental.",
   quick="Open the splitter, choose your song, select <b>No vocals</b> and press split. When it finishes, press <b>Karaoke</b> in the mixer and export the <b>Full mix</b> as a WAV file.",
   related=["guide-make-karaoke-track.html", "guide-better-separation-tips.html", "guide-how-ai-separation-works.html"]),
 "guide-make-karaoke-track.html": dict(
   seo="Karaoke Maker Online: Make a Karaoke Track from Any Song",
   desc="Make a karaoke track from any song with a free online karaoke maker. Split the song with AI, mute the vocals and export your backing track.",
   quick="Split the song with <b>No vocals</b>, press <b>Karaoke</b> in the mixer to mute the singer, then export the <b>Full mix</b> as a backing track.",
   related=["guide-remove-vocals.html", "guide-better-separation-tips.html", "guide-what-are-stems.html"]),
 "guide-what-are-stems.html": dict(
   seo="What Are Stems in Music? Vocals, Drums and Bass Explained",
   desc="What are stems? Learn what music stems are, the four common stems (vocals, drums, bass, other) and how AI can split a finished song into stems.",
   quick="Stems are groups of instruments mixed together, usually <b>vocals, drums, bass and other</b>. They let you change the balance of a finished song.",
   related=["guide-how-ai-separation-works.html", "guide-isolate-drums-bass.html", "guide-remove-vocals.html"]),
 "guide-how-ai-separation-works.html": dict(
   seo="How AI Audio Separation Works: Stem Splitting Explained",
   desc="A plain-language explanation of how AI music source separation works, what Demucs-style models learn, and why the splitting runs in your browser.",
   quick="A neural network trained on many songs learns what voices, drums and bass look like in sound, then estimates each one as its own track.",
   related=["guide-what-are-stems.html", "guide-better-separation-tips.html", "guide-remove-vocals.html"]),
 "guide-better-separation-tips.html": dict(
   seo="10 Tips for Cleaner AI Stem Separation and Vocal Removal",
   desc="Ten practical tips for cleaner stem separation: choose a better source file, pick the right quality setting and fix small leftovers in the mixer.",
   quick="Start from the best file you have, choose <b>High</b> quality for songs that matter, listen on headphones, and fix small leftovers in the mixer.",
   related=["guide-remove-vocals.html", "guide-how-ai-separation-works.html", "guide-isolate-drums-bass.html"]),
 "guide-isolate-drums-bass.html": dict(
   seo="Separate Drums and Isolate Bass from a Song with AI",
   desc="How to separate drums from a song and isolate the bass line with a free AI stem splitter. Useful for practice, study and making samples.",
   quick="Split the song with <b>All tracks</b>, then press <b>Solo</b> on the Drums or Bass track in the mixer and export just that stem as WAV.",
   related=["guide-what-are-stems.html", "guide-better-separation-tips.html", "guide-how-ai-separation-works.html"]),
}
NEW_GUIDE = ("guide-isolate-drums-bass.html", "How to Separate Drums and Isolate Bass from a Song", "",
'''<p class="lead">Hearing only the drums, or only the bass, is one of the best ways to learn how a song is built. It is also the quickest way to get a loop, a groove to practise with, or a reference for your own mix. This guide shows how to separate drums and isolate the bass with AI.</p>
<h2>Which stems you will get</h2>
<p>AudioSplitAI splits a song into four stems: <b>vocals</b>, <b>drums</b>, <b>bass</b> and <b>other</b> (guitars, keys, strings and everything else). The drum stem contains the kick, snare, cymbals and percussion. The bass stem contains the bass guitar or synth bass. If you are new to the idea, read <a href="guide-what-are-stems.html">what stems are</a> first.</p>
<h2>Step by step</h2>
<ol><li>Open the <a href="./#tool">AudioSplitAI stem splitter</a> and choose your song.</li>
<li>Keep <b>All tracks</b> selected. The AI always analyses the whole song, so you lose nothing by creating every stem, and you can compare them.</li>
<li>Choose <b>High</b> quality in the options if you want the smoothest result and are happy to wait longer.</li>
<li>When processing ends, press <b>S</b> (solo) on the Drums strip to hear only the drums, or on the Bass strip to hear only the bass.</li>
<li>Use <b>Export</b>, tick the stem you need and download it as WAV. If you tick several, you get one ZIP file.</li></ol>
<h2>What to listen for</h2>
<ul><li><b>Drums:</b> you may hear small traces of hi-hat or cymbal bleed in the "other" stem and the reverse. That is normal.</li>
<li><b>Bass:</b> very low synth bass and the kick drum share the same frequencies, so the model sometimes places part of a low note in the drums. Listen to both stems together to judge it.</li>
<li><b>Sections:</b> use the waveform to jump to the chorus and check that the separation holds up in the busiest part of the song.</li></ul>
<h2>Practical uses</h2>
<ul><li><b>Practising an instrument.</b> Mute only your own instrument and play along with the rest. For example, mute the bass and play the bass line yourself.</li>
<li><b>Learning a groove.</b> Solo the drums and loop a bar with the loop button, or step back five seconds to hear a fill again.</li>
<li><b>Making samples.</b> Export the drum or bass stem as WAV to study or sample, as long as you have the right to use the recording.</li>
<li><b>Checking a mix.</b> Soloing the bass and drums shows whether the low end of a song is clean.</li></ul>
<h2>Common questions</h2>
<h3>Can I separate individual drums such as kick and snare?</h3>
<p>Not here. The model produces one drum stem. Separating the individual drums needs a different, more specialised tool.</p>
<h3>Why does my bass stem sound quiet?</h3>
<p>Small speakers do not reproduce low notes well. Listen on headphones or raise the bass strip volume in the mixer.</p>
<h3>Is the result the same as the studio stems?</h3>
<p>No. The stems are an AI estimate from the finished song. They are excellent for practice and study, but not identical to the original multitrack recording.</p>''')

GUIDES = [(fn, t, d, b) for fn, t, d, b in OLD] + [NEW_GUIDE]
# small improvements of the older texts
PATCH = {
 "guide-remove-vocals.html": [
   ("<li>Open the splitter and select your song.", '<li>Open the <a href="./#tool">free online stem splitter</a> and select your song.'),
   ("<li>Export the result as a WAV file.</li></ol>", "<li>For a single instrumental file, press <b>Karaoke</b> and use <b>Export</b> with <b>Full mix</b> ticked. For separate stems, tick the tracks you want. Files are saved as WAV.</li></ol>"),
   ("<h2>What it is good for</h2>", '''<h2>Common problems and fixes</h2>
<ul><li><b>A faint voice is still audible.</b> Try the <b>High</b> quality setting, or lower the other tracks slightly so the trace is hidden.</li>
<li><b>The instrumental sounds thin.</b> Check that the Bass and Other tracks are on and not muted, then export the Full mix again.</li>
<li><b>The page stops or reloads.</b> Close other tabs, try a shorter song, or use a computer. Phones have less memory than computers.</li></ul>
<h2>What it is good for</h2>'''),
 ],
 "guide-make-karaoke-track.html": [
   ("<li>Open the splitter and choose your song.</li>", '<li>Open the <a href="./#tool">AudioSplitAI karaoke maker</a> and choose your song.</li>'),
   ("<li>Use <b>Export</b> to save the backing track as WAV and play it on any device.</li></ol>", "<li>Use <b>Export</b>, tick <b>Full mix</b> and download the backing track as WAV. It keeps the Karaoke setting from the mixer.</li></ol>"),
 ],
}

# ------------------------------------------------------------------ shared pieces
bars = [(3,8),(8,14),(13,22),(18,32),(23,20),(28,26),(33,14),(38,8)]
LOGO = '<svg viewBox="0 0 44 36" width="34" height="28" aria-hidden="true" focusable="false"><defs><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7dffd0"/><stop offset="1" stop-color="#00c78a"/></linearGradient></defs>' + "".join(f'<rect class="lb" x="{x}" y="{18 - h / 2}" width="3.4" height="{h}" rx="1.7" fill="url(#lg)"/>' for x, h in bars) + '</svg>'
def header(active=""):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="sh"><div class="sh-in">
<a class="brand" href="./" aria-label="AudioSplitAI home">{LOGO}<span>Audio<b>Split</b>AI</span></a>
<nav id="nav" aria-label="Main">{a("./","Home","home")}{a("./#how","How It Works","how")}{a("guides.html","Guides","guides")}{a("./#faq","FAQ","faq")}{a("contact.html","Contact","contact")}</nav>
<a class="btn primary sm" href="./#tool"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M7 4.5v15l13-7.5z"/></svg>Start Splitting</a>
<button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><i></i><i></i><i></i></button>
</div></header>'''

def footer():
    return f'''<footer class="sf"><div class="sf-in">
<div class="sf-about"><a class="brand" href="./">{LOGO}<span>Audio<b>Split</b>AI</span></a>
<p>AudioSplitAI is a free online AI stem splitter. It separates songs into vocals, drums, bass and other stems and runs in your browser, so your audio is not uploaded.</p></div>
<nav aria-label="Footer"><b>Site</b><a href="./">Home</a><a href="guides.html">Guides</a><a href="about.html">About</a><a href="contact.html">Contact</a></nav>
<nav aria-label="Legal"><b>Legal</b><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Service</a><a href="#" id="ad-choices" hidden>Ad choices</a></nav>
</div><p class="copy">&copy; 2026 AudioSplitAI. Use only music you own or have permission to use.</p></footer>'''

def head(title, desc, path, og_type="website", extra=""):
    url = BASE + path
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#090D0B">
<meta property="og:site_name" content="{BRAND}"><meta property="og:type" content="{og_type}"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="AudioSplitAI: split music into vocals, drums, bass and other stems">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{BASE}/og-image.png">
<link rel="icon" href="icon.svg" type="image/svg+xml"><link rel="icon" href="icon-192.png" sizes="192x192" type="image/png"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="manifest.webmanifest">
<link rel="stylesheet" href="style.css">
{extra}</head>'''

def ld(*objs):
    return "".join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",", ":")) + "</script>\n" for o in objs)

def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement":
            [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(items)]}

ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": BRAND, "url": BASE + "/", "logo": {"@type": "ImageObject", "url": BASE + "/icon-512.png", "width": 512, "height": 512}, "email": EMAIL}

def tail(): return '<script src="ads-config.js" defer></script><script src="site.js" defer></script><script src="motion.js" defer></script>'

def write(fn, s): open(os.path.join(OUT, fn), "w", encoding="utf-8").write(s)

def info_page(fn, title, desc, body, active="", crumbs=None, og_type="website", extra_ld=()):
    crumbs = crumbs or [("Home", "/"), (title.split(" | ")[0], "/" + fn)]
    page = head(title, desc, "/" + fn, og_type) + f'''<body class="site">{header(active)}
<main id="main" class="doc">{body}</main>{footer()}
{ld(breadcrumb(crumbs), *extra_ld)}{tail()}</body></html>'''
    write(fn, page)

CTA = f'''<aside class="cta"><div><b>Try the free AI stem splitter</b><p>Split a song into vocals, drums, bass and other instruments, directly in your browser.</p></div><a class="btn primary" href="./#tool">Start Splitting</a></aside>
<aside class="cta app"><div><b>Prefer your phone?</b><p>The Audio Splitter Pro Android app adds MP3 export, voice recording over the music and a library of your songs.</p></div><a class="gbadge sm" href="{PLAY}" target="_blank" rel="noopener" aria-label="Get Audio Splitter Pro on Google Play"><img src="img/badge-android.webp" alt="Available on Android - Google Play" width="720" height="240" loading="lazy" decoding="async"><span class="shine" aria-hidden="true"></span></a></aside>'''

# ------------------------------------------------------------------ guides
def words(s): return len(re.sub(r"<[^>]+>", " ", s).split())
by_fn = {g[0]: g for g in GUIDES}
SEO_DESC = {}
for fn, t, d, b in GUIDES:
    m = META[fn]
    for old, new in PATCH.get(fn, []):
        assert old in b, (fn, old[:40]); b = b.replace(old, new)
    mins = max(1, math.ceil(words(b) / 200))
    rel = "".join(f'<a class="card" href="{r}"><b>{esc(by_fn[r][1])}</b><span>{esc(META[r]["desc"].split(".")[0])}.</span></a>' for r in m["related"])
    body = f'''<nav class="crumb" aria-label="Breadcrumb"><a href="./">Home</a> <span aria-hidden="true">&rsaquo;</span> <a href="guides.html">Guides</a></nav>
<article><h1>{esc(t)}</h1><p class="meta">{mins} min read &middot; Updated <time datetime="{ISO}">{UPDATED}</time></p>
<div class="quick"><b>Quick answer</b><p>{m["quick"]} <a href="./#tool">Open the splitter</a></p></div>
{b}</article>
<section aria-labelledby="rel"><h2 id="rel">Related guides</h2><div class="cards">{rel}</div></section>{CTA}'''
    art = {"@context": "https://schema.org", "@type": "Article", "headline": t, "description": m["desc"], "datePublished": ISO, "dateModified": ISO,
           "image": BASE + "/og-image.png", "inLanguage": "en", "mainEntityOfPage": BASE + "/" + fn,
           "author": {"@type": "Organization", "name": BRAND, "url": BASE + "/"}, "publisher": ORG}
    info_page(fn, m["seo"], m["desc"], body, "guides", [("Home", "/"), ("Guides", "/guides.html"), (t, "/" + fn)], "article", [art])
    SEO_DESC[fn] = (t, m["desc"], mins)

cards = "".join(f'<a class="card" href="{fn}"><b>{esc(SEO_DESC[fn][0])}</b><span>{esc(SEO_DESC[fn][1])}</span><em>{SEO_DESC[fn][2]} min read</em></a>' for fn, *_ in GUIDES)
info_page("guides.html", "AudioSplitAI Guides: Vocal Removal, Karaoke and Stem Splitting",
  "Practical guides on removing vocals, making karaoke tracks, understanding stems and getting cleaner AI audio separation.",
  f'<nav class="crumb" aria-label="Breadcrumb"><a href="./">Home</a> <span aria-hidden="true">&rsaquo;</span> <span>Guides</span></nav><h1>Guides</h1><p class="lead">Short, practical articles about splitting music with AI. Each one answers a specific question and links to the free stem splitter.</p><div class="cards">{cards}</div>{CTA}',
  "guides", [("Home", "/"), ("Guides", "/guides.html")])

# ------------------------------------------------------------------ about / contact / terms / privacy
info_page("about.html", "About AudioSplitAI: A Free, Private AI Stem Splitter",
  "What AudioSplitAI is, how the AI stem splitter works in your browser, and who is behind the site.", f'''
<nav class="crumb" aria-label="Breadcrumb"><a href="./">Home</a> <span aria-hidden="true">&rsaquo;</span> <span>About</span></nav>
<h1>About AudioSplitAI</h1>
<p class="lead">AudioSplitAI is a free online tool that separates a song into vocals, drums, bass and other instruments. The AI runs on your own device, inside your browser.</p>
<h2>Why it exists</h2>
<p>Many online vocal removers ask you to upload your music to a server, wait in a queue, or pay. We wanted a simpler option: open a page, choose a song and let your own computer do the work. Your files stay with you.</p>
<h2>What you can do</h2>
<ul><li>Split a song into four stems: vocals, drums, bass and other.</li><li>Create a karaoke version in one tap.</li><li>Preview and mix the stems with volume, mute and solo controls.</li><li>Download WAV files, or a ZIP when you export several tracks.</li></ul>
<h2>How it works</h2>
<p>The site uses a Hybrid Transformer Demucs model converted to the ONNX format. It is executed in your browser with ONNX Runtime Web. The model is downloaded once from Hugging Face and stored in your browser, and the separation itself happens on your device. For a plain-language explanation, read <a href="guide-how-ai-separation-works.html">how AI audio separation works</a>.</p>
<h2>Limits we are honest about</h2>
<ul><li>The stems are an AI estimate. Small traces of other instruments can remain, especially in dense mixes.</li><li>Processing speed depends on your device. Computers are usually faster than phones, and long songs need more memory.</li><li>Use only music you own or have permission to use.</li></ul>
<h2>The Android app</h2>
<p>The same idea is available as an Android app, Audio Splitter Pro, with MP3 export, voice recording over your music and a library of your songs. <a href="{PLAY}" target="_blank" rel="noopener">Get it on Google Play</a>.</p>
<h2>Funding and advertising</h2>
<p>The website is free. It may show advertising on its information pages to cover small running costs. The splitter itself does not show ads. Details are in the <a href="privacy.html">Privacy Policy</a>.</p>
<h2>Contact</h2><p>Questions, bugs or ideas? See the <a href="contact.html">contact page</a>.</p>{CTA}''', "about")

info_page("contact.html", "Contact AudioSplitAI: Support, Feedback and Copyright",
  "How to contact AudioSplitAI for support, feedback, bug reports and copyright questions.", f'''
<nav class="crumb" aria-label="Breadcrumb"><a href="./">Home</a> <span aria-hidden="true">&rsaquo;</span> <span>Contact</span></nav>
<h1>Contact</h1>
<p class="lead">We read every message. Please allow a few days for a reply.</p>
<h2>Email</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h2>For a faster fix, please include</h2>
<ul><li>Your device and browser, for example "Chrome on Windows" or "Safari on iPhone".</li><li>What you did and what you expected.</li><li>The exact error message shown on screen, if any.</li><li>The length and format of the song (for example "4 minutes, MP3").</li></ul>
<h2>Copyright and removal requests</h2><p>AudioSplitAI does not host, store or publish any music. Songs you choose are processed on your device only. If you believe the site is being used in a way that infringes your rights, write to the address above.</p>
<h2>Android app support</h2><p>For the Android app you can also reply to a review on <a href="{PLAY}" target="_blank" rel="noopener">Google Play</a> or email us.</p>
<h2>Before you write</h2><p>Many answers are in the <a href="./#faq">FAQ</a> and the <a href="guides.html">guides</a>.</p>''', "contact")

info_page("terms.html", "Terms of Service | AudioSplitAI",
  "Terms of Service for AudioSplitAI, the free online AI stem splitter.", f'''
<nav class="crumb" aria-label="Breadcrumb"><a href="./">Home</a> <span aria-hidden="true">&rsaquo;</span> <span>Terms of Service</span></nav>
<h1>Terms of Service</h1><p class="meta">Last updated {UPDATED}</p>
<h2>1. Using the service</h2><p>AudioSplitAI is a free tool that processes audio files inside your browser. By using it you agree to these terms.</p>
<h2>2. Your content</h2><p>Your files are processed on your device and are not uploaded to us. You are responsible for having the right to use the music you process and export. Do not use the service to infringe copyright or other rights.</p>
<h2>3. No warranty</h2><p>The service is provided "as is". Separation quality depends on the song and your device, and we do not guarantee any particular result or that the service will be uninterrupted or error free.</p>
<h2>4. Limitation of liability</h2><p>To the extent allowed by law, we are not liable for any loss or damage arising from the use of the service, including loss of data.</p>
<h2>5. Third-party services</h2><p>The site relies on third-party services such as content delivery networks and Hugging Face to load software and the AI model, and may display ads provided by Google. Their own terms and policies apply.</p>
<h2>6. Changes</h2><p>We may change the service or these terms at any time. Continued use means you accept the updated terms.</p>
<h2>7. Contact</h2><p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>''', "terms")

info_page("privacy.html", "Privacy Policy | AudioSplitAI",
  "How AudioSplitAI handles your audio, browser storage, third-party services, cookies and advertising.", f'''
<nav class="crumb" aria-label="Breadcrumb"><a href="./">Home</a> <span aria-hidden="true">&rsaquo;</span> <span>Privacy Policy</span></nav>
<h1>Privacy Policy</h1><p class="meta">Last updated {UPDATED}</p>
<p class="lead">AudioSplitAI processes your music <b>on your own device</b>, inside your browser. The songs you select and the tracks created are never uploaded to us or to anyone else. We have no accounts and no database of users.</p>
<h2>Data stored on your device</h2>
<p>The AI model (about 165 MB) is saved in your browser's storage after the first download, so it does not have to be downloaded again. Your choice about advertising cookies is saved in your browser's local storage. You can remove all of this by clearing this site's data in your browser settings.</p>
<h2>Third-party services</h2>
<p>To work, the page loads the ONNX Runtime Web library from the jsDelivr content network and downloads the AI model from Hugging Face. The site is hosted on GitHub Pages. These services may receive technical information such as your IP address and browser type, as with any web request. No audio or personal content is sent.</p>
<h2>Advertising and cookies</h2>
<p>This site may display ads from Google AdSense on its information pages (guides, about and similar). The splitter itself does not show ads.</p>
<ul><li>Third-party vendors, including Google, use cookies to serve ads based on your previous visits to this and other websites.</li>
<li>Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to this site and other sites on the internet.</li>
<li>You can opt out of personalised advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>. You can also visit <a href="https://www.aboutads.info" target="_blank" rel="noopener">aboutads.info</a> to opt out of some third-party vendors' use of cookies for personalised advertising.</li>
<li>More about how Google uses data: <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">How Google uses information from sites or apps that use our services</a>.</li>
<li>If you choose non-personalised ads in our banner, only non-personalised ads are requested. Visitors in the European Economic Area, the United Kingdom and Switzerland are asked for consent through Google's consent message where it is enabled.</li></ul>
<p>We do not use analytics or tracking tools of our own.</p>
<h2>Children</h2><p>The site is not directed at children under 13 and we do not knowingly collect personal information from children.</p>
<h2>Your rights</h2><p>Because we do not collect personal data ourselves, there is nothing for us to access or delete. For data held by the third parties above, please contact them directly.</p>
<h2>Changes</h2><p>We may update this policy. The date above shows the latest version.</p>
<h2>Contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>''', "privacy")

# 404
write("404.html", head("Page not found | AudioSplitAI", "This page does not exist. Go back to the AudioSplitAI stem splitter.", "/404.html").replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">').replace('<link rel="stylesheet" href="style.css">', '<base href="/"><link rel="stylesheet" href="style.css">') +
      f'<body class="site">{header()}<main id="main" class="doc"><h1>Page not found</h1><p class="lead">The page you are looking for does not exist or has moved.</p><p><a class="btn primary" href="./">Back to the splitter</a> <a class="btn outline" href="guides.html">Read the guides</a></p></main>{footer()}{tail()}</body></html>')

# ------------------------------------------------------------------ home page
FAQ = [
 ("Is AudioSplitAI free?", "Yes. You can split songs and download the stems for free. There is nothing to install and no account to create."),
 ("Is my music uploaded to a server?", "No. The AI model is downloaded to your browser and the separation runs on your own device. Your audio file is not sent to us or to any other server."),
 ("Which audio files can I use?", "Any audio file your browser can decode. This usually includes MP3, WAV, M4A/AAC, FLAC and OGG. If a file cannot be read, try converting it to MP3 or WAV."),
 ("Why does the first run take longer?", "The AI model (about 165 MB) is downloaded the first time and stored in your browser. Next time it loads from your device."),
 ("How long does splitting take?", "It depends on the length of the song, the quality setting and your device. A computer is usually faster than a phone. Keep the tab open while it works."),
 ("Why did the page stop or reload on my phone?", "The AI needs a lot of memory. Phones have less than computers, so long songs can fail. Close other tabs, try a shorter song, or use a computer."),
 ("Can I make a karaoke track?", "Yes. Split the song, press Karaoke in the mixer to mute the vocals, and export the Full mix as a WAV file."),
 ("Can I use the results commercially?", "Only if you have the rights to the original music. AudioSplitAI is a tool, and you are responsible for how you use the files you export."),
]
faq_html = "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)

STEMS = [("Vocals", "#00E08F", "Lead and backing vocals", '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>'),
         ("Drums", "#2BB5FF", "Kick, snare, cymbals", '<ellipse cx="12" cy="9" rx="8" ry="3"/><path d="M4 9v6c0 1.7 3.6 3 8 3s8-1.3 8-3V9M9 3l3 6M15 3l-3 6"/>'),
         ("Bass", "#FF9F1C", "Bass guitar or synth bass", '<path d="m14 4 6 6M10.5 7.5l6 6M4.2 19.8a3 3 0 0 0 4.2 0l.8-.8c.9-.9 1-2.3.2-3.3l-.9-1.1 5.3-5.3-3.2-3.2-5.3 5.3-1.1-.9c-1-.8-2.4-.7-3.3.2l-.8.8a3 3 0 0 0 0 4.2z"/>'),
         ("Other", "#B65CFF", "Guitar, keys, strings", '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>')]
stem_chips = "".join(f'<li style="--c:{c}"><i><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ic}</svg></i><div><b>{n}</b><span>{h}</span></div></li>' for n, c, h, ic in STEMS)
ICON = lambda p: f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
I_SPLIT = ICON('<path d="M3 12h3l2-6 4 12 3-9 2 3h4"/>')
I_MIC = ICON('<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>')
I_LAYERS = ICON('<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>')
I_LOCK = ICON('<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>')
I_UP = ICON('<path d="M12 16V4m0 0-4 4m4-4 4 4M4 20h16"/>')
I_CHIP = ICON('<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>')
I_DOWN = ICON('<path d="M12 4v12m0 0-4-4m4 4 4-4M4 20h16"/>')

FEATURES = [
 (I_SPLIT, "AI Stem Separation", "A Hybrid Transformer Demucs model splits a finished song into four stems: vocals, drums, bass and other. Choose which stems to create."),
 (I_MIC, "Online Karaoke Maker", "Press Karaoke in the mixer to mute the lead vocal and keep the backing music, then export it as a WAV file."),
 (I_LAYERS, "Individual Instrument Extraction", "Solo or mute the drums, the bass or the rest of the band to practise, study or collect samples you have the right to use."),
 (I_LOCK, "Private Browser-Based Processing", "The AI runs inside your browser. Your audio file is not uploaded, and nothing needs to be installed."),
]
feat_html = "".join(f'<article class="feat"><span class="fi">{i}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d in FEATURES)
STEPS = [(I_UP, "Upload Your Audio", "Choose a song or drop a file. MP3, WAV, M4A, FLAC and OGG are common formats that work in most browsers."),
         (I_CHIP, "AI Separates the Stems", "Pick the stems you want and start. The model works on your device, and a progress ring shows how far it is."),
         (I_DOWN, "Preview and Download Your Tracks", "Play the stems together, mute or solo each one, then download WAV files, or one ZIP for several tracks.")]
steps_html = "".join(f'<li><span class="si">{i}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in STEPS)
USES = [("Create karaoke instrumentals", "guide-make-karaoke-track.html"), ("Extract vocals for remixes", "guide-remove-vocals.html"), ("Isolate drums and bass", "guide-isolate-drums-bass.html"),
        ("Practice instruments", "guide-better-separation-tips.html"), ("Create music samples", "guide-what-are-stems.html")]
uses_html = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in USES)
home_guides = "".join(f'<a class="card" href="{fn}"><b>{esc(SEO_DESC[fn][0])}</b><span>{esc(SEO_DESC[fn][1].split(". ")[0].rstrip("."))}.</span><em>{SEO_DESC[fn][2]} min read</em></a>' for fn, *_ in GUIDES)

HOME_TITLE = "Free AI Stem Splitter Online | Separate Vocals, Drums & Bass — AudioSplitAI"
HOME_DESC = "Split songs into vocals, drums, bass and other stems with AudioSplitAI, a free online AI audio splitter. Create karaoke tracks and isolate instruments directly in your browser."

TOOL = '''<div class="tool-card" id="tool-box">
  <!-- HOME / UPLOAD -->
  <section class="screen" id="s-home" aria-label="Choose a song">
    <div class="drop" id="dropzone">
      <span class="drop-ic" aria-hidden="true"><img src="img/cloud.webp" alt="" width="92" height="69"></span>
      <h3>Upload your audio</h3>
      <label class="btn primary big" id="pick-btn">
        <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 3v10.55A4 4 0 1 0 14 17V7h4V3z"/></svg>
        Select a song
        <input type="file" id="file" accept="audio/*,.mp3,.m4a,.wav,.flac,.ogg,.aac" aria-label="Select an audio file">
      </label>
      <p class="hint" id="drop-hint">or drop an audio file here</p>
      <p class="formats">MP3, WAV, M4A, FLAC, OGG and other formats your browser can play</p>
    </div>
    <ul class="stem-chips" aria-label="Stems you can create">STEMCHIPS</ul>
    <p class="note" id="iso-note" hidden>Tip: reload this page once if splitting feels slow, so the browser can use more CPU threads.</p>
    <p class="small muted center-t">The AI engine (about 165 MB) downloads the first time and is then kept on your device. Your music never leaves it.</p>
  </section>

  <!-- PICK TRACKS -->
  <section class="screen" id="s-pick" hidden aria-label="Choose tracks">
    <header class="bar"><button class="icon" id="pick-back" aria-label="Back">&#8592;</button><h3>Split Audio</h3></header>
    <div class="song">
      <div class="disc" aria-hidden="true">&#9835;</div>
      <div class="grow"><div class="song-name" id="pick-name">song</div><div class="muted" id="pick-info">Reading file...</div></div>
    </div>
    <div class="label" id="what">WHAT DO YOU WANT?</div>
    <div class="chips" id="chips" role="group" aria-labelledby="what">
      <button class="chip on" data-set="all">All tracks</button>
      <button class="chip" data-set="vocals">Vocals only</button>
      <button class="chip" data-set="novocals">No vocals</button>
    </div>
    <div class="tiles" id="tiles"></div>
    <p class="muted small" id="pick-note">Only the tracks you choose are created. The AI always works on the whole song.</p>
    <details class="adv">
      <summary>Options</summary>
      <label class="row">Quality
        <select id="quality"><option value="4">High (slowest)</option><option value="10" selected>Balanced</option><option value="32">Fast</option></select>
      </label>
      <label class="row" id="gpu-row" hidden>Use the graphics card (experimental)
        <input type="checkbox" id="gpu">
      </label>
    </details>
    <p class="warn" id="pick-warn" hidden></p>
    <button class="btn primary wide" id="split" disabled>Split all 4 tracks</button>
  </section>

  <!-- PROCESSING -->
  <section class="screen center" id="s-proc" hidden aria-live="polite" aria-label="Processing">
    <div class="ring"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="track" cx="60" cy="60" r="52"/><circle class="arc" id="ring-arc" cx="60" cy="60" r="52"/></svg>
      <div class="pct" id="proc-pct">0%</div></div>
    <h3 id="proc-title">Processing your audio...</h3>
    <p class="muted" id="proc-status">Starting...</p>
    <div class="bar-wrap" id="dl-wrap" hidden><div class="bar-fill" id="dl-fill"></div></div>
    <p class="muted small" id="proc-eta"></p>
    <p class="muted small">Keep this tab open and in front. Browsers slow down tabs in the background, and splitting a song takes a few minutes.</p>
    <button class="btn outline" id="cancel">Cancel</button>
    <a class="miniad" href="PLAYURL" target="_blank" rel="noopener"><img src="icon.svg" alt="" width="38" height="38"><span><b>Waiting? Try the Android app</b><small>MP3 export, voice recording and a song library</small></span><em aria-hidden="true">&#8250;</em></a>
  </section>

  <!-- MIXER -->
  <section class="screen" id="s-mix" hidden aria-label="Mixer">
    <header class="bar">
      <button class="icon" id="mix-back" aria-label="Back">&#8592;</button>
      <h3 class="grow">Preview and download</h3>
      <button class="btn pill" id="open-export">&#11015; Export</button>
    </header>
    <div class="songrow"><div class="song-name grow" id="mix-name">song</div>
      <button class="btn pill karaoke" id="karaoke" hidden><span id="karaoke-ico" aria-hidden="true">&#127908;</span> Karaoke</button></div>
    <div id="strips" class="strips"></div>
    <div class="transport">
      <div class="seekrow"><span id="t-pos">0:00</span><input type="range" id="seek" min="0" max="1000" value="0" aria-label="Seek"><span id="t-dur">0:00</span></div>
      <div class="controls">
        <button class="icon" id="loop" aria-label="Loop" title="Loop">&#8635;</button>
        <button class="icon" id="back5" aria-label="Back 5 seconds" title="Back 5 seconds">&#9194;</button>
        <button class="play" id="play" aria-label="Play">&#9654;</button>
        <button class="icon" id="fwd5" aria-label="Forward 5 seconds" title="Forward 5 seconds">&#9193;</button>
        <span class="ghost"></span>
      </div>
    </div>
  </section>
</div>
<noscript><p class="note">The stem splitter needs JavaScript. Please turn it on in your browser settings.</p></noscript>'''.replace("STEMCHIPS", stem_chips).replace("PLAYURL", PLAY)

home_ld = [
 {"@context": "https://schema.org", "@graph": [
   {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": BRAND, "description": HOME_DESC, "inLanguage": "en", "publisher": {"@id": BASE + "/#org"}},
   ORG,
   {"@type": "WebApplication", "@id": BASE + "/#app", "name": BRAND, "url": BASE + "/", "description": "Free online AI stem splitter. Separates songs into vocals, drums, bass and other stems in your browser.",
    "applicationCategory": "MultimediaApplication", "operatingSystem": "Any modern web browser", "browserRequirements": "Requires JavaScript and WebAssembly",
    "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "inLanguage": "en",
    "featureList": ["Split songs into vocals, drums, bass and other stems", "Karaoke mode", "Mixer with volume, mute and solo", "Download WAV files or a ZIP"], "publisher": {"@id": BASE + "/#org"}}]}]

home = head(HOME_TITLE, HOME_DESC, "/", extra='<script src="coi-serviceworker.js"></script>\n') + f'''<body class="site home" data-noads>{header("home")}
<main id="main">
<section class="hero">
  <div class="hero-bg" aria-hidden="true"><img src="img/ribbon.webp" alt="" width="1536" height="210"></div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg>Free AI audio splitter</p>
      <h1>Split Music Into Vocals, Drums, Bass &amp; More <span class="g">with AI</span></h1>
      <p class="sub">Separate any song into individual audio stems with our free online AI stem splitter. Create karaoke tracks, isolate vocals, and extract instrumentals directly in your browser.</p>
      <div class="cta-row">
        <a class="btn primary big" href="#tool"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 18a4.5 4.5 0 0 1-.6-9A6 6 0 0 1 18 9.5a4 4 0 0 1-.5 8.5M12 21v-9m0 0-3 3m3-3 3 3"/></svg>Start Splitting<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg></a>
        <a class="btn outline big" href="#how"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M7 4.5v15l13-7.5z"/></svg>How It Works</a>
      </div>
    </div>
    <div class="hero-art"><img src="img/hero-mic.webp" alt="Studio microphone with headphones and glowing green sound waves" width="860" height="610" fetchpriority="high"></div>
  </div>
  <ul class="benefits">
    <li><img src="img/ic-bolt.webp" alt="" width="52" height="52"><span>Free Online<br>Audio Separation</span></li>
    <li><img src="img/ic-shield.webp" alt="" width="52" height="52"><span>No Software<br>Installation</span></li>
    <li><img src="img/ic-browser.webp" alt="" width="52" height="52"><span>Browser-Based<br>Processing</span></li>
    <li><img src="img/ic-lock.webp" alt="" width="52" height="52"><span>Private Audio<br>Processing</span></li>
  </ul>
</section>

<section class="sec" id="tool" aria-labelledby="tool-h"><div class="wrap narrow">
  <img class="sec-wave" src="img/wave.webp" alt="" width="96" height="42">
  <h2 id="tool-h">AI Stem <span class="g">Splitter</span></h2>
  <p class="sec-sub">Choose a song, pick the stems you need, then preview and download them.</p>
  {TOOL}
</div></section>

<section class="sec alt" aria-labelledby="feat-h"><div class="wrap">
  <div class="sec-title"><h2 id="feat-h">What <span class="g">AudioSplitAI</span> Does</h2></div>
  <p class="sec-sub">A free online stem splitter and karaoke maker that works in the browser.</p>
  <div class="feats">{feat_html}</div>
</div></section>

<section class="sec" aria-labelledby="stem-h"><div class="wrap">
  <div class="sec-title"><h2 id="stem-h">Four stems from <span class="g">every song</span></h2></div>
  <p class="sec-sub">Choose all of them, or only the ones you need.</p>
  <div class="stems-show">
    <figure><img src="img/stem-vocals.webp" alt="Vocals stem: lead and backing vocals" width="300" height="663" loading="lazy"></figure>
    <figure><img src="img/stem-drums.webp" alt="Drums stem: kick, snare and cymbals" width="300" height="675" loading="lazy"></figure>
    <figure><img src="img/stem-bass.webp" alt="Bass stem: bass guitar or synth bass" width="300" height="675" loading="lazy"></figure>
    <figure><img src="img/stem-other.webp" alt="Other stem: guitar, keys and strings" width="300" height="689" loading="lazy"></figure>
  </div>
</div></section>

<section class="sec" id="how" aria-labelledby="how-h"><div class="wrap narrow">
  <h2 id="how-h">How It Works</h2>
  <p class="sec-sub">Three steps from a finished song to separate stems.</p>
  <ol class="steps">{steps_html}</ol>
</div></section>

<section class="sec alt" aria-labelledby="use-h"><div class="wrap narrow">
  <h2 id="use-h">What you can use stems for</h2>
  <ul class="uses">{uses_html}</ul>
  <p class="muted small">Use only music you own or have permission to use.</p>
</div></section>

<section class="sec" aria-labelledby="gd-h"><div class="wrap">
  <h2 id="gd-h">Guides</h2>
  <p class="sec-sub">Learn how to remove vocals, make karaoke tracks and get cleaner results.</p>
  <div class="cards">{home_guides}</div>
  <p class="more"><a href="guides.html">All guides &rsaquo;</a></p>
</div></section>

<section class="sec" aria-labelledby="band-h"><div class="wrap narrow">
  <div class="band"><img src="img/eq.webp" alt="" width="736" height="300" loading="lazy">
    <h2 id="band-h">Ready to split your music?</h2>
    <p>Pick a song and get separate vocals, drums, bass and other stems in a few minutes.</p>
    <a class="btn big" href="#tool">Start Splitting</a></div>
</div></section>

<section class="sec alt" aria-labelledby="app-h"><div class="wrap narrow">
  <div class="promo"><div class="promo-glow" aria-hidden="true"></div><div class="promo-glow g2" aria-hidden="true"></div>
    <div class="promo-copy">
      <span class="tag"><i aria-hidden="true"></i>ANDROID APP</span>
      <h2 id="app-h">Take it everywhere with <span class="grad">the app</span></h2>
      <p>Audio Splitter Pro is our Android app. It runs the AI right on your phone, works without internet once installed, and adds even more features.</p>
      <ul class="ticks"><li>Export as <b>MP3</b>, M4A or WAV</li><li><b>Record your voice</b> over the music, then export</li><li>Your own <b>library</b> of split songs</li></ul>
      <a class="gbadge" href="{PLAY}" target="_blank" rel="noopener" aria-label="Get Audio Splitter Pro on Google Play"><img src="img/badge-android.webp" alt="Available on Android - Google Play" width="720" height="240" loading="lazy" decoding="async"><span class="shine" aria-hidden="true"></span></a>
    </div>
    <div class="promo-visual" aria-hidden="false"><div class="ring r1" aria-hidden="true"></div><div class="ring r2" aria-hidden="true"></div><img class="phones" src="img/app-phones.webp" alt="Audio Splitter Pro app: the mixer with vocals, drums, bass and your voice, and the export screen" width="1200" height="800" loading="lazy" decoding="async"><i class="note n1" aria-hidden="true">&#9835;</i><i class="note n2" aria-hidden="true">&#9834;</i><i class="note n3" aria-hidden="true">&#9833;</i></div>
  </div>
</div></section>

<section class="sec" id="faq" aria-labelledby="faq-h"><div class="wrap narrow">
  <h2 id="faq-h">Frequently asked questions</h2>
  {faq_html}
</div></section>
</main>{footer()}
{ld(*home_ld)}<script src="app.js" defer></script><script src="site.js" defer></script><script src="motion.js" defer></script>
<dialog id="exp" aria-labelledby="exp-h">
  <h3 id="exp-h">Export</h3>
  <div class="label">WHAT TO EXPORT</div>
  <div id="exp-list" class="exp-list"></div>
  <p class="muted small">WAV, lossless. Several files are downloaded together as one ZIP.</p>
  <p class="muted small" id="exp-msg" role="status"></p>
  <a class="miniad" href="{PLAY}" target="_blank" rel="noopener"><img src="icon.svg" alt="" width="38" height="38"><span><b>Need MP3 or M4A?</b><small>Get the Android app on Google Play</small></span><em aria-hidden="true">&#8250;</em></a>
  <div class="dlg-actions"><button class="btn outline" id="exp-close">Close</button><button class="btn primary" id="exp-go">Download</button></div>
</dialog>
<div id="toast" class="toast" hidden role="status"></div>
</body></html>'''
write("index.html", home)
print("pages:", len(GUIDES) + 6)

# sitemap.xml (official domain)
urls = ["/"] + ["/" + f for f in ["guides.html", "about.html", "contact.html", "privacy.html", "terms.html"] + [g[0] for g in GUIDES]]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{ISO}</lastmod></url>\n" for u in urls) + "</urlset>\n")

# ------------------------------------------------------------------ Windows app renderer (desktop/renderer)
import shutil
DESK = os.path.join(os.path.dirname(__file__), "..", "desktop", "renderer")
os.makedirs(DESK, exist_ok=True)
for f in ["app.js", "style.css", "icon.svg"]:
    shutil.copy(os.path.join(OUT, f), os.path.join(DESK, f))
desk = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data: blob:; media-src 'self' blob:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self' blob:">
<title>AudioSplitAI</title><link rel="stylesheet" href="style.css"></head>
<body class="site desktop">
<header class="sh"><div class="sh-in"><span class="brand">{LOGO}<span>Audio<b>Split</b>AI</span></span>
<a class="btn outline sm" style="margin-left:auto" href="{PLAY}" target="_blank" rel="noopener">Android app</a></div></header>
<main id="main"><section class="sec" id="tool" style="padding-top:28px"><div class="wrap narrow">
  <h1 style="font-size:clamp(24px,4vw,32px);text-align:center;margin-bottom:6px">Split music into stems</h1>
  <p class="sec-sub">Vocals, drums, bass and other. Everything runs on your PC, nothing is uploaded.</p>
  {TOOL}
</div></section></main>
<footer class="sf"><p class="copy" style="text-align:center">AudioSplitAI for Windows &middot; Uses HT-Demucs and ONNX Runtime (MIT licenses). Use only music you own or have permission to use.</p></footer>
<dialog id="exp" aria-labelledby="exp-h">
  <h3 id="exp-h">Export</h3>
  <div class="label">WHAT TO EXPORT</div>
  <div id="exp-list" class="exp-list"></div>
  <p class="muted small">WAV, lossless. Several files are downloaded together as one ZIP.</p>
  <p class="muted small" id="exp-msg" role="status"></p>
  <div class="dlg-actions"><button class="btn outline" id="exp-close">Close</button><button class="btn primary" id="exp-go">Save</button></div>
</dialog>
<div id="toast" class="toast" hidden role="status"></div>
<script src="app.js"></script>
</body></html>'''
open(os.path.join(DESK, "index.html"), "w", encoding="utf-8").write(desk)
