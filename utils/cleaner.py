import bleach

def clean_content(content):
    allowed_tags = ['b', 'strong', 'i', 'em', 'u', 'ins', 's', 'strike', 'del', 'span', 'tg-spoiler', 'a', 'code', 'pre']
    allowed_attrs = {
        'a': ['href'],
        'span': ['class'],
    }
    return bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, strip=True)