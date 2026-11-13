"""
Tekstet e ndërfaqes së Go Tirana në tre gjuhë (EN / IT / SQ).
Çdo çelës përdoret në shabllonet si {{ t.celesi }}.
"""

GJUHET = ["en", "it", "sq"]
EMRAT_E_GJUHEVE = {"en": "English", "it": "Italiano", "sq": "Shqip"}
LOCALE = {"en": "en_GB", "it": "it_IT", "sq": "sq_AL"}

KATEGORITE = {
    "history":   {"color": "#a33c26", "en": "History & culture", "it": "Storia e cultura", "sq": "Histori dhe kulturë"},
    "photo":     {"color": "#11707c", "en": "Photo spots", "it": "Luoghi per foto", "sq": "Vende për foto"},
    "nature":    {"color": "#2d6a31", "en": "Nature & views", "it": "Natura e panorami", "sq": "Natyrë dhe pamje"},
    "food":      {"color": "#8f5a0a", "en": "Food & markets", "it": "Cibo e mercati", "sq": "Ushqim dhe pazare"},
    "nightlife": {"color": "#5b3fa6", "en": "Nightlife", "it": "Vita notturna", "sq": "Jeta e natës"},
}

KATEGORITE_PERSHKRIM = {
    "history": {
        "en": "Ottoman mosques, communist bunkers and the stories in between.",
        "it": "Moschee ottomane, bunker comunisti e le storie che stanno in mezzo.",
        "sq": "Xhami osmane, bunkerë komunistë dhe historitë mes tyre.",
    },
    "photo": {
        "en": "Where to stand, and when to go, for the shots you'll keep.",
        "it": "Dove metterti, e quando andare, per le foto che vorrai tenere.",
        "sq": "Ku të qëndrosh, dhe kur të shkosh, për fotot që do t'i mbash.",
    },
    "nature": {
        "en": "A lake in the city and a mountain a cable car away.",
        "it": "Un lago in città e una montagna a una corsa di funivia.",
        "sq": "Një liqen në qytet dhe një mal një teleferik larg.",
    },
    "food": {
        "en": "Markets, raki and the dishes locals actually eat.",
        "it": "Mercati, raki e i piatti che mangiano davvero i tiranesi.",
        "sq": "Tregje, raki dhe gatimet që hanë vërtet vendasit.",
    },
    "nightlife": {
        "en": "From a quiet raki to a late DJ set.",
        "it": "Da una raki tranquilla a un DJ set a notte fonda.",
        "sq": "Nga një raki e qetë deri te një DJ set vonë natën.",
    },
}

T = {
    "en": {
        "site_desc": "The sights, views and late nights of Tirana, Albania, with the city bus that takes you there.",
        "nav_explore": "Explore", "nav_planner": "Bus planner", "nav_contact": "Contact", "nav_menu": "Menu",
        "lang_label": "Language",
        "skip": "Skip to content",
        "hero_title": "Tirana, one stop at a time.",
        "hero_lead": "The sights, views and late nights of Albania's capital, and the city bus that gets you to each one.",
        "hero_cta": "Explore places", "hero_cta2": "Plan a bus trip", "hero_pause": "Pause background video", "hero_play": "Play background video",
        "hero_eyebrow": "Your city guide to Tirana",
        "day_title": "A day in Tirana", "day_lead": "Three stops, from the first coffee to the last drink.",
        "day_slots": [("Morning", "Start at the square", "Walk Skanderbeg Square while the city wakes up, then find a coffee on its edge."),
                      ("Afternoon", "Ride up the mountain", "Take the Dajti Ekspres cable car for a long view over the whole valley."),
                      ("Evening", "Watch the sunset turn", "End at the Sky Tower's revolving bar as the lights come on below.")],
        "home_cats": "What are you in the mood for?",
        "home_start": "Start here", "home_start_lead": "If you only have a day or two, these are the places to see.",
        "home_bus_title": "Every place, one bus ride away",
        "home_bus_text": "Tap “Get there by bus” on any place and our planner finds the fastest route with Tirana's city buses: where to wait, which line to take and where to get off.",
        "home_bus_cta": "Open the bus planner",
        "home_bus_points": ["All 15 city lines, 27 routes", "Walking directions to and from the stop", "Times based on how often each line runs"],
        "places_count": "{n} places", "see_all": "See all",
        "explore_title": "Explore Tirana", "explore_lead": "{n} places, from Ottoman mosques to rooftop views.",
        "filter_all": "All", "show_map": "Map", "show_list": "List",
        "cat_lead_suffix": "",
        "breadcrumb_home": "Home",
        "facts": "At a glance", "fact_area": "Area", "fact_hours": "Opening hours", "fact_entry": "Entry",
        "fact_time": "Time to spend", "fact_website": "Website",
        "entry_free": "Free", "entry_paid": "Ticket required", "hours_unknown": "Check before you go",
        "dur_min": "{a}–{b} min", "dur_h": "{a}–{b} h", "dur_mixed": "{a} min – {b} h",
        "about": "About", "tips": "Good to know",
        "get_bus": "Get there by bus", "open_maps": "Open in maps",
        "nearby": "Nearby", "walk_min": "{n} min walk",
        "photo_by": "Photo", "photo_venue": "courtesy of the venue", "gallery_all": "Show all {n} photos", "lb_prev": "Previous photo", "lb_next": "Next photo", "lb_close": "Close", "lb_label": "Photo gallery", "no_photo": "Illustration: no free-licence photo available for this venue.",
        "venue_note": "Bars and clubs change often. Check current opening hours before you go.",
        "contact_title": "Contact", "contact_lead": "Suggest a place, report a mistake or just say hello. We read every message.",
        "f_name": "Your name", "f_email": "Email", "f_topic": "Topic", "f_message": "Message",
        "f_topic_suggest": "Suggest a place", "f_topic_fix": "Report a mistake", "f_topic_other": "Something else",
        "f_consent": "I agree that my message is stored to answer me, as described in the privacy policy.",
        "f_send": "Send message", "f_sending": "Sending…",
        "f_ok": "Thanks! Your message has been sent.",
        "f_err_required": "Please fill in this field.", "f_err_email": "Please enter a valid email address.",
        "f_err_short": "Please write at least 10 characters.", "f_err_long": "Please keep it under 2,000 characters.",
        "f_err_consent": "Please accept to continue.",
        "f_err_server": "We couldn't send your message. Please try again in a few minutes.",
        "f_err_rate": "Too many messages from your connection. Please try again later.",
        "f_hp": "Leave this field empty",
        "privacy": "Privacy policy", "terms": "Terms & conditions", "cookie_settings": "Cookie settings",
        "footer_about": "An independent guide to Tirana built on open data. Not affiliated with the Municipality of Tirana.",
        "footer_data": "Maps © Google; bus line and stop data © OpenStreetMap contributors. Photos from Wikimedia Commons and the venues themselves, credited on each page.",
        "cookie_title": "Privacy choices",
        "cookie_text": "We don't use advertising or tracking cookies. With your permission, we count page visits with GoatCounter, which stores no cookies and no personal data.",
        "cookie_accept": "Allow statistics", "cookie_decline": "No thanks", "cookie_more": "Read the privacy policy",
        "nf_title": "Page not found", "nf_text": "This page doesn't exist, or it moved. Try one of these instead:",
        "updated": "Last updated", "legal_note": "",
        "your_destination": "Your destination",
        "planner_hint": "Choose your starting point on the map.",
    },
    "it": {
        "site_desc": "Monumenti, panorami e vita notturna di Tirana, in Albania, con l'autobus urbano che ti porta lì.",
        "nav_explore": "Esplora", "nav_planner": "Percorsi in bus", "nav_contact": "Contatti", "nav_menu": "Menu",
        "lang_label": "Lingua",
        "skip": "Vai al contenuto",
        "hero_title": "Tirana, una fermata alla volta.",
        "hero_lead": "Monumenti, panorami e notti della capitale albanese, e l'autobus urbano che ti porta a ognuno.",
        "hero_cta": "Esplora i luoghi", "hero_cta2": "Pianifica un viaggio in bus", "hero_pause": "Metti in pausa il video", "hero_play": "Riproduci il video",
        "hero_eyebrow": "La tua guida di Tirana",
        "day_title": "Una giornata a Tirana", "day_lead": "Tre tappe, dal primo caffè all'ultimo drink.",
        "day_slots": [("Mattina", "Comincia dalla piazza", "Passeggia in piazza Skanderbeg mentre la città si sveglia, poi prendi un caffè ai suoi margini."),
                      ("Pomeriggio", "Sali sulla montagna", "Prendi la funivia Dajti Ekspres per una vista su tutta la valle."),
                      ("Sera", "Il tramonto che gira", "Finisci al bar girevole della Sky Tower mentre sotto si accendono le luci.")],
        "home_cats": "Cosa ti va di fare?",
        "home_start": "Da dove iniziare", "home_start_lead": "Se hai solo uno o due giorni, questi sono i luoghi da vedere.",
        "home_bus_title": "Ogni luogo, a una corsa di autobus",
        "home_bus_text": "Tocca “Arrivaci in autobus” su qualsiasi luogo e il nostro pianificatore trova il percorso più veloce con gli autobus urbani di Tirana: dove aspettare, quale linea prendere e dove scendere.",
        "home_bus_cta": "Apri il pianificatore",
        "home_bus_points": ["Tutte le 15 linee urbane, 27 percorsi", "Indicazioni a piedi da e per la fermata", "Tempi basati sulla frequenza di ogni linea"],
        "places_count": "{n} luoghi", "see_all": "Vedi tutti",
        "explore_title": "Esplora Tirana", "explore_lead": "{n} luoghi, dalle moschee ottomane ai panorami dall'alto.",
        "filter_all": "Tutti", "show_map": "Mappa", "show_list": "Elenco",
        "cat_lead_suffix": "",
        "breadcrumb_home": "Home",
        "facts": "In breve", "fact_area": "Zona", "fact_hours": "Orari", "fact_entry": "Ingresso",
        "fact_time": "Tempo da dedicare", "fact_website": "Sito web",
        "entry_free": "Gratuito", "entry_paid": "A pagamento", "hours_unknown": "Verifica prima di andare",
        "dur_min": "{a}–{b} min", "dur_h": "{a}–{b} h", "dur_mixed": "{a} min – {b} h",
        "about": "Informazioni", "tips": "Buono a sapersi",
        "get_bus": "Arrivaci in autobus", "open_maps": "Apri nelle mappe",
        "nearby": "Nei dintorni", "walk_min": "{n} min a piedi",
        "photo_by": "Foto", "photo_venue": "per gentile concessione del locale", "gallery_all": "Mostra tutte le {n} foto", "lb_prev": "Foto precedente", "lb_next": "Foto successiva", "lb_close": "Chiudi", "lb_label": "Galleria fotografica", "no_photo": "Illustrazione: nessuna foto con licenza libera disponibile per questo locale.",
        "venue_note": "Bar e club cambiano spesso. Verifica gli orari attuali prima di andare.",
        "contact_title": "Contatti", "contact_lead": "Suggerisci un luogo, segnala un errore o scrivici semplicemente. Leggiamo ogni messaggio.",
        "f_name": "Il tuo nome", "f_email": "Email", "f_topic": "Argomento", "f_message": "Messaggio",
        "f_topic_suggest": "Suggerisci un luogo", "f_topic_fix": "Segnala un errore", "f_topic_other": "Altro",
        "f_consent": "Accetto che il mio messaggio venga conservato per rispondermi, come descritto nell'informativa sulla privacy.",
        "f_send": "Invia messaggio", "f_sending": "Invio in corso…",
        "f_ok": "Grazie! Il tuo messaggio è stato inviato.",
        "f_err_required": "Compila questo campo.", "f_err_email": "Inserisci un indirizzo email valido.",
        "f_err_short": "Scrivi almeno 10 caratteri.", "f_err_long": "Resta sotto i 2.000 caratteri.",
        "f_err_consent": "Accetta per continuare.",
        "f_err_server": "Non siamo riusciti a inviare il messaggio. Riprova tra qualche minuto.",
        "f_err_rate": "Troppi messaggi dalla tua connessione. Riprova più tardi.",
        "f_hp": "Lascia vuoto questo campo",
        "privacy": "Informativa sulla privacy", "terms": "Termini e condizioni", "cookie_settings": "Impostazioni cookie",
        "footer_about": "Una guida indipendente a Tirana basata su dati aperti. Non affiliata al Comune di Tirana.",
        "footer_data": "Mappe © Google; dati di linee e fermate © contributori di OpenStreetMap. Foto da Wikimedia Commons e dai locali stessi, citate in ogni pagina.",
        "cookie_title": "Scelte sulla privacy",
        "cookie_text": "Non usiamo cookie pubblicitari o di tracciamento. Con il tuo permesso contiamo le visite con GoatCounter, che non salva cookie né dati personali.",
        "cookie_accept": "Consenti statistiche", "cookie_decline": "No, grazie", "cookie_more": "Leggi l'informativa",
        "nf_title": "Pagina non trovata", "nf_text": "Questa pagina non esiste o è stata spostata. Prova invece una di queste:",
        "updated": "Ultimo aggiornamento", "legal_note": "",
        "your_destination": "La tua destinazione",
        "planner_hint": "Scegli il punto di partenza sulla mappa.",
    },
    "sq": {
        "site_desc": "Vendet, pamjet dhe netët e Tiranës, me autobusin e qytetit që të çon atje.",
        "nav_explore": "Eksploro", "nav_planner": "Planifikuesi i autobusëve", "nav_contact": "Kontakt", "nav_menu": "Menyja",
        "lang_label": "Gjuha",
        "skip": "Kalo te përmbajtja",
        "hero_title": "Tirana, stacion pas stacioni.",
        "hero_lead": "Vendet, pamjet dhe netët e kryeqytetit, dhe autobusi i qytetit që të çon te secili.",
        "hero_cta": "Eksploro vendet", "hero_cta2": "Planifiko një udhëtim", "hero_pause": "Ndalo videon", "hero_play": "Luaj videon",
        "hero_eyebrow": "Udhëzuesi yt për Tiranën",
        "day_title": "Një ditë në Tiranë", "day_lead": "Tri ndalesa, nga kafeja e parë te pija e fundit.",
        "day_slots": [("Mëngjes", "Nis nga sheshi", "Shëtit në Sheshin Skënderbej ndërsa qyteti zgjohet, pastaj pi një kafe në anë të tij."),
                      ("Pasdite", "Ngjitu në mal", "Merr teleferikun Dajti Ekspres për një pamje mbi gjithë luginën."),
                      ("Mbrëmje", "Perëndimi që rrotullohet", "Mbyll ditën te bari rrotullues i Sky Tower, kur poshtë ndizen dritat.")],
        "home_cats": "Çfarë ke qejf të bësh?",
        "home_start": "Fillo këtu", "home_start_lead": "Nëse ke vetëm një ose dy ditë, këto janë vendet që duhen parë.",
        "home_bus_title": "Çdo vend, një autobus larg",
        "home_bus_text": "Shtyp “Shko me autobus” te çdo vend dhe planifikuesi ynë gjen rrugën më të shpejtë me autobusët e qytetit: ku të presësh, cilën linjë të marrësh dhe ku të zbresësh.",
        "home_bus_cta": "Hap planifikuesin",
        "home_bus_points": ["Të 15 linjat e qytetit, 27 degëzime", "Udhëzime në këmbë deri te stacioni", "Kohë sipas frekuencës së çdo linje"],
        "places_count": "{n} vende", "see_all": "Shiko të gjitha",
        "explore_title": "Eksploro Tiranën", "explore_lead": "{n} vende, nga xhamitë osmane te pamjet nga lart.",
        "filter_all": "Të gjitha", "show_map": "Harta", "show_list": "Lista",
        "cat_lead_suffix": "",
        "breadcrumb_home": "Kreu",
        "facts": "Shkurt", "fact_area": "Zona", "fact_hours": "Orari", "fact_entry": "Hyrja",
        "fact_time": "Koha që duhet", "fact_website": "Faqja",
        "entry_free": "Falas", "entry_paid": "Me biletë", "hours_unknown": "Kontrollo para se të shkosh",
        "dur_min": "{a}–{b} min", "dur_h": "{a}–{b} orë", "dur_mixed": "{a} min – {b} orë",
        "about": "Rreth vendit", "tips": "Mirë ta dish",
        "get_bus": "Shko me autobus", "open_maps": "Hape në harta",
        "nearby": "Afër", "walk_min": "{n} min në këmbë",
        "photo_by": "Foto", "photo_venue": "me lejen e lokalit", "gallery_all": "Shiko të {n} fotot", "lb_prev": "Fotoja e mëparshme", "lb_next": "Fotoja tjetër", "lb_close": "Mbyll", "lb_label": "Galeria e fotove", "no_photo": "Ilustrim: nuk ka foto me licencë të lirë për këtë lokal.",
        "venue_note": "Baret dhe klubet ndryshojnë shpesh. Kontrollo orarin aktual para se të shkosh.",
        "contact_title": "Kontakt", "contact_lead": "Sugjero një vend, na trego një gabim ose thjesht na shkruaj. I lexojmë të gjitha mesazhet.",
        "f_name": "Emri yt", "f_email": "Email", "f_topic": "Tema", "f_message": "Mesazhi",
        "f_topic_suggest": "Sugjero një vend", "f_topic_fix": "Raporto një gabim", "f_topic_other": "Diçka tjetër",
        "f_consent": "Pranoj që mesazhi im të ruhet për të më kthyer përgjigje, siç përshkruhet në politikën e privatësisë.",
        "f_send": "Dërgo mesazhin", "f_sending": "Po dërgohet…",
        "f_ok": "Faleminderit! Mesazhi yt u dërgua.",
        "f_err_required": "Plotëso këtë fushë.", "f_err_email": "Shkruaj një adresë email të vlefshme.",
        "f_err_short": "Shkruaj të paktën 10 shkronja.", "f_err_long": "Mbaje nën 2.000 shkronja.",
        "f_err_consent": "Prano për të vazhduar.",
        "f_err_server": "Mesazhi nuk u dërgua. Provo përsëri pas disa minutash.",
        "f_err_rate": "Shumë mesazhe nga lidhja jote. Provo përsëri më vonë.",
        "f_hp": "Lëre bosh këtë fushë",
        "privacy": "Politika e privatësisë", "terms": "Kushtet e përdorimit", "cookie_settings": "Cilësimet e cookies",
        "footer_about": "Një udhëzues i pavarur për Tiranën, i ndërtuar mbi të dhëna të hapura. Nuk lidhet me Bashkinë e Tiranës.",
        "footer_data": "Hartat © Google; të dhënat e linjave dhe stacioneve © kontribuuesit e OpenStreetMap. Fotot nga Wikimedia Commons dhe nga vetë lokalet, me burimin në çdo faqe.",
        "cookie_title": "Zgjedhjet e privatësisë",
        "cookie_text": "Nuk përdorim cookies reklamash apo gjurmimi. Me lejen tënde, numërojmë vizitat me GoatCounter, që nuk ruan cookies as të dhëna personale.",
        "cookie_accept": "Lejo statistikat", "cookie_decline": "Jo, faleminderit", "cookie_more": "Lexo politikën e privatësisë",
        "nf_title": "Faqja nuk u gjet", "nf_text": "Kjo faqe nuk ekziston ose është zhvendosur. Provo një nga këto:",
        "updated": "Përditësuar më", "legal_note": "",
        "your_destination": "Destinacioni yt",
        "planner_hint": "Zgjidh pikën e nisjes në hartë.",
    },
}

# ---------------------------------------------------------------------------
# Faqet ligjore. {owner} dhe {email} plotësohen nga konfigurimi.json.
# KUJDES: shabllon i saktë për mënyrën si funksionon faqja, jo këshillë ligjore.
# ---------------------------------------------------------------------------
PRIVATESIA = {
    "en": [
        ("Who we are", "Go Tirana is an independent guide to Tirana run by {owner}. For any question about your data, write to {email} or use the contact form."),
        ("What we collect", "We only collect what you send us through the contact form: your name, email address, topic and message. We store it on our server to answer you and keep it for up to 12 months, then delete it. We don't sell or share it."),
        ("Statistics", "If you allow it in the privacy banner, we count visits with GoatCounter. It records the page, the referring site, browser type and country, without cookies and without storing your IP address. You can change your choice at any time via “Cookie settings” in the footer."),
        ("Your browser's storage", "We save your language, your privacy choice and, in the bus planner, your calibration measurements in your browser's local storage. This data never leaves your device and you can clear it at any time."),
        ("Third-party services", "To show maps and photos, your browser connects directly to: Google Maps (all maps on the site, including the bus planner, under Google's privacy policy) and Wikimedia Commons (photos). These providers receive your IP address as part of the connection, under their own privacy policies. Fonts are served from our own server."),
        ("Security", "The site is served over HTTPS. The contact form is protected against spam without tracking you: we use a hidden field, a time check and a limit on how many messages can be sent from one connection."),
        ("Your rights", "You can ask to see, correct or delete the personal data we hold about you, or object to its use, by writing to {email}. You also have the right to complain to the data protection authority in your country; in Albania this is the Information and Data Protection Commissioner (IDP)."),
    ],
    "it": [
        ("Chi siamo", "Go Tirana è una guida indipendente a Tirana gestita da {owner}. Per qualsiasi domanda sui tuoi dati scrivi a {email} o usa il modulo di contatto."),
        ("Cosa raccogliamo", "Raccogliamo solo ciò che ci invii tramite il modulo di contatto: nome, indirizzo email, argomento e messaggio. Li conserviamo sul nostro server per risponderti, per un massimo di 12 mesi, poi li cancelliamo. Non li vendiamo né li condividiamo."),
        ("Statistiche", "Se lo consenti nel banner sulla privacy, contiamo le visite con GoatCounter. Registra la pagina, il sito di provenienza, il tipo di browser e il paese, senza cookie e senza salvare il tuo indirizzo IP. Puoi cambiare scelta in qualsiasi momento da “Impostazioni cookie” nel piè di pagina."),
        ("Memoria del browser", "Salviamo la lingua, la tua scelta sulla privacy e, nel pianificatore, le tue misurazioni di calibrazione nella memoria locale del browser. Questi dati non lasciano mai il tuo dispositivo e puoi cancellarli quando vuoi."),
        ("Servizi di terzi", "Per mostrare mappe e foto, il tuo browser si collega direttamente a: Google Maps (tutte le mappe del sito, compreso il pianificatore, secondo l'informativa di Google) e Wikimedia Commons (foto). Questi fornitori ricevono il tuo indirizzo IP come parte della connessione, secondo le loro informative. I font sono serviti dal nostro server."),
        ("Sicurezza", "Il sito è servito tramite HTTPS. Il modulo di contatto è protetto dallo spam senza tracciarti: usiamo un campo nascosto, un controllo sul tempo e un limite ai messaggi inviabili da una stessa connessione."),
        ("I tuoi diritti", "Puoi chiedere di vedere, correggere o cancellare i dati personali che conserviamo, oppure opporti al loro uso, scrivendo a {email}. Hai anche il diritto di presentare reclamo all'autorità per la protezione dei dati del tuo paese; in Albania è il Commissario per il Diritto all'Informazione e la Protezione dei Dati (IDP)."),
    ],
    "sq": [
        ("Kush jemi", "Go Tirana është një udhëzues i pavarur për Tiranën, i drejtuar nga {owner}. Për çdo pyetje rreth të dhënave të tua, shkruaj te {email} ose përdor formularin e kontaktit."),
        ("Çfarë mbledhim", "Mbledhim vetëm atë që na dërgon përmes formularit të kontaktit: emrin, adresën email, temën dhe mesazhin. I ruajmë në serverin tonë për të të kthyer përgjigje, deri në 12 muaj, pastaj i fshijmë. Nuk i shesim dhe nuk i ndajmë me askënd."),
        ("Statistikat", "Nëse e lejon te banderola e privatësisë, numërojmë vizitat me GoatCounter. Regjistron faqen, faqen nga ke ardhur, llojin e shfletuesit dhe vendin, pa cookies dhe pa ruajtur adresën tënde IP. Mund ta ndryshosh zgjedhjen në çdo kohë te “Cilësimet e cookies” në fund të faqes."),
        ("Ruajtja në shfletues", "Ruajmë gjuhën, zgjedhjen tënde të privatësisë dhe, te planifikuesi, matjet e kalibrimit në memorien lokale të shfletuesit. Këto të dhëna nuk largohen kurrë nga pajisja jote dhe mund t'i fshish kur të duash."),
        ("Shërbime të palëve të treta", "Për të shfaqur hartat dhe fotot, shfletuesi yt lidhet direkt me: Google Maps (të gjitha hartat e faqes, edhe planifikuesi, sipas politikës së privatësisë së Google) dhe Wikimedia Commons (fotot). Këta ofrues marrin adresën tënde IP si pjesë e lidhjes, sipas politikave të tyre. Shkronjat shërbehen nga serveri ynë."),
        ("Siguria", "Faqja shërbehet përmes HTTPS. Formulari i kontaktit mbrohet nga spam-i pa të gjurmuar: përdorim një fushë të fshehur, një kontroll kohe dhe një kufi për numrin e mesazheve nga e njëjta lidhje."),
        ("Të drejtat e tua", "Mund të kërkosh të shohësh, të korrigjosh ose të fshish të dhënat personale që ruajmë për ty, ose të kundërshtosh përdorimin e tyre, duke shkruar te {email}. Ke gjithashtu të drejtë të ankohesh te autoriteti i mbrojtjes së të dhënave; në Shqipëri është Komisioneri për të Drejtën e Informimit dhe Mbrojtjen e të Dhënave Personale (IDP)."),
    ],
}

KUSHTET = {
    "en": [
        ("About this site", "Go Tirana is a free, independent guide run by {owner}. By using it you accept these terms."),
        ("Information is a guide, not a guarantee", "We do our best to keep places, opening hours and bus routes accurate, but things change. Bus travel times are estimates based on open data and average speeds, not official timetables. Always check important details, such as opening hours or the last bus, before you travel."),
        ("No liability", "The site is provided as is. To the extent permitted by law, we are not responsible for losses or inconvenience caused by relying on its information, or by third-party sites we link to."),
        ("Content and credits", "Map and route data come from OpenStreetMap contributors under the Open Database License. Photos come from Wikimedia Commons under the licences shown next to each one, or are used with the permission of the venues shown. Texts and design are ours; please ask before reusing them."),
        ("Your messages", "If you send us a suggestion or correction, you allow us to use it to improve the guide. Please don't send content that is unlawful, offensive or not yours to share."),
        ("Changes and law", "We may update these terms; the date below shows the latest version. These terms are governed by the laws of the Republic of Albania."),
    ],
    "it": [
        ("Su questo sito", "Go Tirana è una guida gratuita e indipendente gestita da {owner}. Usandola accetti questi termini."),
        ("Le informazioni sono una guida, non una garanzia", "Facciamo del nostro meglio per mantenere accurati luoghi, orari e percorsi in autobus, ma le cose cambiano. I tempi di viaggio in autobus sono stime basate su dati aperti e velocità medie, non orari ufficiali. Verifica sempre i dettagli importanti, come gli orari di apertura o l'ultimo autobus, prima di partire."),
        ("Nessuna responsabilità", "Il sito è fornito così com'è. Nei limiti consentiti dalla legge, non siamo responsabili di perdite o disagi derivanti dall'uso delle sue informazioni o dei siti di terzi a cui rimandiamo."),
        ("Contenuti e crediti", "I dati di mappe e percorsi provengono dai contributori di OpenStreetMap con licenza Open Database License. Le foto provengono da Wikimedia Commons con le licenze indicate accanto a ciascuna, oppure sono usate con il permesso dei locali raffigurati. Testi e design sono nostri; chiedici prima di riutilizzarli."),
        ("I tuoi messaggi", "Se ci invii un suggerimento o una correzione, ci consenti di usarlo per migliorare la guida. Non inviare contenuti illegali, offensivi o che non hai il diritto di condividere."),
        ("Modifiche e legge applicabile", "Potremmo aggiornare questi termini; la data qui sotto indica la versione più recente. Questi termini sono regolati dalle leggi della Repubblica d'Albania."),
    ],
    "sq": [
        ("Rreth kësaj faqeje", "Go Tirana është një udhëzues falas dhe i pavarur, i drejtuar nga {owner}. Duke e përdorur, pranon këto kushte."),
        ("Informacioni është udhëzues, jo garanci", "Përpiqemi t'i mbajmë të sakta vendet, oraret dhe linjat e autobusëve, por gjërat ndryshojnë. Kohët e udhëtimit me autobus janë vlerësime nga të dhëna të hapura dhe shpejtësi mesatare, jo orare zyrtare. Kontrollo gjithmonë detajet e rëndësishme, si orari i hapjes ose autobusi i fundit, para se të nisesh."),
        ("Pa përgjegjësi", "Faqja ofrohet ashtu siç është. Brenda kufijve të ligjit, nuk mbajmë përgjegjësi për humbje ose shqetësime nga mbështetja te informacioni i saj, ose te faqet e palëve të treta që lidhim."),
        ("Përmbajtja dhe autorët", "Të dhënat e hartës dhe të linjave vijnë nga kontribuuesit e OpenStreetMap me licencën Open Database License. Fotot vijnë nga Wikimedia Commons me licencat e shënuara pranë secilës, ose përdoren me lejen e lokaleve që shfaqin. Tekstet dhe dizajni janë tonat; na pyet para se t'i ripërdorësh."),
        ("Mesazhet e tua", "Nëse na dërgon një sugjerim ose korrigjim, na lejon ta përdorim për të përmirësuar udhëzuesin. Mos dërgo përmbajtje të paligjshme, fyese ose që nuk ke të drejtë ta ndash."),
        ("Ndryshimet dhe ligji", "Mund t'i përditësojmë këto kushte; data më poshtë tregon versionin e fundit. Këto kushte rregullohen nga ligjet e Republikës së Shqipërisë."),
    ],
}


# ---- Dizajni i ri (v2): tekstet shtesë dhe ato që zëvendësohen ----
from tekstet_v2 import SHTESA, KAT_PERSHKRIM, PRIVATESIA_NL   # noqa: E402
for _l in GJUHET:
    T[_l].update(SHTESA[_l])
    PRIVATESIA[_l].insert(2, PRIVATESIA_NL[_l])
for _k, _v in KAT_PERSHKRIM.items():
    KATEGORITE_PERSHKRIM[_k] = _v

# ---- Faqja "Informacion praktik" ----
from tekstet_info import INFO   # noqa: E402
for _l in GJUHET:
    T[_l]["nav_info"] = INFO[_l]["nav"]
    T[_l]["info_title"] = INFO[_l]["title"]
    T[_l]["info_link"] = INFO[_l]["link"]

# ---- "Afër meje" (Eksploro) dhe faqja pa internet ----
_SHTESA_3 = {
    "en": {"near_btn": "Near me", "near_reset": "Default order", "near_loading": "Finding where you are…",
           "near_done": "Sorted by distance from you.", "near_rough": "Sorted by distance. Your location is approximate (up to {d} off).",
           "near_far": "You seem to be outside Tirana, so distances are not shown.",
           "near_denied": "Location access was blocked. You can allow it from the lock icon next to the address.",
           "near_fail": "We couldn't find your location. Try again outside or with Wi-Fi on.",
           "near_away": "{d} away", "my_location": "My location",
           "off_title": "You're offline", "off_text": "This page isn't saved on your phone yet. These pages work without internet:",
           "off_retry": "Try again"},
    "it": {"near_btn": "Vicino a me", "near_reset": "Ordine iniziale", "near_loading": "Sto cercando dove ti trovi…",
           "near_done": "Ordinati per distanza da te.", "near_rough": "Ordinati per distanza. La tua posizione è approssimativa (fino a {d}).",
           "near_far": "Sembri fuori da Tirana, quindi le distanze non vengono mostrate.",
           "near_denied": "L'accesso alla posizione è bloccato. Puoi consentirlo dall'icona del lucchetto accanto all'indirizzo.",
           "near_fail": "Non riusciamo a trovare la tua posizione. Riprova all'aperto o con il Wi-Fi acceso.",
           "near_away": "a {d}", "my_location": "La mia posizione",
           "off_title": "Sei offline", "off_text": "Questa pagina non è ancora salvata sul telefono. Queste pagine funzionano senza internet:",
           "off_retry": "Riprova"},
    "sq": {"near_btn": "Afër meje", "near_reset": "Rendi fillestar", "near_loading": "Po gjejmë ku ndodhesh…",
           "near_done": "Të renditura sipas largësisë nga ti.", "near_rough": "Të renditura sipas largësisë. Vendndodhja jote është e përafërt (deri në {d}).",
           "near_far": "Duket se je jashtë Tiranës, ndaj largësitë nuk shfaqen.",
           "near_denied": "Vendndodhja u bllokua. Mund ta lejosh te ikona e drynit pranë adresës.",
           "near_fail": "Nuk e gjetëm vendndodhjen. Provo përsëri jashtë ose me Wi-Fi të ndezur.",
           "near_away": "{d} larg", "my_location": "Vendndodhja ime",
           "off_title": "Je pa internet", "off_text": "Kjo faqe nuk është ruajtur ende në telefon. Këto faqe punojnë pa internet:",
           "off_retry": "Provo përsëri"},
}
for _l in GJUHET:
    T[_l].update(_SHTESA_3[_l])

# ---- Hero: butonat e shpejtë (xhami) djathtas ----
_HERO_QUICK = {
    "en": {"hq_label": "Jump to", "hq": ["Iconic places", "Culture & history", "Food & drink", "Nature & views"]},
    "it": {"hq_label": "Vai a", "hq": ["Luoghi iconici", "Cultura e storia", "Gastronomia", "Natura e panorami"]},
    "sq": {"hq_label": "Shko te", "hq": ["Vendet ikonike", "Kultura dhe historia", "Gastronomia", "Natyra dhe pamjet"]},
}
for _l in GJUHET:
    T[_l].update(_HERO_QUICK[_l])

# ---- Hero: titulli i vogël sipër ----
for _l, _k in (("en", "Explore Tirana"), ("it", "Esplora Tirana"), ("sq", "Eksploro Tiranën")):
    T[_l]["hero_kicker"] = _k

# ---- Itineraret: emri në menu/fund të faqes ----
from tekstet_itinerare import UI as _IT_UI
for _l in T:
    T[_l]["nav_itins"] = _IT_UI[_l]["nav"]

# ---- Google Maps (lidhje, pa çelës API) ----
_GMAPS = {
    "en": {"gmaps_open": "Open in Google Maps", "gmaps_dir": "Directions in Google Maps"},
    "it": {"gmaps_open": "Apri in Google Maps", "gmaps_dir": "Indicazioni su Google Maps"},
    "sq": {"gmaps_open": "Hape në Google Maps", "gmaps_dir": "Udhëzime në Google Maps"},
}
for _l in T:
    T[_l].update(_GMAPS[_l])

# ---- "Hapur tani / Mbyllur" (llogaritet në shfletues sipas orës së Tiranës; shih assets/js/site.js) ----
_ORARI = {
    "en": {"open": "Open now", "closed": "Closed", "always": "Always open", "closes": "closes {t}",
           "opens": "opens {t}", "opens_tomorrow": "opens tomorrow {t}", "opens_day": "opens {d} {t}",
           "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
    "it": {"open": "Aperto ora", "closed": "Chiuso", "always": "Sempre aperto", "closes": "chiude alle {t}",
           "opens": "apre alle {t}", "opens_tomorrow": "apre domani alle {t}", "opens_day": "apre {d} alle {t}",
           "days": ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]},
    "sq": {"open": "Hapur tani", "closed": "Mbyllur", "always": "Gjithmonë e hapur", "closes": "mbyll në {t}",
           "opens": "hap në {t}", "opens_tomorrow": "hap nesër në {t}", "opens_day": "hap të {d} në {t}",
           "days": ["hënën", "martën", "mërkurën", "enjten", "premten", "shtunën", "dielën"]},
}
for _l in T:
    T[_l]["orari_js"] = _ORARI[_l]

# ---- Udhëtime ditore: emri në fund të faqes ----
from tekstet_udhetime import UI as _UDH_UI
for _l in T:
    T[_l]["nav_daytrips"] = _UDH_UI[_l]["nav"]
