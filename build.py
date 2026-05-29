#!/usr/bin/env python3
"""SEA brand channel spark brainstorm board.
Plain HTML (no gate), mobile-first, single page.
"""
import os, json
from html import escape

# -------- DATA --------

CONTEXT = {
    "title": "Sourcing electronics from China: angle iteration",
    "description": "Live brainstorm for short-form video angles on sourcing electronics from China. Core idea: electronics are cheap at the source, smart operators import and keep the margin, and WorldFirst is how you pay the supplier fast, cheap and safe. Each round narrows the list. Tick formats to bank for production, comment to keep iterating, leave untouched to archive.",
}
VERSION = "v2"

# Angles locked into the bank, seeded server-side so the narrowed state is canonical across
# devices (localStorage still carries per-device picks; this is the default fallback).
# Format keys: reel / longform / image / carousel / kol.
SEED_BANK = {
    "P1-A1": ["reel"],
    "P1-A2": ["reel"],
    "P1-A3": ["reel"],
}

PILLARS = {
    "p1": {
        "id": "p1",
        "name": "P1 — The opportunity",
        "funnel": "TOFU · hook + desire",
        "job": "Make the viewer feel the margin gap is real and bigger than they think. The arbitrage, the proof, the maths.",
    },
    "p2": {
        "id": "p2",
        "name": "P2 — How to source",
        "funnel": "TOFU/MOFU · how-to + save-bait",
        "job": "Show the real sourcing playbook: finding the factory, 1688, samples, MOQ, the Shenzhen markets.",
    },
    "p3": {
        "id": "p3",
        "name": "P3 — Paying the supplier",
        "funnel": "MOFU/BOFU · product wedge",
        "job": "The hard part nobody films: paying a Chinese supplier fast, cheap and safe. Where WorldFirst lands.",
    },
    "p4": {
        "id": "p4",
        "name": "P4 — Don't get burned",
        "funnel": "TOFU/MOFU · trust",
        "job": "De-risk the fear that stops first-timers: scams, quality, verification, the bad batch.",
    },
}

ANGLES = [
    # ---------- P1 — The opportunity ----------
    {
        "id": "P1-A1",
        "pillar": "p1",
        "framework": "Reframe (MAG)",
        "title": "That $80 gadget costs $11 in Shenzhen",
        "hooks": [
            "The $80 gadget you bought online costs about $11 to source in Shenzhen. Someone in the middle kept $69. That someone could be you.",
            "Most 'innovative' electronics brands aren't making anything. They buy it in Shenzhen, put a logo on it, and keep the gap.",
            "Open a best-seller on Amazon. Search the same product on 1688. The price difference is the entire business.",
        ],
        "mechanism": "Reframes building an electronics brand as arbitrage you can see with two browser tabs. The price gap is the hook and the business model at once.",
        "formats": ["SF 45s reveal", "SF 60s two-tab walkthrough"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": True,
        "why": "This is the exact idea Steven handed over. Strongest single TOFU hook, the whole campaign hangs off it.",
    },
    {
        "id": "P1-A2",
        "pillar": "p1",
        "framework": "Demo-before-tell",
        "title": "Same earbuds, two prices, split screen",
        "hooks": [
            "Left: $129 on a brand's website. Right: $9.50 on the factory listing. Same product, same box. Watch.",
            "I'm putting the retail page and the factory page side by side. The logo is the only difference. It costs you $119.",
            "This is the same pair of earbuds at two prices. One has a brand. Watch what the brand actually adds.",
        ],
        "mechanism": "Visual split-screen proof. Show, don't claim. The identical product at two prices is undeniable and native to the short-form scroll.",
        "formats": ["SF 30s split-screen", "SF 45s reveal cut"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": True,
        "why": "Split-screen is the most scroll-stopping SF format. Pure visual, no talent dependency, infinitely repeatable per product.",
    },
    {
        "id": "P1-A3",
        "pillar": "p1",
        "framework": "Math-led",
        "title": "The real margin on a $25 power bank",
        "hooks": [
            "Source a power bank for $4, sell it for $25. Everyone sees the $21. Almost nobody budgets the 7 costs that eat half of it.",
            "The real margin on imported electronics isn't sale price minus unit cost. Here's the full landed-cost maths.",
            "$4 in, $25 out. Here's exactly where every dollar of that gap actually goes before it's yours.",
        ],
        "mechanism": "Honest margin breakdown. Credibility comes from not overselling: names shipping, duty, QC, returns and payment fees. The payment-fee line sets up WorldFirst naturally.",
        "formats": ["SF 60s number reveal", "SF 45s calculator cut"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": True,
        "why": "Carries the 'take the profit' half of the brief honestly. Math-led builds trust and tees up the payments pillar.",
    },
    {
        "id": "P1-A4",
        "pillar": "p1",
        "framework": "Curiosity gap",
        "title": "The category beginners pick that's already dead",
        "hooks": [
            "Most first-time electronics importers pick a category that's already saturated. Here are the 3 filters that spot a live one.",
            "The electronics niche everyone starts with is the one most likely to bankrupt them. The reason why.",
            "Saturation, certification, returns: the 3 filters that kill most electronics categories before you order a single unit.",
        ],
        "mechanism": "Curiosity plus a filtering framework. Saves the beginner from the obvious mistake and establishes authority early.",
        "formats": ["SF 60s listicle cut", "SF 45s reveal"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P1-A5",
        "pillar": "p1",
        "framework": "Counter-case (MAG)",
        "title": "Cheapest products have the worst margins",
        "hooks": [
            "The cheapest products to source often make the worst businesses. The counterintuitive reason.",
            "Why a $40 mini projector is a better business than a $2 phone case. The margin maths nobody runs.",
            "Low unit cost feels safe. It's usually a trap. Here's what actually drives electronics margin.",
        ],
        "mechanism": "Counter-intuitive reframe. Shifts thinking from unit cost to margin percentage and defensibility. Cheap is not the same as profitable.",
        "formats": ["SF 45s reframe cut", "SF 60s explainer"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },

    # ---------- P2 — How to source ----------
    {
        "id": "P2-A1",
        "pillar": "p2",
        "framework": "Tutorial",
        "title": "Find the actual factory, not a reseller",
        "hooks": [
            "The supplier you found on Alibaba is probably a reseller. Here are the 3 signs you're talking to the real factory.",
            "Trading company or factory? If you can't tell, you're paying 10 to 15% more. The checklist.",
            "How to tell if your 'manufacturer' actually manufactures anything. 3 questions they can't fake.",
        ],
        "mechanism": "Tutorial plus an insider checklist. Trading-company-versus-factory is the number one beginner blind spot. High save rate.",
        "formats": ["SF 60s checklist", "SF 45s tutorial cut"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": True,
        "why": "Highest-save how-to in the set. Evergreen, search-intent, and a credibility builder for the channel.",
    },
    {
        "id": "P2-A2",
        "pillar": "p2",
        "framework": "Listicle",
        "title": "5 things to ask before you pay a deposit",
        "hooks": [
            "Before you send any electronics supplier a deposit, ask these 5 things. Skip one and you're gambling.",
            "5 questions that separate a real supplier from a scam. Ask all 5 before any money moves.",
            "The 5-question script I send every new electronics supplier before the first payment.",
        ],
        "mechanism": "Listicle, save-bait, fast. Protective and actionable, bridges naturally into the payments and trust pillars.",
        "formats": ["SF 60s listicle", "SF 45s script read"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P2-A3",
        "pillar": "p2",
        "framework": "Demo-before-tell",
        "title": "Sourcing a product live on 1688",
        "hooks": [
            "Watch me find a sellable electronics product on 1688 in 4 minutes. Screen recorded, no cuts.",
            "I don't read Mandarin and I'm about to source a product on a Chinese-only site. Here's how.",
            "1688 is where the factories actually sell. Here's how to use it without reading a word of Chinese.",
        ],
        "mechanism": "Live screen-share demo. 1688 feels inaccessible to Western importers, so showing it demystifies and the novelty holds attention.",
        "formats": ["SF 60s screen-record", "SF 45s demo cut"],
        "bilingual": True,
        "talent_fit": "strong",
        "shortlist": True,
        "why": "1688 access is a genuine knowledge gap. Screen-record demo is strong SF and bilingual unlocks Mandarin search too.",
    },
    {
        "id": "P2-A4",
        "pillar": "p2",
        "framework": "Pain-first",
        "title": "The sample was perfect, the bulk order wasn't",
        "hooks": [
            "Your sample was flawless. Your 1,000-unit order arrived 40% defective. This is the oldest trick in sourcing.",
            "Why the sample is always perfect and the bulk run sometimes isn't. And how to stop it.",
            "The golden sample trap: how a supplier passes your test then changes the spec. The defence.",
        ],
        "mechanism": "Names a real, painful failure mode (the golden sample). Pain-first opening that sets up quality control and balance-payment leverage.",
        "formats": ["SF 60s pain hook", "SF 45s explainer"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P2-A5",
        "pillar": "p2",
        "framework": "Decision-tree",
        "title": "MOQ too high? Here are your 3 moves",
        "hooks": [
            "The factory says minimum order is 5,000 units. You want 500. Here are your 3 real options.",
            "A high minimum order doesn't always mean walk away. The decision tree for negotiating it down.",
            "5,000 MOQ, $20K outlay, you're not ready. 3 ways importers handle this without overcommitting.",
        ],
        "mechanism": "Decision tree gives the viewer agency on the most common dealbreaker. Practical and self-qualifying.",
        "formats": ["SF 60s decision cut", "SF 45s reveal"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P2-A6",
        "pillar": "p2",
        "framework": "Curiosity gap",
        "title": "The Shenzhen market that has everything",
        "hooks": [
            "There's one market in Shenzhen where you can source almost any electronic component on earth. Most importers never go.",
            "Huaqiangbei: ten city blocks of electronics that feed half the world's gadgets. A walk-through.",
            "Why serious electronics importers fly to one square mile in Shenzhen before they order anything.",
        ],
        "mechanism": "Curiosity plus place-based intrigue. Huaqiangbei is aspirational, gives a behind-the-scenes feel, and shoots beautifully as b-roll.",
        "formats": ["SF 60s walk-through", "SF 45s reveal"],
        "bilingual": True,
        "talent_fit": "stretch",
        "shortlist": False,
        "why": None,
    },

    # ---------- P3 — Paying the supplier ----------
    {
        "id": "P3-A1",
        "pillar": "p3",
        "framework": "Pain-first",
        "title": "Supplier wants 30% deposit by wire. Now what?",
        "hooks": [
            "Your new supplier wants a 30% deposit, by bank wire, to an account in a different company's name. Is this normal?",
            "First electronics order: they want $6,000 upfront before making anything. How to send it without losing it.",
            "The deposit moment is where most first-time importers freeze. Here's how the experienced ones handle it.",
        ],
        "mechanism": "Pain-first at the exact anxiety moment. The 'different company name' detail is real and frightening, and positions WorldFirst as the safe rail.",
        "formats": ["SF 60s pain hook", "SF 45s explainer"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": True,
        "why": "The precise moment WorldFirst's product matters most. Universal first-order anxiety, direct product wedge.",
    },
    {
        "id": "P3-A2",
        "pillar": "p3",
        "framework": "Hidden cost (MAG)",
        "title": "Your $10K wire arrived as $9,760",
        "hooks": [
            "You wired your supplier $10,000. They received $9,760. The $240 wasn't a fee. It was the FX margin nobody showed you.",
            "Why your supplier keeps saying the payment came up short. The hidden cost in every bank wire to China.",
            "The $240 your bank quietly takes on a $10K China payment, and how to stop paying it.",
        ],
        "mechanism": "Hidden cost reveal. FX margin on supplier payments stays invisible until the supplier flags the shortfall. The cleanest WorldFirst wedge.",
        "formats": ["SF 45s number reveal", "SF 60s pain cut"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": True,
        "why": "WorldFirst's core value made concrete on a real electronics payment. The shortfall moment is visceral.",
    },
    {
        "id": "P3-A3",
        "pillar": "p3",
        "framework": "Math-led",
        "title": "FX margin eats 9% of your profit",
        "hooks": [
            "Your electronics margin is 22%. Your bank takes 2% on every supplier payment. That's 9% of your profit, gone to FX.",
            "The cost that scales with your success: the more you import, the more your bank's FX margin quietly eats.",
            "On $200K of supplier payments a year, a 2% FX margin is $4,000. That's your next product launch.",
        ],
        "mechanism": "Math reframe linking FX margin to product margin percentage. The 'scales with your success' framing stings the operators who are actually growing.",
        "formats": ["SF 60s calculator cut", "SF 45s number reveal"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P3-A4",
        "pillar": "p3",
        "framework": "Comparison",
        "title": "Bank wire vs WorldFirst to a Shenzhen factory",
        "hooks": [
            "Same $20K to the same Shenzhen factory: bank wire vs WorldFirst. Speed, cost, and what the supplier actually receives.",
            "I paid the same supplier two ways. One arrived next day in full. One took 4 days and came up short.",
            "Bank wire takes 3 to 5 days and a hidden cut. Here's the side by side on a real electronics order.",
        ],
        "mechanism": "Head-to-head comparison on a real electronics payment. Concrete, removes ambiguity, WorldFirst wins on speed, cost and amount received.",
        "formats": ["SF 60s comparison", "SF 45s numbers cut"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P3-A5",
        "pillar": "p3",
        "framework": "Demo-before-tell",
        "title": "Paying a 1688 supplier in CNY in 60 seconds",
        "hooks": [
            "Paying a Chinese electronics supplier in their own currency, same day. Watch the whole thing, uncut.",
            "Your supplier quoted in CNY. Most importers pay in USD and lose twice. Here's paying in CNY directly.",
            "60 seconds: a deposit to a Shenzhen factory, in CNY, no SWIFT delay. Real payment.",
        ],
        "mechanism": "Product demo. Paying in CNY directly versus the USD double-conversion, shown live. Proof of capability rather than a claim.",
        "formats": ["SF 60s demo", "SF 45s screen-record"],
        "bilingual": True,
        "talent_fit": "stretch",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P3-A6",
        "pillar": "p3",
        "framework": "Reframe (MAG)",
        "title": "Pay in CNY, get a better unit price",
        "hooks": [
            "Offer to pay your Shenzhen supplier in CNY and watch your unit price drop. Here's why it works.",
            "USD feels safer to you. CNY is cheaper for them. Pay in CNY and some of that saving comes back to you.",
            "The negotiation lever nobody uses: paying in the supplier's own currency. The mechanism.",
        ],
        "mechanism": "Reframes paying in CNY as a negotiation advantage, not a risk. The supplier avoids their own conversion cost and can quote lower. WorldFirst enables it.",
        "formats": ["SF 45s reframe cut", "SF 60s explainer"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },

    # ---------- P4 — Don't get burned ----------
    {
        "id": "P4-A1",
        "pillar": "p4",
        "framework": "Pain-first",
        "title": "The supplier vanished after the deposit",
        "hooks": [
            "You sent a 30% deposit. The supplier stopped replying. This happens more than anyone admits. How to avoid it.",
            "The disappearing-supplier scam: how it works, and the 4 checks that would have caught it.",
            "$6,000 deposit, dead WeChat, no goods. The post-mortem on a scam that's completely preventable.",
        ],
        "mechanism": "Pain-first on the worst-case fear, then the prevention checklist. The single biggest psychological blocker for first-time importers.",
        "formats": ["SF 60s pain hook", "SF 45s checklist"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": True,
        "why": "The number one fear that stops people sourcing at all. High engagement, and it earns the trust to sell the payment product.",
    },
    {
        "id": "P4-A2",
        "pillar": "p4",
        "framework": "Tutorial",
        "title": "Verify a supplier before you pay",
        "hooks": [
            "Before you pay any electronics supplier, run these 4 verification checks. Takes 20 minutes, saves thousands.",
            "Business licence, factory audit, trade history, payment trail: how to verify a Chinese supplier is real.",
            "The 20-minute supplier background check that separates real factories from scams.",
        ],
        "mechanism": "Tutorial and verification checklist. Actionable, save-bait, authority-building. Pairs directly with the vanished-supplier pain angle.",
        "formats": ["SF 60s checklist", "SF 45s tutorial cut"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P4-A3",
        "pillar": "p4",
        "framework": "Counter-case (MAG)",
        "title": "The cheapest quote is the riskiest",
        "hooks": [
            "The supplier with the lowest quote is the one most likely to burn you. The counterintuitive reason.",
            "Why the cheapest electronics quote should make you nervous, not excited.",
            "Race-to-the-bottom pricing hides 3 risks. Here's what the lowest quote is really telling you.",
        ],
        "mechanism": "Counter-case. Reframes price-shopping as risk-taking. Cheapest is not best, and the framing protects the viewer from their own instinct.",
        "formats": ["SF 45s reframe cut", "SF 60s explainer"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P4-A4",
        "pillar": "p4",
        "framework": "Listicle",
        "title": "4 red flags in a supplier's first message",
        "hooks": [
            "4 red flags hiding in your supplier's very first reply. Spot them before you send a cent.",
            "The way a supplier writes their first message tells you if they're real. 4 tells.",
            "Personal email, no business licence, pressure to pay fast: the first-message red flags.",
        ],
        "mechanism": "Listicle, fast, save-able. Pattern recognition for scam avoidance at the earliest possible contact point.",
        "formats": ["SF 45s listicle", "SF 60s reveal"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
    {
        "id": "P4-A5",
        "pillar": "p4",
        "framework": "Case study narration",
        "title": "How one importer recovered from a bad batch",
        "hooks": [
            "1,000 defective units, $12K on the line. How one importer turned a bad batch into a refund and a better supplier.",
            "The bad-batch playbook: what to do the day your quality inspection fails.",
            "A real recovery: failed inspection, held the balance payment, full renegotiation. Step by step.",
        ],
        "mechanism": "Case study narration. Shows that holding the 70% balance is real leverage. Evidence-led trust content that turns fear into a plan.",
        "formats": ["SF 60s story cut", "SF 45s playbook"],
        "bilingual": False,
        "talent_fit": "strong",
        "shortlist": False,
        "why": None,
    },
]

FRAMEWORKS_LIB = [
    {"id": "pain_first", "name": "Pain-first", "rule": "Open with the user's specific failure moment, then reverse-engineer."},
    {"id": "curiosity_gap", "name": "Curiosity gap", "rule": "Reveal information asymmetry the audience didn't know they had."},
    {"id": "demo_first", "name": "Demo-before-tell", "rule": "Show the action first, hold attention through novelty, then layer the explanation."},
    {"id": "mag_hidden", "name": "Hidden cost (MAG)", "rule": "Surface the invisible cost component the category hides."},
    {"id": "listicle", "name": "Listicle", "rule": "Enumerated structure. Save-bait. Carousel-native."},
    {"id": "mag_counter", "name": "Counter-case (MAG)", "rule": "Show when the category convention is wrong. Trust signal."},
    {"id": "math", "name": "Math-led", "rule": "Concrete numbers over abstract claims. Compounding feels large."},
    {"id": "comparison", "name": "Comparison", "rule": "Direct head-to-head on a specific real-world transaction."},
    {"id": "decision_tree", "name": "Decision-tree", "rule": "Viewer self-qualifies through structured questions."},
    {"id": "tutorial", "name": "Tutorial", "rule": "Step-by-step. High SEO value. Save-bait."},
    {"id": "case_study", "name": "Case study narration", "rule": "Third-person VO over real data. Evidence-led trust signal."},
    {"id": "story_narration", "name": "Story-led narration", "rule": "Documentary-style. Audience self-recognises in the subject."},
    {"id": "bts", "name": "Behind-the-scenes", "rule": "Reveal the human and operational layer behind the product."},
    {"id": "authority_scale", "name": "Authority / scale", "rule": "Data + visual proof of footprint."},
    {"id": "mag_reframe", "name": "Reframe (MAG)", "rule": "Recategorise the category. Manifesto register."},
]

# -------- HTML RENDERING --------

def render_pillar_section(pillar_key, pillar, angles_in_pillar):
    angle_cards = "\n".join(render_angle_card(a) for a in angles_in_pillar)
    return f"""
<section class="pillar" data-pillar="{pillar_key}">
  <header class="pillar-head">
    <div class="pillar-name">{escape(pillar['name'])}</div>
    <div class="pillar-meta">{escape(pillar['funnel'])}</div>
    <div class="pillar-job">{escape(pillar['job'])}</div>
  </header>
  <div class="angle-grid">
    {angle_cards}
  </div>
</section>
"""

def render_angle_card(a):
    hooks_html = "\n".join(
        f'<li class="hook"><span class="hook-num">{i+1}</span><span class="hook-text">{escape(h)}</span></li>'
        for i, h in enumerate(a["hooks"])
    )
    formats = " · ".join(escape(f) for f in a["formats"])
    bilingual_tag = '<span class="tag tag-bilingual">EN + ZH</span>' if a["bilingual"] else ""
    fit_class = "fit-strong" if a["talent_fit"] == "strong" else "fit-stretch"
    fit_label = "Strong fit" if a["talent_fit"] == "strong" else "Stretch"
    shortlist_badge = '<span class="badge-shortlist">First batch</span>' if a["shortlist"] else ""
    why_block = f'<div class="why"><span class="why-label">Why shortlisted:</span> {escape(a["why"])}</div>' if a.get("why") else ""
    v2_note_block = f'<div class="v2-note"><span class="v2-note-label">v2 update:</span> {escape(a["v2_note"])}</div>' if a.get("v2_note") else ""
    derived_badge = f'<span class="badge-derived">Sparked from {escape(a["derived_from"])}</span>' if a.get("derived_from") else ""
    prev_note_block = f'<div class="prev-note"><span class="prev-note-label">Your v3 note (kept for context)</span><span class="prev-note-text">{escape(a["previous_note"])}</span></div>' if a.get("previous_note") else ""
    has_context = "1" if a.get("previous_note") else "0"
    aid = a["id"]
    seed_fmts = SEED_BANK.get(aid, [])
    def _ck(fmt):
        return " checked" if fmt in seed_fmts else ""
    selectors_html = f"""
  <div class="selectors">
    <div class="selectors-label">Use this angle as</div>
    <div class="selector-group">
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="{aid}" data-fmt="reel"{_ck('reel')}><span>Short-form reel</span></label>
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="{aid}" data-fmt="longform"{_ck('longform')}><span>Long-form video</span></label>
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="{aid}" data-fmt="image"{_ck('image')}><span>Single image</span></label>
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="{aid}" data-fmt="carousel"{_ck('carousel')}><span>Carousel</span></label>
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="{aid}" data-fmt="kol"{_ck('kol')}><span>KOL angle</span></label>
    </div>
    <label class="selector selector-action"><input type="checkbox" class="sel-cb" data-id="{aid}" data-fmt="findmore"><span>Find more angles like this</span></label>
  </div>
  <div class="card-comment">
    <label class="card-comment-label" for="comment-{aid}">Your note on this angle (optional)</label>
    <textarea class="card-comment-input" id="comment-{aid}" data-id="{aid}" placeholder="e.g. lean harder into the pain moment, drop this one, change the second hook..."></textarea>
  </div>
"""
    v2new = "1" if (a.get("derived_from") or a.get("v2_note")) else "0"
    return f"""
<article class="angle" id="{a['id']}" data-pillar="{a['pillar']}" data-fit="{a['talent_fit']}" data-bilingual="{'1' if a['bilingual'] else '0'}" data-shortlist="{'1' if a['shortlist'] else '0'}" data-v2new="{v2new}" data-has-prev="{has_context}">
  <header class="angle-head">
    <div class="angle-id-row">
      <span class="angle-id">{escape(a['id'])}</span>
      <span class="angle-framework">{escape(a['framework'])}</span>
      {shortlist_badge}
      {derived_badge}
    </div>
    <h3 class="angle-title">{escape(a['title'])}</h3>
  </header>
  <div class="meta-row">
    <span class="tag tag-format">{formats}</span>
    {bilingual_tag}
    <span class="tag {fit_class}">{fit_label}</span>
  </div>
  <div class="angle-body">
    {v2_note_block}
    {prev_note_block}
    <div class="hooks">
      <div class="hooks-label">3 hook variants</div>
      <ul class="hook-list">{hooks_html}</ul>
    </div>
    <div class="mechanism"><span class="mech-label">Mechanism:</span> {escape(a['mechanism'])}</div>
    {why_block}
  </div>
  {selectors_html}
  <button class="card-expand-toggle" onclick="toggleCardDetails(this)">Show details ▾</button>
</article>
"""

def render_filters():
    return """
<aside class="filters">
  <div class="filter-row">
    <button class="chip chip-active" data-filter="all">All angles</button>
    <button class="chip" data-filter="shortlist">First batch (8)</button>
    <button class="chip" data-filter="bilingual">Bilingual</button>
    <button class="chip" data-filter="strong">Strong fit</button>
    <button class="chip" data-filter="v2new">v2 new</button>
    <button class="chip" data-filter="custom">My cards</button>
  </div>
  <div class="filter-row">
    <button class="chip chip-pillar chip-active" data-pillar-filter="all">All pillars</button>
    <button class="chip chip-pillar" data-pillar-filter="p1">P1 Opportunity</button>
    <button class="chip chip-pillar" data-pillar-filter="p2">P2 Sourcing</button>
    <button class="chip chip-pillar" data-pillar-filter="p3">P3 Payments</button>
    <button class="chip chip-pillar" data-pillar-filter="p4">P4 Trust</button>
  </div>
</aside>
"""

def render_add_card_modal():
    return """
<button class="fab-add" onclick="openAddCardModal()" id="fab-add" title="Add your own angle">+ Add angle</button>
<div class="modal-overlay" id="add-card-overlay" hidden onclick="closeAddCardModalOverlay(event)">
  <div class="modal-card" onclick="event.stopPropagation()">
    <div class="modal-head">
      <h3>Add your own angle</h3>
      <button class="modal-close" onclick="closeAddCardModal()" title="Close">×</button>
    </div>
    <div class="form-row">
      <label class="form-label">Title (required)</label>
      <input type="text" id="custom-title" placeholder="Your angle title">
    </div>
    <div class="form-row">
      <label class="form-label">Pillar</label>
      <select id="custom-pillar">
        <option value="p1">P1 — The opportunity</option>
        <option value="p2">P2 — How to source</option>
        <option value="p3">P3 — Paying the supplier</option>
        <option value="p4">P4 — Don't get burned</option>
      </select>
    </div>
    <div class="form-row">
      <label class="form-label">Hook (optional)</label>
      <textarea id="custom-hook" placeholder="Your opening line"></textarea>
    </div>
    <div class="form-row">
      <label class="form-label">Note (optional)</label>
      <textarea id="custom-note" placeholder="Why this angle, what direction it's going"></textarea>
    </div>
    <div class="form-actions">
      <button class="form-btn form-btn-primary" onclick="saveCustomAngle()">Save card</button>
      <button class="form-btn" onclick="closeAddCardModal()">Cancel</button>
    </div>
  </div>
</div>
"""

def render_frameworks_section():
    cards = "\n".join(
        f'<div class="fw-card"><div class="fw-name">{escape(f["name"])}</div><div class="fw-rule">{escape(f["rule"])}</div></div>'
        for f in FRAMEWORKS_LIB
    )
    return f"""
<section class="frameworks-section">
  <header><h2>Angle framework library</h2><p>The 15 frameworks behind the 22 angles. Each pulls a different attention lever.</p></header>
  <div class="fw-grid">
    {cards}
  </div>
</section>
"""

def render_selection_panel():
    return """
<div id="selection-panel" class="selection-panel collapsed">
  <div class="selection-panel-bar" onclick="togglePanel()">
    <span class="panel-summary"><span class="count count-zero" id="panel-count">0 selections</span></span>
    <span class="panel-toggle" id="panel-toggle">tap to expand</span>
  </div>
  <div class="panel-expanded">
    <label class="panel-label">Generated prompt (auto-updates with selections + per-card notes)</label>
    <textarea class="panel-prompt" id="panel-prompt" readonly></textarea>
    <div class="panel-actions">
      <button class="panel-btn btn-copy" onclick="copyPrompt()" id="btn-copy">Copy prompt</button>
    </div>
  </div>
</div>
"""

def render_angle_meta_json():
    meta = {a["id"]: a["title"] for a in ANGLES}
    return json.dumps(meta)

def render_inner_html():
    pillar_sections = "\n".join(
        render_pillar_section(pk, p, [a for a in ANGLES if a["pillar"] == pk])
        for pk, p in PILLARS.items()
    )
    return f"""
<header class="page-head">
  <h1>{escape(CONTEXT['title'])} <span class="version-badge">{VERSION}</span></h1>
  <p class="page-desc">{escape(CONTEXT['description'])}</p>
</header>

{render_filters()}

<section class="bank-section" id="bank-section" hidden>
  <header class="section-head">
    <h2><span class="section-tag tag-bank">BANKED</span> Locked in <span class="section-count" id="bank-count">0</span></h2>
    <p>Selected format, no further notes. Untick or add a note to move back to iterating.</p>
  </header>
  <div class="bank-grid" id="bank-grid"></div>
</section>

<section class="active-section" id="active-section">
  <header class="section-head section-head-active">
    <h2><span class="section-tag tag-active">ITERATING</span> Still shaping <span class="section-count" id="active-count">0</span></h2>
    <p>The focus area. Read the hooks, tick formats, write notes, flag "find more" for any direction worth pulling on.</p>
  </header>
  <main class="board" id="active-board">
    {pillar_sections}
  </main>
</section>

<section class="archive-section" id="archive-section" hidden>
  <details class="archive-details">
    <summary class="archive-summary"><span class="section-tag tag-archive">ARCHIVED</span> Set aside <span class="section-count" id="archive-count">0</span></summary>
    <p class="archive-help">No engagement. Click any tick or note to bring back to active.</p>
    <div class="archive-grid" id="archive-grid"></div>
  </details>
</section>

{render_frameworks_section()}

{render_add_card_modal()}

<footer class="page-foot">
  <p>Electronics sourcing spark · WorldFirst · CY26 · {VERSION}</p>
</footer>

<script type="application/json" id="angle-meta">{render_angle_meta_json()}</script>
<script type="application/json" id="version-tag">"{VERSION}"</script>
{render_selection_panel()}
"""

CSS = r"""
* { box-sizing: border-box; -webkit-text-size-adjust: 100%; }
html, body { margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Helvetica, Arial, sans-serif; background: #fafafa; color: #111; line-height: 1.5; font-size: 16px; }
a { color: #111; }

/* PAGE */
.content-wrap { max-width: 1200px; margin: 0 auto; padding: 20px 18px 110px; }
.page-head { padding: 0 0 12px; border-bottom: 1px solid rgba(0,0,0,0.06); margin-bottom: 18px; }
.page-head h1 { font-size: 20px; font-weight: 700; margin: 0; letter-spacing: -0.01em; }

/* VERSION BADGE */
.version-badge { display: inline-block; font-size: 11px; padding: 3px 8px; border: 1px solid rgba(0,0,0,0.15); border-radius: 100px; color: #555; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; margin-left: 6px; vertical-align: middle; font-weight: 500; }

/* FILTERS */
.filters { position: sticky; top: 0; z-index: 50; background: #fafafa; padding: 12px 0; margin: 0 -18px 20px; padding-left: 18px; padding-right: 18px; border-bottom: 1px solid rgba(0,0,0,0.06); }
.filter-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
.filter-row:last-child { margin-bottom: 0; }
.chip { font-size: 13px; padding: 7px 12px; border: 1px solid rgba(0,0,0,0.12); border-radius: 100px; background: #fff; cursor: pointer; color: #333; touch-action: manipulation; min-height: 36px; font-family: inherit; }
.chip:hover { border-color: rgba(0,0,0,0.3); }
.chip-active { background: #111; color: #fff; border-color: #111; }

/* PILLARS */
.pillar { margin-bottom: 36px; }
.pillar-head { padding-bottom: 12px; border-bottom: 1px solid rgba(0,0,0,0.06); margin-bottom: 16px; }
.pillar-name { font-size: 18px; font-weight: 600; margin-bottom: 4px; letter-spacing: -0.01em; }
.pillar-meta { font-size: 12px; color: #999; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; text-transform: lowercase; margin-bottom: 6px; }
.pillar-job { font-size: 14px; color: #555; max-width: 620px; }

/* ANGLE CARDS */
.angle-grid { display: grid; grid-template-columns: 1fr; gap: 14px; }
.angle { background: #fff; border: 1px solid rgba(0,0,0,0.08); border-radius: 12px; padding: 18px 16px; transition: border-color 0.15s; }
.angle:hover { border-color: rgba(0,0,0,0.18); }
.angle.hidden { display: none; }
.angle-head { margin-bottom: 14px; }
.angle-id-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 6px; }
.angle-id { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; color: #999; }
.angle-framework { font-size: 11px; color: #555; padding: 2px 8px; border: 1px solid rgba(0,0,0,0.12); border-radius: 100px; }
.badge-shortlist { font-size: 10px; padding: 3px 8px; background: #111; color: #fff; border-radius: 100px; font-weight: 500; letter-spacing: 0.02em; text-transform: uppercase; }
.angle-title { margin: 0; font-size: 16px; font-weight: 600; line-height: 1.35; letter-spacing: -0.01em; }

.hooks { margin-bottom: 14px; }
.hooks-label { font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
.hook-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
.hook { display: grid; grid-template-columns: 18px 1fr; gap: 8px; align-items: start; font-size: 14px; line-height: 1.45; color: #222; }
.hook-num { color: #aaa; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; padding-top: 2px; }

.mechanism { font-size: 13px; color: #555; padding-top: 12px; border-top: 1px solid rgba(0,0,0,0.06); margin-bottom: 12px; line-height: 1.5; }
.mech-label { font-weight: 600; color: #333; }

.meta-row { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.tag { font-size: 11px; padding: 3px 8px; border-radius: 100px; border: 1px solid rgba(0,0,0,0.1); color: #555; }
.tag-format { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 10px; }
.tag-bilingual { color: #111; border-color: rgba(0,0,0,0.25); }
.fit-strong { color: #0a6d2f; border-color: rgba(10,109,47,0.3); }
.fit-stretch { color: #946100; border-color: rgba(148,97,0,0.3); }

.why { font-size: 12px; color: #444; padding: 10px 12px; background: rgba(0,0,0,0.025); border-radius: 8px; line-height: 1.5; margin-bottom: 14px; }
.why-label { font-weight: 600; }

/* PAGE DESC */
.page-desc { margin: 6px 0 0; font-size: 13px; color: #555; line-height: 1.55; max-width: 760px; }

/* FRESH (iteration-new) cards — derived or v3-updated. Excludes initial v1 brainstorm. */
.angle[data-v2new="1"] {
  border-left-color: rgba(148,97,0,0.5);
  border-left-width: 3px;
  position: relative;
}
.angle[data-v2new="1"]::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 12px 12px 0;
  border-color: transparent rgba(148,97,0,0.5) transparent transparent;
  border-radius: 0 12px 0 0;
}

/* PREV NOTE */
.prev-note { font-size: 13px; padding: 10px 14px; background: rgba(0,0,0,0.03); border-left: 3px solid rgba(0,0,0,0.3); border-radius: 0 8px 8px 0; line-height: 1.55; margin-bottom: 12px; color: #333; }
.prev-note-label { display: block; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; color: #888; margin-bottom: 4px; font-weight: 600; }
.prev-note-text { display: block; font-style: italic; }

/* SPARK GROUP CONTAINER (parent + derived as one cluster) */
.spark-group { background: linear-gradient(180deg, rgba(148,97,0,0.06) 0%, rgba(148,97,0,0.02) 100%); border: 2px solid rgba(148,97,0,0.25); border-radius: 16px; padding: 18px; margin-bottom: 18px; grid-column: 1 / -1; position: relative; }
.spark-group::before { content: 'SPARK CLUSTER'; position: absolute; top: -10px; left: 16px; font-size: 10px; padding: 3px 10px; background: #946100; color: #fff; border-radius: 100px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 600; letter-spacing: 0.06em; }
.spark-group > .angle.spark-parent { background: #fff7e6; border: 2px solid rgba(148,97,0,0.4); margin-bottom: 14px; box-shadow: 0 2px 8px rgba(148,97,0,0.08); }
.spark-group > .angle.spark-parent .angle-id-row::before { content: '★ ANCHOR'; font-size: 9px; padding: 3px 7px; background: #946100; color: #fff; border-radius: 100px; margin-right: 6px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 600; letter-spacing: 0.05em; }
.spark-group .spark-derived-list { display: flex; flex-direction: column; gap: 10px; margin-left: 20px; padding-left: 16px; border-left: 2px dashed rgba(148,97,0,0.3); }
.spark-group .spark-derived-list > .angle.spark-derived { background: #fff; margin-bottom: 0; position: relative; }
.spark-group .spark-derived-list > .angle.spark-derived::before { content: '↳'; position: absolute; left: -22px; top: 14px; color: rgba(148,97,0,0.6); font-size: 18px; font-weight: 600; }

/* FULL-WIDTH for cards with comments or previous notes (active section only) */
.angle[data-status="active"].full-width,
.angle[data-status="active"][data-has-prev="1"] { grid-column: 1 / -1; }

/* V2 + DERIVED + ADD CARD */
.badge-derived { font-size: 10px; padding: 3px 8px; border: 1px solid rgba(148,97,0,0.25); border-radius: 100px; color: #946100; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.v2-note { font-size: 12px; color: #946100; padding: 8px 10px; background: rgba(255,251,234,0.7); border: 1px solid rgba(148,97,0,0.18); border-radius: 6px; line-height: 1.5; margin-bottom: 12px; }
.v2-note-label { font-weight: 600; }
.angle.angle-custom { background: #fffef5; border-color: rgba(148,97,0,0.18); }

.form-row { margin-bottom: 12px; }
.form-label { display: block; font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }
.form-actions { display: flex; gap: 8px; }
.form-btn { padding: 10px 16px; border-radius: 8px; font-size: 13px; cursor: pointer; border: 1px solid rgba(0,0,0,0.15); background: #fff; color: #111; font-family: inherit; min-height: 40px; }
.form-btn-primary { background: #111; color: #fff; border-color: #111; }
.form-btn-primary:hover { background: #333; }
.custom-delete { background: none; border: none; color: #999; cursor: pointer; font-size: 18px; padding: 0 4px; line-height: 1; margin-left: auto; }
.custom-delete:hover { color: #b00020; }

/* FLOATING ADD BUTTON */
.fab-add { position: fixed; bottom: 80px; right: 18px; z-index: 90; background: #111; color: #fff; border: none; border-radius: 100px; padding: 12px 18px; font-size: 14px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 16px rgba(0,0,0,0.2); font-family: inherit; min-height: 44px; touch-action: manipulation; }
.fab-add:hover { background: #333; transform: translateY(-1px); }

/* MODAL */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 200; display: flex; align-items: center; justify-content: center; padding: 18px; overflow-y: auto; }
.modal-overlay[hidden] { display: none !important; }
.modal-card { background: #fff; border-radius: 14px; padding: 24px; width: 100%; max-width: 480px; max-height: 90vh; overflow-y: auto; box-shadow: 0 12px 40px rgba(0,0,0,0.3); }
.modal-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.modal-head h3 { margin: 0; font-size: 18px; font-weight: 600; }
.modal-close { background: none; border: none; font-size: 26px; line-height: 1; color: #999; cursor: pointer; padding: 0 6px; }
.modal-close:hover { color: #111; }
.modal-card input[type="text"], .modal-card select, .modal-card textarea { width: 100%; padding: 10px 12px; border: 1px solid rgba(0,0,0,0.12); border-radius: 8px; font-size: 14px; font-family: inherit; box-sizing: border-box; background: #fff; color: #111; }
.modal-card textarea { min-height: 60px; resize: vertical; }
.modal-card input:focus, .modal-card select:focus, .modal-card textarea:focus { outline: none; border-color: rgba(0,0,0,0.3); }

/* SECTION TAGS + COUNTS (shared across all three sections) */
.section-tag { display: inline-block; font-size: 10px; padding: 3px 8px; border-radius: 100px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 600; letter-spacing: 0.04em; margin-right: 8px; vertical-align: middle; }
.tag-bank { background: #0a6d2f; color: #fff; }
.tag-active { background: #946100; color: #fff; }
.tag-archive { background: #999; color: #fff; }
.section-count { display: inline-block; font-size: 12px; padding: 2px 9px; border-radius: 100px; margin-left: 6px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background: rgba(0,0,0,0.06); color: #555; vertical-align: middle; font-weight: 600; }
.bank-section .section-count { background: rgba(10,109,47,0.12); color: #0a6d2f; }
.active-section .section-count { background: rgba(148,97,0,0.12); color: #946100; }

/* BANK SECTION */
.bank-section { margin-bottom: 20px; padding: 12px 14px; background: rgba(10,109,47,0.04); border: 1px solid rgba(10,109,47,0.18); border-radius: 10px; }
.bank-section .section-head h2 { margin: 0 0 2px; font-size: 14px; font-weight: 600; color: #222; }
.bank-section .section-head p { margin: 0 0 10px; font-size: 11px; color: #666; line-height: 1.4; }
.bank-grid { display: grid; grid-template-columns: 1fr; gap: 4px; }
.angle[data-status="bank"] { background: #fff; border-color: rgba(10,109,47,0.18); }
.angle[data-status="bank"] .badge-shortlist { display: none; }

/* ACTIVE SECTION */
.active-section { margin-bottom: 24px; }
.section-head-active { padding: 14px 16px; background: rgba(148,97,0,0.04); border: 1px solid rgba(148,97,0,0.18); border-radius: 10px; margin-bottom: 18px; }
.section-head-active h2 { margin: 0 0 4px; font-size: 16px; font-weight: 600; color: #222; }
.section-head-active p { margin: 0; font-size: 12px; color: #666; line-height: 1.4; }

/* ARCHIVE SECTION */
.archive-section { margin-top: 28px; margin-bottom: 20px; }
.archive-details { background: rgba(0,0,0,0.02); border: 1px solid rgba(0,0,0,0.08); border-radius: 10px; padding: 12px 14px; }
.archive-summary { font-size: 13px; color: #555; cursor: pointer; user-select: none; font-weight: 500; list-style-position: inside; }
.archive-summary:hover { color: #111; }
.archive-details[open] > .archive-summary { margin-bottom: 8px; }
.archive-help { font-size: 11px; color: #888; margin: 6px 0 12px; line-height: 1.4; }
.archive-grid { display: grid; grid-template-columns: 1fr; gap: 4px; }
.angle[data-status="archive"] { opacity: 0.8; background: #fff; }
.angle[data-status="archive"]:hover { opacity: 1; }
.archive-section .section-count { background: rgba(0,0,0,0.08); color: #666; }

/* Hide archived cards entirely from the main view (they only appear in archive summary at bottom) */
.angle[data-status="archive"] { display: none !important; }

/* Banked cards stay in main view but visually marked + compact */
.angle[data-status="bank"] .angle-id-row::after {
  content: 'BANKED';
  font-size: 9px;
  padding: 3px 7px;
  background: #0a6d2f;
  color: #fff;
  border-radius: 100px;
  font-weight: 600;
  letter-spacing: 0.05em;
  margin-left: auto;
  flex-shrink: 0;
}
.angle[data-status="bank"] { background: rgba(10,109,47,0.04); border-color: rgba(10,109,47,0.25); }

/* SUMMARY ROWS (used for bank-grid + archive-grid as read-only lists) */
.summary-row { display: grid; grid-template-columns: 64px 1fr auto; gap: 10px; align-items: center; padding: 8px 12px; background: #fff; border: 1px solid rgba(0,0,0,0.06); border-radius: 8px; text-decoration: none; color: #111; font-size: 13px; transition: background 0.1s; }
.summary-row:hover { background: rgba(0,0,0,0.03); }
.summary-id { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; color: #777; }
.summary-title { font-weight: 500; line-height: 1.3; }
.summary-tag { font-size: 11px; color: #555; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.bank-grid .summary-row { border-color: rgba(10,109,47,0.2); }
.archive-grid .summary-row { background: rgba(0,0,0,0.02); }

/* Default: toggle hidden, body visible */
.card-expand-toggle { display: none; padding: 4px 10px; background: none; border: none; font-size: 11px; cursor: pointer; color: #888; font-family: inherit; min-height: 24px; touch-action: manipulation; text-decoration: underline; text-underline-offset: 3px; }
.card-expand-toggle:hover { color: #111; }
.angle .angle-body { display: block; }

/* ACTIVE = full card, no toggle */
.angle[data-status="active"] .card-expand-toggle { display: none; }

/* BANKED (collapsed default) = compact one-row layout, toggle visible */
.angle[data-fold-init="1"]:not([data-expanded="true"]) {
  padding: 8px 12px;
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 10px;
  row-gap: 4px;
}
.angle[data-fold-init="1"]:not([data-expanded="true"]) .angle-head { grid-column: 1; margin-bottom: 0; min-width: 0; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .angle-head .angle-id-row { gap: 6px; margin-bottom: 2px; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .angle-head .badge-shortlist { display: none; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .angle-head .angle-framework { display: none; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .angle-title { font-size: 13px; font-weight: 500; line-height: 1.3; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .meta-row { display: none; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .angle-body { display: none; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .card-comment { display: none; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .selectors { grid-column: 1; padding-top: 0; border-top: none; margin-top: 0; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .selectors-label { display: none; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .selector-group { display: inline-flex; flex-wrap: wrap; gap: 10px; margin-bottom: 0; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .selector { font-size: 11px; min-height: 22px; padding: 0; gap: 6px; color: #0a6d2f; font-weight: 500; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .selector input[type="checkbox"] { width: 14px; height: 14px; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .selector:has(input:not(:checked)) { display: none; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .selector-action { display: none; }
.angle[data-fold-init="1"]:not([data-expanded="true"]) .card-expand-toggle {
  display: inline-block;
  grid-column: 2;
  grid-row: 1 / span 2;
  align-self: center;
  padding: 4px 8px;
  font-size: 11px;
}

/* BANKED expanded = full card, toggle visible (to collapse back) */
.angle[data-fold-init="1"][data-expanded="true"] .card-expand-toggle { display: block; margin: 10px 0 0; width: 100%; text-align: center; }

/* CARD COMMENT */
.card-comment { margin-top: 14px; padding-top: 14px; border-top: 1px dashed rgba(0,0,0,0.1); }
.card-comment-label { font-size: 10px; color: #999; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; display: block; }
.card-comment-input { width: 100%; min-height: 64px; padding: 10px 12px; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; font-family: inherit; font-size: 13px; line-height: 1.5; resize: vertical; box-sizing: border-box; color: #222; background: #fafafa; }
.card-comment-input:focus { outline: 1px solid rgba(0,0,0,0.2); border-color: rgba(0,0,0,0.25); background: #fff; }
.card-comment-input::placeholder { color: rgba(0,0,0,0.3); }
.card-comment.has-note .card-comment-input { background: #fffbea; border-color: rgba(148,97,0,0.25); }

/* SELECTORS */
.selectors { padding-top: 14px; border-top: 1px solid rgba(0,0,0,0.06); }
.selectors-label { font-size: 10px; color: #999; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px; }
.selector-group { display: flex; flex-direction: column; gap: 2px; margin-bottom: 8px; }
.selector { display: flex; align-items: center; gap: 10px; font-size: 14px; color: #333; cursor: pointer; padding: 8px 4px; user-select: none; min-height: 36px; -webkit-tap-highlight-color: transparent; }
.selector input[type="checkbox"] { width: 18px; height: 18px; accent-color: #111; cursor: pointer; flex-shrink: 0; margin: 0; }
.selector:hover { color: #111; }
.selector-action { padding-top: 12px; border-top: 1px dashed rgba(0,0,0,0.1); margin-top: 6px; color: #555; }
.selector-action input[type="checkbox"] { accent-color: #946100; }
.selector-action span { font-style: italic; }

/* SELECTION PANEL */
.selection-panel { position: fixed; bottom: 0; left: 0; right: 0; background: #111; color: #fff; z-index: 100; box-shadow: 0 -2px 16px rgba(0,0,0,0.18); }
.selection-panel.collapsed .panel-expanded { display: none; }
.selection-panel-bar { display: flex; align-items: center; justify-content: space-between; padding: 14px 18px; cursor: pointer; gap: 12px; min-height: 56px; }
.panel-summary { font-size: 14px; font-weight: 500; flex: 1; min-width: 0; }
.count { font-weight: 600; }
.count-zero { color: #888; font-weight: 400; }
.panel-toggle { font-size: 11px; color: #aaa; text-transform: uppercase; letter-spacing: 0.05em; }
.panel-expanded { padding: 6px 18px 18px; max-height: 70vh; overflow-y: auto; }
.panel-label { display: block; font-size: 11px; color: #aaa; text-transform: uppercase; letter-spacing: 0.05em; margin: 12px 0 6px; }
.panel-label:first-child { margin-top: 4px; }
.panel-comment, .panel-prompt { width: 100%; padding: 12px; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; background: rgba(255,255,255,0.05); color: #fff; font-family: inherit; font-size: 14px; line-height: 1.55; resize: vertical; box-sizing: border-box; }
.panel-comment { min-height: 100px; }
.panel-prompt { min-height: 200px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; white-space: pre-wrap; }
.panel-comment::placeholder { color: rgba(255,255,255,0.35); }
.panel-comment:focus, .panel-prompt:focus { outline: 1px solid rgba(255,255,255,0.25); }
.panel-actions { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }
.panel-btn { padding: 11px 18px; border-radius: 8px; font-size: 13px; font-weight: 500; cursor: pointer; border: none; min-height: 42px; touch-action: manipulation; font-family: inherit; }
.btn-copy { background: #fff; color: #111; }
.btn-copy:active, .btn-copy:hover { background: #e8e8e8; }
.btn-copy.copied { background: #0a6d2f; color: #fff; }
.btn-clear { background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.25); }
.btn-clear:active, .btn-clear:hover { background: rgba(255,255,255,0.08); }

/* FRAMEWORKS */
.frameworks-section { margin-top: 36px; padding: 18px; background: #fff; border: 1px solid rgba(0,0,0,0.06); border-radius: 10px; }
.frameworks-section header h2 { margin: 0 0 4px; font-size: 17px; font-weight: 600; }
.frameworks-section header p { margin: 0 0 16px; font-size: 13px; color: #555; }
.fw-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
.fw-card { padding: 12px 14px; border: 1px solid rgba(0,0,0,0.06); border-radius: 8px; }
.fw-name { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.fw-rule { font-size: 12px; color: #555; line-height: 1.5; }

/* FOOTER */
.page-foot { margin-top: 36px; padding-top: 20px; border-top: 1px solid rgba(0,0,0,0.06); text-align: center; color: #999; font-size: 12px; }
.page-foot p { margin: 4px 0; }

/* TABLET */
@media (min-width: 720px) {
  .content-wrap { padding: 28px 24px 130px; }
  .angle-grid { grid-template-columns: repeat(2, 1fr); gap: 16px; }
  .fw-grid { grid-template-columns: repeat(2, 1fr); }
  .page-head h1 { font-size: 24px; }
  .pillar-name { font-size: 20px; }
  .selector-group { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
}

/* DESKTOP */
@media (min-width: 1024px) {
  .content-wrap { padding: 36px 32px 150px; }
  .angle-grid { grid-template-columns: repeat(3, 1fr); }
  .fw-grid { grid-template-columns: repeat(3, 1fr); }
  .page-head h1 { font-size: 28px; }
  .selection-panel { max-width: 760px; left: 50%; transform: translateX(-50%); border-radius: 12px 12px 0 0; }
}
"""

APP_JS = r"""
const FMT_LABELS = {
  reel: 'Short-form reel',
  longform: 'Long-form video',
  image: 'Single image',
  carousel: 'Carousel',
  kol: 'KOL angle',
  findmore: 'Find more angles like'
};
let angleMeta = {};
let selections = {};
let versionTag = 'v2';
let cardComments = {};
let customAngles = [];
let customCounter = 0;

function loadAngleMeta() {
  try {
    const el = document.getElementById('angle-meta');
    if (el) angleMeta = JSON.parse(el.textContent);
  } catch (_) { angleMeta = {}; }
  try {
    const vt = document.getElementById('version-tag');
    if (vt) versionTag = JSON.parse(vt.textContent);
  } catch (_) {}
}
function loadSelections() {
  try {
    const stored = localStorage.getItem('spark_elec_sel_v2');
    if (stored) selections = JSON.parse(stored);
  } catch (_) { selections = {}; }
}
function saveSelections() {
  try { localStorage.setItem('spark_elec_sel_v2', JSON.stringify(selections)); } catch (_) {}
}
function loadCardComments() {
  try {
    const stored = localStorage.getItem('spark_elec_card_comments_v2');
    if (stored) cardComments = JSON.parse(stored);
  } catch (_) { cardComments = {}; }
}
function saveCardComments() {
  try { localStorage.setItem('spark_elec_card_comments_v2', JSON.stringify(cardComments)); } catch (_) {}
}
function loadCustomAngles() {
  try {
    const stored = localStorage.getItem('spark_elec_custom_angles_v2');
    if (stored) {
      customAngles = JSON.parse(stored);
      customAngles.forEach(c => {
        const m = c.id.match(/^C(\d+)$/);
        if (m && parseInt(m[1]) > customCounter) customCounter = parseInt(m[1]);
      });
    }
  } catch (_) { customAngles = []; }
}
function saveCustomAngles() {
  try { localStorage.setItem('spark_elec_custom_angles_v2', JSON.stringify(customAngles)); } catch (_) {}
}
function escapeHtml(s) {
  return String(s || '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function renderCustomCard(c) {
  const hookBlock = c.hook ? `<div class="hooks"><div class="hooks-label">Your hook</div><ul class="hook-list"><li class="hook"><span class="hook-num">1</span><span class="hook-text">${escapeHtml(c.hook)}</span></li></ul></div>` : '';
  const noteBlock = c.note ? `<div class="v2-note"><span class="v2-note-label">Your note:</span> ${escapeHtml(c.note)}</div>` : '';
  return `
<article class="angle angle-custom" id="${c.id}" data-pillar="${c.pillar}" data-fit="strong" data-bilingual="0" data-shortlist="0" data-custom="1">
  <header class="angle-head">
    <div class="angle-id-row">
      <span class="angle-id">${escapeHtml(c.id)}</span>
      <span class="angle-framework">Custom</span>
      <button class="custom-delete" onclick="deleteCustomAngle('${c.id}')" title="Remove this card">×</button>
    </div>
    <h3 class="angle-title">${escapeHtml(c.title)}</h3>
  </header>
  <div class="meta-row"><span class="tag">Custom card</span></div>
  <div class="angle-body">
    ${noteBlock}
    ${hookBlock}
  </div>
  <div class="selectors">
    <div class="selectors-label">Use this angle as</div>
    <div class="selector-group">
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="${c.id}" data-fmt="reel"><span>Short-form reel</span></label>
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="${c.id}" data-fmt="longform"><span>Long-form video</span></label>
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="${c.id}" data-fmt="image"><span>Single image</span></label>
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="${c.id}" data-fmt="carousel"><span>Carousel</span></label>
      <label class="selector"><input type="checkbox" class="sel-cb" data-id="${c.id}" data-fmt="kol"><span>KOL angle</span></label>
    </div>
    <label class="selector selector-action"><input type="checkbox" class="sel-cb" data-id="${c.id}" data-fmt="findmore"><span>Find more angles like this</span></label>
  </div>
  <div class="card-comment">
    <label class="card-comment-label" for="comment-${c.id}">Your note on this angle (optional)</label>
    <textarea class="card-comment-input" id="comment-${c.id}" data-id="${c.id}" placeholder="anything else to add..."></textarea>
  </div>
  <button class="card-expand-toggle" onclick="toggleCardDetails(this)">Show details ▾</button>
</article>`;
}
function toggleCardDetails(btn) {
  const card = btn.closest('.angle');
  const expanded = card.dataset.expanded === 'true';
  card.dataset.expanded = expanded ? 'false' : 'true';
  btn.textContent = expanded ? 'Show details ▾' : 'Hide details ▴';
}
function renderCustomCards() {
  customAngles.forEach(c => {
    const existing = document.getElementById(c.id);
    if (existing) existing.remove();
    const pillarSection = document.querySelector(`.pillar[data-pillar="${c.pillar}"] .angle-grid`);
    if (pillarSection) {
      const wrap = document.createElement('div');
      wrap.innerHTML = renderCustomCard(c);
      pillarSection.appendChild(wrap.firstElementChild);
    }
    angleMeta[c.id] = c.title;
  });
}
function openAddCardModal() {
  const ov = document.getElementById('add-card-overlay');
  if (ov) {
    ov.hidden = false;
    setTimeout(() => document.getElementById('custom-title').focus(), 50);
  }
}
function closeAddCardModal() {
  const ov = document.getElementById('add-card-overlay');
  if (ov) ov.hidden = true;
}
function closeAddCardModalOverlay(e) {
  // Only close if user clicks the dimmed background, not the card itself
  if (e.target === document.getElementById('add-card-overlay')) closeAddCardModal();
}
function saveCustomAngle() {
  const titleEl = document.getElementById('custom-title');
  const pillarEl = document.getElementById('custom-pillar');
  const hookEl = document.getElementById('custom-hook');
  const noteEl = document.getElementById('custom-note');
  const title = titleEl.value.trim();
  if (!title) { titleEl.focus(); return; }
  customCounter += 1;
  const newCard = {
    id: 'C' + customCounter,
    pillar: pillarEl.value,
    title: title,
    hook: hookEl.value.trim(),
    note: noteEl.value.trim(),
  };
  customAngles.push(newCard);
  saveCustomAngles();
  titleEl.value = '';
  hookEl.value = '';
  noteEl.value = '';
  // re-render the new card
  const pillarSection = document.querySelector(`.pillar[data-pillar="${newCard.pillar}"] .angle-grid`);
  if (pillarSection) {
    const wrap = document.createElement('div');
    wrap.innerHTML = renderCustomCard(newCard);
    const newEl = wrap.firstElementChild;
    pillarSection.appendChild(newEl);
    angleMeta[newCard.id] = newCard.title;
    // wire up handlers for the new card
    newEl.querySelectorAll('.sel-cb').forEach(cb => cb.addEventListener('change', onSelectionChange));
    newEl.querySelectorAll('.card-comment-input').forEach(ta => ta.addEventListener('input', onCardCommentChange));
    // init defaults
    newEl.querySelectorAll('.sel-cb').forEach(cb => {
      const id = cb.dataset.id;
      if (!selections[id]) selections[id] = {};
      selections[id][cb.dataset.fmt] = false;
    });
    saveSelections();
  }
  closeAddCardModal();
  categorizeCards();
  updatePanel();
}
function deleteCustomAngle(id) {
  if (!confirm('Remove this custom card?')) return;
  customAngles = customAngles.filter(c => c.id !== id);
  saveCustomAngles();
  // remove from DOM
  const el = document.getElementById(id);
  if (el) el.remove();
  // clean selections + comments + meta
  delete selections[id];
  delete cardComments[id];
  delete angleMeta[id];
  saveSelections();
  saveCardComments();
  updatePanel();
}
function initSelectionState() {
  document.querySelectorAll('.sel-cb').forEach(cb => {
    const id = cb.dataset.id;
    const fmt = cb.dataset.fmt;
    if (!selections[id]) selections[id] = {};
    if (cb.defaultChecked) {
      // Server-seeded bank pick: authoritative, overrides any stored/prior value so the
      // locked angles always show banked regardless of this device's saved history.
      selections[id][fmt] = true;
      cb.checked = true;
    } else if (typeof selections[id][fmt] !== 'undefined') {
      cb.checked = selections[id][fmt];
    } else {
      selections[id][fmt] = cb.checked;
    }
  });
  saveSelections();
}
function initCardCommentState() {
  document.querySelectorAll('.card-comment-input').forEach(ta => {
    const id = ta.dataset.id;
    const text = cardComments[id] || '';
    ta.value = text;
    const wrap = ta.closest('.card-comment');
    if (wrap) wrap.classList.toggle('has-note', text.trim().length > 0);
  });
}
function onSelectionChange(e) {
  const cb = e.target;
  const id = cb.dataset.id;
  const fmt = cb.dataset.fmt;
  if (!selections[id]) selections[id] = {};
  selections[id][fmt] = cb.checked;
  saveSelections();
  categorizeCards();
  updatePanel();
}
function onCardCommentChange(e) {
  const ta = e.target;
  const id = ta.dataset.id;
  const txt = ta.value;
  cardComments[id] = txt;
  saveCardComments();
  const wrap = ta.closest('.card-comment');
  if (wrap) wrap.classList.toggle('has-note', txt.trim().length > 0);
  // Debounce categorisation slightly so it doesn't fire on every keystroke (visual jump)
  clearTimeout(window._catTimer);
  window._catTimer = setTimeout(categorizeCards, 400);
  updatePanel();
}
function attachSelectionHandlers() {
  document.querySelectorAll('.sel-cb').forEach(cb => {
    cb.addEventListener('change', onSelectionChange);
  });
  document.querySelectorAll('.card-comment-input').forEach(ta => {
    ta.addEventListener('input', onCardCommentChange);
  });
}
function getCardStatus(id) {
  const sels = selections[id] || {};
  const card = document.getElementById(id);
  const hasPrevNote = card && card.dataset.hasPrev === '1';
  const hasFormat = ['reel','longform','image','carousel','kol'].some(f => sels[f]);
  const hasComment = (cardComments[id] || '').trim().length > 0;
  const hasFindmore = !!sels.findmore;
  // A card with a previous-iteration note is still being iterated on (not yet finalised).
  if (hasFormat && !hasComment && !hasFindmore && !hasPrevNote) return 'bank';
  if (hasFormat || hasComment || hasFindmore || hasPrevNote) return 'active';
  // v1 = pristine: untouched cards stay active for triage.
  // v2+ (or once any previous_note exists) = narrowing: untouched cards fall to archive.
  let ver = 'v1';
  try { ver = JSON.parse(document.getElementById('version-tag').textContent); } catch (e) {}
  const narrowing = (ver !== 'v1') || document.querySelector('.angle[data-has-prev="1"]') !== null;
  return narrowing ? 'archive' : 'active';
}
let _clustersWrapped = false;
let _foldStateLocked = false;
function unwrapSparkGroups() {
  // Move parent + derived back to their pillar grid before re-categorising
  document.querySelectorAll('.spark-group').forEach(group => {
    const parent = group.querySelector('.spark-parent');
    const derivedList = group.querySelector('.spark-derived-list');
    const cards = [parent, ...(derivedList ? Array.from(derivedList.children) : [])].filter(Boolean);
    cards.forEach(card => {
      card.classList.remove('spark-parent', 'spark-derived');
      const pillar = card.dataset.pillar;
      const pillarGrid = document.querySelector(`.pillar[data-pillar="${pillar}"] .angle-grid`);
      if (pillarGrid) pillarGrid.appendChild(card);
    });
    group.remove();
  });
}
function wrapSparkGroups() {
  // For each active parent that has active derived children, wrap them in .spark-group
  document.querySelectorAll('.pillar .angle-grid').forEach(grid => {
    const activeCards = Array.from(grid.querySelectorAll(':scope > .angle[data-status="active"]'));
    activeCards.forEach(card => {
      if (card.dataset.parentId) return; // skip derived
      const derived = activeCards.filter(d => d.dataset.parentId === card.id);
      if (derived.length === 0) return;
      // create wrapper
      const group = document.createElement('div');
      group.className = 'spark-group';
      grid.insertBefore(group, card);
      group.appendChild(card);
      card.classList.add('spark-parent');
      const list = document.createElement('div');
      list.className = 'spark-derived-list';
      group.appendChild(list);
      derived.forEach(d => {
        list.appendChild(d);
        d.classList.add('spark-derived');
      });
    });
  });
}
function applyFullWidth() {
  document.querySelectorAll('.angle[data-status="active"]').forEach(card => {
    const id = card.id;
    const hasComment = (cardComments[id] || '').trim().length > 0;
    card.classList.toggle('full-width', hasComment);
  });
}
function renderSummaryRows(gridId, status) {
  const grid = document.getElementById(gridId);
  if (!grid) return;
  grid.innerHTML = '';
  document.querySelectorAll(`.angle[data-status="${status}"]`).forEach(card => {
    const id = card.id;
    const title = (card.querySelector('.angle-title') ? card.querySelector('.angle-title').textContent : '').trim();
    const formats = [];
    card.querySelectorAll('.sel-cb').forEach(cb => {
      if (cb.checked && cb.dataset.fmt !== 'findmore' && FMT_LABELS[cb.dataset.fmt]) {
        formats.push(FMT_LABELS[cb.dataset.fmt]);
      }
    });
    const row = document.createElement('a');
    row.className = 'summary-row';
    row.href = '#' + id;
    row.innerHTML = `<span class="summary-id">${id}</span><span class="summary-title">${title}</span><span class="summary-tag">${formats.join(' · ') || '—'}</span>`;
    grid.appendChild(row);
  });
}
function categorizeCards() {
  const bankSection = document.getElementById('bank-section');
  const archiveSection = document.getElementById('archive-section');
  const bankCount = document.getElementById('bank-count');
  const activeCount = document.getElementById('active-count');
  const archiveCount = document.getElementById('archive-count');

  // First pass: assign initial status from own engagement
  document.querySelectorAll('.angle').forEach(card => {
    card.dataset.status = getCardStatus(card.id);
  });
  // Second pass: promote derived-from-active-parent to active
  document.querySelectorAll('.angle[data-parent-id]').forEach(card => {
    const parentEl = document.getElementById(card.dataset.parentId);
    if (parentEl && parentEl.dataset.status === 'active' && card.dataset.status === 'archive') {
      card.dataset.status = 'active';
    }
  });

  // Counts
  let bankN = 0, activeN = 0, archiveN = 0;
  document.querySelectorAll('.angle').forEach(card => {
    const s = card.dataset.status;
    if (s === 'bank') bankN++;
    else if (s === 'archive') archiveN++;
    else activeN++;
  });

  // Section visibility + counts (no physical moves)
  const activeSection = document.getElementById('active-section');
  if (bankSection) bankSection.hidden = bankN === 0;
  if (archiveSection) archiveSection.hidden = archiveN === 0;
  // Fully-narrowed state (0 iterating): keep banked cards visible as full cards, but drop the
  // empty "iterating" header and any pillar with no banked cards, so it reads cleanly.
  const narrowed = activeN === 0;
  if (activeSection) activeSection.hidden = false;
  const activeHeader = activeSection ? activeSection.querySelector('.section-head-active') : null;
  if (activeHeader) activeHeader.style.display = narrowed ? 'none' : '';
  document.querySelectorAll('.pillar').forEach(p => {
    if (!narrowed) { p.style.display = ''; return; }
    const hasBank = [...p.querySelectorAll('.angle')].some(c => c.dataset.status === 'bank');
    p.style.display = hasBank ? '' : 'none';
  });
  if (bankCount) bankCount.textContent = bankN;
  if (activeCount) activeCount.textContent = activeN;
  if (archiveCount) archiveCount.textContent = archiveN;

  // Render read-only summary lists into bank-grid + archive-grid
  renderSummaryRows('bank-grid', 'bank');
  renderSummaryRows('archive-grid', 'archive');

  // Lock fold + full-width state ONCE on first run — nothing about visual layout changes on user ticks/typing
  if (!_foldStateLocked) {
    document.querySelectorAll('.angle').forEach(card => {
      card.dataset.foldInit = card.dataset.status === 'bank' ? '1' : '0';
    });
    applyFullWidth();
    _foldStateLocked = true;
  }
  // Wrap spark clusters ONCE on first run; never re-wrap after that
  if (!_clustersWrapped) {
    wrapSparkGroups();
    _clustersWrapped = true;
  }
}
function generatePrompt() {
  const groups = { reel: [], longform: [], image: [], carousel: [], kol: [], findmore: [] };
  const bankGroups = { reel: [], longform: [], image: [], carousel: [], kol: [] };
  Object.keys(selections).sort().forEach(angleId => {
    const fmts = selections[angleId];
    const status = getCardStatus(angleId);
    Object.entries(fmts).forEach(([fmt, checked]) => {
      if (!checked) return;
      if (status === 'bank' && bankGroups[fmt]) bankGroups[fmt].push(angleId);
      else if (groups[fmt]) groups[fmt].push(angleId);
    });
  });
  const lines = [];
  lines.push(versionTag + ' selections from sourcing electronics from China spark:');
  lines.push('');

  // Bank section
  const bankTotal = Object.values(bankGroups).reduce((s, arr) => s + arr.length, 0);
  if (bankTotal > 0) {
    lines.push('== FINALISED (saved to bank) ==');
    lines.push('');
    ['reel', 'longform', 'image', 'carousel', 'kol'].forEach(fmt => {
      const ids = bankGroups[fmt];
      if (ids.length === 0) return;
      lines.push(FMT_LABELS[fmt] + ' (' + ids.length + '):');
      ids.forEach(id => lines.push('  - ' + id + ': ' + (angleMeta[id] || '')));
      lines.push('');
    });
  }

  // Active notes
  const noteEntries = Object.entries(cardComments)
    .filter(([id, txt]) => txt && txt.trim())
    .sort();
  if (noteEntries.length > 0) {
    lines.push('== STILL ITERATING - NOTES ==');
    lines.push('');
    noteEntries.forEach(([id, txt]) => {
      const title = angleMeta[id] || '';
      lines.push(id + ' (' + title + '):');
      txt.trim().split('\n').forEach(line => lines.push('  ' + line));
      lines.push('');
    });
  }

  // Active selections
  const activeTotal = Object.values(groups).slice(0,5).reduce((s, arr) => s + arr.length, 0);
  if (activeTotal > 0 || groups.findmore.length > 0) {
    lines.push('== STILL ITERATING - SELECTIONS ==');
    ['reel', 'longform', 'image', 'carousel', 'kol'].forEach(fmt => {
      const ids = groups[fmt];
      lines.push('');
      lines.push(FMT_LABELS[fmt] + ' (' + ids.length + '):');
      if (ids.length === 0) lines.push('  (none)');
      else ids.forEach(id => lines.push('  - ' + id + ': ' + (angleMeta[id] || '')));
    });
    if (groups.findmore.length > 0) {
      lines.push('');
      lines.push(FMT_LABELS.findmore + ' (' + groups.findmore.length + '):');
      groups.findmore.forEach(id => lines.push('  - ' + id + ': ' + (angleMeta[id] || '')));
    }
    lines.push('');
  }

  lines.push('(paste back to me to generate the next version)');
  return lines.join('\n');
}
function countSelections() {
  let total = 0;
  Object.values(selections).forEach(fmts => {
    Object.values(fmts).forEach(v => { if (v) total++; });
  });
  return total;
}
function updatePanel() {
  const total = countSelections();
  const countEl = document.getElementById('panel-count');
  if (countEl) {
    countEl.textContent = total + (total === 1 ? ' selection' : ' selections');
    countEl.classList.toggle('count-zero', total === 0);
  }
  const promptEl = document.getElementById('panel-prompt');
  if (promptEl) promptEl.value = generatePrompt();
}
function togglePanel() {
  const panel = document.getElementById('selection-panel');
  const toggle = document.getElementById('panel-toggle');
  if (panel) {
    panel.classList.toggle('collapsed');
    if (toggle) toggle.textContent = panel.classList.contains('collapsed') ? 'tap to expand' : 'tap to collapse';
  }
}
function copyPrompt() {
  const promptEl = document.getElementById('panel-prompt');
  const btn = document.getElementById('btn-copy');
  if (!promptEl || !btn) return;
  const txt = promptEl.value;
  const flash = () => {
    btn.textContent = 'Copied';
    btn.classList.add('copied');
    setTimeout(() => { btn.textContent = 'Copy prompt'; btn.classList.remove('copied'); }, 1500);
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(txt).then(flash).catch(() => {
      promptEl.select();
      try { document.execCommand('copy'); flash(); } catch (_) {}
    });
  } else {
    promptEl.select();
    try { document.execCommand('copy'); flash(); } catch (_) {}
  }
}
function clearSelections() {
  selections = {};
  cardComments = {};
  document.querySelectorAll('.sel-cb').forEach(cb => {
    cb.checked = false;
    const id = cb.dataset.id;
    if (!selections[id]) selections[id] = {};
    selections[id][cb.dataset.fmt] = false;
  });
  document.querySelectorAll('.card-comment-input').forEach(ta => {
    ta.value = '';
    const wrap = ta.closest('.card-comment');
    if (wrap) wrap.classList.remove('has-note');
  });
  saveSelections();
  saveCardComments();
  updatePanel();
}
function attachFilters() {
  const chips = document.querySelectorAll('.chip[data-filter]');
  const pillarChips = document.querySelectorAll('.chip[data-pillar-filter]');
  let activeFilter = 'all';
  let activePillar = 'all';
  function apply() {
    document.querySelectorAll('.angle').forEach(card => {
      let show = true;
      if (activeFilter === 'shortlist' && card.dataset.shortlist !== '1') show = false;
      if (activeFilter === 'bilingual' && card.dataset.bilingual !== '1') show = false;
      if (activeFilter === 'strong' && card.dataset.fit !== 'strong') show = false;
      if (activeFilter === 'v2new' && card.dataset.v2new !== '1') show = false;
      if (activeFilter === 'custom' && card.dataset.custom !== '1') show = false;
      if (activePillar !== 'all' && card.dataset.pillar !== activePillar) show = false;
      card.classList.toggle('hidden', !show);
    });
    document.querySelectorAll('.pillar').forEach(p => {
      const visible = p.querySelectorAll('.angle:not(.hidden)').length;
      p.style.display = (activePillar !== 'all' && p.dataset.pillar !== activePillar) ? 'none' : (visible === 0 ? 'none' : '');
    });
  }
  chips.forEach(c => c.addEventListener('click', () => {
    chips.forEach(x => x.classList.remove('chip-active'));
    c.classList.add('chip-active');
    activeFilter = c.dataset.filter;
    apply();
  }));
  pillarChips.forEach(c => c.addEventListener('click', () => {
    pillarChips.forEach(x => x.classList.remove('chip-active'));
    c.classList.add('chip-active');
    activePillar = c.dataset.pillarFilter;
    apply();
  }));
}
function init() {
  loadAngleMeta();
  loadSelections();
  loadCardComments();
  loadCustomAngles();
  renderCustomCards();
  initSelectionState();
  initCardCommentState();
  attachSelectionHandlers();
  attachFilters();
  // Tag derived cards with their parent for nesting
  document.querySelectorAll('.angle').forEach(card => {
    const derived = card.querySelector('.badge-derived');
    if (derived) {
      const m = derived.textContent.match(/Sparked from (\S+)/);
      if (m) card.dataset.parentId = m[1];
    }
  });
  categorizeCards();
  updatePanel();
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
"""

def render_full_html(inner_html):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=5">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#fafafa">
<title>Sourcing electronics from China spark</title>
<style>{CSS}</style>
</head>
<body>
<div class="content-wrap">
{inner_html}
</div>
<script>{APP_JS}</script>
</body>
</html>
"""

# -------- MAIN --------

def main():
    inner = render_inner_html()
    html = render_full_html(inner)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Built: {out_path}")
    print(f"Inner HTML size: {len(inner)} chars")
    print(f"Total HTML size: {len(html)} chars")

if __name__ == "__main__":
    main()
