"""Generate Cascade Local SEO vertical landing pages from a single source of truth.

Each entry in VERTICALS produces public/local-seo-for-<slug>.html with full on-page
SEO + Service/BreadcrumbList/FAQPage schema, matching the homepage design via
/cascade.css. generate_og_image.py imports VERTICALS to render matching share cards.

Add a vertical = add a dict entry here, then also add it to sitemap.xml, the homepage
"Industries" section, and the render-audit verticalPageFor() map.
"""
from __future__ import annotations
import os, json, html

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public")
BASE = "https://cascadelocalseo.com"

# Shared pricing block bits (constant across verticals)
STARTER_LINK = "https://buy.stripe.com/28EaEZ0Kv2Hu18j9DC0co0e"
STANDARD_LINK = "https://buy.stripe.com/7sY9AV78Ta9W5oz1760co0i"

VERTICALS = {
    "med-spas": {
        "nav_meta": "Local SEO for med spas",
        "title": 'Local SEO for Med Spas — Rank for Botox, Filler &amp; "Med Spa Near Me" | Cascade',
        "meta_desc": "Local SEO built for med spas: rank in the Google map pack for treatment searches, build review velocity, and win high-intent patients from competitors. Start with a free audit.",
        "og_title": "Local SEO for Med Spas | Cascade Local SEO",
        "og_desc": "Get your med spa into the Google map pack for the treatment searches that actually convert. Free, specific audit — no pitch.",
        "tw_desc": "Rank your med spa in the map pack for treatment searches that convert. Free audit, no pitch.",
        "og_headline": "Local SEO for med spas.",
        "og_subline": "Get into the Google map pack for the treatment searches that actually book.",
        "h1": "Get your med spa into the map pack for the searches that actually book.",
        "lede": '"Botox near me." "Lip filler [your city]." "Med spa near me." These are people ready to book this week — and they click whoever owns the top three spots on Google Maps. I get med spas into those spots, then keep them there. Start with a free, specific audit. No pitch attached.',
        "cta_label": "Get your free med spa audit →",
        "why_heading": "Why med spa SEO is its own game",
        "why_intro": "The local-SEO fundamentals are the same everywhere, but what moves the needle for a med spa is specific. The audit and the work both account for it:",
        "why_bullets": [
            ("Treatment-level intent.", 'Patients rarely search "med spa." They search "botox," "lip filler," "morpheus8," "laser hair removal [city]." Your Google Business Profile services and your site need to map to those exact treatments — most med spas leave this blank.'),
            ("Reviews are the currency.", "Aesthetics is a trust purchase. Review volume and recency are among the heaviest local-pack signals, and your top competitors are usually winning on count, not quality. This is the single most closeable gap for most med spas."),
            ("You're competing with bigger logos.", "Dermatology and plastic-surgery groups outrank you on brand — but they often neglect their Google profiles. That's the opening."),
            ("Map pack &gt; website.", 'For "near me" treatment searches, the three-result map pack captures the majority of clicks before anyone scrolls to a website. Winning local means winning the pack first.'),
        ],
        "sample": {
            "name": "Lumière Aesthetics &amp; Med Spa", "sub": "Med spa / aesthetics",
            "stats": [("Google Rating", "4.4★", "warn"), ("Reviews", "23", "bad"), ('Rank for "med spa"', "#7", "bad")],
            "losing_title": "Where you're losing high-intent searches",
            "losing": [
                ("Review volume:", "23 reviews vs the top-3 average of 140+. In aesthetics, review count is the heaviest local-pack lever — and the biggest gap here."),
                ("Treatment keywords unmapped:", "your profile lists \"med spa\" but not botox, filler, or laser as services — so you're invisible for the searches that actually book."),
                ("Local pack position:", "#7 — off the map pack entirely for your primary term, where ~70% of clicks happen."),
            ],
            "levers": [
                ("Review velocity system:", "a structured monthly collection flow plus a response on every review, closing the gap to the top-3 count."),
                ("Treatment-mapped profile + posts:", "services and weekly GBP posts targeting botox, filler, and your highest-margin treatments by name."),
                ("Citation + NAP cleanup:", "consistent name/address/phone across the directories that aesthetics patients and Google both check."),
            ],
        },
        "how_keywords": "treatment keywords",
        "rank_keyword_phrase": "top treatment keywords",
        "longtail_phrase": "treatment long-tails",
        "human_review_note": " — important for a med spa's compliance line",
        "mailto_suffix": "med spa", "mailto_biz": "med spa",
        "faq_heading": "Med spa SEO — FAQ",
        "faqs": [
            {"q": 'How long until my med spa ranks for treatment keywords like "botox near me"?',
             "a": "For most map-pack improvements: 30–90 days. Treatment-level keywords (botox, filler, laser, microneedling) move once your Google Business Profile categories, services, and review velocity line up with intent. High-competition metros take longer than suburban markets. You'll get a realistic timeline in your free audit."},
            {"q": "We already get patients from Instagram. Do we need Google too?",
             "a": 'Instagram builds demand; Google captures it. Someone who sees your work on Instagram still searches your name or "med spa near me" before booking — and if a competitor owns the map pack, that\'s who they call. The channels compound.'},
            {"q": "How do we compete with dermatology and plastic surgery groups?",
             "a": "Bigger groups often under-optimize their Google profiles and lean on brand. Med spas win locally by mapping services to specific treatment searches, posting consistently, and out-collecting reviews. The audit shows where the larger competitors are beatable in your area."},
            {"q": "Is review collection and responding HIPAA-safe?",
             "a": "Yes, done carefully. Review responses never confirm treatments or disclose patient details — they stay generic and warm. I draft every response for your approval before anything posts, so you keep control of the compliance line."},
            {"q": "Do you only work with med spas?",
             "a": "No — the same playbook works for any local service business. But med spas are a vertical I work in often, so the audit speaks the language of treatment searches, review velocity, and aesthetic-market competition.",
             "more": ' <a href="/">See the main page →</a>'},
        ],
        "service_type": "Local SEO for med spas and aesthetic clinics",
        "service_desc": "Local search marketing for med spas: Google map pack ranking for treatment keywords, review velocity programs, Google Business Profile content, and citation cleanup.",
    },

    "chiropractors": {
        "nav_meta": "Local SEO for chiropractors",
        "title": 'Local SEO for Chiropractors — Own "Chiropractor Near Me" | Cascade',
        "meta_desc": "Local SEO built for chiropractors: rank in the Google map pack for 'chiropractor near me', win new-patient searches, and out-rank the practices fighting for the same three spots. Free audit.",
        "og_title": "Local SEO for Chiropractors | Cascade Local SEO",
        "og_desc": "Own 'chiropractor near me' in your town. Get into the Google map pack for new-patient searches. Free, specific audit — no pitch.",
        "tw_desc": "Own 'chiropractor near me' in your town and win new-patient searches. Free audit, no pitch.",
        "og_headline": "Local SEO for chiropractors.",
        "og_subline": "Own “chiropractor near me” in your town and win the new-patient searches.",
        "h1": 'Own "chiropractor near me" in your town.',
        "lede": 'When someone\'s back goes out, they search "chiropractor near me" and call one of the top three on Google Maps — usually before they finish their coffee. I get chiropractic practices into those three spots and keep them there. Start with a free, specific audit. No pitch attached.',
        "cta_label": "Get your free chiropractic audit →",
        "why_heading": "Why chiropractic SEO is different",
        "why_intro": "The local-SEO fundamentals are universal, but what actually wins new patients for a chiropractor is specific. The audit and the work both account for it:",
        "why_bullets": [
            ("High-intent, now-or-never searches.", '"Chiropractor near me" and "back pain [city]" are booked-this-week intent. There\'s no long consideration cycle — whoever\'s in the map pack gets the call. Ranking matters more here than in almost any vertical.'),
            ("Dense local competition.", "Most towns have far more chiropractors than top-3 map slots. The ones ranking aren't the best clinicians — they're the ones who optimized their Google profile and collect reviews. That's a beatable bar."),
            ("Reviews drive the choice.", "People in pain pick on trust and proximity. Review volume and recency are heavy ranking signals and the deciding factor once you're visible — and it's where most practices fall behind."),
            ("Recurring-visit value.", "A new chiropractic patient is worth months of visits, so a single top-3 ranking compounds into real revenue. The math on local SEO works better here than for one-off-purchase businesses."),
        ],
        "sample": {
            "name": "Summit Spine &amp; Chiropractic", "sub": "Chiropractic practice",
            "stats": [("Google Rating", "4.5★", "warn"), ("Reviews", "31", "bad"), ('Rank for "chiropractor"', "#6", "bad")],
            "losing_title": "Where you're losing new patients",
            "losing": [
                ("Review volume:", "31 reviews vs the top-3 average of 110+. For a now-or-never search, review count decides both ranking and the click."),
                ("Local pack position:", "#6 — outside the top three that capture the bulk of \"chiropractor near me\" calls in your area."),
                ("Profile + posting gaps:", "services and weekly posts don't target \"back pain\", \"sciatica\", or \"auto injury\" — the searches that bring new patients, not just brand lookups."),
            ],
            "levers": [
                ("Review velocity system:", "a structured monthly ask plus a response on every review, closing the gap to the top-3 count."),
                ("Intent-mapped profile + posts:", "services and weekly GBP posts targeting your highest-value conditions and treatments by name."),
                ("Citation + NAP cleanup:", "consistent name/address/phone across the health directories Google cross-checks for trust."),
            ],
        },
        "how_keywords": "patient-intent keywords",
        "rank_keyword_phrase": "top patient keywords",
        "longtail_phrase": "condition long-tails",
        "human_review_note": "",
        "mailto_suffix": "chiropractic", "mailto_biz": "practice",
        "faq_heading": "Chiropractic SEO — FAQ",
        "faqs": [
            {"q": "How fast will local SEO bring my practice new patients?",
             "a": 'Most map-pack improvements show in 30–90 days. "Chiropractor near me" is high-intent — people looking to book now — so once you\'re in the top three, new-patient calls tend to follow quickly. Saturated towns take longer. Your free audit includes a realistic timeline.'},
            {"q": "Most of my patients come from referrals. Why do I need Google?",
             "a": 'Even referred patients Google your name before they call — and "chiropractor near me" is how people in pain find a new practice today. If you\'re not in the map pack, those searches go to whoever is. Local SEO captures the demand referrals don\'t cover.'},
            {"q": "Five chiropractors in my town fight for the top spots. Can I still rank?",
             "a": "Usually yes. The ranking practices are rarely the best chiropractors — they're the ones who optimized their Google profile, collect reviews consistently, and post regularly. Most of your competitors aren't doing that. The audit shows which gaps are open."},
            {"q": "I'm a solo chiropractor, not a group. Is this overkill?",
             "a": "No — solo and single-location practices are the best fit, because the whole game is one Google Business Profile ranking in one town. You don't need national SEO; you need to own your local map pack."},
            {"q": "Do you only work with chiropractors?",
             "a": "No — the same playbook works for any local service business. But chiropractic is a vertical I work in often, so the audit understands new-patient intent and dense local competition.",
             "more": ' <a href="/">See the main page →</a>'},
        ],
        "service_type": "Local SEO for chiropractic practices",
        "service_desc": "Local search marketing for chiropractors: Google map pack ranking for 'chiropractor near me' and new-patient searches, review velocity programs, Google Business Profile content, and citation cleanup.",
    },

    "dentists": {
        "nav_meta": "Local SEO for dentists",
        "title": 'Local SEO for Dentists — Win "Dentist Near Me" &amp; New Patients | Cascade',
        "meta_desc": "Local SEO built for dental practices: rank in the Google map pack for 'dentist near me' and high-value treatment searches, build reviews, and beat corporate dental groups. Free audit.",
        "og_title": "Local SEO for Dentists | Cascade Local SEO",
        "og_desc": "Win 'dentist near me' and the high-value patient searches in your area. Free, specific audit — no pitch.",
        "tw_desc": "Win 'dentist near me' and the high-value patient searches in your area. Free audit, no pitch.",
        "og_headline": "Local SEO for dentists.",
        "og_subline": "Win “dentist near me” and the high-value patient searches in your area.",
        "h1": 'Win "dentist near me" — and the new patients behind it.',
        "lede": 'People choosing a dentist search "dentist near me" or "emergency dentist [city]," then pick from the top three on the map by reviews and proximity. I get dental practices into those spots and keep them there. Start with a free, specific audit. No pitch attached.',
        "cta_label": "Get your free dental audit →",
        "why_heading": "Why dental SEO is different",
        "why_intro": "The local-SEO fundamentals are universal, but what actually brings a dental practice new patients is specific. The audit and the work both account for it:",
        "why_bullets": [
            ("High-value, recurring patients.", "A new patient is worth years of cleanings, plus crowns, implants, and ortho. One top-3 ranking compounds into serious lifetime value — the math on local SEO is strong for dental."),
            ("Treatment + emergency intent.", '"Dentist near me" is the floor. "Emergency dentist," "dental implants [city]," and "Invisalign near me" are higher-value searches most practices never map to their profile or site.'),
            ("Competing with corporate groups (DSOs).", "Aspen, Heartland, and local DSOs outspend you — but they run generic, cookie-cutter profiles. Independent practices win on reviews, responsiveness, and treatment-specific optimization."),
            ("Reviews decide the click.", "Dentistry is high-trust. Review volume and recency drive both ranking and which practice the patient actually calls — and most offices are behind."),
        ],
        "sample": {
            "name": "Riverbend Family &amp; Cosmetic Dentistry", "sub": "General &amp; cosmetic dentistry",
            "stats": [("Google Rating", "4.6★", "warn"), ("Reviews", "41", "bad"), ('Rank for "dentist"', "#5", "bad")],
            "losing_title": "Where you're losing new patients",
            "losing": [
                ("Review volume:", "41 reviews vs the top-3 average of 160+. For a high-trust choice, review count drives both ranking and the call."),
                ("Local pack position:", "#5 — outside the top three that capture the bulk of \"dentist near me\" searches in your area."),
                ("High-value keywords unmapped:", "implants, Invisalign, and emergency care aren't listed as services — so you're invisible for the searches worth the most."),
            ],
            "levers": [
                ("Review velocity system:", "a structured post-visit ask plus a response on every review, closing the gap to the top-3 count."),
                ("Treatment-mapped profile + posts:", "services and weekly GBP posts targeting implants, cosmetic, and emergency care by name."),
                ("Citation + NAP cleanup:", "consistent name/address/phone across the health and dental directories Google cross-checks."),
            ],
        },
        "how_keywords": "patient-intent keywords",
        "rank_keyword_phrase": "top patient keywords",
        "longtail_phrase": "treatment long-tails",
        "human_review_note": "",
        "mailto_suffix": "dental", "mailto_biz": "practice",
        "faq_heading": "Dental SEO — FAQ",
        "faqs": [
            {"q": 'How long until my practice ranks for "dentist near me"?',
             "a": "Most map-pack improvements show in 30–90 days, once your Google Business Profile categories, services, and review velocity line up with intent. Competitive metros take longer than suburban markets. Your free audit includes a realistic timeline."},
            {"q": "We're already busy — do we even need more visibility?",
             "a": "Visibility isn't just more patients; it's the right patients — high-value treatments, filling a new hygienist's column, and replacing the natural attrition every practice has. Rankings also protect you against slow seasons and a new competitor opening nearby."},
            {"q": "How do we compete with the big dental chains?",
             "a": "DSOs outspend you but run generic profiles and lean on ads. Independent practices win on review volume, fast responses, and mapping specific treatments to search — exactly where the audit finds the openings."},
            {"q": "Is review collection compliant for a dental office?",
             "a": "Yes, done carefully. Review responses never disclose patient health information — they stay generic and warm. I draft every response for your approval before it posts, so you keep control of the compliance line."},
            {"q": "Do you only work with dentists?",
             "a": "No — the same playbook works for any local service business. But dental is a vertical I work in often, so the audit understands patient lifetime value, treatment intent, and DSO competition.",
             "more": ' <a href="/">See the main page →</a>'},
        ],
        "service_type": "Local SEO for dental practices",
        "service_desc": "Local search marketing for dentists: Google map pack ranking for 'dentist near me' and treatment searches, review velocity programs, Google Business Profile content, and citation cleanup.",
    },

    "lawyers": {
        "nav_meta": "Local SEO for law firms",
        "title": 'Local SEO for Lawyers — Rank for "Attorney Near Me" | Cascade',
        "meta_desc": "Local SEO for law firms: rank in the Google map pack for high-value practice-area searches, build reviews, and compete without burning budget on LSAs and PPC alone. Free audit.",
        "og_title": "Local SEO for Law Firms | Cascade Local SEO",
        "og_desc": "Rank for the high-value practice-area searches before you pay for the click. Free, specific audit — no pitch.",
        "tw_desc": "Rank for practice-area searches before you pay per click. Free audit, no pitch.",
        "og_headline": "Local SEO for law firms.",
        "og_subline": "Rank for the high-value practice-area searches before you pay for the click.",
        "h1": 'Rank for "attorney near me" — before you pay for the click.',
        "lede": 'Legal clicks are some of the most expensive in all of paid search. Ranking organically in the map pack for "personal injury attorney [city]" or "DUI lawyer near me" puts you in front of the same high-intent clients without paying per click. I get firms into those spots and keep them there. Free, specific audit — no pitch.',
        "cta_label": "Get your free law firm audit →",
        "why_heading": "Why law firm SEO is different",
        "why_intro": "The local-SEO fundamentals are universal, but what actually wins cases for a firm is specific. The audit and the work both account for it:",
        "why_bullets": [
            ("The highest-value clicks in local search.", "A single case can be worth thousands to six figures — and legal keywords are the priciest in PPC. Ranking organically captures that intent without the per-click bill."),
            ("Practice-area intent.", 'Clients don\'t search "lawyer." They search "DUI attorney," "personal injury lawyer near me," "family law attorney [city]." Your profile and site need to map to your exact practice areas.'),
            ("Reviews and trust signals decide it.", "People hiring a lawyer are anxious and skeptical. Review volume, recency, and thoughtful responses move both ranking and whether they call you or the firm above you."),
            ("Beatable competition.", "Many firms over-rely on LSAs and PPC and neglect organic and their Google profile. That's the opening to own the map pack."),
        ],
        "sample": {
            "name": "Harbor &amp; Vance, LLP", "sub": "Personal injury &amp; family law",
            "stats": [("Google Rating", "4.7★", "warn"), ("Reviews", "28", "bad"), ('Rank for "PI attorney"', "#6", "bad")],
            "losing_title": "Where you're losing high-value clients",
            "losing": [
                ("Review volume:", "28 reviews vs the top-3 average of 110+. For an anxious, high-stakes decision, review count drives both ranking and the call."),
                ("Local pack position:", "#6 — off the map pack for your primary practice area, where the highest-intent searches happen."),
                ("Practice areas unmapped:", 'your profile says "law firm" but not "personal injury," "family law," or "criminal defense" — so you miss the searches that match your best cases.'),
            ],
            "levers": [
                ("Review velocity system:", "a structured ask at case close plus a response on every review, closing the gap to the top-3 count."),
                ("Practice-area-mapped profile + posts:", "services and weekly GBP posts targeting each practice area by name."),
                ("Citation + NAP cleanup:", "consistent name/address/phone across legal directories like Avvo, Justia, and FindLaw that Google cross-checks."),
            ],
        },
        "how_keywords": "practice-area keywords",
        "rank_keyword_phrase": "top practice-area keywords",
        "longtail_phrase": "practice-area long-tails",
        "human_review_note": " — important for your bar advertising rules",
        "mailto_suffix": "law firm", "mailto_biz": "firm",
        "faq_heading": "Law firm SEO — FAQ",
        "faqs": [
            {"q": "How is this different from Google LSAs or PPC?",
             "a": "LSAs and PPC charge per lead or click and stop the moment your budget does. Map-pack rankings are owned and compound over time — they capture the same high-intent searches without the per-click bill. They work best running alongside paid, not instead of it."},
            {"q": "We handle multiple practice areas — can you rank us for all of them?",
             "a": "Yes, prioritized. We map each practice area to your profile services and content and start with your highest-value, most-winnable areas, then expand. The audit shows which are realistic in your market."},
            {"q": "Bar advertising rules are strict — is review collection compliant?",
             "a": "Yes, done carefully. We never solicit prohibited testimonials, and every response is generic and drafted for your approval before it posts. You keep control of the ethics line."},
            {"q": "How fast will I rank for a competitive area like personal injury?",
             "a": "Competitive metros for PI take longer; suburban and secondary practice areas move faster. Most map-pack gains land in 30–90 days. You'll get a realistic, area-by-area timeline in your free audit."},
            {"q": "Do you only work with law firms?",
             "a": "No — the same playbook works for any local service business. But legal is a vertical I work in often, so the audit understands practice-area intent and the LSA/PPC landscape.",
             "more": ' <a href="/">See the main page →</a>'},
        ],
        "service_type": "Local SEO for law firms",
        "service_desc": "Local search marketing for law firms: Google map pack ranking for practice-area searches, review velocity programs, Google Business Profile content, and citation cleanup.",
    },

    "hvac": {
        "nav_meta": "Local SEO for HVAC companies",
        "title": 'Local SEO for HVAC Companies — Win "AC Repair Near Me" | Cascade',
        "meta_desc": "Local SEO for HVAC contractors: rank in the Google map pack for emergency and seasonal searches like 'AC repair near me', build reviews, and own your service area. Free audit.",
        "og_title": "Local SEO for HVAC Companies | Cascade Local SEO",
        "og_desc": "Own 'AC repair near me' when the heat hits and the calls spike. Free, specific audit — no pitch.",
        "tw_desc": "Own 'AC repair near me' when demand spikes. Free audit, no pitch.",
        "og_headline": "Local SEO for HVAC companies.",
        "og_subline": "Own “AC repair near me” when the heat hits and the calls spike.",
        "h1": 'Own "AC repair near me" when the temperature spikes.',
        "lede": 'When the AC dies in a heatwave, people search "AC repair near me" and call the top three on the map — fast. HVAC is won on emergency intent, seasonal surges, and reviews. I get HVAC companies into the pack and keep them there. Free, specific audit — no pitch.',
        "cta_label": "Get your free HVAC audit →",
        "why_heading": "Why HVAC SEO is different",
        "why_intro": "The local-SEO fundamentals are universal, but what actually brings an HVAC company calls is specific. The audit and the work both account for it:",
        "why_bullets": [
            ("Emergency and seasonal intent.", '"AC repair near me," "furnace not working," and "emergency HVAC" are book-now searches that spike with the weather. Being in the pack the moment demand surges is the whole game.'),
            ("You're a service-area business.", "No storefront means you rank by service area, not a street address. Getting your service areas and primary category right in Google Business Profile is make-or-break — and usually misconfigured."),
            ("Reviews drive the call.", "Homeowners pick on trust under pressure. Review volume and recency move ranking and the click — and most of your local competitors are behind on both."),
            ("Competing with franchises.", "Big franchise brands outspend you but run cookie-cutter profiles. A sharp local profile plus a steady review cadence beats them in the pack."),
        ],
        "sample": {
            "name": "Cascade Comfort Heating &amp; Air", "sub": "Residential HVAC · service-area business",
            "stats": [("Google Rating", "4.5★", "warn"), ("Reviews", "38", "bad"), ('Rank for "AC repair"', "#7", "bad")],
            "losing_title": "Where you're losing calls",
            "losing": [
                ("Review volume:", "38 reviews vs the top-3 average of 130+. For an urgent search, review count drives both ranking and the call."),
                ("Local pack position:", "#7 — off the map pack for your primary service, where the book-now searches happen."),
                ("Service areas unset:", "neighboring towns you actually serve aren't configured, so you never appear for their searches."),
            ],
            "levers": [
                ("Review velocity system:", "an automatic text-to-review after each completed job, closing the gap to the top-3 count."),
                ("Service-area + category setup:", "correct primary category, service areas, and seasonal GBP posts so you show up across your whole territory."),
                ("Citation + NAP cleanup:", "consistent name/address/phone across the home-service directories Google cross-checks."),
            ],
        },
        "how_keywords": "service keywords",
        "rank_keyword_phrase": "top service keywords",
        "longtail_phrase": "service long-tails",
        "human_review_note": "",
        "mailto_suffix": "HVAC company", "mailto_biz": "company",
        "faq_heading": "HVAC SEO — FAQ",
        "faqs": [
            {"q": "We don't have a storefront — can we still rank?",
             "a": "Yes. You're a service-area business, and Google ranks you by the areas you serve, not a street address. Configuring service areas and your primary category correctly is exactly what most HVAC companies get wrong — and it's the first thing the audit checks."},
            {"q": "Our demand is seasonal — does SEO keep up?",
             "a": "Rankings compound year-round, so you're already on top of the pack when the season hits instead of scrambling for visibility mid-heatwave. We lean your posts and keywords into the upcoming season ahead of the surge."},
            {"q": "How do we compete with the big franchises?",
             "a": "Franchises run generic profiles and lean on ad spend. A well-configured local profile, a steady review cadence, and seasonal posts beat them in the map pack — where the book-now calls actually happen."},
            {"q": "How fast will I see more calls?",
             "a": "Most map-pack improvements land in 30–90 days. Emergency intent converts fast once you're visible — being top-3 means you're the first call when something breaks."},
            {"q": "Do you only work with HVAC companies?",
             "a": "No — the same playbook works for any local service business. But HVAC is a vertical I work in often, so the audit understands emergency intent, seasonality, and service-area configuration.",
             "more": ' <a href="/">See the main page →</a>'},
        ],
        "service_type": "Local SEO for HVAC contractors",
        "service_desc": "Local search marketing for HVAC companies: Google map pack ranking for emergency and seasonal service searches, service-area configuration, review velocity programs, and citation cleanup.",
    },

    "plumbers": {
        "nav_meta": "Local SEO for plumbers",
        "title": 'Local SEO for Plumbers — Win "Emergency Plumber Near Me" | Cascade',
        "meta_desc": "Local SEO for plumbing companies: rank in the Google map pack for urgent searches like 'emergency plumber near me', build reviews, and own your service area. Free audit.",
        "og_title": "Local SEO for Plumbers | Cascade Local SEO",
        "og_desc": "Be the first call when 'emergency plumber near me' gets searched. Free, specific audit — no pitch.",
        "tw_desc": "Be the first call for 'emergency plumber near me'. Free audit, no pitch.",
        "og_headline": "Local SEO for plumbers.",
        "og_subline": "Be the first call when “emergency plumber near me” gets searched.",
        "h1": 'Be the first call for "emergency plumber near me."',
        "lede": 'A burst pipe doesn\'t wait. People search "emergency plumber near me" and call the top of the map immediately. Plumbing is won on urgent intent and reviews — and most competitors leave their Google profile half-built. I fix that and get you in the pack. Free, specific audit — no pitch.',
        "cta_label": "Get your free plumbing audit →",
        "why_heading": "Why plumbing SEO is different",
        "why_intro": "The local-SEO fundamentals are universal, but what actually brings a plumbing company calls is specific. The audit and the work both account for it:",
        "why_bullets": [
            ("Urgent, right-now intent.", '"Emergency plumber," "water heater repair near me," and "clogged drain" are book-this-hour searches. Whoever owns the top three gets the call before anyone reads a website.'),
            ("You're a service-area business.", "You rank by where you serve, not a storefront. Service areas and primary category in Google Business Profile decide whether you show up in neighboring towns — and they're usually wrong."),
            ("Reviews are the tiebreaker.", "Under pressure, homeowners pick the trusted name. Review volume and recency drive both ranking and the call."),
            ("Beatable local field.", "Most plumbers don't post, don't ask for reviews systematically, and have inconsistent citations. That's three open gaps the audit pinpoints."),
        ],
        "sample": {
            "name": "Summit Drain &amp; Plumbing", "sub": "Residential plumbing · service-area business",
            "stats": [("Google Rating", "4.6★", "warn"), ("Reviews", "34", "bad"), ('Rank for "emergency plumber"', "#6", "bad")],
            "losing_title": "Where you're losing calls",
            "losing": [
                ("Review volume:", "34 reviews vs the top-3 average of 120+. For an urgent call, review count drives both ranking and the click."),
                ("Local pack position:", "#6 — off the map pack for your primary service, where the book-now searches happen."),
                ("Service areas unset:", "the nearby towns you serve aren't configured, so you miss their searches entirely."),
            ],
            "levers": [
                ("Review velocity system:", "an automatic text-to-review on job completion, closing the gap to the top-3 count."),
                ("Service-area + category setup:", "correct primary category, service areas, and posts for high-value jobs like water-heater and repipe."),
                ("Citation + NAP cleanup:", "consistent name/address/phone across the home-service directories Google cross-checks."),
            ],
        },
        "how_keywords": "service keywords",
        "rank_keyword_phrase": "top service keywords",
        "longtail_phrase": "service long-tails",
        "human_review_note": "",
        "mailto_suffix": "plumbing company", "mailto_biz": "company",
        "faq_heading": "Plumbing SEO — FAQ",
        "faqs": [
            {"q": "We don't have a storefront — can we still rank?",
             "a": "Yes. You're a service-area business, and Google ranks you by the areas you serve. Setting up service areas and your primary category correctly is exactly what most plumbers get wrong — and the first thing the audit checks."},
            {"q": "Most of our jobs are emergencies — does SEO actually help?",
             "a": 'It helps most there. "Emergency plumber near me" is a map-pack search by definition — being top-3 means you\'re the first call when a pipe bursts, before anyone compares websites.'},
            {"q": "How do we compete with bigger plumbing outfits?",
             "a": "Bigger outfits often run generic profiles and lean on ads. A well-configured local profile and a steady review cadence beat them in the pack, where the urgent calls happen."},
            {"q": "How fast will I see more calls?",
             "a": "Most map-pack improvements land in 30–90 days. Urgent intent converts fast once you're visible."},
            {"q": "Do you only work with plumbers?",
             "a": "No — the same playbook works for any local service business. But plumbing is a vertical I work in often, so the audit understands urgent intent and service-area configuration.",
             "more": ' <a href="/">See the main page →</a>'},
        ],
        "service_type": "Local SEO for plumbing companies",
        "service_desc": "Local search marketing for plumbers: Google map pack ranking for emergency and urgent service searches, service-area configuration, review velocity programs, and citation cleanup.",
    },

    "roofers": {
        "nav_meta": "Local SEO for roofers",
        "title": 'Local SEO for Roofers — Win "Roof Repair Near Me" &amp; High-Ticket Jobs | Cascade',
        "meta_desc": "Local SEO for roofing companies: rank in the Google map pack for 'roof repair near me' and storm-driven searches, build reviews, and win high-ticket jobs without buying shared leads. Free audit.",
        "og_title": "Local SEO for Roofers | Cascade Local SEO",
        "og_desc": "Win high-ticket roof jobs from search — without buying leads from Angi. Free, specific audit — no pitch.",
        "tw_desc": "Win high-ticket roof jobs from search, without renting shared leads. Free audit, no pitch.",
        "og_headline": "Local SEO for roofers.",
        "og_subline": "Win high-ticket roof jobs from search — without buying leads from Angi.",
        "h1": "Win roof jobs from search — without renting leads from Angi.",
        "lede": 'Marketplace roofing leads are expensive and shared with your competitors. Ranking in the Google map pack for "roof repair near me" and "roof replacement [city]" puts high-ticket jobs in front of you exclusively. I get roofers into the pack and keep them there. Free, specific audit — no pitch.',
        "cta_label": "Get your free roofing audit →",
        "why_heading": "Why roofing SEO is different",
        "why_intro": "The local-SEO fundamentals are universal, but what actually wins a roofing company high-ticket jobs is specific. The audit and the work both account for it:",
        "why_bullets": [
            ("High-ticket, exclusive leads.", "A roof job runs thousands to tens of thousands. A map-pack ranking sends those searches straight to you — not shared three ways like an Angi or HomeAdvisor lead."),
            ("Storm and seasonal surges.", '"Roof repair near me," "storm damage roof," and "roof leak" spike after weather. Ranking before the storm means you catch the surge instead of bidding for scraps.'),
            ("You're a service-area business.", "You rank by service area, not a storefront. Getting service areas and primary category right decides which towns you appear in."),
            ("Reviews and trust on a big purchase.", "Homeowners vet roofers hard. Review volume, recency, and job photos move both ranking and the call."),
        ],
        "sample": {
            "name": "Ridgeline Roofing &amp; Exteriors", "sub": "Residential roofing · service-area business",
            "stats": [("Google Rating", "4.7★", "warn"), ("Reviews", "45", "bad"), ('Rank for "roof repair"', "#6", "bad")],
            "losing_title": "Where you're losing jobs",
            "losing": [
                ("Review volume:", "45 reviews vs the top-3 average of 140+. On a big-ticket, high-trust purchase, review count drives both ranking and the call."),
                ("Local pack position:", "#6 — off the map pack for your primary service, where the highest-intent searches happen."),
                ("Service areas + jobs unmapped:", "neighboring towns aren't configured and posts don't target replacement, storm, or metal-roof jobs — your most valuable work."),
            ],
            "levers": [
                ("Review velocity system:", "a structured ask at job completion with photos, closing the gap to the top-3 count."),
                ("Service-area + category setup:", "correct primary category, service areas, and posts targeting replacement and storm-damage jobs."),
                ("Citation + NAP cleanup:", "consistent name/address/phone across home-service and roofing directories Google cross-checks."),
            ],
        },
        "how_keywords": "service keywords",
        "rank_keyword_phrase": "top service keywords",
        "longtail_phrase": "service long-tails",
        "human_review_note": "",
        "mailto_suffix": "roofing company", "mailto_biz": "company",
        "faq_heading": "Roofing SEO — FAQ",
        "faqs": [
            {"q": "We buy leads from Angi/HomeAdvisor — why bother with SEO?",
             "a": "Those leads are shared with competitors and cost you on every one. Map-pack leads are exclusive and don't cost per click. Owning search means you stop renting leads and keep the margin on every job."},
            {"q": "Demand spikes after storms — does SEO keep up?",
             "a": "Rankings compound, so you're already on top of the pack before the storm instead of bidding against everyone after it. We lean posts and keywords into storm and seasonal demand ahead of time."},
            {"q": "We don't have a storefront — can we still rank?",
             "a": "Yes. You're a service-area business, and Google ranks you by the areas you serve. Configuring service areas and your primary category correctly is exactly what most roofers miss — and the first thing the audit checks."},
            {"q": "How fast will I win high-ticket jobs?",
             "a": "Most map-pack improvements land in 30–90 days. The consideration cycle is longer than emergency trades, but visibility and reviews compound — and one won roof job pays for a lot of months."},
            {"q": "Do you only work with roofers?",
             "a": "No — the same playbook works for any local service business. But roofing is a vertical I work in often, so the audit understands high-ticket intent, storm seasonality, and the lead-marketplace landscape.",
             "more": ' <a href="/">See the main page →</a>'},
        ],
        "service_type": "Local SEO for roofing companies",
        "service_desc": "Local search marketing for roofers: Google map pack ranking for 'roof repair near me' and storm-driven searches, service-area configuration, review velocity programs, and citation cleanup.",
    },
}


def _bullets(items):
    return "\n".join(f"      <li><strong>{s}</strong> {t}</li>" for s, t in items)


def _sample_bullets(items):
    return "\n".join(f"          <li><strong>{s}</strong> {t}</li>" for s, t in items)


def _faq_details(faqs):
    out = []
    for f in faqs:
        more = f.get("more", "")
        out.append(
            f"    <details>\n      <summary>{f['q']}</summary>\n      <p>{f['a']}{more}</p>\n    </details>"
        )
    return "\n".join(out)


def _graph(slug, v):
    url = f"{BASE}/local-seo-for-{slug}"
    graph = [
        {
            "@type": "Service",
            "name": v["nav_meta"][0].upper() + v["nav_meta"][1:],
            "serviceType": v["service_type"],
            "description": v["service_desc"],
            "areaServed": {"@type": "Country", "name": "United States"},
            "provider": {
                "@type": "ProfessionalService",
                "name": "Cascade Local SEO",
                "url": f"{BASE}/",
                "email": "jonathan@cascadelocalseo.com",
                "priceRange": "$1,000–$3,000/mo",
            },
            "offers": {"@type": "Offer", "price": "1000", "priceCurrency": "USD", "description": "Plans from $1,000/mo, month-to-month."},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": v["nav_meta"], "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": _unescape(f["q"]),
                 "acceptedAnswer": {"@type": "Answer", "text": _unescape(f["a"])}}
                for f in v["faqs"]
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)


def _unescape(s):
    # schema text should be plain (no HTML entities)
    return html.unescape(s)


PRICING = """  <section id="pricing">
    <h2>Plans &amp; pricing</h2>
    <p>Flat monthly, month-to-month, no contracts. Same plans as everything else I do.</p>
    <div class="pricing">
      <div class="tier recommended">
        <h3>Starter</h3>
        <div class="price">$1,000<small>/mo</small></div>
        <ul>
          <li>Daily review monitoring + drafted responses</li>
          <li>2× weekly GBP posts (Tues + Thurs)</li>
          <li>Monthly progress report (1st of month)</li>
          <li>One-time citation cleanup across 30-40 directory sites in your first 30 days</li>
          <li>Rank tracking on your {rank_keyword_phrase} + alerts</li>
        </ul>
        <a class="cta" href="{starter}">Start Starter — $1,000/mo →</a>
      </div>
      <div class="tier">
        <h3>Standard</h3>
        <div class="price">$1,500<small>/mo</small></div>
        <ul>
          <li>Everything in Starter</li>
          <li>3× weekly GBP posts (Mon + Wed + Fri)</li>
          <li>Bi-weekly competitor scan with specific actions</li>
          <li>Quarterly keyword expansion (5 new {longtail_phrase} every 90 days)</li>
        </ul>
        <a class="cta cta-secondary" href="{standard}">Start Standard — $1,500/mo →</a>
      </div>
      <div class="tier">
        <h3>Full retainer</h3>
        <div class="price">$3,000<small>/mo</small></div>
        <ul>
          <li>Everything in Standard</li>
          <li>5× weekly GBP posts (every weekday)</li>
          <li>Weekly content briefs + 2 SEO blog posts/month (1,500-2,500 words)</li>
          <li>Bi-monthly reports (1st + 15th)</li>
          <li>Monthly 30-min strategy call</li>
        </ul>
        <a class="cta cta-secondary" href="mailto:jonathan@go.cascadelocalseo.com?subject=Full%20tier%20inquiry%20({mailto_suffix})&body=Hi%20Jonathan%2C%20I'm%20interested%20in%20the%20Full%20tier%20for%20my%20{mailto_biz}%3A%20%5Bbusiness%20name%5D.%20">Talk to Jonathan →</a>
      </div>
    </div>
    <p class="small muted">Month-to-month. Cancel anytime. No setup fees.</p>
  </section>"""


def render(slug, v):
    url = f"{BASE}/local-seo-for-{slug}"
    og_img = f"{BASE}/og-{slug}.png"
    pricing = PRICING.format(
        rank_keyword_phrase=v["rank_keyword_phrase"], longtail_phrase=v["longtail_phrase"],
        starter=STARTER_LINK, standard=STANDARD_LINK,
        mailto_suffix=v["mailto_suffix"].replace(" ", "%20"), mailto_biz=v["mailto_biz"].replace(" ", "%20"),
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{v['title']}</title>
  <meta name="description" content="{v['meta_desc']}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Cascade Local SEO">
  <meta property="og:title" content="{v['og_title']}">
  <meta property="og:description" content="{v['og_desc']}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{v['og_title']}">
  <meta name="twitter:description" content="{v['tw_desc']}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <meta name="theme-color" content="#0a3d24">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/cascade.css">
  <style>
    .crumb {{ font-size: 0.8rem; color: var(--ink-faint); margin-bottom: 12px; }}
    .crumb a {{ color: var(--ink-soft); border-bottom: none; }}
    .crumb a:hover {{ color: var(--green); }}
    .btn-row {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 24px; }}
    .btn {{ display: inline-block; background: var(--green); color: #fff; padding: 13px 22px; border-radius: 7px; font-weight: 600; border-bottom: none; letter-spacing: 0.2px; transition: background 0.15s; }}
    .btn:hover {{ background: var(--green-dark); color: #fff; }}
    .btn-ghost {{ background: transparent; color: var(--green-dark); border: 1px solid var(--border); }}
    .btn-ghost:hover {{ background: var(--green-tint); color: var(--green-dark); }}
    .lead-list li {{ margin: 8px 0; }}
  </style>

  <script type="application/ld+json">
{_graph(slug, v)}
  </script>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <a class="logo" href="/">Cascade Local SEO<span class="dot">.</span></a>
    <div class="meta">{v['nav_meta']}</div>
  </div>
</nav>

<div class="hero">
  <div class="wrap">
    <div class="crumb"><a href="/">Home</a> › {v['nav_meta']}</div>
    <div class="tag">{v['nav_meta']}</div>
    <h1>{v['h1']}</h1>
    <p class="lede">{v['lede']}</p>
    <div class="btn-row">
      <a class="btn" href="/audit">{v['cta_label']}</a>
      <a class="btn btn-ghost" href="#pricing">See plans &amp; pricing</a>
    </div>
  </div>
</div>

<main class="wrap">

  <section>
    <h2>{v['why_heading']}</h2>
    <p>{v['why_intro']}</p>
    <ul class="lead-list">
{_bullets(v['why_bullets'])}
    </ul>
  </section>

  <section>
    <h2>What your audit looks like</h2>
    <p>Roughly a one-page report built on your real numbers and your three closest local competitors. Below is the format — yours will be specific to your numbers and the businesses competing with you for top-3 visibility.</p>

    <article class="sample-preview">
      <header class="sample-header">
        <div class="sample-eyebrow">Sample audit · format preview</div>
        <h3 class="sample-title">{v['sample']['name']}</h3>
        <p class="sample-sub">{v['sample']['sub']} · <em>(example business — not a real prospect)</em></p>
      </header>

      <div class="sample-stats">
{chr(10).join(f'        <div class="sample-stat {tone}"><div class="label">{label}</div><div class="value">{val}</div></div>' for label, val, tone in v['sample']['stats'])}
      </div>

      <div class="sample-body">
        <h4>{v['sample']['losing_title']}</h4>
        <ul>
{_sample_bullets(v['sample']['losing'])}
        </ul>

        <h4>Three levers that would move the needle</h4>
        <div class="sample-fade">
          <ul>
{_sample_bullets(v['sample']['levers'])}
          </ul>
        </div>
      </div>

      <div class="sample-cta">
        <div class="sample-cta-text">Get yours — uses your real numbers + local competitors</div>
        <a class="sample-cta-link" href="/audit">Take the full self-audit →</a>
      </div>
    </article>
  </section>

  <section>
    <h2>How this works</h2>
    <p>The recurring work agencies bill $2,500–$5,000/mo for — review monitoring, weekly posts, rank tracking, citation cleanup, reporting — is mostly repetitive. Software does repetitive well; strategy still needs a human. Here's the split.</p>
    <div class="how-grid">
      <div class="how-step">
        <div class="how-num">1</div>
        <span class="how-tag">Week 1</span>
        <h3>Audit + setup</h3>
        <p>You take the 5-minute self-audit. I review it personally and reply within 24 hours. If we work together, week one maps your {v['how_keywords']}, baselines your reviews and citations, and sets your brand voice.</p>
      </div>
      <div class="how-step">
        <div class="how-num">2</div>
        <span class="how-tag">Daily, ongoing</span>
        <h3>Automated delivery</h3>
        <p>Review monitoring with drafted responses, GBP posts in your voice, rank tracking, competitor scans, citation building — all on schedule. Your tier sets the cadence.</p>
      </div>
      <div class="how-step">
        <div class="how-num">3</div>
        <span class="how-tag">Before publish + monthly</span>
        <h3>Human review + reporting</h3>
        <p>Nothing publishes without my review first{v['human_review_note']}. On the 1st you get a real report: rank changes, review delta, what moved, what's next.</p>
      </div>
    </div>
    <div class="how-footer">
      <strong>Same playbook as the bigger agencies — a fraction of the cost.</strong> Automation does the labor, I hold the quality bar, and you don't pay an account-manager markup.
    </div>
  </section>

{pricing}

  <section class="faq">
    <h2>{v['faq_heading']}</h2>
{_faq_details(v['faqs'])}
  </section>

  <section>
    <h2>Start with the audit</h2>
    <p>No call, no contract, no pitch. Tell me about your business and I'll send back exactly where you rank, your three biggest gaps, and a 60-day plan — usually within 24 hours.</p>
    <div class="btn-row">
      <a class="btn" href="/audit">{v['cta_label']}</a>
      <a class="btn btn-ghost" href="/">Back to home</a>
    </div>
  </section>

</main>

<footer>
  <div class="wrap">
    <div><strong>Cascade Local SEO</strong> · built by Jonathan</div>
    <div><a href="mailto:jonathan@cascadelocalseo.com">jonathan@cascadelocalseo.com</a></div>
  </div>
</footer>

</body>
</html>
"""


def main():
    for slug, v in VERTICALS.items():
        path = os.path.join(OUT_DIR, f"local-seo-for-{slug}.html")
        with open(path, "w") as f:
            f.write(render(slug, v))
        # validate the JSON-LD we just emitted
        json.loads(_graph(slug, v))
        print("wrote", os.path.basename(path))


if __name__ == "__main__":
    main()
