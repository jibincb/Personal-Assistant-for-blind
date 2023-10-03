import threading
import concurrent.futures
import speech_recognition as sr
import pyttsx3
from .face_recogn import face_regn
from .objdect import obj_dect
from .chatgpt import send_message


def listen_for_wake_word():
    speak('The buddy program is running....')
    speak("Say hey buddy to activate me")
    r = sr.Recognizer()
    with sr.Microphone() as source:

        print("Listening for wake word...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        wake_word = r.recognize_google(audio)
        print("Wake word:", wake_word)
        if "buddy" in wake_word.lower():
            speak("Hi buddy, How can I help you?")
            return True
        # if wake_word.lower() == "ok jackie":
        #     return True
        else:
            print("Did not recognize the wake word.")
            return False
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return False
    except sr.RequestError as e:
        print("Sorry, an error occurred. {0}".format(e))
        return False


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
    except sr.RequestError as e:
        print("Sorry, an error occurred. {0}".format(e))


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def process_query(query):
    if query is not None:
        # if "hi" in query:
        #     speak("hi, How can I help you?")
        if "who is this" in query:
            # thread = threading.Thread(target=face_regn)
            # thread.start()
            executor = concurrent.futures.ThreadPoolExecutor()
            future = executor.submit(face_regn)
            face = future.result()
            if face is not None:
                speak("It look like " + face)
            else:
                speak("I think its a stranger")
        elif "find" in query and "object" in query:
            speak("what object do you need to find?")

            def objfind():
                obj = str(listen())
                if obj is None:
                    speak("Sorry I couldn't understand the object please repeat the object name again")
                    objfind()
                else:
                    speak("did you say " + obj + " ?")
                    ans = listen()
                    if ans is not None:
                        if 'yes' in ans:
                            print(obj, "is finding")
                            obj_dect(obj)
                        else:
                            print(ans)
                            speak("Sorry I couldn't understand the object please repeat the object name again")
                            objfind()
                    else:
                        print(ans)
                        speak("Sorry I couldn't understand the object please repeat the object name again")
                        objfind()

            objfind()

        # elif "what" in query and "time" in query:
        #     speak("current time")
        elif "goodbye" in query:
            speak("Goodbye! Have a nice day.")
            return 1
        else:
            user_message = query
            bot_message = send_message(user_message)
            speak(bot_message)
    else:
        speak('sorry, I could not understand. Please repeat it again')
# Wait for the wake word before starting the assistant
# while True:
#     if listen_for_wake_word():
#         break

# # The assistant is now active
# while True:
#     query = listen()
#     process_query(query)
