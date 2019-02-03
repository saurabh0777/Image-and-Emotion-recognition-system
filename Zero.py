import speech_recognition as sr
import webbrowser
import wolframalpha
import wikipedia
import time
import os
import pyvona
import pyperclip
import win32com.client
import voice.error_route as err

app_id = "P2496K-JA3U2QUWL4"
cl = wolframalpha.Client(app_id)                                                        #api for wolfram alpha
v = win32com.client.Dispatch("SAPI.SpVoice")

r = sr.Recognizer()                                                                         #starting the speech_recognition recognizer
r.pause_threshold = 0.7                                                                     #it works with 1.2 as well
r.energy_threshold = 4000

shell = win32com.client.Dispatch("WScript.Shell")                                           #to handle keyboard events
v.speak('Hello, I am Zero & I am a work in Progress of being Maxis first Artificial Intelligence Synthetic Assistant, Please ask a question or say "Alpha" for the Quick Commands...')
#print("Please ask a question or say 'Keyword' for the Commands'...")

#List of Available Commands

keywd = 'Alpha'
google = 'search for'
acad = 'academic search'
sc = 'deep search'
wkp = 'wiki page for'
rdds = 'read this text'
sav = 'save this text'
bkmk = 'bookmark this page'
vid = 'video for'
wtis = 'what is'
wtar = 'what are'
whis = 'who is'
whws = 'who was'
when = 'when'
where = 'where'
how = 'how'
paint = 'open paint'
lsp = 'sleep'
lsc = 'wake up'
stoplst = 'stop listening'

while True:                                                                                 #The main loop

    with sr.Microphone() as source:

        try:

            #audio = r.listen(source, timeout = None)                                        #instantiating the Microphone, (timeout = None) can be an option
            audio = r.listen(source)
            message = str(r.recognize_google(audio))
            print('You said: ' + message)
            v.speak('You said: ' + message)

            if google in message:                                                           #what happens when google keyword is recognized

                words = message.split()
                del words[0:2]
                st = ' '.join(words)
                print('Google Results for: '+str(st))
                url='http://google.com/search?q='+st
                webbrowser.open(url)
                v.speak('Google Results for: '+str(st))

            elif acad in message:                                                           #what happens when acad keyword is recognized

                words = message.split()
                del words[0:2]
                st = ' '.join(words)
                print('Academic Results for: '+str(st))
                url='https://scholar.google.ro/scholar?q='+st
                webbrowser.open(url)
                v.speak('Academic Results for: '+str(st))

            elif wkp in message:                                                            #what happens when wkp keyword is recognized

                try:

                    words = message.split()
                    del words[0:3]
                    st = ' '.join(words)
                    wkpres = wikipedia.summary(st, sentences=2)

                    try:

                        print('\n' + str(wkpres) + '\n')
                        v.speak(wkpres)

                    except UnicodeEncodeError:
                        try:
                            err.get_error_txt(message)
                        except:
                            v.speak(wkpres)

                except wikipedia.exceptions.DisambiguationError as e:
                    try:
                        err.get_error_txt(message)
                    except:
                        print (e.options)
                        v.speak("Too many results for this keyword. Please be more specific and try again")
                        continue

                except wikipedia.exceptions.PageError as e:
                    try:
                        err.get_error_txt(message)
                    except:
                        print('The page does not exist')
                        v.speak('The page does not exist')
                        continue

            elif sc in message:                                                             #what happens when sc keyword is recognized

                try:
                    words = message.split()
                    del words[0:1]
                    st = ' '.join(words)
                    scq = cl.query(st)
                    sca = next(scq.results).text
                    print('The answer is: '+str(sca))
                    #url='http://www.wolframalpha.com/input/?i='+st
                    #webbrowser.open(url)
                    v.speak('The answer is: '+str(sca))

                except StopIteration:
                    print('Your question is ambiguous. Please try again!')
                    v.speak('Your question is ambiguous. Please try again!')

                else:
                    print('No query provided')

            elif paint in message:                                                          #what happens when paint keyword is recognized
                os.system('mspaint')

            elif rdds in message:                                                           #what happens when rdds keyword is recognized
                print("Reading your text")
                v.speak(pyperclip.paste())

            elif sav in message:                                                            #what happens when sav keyword is recognized
                with open('path to your text file', 'a') as f:
                    f.write(pyperclip.paste())
                print("Saving your text to file")
                v.speak("Saving your text to file")

            elif bkmk in message:                                                           #what happens when bkmk keyword is recognized
                shell.SendKeys("^d")
                v.speak("Page bookmarked")

            elif keywd in message:                                                          #what happens when keywd keyword is recognized

                print('')
                print('Say ' + google + ' to return a Google search')
                print('Say ' + acad + ' to return a Google Scholar search')
                print('Say ' + sc + ' to return a Wolfram Alpha query')
                print('Say ' + wkp + ' to return a Wikipedia page')
                #print('Say ' + book + ' to return an Amazon book search')
                print('Say ' + rdds + ' to read the text you have highlighted and Ctrl+C (copied to clipboard)')
                print('Say ' + sav + ' to save the text you have highlighted and Ctrl+C-ed (copied to clipboard) to a file')
                print('Say ' + bkmk + ' to bookmark the page your are currently reading in your browser')
                print('Say ' + vid + ' to return video results for your query')
                print('For more general questions, ask them naturally and I will do my best to find a good answer')
                print('Say ' + stoplst + ' to shut down')
                print('')

            elif vid in message:                                                            #what happens when vid keyword is recognized

                words = message.split()
                del words[0:2]
                st = ' '.join(words)
                print('Video Results for: '+str(st))
                url='https://www.youtube.com/results?search_query='+st
                webbrowser.open(url)
                v.speak('Video Results for: '+str(st))

            elif wtis in message:                                                           #what happens when wtis keyword is recognized
                try:
                    scq = cl.query(message)
                    print(scq)
                    xyr = ' '
                    xyr = str(scq)
                    print(xyr[1:19])
                    if xyr[1:19] == "'@success': 'true'" :
                       print('im in')
                       sca = next(scq.results).text
                       print('\nThe answer is yes yes: '+str(sca)+'\n')
                       v.speak('The answer is: '+str(sca))
                    else:
                        try:
                            err.get_error_txt(message)
                        except:
                            pass

                except UnicodeEncodeError:
                    try:
                        err.get_error_txt(message)
                    except:
                        v.speak('The answer is: '+str(sca))
                        pass

                except StopIteration:

                    words = message.split()
                    del words[0:2]
                    st = ' '.join(words)
                    print('Google Results for: '+str(st))
                    url='http://google.com/search?q='+st
                    webbrowser.open(url)
                    v.speak('Google Results for: '+str(st))

            elif wtar in message:                                                           #what happens when wtar keyword is recognized

                try:
                    scq = cl.query(message)
                    print(scq)
                    xyr = ' '
                    xyr = str(scq)
                    print(xyr[1:19])
                    if xyr[1:19] == "'@success': 'true'" :
                       print('im in')
                       sca = next(scq.results).text
                       print('\nThe answer is yes yes: '+str(sca)+'\n')
                       v.speak('The answer is: '+str(sca))
                    else:
                        try:
                            err.get_error_txt(message)
                        except:
                            pass

                except UnicodeEncodeError:
                    try:
                        err.get_error_txt(message)
                    except:
                        v.speak('The answer is: '+str(sca))

                except StopIteration:

                    words = message.split()
                    del words[0:2]
                    st = ' '.join(words)
                    print('Google Results for: '+str(st))
                    url='http://google.com/search?q='+st
                    webbrowser.open(url)
                    v.speak('Google Results for: '+str(st))

            elif whis in message:                                                           #what happens when whis keyword is recognized
                try:
                    scq = cl.query(message)
                    print(scq)
                    xyr = ' '
                    xyr = str(scq)
                    print(xyr[1:19])
                    if xyr[1:19] == "'@success': 'true'" :
                       print('im in')
                       sca = next(scq.results).text
                       if sca == "(data not available)":
                           err.get_error_txt(message)
                       else:
                           print('\nThe answer is yes : '+str(sca)+'\n')
                           v.speak('The answer is: '+str(sca))
                    else:
                        try:
                            err.get_error_txt(message)
                        except:
                            pass
                except StopIteration:

                    try:

                        words = message.split()
                        del words[0:2]
                        st = ' '.join(words)
                        wkpres = wikipedia.summary(st, sentences=2)
                        print('\n' + str(wkpres) + '\n')
                        v.speak(wkpres)

                    except UnicodeEncodeError:
                        try:
                            err.get_error_txt(message)
                        except:
                            v.speak(wkpres)

                    except:

                        words = message.split()
                        del words[0:2]
                        st = ' '.join(words)
                        print('Google Results (last exception) for: '+str(st))
                        url='http://google.com/search?q='+st
                        webbrowser.open(url)
                        v.speak('Google Results for: '+str(st))

            elif whws in message:                                                           #what happens when whws keyword is recognized

                try:
                    scq = cl.query(message)
                    print(scq)
                    xyr = ' '
                    xyr = str(scq)
                    print(xyr[1:19])
                    if xyr[1:19] == "'@success': 'true'" :
                       print('im in')
                       sca = next(scq.results).text
                       print('\nThe answer is yes yes: '+str(sca)+'\n')
                       v.speak('The answer is: '+str(sca))
                    else:
                        try:
                            err.get_error_txt(message)
                        except:
                            pass

                except StopIteration:

                    try:

                        words = message.split()
                        del words[0:2]
                        st = ' '.join(words)
                        wkpres = wikipedia.summary(st, sentences=2)
                        print('\n' + str(wkpres) + '\n')
                        v.speak(wkpres)

                    except UnicodeEncodeError:
                        try:
                            err.get_error_txt(message)
                        except:
                            v.speak(wkpres)

                    except:

                        words = message.split()
                        del words[0:2]
                        st = ' '.join(words)
                        print('Google Results for: '+str(st))
                        url='http://google.com/search?q='+st
                        webbrowser.open(url)
                        v.speak('Google Results for: '+str(st))

            elif when in message:                                                         #what happens when 'when' keyword is recognized

                try:
                    scq = cl.query(message)
                    print(scq)
                    xyr = ' '
                    xyr = str(scq)
                    print(xyr[1:19])
                    if xyr[1:19] == "'@success': 'true'" :
                       print('im in')
                       sca = next(scq.results).text
                       print('\nThe answer is yes yes: '+str(sca)+'\n')
                       v.speak('The answer is: '+str(sca))
                    else:
                        try:
                            err.get_error_txt(message)
                        except:
                            pass

                except UnicodeEncodeError:
                    try:
                        err.get_error_txt(message)
                    except:
                        v.speak('The answer is: '+str(sca))

                except:

                    print('Google Results for: '+str(message))
                    url='http://google.com/search?q='+str(message)
                    webbrowser.open(url)
                    v.speak('Google Results for: '+str(message))

            elif where in message:                                                        #what happens when 'where' keyword is recognized

                try:
                    scq = cl.query(message)
                    print(scq)
                    xyr = ' '
                    xyr = str(scq)
                    print(xyr[1:19])
                    if xyr[1:19] == "'@success': 'true'" :
                       print('im in')
                       sca = next(scq.results).text
                       print('\nThe answer is yes yes: '+str(sca)+'\n')
                       v.speak('The answer is: '+str(sca))
                    else:
                        try:
                            err.get_error_txt(message)
                        except:
                            pass

                except UnicodeEncodeError:
                    try:
                        err.get_error_txt(message)
                    except:
                        v.speak('The answer is: '+str(sca))

                except:

                    print('Google Results for: '+str(message))
                    url='http://google.com/search?q='+str(message)
                    webbrowser.open(url)
                    v.speak('Google Results for: '+str(message))

            elif how in message:                                                          #what happens when 'how' keyword is recognized

                try:
                    scq = cl.query(message)
                    print(scq)
                    xyr = ' '
                    xyr = str(scq)
                    print(xyr[1:19])
                    if xyr[1:19] == "'@success': 'true'" :
                       print('im in')
                       sca = next(scq.results).text
                       print('\nThe answer is yes yes: '+str(sca)+'\n')
                       v.speak('The answer is: '+str(sca))
                    else:
                        try:
                            err.get_error_txt(message)
                        except:
                            pass

                except UnicodeEncodeError:
                    try:
                        err.get_error_txt(message)
                    except:
                        v.speak('The answer is: '+str(sca))

                except:

                    print('Google Results for: '+str(message))
                    url='http://google.com/search?q='+str(message)
                    webbrowser.open(url)
                    v.speak('Google Results for: '+str(message))

            elif stoplst in message:                                                        #what happens when stoplst keyword is recognized
                v.speak("I am shutting down")
                print("Shutting down...")
                break

            elif lsp in message:

                v.speak('Listening is paused')
                print('Listening is paused')
                r2 = sr.Recognizer()
                #r2.pause_threshold = 0.7
                r2.energy_threshold = 4000

                while True:

                    with sr.Microphone() as source2:

                        try:

                            #audio2 = r2.listen(source2, timeout = None)
                            audio2 = r2.listen(source2)
                            message2 = r.recognize_google(audio2)

                            if lsc in message2:
                                v.speak('I am listening')
                                break

                            else:
                                continue

                        except sr.UnknownValueError:
                            print("Listening is paused. Say wake up when you're ready...")

                        except sr.RequestError:
                            v.speak("I'm sorry, I couldn't reach google")
                            print("I'm sorry, I couldn't reach google")


            else:
                try:
                    err.get_error_txt(message)
                except:
                    #v.speak('The answer is: ' + str(message))
                    pass

        except sr.UnknownValueError:
            print("For a list of commands, say: 'alpha'...")

        except sr.RequestError:
            v.speak("I'm sorry, I couldn't reach google")
            print("I'm sorry, I couldn't reach google")

    time.sleep(0.3)
