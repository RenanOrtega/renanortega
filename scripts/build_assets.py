"""Generates the SVG assets used by the profile README (dark + light variants).

Run: python3 scripts/build_assets.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

W = 840
SANS = "'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono','Cascadia Code',Menlo,Consolas,monospace"

THEMES = {
    "dark": dict(
        bg="#0A0D14", panel="#0F141F", border="#1E2635", text="#E8EBF2",
        muted="#8892A6", faint="#2A3345", a1="#8B5CF6", a2="#22D3EE",
        ok="#34D399", chip="#151B29", chipText="#C9CFDC",
    ),
    "light": dict(
        bg="#FBFCFE", panel="#FFFFFF", border="#E2E6EE", text="#0E1220",
        muted="#5A6377", faint="#D5DBE6", a1="#6D28D9", a2="#0891B2",
        ok="#059669", chip="#F1F3F8", chipText="#2B3245",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def defs(t, uid):
    return f"""
  <defs>
    <linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/>
    </linearGradient>
    <pattern id="dots{uid}" width="18" height="18" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{t['faint']}"/>
    </pattern>
  </defs>"""


def chip(x, y, label, t, size=12):
    w = len(label) * size * 0.62 + 22
    return (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="{t["chip"]}" stroke="{t["border"]}"/>'
        f'<text x="{x + w / 2:.1f}" y="{y + 17.5}" text-anchor="middle" font-family="{MONO}" '
        f'font-size="{size}" fill="{t["chipText"]}">{esc(label)}</text>',
        w,
    )


# ---------------------------------------------------------------- header
def header(t, name):
    H = 300
    uid = "h"
    nodes = [("api", 585, 92), ("outbox", 755, 92), ("queue", 755, 216), ("worker", 585, 216)]
    flow = "M585,92 H755 V216 H585"

    dots = ""
    for i in range(4):
        dots += (
            f'<circle r="4" fill="url(#g{uid})"><animateMotion dur="4s" repeatCount="indefinite" '
            f'begin="-{i}s" path="{flow}" keyPoints="0;1" keyTimes="0;1" calcMode="linear"/></circle>'
        )

    boxes = ""
    for label, cx, cy in nodes:
        boxes += (
            f'<rect x="{cx - 55}" y="{cy - 18}" width="110" height="36" rx="9" fill="{t["panel"]}" stroke="{t["border"]}"/>'
            f'<circle cx="{cx - 36}" cy="{cy}" r="3.5" fill="{t["ok"]}">'
            f'<animate attributeName="opacity" values="1;.35;1" dur="2s" begin="{nodes.index((label, cx, cy)) * .5}s" repeatCount="indefinite"/></circle>'
            f'<text x="{cx - 24}" y="{cy + 4.5}" font-family="{MONO}" font-size="13" fill="{t["text"]}">{label}</text>'
        )

    events = ["order.created", "payment.requested", "match.updated", "stock.reserved"]
    ev = ""
    n = len(events)
    for i, e in enumerate(events):
        a, b = i / n, (i + 1) / n
        ev += (
            f'<text x="670" y="158" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["muted"]}" opacity="0">'
            f'{e}<animate attributeName="opacity" dur="8s" repeatCount="indefinite" '
            f'keyTimes="0;{a:.3f};{a + .02:.3f};{b - .02:.3f};{b:.3f};1" values="0;0;1;1;0;0"/></text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Renan Ortega — Software Engineer, backend and distributed systems">
{defs(t, uid)}
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{t['bg']}" stroke="{t['border']}"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#dots{uid})" opacity=".7"/>
  <rect x="40" y="0" width="120" height="3" rx="1.5" fill="url(#g{uid})"/>

  <text x="40" y="62" font-family="{MONO}" font-size="13" fill="{t['muted']}">~/renan $ whoami<tspan fill="{t['a2']}">▍<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></tspan></text>
  <text x="38" y="124" font-family="{SANS}" font-size="54" font-weight="800" letter-spacing="-1.5" fill="{t['text']}">Renan Ortega</text>
  <text x="40" y="160" font-family="{SANS}" font-size="19" fill="{t['text']}">Software Engineer, <tspan fill="url(#g{uid})" font-weight="700">backend &amp; distributed systems</tspan></text>
  <text x="40" y="190" font-family="{MONO}" font-size="13" fill="{t['muted']}">.NET / C#  ·  event-driven  ·  multicloud  ·  São Paulo, BR</text>

  <rect x="40" y="226" width="232" height="32" rx="16" fill="{t['panel']}" stroke="{t['border']}"/>
  <circle cx="60" cy="242" r="9" fill="{t['ok']}" opacity=".25"><animate attributeName="r" values="4;10;4" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".45;0;.45" dur="2s" repeatCount="indefinite"/></circle>
  <circle cx="60" cy="242" r="4" fill="{t['ok']}"/>
  <text x="74" y="246.5" font-family="{MONO}" font-size="12.5" fill="{t['text']}">open to new opportunities</text>

  <path d="{flow}" fill="none" stroke="{t['faint']}" stroke-width="1.5" stroke-dasharray="4 5">
    <animate attributeName="stroke-dashoffset" from="18" to="0" dur="1.2s" repeatCount="indefinite"/>
  </path>
  {dots}
  {boxes}
  {ev}
</svg>
"""


# ---------------------------------------------------------------- project cards
def card(t, idx, title, kind, desc, flow, tags):
    H = 214
    uid = f"c{idx}"
    lines = "".join(
        f'<text x="118" y="{98 + i * 21}" font-family="{SANS}" font-size="14.5" fill="{t["muted"]}">{esc(l)}</text>'
        for i, l in enumerate(desc)
    )
    f = ""
    for i, step in enumerate(flow):
        if i:
            f += f'<tspan fill="url(#g{uid})" font-weight="700">  →  </tspan>'
        f += f'<tspan>{esc(step)}</tspan>'
    x, chips = 118, ""
    for tag in tags:
        c, w = chip(x, 166, tag, t, 11.5)
        chips += c
        x += w + 8
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">
{defs(t, uid)}
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t['panel']}" stroke="{t['border']}"/>
  <rect x="0" y="28" width="3" height="44" rx="1.5" fill="url(#g{uid})"/>
  <text x="36" y="66" font-family="{MONO}" font-size="34" font-weight="700" fill="url(#g{uid})">{idx:02d}</text>
  <text x="118" y="64" font-family="{SANS}" font-size="23" font-weight="750" letter-spacing="-.4" fill="{t['text']}">{esc(title)}</text>
  <text x="{W - 32}" y="62" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t['muted']}">{esc(kind)}</text>
  {lines}
  <text x="118" y="150" font-family="{MONO}" font-size="12.5" fill="{t['text']}">{f}</text>
  {chips}
  <text x="{W - 32}" y="184" text-anchor="end" font-family="{MONO}" font-size="16" fill="{t['muted']}">↗</text>
</svg>
"""


PROJECTS = [
    dict(
        slug="order-processing",
        title="Order Processing Platform",
        kind="event-driven backend",
        desc=[
            "Asynchronous order processing using the Transactional Outbox pattern:",
            "orders and events saved atomically, then fanned out to Lambdas via SQS.",
        ],
        flow=["API", "Outbox", "Worker", "SQS", "Lambda"],
        tags=[".NET 10", "CQRS", "PostgreSQL", "EF Core", "AWS SQS", "AWS Lambda"],
    ),
    dict(
        slug="quadra",
        title="Quadra",
        kind="mobile app · building now",
        desc=[
            "Volleyball app to organize matches, follow live games and climb group",
            "rankings. Nearby matches on a map with PostGIS, live updates via SignalR.",
        ],
        flow=["Expo app", ".NET API", "PostGIS", "SignalR"],
        tags=[".NET 10", "PostGIS", "SignalR", "React Native", "Expo", "Sentry"],
    ),
    dict(
        slug="rei-das-figurinhas",
        title="Rei das Figurinhas",
        kind="e-commerce",
        desc=[
            "Store for school sticker albums: catalog by school, cart, coupons and",
            "Mercado Pago checkout, plus an admin dashboard for orders and sales.",
        ],
        flow=["Store", "API", "Mercado Pago", "Admin"],
        tags=[".NET 9", "Clean Arch", "MongoDB", "React", "Tailwind", "Fly.io"],
    ),
]


# ---------------------------------------------------------------- stack
STACK = [
    ("core", ["C#", ".NET", "ASP.NET Core", "TypeScript"]),
    ("messaging", ["Kafka", "AWS SQS", "GCP Pub/Sub", "Azure Service Bus"]),
    ("cloud", ["AWS", "GCP", "Azure"]),
    ("data", ["PostgreSQL", "SQL Server", "MongoDB"]),
    ("delivery", ["Docker", "Kubernetes", "GitHub Actions", "ArgoCD"]),
    ("observability", ["OpenTelemetry", "Grafana", "SigNoz", "Sentry"]),
    ("also", ["React", "React Native", "Expo", "Tailwind"]),
]


def stack(t):
    row_h = 40
    H = 40 + row_h * len(STACK) + 8
    uid = "s"
    rows = ""
    for i, (label, items) in enumerate(STACK):
        y = 32 + i * row_h
        rows += (
            f'<text x="36" y="{y + 18}" font-family="{MONO}" font-size="12.5" fill="{t["muted"]}">'
            f'<tspan fill="url(#g{uid})">›</tspan> {label}</text>'
        )
        if i:
            rows += f'<line x1="36" y1="{y - 7}" x2="{W - 36}" y2="{y - 7}" stroke="{t["border"]}" stroke-dasharray="2 4"/>'
        x = 200
        for it in items:
            c, w = chip(x, y, it, t)
            rows += c
            x += w + 8
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">
{defs(t, uid)}
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t['panel']}" stroke="{t['border']}"/>
  {rows}
</svg>
"""


for theme, t in THEMES.items():
    (OUT / f"header-{theme}.svg").write_text(header(t, theme), encoding="utf-8")
    (OUT / f"stack-{theme}.svg").write_text(stack(t), encoding="utf-8")
    for i, p in enumerate(PROJECTS, 1):
        args = {k: v for k, v in p.items() if k != "slug"}
        (OUT / f"project-{p['slug']}-{theme}.svg").write_text(card(t, i, **args), encoding="utf-8")

print("assets written to", OUT)
