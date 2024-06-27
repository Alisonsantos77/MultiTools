import flet as ft
import yt_dlp
import os
import subprocess


def Youtube(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO

    def resize_window(e=None):
        print(f"New window size: {page.window.width}, {page.window.height}")
        page.window.update()
    page.on_resized = resize_window


    # Variável para armazenar o caminho do diretório selecionado
    directory_selected = ft.Text(visible=False)

    # Variáveis para armazenar o progresso do download e o nome do arquivo
    barra_progress = ft.ProgressBar(width=300, bgcolor=ft.colors.GREY_200, color=ft.colors.RED, visible=False)

    # Função para tratar o resultado da seleção do diretório
    def get_directory_result(e: ft.FilePickerResultEvent):
        directory_selected.value = e.path if e.path else "Nenhum diretório selecionado!"
        directory_selected.update()
        if directory_selected.value != "Nenhum diretório selecionado!":
            download_video(None)
        close_dialog(None)

    # Configuração do diálogo de seleção de diretório
    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)

    # Função para abrir o diálogo de seleção de diretório
    def abrir_diretorio(e):
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

    def progress_hook(d):
        if d['status'] == 'downloading':
            barra_progress.visible = True
            barra_progress.update()
            barra_progress.value = float(d['_percent_str'].strip('%')) / 100
            snack_bar.content.value = f"Baixando: {d['filename']}"
            snack_bar.bgcolor = ft.colors.BLUE_500
            snack_bar.open = True
            snack_bar.update()
        elif d['status'] == 'finished':
            barra_progress.visible = False
            barra_progress.update()
            barra_progress.value = 1.0
            barra_progress.update()
            snack_bar.content.value = f"Baixando: {d['filename']}"
            snack_bar.update()
            snack_bar.content.value = f"Download concluído: {d['filename']}"
            snack_bar.bgcolor = ft.colors.GREEN_500
            snack_bar.open = True
            snack_bar.update()

    def download_video(e):
        url = input_text_video.value  # Obtém o URL do campo de texto
        if not url:
            snack_bar.content.value = "Por favor, insira um URL válido."
            snack_bar.open = True
            snack_bar.update()
            return

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{directory_selected.value}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook]  # Adiciona a função de hook de progresso
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            snack_bar.content.value = "Download concluído com sucesso!"
            snack_bar.bgcolor = ft.colors.GREEN_500
            input_text_video.value = ""
            input_text_video.update()
            btn_folder_video.icon_color = ft.colors.RED
            btn_folder_audio.icon_color = ft.colors.RED
            btn_folder_video.disabled = False
            btn_folder_audio.disabled = False
            btn_folder_video.update()
            btn_folder_audio.update()

        except Exception as ex:
            snack_bar.content.value = f"Erro no download: {str(ex)}"
            snack_bar.bgcolor = ft.colors.RED_500
        finally:
            snack_bar.open = True
            snack_bar.update()

    def open_dialog(e):
        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()

    def close_dialog(e):
        dlg_modal.open = False
        page.update()

    def abrir_diretorio_download(e):
        # Supondo que directory_selected.value contenha o caminho do diretório
        if directory_selected.value and os.path.isdir(directory_selected.value):
            path = os.path.realpath(directory_selected.value)
            if os.name == 'nt':  # Para Windows
                subprocess.Popen(f'explorer "{path}"')
            elif os.name == 'posix':  # Para Linux e macOS
                subprocess.Popen(['xdg-open', path])
        else:
            print("Diretório inválido ou não selecionado.")

    dlg_modal = ft.AlertDialog(
        modal=False,
        title=ft.Row(
            [
                ft.Text("Selecionar destino", size=24, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        content=ft.Text(
            "Por favor, escolha um diretório para salvar o vídeo.",
            size=18,
            color=ft.colors.BLACK,
        ),
        actions=[
            ft.TextButton("Escolher", on_click=abrir_diretorio, style=ft.ButtonStyle(color=ft.colors.GREEN)),
            ft.TextButton("Cancelar", on_click=close_dialog, style=ft.ButtonStyle(color=ft.colors.RED)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        content_padding=ft.padding.all(20),
        actions_padding=ft.padding.symmetric(horizontal=10, vertical=5),
        elevation=10,
    )

    side_video = ft.Container(
        padding=ft.padding.all(20),
        bgcolor=ft.colors.WHITE,
        col={'xs': 12, 'sm': 6},
        aspect_ratio=9 / 16,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            run_spacing=100,
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            col={'xs': 10, 'sm': 12},
                            controls=[
                                ft.Lottie(
                                    src='https://lottie.host/5b3e7b47-d1a0-4c7b-bc51-070d2e81b97b/6Az1KFy5OK.json',
                                    width=300,
                                    repeat=True,
                                    reverse=False,
                                    animate=True
                                )
                            ]
                        ),
                        ft.Row(
                            run_spacing=50,
                            col={'xs': 10, 'sm': 12},
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                barra_progress,
                            ]
                        ),
                        ft.ResponsiveRow(
                            alignment=ft.MainAxisAlignment.CENTER,
                            col={'xs': 10, 'sm': 12},
                            controls=[
                                ft.Column(
                                    col={'xs': 10, 'sm': 6},
                                    controls=[
                                        input_text_video := ft.TextField(
                                            col={'xs': 10, 'sm': 6},
                                            hint_text='Insira seu link',
                                            text_size=18,
                                            border=ft.InputBorder.UNDERLINE,
                                            border_color=ft.colors.RED,
                                        ),
                                        ft.ResponsiveRow(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=20,
                                            col={'xs': 10, 'sm': 6},
                                            controls=[
                                                ft.Row(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    controls=[
                                                        ft.FilledButton(
                                                            col=6,
                                                            text='Baixar',
                                                            icon='download',
                                                            on_click=open_dialog,
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
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        directory_selected
                    ]
                )
            ]
        ),
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )

    side_audio = ft.Container(
        bgcolor=ft.colors.BLACK45,
        col={'xs': 12, 'sm': 6},
        aspect_ratio=9 / 16,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            run_spacing=100,
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Column(
                                    col={'xs': 10, 'sm': 6},
                                    controls=[
                                        ft.Image(
                                            col={'xs': 10, 'sm': 6},
                                            src='images/youtube_img/icon_song.png',
                                            width=300,
                                            fit=ft.ImageFit.CONTAIN
                                        ),
                                        ft.Text(
                                            col={'xs': 10, 'sm': 6},
                                            value='Baixe áudios/músicas',
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.colors.RED_ACCENT,
                                            size=32
                                        ),
                                        input_text_audio := ft.TextField(
                                            col={'xs': 10, 'sm': 6},
                                            hint_text='Insira seu link',
                                            text_size=18,
                                            border=ft.InputBorder.UNDERLINE,
                                            border_color=ft.colors.RED,
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        ft.ResponsiveRow(
                            alignment=ft.MainAxisAlignment.CENTER,
                            col={'xs': 10, 'sm': 12},
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.FilledButton(
                                            col=6,
                                            text='Baixar',
                                            icon='download',
                                            on_click=open_dialog,
                                            icon_color=ft.colors.RED,
                                            style=ft.ButtonStyle(
                                                color=ft.colors.RED,
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                bgcolor=ft.colors.WHITE
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
                    ]
                )
            ]
        ),
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )
    return ft.Container(
        alignment=ft.alignment.center,
        margin=ft.margin.all(30),
        height=800,
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
