import flet as ft
from pages.weather import Weather
from pages.youtube import Youtube
from pages.speed import Speed


def main(page: ft.Page):
    # Refs
    icone_tema = ft.Ref[ft.IconButton]()

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

    menu = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Multi Tools", size=30, weight=ft.FontWeight.W_900),
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
            ft.Container(expand=True),
            ft.Divider(height=2),

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

    def troca_tema(e):
        e.page.theme_mode = (
            ft.ThemeMode.DARK if e.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        if e.page.theme_mode == ft.ThemeMode.DARK:
            icone_tema.current.icon = ft.icons.WB_SUNNY_SHARP
            icone_tema.current.update()
        else:
            icone_tema.current.icon = ft.icons.DARK_MODE_SHARP
            icone_tema.current.update()
        e.page.update()

    appbar_menu = ft.AppBar(
        toolbar_height=50,
        bgcolor=ft.colors.TRANSPARENT,
        color=ft.colors.INVERSE_PRIMARY,
        leading=ft.IconButton(ft.icons.MENU, on_click=abrir_menu),
        actions=[
            ft.IconButton(
                ft.icons.WB_SUNNY_OUTLINED,
                ref=icone_tema,
                on_click=troca_tema,
                icon_color=ft.colors.INVERSE_PRIMARY,
                padding=ft.padding.only(right=10),
            )
        ]
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                route='/',
                appbar=appbar_menu,
                drawer=menu,
                controls=
                [
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
                    controls=
                    [
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
                    controls=
                    [
                        Youtube(page)
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(main)
