import flet as ft


def Weather(page: ft.Page):
    page.title = "Weather App"

    # Refs
    ClimaNowText = ft.Ref[ft.Text]()
    TempNowText = ft.Ref[ft.Text]()
    ImageNow = ft.Ref[ft.Image]()
    IconHours = ft.Ref[ft.Image]()
    CityName = ft.Ref[ft.TextSpan]()
    RowCards = ft.Ref[ft.Row]()
    UnitsSelector = ft.Ref[ft.Dropdown]()

    gl = ft.Geolocator()
    page.overlay.append(gl)

    def handle_get_current_position(e):
        position = gl.get_current_position()
        print(f"Posição Atual: ({position.latitude}, {position.longitude})")

    def handle_resize(e):
        print(f"Window resized to: {page.window.width}x{page.window.height}")
        if page.window.width <= 700:
            RowCards.current.scroll = ft.ScrollMode.HIDDEN
            RowCards.current.update()
            page.update()
        else:
            RowCards.current.scroll = None
            RowCards.current.update()
            page.update()

    page.on_resized = handle_resize

    return ft.Container(
        bgcolor=ft.colors.DEEP_PURPLE_300,
        padding=20,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Washington, DC, USA", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, color=ft.colors.BLACK,
                        size=30),
                ft.Text(
                    value="Tue, jun 30", size=20, color=ft.colors.GREY_700
                ),
                ft.ElevatedButton(
                    text="Coordenadas Geolocator",
                    on_click=handle_get_current_position
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                ft.Image(src="images/iconesWeather/chuva.png", width=150, height=200),
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            spans=[
                                                ft.TextSpan(
                                                    text="23",
                                                    style=ft.TextStyle(
                                                        size=70,
                                                        weight=ft.FontWeight.W_700,
                                                        color=ft.colors.GREY_900
                                                    )
                                                ),
                                                ft.TextSpan(
                                                    text="°C",
                                                    style=ft.TextStyle(
                                                        size=30,
                                                        weight=ft.FontWeight.W_600,
                                                        color=ft.colors.GREY_700
                                                    )
                                                ),
                                            ]
                                        ),
                                        ft.Text(
                                            value="Chuva forte", size=20, color=ft.colors.BLUE_GREY_700
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                ft.Container(
                    padding=20,
                    margin=10,
                    border_radius=30,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                padding=20,
                                margin=ft.margin.symmetric(horizontal=10),
                                border_radius=30,
                                bgcolor=ft.colors.WHITE54,
                                content=ft.ResponsiveRow(
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        ft.Container(
                                                            bgcolor=ft.colors.WHITE,
                                                            padding=10,
                                                            border_radius=20,
                                                            margin=10,
                                                            content=ft.Image(
                                                                src="images/iconesWeather/nuvem_raio.png",
                                                                width=50,
                                                                height=50),
                                                        ),
                                                        ft.Text(
                                                            value="RainFall", size=20,
                                                            color=ft.colors.BLUE_GREY_700,
                                                            weight=ft.FontWeight.W_600
                                                        ),
                                                    ]
                                                ),
                                                ft.Text(
                                                    value="100%", size=20, color=ft.colors.BLUE_GREY_700,
                                                    weight=ft.FontWeight.W_600

                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ),
                            ft.Container(
                                padding=20,
                                margin=ft.margin.symmetric(horizontal=10),
                                border_radius=30,
                                bgcolor=ft.colors.WHITE54,
                                content=ft.ResponsiveRow(
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        ft.Container(
                                                            bgcolor=ft.colors.WHITE,
                                                            padding=10, border_radius=20,
                                                            margin=10,
                                                            content=ft.Image(src="images/iconesWeather/gotas.png",
                                                                             width=50,
                                                                             height=50),
                                                        ),
                                                        ft.Text(
                                                            value="Humidity", size=20,
                                                            color=ft.colors.BLUE_GREY_700,
                                                            weight=ft.FontWeight.W_600
                                                        ),
                                                    ]
                                                ),
                                                ft.Text(
                                                    value="100%", size=20, color=ft.colors.BLUE_GREY_700,
                                                    weight=ft.FontWeight.W_600
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ),
                            ft.Container(
                                padding=20,
                                margin=ft.margin.symmetric(horizontal=10),
                                border_radius=30,
                                bgcolor=ft.colors.WHITE54,
                                content=ft.ResponsiveRow(
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Row(
                                                    controls=[
                                                        ft.Container(
                                                            bgcolor=ft.colors.WHITE,
                                                            padding=10,
                                                            border_radius=20,
                                                            margin=10,
                                                            content=ft.Image(src="images/iconesWeather/ventos.png",
                                                                             width=50,
                                                                             height=50),
                                                        ),
                                                        ft.Text(
                                                            value="Wind", size=20, color=ft.colors.BLUE_GREY_700,
                                                            weight=ft.FontWeight.W_600
                                                        ),
                                                    ]
                                                ),
                                                ft.Text(
                                                    value="11km/h", size=20, color=ft.colors.BLUE_GREY_700,
                                                    weight=ft.FontWeight.W_600
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ),

                        ]
                    )
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ref=RowCards,
                    controls=[
                        ft.Container(
                            bgcolor=ft.colors.WHITE60,
                            padding=25,
                            margin=10,
                            border_radius=50,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        value="00:00", size=20, color=ft.colors.GREY_700,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    ft.Image(
                                        src="images/iconesWeather/sol_nuvem.png",
                                        width=50,
                                        height=50,
                                    ),
                                    ft.Text(
                                        value="23°", size=24, color=ft.colors.BLACK,
                                        weight=ft.FontWeight.W_700
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            bgcolor=ft.colors.WHITE60,
                            padding=25,
                            margin=10,
                            border_radius=50,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        value="03:00", size=20, color=ft.colors.GREY_700,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    ft.Image(
                                        src="images/iconesWeather/chuva.png",
                                        width=50,
                                        height=50,
                                    ),
                                    ft.Text(
                                        value="28°", size=24, color=ft.colors.BLACK,
                                        weight=ft.FontWeight.W_700
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            bgcolor=ft.colors.WHITE60,
                            padding=25,
                            margin=10,
                            border_radius=50,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        value="06:00", size=20, color=ft.colors.GREY_700,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    ft.Image(
                                        src="images/iconesWeather/chuva_forte.png",
                                        width=50,
                                        height=50,
                                    ),
                                    ft.Text(
                                        value="30°", size=24, color=ft.colors.BLACK,
                                        weight=ft.FontWeight.W_700
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            bgcolor=ft.colors.WHITE60,
                            padding=25,
                            margin=10,
                            border_radius=50,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        value="09:00", size=20, color=ft.colors.GREY_700,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    ft.Image(
                                        src="images/iconesWeather/raio.png",
                                        width=50,
                                        height=50,
                                    ),
                                    ft.Text(
                                        value="34°", size=24, color=ft.colors.BLACK,
                                        weight=ft.FontWeight.W_700
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            bgcolor=ft.colors.WHITE60,
                            padding=25,
                            margin=10,
                            border_radius=50,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        value="12:00", size=20, color=ft.colors.GREY_700,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    ft.Image(
                                        src="images/iconesWeather/ventos.png",
                                        width=50,
                                        height=50,
                                    ),
                                    ft.Text(
                                        value="23°", size=24, color=ft.colors.BLACK,
                                        weight=ft.FontWeight.W_700
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            bgcolor=ft.colors.WHITE60,
                            padding=25,
                            margin=10,
                            border_radius=50,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        value="15:00", size=20, color=ft.colors.GREY_700,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    ft.Image(
                                        src="images/iconesWeather/sol_nuvem.png",
                                        width=50,
                                        height=50,
                                    ),
                                    ft.Text(
                                        value="22°", size=24, color=ft.colors.BLACK,
                                        weight=ft.FontWeight.W_700
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            bgcolor=ft.colors.WHITE60,
                            padding=25,
                            margin=10,
                            border_radius=50,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        value="18:00", size=20, color=ft.colors.GREY_700,
                                        weight=ft.FontWeight.W_600
                                    ),
                                    ft.Image(
                                        src="images/iconesWeather/nuvem_raio.png",
                                        width=50,
                                        height=50,
                                    ),
                                    ft.Text(
                                        value="23°", size=24, color=ft.colors.BLACK,
                                        weight=ft.FontWeight.W_700
                                    ),
                                ]
                            )
                        ),
                    ]
                ),
            ]
        )
    )
