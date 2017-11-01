import requests, bs4, os, sys
from slugify import slugify


try:
    user = sys.argv[1]
    password = sys.argv[2]
except IndexError:
    sys.stdout.write('\033[91mERROR: You have to specify a username and a password \033[0m')
    sys.exit()

try:
    directory = sys.argv[3]
except IndexError:
    directory = './books'

basic_url = 'https://www.packtpub.com/'

payload = {
    'email': user,
    'password': password,
    'op': 'Login',
    'form_build_id': '',
    'form_id': 'packt_user_login_form'
}

headers = requests.utils.default_headers()
headers.update(
    {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/50.0.2661.102 Safari/537.36',
    'Accept': 'text/html'
    }
)

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

with requests.Session() as s:

    sys.stdout.write('Getting form version id...\n\r')
    sys.stdout.flush()
    i = s.get(basic_url, headers=headers)
    page = bs4.BeautifulSoup(i.text, 'html.parser')
    form_id = page.select('input[name="form_build_id"]')
    payload['form_build_id'] = form_id[0].get('value')

    sys.stdout.write('Logging...\n\r')
    sys.stdout.flush()
    p = s.post(basic_url, data=payload, headers=headers)
    
    sys.stdout.write('Getting books list...\n\r')
    sys.stdout.flush()
    r = s.get(basic_url+'/account/my-ebooks', headers=headers)

    soup = bs4.BeautifulSoup(r.text, 'html.parser')

    ebooks = soup.select('#product-account-list > div.product-line > div.product-buttons-line.toggle > div:nth-of-type(2) > a:nth-of-type(1)')
    ebooks_titles = soup.select('#product-account-list > div.product-line  div.title')
    numEbooks = len(ebooks)
    
    try: 
        os.makedirs(directory)
    except OSError:
        if not os.path.isdir(directory):
            raise

    for i in range(numEbooks):
        name = slugify(ebooks_titles[i].getText().strip(), separator="_")
        sys.stdout.write('Downloading '+name+'...\n\r')
        sys.stdout.flush()
        url_ebook = ebooks[i].get('href')
        ebook_request = s.get(basic_url+url_ebook, headers=headers)
        ebookFile = open(directory+'/'+name+'.pdf', 'wb')
        total_length = int(ebook_request.headers.get('content-length'))/1024
        counter = 0
        for chunk in ebook_request.iter_content(1024):
            ebookFile.write(chunk)
            progress(counter, total_length)
            counter = counter +1
        ebookFile.close()
        sys.stdout.write('\n\r')
        


sys.stdout.write('All books downloaded')