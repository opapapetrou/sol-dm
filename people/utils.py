# utils.py
import json
from html import escape


order = ["PUBRecent_publications", "PUBJournals", "PUBConferences", "PUBOther"]

def is_truthy(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() == "true"
    return False


def createPubList(data,filter_text, affiliation=None):
    html = []
    for sec in order:
        pubs = data.get(sec, [])
        section_title = sec.replace("PUB", "").replace("_", " ").capitalize()
        html.append(f"<h2>{escape(section_title)}</h2>")
        html.append("<ul>")
        for p in pubs:
            title = p.get("title", "")
            # Check if filter_text is NOT in the title
            if filter_text.strip() and filter_text not in title:
                continue
            if affiliation is None or p.get("affiliation","notgiven") not in affiliation:
                continue
            hl = is_truthy(p.get("highlight"))
            cls = ' class="highlight"' if hl else ""
            html.append(f"<li{cls}>")
            html.append(p.get("title", ""))  # contains <b>…</b>, so keep as-is
            if p.get("url"):
                html.append(f' <a href="{escape(p["url"])}" target="_blank" rel="noopener">(Link)</a>')
            if p.get("note"):
                html.append(f'<div class="pub-note">{p["note"]}</div>')
            html.append("</li>")
        html.append("</ul>")
    html.append("<br><br>")
    html.append("Copyright Notice: The documents distributed by this server have been provided by the contributing authors as a means to ensure timely dissemination of scholarly and technical work on a noncommercial basis. Copyright and all rights therein are maintained by the authors or by other copyright holders, notwithstanding that they have offered their works here electronically. It is understood that all persons copying this information will adhere to the terms and constraints invoked by each author's copyright. These works may not be reposted without the explicit permission of the copyright holder.")
    return html
