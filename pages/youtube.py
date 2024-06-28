import flet as ft
import yt_dlp
import os
import subprocess
import threading

# Variável global para controle de cancelamento e gerenciamento de downloads
download_canceled = False
current_download_type = None


def Youtube(page: ft.Page):
    global download_canceled, current_download_type
    page.scroll = ft.ScrollMode.AUTO

    # Variável para armazenar o caminho do diretório selecionado
    directory_selected = ft.Text(visible=False)

    # Variáveis para armazenar o progresso do download e o nome do arquivo
    barra_progress_video = ft.ProgressBar(width=300, bgcolor=ft.colors.GREY_200, color=ft.colors.RED, visible=False)
    barra_progress_audio = ft.ProgressBar(width=300, bgcolor=ft.colors.GREY_200, color=ft.colors.RED, visible=False)

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
            color=ft.colors.WHITE,
            weight=ft.FontWeight.W_600,
            italic=True
        ),
        bgcolor=ft.colors.BLUE_500,
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
        cancel_button.visible = False
        cancel_button.update()

    # Botão de cancelamento
    cancel_button = ft.ElevatedButton(
        text="Cancelar Download",
        icon=ft.icons.CANCEL,
        bgcolor=ft.colors.RED_500,
        color=ft.colors.WHITE,
        on_click=cancel_download,
        visible=False
    )

    def progress_hook(d):
        if download_canceled:
            raise Exception("Download cancelado pelo usuário")

        if d['status'] == 'downloading':
            barra_progress_video.visible = True
            barra_progress_video.update()
            barra_progress_video.value = float(d['_percent_str'].strip('%')) / 100
            snack_bar.content.value = f"Baixando: {d['filename']}"
            snack_bar.bgcolor = ft.colors.BLUE_500
            snack_bar.open = True
            snack_bar.update()
        elif d['status'] == 'finished':
            barra_progress_video.visible = False
            barra_progress_video.update()
            barra_progress_video.value = 1.0
            barra_progress_video.update()
            snack_bar.content.value = f"Baixando: {d['filename']}"
            snack_bar.update()
            snack_bar.content.value = f"Download concluído: {d['filename']}"
            snack_bar.bgcolor = ft.colors.GREEN_500
            snack_bar.open = True
            snack_bar.update()

    def download_video():
        global download_canceled
        download_canceled = False
        url = input_text_video.value
        if not url:
            snack_bar.content.value = "Por favor, insira um URL válido."
            snack_bar.open = True
            snack_bar.update()
            return

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{directory_selected.value}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook]
        }

        cancel_button.visible = True
        cancel_button.update()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if not download_canceled:
                snack_bar.content.value = "Download concluído com sucesso!"
                snack_bar.bgcolor = ft.colors.GREEN_500
                snack_bar.open = True
                snack_bar.update()
                input_text_video.value = ""
                input_text_video.update()
                btn_folder_video.icon_color = ft.colors.RED
                btn_folder_video.disabled = False
                btn_folder_video.update()
        except Exception as ex:
            snack_bar.content.value = f"Erro no download: {str(ex)}"
            snack_bar.bgcolor = ft.colors.RED_500
            snack_bar.open = True
            snack_bar.update()
        finally:
            cancel_button.visible = False
            cancel_button.update()

    def download_audio():
        global download_canceled
        download_canceled = False  # Reset the cancellation flag
        url_audio = input_text_audio.value
        if not url_audio:
            snack_bar.content.value = "Por favor, insira um URL válido."
            snack_bar.open = True
            snack_bar.update()
            return

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

        cancel_button.visible = True
        cancel_button.update()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_audio])
            if not download_canceled:
                snack_bar.content.value = "Download de áudio concluído com sucesso!"
                snack_bar.bgcolor = ft.colors.GREEN_500
                snack_bar.open = True
                snack_bar.update()
                input_text_audio.value = ""
                input_text_audio.update()
                btn_folder_audio.icon_color = ft.colors.RED
                btn_folder_audio.disabled = False
                btn_folder_audio.update()
        except Exception as ex:
            snack_bar.content.value = f"Erro no download: {str(ex)}"
            snack_bar.bgcolor = ft.colors.RED_500
            snack_bar.open = True
            snack_bar.update()
        finally:
            snack_bar.open = True
            snack_bar.update()
            cancel_button.visible = False
            cancel_button.update()

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
                            animate=True
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
                        ft.FilledButton(
                            col=6,
                            text='Baixar',
                            icon='download',
                            on_click=lambda e: abrir_diretorio(e, 'video'),
                            icon_color=ft.colors.RED,
                            style=ft.ButtonStyle(
                                color=ft.colors.RED,
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor=ft.colors.WHITE
                            ),
                        ),
                        btn_folder_video := ft.IconButton(
                            col=6,
                            icon='folder_open',
                            icon_color=ft.colors.GREY,
                            disabled=True,
                            on_click=abrir_diretorio_download
                        ),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        cancel_button
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
                        ft.FilledButton(
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
                            on_click=abrir_diretorio_download
                        ),
                    ]
                ),
            ]
        ),
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )

    return ft.Container(
        margin=ft.margin.all(30),
        shadow=ft.BoxShadow(blur_radius=300, color=ft.colors.RED_ACCENT),
        height=800,
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
