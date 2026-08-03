import io
import json
import os
import random
import re
from gtts import gTTS
import streamlit as st

# 🚀 全域系統版本號 (可愛卡通王子特別版)
APP_VERSION = "v2.2.0-Prince (Build 20260803 - Dynamic TTS & Exam Guide Link)"

# ==========================================
# 🛡️ 防腐層：保留指定的原始結構與函數
# ==========================================
VOCABULARY = []
SENTENCES = []


def init_quiz():
  pass


def play_audio():
  pass


def show_learning_mode():
  pass


def show_quiz_mode():
  pass


def show_debug_info():
  pass


# 原始聽力題庫 (15題標準數據庫，完全保留)
QUIZ_DATA = [
    {
        "id": 1,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-01.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["riyar", "'alo", "fanaw", "sa'owac"],
        "correct_text": "riyar",
    },
    {
        "id": 2,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-02.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["korkor", "rohayan", "romakat", "rotarot"],
        "correct_text": "romakat",
    },
    {
        "id": 3,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-03.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["hadhad", "hakhak", "hawan", "hafay"],
        "correct_text": "hafay",
    },
    {
        "id": 4,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-04.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["tefo'", "'okoy", "tafokod", "tafolod"],
        "correct_text": "tafokod",
    },
    {
        "id": 5,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-05.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["fakar", "tayhi", "pitaw", "tarakar"],
        "correct_text": "pitaw",
    },
    {
        "id": 6,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-06.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["sariri'", "riri'", "siri", "riyar"],
        "correct_text": "siri",
    },
    {
        "id": 7,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-07.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["koleto", "lokot", "kewaw", "kakorot"],
        "correct_text": "koleto",
    },
    {
        "id": 8,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-08.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["siwoy", "kodasing", "konga", "damay"],
        "correct_text": "konga",
    },
    {
        "id": 9,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-09.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["mali'", "tikami", "tilifi", "pawli"],
        "correct_text": "tilifi",
    },
    {
        "id": 10,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-10.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["picakay", "pitangtang", "picaliw", "pafeli'"],
        "correct_text": "picakay",
    },
    {
        "id": 11,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-11.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["'olaw", "'alo", "fao", "tao"],
        "correct_text": "tao",
    },
    {
        "id": 12,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-12.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["rorang", "kolong", "lotong", "ekong"],
        "correct_text": "lotong",
    },
    {
        "id": 13,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-13.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["Halitamako", "Haliradiw", "Haliepah", "Hali'ecaw"],
        "correct_text": "Haliepah",
    },
    {
        "id": 14,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-14.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["dafak", "a'ayad", "dadaya", "kamaya"],
        "correct_text": "dadaya",
    },
    {
        "id": 15,
        "audio_path": (
            "assets/audio/01_listening/listening_words/tengil-a1-15.mp3"
        ),
        "question_text": "聆聽音檔，選出關聯的詞彙：",
        "options": ["sioy", "simal", "sinafel", "simico"],
        "correct_text": "sinafel",
    },
]


# ==========================================
# 🎵 新增功能：南島語系動態發音引擎 (TTS)
# ==========================================
def play_tts(text):
  match = re.search(r'「(.*?)」', text)
  if match:
    target_text = match.group(1)
  else:
    target_text = re.sub(
        r'請問.*?中文意思是什麼|的阿美語是哪一個|聆聽音檔.*?|題目：|阿美語：|中文：.*',
        '',
        text,
    )
    target_text = re.sub(r'[\u4e00-\u9fa5]', '', target_text)
    target_text = re.sub(r'^\d+[\.\、]\s*', '', target_text)

  target_text = target_text.strip()
  if not target_text:
    target_text = text

  try:
    tts = gTTS(text=target_text, lang='id')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp.getvalue(), format='audio/mp3')
  except Exception as e:
    st.error('⚠️ 無法生成語音，請確認環境是否支援 gTTS 或檢查網路連線。')


# ==========================================
# 🧠 動態解析引擎：跨行讀取與穩定分割版
# ==========================================
def load_question_bank():
  base_dir = os.path.dirname(os.path.abspath(__file__))
  cwd_dir = os.getcwd()

  db = {
      '聽音選詞': [],
      '對話理解': [],
      '段落朗讀': [],
      '情境問答': [],
      '看圖表達': [],
      '詞彙語意': [],
      '語言結構': [],
      '句子聽寫': [],
      '問答': [],
  }

  scanned_files = []
  for d in [base_dir, cwd_dir]:
    if not os.path.exists(d):
      continue
    try:
      for f in os.listdir(d):
        if f.lower().endswith('.txt') and f.lower() not in [
            'app.txt',
            'requirements.txt',
            '提示詞.txt',
        ]:
          scanned_files.append(os.path.join(d, f))
    except:
      pass

  target_content = ''
  file_loaded = False
  encodings_to_try = ['utf-8', 'utf-8-sig', 'big5', 'cp950']

  for filepath in set(scanned_files):
    for enc in encodings_to_try:
      try:
        with open(filepath, 'r', encoding=enc) as f:
          text_data = f.read()
          if '聽音選詞' in text_data and '對話理解' in text_data:
            target_content = text_data
            file_loaded = True
            break
      except:
        continue
    if file_loaded:
      break

  if not file_loaded:
    return db

  current_section = None
  current_question = []

  def save_question():
    if current_section and current_question:
      q_text = ' '.join(current_question).strip()
      if re.match(r'^\d+[\.\、]', q_text):
        db[current_section].append(q_text)
      current_question.clear()

  for line in target_content.split('\n'):
    line = line.strip()
    if not line:
      save_question()
      continue

    if '一、選擇題（聽音選詞）' in line:
      save_question()
      current_section = '聽音選詞'
    elif '二、選擇題（對話理解）' in line:
      save_question()
      current_section = '對話理解'
    elif '三、段落朗讀' in line:
      save_question()
      current_section = '段落朗讀'
    elif '四、情境問答' in line:
      save_question()
      current_section = '情境問答'
    elif '五、看圖表達' in line:
      save_question()
      current_section = '看圖表達'
    elif '六、選擇題（詞彙語意）' in line:
      save_question()
      current_section = '詞彙語意'
    elif '七、選擇題（語言結構）' in line:
      save_question()
      current_section = '語言結構'
    elif '八、句子聽寫' in line:
      save_question()
      current_section = '句子聽寫'
    elif '九、問答' in line:
      save_question()
      current_section = '問答'

    elif re.match(r'^\d+[\.\、]', line):
      save_question()
      current_question.append(line)
    else:
      if current_question:
        current_question.append(line)

  save_question()

  return db


# ==========================================
# 🎨 終極 UI 渲染邏輯 (結合動態 TTS 發音按鈕)
# ==========================================
def render_mcq(line, prefix):
  try:
    if '(A)' not in line:
      st.info(line)
      return

    parts = line.split('(A)', 1)
    q_part = parts[0].strip()
    rest = '(A)' + parts[1]

    opts_str = rest
    ans_str = ''
    ana_str = ''

    if '答案：' in rest:
      ans_parts = rest.split('答案：', 1)
      opts_str = ans_parts[0].strip()
      ans_ana = ans_parts[1]

      if '分析：' in ans_ana:
        final_parts = ans_ana.split('分析：', 1)
        ans_str = final_parts[0].strip('。 ')
        ana_str = final_parts[1].strip()
      else:
        ans_str = ans_ana.strip('。 ')

    is_listening = '聽音選詞' in prefix or '對話理解' in prefix
    col_q, col_btn = st.columns([4, 1.5])

    with col_q:
      if is_listening:
        if st.toggle('👁️ 顯示題目文字', key=f't_show_q_{prefix}'):
          st.markdown(f'**{q_part}**')
        else:
          st.markdown('**[👑 密語隱藏中，請點擊右方魔法按鈕收聽音檔]**')
      else:
        st.markdown(f'**{q_part}**')

    with col_btn:
      if st.button('🔊 魔法發音', key=f'tts_btn_{prefix}'):
        play_tts(q_part)

    opts = []
    for tag in ['(A)', '(B)', '(C)', '(D)']:
      if tag in opts_str:
        opt_text = opts_str.split(tag, 1)[1]
        for next_tag in ['(B)', '(C)', '(D)']:
          if next_tag > tag and next_tag in opt_text:
            opt_text = opt_text.split(next_tag, 1)[0]
        opts.append(tag + ' ' + opt_text.strip())

    user_ans = st.radio('👑 請選擇皇家答案：', opts, index=None, key=prefix)

    if st.toggle('💡 揭曉解答與分析', key=f't_ans_{prefix}'):
      if ans_str:
        msg = f'**正確答案：** {ans_str}'
        if ana_str:
          msg += f'\n\n**分析：** {ana_str}'
        st.success(msg)
      else:
        st.warning('無標準答案。')
    elif user_ans and ans_str:
      if ans_str in user_ans:
        st.success(
            f'🎉 答對了！太棒了，小王子為你喝采！'
            + (f'分析：{ana_str}' if ana_str else '')
        )
      else:
        st.error(
            f'👑 再試一次喔！正確答案是：{ans_str}。'
            + (f'分析：{ana_str}' if ana_str else '')
        )
  except Exception as e:
    st.info(line)


def render_reading(line, prefix):
  try:
    q_part = line
    ch_part = ''
    if '(中文：' in line:
      parts = line.split('(中文：', 1)
      q_part = parts[0].strip()
      ch_part = parts[1].strip(')')
    elif '(中文大意：' in line:
      parts = line.split('(中文大意：', 1)
      q_part = parts[0].strip()
      ch_part = parts[1].strip(')')

    col_q, col_btn = st.columns([4, 1.5])
    with col_q:
      st.markdown(f'📖 **{q_part}**')
    with col_btn:
      if st.button('🔊 皇家朗讀', key=f'tts_btn_{prefix}'):
        play_tts(q_part)

    if ch_part:
      if st.toggle('💡 展開中文翻譯', key=f't_{prefix}'):
        st.success(ch_part)
  except:
    st.info(line)


def render_qa(line, prefix):
  try:
    text = line
    q_am = text
    ch_hint = ''
    ans = ''
    ana = ''

    if '中文：' in text:
      parts = text.split('中文：', 1)
      q_am = parts[0].strip()
      text = parts[1]

    if '參考回答：' in text:
      parts = text.split('參考回答：', 1)
      ch_hint = parts[0].strip()
      text = parts[1]
    elif '作答參考：' in text:
      parts = text.split('作答參考：', 1)
      ch_hint = parts[0].strip()
      text = parts[1]

    if '分析：' in text:
      parts = text.split('分析：', 1)
      ans = parts[0].strip()
      ana = parts[1].strip()
    else:
      if not ans:
        ans = text.strip()

    q_am = q_am.replace('題目：', ' 題目：')

    col_q, col_btn = st.columns([4, 1.5])
    with col_q:
      is_situational = '情境問答' in prefix
      if is_situational:
        if st.toggle('👁️ 顯示題目與提示', key=f't_show_q_{prefix}'):
          st.markdown(f'🗣️ **{q_am}**')
          if ch_hint:
            st.caption(f'💡 中文提示：{ch_hint}')
        else:
          st.markdown('**[👑 騎士考驗提示隱藏中]**')
      else:
        st.markdown(f'🗣️ **{q_am}**')
        if ch_hint:
          st.caption(f'💡 中文提示：{ch_hint}')

    with col_btn:
      if st.button('🔊 聽取問句', key=f'tts_btn_{prefix}'):
        play_tts(q_am)

    if ans or ana:
      if st.toggle('💡 顯示參考解答', key=f't_{prefix}'):
        msg = ''
        if ans:
          msg += f'參考解答：{ans}'
        if ana:
          msg += f'\n\n分析：{ana}'
        st.success(msg)
        if ans:
          if st.button('🔊 發音參考解答', key=f'tts_ans_{prefix}'):
            play_tts(ans)
  except:
    st.info(line)


def render_picture(line, prefix):
  try:
    text = line
    pic = text
    hint = ''
    ans = ''
    ana = ''

    if '圖片情境：' in text:
      parts = text.split('圖片情境：', 1)
      pic = parts[1]

    if '中文提示：' in pic:
      parts = pic.split('中文提示：', 1)
      pic = parts[0].strip()
      hint_part = parts[1]

      if '作答參考：' in hint_part:
        h_parts = hint_part.split('作答參考：', 1)
        hint = h_parts[0].strip()
        ans_part = h_parts[1]

        if '重點分析：' in ans_part:
          a_parts = ans_part.split('重點分析：', 1)
          ans = a_parts[0].strip()
          ana = a_parts[1].strip()
        elif '重點：' in ans_part:
          a_parts = ans_part.split('重點：', 1)
          ans = a_parts[0].strip()
          ana = a_parts[1].strip()
        else:
          ans = ans_part.strip()
      else:
        hint = hint_part.strip()

    try:
      idx = int(prefix.split('_')[-1]) + 1
      img_path_jpg = f'assets/images/picture_{idx}.jpg'
      img_path_png = f'assets/images/picture_{idx}.png'

      if os.path.exists(img_path_jpg):
        st.image(img_path_jpg, use_container_width=True)
      elif os.path.exists(img_path_png):
        st.image(img_path_png, use_container_width=True)
      else:
        st.info(
            f'🖼️ 繪本圖片佔位區：若要顯示圖片，請將圖片命名為 `picture_{idx}.jpg` 或'
            f' `.png`，並放置於 `assets/images/` 資料夾中。'
        )
    except:
      pass

    st.markdown(f'🖼️ **繪本情境：** {pic}')

    if hint:
      st.caption(f'💡 中文提示：{hint}')

    st.text_area(
        '請在此作答：',
        key=f'input_{prefix}',
        label_visibility='collapsed',
        placeholder='可以在此寫下小王子的口說草稿...',
    )

    if ans or ana:
      if st.toggle('💡 顯示作答參考', key=f't_{prefix}'):
        msg = ''
        if ans:
          msg += f'作答參考：{ans}'
        if ana:
          msg += f'\n\n重點：{ana}'
        st.success(msg)

        if ans:
          if st.button('🔊 發音作答參考', key=f'tts_ans_{prefix}'):
            play_tts(ans)
  except:
    st.info(line)


def render_dictation(line, prefix):
  try:
    text = line
    am = text
    ch = ''
    ana = ''

    if '中文：' in text:
      parts = text.split('中文：', 1)
      am = parts[0].replace('阿美語：', '').strip()
      text = parts[1]

      if '分析：' in text:
        sub_parts = text.split('分析：', 1)
        ch = sub_parts[0].strip()
        ana = sub_parts[1].strip()
      else:
        ch = text.strip()

    st.text_area(
        '請在此作答：',
        key=f'input_{prefix}',
        label_visibility='collapsed',
        placeholder='請在此輸入您聽寫的羽毛筆筆記...',
    )

    col_q, col_btn = st.columns([4, 1.5])

    with col_q:
      if st.toggle('👁️ 顯示聽寫原文', key=f't_show_dict_{prefix}'):
        st.markdown(f'✍️ **{am}**')
      else:
        st.markdown('**[👑 原文隱藏中，請點擊右側魔法按鈕進行聽寫測試]**')

    with col_btn:
      if st.button('🔊 魔法發音', key=f'tts_btn_{prefix}'):
        play_tts(am)

    if ch or ana:
      if st.toggle('💡 顯示翻譯與分析', key=f't_{prefix}'):
        msg = ''
        if ch:
          msg += f'中文：{ch}'
        if ana:
          msg += f'\n\n分析：{ana}'
        st.success(msg)
  except:
    st.info(line)


def render_section(section_name, db):
  questions = db.get(section_name, [])
  if not questions:
    st.warning(f'⚠️ 系統抓不到【{section_name}】的資料。')
    return

  for i, line in enumerate(questions):
    with st.container():
      st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
      if (
          '聽音選詞' in section_name
          or '對話理解' in section_name
          or section_name in ['詞彙語意', '語言結構']
      ):
        render_mcq(line, f'{section_name}_{i}')
      elif section_name == '段落朗讀':
        render_reading(line, f'{section_name}_{i}')
      elif section_name in ['情境問答', '問答']:
        render_qa(line, f'{section_name}_{i}')
      elif section_name == '看圖表達':
        render_picture(line, f'{section_name}_{i}')
      elif section_name == '句子聽寫':
        render_dictation(line, f'{section_name}_{i}')
      st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 🚀 應用程式主邏輯 (Main) - 替換為可愛卡通王子風格
# ==========================================
def main():
  st.set_page_config(
      page_title="🤴 小王子族語王國 ‧ 中高級認證大冒險",
      page_icon="👑",
      layout="centered",
      initial_sidebar_state="collapsed",
  )

  # 👑 可愛卡通王子風 (Cute Cartoon Prince Theme) CSS
  st.markdown(
      """
    <style>
    /* Google Fonts 引入可愛圓潤字體 */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Zen+Maru+Gothic:wght@500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Zen Maru Gothic', 'Fredoka', sans-serif;
    }

    /* 應用程式主背景：夢幻皇室粉藍與童話鵝黃柔和漸層 */
    .stApp {
        background: linear-gradient(135deg, #eef4ff 0%, #f7f3ff 40%, #fff9e6 100%);
        background-attachment: fixed;
        color: #3c3250;
    }
    
    /* 頂級皇家標題盒 */
    .prince-header {
        text-align: center;
        background: linear-gradient(135deg, #7b2cbf 0%, #9d4edd 50%, #c77dff 100%);
        padding: 22px 25px;
        border-radius: 25px;
        box-shadow: 0 8px 20px rgba(123, 44, 191, 0.25), inset 0 0 15px rgba(255, 255, 255, 0.3);
        border: 3px solid #ffca3a;
        margin-bottom: 25px;
        color: #ffffff;
    }

    .prince-header h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2) !important;
        margin: 0 !important;
        font-size: 2.1rem !important;
    }

    .prince-header p {
        color: #ffe6a7 !important;
        margin: 6px 0 0 0 !important;
        font-weight: 700;
        font-size: 1.05rem;
    }

    /* 可愛卡通測驗卡片 (城堡繪本風格) */
    .quiz-card {
        background: #ffffff;
        padding: 24px 28px;
        border-radius: 24px;
        border: 3px solid #ffe066;
        box-shadow: 0 10px 22px rgba(157, 78, 221, 0.1);
        margin-top: 18px;
        margin-bottom: 24px;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        color: #3c3250;
        position: relative;
    }
    
    /* Hover 懸浮時的小王子魔法動態 */
    .quiz-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 30px rgba(255, 202, 58, 0.35);
        border-color: #ffca3a;
    }
    
    /* 標題與內文色彩 */
    h1, h2, h3 {
        color: #5a189a !important;
        font-weight: 700 !important;
    }

    p, span, label {
        color: #3c3250 !important;
        font-weight: 500;
    }

    /* 可愛卡通按鈕樣式 (圓潤糖果風) */
    div.stButton > button {
        background: linear-gradient(135deg, #ffca3a 0%, #ffb703 100%) !important;
        border: 2px solid #ffffff !important;
        border-radius: 50px !important;
        color: #4a2800 !important;
        font-weight: 800 !important;
        padding: 8px 20px !important;
        box-shadow: 0 4px 12px rgba(255, 183, 3, 0.35) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #ffb703 0%, #fb8500 100%) !important;
        color: #ffffff !important;
        transform: scale(1.05) !important;
        box-shadow: 0 6px 16px rgba(251, 133, 0, 0.45) !important;
    }

    /* Toggle 開關與選單客製化 */
    div[data-baseweb="segmented-control"] {
        background-color: #f0e6ff !important;
        border-radius: 30px !important;
        padding: 5px !important;
        border: 2px solid #d8b4fe !important;
    }

    /* 分隔線星光風格 */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #ffca3a, #9d4edd, #ffca3a, transparent);
        margin: 20px 0;
    }

    /* Alert / Success 提示框可愛畫風 */
    .stAlert {
        border-radius: 18px !important;
        border: 2px solid #c77dff !important;
    }

    </style>
    """,
      unsafe_allow_html=True,
  )

  # 👑 可愛王子主題 Header Banner
  st.markdown(
      """
    <div class="prince-header">
        <h1>🤴 小王子族語王國 ‧ 中高級認證大冒險 👑</h1>
        <p>✨ 勇敢的皇家小騎士，一起踏上南島語言的奇幻冒險旅程吧！ ✨</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

  main_options = [
      "📋 城堡公告",
      "🎧 皇家聽力",
      "🗣️ 騎士口說",
      "📖 智者閱讀",
      "✍️ 魔法寫作",
  ]
  current_tab = st.segmented_control(
      "主選單導覽",
      main_options,
      default="📋 城堡公告",
      label_visibility="collapsed",
  )

  if "previous_tab" not in st.session_state:
    st.session_state.previous_tab = None

  if st.session_state.previous_tab != current_tab:
    st.session_state.submitted = False
    st.session_state.audio_triggered = False
    if "writing_submitted" in st.session_state:
      st.session_state.writing_submitted = False
    st.session_state.previous_tab = current_tab

  db = load_question_bank()

  if current_tab == "📋 城堡公告":
    st.subheader(
        "📜"
        " [城堡公告：簡章與認證考試說明](https://lokahsu.ilrdf.org.tw/web_lokahsu/Files/Guide/1_20251211_162558.pdf)"
    )
    st.divider()
    st.info(
        "🏰"
        " 歡迎來到族語學習王國！請透過上方導覽列選擇您要挑戰的試煉項目。系統將自動載入皇家題庫，並提供魔法語音發音試聽！"
    )

  elif current_tab == "🎧 皇家聽力":
    st.subheader("🎧 皇家聽力試煉 (pitengil)")
    st.divider()
    listening_sub = st.radio(
        "👑 請選擇試煉題型：",
        ["選擇題-聽音選詞", "選擇題-對話理解"],
        horizontal=True,
    )
    if listening_sub == "選擇題-聽音選詞":
      render_section("聽音選詞", db)
    elif listening_sub == "選擇題-對話理解":
      render_section("對話理解", db)

  elif current_tab == "🗣️ 騎士口說":
    st.subheader("🗣️ 騎士口說試煉 (pisowal)")
    st.divider()
    speaking_sub = st.radio(
        "👑 請選擇試煉題型：",
        ["段落朗讀", "情境問答", "看圖表達"],
        horizontal=True,
    )
    if speaking_sub == "段落朗讀":
      render_section("段落朗讀", db)
    elif speaking_sub == "情境問答":
      render_section("情境問答", db)
    elif speaking_sub == "看圖表達":
      render_section("看圖表達", db)

  elif current_tab == "📖 智者閱讀":
    st.subheader("📖 智者閱讀試煉 (piasip)")
    st.divider()
    reading_sub = st.radio(
        "👑 請選擇試煉題型：",
        ["選擇題-詞彙語意", "選擇題-語言結構"],
        horizontal=True,
    )
    if reading_sub == "選擇題-詞彙語意":
      render_section("詞彙語意", db)
    elif reading_sub == "選擇題-語言結構":
      render_section("語言結構", db)

  elif current_tab == "✍️ 魔法寫作":
    st.subheader("✍️ 魔法寫作試煉 (pitilid)")
    st.divider()
    writing_sub = st.radio(
        "👑 請選擇試煉題型：", ["句子聽寫", "問答"], horizontal=True
    )
    if writing_sub == "句子聽寫":
      render_section("句子聽寫", db)
    elif writing_sub == "問答":
      render_section("問答", db)

  st.write("---")
  st.caption(
      f"👑 2026 小王子族語王國 ‧ 三一魔法開發團隊 ｜ 系統版本： **{APP_VERSION}** "
  )


if __name__ == "__main__":
  main()
