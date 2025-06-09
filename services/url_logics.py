from urllib.parse import urlparse
import hashlib

def url_logic(url):
    try:
        valid_url = urlparse(url) 
        url_scheme = True if valid_url.scheme in ["https","http"] else False
        if all([url_scheme,valid_url.netloc]):
            sha256 = hashlib.sha256()
            sha256.update(url.encode('utf-8'))
            short_url = sha256.hexdigest()
        return short_url[:8]
    except AttributeError:
        return "not valid url"
    
