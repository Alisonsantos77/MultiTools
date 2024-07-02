import flet as ft
from pages.weather import Weather
from pages.youtube import Youtube
from pages.speed import Speed


def main(page: ft.Page):
    # Refs
    icone_tema = ft.Ref[ft.IconButton]()
    icone_menu = ft.Ref[ft.IconButton]()

    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True

    def change_route(e):
        match e.control.selected_index:
            case 0:
                page.go('/')
            case 1:
                page.go('/youtube')
            case 2:
                page.go('/weather')

    def abrir_menu(e):
        menu.open = True
        page.update()

    def troca_tema(e):
        e.page.theme_mode = (
            ft.ThemeMode.DARK if e.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        e.page.update()

    def change_color_scheme(e):
        selected_color = e.control.selected
        if "red" in selected_color:
            page.theme = ft.colors.RED
            page.theme = ft.Theme(
                color_scheme=ft.ColorScheme(primary=ft.colors.RED))
        elif "blue" in selected_color:
            page.theme = ft.colors.BLUE
            page.theme = ft.Theme(
                color_scheme=ft.ColorScheme(primary=ft.colors.BLUE))
        elif "green" in selected_color:
            page.theme = ft.colors.GREEN
            page.theme = ft.Theme(
                color_scheme=ft.ColorScheme(primary=ft.colors.GREEN))
        page.update()

    def confirm_close_window(e):
        close_dialog.open = True
        page.update()

    def cancel_close_window(e):
        close_dialog.open = False
        page.update()

    def close_window(e):
        page.window.close()
        page.update()

    def open_dialog(e):
        dlg.open = True
        page.update()

    def close_dialog(e):
        dlg.open = False
        page.update()

    def minimize_window(e):
        page.window.minimized = True
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Row(
            [
                ft.Text("Fale conosco", size=24,
                        weight=ft.FontWeight.BOLD, expand=1),
                ft.IconButton(
                    icon=ft.icons.CLOSE,
                    tooltip="Fechar",
                    on_click=close_dialog,
                    icon_color=ft.colors.RED,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        actions=[
            ft.IconButton(
                content=ft.Image(src='images/whatsapp-logo.png',
                                 width=40, height=40),
                icon_color=ft.colors.GREEN,
                tooltip="Abrir Whatsapp",
                url="https://wa.link/oebrg2",
                style=ft.ButtonStyle(
                    overlay_color={"": ft.colors.TRANSPARENT,
                                   "hovered": ft.colors.LIGHT_GREEN_200},
                )
            ),
            ft.IconButton(
                content=ft.Image(
                    src='images/microsoft-outlook-logo.png', width=40, height=40),
                icon_color=ft.colors.BLUE,
                tooltip="Enviar Email",
                url="mailto:Alisondev77@hotmail.com?subject=Feedback%20-%20MultiTools&body=Ol%C3%A1,"
                    "%20equipe!%20Gostaria%20de%20fornecer%20feedback%20sobre%20o%20aplicativo%20MultiTools.%20["
                    "Descreva%20o%20feedback].%20Obrigado("
                    "a)%20pela%20oportunidade%20de%20compartilhar%20minha%20opini%C3%A3o.",
                style=ft.ButtonStyle(
                    overlay_color={"": ft.colors.TRANSPARENT,
                                   "hovered": ft.colors.LIGHT_BLUE_200},
                )
            ),
            ft.IconButton(
                content=ft.Image(src='images/linkedin-logo.png',
                                 width=40, height=40),
                icon_color=ft.colors.BLUE,
                tooltip="Acessar Linkedin",
                url="www.linkedin.com/in/alisonsantosdev",
                style=ft.ButtonStyle(
                    overlay_color={"": ft.colors.TRANSPARENT,
                                   "hovered": ft.colors.LIGHT_BLUE_200},
                )
            ),
            ft.IconButton(
                content=ft.Image(src='images/github-logo.png',
                                 width=40, height=40),
                icon_color=ft.colors.GREY,
                tooltip="Acessar Github",
                url="https://github.com/Alisonsantos77",
                style=ft.ButtonStyle(
                    overlay_color={"": ft.colors.TRANSPARENT,
                                   "hovered": ft.colors.GREY_300},
                )
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )

    page.overlay.append(dlg)

    menu = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Multi Tools", size=30,
                                weight=ft.FontWeight.W_900),
                        ft.Icon(ft.icons.SETTINGS, size=30),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.all(10),
            ),
            ft.Divider(height=2),
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label='Speed Net',
                icon=ft.icons.SPEED,
                selected_icon_content=ft.FilledButton(text="Abrir")  # 0
            ),
            ft.NavigationDrawerDestination(
                label='Youtube Downloader',
                icon=ft.icons.CLOUD_DOWNLOAD_OUTLINED,
                selected_icon_content=ft.FilledButton(text="Abrir")  # 1
            ),
            ft.NavigationDrawerDestination(
                label='Weather Now',
                icon=ft.icons.WATER_DROP_OUTLINED,
                selected_icon_content=ft.FilledButton(text="Abrir")  # 2
            ),
            ft.Divider(height=2),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Tema", size=18, weight=ft.FontWeight.W_600,
                                color=ft.colors.GREY_700),
                        ft.SegmentedButton(
                            on_change=change_color_scheme,
                            selected={"red"},
                            segments=[
                                ft.Segment(
                                    value="red",
                                    label=ft.Text("Red", color=ft.colors.RED),
                                    icon=ft.Icon(ft.icons.PALETTE,
                                                 color=ft.colors.RED)
                                ),
                                ft.Segment(
                                    value="blue",
                                    label=ft.Text(
                                        "Blue", color=ft.colors.BLUE),
                                    icon=ft.Icon(ft.icons.PALETTE,
                                                 color=ft.colors.BLUE)
                                ),
                                ft.Segment(
                                    value="green",
                                    label=ft.Text(
                                        "Green", color=ft.colors.GREEN),
                                    icon=ft.Icon(ft.icons.PALETTE,
                                                 color=ft.colors.GREEN)
                                ),
                            ],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                ),
                padding=ft.padding.all(10),
            ),
            ft.Divider(height=2),
            # Seção "Me Conheça Mais" e "Suporte"
            ft.Container(
                content=ft.ElevatedButton(
                    "Fale com o suporte.",
                    icon=ft.icons.HEADSET,
                    on_click=open_dialog,
                ),
                padding=ft.padding.all(10),
            ),
            ft.Container(
                content=ft.Text(
                    "Desenvolvido por Alison Santos",
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color=ft.colors.GREY_600,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.all(10),
            ),
        ],
        tile_padding=ft.padding.all(5),
        on_change=change_route,
    )

    close_dialog = ft.AlertDialog(
        content=ft.Row(
            controls=[
                ft.Icon(ft.icons.WARNING, color=ft.colors.RED, size=30),
                ft.Text(
                    value="Tem certeza que deseja fechar o aplicativo?",
                    size=16,
                    color=ft.colors.RED
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        actions=[
            ft.TextButton(
                "Certeza",
                on_click=close_window,
                style=ft.ButtonStyle(color=ft.colors.RED)
            ),
            ft.TextButton(
                "Cancelar",
                on_click=cancel_close_window,
                style=ft.ButtonStyle(color=ft.colors.WHITE)
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        elevation=10,
    )

    # Adicionando o diálogo à sobreposição da página
    page.overlay.append(close_dialog)

    # Atualizando o AppBar
    appbar_menu = ft.AppBar(
        toolbar_height=50,
        color=ft.colors.INVERSE_PRIMARY,
        leading=ft.WindowDragArea(
            ft.Container(
                content=ft.IconButton(
                    ref=icone_menu, icon=ft.icons.MENU, on_click=abrir_menu),
                padding=ft.padding.all(10),
            )
        ),
        actions=[
            ft.WindowDragArea(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.DARK_MODE,
                                ref=icone_tema,
                                on_click=troca_tema,
                                tooltip="Modo Escuro",
                            ),
                            ft.IconButton(
                                icon=ft.icons.MINIMIZE,
                                on_click=minimize_window,
                                tooltip="Minimizar",
                            ),
                            ft.IconButton(
                                icon=ft.icons.CLOSE,
                                on_click=confirm_close_window,
                                tooltip="Fechar",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,  # Alinhamento à direita
                    ),
                    padding=ft.padding.symmetric(horizontal=10),
                    expand=True,
                )
            ),
        ],
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                route='/',
                appbar=appbar_menu,
                drawer=menu,
                controls=[
                    Speed(page)
                ],
            )
        )
        if page.route == '/weather':
            page.views.append(
                ft.View(
                    route='/weather',
                    appbar=appbar_menu,
                    drawer=menu,
                    controls=[
                        Weather(page)
                    ],
                )
            )
        if page.route == '/youtube':
            page.views.append(
                ft.View(
                    route='/youtube',
                    appbar=appbar_menu,
                    drawer=menu,
                    controls=[
                        Youtube(page)
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(main)
