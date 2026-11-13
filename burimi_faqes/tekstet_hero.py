"""GO TIRANA: fotot e slider-it në krye të faqes kryesore.
Fotoja e parë është ajo lokale (hero-1811 / hero-mobile) dhe ngarkohet menjëherë.
Të tjerat vijnë nga Wikimedia Commons (CC BY-SA, prandaj tregojmë autorin) dhe ngarkohen
vetëm pasi faqja të jetë hapur plotësisht."""

SLIDET = [
    {"path": "b/b7/Monumento_a_Skanderbeg%2C_Tirana%2C_Albania%2C_2014-04-17%2C_DD_02.JPG",
     "name": "Monumento_a_Skanderbeg%2C_Tirana%2C_Albania%2C_2014-04-17%2C_DD_02.JPG",
     "page": "https://commons.wikimedia.org/wiki/File:Monumento_a_Skanderbeg,_Tirana,_Albania,_2014-04-17,_DD_02.JPG",
     "artist": "Diego Delso", "license": "CC BY-SA 3.0", "licenseUrl": "https://creativecommons.org/licenses/by-sa/3.0",
     "pos": "50% 45%",
     "label": {"en": "Skanderbeg Square", "it": "Piazza Skanderbeg", "sq": "Sheshi Skënderbej"}},
    {"path": "8/86/Pyramid_of_Tirana_October_2023.jpg", "name": "Pyramid_of_Tirana_October_2023.jpg",
     "page": "https://commons.wikimedia.org/wiki/File:Pyramid_of_Tirana_October_2023.jpg",
     "artist": "BBB2021", "license": "CC BY-SA 4.0", "licenseUrl": "https://creativecommons.org/licenses/by-sa/4.0",
     "pos": "50% 55%",
     "label": {"en": "The Pyramid of Tirana", "it": "La Piramide di Tirana", "sq": "Piramida e Tiranës"}},
    {"path": "0/08/Tirana_Night_View.jpg", "name": "Tirana_Night_View.jpg",
     "page": "https://commons.wikimedia.org/wiki/File:Tirana_Night_View.jpg",
     "artist": "Alban1989", "license": "CC BY-SA 3.0", "licenseUrl": "https://creativecommons.org/licenses/by-sa/3.0",
     "pos": "50% 50%",
     "label": {"en": "Tirana by night", "it": "Tirana di notte", "sq": "Tirana natën"}},
]

UI = {
    "en": {"slides": "Background photos", "go": "Show photo {n}", "pause": "Pause slideshow", "play": "Play slideshow", "photo": "Photo"},
    "it": {"slides": "Foto di sfondo", "go": "Mostra la foto {n}", "pause": "Metti in pausa le foto", "play": "Riproduci le foto", "photo": "Foto"},
    "sq": {"slides": "Fotot e sfondit", "go": "Shfaq foton {n}", "pause": "Ndalo fotot", "play": "Luaj fotot", "photo": "Foto"},
}

# Moti në hero (të dhënat nga Open-Meteo, pa çelës, CC BY 4.0)
MOTI = {
    "en": {"label": "Weather in Tirana now", "src": "Weather: Open-Meteo.com",
           "d": {"clear": "Clear", "mostly": "Mostly sunny", "cloudy": "Cloudy", "fog": "Foggy", "drizzle": "Drizzle",
                 "rain": "Rain", "snow": "Snow", "showers": "Showers", "storm": "Thunderstorm", "night": "Clear night"},
           "tip": {"rain": "Rainy day? Try the indoor itinerary", "cold": "Chilly: museums and warm cafés",
                   "night": "Evening: Blloku and the city lights", "hot": "Hot: go early, or to the lake park's shade",
                   "nice": "Clear skies: perfect for Dajti", "grey": "A good day to walk the centre"}},
    "it": {"label": "Il meteo a Tirana ora", "src": "Meteo: Open-Meteo.com",
           "d": {"clear": "Sereno", "mostly": "Soleggiato", "cloudy": "Nuvoloso", "fog": "Nebbia", "drizzle": "Pioviggine",
                 "rain": "Pioggia", "snow": "Neve", "showers": "Rovesci", "storm": "Temporale", "night": "Notte serena"},
           "tip": {"rain": "Piove? Prova l'itinerario al coperto", "cold": "Fa freddo: musei e caffè caldi",
                   "night": "Sera: il Blloku e le luci della città", "hot": "Fa caldo: esci presto o all'ombra del parco del lago",
                   "nice": "Cielo limpido: perfetto per il Dajti", "grey": "Una buona giornata per girare il centro"}},
    "sq": {"label": "Moti në Tiranë tani", "src": "Moti: Open-Meteo.com",
           "d": {"clear": "Kthjellët", "mostly": "Kryesisht me diell", "cloudy": "Vranët", "fog": "Mjegull", "drizzle": "Shi i imët",
                 "rain": "Shi", "snow": "Borë", "showers": "Rrebeshe", "storm": "Stuhi", "night": "Natë e kthjellët"},
           "tip": {"rain": "Bie shi? Provo itinerarin për ditë me shi", "cold": "Ftohtë: muzetë dhe kafenetë e ngrohta",
                   "night": "Mbrëmje: Blloku dhe dritat e qytetit", "hot": "Vapë: dil herët, ose në hijen e Parkut të Liqenit",
                   "nice": "Qiell i pastër: ditë e mirë për Dajtin", "grey": "Ditë e mirë për të ecur në qendër"}},
}
LIDHJET_MOTI = {"rain": "itineraries/rainy-day/", "cold": "explore/history/", "night": "explore/nightlife/",
                "hot": "explore/nature/", "nice": "itineraries/mountain-and-lake/", "grey": "itineraries/one-day/"}
