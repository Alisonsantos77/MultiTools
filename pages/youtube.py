import flet as ft
import yt_dlp
import os
import subprocess
import threading
import logging
import re

# Variável global para controle de cancelamento e gerenciamento de downloads
download_canceled = False
current_download_type = None
download_type = None


def Youtube(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO  # Habilita o scroll para todas as rotas
    page.title = "Youtube Downloader"

    global download_canceled, current_download_type

    # Variável para armazenar o caminho do diretório selecionado
    directory_selected = ft.Text(visible=False)

    # Variáveis para armazenar o progresso do download e o nome do arquivo
    barra_progress_video = ft.ProgressBar(width=300, bgcolor=ft.colors.GREY_200, color=ft.colors.RED, visible=False)
    barra_progress_audio = ft.ProgressBar(width=300, bgcolor=ft.colors.RED_900, color=ft.colors.WHITE, visible=False)

    # Função para tratar o resultado da seleção do diretório
    def get_directory_result(e: ft.FilePickerResultEvent):
        directory_selected.value = e.path if e.path else "Nenhum diretório selecionado!"
        directory_selected.update()
        if directory_selected.value != "Nenhum diretório selecionado!":
            if current_download_type == 'video':
                threading.Thread(target=download_video).start()
            elif current_download_type == 'audio':
                threading.Thread(target=download_audio).start()

    # Configuração do diálogo de seleção de diretório
    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)

    # Função para abrir o diálogo de seleção de diretório
    def abrir_diretorio(e, download_type):
        global current_download_type
        current_download_type = download_type
        get_directory_dialog.get_directory_path()

    # Adicionar o diálogo de seleção de diretório à sobreposição da página
    page.overlay.append(get_directory_dialog)

    # Configuração do SnackBar
    snack_bar = ft.SnackBar(
        content=ft.Text(
            '',
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
        global download_canceled
        download_canceled = True
        snack_bar.content.value = "Download cancelado!"
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
        if download_canceled:
            raise Exception("Download cancelado pelo usuário")

        # Verificar tipo de download e atualizar a barra de progresso correspondente
        if d['status'] == 'downloading':
            if download_type == 'video':
                input_text_video.disabled = True
                input_text_video.update()
                btn_download_video.disabled = True
                btn_download_video.update()
                barra_progress_video.visible = True
                barra_progress_video.value = float(d['_percent_str'].strip('%')) / 100
                barra_progress_video.update()
                snack_bar.content.value = f"Baixando: {d['filename']}"
                snack_bar.bgcolor = ft.colors.WHITE
                snack_bar.content.color = ft.colors.RED
                snack_bar.open = True
                snack_bar.update()
            elif download_type == 'audio':
                input_text_audio.disabled = True
                input_text_audio.update()
                btn_download_audio.disabled = True
                btn_download_audio.update()
                barra_progress_audio.visible = True
                barra_progress_audio.value = float(d['_percent_str'].strip('%')) / 100
                barra_progress_audio.update()
                snack_bar.content.value = f"Baixando: {d['filename']}"
                snack_bar.bgcolor = ft.colors.WHITE
                snack_bar.content.color = ft.colors.RED
                snack_bar.open = True
                snack_bar.update()
            # Lidar com o estado de finalização do download
        elif d['status'] == 'finished':
            if download_type == 'video':
                input_text_video.disabled = False
                input_text_video.update()
                btn_download_video.disabled = False
                btn_download_video.update()
                barra_progress_video.visible = False
                barra_progress_video.value = 1.0
                barra_progress_video.update()
            elif download_type == 'audio':
                input_text_audio.disabled = False
                input_text_audio.update()
                btn_download_audio.disabled = False
                btn_download_audio.update()
                barra_progress_audio.visible = False
                barra_progress_audio.value = 1.0
                barra_progress_audio.update()
            # Atualizar Snackbar ao concluir o download
            snack_bar.content.value = f"Download concluído: {d['filename']}"
            snack_bar.bgcolor = ft.colors.BLACK12
            snack_bar.content.color = ft.colors.WHITE
            snack_bar.open = True
            snack_bar.update()

    def is_valid_url(url):
        # Regex para verificar se é uma URL válida
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// ou https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domínio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # endereço de IP
            r'\[?[A-F0-9]*:[A-F0-9:]+]?)'  # endereço de IP versão 6
            r'(?::\d+)?'  # porta
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        # Verificar se a URL corresponde ao padrão e se pertence a um domínio permitido
        return re.match(regex, url) is not None and 'youtube.com' in url

    def download_video():
        global download_canceled, download_type
        download_canceled = False
        download_type = 'video'
        url = input_text_video.value
        if not url or not is_valid_url(url):
            snack_bar.content.value = "Por favor, insira um URL válido do YouTube."
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.content.color = ft.colors.WHITE
            snack_bar.open = True
            snack_bar.update()
            return

        # Indicar início do download
        snack_bar.content.value = "Download de vídeo iniciado..."
        snack_bar.bgcolor = ft.colors.WHITE
        snack_bar.content.color = ft.colors.RED
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
            if not download_canceled:
                snack_bar.content.value = "Download concluído com sucesso!"
                snack_bar.bgcolor = ft.colors.BLACK12
                snack_bar.content.color = ft.colors.WHITE
                snack_bar.open = True
                snack_bar.update()
                input_text_video.value = ""
                input_text_video.update()
                btn_folder_video.icon_color = ft.colors.RED
                btn_folder_video.disabled = False
                btn_folder_audio.tooltip = "Abrir pasta de áudio"
                btn_folder_video.update()
        except yt_dlp.DownloadError as yt_err:
            snack_bar.content.value = f"Erro no download do vídeo: {str(yt_err)}"
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.content.color = ft.colors.WHITE
            snack_bar.open = True
            snack_bar.update()
        except Exception as ex:
            logging.error(f"Erro inesperado: {str(ex)}")
            snack_bar.content.value = f"Erro inesperado: {str(ex)}"
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.content.color = ft.colors.WHITE
            snack_bar.open = True
            snack_bar.update()
        finally:
            cancel_button_video.visible = False
            cancel_button_video.update()

    def download_audio():
        global download_canceled, download_type
        download_type = 'audio'
        download_canceled = False  # Reset the cancellation flag
        url_audio = input_text_audio.value
        if not url_audio or not is_valid_url(url_audio):
            snack_bar.content.value = "Por favor, insira um URL válido do YouTube."
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.content.color = ft.colors.WHITE
            snack_bar.open = True
            snack_bar.update()
            return

        # Indicar início do download
        snack_bar.content.value = "Download do aúdio iniciado..."
        snack_bar.bgcolor = ft.colors.WHITE
        snack_bar.content.color = ft.colors.RED
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
            if not download_canceled:
                snack_bar.content.value = "Download de áudio concluído com sucesso!"
                snack_bar.bgcolor = ft.colors.BLACK12
                snack_bar.content.color = ft.colors.WHITE
                snack_bar.open = True
                snack_bar.update()
                input_text_audio.value = ""
                input_text_audio.update()
                btn_folder_audio.icon_color = ft.colors.WHITE
                btn_folder_audio.disabled = False
                btn_folder_audio.tooltip = "Abrir pasta de áudio"
                btn_folder_audio.update()
        except yt_dlp.DownloadError as yt_err:
            snack_bar.content.value = f"Erro no download de áudio: {str(yt_err)}"
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.content.color = ft.colors.WHITE
            snack_bar.open = True
            snack_bar.update()
        except Exception as ex:
            logging.error(f"Erro inesperado no aúdio: {str(ex)}")
            snack_bar.content.value = f"Erro inesperado no aúdio: {str(ex)}"
            snack_bar.bgcolor = ft.colors.RED_900
            snack_bar.content.color = ft.colors.WHITE
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
                        ft.Lottie(
                            src='https://lottie.host/5b3e7b47-d1a0-4c7b-bc51-070d2e81b97b/6Az1KFy5OK.json',
                            width=250,
                            repeat=True,
                            reverse=False,
                            animate=True,

                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        barra_progress_video,
                    ]
                ),
                input_text_video := ft.TextField(
                    col={'xs': 10, 'sm': 6},
                    hint_text='Insira seu link',
                    text_size=18,
                    border=ft.InputBorder.UNDERLINE,
                    border_color=ft.colors.RED,
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
                                bgcolor=ft.colors.TRANSPARENT,
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
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        barra_progress_audio,
                    ]
                ),
                input_text_audio := ft.TextField(
                    col={'xs': 10, 'sm': 6},
                    hint_text='Insira seu link',
                    text_size=18,
                    border=ft.InputBorder.UNDERLINE,
                    border_color=ft.colors.RED,
                    color=ft.colors.WHITE
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
