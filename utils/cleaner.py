def clean_tags(html):
    html = str(html).replace("<h1>", "").replace("</h1>", "")
    html = str(html).replace("<h2>", "").replace("</h2>", "")
    html = str(html).replace("<h3>", "").replace("</h3>", "")
    html = str(html).replace("<h4>", "").replace("</h4>", "")
    html = str(html).replace("<h5>", "").replace("</h5>", "")
    html = str(html).replace("<h6>", "").replace("</h6>", "")
    html = str(html).replace("<p>", "").replace("</p>", "")
    html = str(html).replace("<body>", "").replace("</body>", "")

    return html