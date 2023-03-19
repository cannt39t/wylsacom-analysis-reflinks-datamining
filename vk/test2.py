import re

regex = r"\bhttps?://\S+\?(?:(?:amp;)?|\b)(?:ref|referrer|referral|promo|promocode|coupon|code|invite|invited_by|friend|source|partner|utm_\w+)=\S+\b"

def ref_or_not(link):
    if 'ref' in link:
        return True
    matches = re.findall(regex, link)
    if len(matches) != 0:
        return True
    return False


if __name__ == '__main__':
    text = "This is a sample text with a referral link https://example.com/?ref=1234567890 and another referral link http://example2.com/?ref=abcdef"
    ref_or_not(text)