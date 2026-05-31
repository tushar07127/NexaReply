import pyautogui
import time 
import pyperclip
from ai import ask_ai
import keyboard
from PIL import ImageGrab
import re

pyautogui.click(1258, 1040)
last_message = ""
paused = False

def clean_text(text):
    text = re.sub(r'\[\d{1,2}:\d{2},\s*\d{1,2}/\d{1,2}/\d{4}\]\s*[\w\s]+:', '', text)
    text = re.sub(r'\d{1,2}:\d{2},\s*\d{1,2}/\d{1,2}/\d{4}', '', text)
    return text.strip()

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        print("Bot PAUSED - press F9 to resume")
    else:
        print("Bot RESUMED - press F9 to pause")

keyboard.add_hotkey('f9', toggle_pause)

while True:
    if paused:
        time.sleep(1)
        continue

    pyautogui.click(1400, 600)
    time.sleep(0.3)
    pyautogui.scroll(-10)
    time.sleep(0.5)
    pyautogui.click(1400, 867)
    time.sleep(0.3)
    
    pyautogui.moveTo(966, 278)
    pyautogui.dragTo(1640, 907, duration=0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.3)

    chat_input = pyperclip.paste()

    if chat_input.strip() == "":
        time.sleep(3)
        continue

    raw_last_line = chat_input.strip().split('\n')[-1]
    
    # skip if its our own message
    if 'Tushar' in raw_last_line:
        time.sleep(5)
        continue

    last_line = clean_text(raw_last_line)
    print("Last line:", last_line)

    if last_line == "" or last_line == last_message:
        time.sleep(5)
        continue

    last_message = last_line
    time.sleep(1)
    reply = ask_ai(last_line)
    reply = clean_text(reply)
    print("Reply:", reply)
    pyperclip.copy(reply)
    pyautogui.click(1026, 956)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.click(1861, 949)
    
    time.sleep(15)                  # ← wait 15 seconds after replying

    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"Sender: {last_line}\nBot: {reply}\n\n")