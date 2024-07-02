import os
import subprocess
import threading
import logging
import re
from time import sleep
import yt_dlp
import flet as ft

# Variável global para controle de cancelamento e gerenciamento de downloads
DOWNLOAD_CANCELED = False
CURRENT_DOWNLOAD_TYPE = None
DOWNLOAD_TYPE = None


def Youtube(page: ft.Page):
    page.title = "Youtube Downloader"
    page.window.height = 750
    page.window.width = 700
    page.window.max_height = 750
    page.window.max_width = 700

    SNACK_TEXT = ft.Ref[ft.Text]()
    def handle_resize(e):
        print(f"Window resized to: {page.window.width}x{page.window.height}")
        if page.window.height < 666.0:
            page.scroll = ft.ScrollMode.AUTO
            page.update()
        else:
            page.scroll = ft.ScrollMode.HIDDEN
            page.update()

    page.on_resized = handle_resize

    global DOWNLOAD_CANCELED, CURRENT_DOWNLOAD_TYPE

    # Variável para armazenar o caminho do diretório selecionado
    directory_selected = ft.Text(visible=False)

    # Variáveis para armazenar o progresso do download e o nome do arquivo
    barra_progress_video = ft.ProgressBar(
        width=300,
        col=8,
        bgcolor=ft.colors.GREY_200,
        color=ft.colors.RED,
        visible=False
    )
    barra_progress_audio = ft.ProgressBar(
        width=300,
        col=8,
        bgcolor=ft.colors.RED_900,
        color=ft.colors.WHITE,
        visible=False
    )

    # Função para tratar o resultado da seleção do diretório
    def get_directory_result(e: ft.FilePickerResultEvent):
        directory_selected.value = e.path if e.path else "Nenhum diretório selecionado!"
        directory_selected.update()
        if directory_selected.value != "Nenhum diretório selecionado!":
            if CURRENT_DOWNLOAD_TYPE == 'video':
                threading.Thread(target=download_video).start()
            elif CURRENT_DOWNLOAD_TYPE == 'audio':
                threading.Thread(target=download_audio).start()

    # Configuração do diálogo de seleção de diretório
    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)

    # Função para abrir o diálogo de seleção de diretório
    def abrir_diretorio(e, DOWNLOAD_TYPE):
        global CURRENT_DOWNLOAD_TYPE
        CURRENT_DOWNLOAD_TYPE = DOWNLOAD_TYPE
        get_directory_dialog.get_directory_path()

    # Adicionar o diálogo de seleção de diretório à sobreposição da página
    page.overlay.append(get_directory_dialog)

    # Configuração do SnackBar
    snack_bar = ft.SnackBar(
        content=ft.Text(
            value='',
            ref=SNACK_TEXT,
            size=20,
            color=ft.colors.RED,
            weight=ft.FontWeight.W_600,
            italic=True
        ),
        bgcolor=ft.colors.WHITE,
        duration=4000  # Duração em milissegundos
    )
    # Adicionar o snackbar a sobreposição da página
    page.overlay.append(snack_bar)

    # Função para cancelar o download
    def cancel_download(e):
        global DOWNLOAD_CANCELED
        DOWNLOAD_CANCELED = True
        SNACK_TEXT.current.value = "Download cancelado!"
        SNACK_TEXT.current.color = ft.colors.WHITE
        SNACK_TEXT.current.update()
        snack_bar.bgcolor = ft.colors.RED_500
        snack_bar.open = True
        snack_bar.update()

    # Botão de cancelamento
    cancel_button_video = ft.ElevatedButton(
        text="Cancelar Download",
        icon=ft.icons.CANCEL,
        bgcolor=ft.colors.RED_500,
        color=ft.colors.WHITE,
        on_click=cancel_download,
        visible=False
    )
    # Botão de cancelamento
    cancel_button_audio = ft.ElevatedButton(
        text="Cancelar Download",
        icon=ft.icons.CANCEL,
        bgcolor=ft.colors.WHITE,
        color=ft.colors.RED,
        on_click=cancel_download,
        visible=False
    )

    def progress_hook(d):
        if DOWNLOAD_CANCELED:
            raise Exception("Download cancelado pelo usuário")

        # Verificar tipo de download e atualizar a barra de progresso correspondente
        if d['status'] == 'downloading':
            if DOWNLOAD_TYPE == 'video':
                animacao_video.src = 'https://lottie.host/e0d71710-c179-44cc-bc43-7950c1ab9ffc/3yj7jiRrAx.json'
                animacao_video.update()
                input_text_video.disabled = True
                input_text_video.update()
                btn_download_video.disabled = True
                btn_download_video.update()
                barra_progress_video.visible = True
                barra_progress_video.value = float(
                    d['_percent_str'].strip('%')) / 100
                barra_progress_video.update()
                SNACK_TEXT.current.value = f"Baixando: {d['filename']}"
                SNACK_TEXT.current.color = ft.colors.RED
                SNACK_TEXT.current.update()
                snack_bar.bgcolor = ft.colors.WHITE
                snack_bar.open = True
                snack_bar.update()
            elif DOWNLOAD_TYPE == 'audio':
                input_text_audio.disabled = True
                input_text_audio.update()
                btn_download_audio.disabled = True
                btn_download_audio.update()
                barra_progress_audio.visible = True
                barra_progress_audio.value = float(
                    d['_percent_str'].strip('%')) / 100
                barra_progress_audio.update()
                SNACK_TEXT.current.value = f"Baixando: {d['filename']}"
                SNACK_TEXT.current.color = ft.colors.RED
                SNACK_TEXT.current.update()
                snack_bar.bgcolor = ft.colors.WHITE
                snack_bar.open = True
                snack_bar.update()
            # Lidar com o estado de finalização do download
        elif d['status'] == 'finished':
            if DOWNLOAD_TYPE == 'video':
                animacao_video.src = 'https://lottie.host/5b3e7b47-d1a0-4c7b-bc51-070d2e81b97b/6Az1KFy5OK.json'
                animacao_video.update()
                input_text_video.disabled = False
                input_text_video.update()
                btn_download_video.disabled = False
                btn_download_video.update()
                barra_progress_video.visible = False
                barra_progress_video.value = 1.0
                barra_progress_video.update()
            elif DOWNLOAD_TYPE == 'audio':
                input_text_audio.disabled = False
                input_text_audio.update()
                btn_download_audio.disabled = False
                btn_download_audio.update()
                barra_progress_audio.visible = False
                barra_progress_audio.value = 1.0
                barra_progress_audio.update()
            # Atualizar Snackbar ao concluir o download
            SNACK_TEXT.current.value = f"Download concluído: {d['filename']}"
            SNACK_TEXT.current.color = ft.colors.WHITE
            SNACK_TEXT.current.update()
            snack_bar.bgcolor = ft.colors.BLACK12
            snack_bar.open = True
            snack_bar.update()

    def is_valid_url(url):
        # Regex para verificar se é uma URL válida
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// ou https://
            # domínio
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # endereço de IP
            r'\[?[A-F0-9]*:[A-F0-9:]+]?)'  # endereço de IP versão 6
            r'(?::\d+)?'  # porta
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        # Verificar se a URL corresponde ao padrão e se pertence a um domínio permitido
        return re.match(regex, url) is not None and 'youtube.com' in url

    def download_video():
        global DOWNLOAD_CANCELED, DOWNLOAD_TYPE
        DOWNLOAD_CANCELED = False
        DOWNLOAD_TYPE = 'video'
        url = input_text_video.value
        if not url or not is_valid_url(url):
            input_text_video.color = ft.colors.RED
            input_text_video.update()
            sleep(2)
            input_text_video.value = ""
            input_text_video.color = ft.colors.BLACK
            input_text_video.update()
            SNACK_TEXT.current.value = "Por favor, insira um URL válido do YouTube."
            SNACK_TEXT.current.color = ft.colors.WHITE
            SNACK_TEXT.current.update()
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.open = True
            snack_bar.update()
            return

        # Indicar início do download
        SNACK_TEXT.current.value = "Download de vídeo iniciado. Por favor, aguarde enquanto baixamos o vídeo do YouTube."
        SNACK_TEXT.current.color = ft.colors.RED
        SNACK_TEXT.current.update()
        snack_bar.bgcolor = ft.colors.WHITE
        snack_bar.open = True
        snack_bar.update()

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{directory_selected.value}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook]
        }

        cancel_button_video.visible = True
        cancel_button_video.update()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if not DOWNLOAD_CANCELED:
                SNACK_TEXT.current.value = ("Download de vídeo concluído com sucesso! O arquivo foi salvo no diretório "
                                           "selecionado.")
                SNACK_TEXT.current.color = ft.colors.WHITE
                SNACK_TEXT.current.update()
                snack_bar.bgcolor = ft.colors.BLACK12
                snack_bar.open = True
                snack_bar.update()
                input_text_video.value = ""
                input_text_video.update()
                btn_folder_video.icon_color = ft.colors.RED
                btn_folder_video.disabled = False
                btn_folder_video.tooltip = "Ver downloads"
                btn_folder_video.update()
        except yt_dlp.DownloadError as yt_err:
            if DOWNLOAD_CANCELED:
                SNACK_TEXT.current.value = "Download cancelado pelo usuário."
            else:
                SNACK_TEXT.current.value = (f"Erro no download do vídeo: {str(yt_err)}. Verifique sua conexão à internet e "
                                       f"se o URL é acessível.")
            SNACK_TEXT.current.color = ft.colors.WHITE
            SNACK_TEXT.current.update()
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.open = True
            snack_bar.update()
        except Exception as ex:
            if DOWNLOAD_CANCELED:
                SNACK_TEXT.current.value = "Download cancelado pelo usuário."
            else:
                logging.error('Erro inesperado no vídeo: %s', str(ex))
                SNACK_TEXT.current.value = ('Erro inesperado no download de vídeo: %s. Por favor, tente novamente '
                                       'ou contate o suporte se o problema persistir.') % str(ex)
            SNACK_TEXT.current.color = ft.colors.WHITE
            SNACK_TEXT.current.update()
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.open = True
            snack_bar.update()
        finally:
            if DOWNLOAD_CANCELED:
                cancel_button_video.visible = False
                cancel_button_video.update()
            else:
                cancel_button_video.visible = False
                cancel_button_video.update()

    def download_audio():
        global DOWNLOAD_CANCELED, DOWNLOAD_TYPE
        DOWNLOAD_TYPE = 'audio'
        DOWNLOAD_CANCELED = False  # Reset the cancellation flag
        url_audio = input_text_audio.value
        if not url_audio or not is_valid_url(url_audio):
            SNACK_TEXT.current.value = "Por favor, insira um URL válido do YouTube."
            SNACK_TEXT.current.color = ft.colors.WHITE
            SNACK_TEXT.current.update()
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.open = True
            snack_bar.update()
            return

        # Indicar início do download
        SNACK_TEXT.current.value = "Download de áudio iniciado. Por favor, aguarde enquanto baixamos o áudio do YouTube."
        SNACK_TEXT.current.color = ft.colors.RED
        SNACK_TEXT.current.update()
        snack_bar.bgcolor = ft.colors.WHITE
        snack_bar.open = True
        snack_bar.update()

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{directory_selected.value}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook]
        }

        cancel_button_audio.visible = True
        cancel_button_audio.update()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_audio])
            if not DOWNLOAD_CANCELED:
                SNACK_TEXT.current.value = ("Download de áudio concluído com sucesso! O arquivo foi salvo no diretório "
                                           "selecionado.")
                SNACK_TEXT.current.color = ft.colors.WHITE
                SNACK_TEXT.current.update()
                snack_bar.bgcolor = ft.colors.BLACK12
                snack_bar.open = True
                snack_bar.update()
                input_text_audio.value = ""
                input_text_audio.update()
                btn_folder_audio.icon_color = ft.colors.WHITE
                btn_folder_audio.disabled = False
                btn_folder_audio.tooltip = "Ver aúdios"
                btn_folder_audio.update()
        except yt_dlp.DownloadError as yt_err:
            SNACK_TEXT.current.value = (f"Erro no download de áudio: {str(yt_err)}. Verifique sua conexão à internet e "
                                       f"se o URL é acessível.")
            SNACK_TEXT.current.color = ft.colors.WHITE
            SNACK_TEXT.current.update()
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.open = True
            snack_bar.update()
        except Exception as ex:
            logging.error('Erro inesperado no aúdio: %s', str(ex))
            SNACK_TEXT.current.value = ('Erro inesperado no download de áudio: %s. Por favor, tente novamente '
                                       'ou contate o suporte se o problema persistir.') % str(ex)
            SNACK_TEXT.current.color = ft.colors.WHITE    
            SNACK_TEXT.current.update()
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.open = True
            snack_bar.update()
        finally:
            snack_bar.open = True
            snack_bar.update()
            cancel_button_audio.visible = False
            cancel_button_audio.update()

    def abrir_diretorio_download(e):
        if directory_selected.value and os.path.isdir(directory_selected.value):
            path = os.path.realpath(directory_selected.value)
            if os.name == 'nt':
                subprocess.Popen(f'explorer "{path}"')
            elif os.name == 'posix':
                subprocess.Popen(['xdg-open', path])
        else:
            print("Diretório inválido ou não selecionado.")

    # Função para obter o texto do clipboard e definir no campo de texto
    def paste_video(e):
        clipboard_text = page.get_clipboard()
        input_text_video.value = clipboard_text
        input_text_video.update()

    def paste_audio(e):
        clipboard_text = page.get_clipboard()
        input_text_audio.value = clipboard_text
        input_text_audio.update()

    side_video = ft.Container(
        padding=ft.padding.all(30),
        bgcolor=ft.colors.WHITE,
        col={'xs': 12, 'sm': 6},
        aspect_ratio=9 / 16,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        animacao_video := ft.Lottie(
                            src='https://lottie.host/5b3e7b47-d1a0-4c7b-bc51-070d2e81b97b/6Az1KFy5OK.json',
                            width=250,
                            repeat=True,
                            reverse=False,
                            animate=True,

                        ),
                    ]
                ),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    col=12,
                    controls=[
                        barra_progress_video,
                    ]
                ),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    col=12,
                    spacing=10,
                    controls=[
                        input_text_video := ft.TextField(
                            hint_text='Insira seu link',
                            color=ft.colors.BLACK,
                            col=8,
                            text_size=18,
                            border=ft.InputBorder.UNDERLINE,
                            border_color=ft.colors.RED,
                        ),
                        ft.IconButton(
                            icon=ft.icons.CONTENT_PASTE,
                            col=2,
                            icon_color=ft.colors.RED,
                            tooltip="Colar do Clipboard",
                            on_click=paste_video,
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        btn_download_video := ft.FilledButton(
                            col=6,
                            text='Baixar',
                            icon='download',
                            on_click=lambda e: abrir_diretorio(e, 'video'),
                            icon_color=ft.colors.RED,
                            style=ft.ButtonStyle(
                                color=ft.colors.RED,
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor=ft.colors.TRANSPARENT
                            ),
                        ),
                        btn_folder_video := ft.IconButton(
                            col=6,
                            icon='folder_open',
                            icon_color=ft.colors.GREY,
                            disabled=True,
                            on_click=abrir_diretorio_download,
                            tooltip='Nenhuma pasta selecionada'
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        cancel_button_video
                    ]
                ),
                directory_selected,
            ]
        ),
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )

    side_audio = ft.Container(
        alignment=ft.alignment.center,
        bgcolor=ft.colors.BLACK45,
        col={'xs': 12, 'sm': 6},
        padding=ft.padding.all(30),
        aspect_ratio=9 / 16,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Image(
                            col={'xs': 10, 'sm': 6},
                            src='images/youtube_img/icon_song.png',
                            width=250,
                            fit=ft.ImageFit.CONTAIN
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            value='Baixe áudios/músicas',
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.RED_ACCENT,
                            size=24
                        ),
                    ]
                ),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        barra_progress_audio,
                    ]
                ),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    col=12,
                    spacing=10,
                    controls=[
                        input_text_audio := ft.TextField(
                            hint_text='Insira seu link',
                            color=ft.colors.BLACK,
                            col=8,
                            text_size=18,
                            border=ft.InputBorder.UNDERLINE,
                            border_color=ft.colors.RED,
                        ),
                        ft.IconButton(
                            icon=ft.icons.CONTENT_PASTE,
                            col=2,
                            icon_color=ft.colors.RED,
                            tooltip="Colar do Clipboard",
                            on_click=paste_audio,
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        btn_download_audio := ft.FilledButton(
                            col=6,
                            text='Baixar',
                            icon='download',
                            on_click=lambda e: abrir_diretorio(e, 'audio'),
                            icon_color=ft.colors.WHITE,
                            style=ft.ButtonStyle(
                                color=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor=ft.colors.TRANSPARENT
                            ),
                        ),
                        btn_folder_audio := ft.IconButton(
                            col=6,
                            icon='folder_open',
                            icon_color=ft.colors.GREY,
                            disabled=True,
                            on_click=abrir_diretorio_download,
                            tooltip='Nenhuma pasta selecionada'
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        cancel_button_audio
                    ]
                ),
            ]
        ),
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )

    return ft.Container(
        alignment=ft.alignment.center,
        margin=ft.margin.all(30),
        shadow=ft.BoxShadow(blur_radius=300, color=ft.colors.RED_ACCENT),
        content=ft.ResponsiveRow(
            columns=12,
            spacing=0,
            run_spacing=0,
            controls=[
                side_video,
                side_audio,
            ]
        )
    )
