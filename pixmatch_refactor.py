import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

#Configura el diseño de la pestaña de la pagina
st.set_page_config(page_title="PixMatch", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

#Accede a la ruta para los archivos
vDrive = os.path.splitdrive(os.getcwd())[0]
if vDrive == "C:": vpth = "C:/Users/danio/OneDrive/Documentos/POO/ahhhhhhhhhh/8-pixmatch-interacci-n-con-c-digo-existente-Daniorobio/"   # local developer's disc
else: vpth = "./"

#Ajustes del diseño de la pagina
sbe = """<span style='font-size: 140px;
                      border-radius: 7px;
                      text-align: center;
                      display:inline;
                      padding-top: 3px;
                      padding-bottom: 3px;
                      padding-left: 0.4em;
                      padding-right: 0.4em;
                      '>
                      |fill_variable|
                      </span>"""

# Diseño de emojis
pressed_emoji = """<span style='font-size: 24px;
                                border-radius: 7px;
                                text-align: center;
                                display:inline;
                                padding-top: 3px;
                                padding-bottom: 3px;
                                padding-left: 0.2em;
                                padding-right: 0.2em;
                                '>
                                |fill_variable|
                                </span>"""

#Diseño de barra horizontal
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"  # thin divider line
purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """

#Inicializa las variables del codigo
mystate = st.session_state
if "expired_cells" not in mystate: mystate.expired_cells = []
if "myscore" not in mystate: mystate.myscore = 0
if "plyrbtns" not in mystate: mystate.plyrbtns = {}
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''
if "emoji_bank" not in mystate: mystate.emoji_bank = []
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7, '']  # difficulty level, sec interval for autogen, total_cells_per_row_or_col, player name
if "malos" not in mystate: mystate.malos = 0 #lleva cuenta de los turnos fallidos

#Arreglar el diseño de la pagina
def ReduceGapFromPageTop(wch_section='main page'):
    if wch_section == 'main page':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)  # main area
    elif wch_section == 'sidebar':
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)  # sidebar
    elif wch_section == 'all':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)  # main area
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)  # sidebar


#Jugadores pasados y sus puntaciones
def Leaderboard(what_to_do):
    # Crea la tabla de clasificacion, de los puntajes
    if what_to_do == 'create':
        # Crea la tabla de clasificación si no existe y el nombre del jugador está proporcionado
        if mystate.GameDetails[3] != '' and not os.path.isfile(vpth + 'leaderboard.json'):
            tmpdict = {}
            json.dump(tmpdict, open(vpth + 'leaderboard.json', 'w'))  # Escribir archivo

    elif what_to_do == 'write':
        # Guarda el puntaje del jugador en la tabla de clasificación si el nombre está proporcionado
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))  # Leer archivo
                leaderboard_dict_lngth = len(leaderboard)

                leaderboard[str(leaderboard_dict_lngth + 1)] = {'NameCountry': mystate.GameDetails[3],
                                                                'HighestScore': mystate.myscore}
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'],
                                          reverse=True))  # Ordenar de forma descendente

                if len(leaderboard) > 4:  # Mostrar los cuatro principales jugadores
                    for i in range(len(leaderboard) - 4):
                        leaderboard.popitem()  # Eliminar último jugador

                json.dump(leaderboard, open(vpth + 'leaderboard.json', 'w'))  # Escribir archivo

    elif what_to_do == 'read':
        # Leer puntajes y mostrar a los cuatro principales jugadores en la interfaz gráfica
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))  # Leer archivo

                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'],
                                          reverse=True))  # Ordenar de forma descendente

                sc0, sc1, sc2, sc3, sc4 = st.columns((2, 2, 2, 2, 2))
                rknt = 0

                # Muestra la tabla de posiciones
                for vkey in leaderboard.keys():
                    if leaderboard[vkey]['NameCountry'] != '':
                        rknt += 1
                        if rknt == 1:
                            sc0.write('🏆 Top Players:')
                            sc1.write(
                                f"🥇 | {leaderboard[vkey]['NameCountry']}: **{leaderboard[vkey]['HighestScore']}**")
                        elif rknt == 2:
                            sc2.write(
                                f"🥈 | {leaderboard[vkey]['NameCountry']}: **{leaderboard[vkey]['HighestScore']}**")
                        elif rknt == 3:
                            sc3.write(
                                f"🥉 | {leaderboard[vkey]['NameCountry']}: **{leaderboard[vkey]['HighestScore']}**")
                        elif rknt == 4:
                            sc4.write(
                                f"4️⃣ | {leaderboard[vkey]['NameCountry']}: **{leaderboard[vkey]['HighestScore']}**")


# Pagina principal antes del inicio del juego
def InitialPage():
    with st.sidebar:
        st.subheader("🖼️ Pix Match:")
        st.markdown(horizontal_bar, True)

        # sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 420))
        sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 390))
        st.image(sidebarlogo, use_column_width='auto')

    # ViewHelp
    # Instrucciones del juego
    hlp_dtl = f"""<span style="font-size: 26px;">
    <ol>
    <li style="font-size:15px";>Game play opens with (a) a sidebar picture and (b) a N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
    <li style="font-size:15px";>You need to match the sidebar picture with a grid picture button, by pressing the (matching) button (as quickly as possible).</li>
    <li style="font-size:15px";>Each correct picture match will earn you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match will earn you <strong>-1</strong> point.</li>
    <li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed seconds interval (Easy=8, Medium=6, Hard=5). Each regeneration will have a penalty of <strong>-1</strong> point</li>
    <li style="font-size:15px";>Each of the grid buttons can only be pressed once during the entire game.</li>
    <li style="font-size:15px";>The game completes when all the grid buttons are pressed.</li>
    <li style="font-size:15px";>At the end of the game, if you have a positive score, you will have <strong>won</strong>; otherwise, you will have <strong>lost</strong>.</li>
    </ol></span>"""

    # Muestra las imagenes
    sc1, sc2 = st.columns(2)
    random.seed()
    GameHelpImg = vpth + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    GameHelpImg = Image.open(GameHelpImg).resize((550, 550))
    sc2.image(GameHelpImg, use_column_width='auto')

    # Muestra los encabezados
    sc1.subheader('Rules | Playing Instructions:')
    sc1.markdown(horizontal_bar, True)
    sc1.markdown(hlp_dtl, unsafe_allow_html=True)
    st.markdown(horizontal_bar, True)

    # Nota del autor
    author_dtl = "<strong>Happy Playing: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
    st.markdown(author_dtl, unsafe_allow_html=True)


# Leer las imagenes
def ReadPictureFile(wch_fl):
    try:
        pxfl = f"{vpth}{wch_fl}"
        return base64.b64encode(open(pxfl, 'rb').read()).decode()

    except:
        return ""


# Presionar una celda
def PressedCheck(vcell):
    if mystate.plyrbtns[vcell]['isPressed'] == False:
        mystate.plyrbtns[vcell]['isPressed'] = True
        mystate.expired_cells.append(vcell)

        # Si la respuesta es correcta se añade al puntaje lo correspondiente a la dificultad

        if mystate.plyrbtns[vcell]['eMoji'] == mystate.sidebar_emoji:
            mystate.plyrbtns[vcell]['isTrueFalse'] = True
            mystate.myscore += 5

            if mystate.GameDetails[0] == 'Easy':
                mystate.myscore += 5
            elif mystate.GameDetails[0] == 'Medium':
                mystate.myscore += 3
            elif mystate.GameDetails[0] == 'Hard':
                mystate.myscore += 1

        # Si es incorrecta al puntaje se le resta 1
        else:
            mystate.plyrbtns[vcell]['isTrueFalse'] = False
            mystate.myscore -= 1
            mystate.malos += 1 # Sumador de intentos fallidos

# Si perdio muestra la animacion de perder y se devuelve a la pantalla principal
def Perder():
    if mystate.GameDetails[0] == 'Easy':
        tmp = ((mystate.GameDetails[2] ** 2)/2) + 1
        if tmp == mystate.malos:
            st.snow()
            Leaderboard('write')
            mystate.malos = 0
            tm.sleep(5)
            mystate.runpage = Main
            st.rerun()
    elif mystate.GameDetails[0] == 'Medium':
        tmp = ((mystate.GameDetails[2] ** 2) / 2) + 1
        if tmp == mystate.malos:
            st.snow()
            Leaderboard('write')
            mystate.malos = 0
            tm.sleep(5)
            mystate.runpage = Main
            st.rerun()
    elif mystate.GameDetails[0] == 'Hard':
        tmp = ((mystate.GameDetails[2] ** 2) / 2) + 1
        if tmp == mystate.malos:
            st.snow()
            Leaderboard('write')
            mystate.malos = 0
            tm.sleep(5)
            mystate.runpage = Main
            st.rerun()


# Regenera los emojis despues del tiempo
def ResetBoard():
    total_cells_per_row_or_col = mystate.GameDetails[2]

    sidebar_emoji_no = random.randint(1, len(mystate.emoji_bank)) - 1
    mystate.sidebar_emoji = mystate.emoji_bank[sidebar_emoji_no]

    # Si se ha presionado la celda entonces no se cambia, mientras que si esta presionada si se cambia
    # Se elige de la lista de emojis definida anteriormente
    sidebar_emoji_in_list = False
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        rndm_no = random.randint(1, len(mystate.emoji_bank)) - 1
        if mystate.plyrbtns[vcell]['isPressed'] == False:
            vemoji = mystate.emoji_bank[rndm_no]
            mystate.plyrbtns[vcell]['eMoji'] = vemoji
            if vemoji == mystate.sidebar_emoji: sidebar_emoji_in_list = True

    if sidebar_emoji_in_list == False:  # sidebar pix is not on any button; add pix randomly
        tlst = [x for x in range(1, ((total_cells_per_row_or_col ** 2) + 1))]
        flst = [x for x in tlst if x not in mystate.expired_cells]
        if len(flst) > 0:
            lptr = random.randint(0, (len(flst) - 1))
            lptr = flst[lptr]
            mystate.plyrbtns[lptr]['eMoji'] = mystate.sidebar_emoji


# Se inicializan los emojis que se utilizaran en el juego
def PreNewGame():
    total_cells_per_row_or_col = mystate.GameDetails[2]
    mystate.expired_cells = []
    mystate.myscore = 0

    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛',
              '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩',
              '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱',
              '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓',
              '👴', '👲', '👳']
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬',
             '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗',
             '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊',
             '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻',
             '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽',
             '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽',
             '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔',
               '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗',
               '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆',
               '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕',
               '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍',
                '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬',
                '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍',
              '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️',
                    '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘',
                 '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖',
                  '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟',
                  '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️',
                  '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛',
                  '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    # Dependiendo de la dificultad elegida se utilizan diferentes emojis (son aleatorios)
    random.seed()
    if mystate.GameDetails[0] == 'Easy':
        wch_bank = random.choice(['foods', 'moon', 'animals'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Medium':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Hard':
        wch_bank = random.choice(
            ['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs',
             'red_signs', 'blue_signs', 'moon'])
        mystate.emoji_bank = locals()[wch_bank]

    mystate.plyrbtns = {}
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)): mystate.plyrbtns[vcell] = {'isPressed': False,
                                                                                               'isTrueFalse': False,
                                                                                               'eMoji': ''}


# Define los emojis que se van a utilizar dependiendo del puntaje obtenido
def ScoreEmoji():
    if mystate.myscore == 0:
        return '😐'
    elif -5 <= mystate.myscore <= -1:
        return '😏'
    elif -10 <= mystate.myscore <= -6:
        return '☹️'
    elif mystate.myscore <= -11:
        return '😖'
    elif 1 <= mystate.myscore <= 5:
        return '🙂'
    elif 6 <= mystate.myscore <= 10:
        return '😊'
    elif mystate.myscore > 10:
        return '😁'


# Inicializa el juego
def NewGame():
    ResetBoard()
    total_cells_per_row_or_col = mystate.GameDetails[2]

    # Define el dseño del juego e inicializando las variables
    ReduceGapFromPageTop('sidebar')
    with st.sidebar:
        st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")
        st.markdown(horizontal_bar, True)

        st.markdown(sbe.replace('|fill_variable|', mystate.sidebar_emoji), True)

        aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr")
        if aftimer > 0: mystate.myscore -= 1

        st.info(
            f"{ScoreEmoji()} Score: {mystate.myscore} | Pending: {(total_cells_per_row_or_col ** 2) - len(mystate.expired_cells)}")

        st.markdown(horizontal_bar, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            mystate.runpage = Main
            st.rerun()

    Leaderboard('read')
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    # Set Board Defaults
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ",
                unsafe_allow_html=True)  # make button face big

    for i in range(1, (total_cells_per_row_or_col + 1)):
        tlst = ([1] * total_cells_per_row_or_col) + [2]  # 2 = rt side padding
        globals()['cols' + str(i)] = st.columns(tlst)

    # Reemplaza las celdas con cada uno de los emojis
    for vcell in range(1, (total_cells_per_row_or_col ** 2) + 1):
        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0

        elif ((total_cells_per_row_or_col * 1) + 1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)

        elif ((total_cells_per_row_or_col * 2) + 1) <= vcell <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)

        elif ((total_cells_per_row_or_col * 3) + 1) <= vcell <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)

        elif ((total_cells_per_row_or_col * 4) + 1) <= vcell <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)

        elif ((total_cells_per_row_or_col * 5) + 1) <= vcell <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)

        elif ((total_cells_per_row_or_col * 6) + 1) <= vcell <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)

        elif ((total_cells_per_row_or_col * 7) + 1) <= vcell <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)

        elif ((total_cells_per_row_or_col * 8) + 1) <= vcell <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)

        elif ((total_cells_per_row_or_col * 9) + 1) <= vcell <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)

        # Ahora dependiendo de si el emoji presionado es el correcto, este se reemplaza con una x o una flecha
        globals()['cols' + arr_ref][vcell - mval] = globals()['cols' + arr_ref][vcell - mval].empty()
        if mystate.plyrbtns[vcell]['isPressed'] == True:
            if mystate.plyrbtns[vcell]['isTrueFalse'] == True:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '✅️'), True)

            elif mystate.plyrbtns[vcell]['isTrueFalse'] == False:
                globals()['cols' + arr_ref][vcell - mval].markdown(pressed_emoji.replace('|fill_variable|', '❌'), True)

        else:
            vemoji = mystate.plyrbtns[vcell]['eMoji']
            globals()['cols' + arr_ref][vcell - mval].button(vemoji, on_click=PressedCheck, args=(vcell,),
                                                             key=f"B{vcell}")

    st.caption('')  # vertical filler
    st.markdown(horizontal_bar, True)

    # Verifica si perdio
    Perder()
    # Si ya se han utilizado todas las celdas entonces dependiendo de si el puntaje es positivo o negativo, se gana o se pierde
    if len(mystate.expired_cells) == (total_cells_per_row_or_col ** 2):
        Leaderboard('write')

        if mystate.myscore > 0:
            st.balloons()
        elif mystate.myscore <= 0:
            st.snow()

        tm.sleep(5)
        mystate.runpage = Main
        st.rerun()


# El main el cual muestra la pagina inicial y define la dificultad original
def Main():
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>',
                unsafe_allow_html=True, )  # reduce sidebar width
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    # Empieza mostrano los niveles de dificultad disponibles, al igual que el nombre del jugador
    InitialPage()
    with st.sidebar:
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1,
                                          horizontal=True, )
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India',
                                               help='Optional input only for Leaderboard')

        # Dependiendo de la dificultad que eliga el jugador se inicializa con un intervalo de segundos especifico y de puntos
        if st.button(f"🕹️ New Game", use_container_width=True):

            if mystate.GameDetails[0] == 'Easy':
                mystate.GameDetails[1] = 8  # secs interval
                mystate.GameDetails[2] = 6  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Medium':
                mystate.GameDetails[1] = 6  # secs interval
                mystate.GameDetails[2] = 7  # total_cells_per_row_or_col

            elif mystate.GameDetails[0] == 'Hard':
                mystate.GameDetails[1] = 5  # secs interval
                mystate.GameDetails[2] = 8  # total_cells_per_row_or_col

            # Crea el tablero
            Leaderboard('create')

            # Llama a la funcion PreNewGame para preparar la pantalla para el juego
            PreNewGame()
            # Llama la funcion NewGame para empezar el juego
            mystate.runpage = NewGame

            # Corre con streamlit
            st.rerun()

        st.markdown(horizontal_bar, True)


if 'runpage' not in mystate: mystate.runpage = Main
mystate.runpage()