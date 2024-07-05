import flet as ft
import requests
from icecream import ic
from datetime import datetime
import os
import logging


def Weather(page: ft.Page):
    page.title = "Weather App"
    key_weather = "xxxxxxxxxx"
    api_openweathermap = os.getenv("API_CLIMA")
    api_whatsapp = os.getenv("URL_WHATSAPP")
    print(f"{api_openweathermap} e {api_whatsapp}")
    # Refs
    ClimaNowText = ft.Ref[ft.Text]()
    TempNowText = ft.Ref[ft.Text]()
    ImageNow = ft.Ref[ft.Image]()
    IconHours = ft.Ref[ft.Image]()
    CityName = ft.Ref[ft.TextSpan]()
    RowCards = ft.Ref[ft.Row]()
    RowDays = ft.Ref[ft.Row]()

    gl = ft.Geolocator()
    page.overlay.append(gl)

    # Definir o dropdown para seleção de idioma
    LanguageSelector = ft.Dropdown(
        label="Idioma",
        hint_text="Escolha o idioma",
        options=[
            ft.dropdown.Option("pt_br", "Português"),
            ft.dropdown.Option("en", "Inglês"),
            ft.dropdown.Option("es", "Espanhol")
        ],
    )
    

    # Definir o dropdown para seleção de unidades
    UnitsSelector = ft.Dropdown(
        label="Unidade de Medida",
        hint_text="Escolha a unidade",
        options=[
            ft.dropdown.Option("metric", "Métrico (°C)"),
            ft.dropdown.Option("imperial", "Imperial (°F)"),
            ft.dropdown.Option("standard", "Padrão (K)")
        ],
    )

    def get_weather_by_input(e):
        from main import searchInput
        cidade = searchInput.value
        if not cidade:
            print("Por favor, digite um nome de cidade válido.")
            return
        lang = LanguageSelector.value
        units = UnitsSelector.value

        url_current = f"https://api.openweathermap.org/data/2.5/weather?q={cidade.capitalize()}&units={units}&appid={key_weather}&lang={lang}"
        try:
            response_current = requests.get(url_current)
            response_current.raise_for_status()
            data_current = response_current.json()
            ic(data_current)
            # Verificação de resposta
            if response_current.status_code != 200:
                logging.error(f"Falha na requisição: {response_current.status_code} - {response_current.reason}")
                return
            ic(data_current)
            if 'weather' in data_current and 'main' in data_current:
                # Data atual
                dateNow.value = datetime.now().strftime("%d/%m/%Y")
                dateNow.update()
                # Atualiza icone
                icone = data_current['weather'][0]['icon']
                iconeNow.src = f'https://openweathermap.org/img/wn/{icone}@2x.png'
                iconeNow.update()
                # Temperatura
                temp = data_current['main']['temp']
                unit_symbol = '°C' if units == 'metric' else '°F' if units == 'imperial' else 'K'
                temperatureNow.text = f'{temp:.0f}{unit_symbol}'
                temperatureNow.update()
                # Descrição do Clima
                weather_description = data_current['weather'][0]['description']
                descriptionNow.value = f"{weather_description.capitalize()}"
                descriptionNow.update()
                # Humidade
                humidity = data_current['main']['humidity']
                humidityValue.value = f"{humidity}%"
                humidityValue.update()
                # Velocidade do vento
                windspeed = data_current['wind']['speed']
                windSpeedValue.value = f"{windspeed} km/h"
                windSpeedValue.update()
                # Nome da cidade buscada
                cityName.value = data_current['name']
                cityName.update()
                # Verificar e exibir a quantidade de rainfall, se disponível
                if 'rain' in data_current:
                    rainfall = data_current['rain'].get('1h', 0)  # Obtém a precipitação da última hora, se disponível
                    max_rainfall = 10.0  # Valor de referência para cálculo da porcentagem
                    rainfall_percentage = (rainfall / max_rainfall) * 100
                    rainFallValue.value = f"{rainfall:.2f} mm"
                    rainFallValue.update()
                    logging.info(f"Rainfall: {rainfall}mm, which is {rainfall_percentage:.2f}% of the reference value.")
                else:
                    logging.info("No rainfall data available.")

                logging.info("Clima atualizado com sucesso!")
            else:
                logging.warning("Dados incompletos na resposta da API.")
        except requests.exceptions.RequestException as err:
            logging.error(f"Erro na requisição: {err}")

    def get_weather_by_coordinates(e):
        position = gl.get_current_position()
        lat = position.latitude
        lon = position.longitude
        url_coordinates = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key_weather}&units=metric&lang=pt_br"
        try:
            response_current = requests.get(url_coordinates)
            response_current.raise_for_status()
            data_current = response_current.json()
            ic(data_current)
            # Verificação de resposta
            if response_current.status_code != 200:
                logging.error(f"Falha na requisição: {response_current.status_code} - {response_current.reason}")
                return
            ic(data_current)
            if 'weather' in data_current and 'main' in data_current:
                # Data atual
                dateNow.value = datetime.now().strftime("%d/%m/%Y")
                dateNow.update()
                # Atualiza icone
                icone = data_current['weather'][0]['icon']
                iconeNow.src = f'https://openweathermap.org/img/wn/{icone}@2x.png'
                iconeNow.scale = 1.5
                iconeNow.update()
                # Temperatura
                temp = data_current['main']['temp']
                temperatureNow.text = f'{temp:.0f}'
                temperatureNow.update()
                # Descrição do Clima
                weather_description = data_current['weather'][0]['description']
                descriptionNow.value = f"{weather_description.capitalize()}"
                descriptionNow.update()
                # Humidade
                humidity = data_current['main']['humidity']
                humidityValue.value = f"{humidity}%"
                humidityValue.update()
                # Velocidade do vento
                windspeed = data_current['wind']['speed']
                windSpeedValue.value = f"{windspeed} km/h"
                windSpeedValue.update()
                # Nome da cidade buscada
                cityName.value = data_current['name']
                cityName.update()
                # Verificar e exibir a quantidade de rainfall, se disponível
                if 'rain' in data_current:
                    rainfall = data_current['rain'].get('1h', 0)  # Obtém a precipitação da última hora, se disponível
                    max_rainfall = 10.0  # Valor de referência para cálculo da porcentagem
                    rainfall_percentage = (rainfall / max_rainfall) * 100
                    rainFallValue.value = f"{rainfall:.2f} mm"
                    rainFallValue.update()
                    logging.info(f"Rainfall: {rainfall}mm, which is {rainfall_percentage:.2f}% of the reference value.")
                else:
                    logging.info("No rainfall data available.")

                logging.info("Clima atualizado com sucesso!")
            else:
                logging.warning("Dados incompletos na resposta da API.")
        except requests.exceptions.RequestException as err:
            logging.error(f"Erro na requisição: {err}")

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

    CardsWeather = ft.Container(
        bgcolor=ft.colors.WHITE60,
        padding=25,
        margin=10,
        border_radius=50,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="00:00", size=20, color=ft.colors.PRIMARY,
                    weight=ft.FontWeight.W_600
                ),
                ft.Image(
                    src="images/iconesWeather/sol_nuvem.png",
                    width=50,
                    height=50,
                ),
                ft.Text(
                    value="23°", size=24, color=ft.colors.PRIMARY,
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
                    value="03:00",
                    size=20,
                    color=ft.colors.PRIMARY,
                    weight=ft.FontWeight.W_600
                ),
                ft.Image(
                    src="images/iconesWeather/chuva.png",
                    width=50,
                    height=50,
                ),
                ft.Text(
                    value="28°",
                    size=24,
                    color=ft.colors.PRIMARY,
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
                    value="06:00",
                    size=20,
                    color=ft.colors.PRIMARY,
                    weight=ft.FontWeight.W_600
                ),
                ft.Image(
                    src="images/iconesWeather/chuva_forte.png",
                    width=50,
                    height=50,
                ),
                ft.Text(
                    value="30°",
                    size=24,
                    color=ft.colors.PRIMARY,
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
                    value="09:00",
                    size=20,
                    color=ft.colors.PRIMARY,
                    weight=ft.FontWeight.W_600
                ),
                ft.Image(
                    src="images/iconesWeather/raio.png",
                    width=50,
                    height=50,
                ),
                ft.Text(
                    value="34°",
                    size=24,
                    color=ft.colors.PRIMARY,
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
                    value="12:00",
                    size=20,
                    color=ft.colors.PRIMARY,
                    weight=ft.FontWeight.W_600
                ),
                ft.Image(
                    src="images/iconesWeather/ventos.png",
                    width=50,
                    height=50,
                ),
                ft.Text(
                    value="23°",
                    size=24,
                    color=ft.colors.PRIMARY,
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
                    value="15:00",
                    size=20,
                    color=ft.colors.PRIMARY,
                    weight=ft.FontWeight.W_600
                ),
                ft.Image(
                    src="images/iconesWeather/sol_nuvem.png",
                    width=50,
                    height=50,
                ),
                ft.Text(
                    value="22°",
                    size=24,
                    color=ft.colors.PRIMARY,
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
                    value="18:00",
                    size=20,
                    color=ft.colors.PRIMARY,
                    weight=ft.FontWeight.W_600
                ),
                ft.Image(
                    src="images/iconesWeather/nuvem_raio.png",
                    width=50,
                    height=50,
                ),
                ft.Text(
                    value="23°",
                    size=24,
                    color=ft.colors.PRIMARY,
                    weight=ft.FontWeight.W_700
                ),
            ]
        )
    ),

    days = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        indicator_color=ft.colors.WHITE,
        divider_color=ft.colors.WHITE,
        unselected_label_color=ft.colors.GREY_500,
        scrollable=False,
        height=500,
        label_color=ft.colors.PRIMARY,
        tabs=[
            ft.Tab(
                text="Segunda",
                content=ft.Container(
                    bgcolor=ft.colors.WHITE60,
                    padding=25,
                    margin=10,
                    border_radius=50,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                value="00:00", size=20, color=ft.colors.PRIMARY,
                                weight=ft.FontWeight.W_600
                            ),
                            ft.Image(
                                src="images/iconesWeather/sol_nuvem.png",
                                width=50,
                                height=50,
                            ),
                            ft.Text(
                                value="23°", size=24, color=ft.colors.PRIMARY,
                                weight=ft.FontWeight.W_700
                            ),
                        ]
                    )
                ),
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=True
    )

    return ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                cityName := ft.Text(
                    value="Washington, DC, USA",
                    theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                    size=30,
                    color=ft.colors.PRIMARY
                ),
                dateNow := ft.Text(
                    value="Tue, jun 30", size=20
                ),
                ft.ElevatedButton(
                    text="Coordenadas Geolocator",
                    on_click=get_weather_by_coordinates),
                ft.ResponsiveRow(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                iconeNow := ft.Image(src="images/iconesWeather/chuva.png", width=150, height=200),
                                ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            spans=[
                                                temperatureNow := ft.TextSpan(
                                                    text="23",
                                                    style=ft.TextStyle(
                                                        size=70,
                                                        weight=ft.FontWeight.W_700,
                                                        color=ft.colors.PRIMARY
                                                    )
                                                ),
                                            ]
                                        ),
                                        descriptionNow := ft.Text(
                                            value="Chuva forte",
                                            size=20,
                                            color=ft.colors.ON_BACKGROUND
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
                                                            color=ft.colors.PRIMARY,
                                                            weight=ft.FontWeight.W_600
                                                        ),
                                                    ]
                                                ),
                                                rainFallValue := ft.Text(
                                                    value="Sem precipitação", size=20, color=ft.colors.PRIMARY,
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
                                                            color=ft.colors.PRIMARY,
                                                            weight=ft.FontWeight.W_600
                                                        ),
                                                    ]
                                                ),
                                                humidityValue := ft.Text(
                                                    value="100%", size=20, color=ft.colors.PRIMARY,
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
                                                            value="Wind", size=20, color=ft.colors.PRIMARY,
                                                            weight=ft.FontWeight.W_600
                                                        ),
                                                    ]
                                                ),
                                                windSpeedValue := ft.Text(
                                                    value="11km/h", size=20, color=ft.colors.PRIMARY,
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
                    controls=[
                        days
                    ]
                ),
            ]
        )
    )
