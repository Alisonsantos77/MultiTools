import flet as ft
import speedtest
import threading


def Speed(page: ft.Page):

    def run_speed_test():
        try:
            btn_Start.visible = False
            btn_Start.update()
            loading.visible = True
            loading.update()

            snack_bar.content.value = "Teste de velocidade iniciado."
            snack_bar.open = True
            snack_bar.update()

            st = speedtest.Speedtest()  # Criar uma instância do Speedtest
            best_server = st.get_best_server()  # Encontrar o melhor servidor

            snack_bar.content.value = "Encontrando o melhor servidor..."
            snack_bar.open = True
            snack_bar.update()

            # Exibir detalhes do servidor selecionado
            server_info = f"Servidor: {best_server['host']} ({best_server['name']}, {best_server['country']})"
            print(server_info)
            snack_bar.content.value = f"Melhor servidor: {server_info}"
            snack_bar.open = True
            snack_bar.update()

            # Executa o teste de download
            snack_bar.content.value = "Iniciando teste de download..."
            snack_bar.open = True
            snack_bar.update()
            download_speed = st.download() / 1000000  # Convertendo para Mbps
            download_result.text = f"{download_speed:.2f} Mbps"
            download_result.update()
            print(download_result.text)
            # Atualiza o SnackBar após o teste de download
            snack_bar.content.value = "Teste de download concluído. Iniciando teste de upload..."
            snack_bar.open = True
            snack_bar.update()

            # Executa o teste de upload
            upload_speed = st.upload() / 1000000  # Convertendo para Mbps
            upload_result.text = f"{upload_speed:.2f} Mbps"
            upload_result.update()
            print(upload_result.text)
            # Concluir o teste e atualizar o SnackBar
            snack_bar.content.value = "Teste de velocidade concluído."
            snack_bar.bgcolor = ft.colors.GREEN_500
            snack_bar.open = True
            snack_bar.update()

            btn_Start.visible = True
            btn_Start.update()
            loading.visible = False
            loading.update()

        except Exception as e:
            snack_bar.content.value = f"Erro: {str(e)}"
            snack_bar.bgcolor = ft.colors.RED_500
            snack_bar.open = True
            snack_bar.update()

        # Fechar o SnackBar após alguns segundos
        def close_snackbar():
            snack_bar.open = False
            snack_bar.update()

        threading.Timer(4.0, close_snackbar).start()

    def start_test(e):
        threading.Thread(target=run_speed_test).start()

    def image_hover(e):
        imagem = e.control.content
        imagem.scale = ft.Scale(scale=1.2) if imagem.scale.scale == 1 else ft.Scale(scale=1)
        imagem.update()

    # Elementos da página
    download_result = ft.TextSpan("0.00 Mbps", style=ft.TextStyle(size=20))
    upload_result = ft.TextSpan("0.00 Mbps", style=ft.TextStyle(size=20))

    # Configuração do SnackBar
    snack_bar = ft.SnackBar(
        content=ft.Text(
            '',
            size=20,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.W_600,
            italic=True, ),
        bgcolor=ft.colors.BLUE_500,
        duration=4000  # Duração em milissegundos
    )

    page.overlay.append(snack_bar)

    loading = ft.Lottie(
            src='https://lottie.host/a05785c9-9e0a-4c0d-a13c-dfb322a8ac0c/RfzyzcV0QZ.json',
            repeat=True,
            reverse=False,
            animate=True,
            visible=False,
            height=400
        )

    speedtest_page = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.ResponsiveRow(
                columns=12,
                controls=[
                    btn_Start := ft.Container(
                        content=ft.Image(
                            col={'xs': 6, 'sm': 12},
                            src='/images/icone_home.png',
                            scale=ft.Scale(scale=1),
                            height=200,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        on_click=start_test,
                        padding=ft.padding.symmetric(vertical=100),
                        tooltip='Iniciar teste',
                        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_CUBIC),
                        on_hover=image_hover,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS
                    ),
                    ft.Container(
                        col=12,
                        alignment=ft.alignment.center,
                        content=loading
                    )
                ]),
            ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                columns=12,
                col={'xs': 10, 'sm': 12},
                controls=[
                    ft.Text(
                        col={'xs': 10, 'sm': 12},
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan("Velocidade de Download: ",
                                        style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=30)),
                            download_result
                        ]
                    ),
                    ft.Text(
                        col={'xs': 10, 'sm': 12},
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan("Velocidade de Upload: ",
                                        style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=30)),
                            upload_result
                        ]
                    )
                ]
            ),
        ]
    )

    return speedtest_page
