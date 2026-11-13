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
