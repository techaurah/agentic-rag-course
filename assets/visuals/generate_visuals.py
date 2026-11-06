#!/usr/bin/env python3
"""Generate the course diagram set as clean, branded SVGs.

Style: white canvas, navy (#0B1F4A) primary boxes with white text,
light blue (#E0F2FE) secondary boxes with navy text, cyan (#0891B2)
arrows, amber (#F59E0B) accent for warnings/gates. Run: python3 generate_visuals.py
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
NAVY = "#0B1F4A"
LIGHT = "#E0F2FE"
CYAN = "#0891B2"
GREY = "#475569"
FONT = "Segoe UI, Helvetica, Arial, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, w, h, title, subtitle):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>',
            f'<text x="40" y="52" font-family="{FONT}" font-size="30" font-weight="700" fill="{NAVY}">{esc(title)}</text>',
            f'<text x="40" y="82" font-family="{FONT}" font-size="17" fill="{GREY}">{esc(subtitle)}</text>',
            f'<rect x="40" y="98" width="90" height="5" fill="{CYAN}"/>',
        ]

    def box(self, x, y, w, h, label, sub="", style="navy"):
        fill, tcol, scol = (NAVY, "#FFFFFF", "#BFE3F2") if style == "navy" else (LIGHT, NAVY, "#33506E")
        if style == "amber":
            fill, tcol, scol = "#FEF3C7", NAVY, "#7C5A03"
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}"/>')
        if sub:
            self.parts.append(f'<text x="{x + w/2}" y="{y + h/2 - 4}" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="700" fill="{tcol}">{esc(label)}</text>')
            self.parts.append(f'<text x="{x + w/2}" y="{y + h/2 + 20}" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{scol}">{esc(sub)}</text>')
        else:
            self.parts.append(f'<text x="{x + w/2}" y="{y + h/2 + 7}" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="700" fill="{tcol}">{esc(label)}</text>')

    def arrow(self, x1, y1, x2, y2, label=""):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-width="3" marker-end="url(#ah)"/>')
        if label:
            self.parts.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 8}" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="600" fill="{CYAN}">{esc(label)}</text>')

    def note(self, x, y, text):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="15" fill="{GREY}">{esc(text)}</text>')

    def save(self, name):
        defs = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                'markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
                f'fill="{CYAN}"/></marker></defs>')
        body = "\n".join(self.parts[:2] + [defs] + self.parts[2:]) + "\n</svg>"
        with open(os.path.join(OUT, name), "w") as f:
            f.write(body)
        print("wrote", name)


def course_map():
    s = SVG(1180, 560, "Agentic RAG: the course map", "Ten modules, one corpus, one golden set, one evaluated system")
    mods = [
        ("Start here", "naive RAG fails, measured"), ("Corpus and chunking", "the measuring instrument"),
        ("Lexical retrieval", "TF-IDF and BM25 from scratch"), ("Vector retrieval", "embeddings, honestly labelled"),
        ("Hybrid and ranking", "fusion, permissions, context"), ("Query understanding", "rewrite, decompose, expand"),
        ("Evaluation", "metrics, golden set, refusal"), ("Agentic RAG", "tools, routing, self correction"),
        ("Production", "freshness, budgets, playbook"), ("Capstone", "an evaluated system, gated"),
    ]
    x, y = 40, 140
    for i, (label, sub) in enumerate(mods):
        style = "amber" if i in (0, 9) else ("navy" if i % 2 == 0 else "light")
        s.box(x, y, 340, 76, label, sub, style)
        if i % 3 != 2 and i < 9:
            s.arrow(x + 340, y + 38, x + 380, y + 38)
        x += 380
        if i % 3 == 2:
            x = 40
            y += 120
    s.note(40, 540, "Every module is measured on the same 32 question golden set. The capstone assembles all of it.")
    s.save("course-map.svg")


def rag_pipeline():
    s = SVG(1180, 420, "The RAG pipeline", "Four stages, and the course spends most of its time on the first three")
    s.box(40, 150, 220, 90, "Documents", "the corpus", "light")
    s.box(310, 150, 220, 90, "Chunk and index", "offline, in advance", "navy")
    s.box(580, 150, 220, 90, "Retrieve", "per question", "navy")
    s.box(850, 150, 290, 90, "Answer with citations", "or refuse, on evidence", "light")
    s.arrow(260, 195, 310, 195)
    s.arrow(530, 195, 580, 195)
    s.arrow(800, 195, 850, 195)
    s.box(580, 300, 220, 70, "Golden set", "grades every stage", "amber")
    s.arrow(690, 300, 690, 240)
    s.note(40, 400, "Generation is the visible stage. Retrieval quality decides whether generation has anything true to say.")
    s.save("rag-pipeline.svg")


def chunking():
    s = SVG(1180, 460, "Chunking strategies", "The same document, three ways of cutting it, three different systems")
    s.box(40, 140, 330, 90, "Whole documents", "naive: 420 words of context", "light")
    s.box(430, 140, 330, 90, "Paragraph packing", "about 90 words per chunk", "navy")
    s.box(820, 140, 320, 90, "Sections", "one chunk per heading", "navy")
    s.box(430, 300, 330, 80, "Parent expansion", "retrieve small, answer from the section", "amber")
    s.arrow(595, 230, 595, 300)
    s.note(40, 430, "Lesson 03 and 04 measure all three on the golden set: facts found, and words of context paid for them.")
    s.save("chunking.svg")


def hybrid():
    s = SVG(1180, 480, "Hybrid search and rank fusion", "Two retrievers that fail differently, combined by rank")
    s.box(40, 200, 220, 90, "Question", "", "light")
    s.box(340, 130, 260, 80, "BM25", "exact words, numbers", "navy")
    s.box(340, 260, 260, 80, "Vector stand-in", "morphology, overlap", "navy")
    s.box(680, 195, 220, 90, "Rank fusion", "RRF: ranks, not scores", "amber")
    s.box(960, 195, 180, 90, "Top chunks", "", "light")
    s.arrow(260, 230, 340, 175)
    s.arrow(260, 260, 340, 295)
    s.arrow(600, 175, 680, 220)
    s.arrow(600, 295, 680, 255)
    s.arrow(900, 240, 960, 240)
    s.note(40, 450, "On this corpus the hybrid's win is the worst case: it never scores zero on a question where a single leg does.")
    s.save("hybrid-fusion.svg")


def evaluation_loop():
    s = SVG(1180, 460, "The evaluation loop", "Change one thing, rerun the same questions, keep the change only if the numbers move")
    s.box(40, 170, 230, 90, "Golden set", "32 fixed questions", "light")
    s.box(330, 170, 230, 90, "Run the system", "same code path as users", "navy")
    s.box(620, 170, 230, 90, "Score", "recall, facts, refusals", "navy")
    s.box(910, 170, 230, 90, "Decide", "keep, revert, or fix", "amber")
    s.arrow(270, 215, 330, 215)
    s.arrow(560, 215, 620, 215)
    s.arrow(850, 215, 910, 215)
    s.arrow(1025, 260, 1025, 330)
    s.arrow(1025, 330, 445, 330, "change one thing")
    s.arrow(445, 330, 445, 260)
    s.note(40, 420, "Lessons 18 to 20 build this loop. Every earlier lesson's claim was produced inside it.")
    s.save("evaluation-loop.svg")


def agent_loop():
    s = SVG(1180, 500, "The agentic retrieval loop", "Retrieval as a tool: the agent decides, grades, and tries again")
    s.box(40, 190, 210, 90, "Question", "", "light")
    s.box(310, 190, 230, 90, "Decide", "search, or answer directly", "navy")
    s.box(600, 190, 230, 90, "Search tool", "hybrid, filtered, cited", "navy")
    s.box(890, 120, 250, 80, "Grade the evidence", "coverage, facts, freshness", "amber")
    s.box(890, 300, 250, 80, "Answer or refuse", "with citations", "light")
    s.arrow(250, 235, 310, 235)
    s.arrow(540, 235, 600, 235)
    s.arrow(830, 220, 890, 165)
    s.arrow(1015, 200, 1015, 300)
    s.arrow(890, 340, 715, 340, "grade fails: widen or rewrite, once")
    s.arrow(715, 340, 715, 280)
    s.note(40, 470, "Lessons 21 to 24 build this loop piece by piece, and measure what each piece adds.")
    s.save("agent-loop.svg")


def capstone_flow():
    s = SVG(1180, 420, "The capstone flow", "Spec first, gates fixed, then build, then grade")
    s.box(40, 150, 240, 90, "Spec and gates", "Lesson 28", "amber")
    s.box(330, 150, 240, 90, "Build the system", "Lesson 29", "navy")
    s.box(620, 150, 240, 90, "Evaluate and harden", "Lesson 30", "navy")
    s.box(910, 150, 230, 90, "Ship and showcase", "Lesson 31", "light")
    s.arrow(280, 195, 330, 195)
    s.arrow(570, 195, 620, 195)
    s.arrow(860, 195, 910, 195)
    s.note(40, 300, "Gates: recall at 5 at least 0.95, fact recall at 5 at least 0.95, citations 100 percent,")
    s.note(40, 330, "refusals at least 5 of 6 with zero false refusals, zero restricted leaks.")
    s.note(40, 390, "The reference build's measured results are printed by Lesson 30's harness, not asserted here.")
    s.save("capstone-flow.svg")


if __name__ == "__main__":
    course_map()
    rag_pipeline()
    chunking()
    hybrid()
    evaluation_loop()
    agent_loop()
    capstone_flow()
