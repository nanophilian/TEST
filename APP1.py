import requests
from bs4 import BeautifulSoup
import webbrowser
import pyttsx3
import threading
from transformers import pipeline
from langdetect import detect
from tkinter import ttk
from tkinter import messagebox
from googletrans import Translator

def get_article_text_and_summary(event):
    # 선택된 항목의 텍스트 가져오기
    selection = event.widget.curselection()

    if selection:
        index = selection[0]
        text = "["
        text += event.widget.get(index)
        text += "]"

        # Text Box 1, 2에 텍스트 설정
        text_box1.config(state=NORMAL)
        text_box1.delete(1.0, END)

        text_box2.config(state=NORMAL)
        text_box2.delete(1.0, END)

        # 신문 기사 내용 읽어오기
        url_ = url_mapping[index]
        # requests를 이용해 웹 페이지 가져오기
        response_ = requests.get(url_)
        # BeautifulSoup을 이용해 HTML 파싱
        soup_ = BeautifulSoup(response_.content, 'html.parser')
        # 기사 내용 읽어오기
        article_text = soup_.find('article', id='dic_area').get_text(separator=' ', strip=True)

        text += '\n' # 제목
        text += article_text # 내용

        text_box1.insert(END, text)
        text_box1.config(state=DISABLED)

        # Text Box 1의 내용을 요약 후 그 내용을 Text Box 2로 복사

        text_box2.insert(END, "[기사 내용 요약중]")
        text_box2.config(state=DISABLED)

        if detect(text) == "en":
            # 요약 파이프라인 로드
            summarizer = pipeline("summarization")

            # 텍스트 요약
            summary = summarizer(text, max_length=1000, min_length=30, do_sample=False)
            # summary = type(summary)
            summary = summary[0]['summary_text'][1:]

            text_box2.config(state=NORMAL)
            text_box2.delete(1.0, END)

            text_box2.insert(END, summary)
            text_box2.config(state=DISABLED)
        else:
            # 요약 파이프라인 로드
            # 한국어 기사 내용을 요약하기 위한 모델
            summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

            # 텍스트 요약
            summary = summarizer(text, max_length=10000, min_length=30, do_sample=False)
            # summary = type(summary)
            summary = summary[0]['summary_text'][1:]

            text_box2.config(state=NORMAL)
            text_box2.delete(1.0, END)

            text_box2.insert(END, summary)
            text_box2.config(state=DISABLED)

def get_text():

    button1.config(state=DISABLED)
    button2.config(state=DISABLED)
    button3.config(state=DISABLED)
    button4.config(state=DISABLED)
    button5.config(state=DISABLED)
    button6.config(state=DISABLED)
    button7.config(state=DISABLED)
    button8.config(state=DISABLED)

    # 네이버 뉴스 속보 페이지 URL
    url = "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001"
    # requests를 이용해 웹 페이지 가져오기
    response = requests.get(url)
    # BeautifulSoup을 이용해 HTML 파싱
    soup = BeautifulSoup(response.content, 'html.parser')
    # 뉴스 제목이 포함된 HTML 요소 찾기
    news_headlines = soup.find_all('a', class_="nclicks(fls.list)")

    list_box_for_headlines.delete(0, END)
    url_mapping.clear()

    for index, headline in enumerate(news_headlines[:20]):  # 첫 10개의 제목만 출력
        if len(headline.text.strip()) != 0:
            list_box_for_headlines.insert(END, headline.text.strip())
            url_mapping.append(headline['href'])

    button1.config(state=NORMAL)
    button2.config(state=NORMAL)
    button3.config(state=NORMAL)
    button4.config(state=NORMAL)
    button5.config(state=NORMAL)
    button6.config(state=NORMAL)
    button7.config(state=NORMAL)
    button8.config(state=NORMAL)

def openArticle(event):
    # 선택된 항목의 인덱스를 가져옴
    widget = event.widget
    selection = widget.curselection()
    index = selection[0]

    # 해당 인덱스의 URL을 딕셔너리에서 찾음
    url = url_mapping[index]


    if url:
        webbrowser.open(url)  # 기본 웹 브라우저에서 URL 열기

def speak():

    button1.config(state=DISABLED)
    button2.config(state=DISABLED)
    button3.config(state=DISABLED)
    button4.config(state=DISABLED)
    button5.config(state=DISABLED)
    button6.config(state=DISABLED)
    button7.config(state=DISABLED)
    button8.config(state=DISABLED)

    for index in range(list_box_for_headlines.size()):
        text = list_box_for_headlines.get(index)
        engine.say(text)
        engine.runAndWait()

    button1.config(state=NORMAL)
    button2.config(state=NORMAL)
    button3.config(state=NORMAL)
    button4.config(state=NORMAL)
    button5.config(state=NORMAL)
    button6.config(state=NORMAL)
    button7.config(state=NORMAL)
    button8.config(state=NORMAL)

def speak_article():

    # text_box1의 전체 텍스트를 가져옵니다.
    text_content = text_box1.get("1.0", "end-1c")

    if len(text_content) != 0:
        button1.config(state=DISABLED)
        button2.config(state=DISABLED)
        button3.config(state=DISABLED)
        button4.config(state=DISABLED)
        button5.config(state=DISABLED)
        button6.config(state=DISABLED)
        button7.config(state=DISABLED)
        button8.config(state=DISABLED)

        engine.say(text_content)
        engine.runAndWait()

        button1.config(state=NORMAL)
        button2.config(state=NORMAL)
        button3.config(state=NORMAL)
        button4.config(state=NORMAL)
        button5.config(state=NORMAL)
        button6.config(state=NORMAL)
        button7.config(state=NORMAL)
        button8.config(state=NORMAL)

def speak_summary():

    # text_box1의 전체 텍스트를 가져옵니다.
    text_content = text_box2.get("1.0", "end-1c")

    if len(text_content) != 0 and text_content != "[기사 내용 요약중]":
        button1.config(state=DISABLED)
        button2.config(state=DISABLED)
        button3.config(state=DISABLED)
        button4.config(state=DISABLED)
        button5.config(state=DISABLED)
        button6.config(state=DISABLED)
        button7.config(state=DISABLED)
        button8.config(state=DISABLED)

        engine.say(text_content)
        engine.runAndWait()

        button1.config(state=NORMAL)
        button2.config(state=NORMAL)
        button3.config(state=NORMAL)
        button4.config(state=NORMAL)
        button5.config(state=NORMAL)
        button6.config(state=NORMAL)
        button7.config(state=NORMAL)
        button8.config(state=NORMAL)

def get_text_in_thread():
    # 별도의 스레드에서 speak 함수를 실행
    get_text_thread = threading.Thread(target=get_text)
    get_text_thread.start()

def speak_title_in_thread():
    # 별도의 스레드에서 speak 함수를 실행
    speak_thread = threading.Thread(target=speak)
    speak_thread.start()

def speak_article_in_thread():
    # 별도의 스레드에서 speak 함수를 실행
    speak_thread = threading.Thread(target=speak_article)
    speak_thread.start()

def speak_summary_in_thread():
    # 별도의 스레드에서 speak 함수를 실행
    speak_thread = threading.Thread(target=speak_summary)
    speak_thread.start()

def get_article_text_and_summary_in_thread(event):
    get_article_text_and_summary_thread = threading.Thread(target=get_article_text_and_summary, args=(event,))
    get_article_text_and_summary_thread.start()

def get_open_tts_settings_in_thread():
    open_tts_settings_thread = threading.Thread(target=open_tts_settings)
    open_tts_settings_thread.start()

def search_in_thread():
    search_thread = threading.Thread(target=search)
    search_thread.start()

def translation_in_thread():
    translate_thread = threading.Thread(target=translate)
    translate_thread.start()

def STT_in_thread():
    STT_thread = threading.Thread(target=STT)
    STT_thread.start()

def STT():
    import speech_recognition as sr

    r = sr.Recognizer()
    with sr.Microphone() as source:
        # new_text_box 위젯의 상태를 NORMAL로 변경하여 편집 가능하게 만듭니다
        new_text_box.config(state=NORMAL)

        # new_text_box 내용을 "음성 인식 중 ..."으로 설정
        new_text_box.delete(1.0, END)  # 기존 텍스트를 삭제
        new_text_box.insert(END, "음성 인식 중 ...")

        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ko-KR")

            new_text_box.delete(1.0, END)  # 기존 텍스트를 삭제
            new_text_box.insert(END, text)
            new_text_box.config(state=DISABLED)

            text = text.replace(" ", "")

            if text == "속보가져오기":
                get_text_in_thread()
            elif text == "뉴스제목읽기":
                speak_title_in_thread()
            elif text == "기사내용읽기":
                speak_article_in_thread()
            elif text == "기사요약읽기":
                speak_summary_in_thread()
            elif text == "TTS설정":
                get_open_tts_settings_in_thread()
            elif text == "텍스트검색":
                search_in_thread()
            elif text == "번역":
                translation_in_thread()

        except:
            new_text_box.delete(1.0, END)  # 기존 텍스트를 삭제
            new_text_box.insert(END, "음성을 인식하지 못했습니다.")
            new_text_box.config(state=DISABLED)

def open_tts_settings():
    # 새 창 생성
    tts_settings_window = Toplevel(root)
    tts_settings_window.geometry("400x250")
    tts_settings_window.title("TTS 설정")

    tts_settings_window.grab_set()

    # TTS 속도를 조절하는 슬라이더
    Label(tts_settings_window, text="TTS 속도:").pack()

    speed_slider = Scale(tts_settings_window, from_=100, to=300, orient='horizontal', length=250)
    speed_slider.set(engine.getProperty('rate'))
    speed_slider.pack()

    # TTS 음량을 조절하는 슬라이더
    Label(tts_settings_window, text="TTS 음량:").pack()

    volume_slider = Scale(tts_settings_window, from_=0.0, to=1.0, orient='horizontal', length=250)
    volume_slider.set(engine.getProperty('volume'))
    volume_slider.pack()

    # 언어 선택
    Label(tts_settings_window, text="언어:").pack()

    # 현재 음성 가져오기
    current_voice = engine.getProperty('voice')
    # 사용 가능한 모든 음성 가져오기
    voices = engine.getProperty('voices')

    voice_list = ['한국어', '영어']

    # 콤보 박스 적용
    language_combobox = ttk.Combobox(tts_settings_window, values=voice_list, width=50)

    if current_voice == "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_KO-KR_HEAMI_11.0":
        language_combobox.set("한국어")
    else:
        language_combobox.set("영어")

    language_combobox.pack()

    # 적용 및 창 닫기 버튼을 위한 프레임
    frame_buttons = Frame(tts_settings_window)
    frame_buttons.pack(side=TOP, pady=10)

    # 적용 버튼
    application_button = Button(frame_buttons, text="적용", command=lambda: apply_settings(speed_slider, volume_slider, language_combobox, tts_settings_window))
    application_button.pack(side=LEFT, pady=10)

    # 창 닫기 버튼
    close_button = Button(frame_buttons, text="닫기", command=tts_settings_window.destroy)
    close_button.pack(side=LEFT, pady=10)

    tts_settings_window.wait_window()

def apply_settings(speed_slider, volume_slider, language_combobox, tts_settings_window):
    # 슬라이더의 현재 값을 가져옵니다.
    new_rate = speed_slider.get()
    new_volume = volume_slider.get()
    selected_language = language_combobox.get()

    # 엔진에 새로운 속도와 음량을 설정합니다.
    engine.setProperty('rate', new_rate)
    engine.setProperty('volume', new_volume)

    if selected_language == "한국어":
        engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_KO-KR_HEAMI_11.0")
    else:
        engine.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

    # 설정 적용
    engine.runAndWait()

    # 창 닫기
    tts_settings_window.destroy()

def search():

    if text_box2.get("1.0", "end-1c") == "[기사 내용 요약중]":
        messagebox.showwarning("경고", "기사 내용 요약이 되어야 이 기능을 사용할 수 있습니다.")
        return
    elif len(text_box1.get("1.0", "end-1c")) == 0 or len(text_box2.get("1.0", "end-1c")) == 0:
        messagebox.showwarning("경고", "기사 내용을 불러와야 이 기능을 사용할 수 있습니다.")
        return

    # 새 창 생성
    search_window = Toplevel(root)
    search_window.geometry("350x100")
    search_window.title("텍스트 검색")

    search_window.grab_set()

    # 검색 텍스트 박스
    search_textbox = Entry(search_window, width=30)
    search_textbox.pack(pady=20)

    # 검색 버튼
    search_button = Button(search_window, text="검색", command=lambda: perform_search(search_textbox.get(), search_window))
    search_button.pack(pady=10)

    search_window.wait_window()

def highlight_search_results(text_widget, search_query):
    # 태그를 정의하고 배경색을 설정합니다.
    text_widget.tag_configure('highlight', background='yellow')

    # 기존의 하이라이트를 제거합니다.
    text_widget.tag_remove('highlight', '1.0', 'end')

    # 검색 시작 위치
    start_idx = '1.0'

    while True:
        # search_query를 찾습니다.
        start_idx = text_widget.search(search_query, start_idx, stopindex='end')

        # 검색어가 더 이상 없으면 반복을 중단합니다.
        if not start_idx:
            break

        # 검색어의 끝 인덱스를 찾습니다.
        end_idx = f"{start_idx}+{len(search_query)}c"

        # 찾은 검색어에 하이라이트 태그를 적용합니다.
        text_widget.tag_add('highlight', start_idx, end_idx)

        # 다음 검색을 위해 인덱스를 업데이트합니다.
        start_idx = end_idx

def perform_search(search_query, search_window):
    # 여기에 검색 로직 구현
    print("검색어:", search_query)
    # 검색 결과 처리 로직

    # text_box1과 text_box2에서 전체 텍스트를 가져옵니다.
    text_box1_content = text_box1.get("1.0", "end-1c")
    text_box2_content = text_box2.get("1.0", "end-1c")

    # 가져온 내용을 콘솔에 출력합니다.
    print("text_box1 내용:", text_box1_content)
    print("text_box2 내용:", text_box2_content)

    highlight_search_results(text_box1, search_query)
    highlight_search_results(text_box2, search_query)

    search_window.destroy()

def translate():

    if text_box2.get("1.0", "end-1c") == "[기사 내용 요약중]":
        messagebox.showwarning("경고", "기사 내용 요약이 되어야 이 기능을 사용할 수 있습니다.")
        return
    elif len(text_box1.get("1.0", "end-1c")) == 0 or len(text_box2.get("1.0", "end-1c")) == 0:
        messagebox.showwarning("경고", "기사 내용을 불러와야 이 기능을 사용할 수 있습니다.")
        return

    # 새 창 생성
    translate_window = Toplevel(root)
    translate_window.geometry("350x100")
    translate_window.title("번역")

    translate_window.grab_set()

    # 번역할 언어 선택 콤보 박스
    languages = ['언어 선택', 'English', '한국어', 'español', 'français', 'Deutsch']
    language_combobox = ttk.Combobox(translate_window, values=languages, width=27)

    language_combobox.set('언어 선택')
    language_combobox.pack(pady=10)

    # 검색 버튼
    translate_button = Button(translate_window, text="번역", command=lambda: translate_function(language_combobox.get(), translate_window))
    translate_button.pack(pady=10)

    translate_window.wait_window()

def translate_function(language, translate_window):

    text_box1_content = text_box1.get("1.0", "end-1c")
    text_box2_content = text_box2.get("1.0", "end-1c")

    if language == "English":
        translator = Translator()

        text_box1_content = translator.translate(text_box1_content, dest='en').text
        text_box2_content = translator.translate(text_box2_content, dest='en').text

        # text_box1과 text_box2에 번역된 내용을 업데이트합니다.
        text_box1.config(state=NORMAL)
        text_box1.delete("1.0", "end-1c")
        text_box1.insert("1.0", text_box1_content)
        text_box1.config(state=DISABLED)

        text_box2.config(state=NORMAL)
        text_box2.delete("1.0", "end-1c")
        text_box2.insert("1.0", text_box2_content)
        text_box2.config(state=DISABLED)
    elif language == "한국어":
        translator = Translator()

        text_box1_content = translator.translate(text_box1_content, dest='ko').text
        text_box2_content = translator.translate(text_box2_content, dest='ko').text

        # text_box1과 text_box2에 번역된 내용을 업데이트합니다.
        text_box1.config(state=NORMAL)
        text_box1.delete("1.0", "end-1c")
        text_box1.insert("1.0", text_box1_content)
        text_box1.config(state=DISABLED)

        text_box2.config(state=NORMAL)
        text_box2.delete("1.0", "end-1c")
        text_box2.insert("1.0", text_box2_content)
        text_box2.config(state=DISABLED)
    elif language == "español":
        translator = Translator()

        text_box1_content = translator.translate(text_box1_content, dest='es').text
        text_box2_content = translator.translate(text_box2_content, dest='es').text

        # text_box1과 text_box2에 번역된 내용을 업데이트합니다.
        text_box1.config(state=NORMAL)
        text_box1.delete("1.0", "end-1c")
        text_box1.insert("1.0", text_box1_content)
        text_box1.config(state=DISABLED)

        text_box2.config(state=NORMAL)
        text_box2.delete("1.0", "end-1c")
        text_box2.insert("1.0", text_box2_content)
        text_box2.config(state=DISABLED)
    elif language == "français":
        translator = Translator()

        text_box1_content = translator.translate(text_box1_content, dest='fr').text
        text_box2_content = translator.translate(text_box2_content, dest='fr').text

        # text_box1과 text_box2에 번역된 내용을 업데이트합니다.
        text_box1.config(state=NORMAL)
        text_box1.delete("1.0", "end-1c")
        text_box1.insert("1.0", text_box1_content)
        text_box1.config(state=DISABLED)

        text_box2.config(state=NORMAL)
        text_box2.delete("1.0", "end-1c")
        text_box2.insert("1.0", text_box2_content)
        text_box2.config(state=DISABLED)
    elif language == "Deutsch":
        translator = Translator()

        text_box1_content = translator.translate(text_box1_content, dest='de').text
        text_box2_content = translator.translate(text_box2_content, dest='de').text

        # text_box1과 text_box2에 번역된 내용을 업데이트합니다.
        text_box1.config(state=NORMAL)
        text_box1.delete("1.0", "end-1c")
        text_box1.insert("1.0", text_box1_content)
        text_box1.config(state=DISABLED)

        text_box2.config(state=NORMAL)
        text_box2.delete("1.0", "end-1c")
        text_box2.insert("1.0", text_box2_content)
        text_box2.config(state=DISABLED)

    translate_window.destroy()

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# mBART 모델 이름 (예: 'facebook/mbart-large-cc25'는 다양한 언어를 지원합니다)
model_name = 'facebook/mbart-large-cc25'

# 토크나이저와 모델을 로드합니다.
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 네이버 뉴스 속보 페이지 URL
url = "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1=001"
# requests를 이용해 웹 페이지 가져오기
response = requests.get(url)
# BeautifulSoup을 이용해 HTML 파싱
soup = BeautifulSoup(response.content, 'html.parser')
# 뉴스 제목이 포함된 HTML 요소 찾기
news_headlines = soup.find_all('a', class_="nclicks(fls.list)")

# TTS 엔진 가져오기
engine = pyttsx3.init()

# GUI
from tkinter import *

# Creating the main window
root = Tk()
root.title("네이버 뉴스 속보")

# Define window size
root.geometry("690x900")

# Create a frame for the listbox and scrollbar
frame_listbox = Frame(root)
# 리스트 박스 위에 레이블을 추가
label_listbox = Label(root, text="뉴스 제목", font=("Helvetica", 12), fg='black')
label_listbox.pack(pady=(0,5)) # 레이블의 위치를 조정
frame_listbox.pack(pady=(0,10))

scrollbar = Scrollbar(frame_listbox, orient=VERTICAL)

list_box_for_headlines = Listbox(frame_listbox, yscrollcommand=scrollbar.set, width=100, height=10, bd=2, relief=SUNKEN, fg='black', bg='white')
scrollbar.config(command=list_box_for_headlines.yview)
scrollbar.pack(side=RIGHT, fill=Y)
list_box_for_headlines.pack(side=LEFT, fill=BOTH, expand=True)
url_mapping = []
list_box_for_headlines.bind('<Double-1>', openArticle)

# Create a frame for the text box
""""""
frame_textboxes1 = Frame(root)
# 텍스트 박스 1 위에 레이블을 추가
label_textbox1 = Label(root, text="기사 내용", font=("Helvetica", 12), fg='black')
label_textbox1.pack(pady=(0,5)) # 레이블의 위치를 조정
frame_textboxes1.pack(pady=10)

# Text Box 1
text_box1 = Text(frame_textboxes1, width=100, height=10, bd=2, relief=SUNKEN)
text_box1.pack(side=TOP, fill=X)
text_box1.config(state=DISABLED)

""""""
# Create a frame for the text box
frame_textboxes2 = Frame(root)
# 텍스트 박스 2 위에 레이블을 추가
label_textbox2 = Label(root, text="기사 요약", font=("Helvetica", 12), fg='black')
label_textbox2.pack(pady=(0,5))  # 레이블의 위치를 조정
frame_textboxes2.pack(pady=10)

# Text Box 2
text_box2 = Text(frame_textboxes2, width=100, height=10, bd=2, relief=SUNKEN)
text_box2.pack(side=TOP, fill=X)
text_box2.config(state=DISABLED)

# 첫 번째 버튼 세트를 위한 프레임
frame_buttons_top = Frame(root)
frame_buttons_top.pack(side=TOP, pady=10)

""""""
# 첫 번째 버튼 만들기
button1 = Button(frame_buttons_top, text="속보 가져오기", width=20, height=2, bd=2, fg='white', bg='black', command=get_text_in_thread)
button1.pack(side=LEFT, padx=10, pady=20)

# 두 번째 버튼 만들기
button2 = Button(frame_buttons_top, text="뉴스 제목 읽기", width=20, height=2, bd=2, fg='white', bg='black', command=speak_title_in_thread)
button2.pack(side=LEFT, padx=10, pady=20)

# 세 번째 버튼 만들기
button3 = Button(frame_buttons_top, text="기사 내용 읽기", width=20, height=2, bd=2, fg='white', bg='black', command=speak_article_in_thread)
button3.pack(side=LEFT, padx=10, pady=20)

# 네 번째 버튼 만들기
button4 = Button(frame_buttons_top, text="기사 요약 읽기", width=20, height=2, bd=2, fg='white', bg='black', command=speak_summary_in_thread)
button4.pack(side=LEFT, padx=10, pady=20)

# 다섯 번째 버튼을 위한 프레임
frame_button_bottom = Frame(root)
frame_button_bottom.pack(side=TOP, pady=10)

# 다섯 번째 버튼 추가
button5 = Button(frame_button_bottom, text="TTS 설정", width=20, height=2, bd=2, fg='white', bg='black', command=get_open_tts_settings_in_thread)
button5.pack(side=LEFT, padx=10, pady=20)

# 여섯 번째 버튼 추가
button6 = Button(frame_button_bottom, text="텍스트 검색", width=20, height=2, bd=2, fg='white', bg='black', command=search_in_thread)
button6.pack(side=LEFT, padx=10, pady=20)

# 일곱 번째 버튼 추가
button7 = Button(frame_button_bottom, text="번역", width=20, height=2, bd=2, fg='white', bg='black', command=translation_in_thread)
button7.pack(side=LEFT, padx=10, pady=20)

# 여덞 번째 버튼 추가
button8 = Button(frame_button_bottom, text="음성 인식", width=20, height=2, bd=2, fg='white', bg='black', command=STT_in_thread)
button8.pack(side=LEFT, padx=10, pady=20)

# 새로운 텍스트 박스를 위한 프레임 생성
frame_new_textbox = Frame(root)
frame_new_textbox.pack(pady=10)

# 새로운 텍스트 박스 레이블 추가
label_new_textbox = Label(root, text="음성 인식 텍스트", font=("Helvetica", 12), fg='black')
label_new_textbox.pack(pady=(0,5))

# 새로운 텍스트 박스 추가
new_text_box = Text(frame_new_textbox, width=100, height=1, bd=2, relief=SUNKEN)
new_text_box.pack(side=TOP, fill=X)
new_text_box.config(state=DISABLED)

# 리스트 박스의 항목을 클릭할 때마다 on_listbox_click 함수를 호출
list_box_for_headlines.bind('<Button-1>', get_article_text_and_summary_in_thread)

# Run the application
root.mainloop()