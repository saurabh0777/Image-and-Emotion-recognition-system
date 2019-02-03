import webbrowser as wb
import wikipedia
import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")


chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

def get_error_txt(err_text):
    wikitxt = err_text
    print('You said:\n' + err_text)
    f_text = 'https://www.google.co.in/search?q=' +  err_text
    wb.get(chrome_path).open(f_text)

    from gensim.summarization.summarizer import summarize
    from gensim.summarization import keywords
    import requests
    from bs4 import BeautifulSoup

    try:
        # For Python 3.0 and later
        from urllib.request import urlopen
    except ImportError:
        # Fall back to Python 2's urllib2
        from urllib3 import urlopen

    def get_only_text(url):
        try:
            page = urlopen(url)
            soup = BeautifulSoup(page, "lxml")
            text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
            return soup.title.text, text
        except:
            pass

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    r = requests.get(f_text)

    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.find('cite').text)
    #print(soup.find('wiki').text)
    url = soup.find('cite').text
    text = get_only_text(url)

    print(text)
    if 'wiki' in url:  # what happens when wkp keyword is recognized
        try:
            wkpres = wikipedia.summary(wikitxt, sentences=2)
            print("wkpress "+ wkpres)
        
            try:
        
                print('\n' + str(wkpres) + '\n')
                speak.Speak(wkpres)

            except UnicodeEncodeError:
                speak.Speak(wkpres)
        
        except wikipedia.exceptions.DisambiguationError as e:
            print(e.options)
            speak.Speak("Too many results for this keyword. Please be more specific and try again")
            pass
        
        except wikipedia.exceptions.PageError as e:
            try:
                txt = text[:150]
                txt2 = ''.join(c for c in txt if c not in '1234567890[],?:!/;|\n')
                txtt2 = txt2.replace("\n", "").replace("Wikipedia", "")
                speak.Speak(txtt2)
            except wikipedia.exceptions.PageError as e:
                print('The page does not exist')
                speak.Speak('The page does not exist')
                pass
    else:
        #print('Summary:')
        txt1 = ''.join(c for c in text if c not in '1234567890[],?:!/;|\n')
        txtt1 = txt1.replace("\n", "").replace("Wikipedia","")
        print(summarize(str(txtt1), ratio=0.01))
        speak.Speak(txtt1[:150])
        pass
