import flet as ft
import aiohttp
from icecream import ic
from typing import Any


def Weather(page: ft.Page):

    key_weather = "##################"


    #Refs
    ClimaNowText = ft.Ref[ft.Text]()
    TempNowText = ft.Ref[ft.Text]()
    ImageNow = ft.Ref[ft.Image]()
    IconHours = ft.Ref[ft.Image]()
    CityName = ft.Ref[ft.TextSpan]()
    RowCards = ft.Ref[ft.Row]()

    def resize(e):
        print(page.window.width)
    page.window.on_resized = resize


    async def WeatherNow(e):
        cidade = input_city.value
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade.capitalize()}&units='metric'&appid={key_weather}&lang=pt_br"
        # Função assincrona usando aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    result: dict[str, Any] = await response.json()
                    ic(result)
                    icone = result['weather'][0]['icon']
                    ImageNow.current.src = f'https://openweathermap.org/img/wn/{icone}@2x.png'
                    ImageNow.current.update()
                    weather = result['weather'][0]['main']
                    temperature = result['main']['temp'] - 273.15
                    city = result['name']
                    CityName.current.text = f'{city}'
                    CityName.current.update()
                    ClimaNowText.current.value = f'{weather}'
                    ClimaNowText.current.update()
                    TempNowText.current.value = f'{temperature:.0f}°C'
                    TempNowText.current.update()
                    ic(f'{city} está {weather} com aproximadamente {temperature}')
                else:
                    print(f"Erro na requisição: {response.status}")

    return ft.Container(
        # bgcolor=ft.colors.PURPLE_100,
        padding=50,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=
            [
                ft.ResponsiveRow(
                    run_spacing=100,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            # bgcolor='red',
                            content=
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Image(
                                        ref=ImageNow,
                                        src='/images/iconesWeather/lua.png',
                                        width=200,
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                                    ft.Column(
                                        controls=
                                        [
                                            ft.Text(
                                                ref=ClimaNowText,
                                                value='Céu limpo',
                                                theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                                size=24,
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                            ft.Text(
                                                ref=TempNowText,
                                                value='29',
                                                theme_style=ft.TextThemeStyle.DISPLAY_LARGE,
                                                weight=ft.FontWeight.BOLD,
                                                text_align=ft.TextAlign.CENTER,
                                                size=36
                                            )
                                        ]),
                                ]),
                        ),
                        ft.ResponsiveRow(
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        input_city := ft.TextField(
                                            col={'xs': 12, 'md': 6},
                                            hint_text='Insira sua cidade'),
                                        ft.IconButton(
                                            icon=ft.icons.YOUTUBE_SEARCHED_FOR_OUTLINED,
                                            on_click=WeatherNow,
                                            tooltip='Pesquisar'
                                        ),
                                    ]
                                ),
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(
                                            'Buscando:',
                                            ft.TextStyle(size=18),
                                        ),
                                        ft.TextSpan(
                                            ref=CityName,
                                        ),
                                    ]
                                )
                            ],
                        ),
                        ft.Container(
                            # bgcolor='orange',
                            content=
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ref=RowCards,
                                # scroll=ft.ScrollMode.HIDDEN,
                                controls=[
                                    ft.Container(
                                        padding=ft.padding.all(5),
                                        col={'xs': 12, 'sm': 6},
                                        height=200,
                                        width=150,
                                        border_radius=ft.border_radius.all(20),
                                        alignment=ft.alignment.center,
                                        content=ft.Column(
                                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                            controls=[
                                                ft.ResponsiveRow(
                                                    controls=[
                                                        ft.Text(
                                                            spans=[
                                                                ft.TextSpan(
                                                                    '9',
                                                                    ft.TextStyle(size=20),
                                                                ),
                                                                ft.TextSpan(
                                                                    'AM',
                                                                    ft.TextStyle(size=16)
                                                                )
                                                            ],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                    ],
                                                ),
                                                ft.ResponsiveRow(
                                                    spacing=10,
                                                    controls=[
                                                        ft.Row(
                                                            col={'xs': 12, 'sm': 6},
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            controls=[
                                                                ft.Image(
                                                                    ref=IconHours,
                                                                    src='/images/iconesWeather/nuvens.png',
                                                                    width=50,
                                                                    height=50,
                                                                    fit=ft.ImageFit.CONTAIN,
                                                                ),
                                                            ]),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            col={'xs': 12, 'sm': 6},
                                                            controls=[
                                                                ft.Text(
                                                                    '28',
                                                                    size=24,
                                                                    weight=ft.FontWeight.BOLD,
                                                                    text_align=ft.TextAlign.CENTER,
                                                                )
                                                            ]),
                                                    ]),
                                            ]
                                        )
                                    ),
                                    ft.Container(
                                        padding=ft.padding.all(5),
                                        col={'xs': 12, 'sm': 6},
                                        height=200,
                                        width=150,
                                        border_radius=ft.border_radius.all(20),
                                        alignment=ft.alignment.center,
                                        content=ft.Column(
                                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                            controls=[
                                                ft.ResponsiveRow(
                                                    controls=[
                                                        ft.Text(
                                                            spans=[
                                                                ft.TextSpan(
                                                                    '10',
                                                                    ft.TextStyle(size=20),
                                                                ),
                                                                ft.TextSpan(
                                                                    'AM',
                                                                    ft.TextStyle(size=16)
                                                                )
                                                            ],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                    ],
                                                ),
                                                ft.ResponsiveRow(
                                                    spacing=10,
                                                    controls=[
                                                        ft.Row(
                                                            col={'xs': 12, 'sm': 6},
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            controls=[
                                                                ft.Image(
                                                                    ref=IconHours,
                                                                    src='/images/iconesWeather/sol_nuvem.png',
                                                                    width=50,
                                                                    height=50,
                                                                    fit=ft.ImageFit.CONTAIN,
                                                                ),
                                                            ]),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            col={'xs': 12, 'sm': 6},
                                                            controls=[
                                                                ft.Text(
                                                                    '19',
                                                                    size=24,
                                                                    weight=ft.FontWeight.BOLD,
                                                                    text_align=ft.TextAlign.CENTER,
                                                                )
                                                            ]),
                                                    ]),
                                            ]
                                        )
                                    ),
                                    ft.Container(
                                        padding=ft.padding.all(5),
                                        col={'xs': 12, 'sm': 6},
                                        height=200,
                                        width=150,
                                        border_radius=ft.border_radius.all(20),
                                        alignment=ft.alignment.center,
                                        content=ft.Column(
                                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                            controls=[
                                                ft.ResponsiveRow(
                                                    controls=[
                                                        ft.Text(
                                                            spans=[
                                                                ft.TextSpan(
                                                                    '11',
                                                                    ft.TextStyle(size=20),
                                                                ),
                                                                ft.TextSpan(
                                                                    'AM',
                                                                    ft.TextStyle(size=16)
                                                                )
                                                            ],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                    ],
                                                ),
                                                ft.ResponsiveRow(
                                                    spacing=10,
                                                    controls=[
                                                        ft.Row(
                                                            col={'xs': 12, 'sm': 6},
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            controls=[
                                                                ft.Image(
                                                                    ref=IconHours,
                                                                    src='/images/iconesWeather/nuvens.png',
                                                                    width=50,
                                                                    height=50,
                                                                    fit=ft.ImageFit.CONTAIN,
                                                                ),
                                                            ]),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            col={'xs': 12, 'sm': 6},
                                                            controls=[
                                                                ft.Text(
                                                                    '24',
                                                                    size=24,
                                                                    weight=ft.FontWeight.BOLD,
                                                                    text_align=ft.TextAlign.CENTER,
                                                                )
                                                            ]),
                                                    ]),
                                            ]
                                        )
                                    ),
                                    ft.Container(
                                        padding=ft.padding.all(5),
                                        col={'xs': 12, 'sm': 6},
                                        height=200,
                                        width=150,
                                        border_radius=ft.border_radius.all(20),
                                        alignment=ft.alignment.center,
                                        content=ft.Column(
                                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                            controls=[
                                                ft.ResponsiveRow(
                                                    controls=[
                                                        ft.Text(
                                                            spans=[
                                                                ft.TextSpan(
                                                                    '12',
                                                                    ft.TextStyle(size=20),
                                                                ),
                                                                ft.TextSpan(
                                                                    'AM',
                                                                    ft.TextStyle(size=16)
                                                                )
                                                            ],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                    ],
                                                ),
                                                ft.ResponsiveRow(
                                                    spacing=10,
                                                    controls=[
                                                        ft.Row(
                                                            col={'xs': 12, 'sm': 6},
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            controls=[
                                                                ft.Image(
                                                                    ref=IconHours,
                                                                    src='/images/iconesWeather/sol.png',
                                                                    width=50,
                                                                    height=50,
                                                                    fit=ft.ImageFit.CONTAIN,
                                                                ),
                                                            ]),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            col={'xs': 12, 'sm': 6},
                                                            controls=[
                                                                ft.Text(
                                                                    '25',
                                                                    size=24,
                                                                    weight=ft.FontWeight.BOLD,
                                                                    text_align=ft.TextAlign.CENTER,
                                                                )
                                                            ]),
                                                    ]),
                                            ]
                                        )
                                    ),
                                    ft.Container(
                                        padding=ft.padding.all(5),
                                        col={'xs': 12, 'sm': 6},
                                        height=200,
                                        width=150,
                                        border_radius=ft.border_radius.all(20),
                                        alignment=ft.alignment.center,
                                        content=ft.Column(
                                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                            controls=[
                                                ft.ResponsiveRow(
                                                    controls=[
                                                        ft.Text(
                                                            spans=[
                                                                ft.TextSpan(
                                                                    '1',
                                                                    ft.TextStyle(size=20),
                                                                ),
                                                                ft.TextSpan(
                                                                    'PM',
                                                                    ft.TextStyle(size=16)
                                                                )
                                                            ],
                                                            text_align=ft.TextAlign.CENTER
                                                        ),
                                                    ],
                                                ),
                                                ft.ResponsiveRow(
                                                    spacing=10,
                                                    controls=[
                                                        ft.Row(
                                                            col={'xs': 12, 'sm': 6},
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            controls=[
                                                                ft.Image(
                                                                    ref=IconHours,
                                                                    src='/images/iconesWeather/chuva.png',
                                                                    width=50,
                                                                    height=50,
                                                                    fit=ft.ImageFit.CONTAIN,
                                                                ),
                                                            ]),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.CENTER,
                                                            col={'xs': 12, 'sm': 6},
                                                            controls=[
                                                                ft.Text(
                                                                    '26',
                                                                    size=24,
                                                                    weight=ft.FontWeight.BOLD,
                                                                    text_align=ft.TextAlign.CENTER,
                                                                )
                                                            ]),
                                                    ]),
                                            ]
                                        )
                                    ),
                                ]
                            )
                        ),
                    ]
                ),

            ]
        ))
