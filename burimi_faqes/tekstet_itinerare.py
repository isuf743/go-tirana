# Itineraret e gatshme (/{lang}/itineraries/ dhe /{lang}/itineraries/<slug>/).
# Çdo ndalesë është një vend nga vendet.json (slug). Distancat, koha e ecjes dhe lidhjet me
# planifikuesin llogariten vetë nga scripts/03_nderto_faqen.py, ndaj këtu shkruhen vetëm tekstet.
# Për një itinerar të ri: shto një element te ITINERARET dhe rindërto faqen.

# Mbi këtë distancë (metra në vijë ajrore) nuk sugjerojmë ecje, por autobusin
KUFIRI_ECJES = 1800

ITINERARET = [
    {
        "slug": "one-day",
        "hero": "skanderbeg-square",
        "title": {"en": "One day in Tirana", "it": "Un giorno a Tirana", "sq": "Një ditë në Tiranë"},
        "summary": {
            "en": "The classic first day: the square, a bunker, lunch at the bazaar, the Pyramid and a drink above the city. All on foot.",
            "it": "Il classico primo giorno: la piazza, un bunker, pranzo al bazar, la Piramide e un drink sopra la città. Tutto a piedi.",
            "sq": "Dita e parë klasike: sheshi, një bunker, dreka te pazari, Piramida dhe një pije mbi qytet. Gjithçka në këmbë.",
        },
        "lead": {
            "en": "If you only have one day, this is the route we'd take. It stays in the centre, so you can walk the whole way and never need a taxi.",
            "it": "Se hai un solo giorno, questo è il percorso che faremmo noi. Resta in centro, quindi puoi fare tutto a piedi senza mai prendere un taxi.",
            "sq": "Nëse ke vetëm një ditë, kjo është rruga që do të zgjidhnim ne. Qëndron në qendër, ndaj mund ta bësh gjithë rrugën në këmbë pa marrë asnjë taksi.",
        },
        "when": {"en": "Not on Mondays", "it": "Non di lunedì", "sq": "Jo të hënën"},
        "stops": [
            ("09:00", "skanderbeg-square", {
                "en": "Start in the middle of everything and walk the square while it's still quiet.",
                "it": "Comincia dal centro di tutto e attraversa la piazza finché è ancora tranquilla.",
                "sq": "Nis nga mesi i gjithçkaje dhe shëtit në shesh sa është ende i qetë."}),
            ("09:30", "etem-bey-mosque", {
                "en": "Step inside to see the painted walls. Visit outside prayer times and dress modestly.",
                "it": "Entra a vedere le pareti affrescate. Visita fuori dagli orari di preghiera, con un abbigliamento sobrio.",
                "sq": "Hyr brenda të shohësh muret e pikturuara. Shko jashtë orëve të faljes dhe vishu thjesht."}),
            ("09:50", "clock-tower", {
                "en": "Right next door. If it's open, climb the narrow stairs for a view over the square.",
                "it": "Proprio accanto. Se è aperta, sali le scale strette per vedere la piazza dall'alto.",
                "sq": "Menjëherë ngjitur. Nëse është hapur, ngjitu shkallëve të ngushta për ta parë sheshin nga lart."}),
            ("10:30", "bunkart-2", {
                "en": "An hour underground to understand the communist years before you see the rest of the city.",
                "it": "Un'ora sottoterra per capire gli anni del comunismo prima di vedere il resto della città.",
                "sq": "Një orë nën tokë për të kuptuar vitet e komunizmit para se të shohësh pjesën tjetër të qytetit."}),
            ("12:30", "new-bazaar", {
                "en": "Wander the market hall: cheese, honey, olives and homemade raki.",
                "it": "Gira per il mercato coperto: formaggi, miele, olive e raki fatta in casa.",
                "sq": "Shëtit në tregun e mbuluar: djathë, mjaltë, ullinj dhe raki shtëpie."}),
            ("13:00", "oda-garden", {
                "en": "Lunch. Ask for a mix of traditional starters to share.",
                "it": "Pranzo. Chiedi un assaggio di antipasti tradizionali da dividere.",
                "sq": "Dreka. Kërko disa meze tradicionale për t'i ndarë bashkë."}),
            ("15:00", "pyramid", {
                "en": "Climb the steps to the top for a free view down the boulevard.",
                "it": "Sali i gradini fino in cima per una vista gratuita sul viale.",
                "sq": "Ngjitu shkallëve deri në majë për një pamje falas mbi bulevardin."}),
            ("16:00", "postbllok", {
                "en": "A bunker, a piece of the Berlin Wall and pillars from a prison camp, at the gate of Blloku.",
                "it": "Un bunker, un pezzo del Muro di Berlino e i pilastri di un campo di prigionia, all'ingresso del Blloku.",
                "sq": "Një bunker, një copë e Murit të Berlinit dhe shtylla nga një kamp burgu, në hyrje të Bllokut."}),
            ("16:30", "blloku", {
                "en": "Coffee and a slow walk through the district that was once closed to ordinary Albanians.",
                "it": "Un caffè e una passeggiata nel quartiere un tempo vietato agli albanesi comuni.",
                "sq": "Një kafe dhe një shëtitje e ngadaltë në lagjen që dikur ishte e ndaluar për shqiptarët e thjeshtë."}),
            ("18:30", "sky-tower", {
                "en": "End with a drink at the revolving bar as the lights come on. Closed on Mondays: then finish on top of the Pyramid instead.",
                "it": "Chiudi con un drink al bar girevole mentre si accendono le luci. Chiuso il lunedì: in quel caso finisci in cima alla Piramide.",
                "sq": "Mbylle me një pije te bari që rrotullohet, ndërsa ndizen dritat. Mbyllur të hënën: atëherë mbylle ditën në majë të Piramidës."}),
        ],
    },
    {
        "slug": "mountain-and-lake",
        "hero": "dajti-ekspres",
        "start": "skanderbeg-square",
        "title": {"en": "Mountain and lake", "it": "Montagna e lago", "sq": "Mali dhe liqeni"},
        "summary": {
            "en": "A second day: the biggest bunker, the cable car up Mount Dajti, a walk around the lake and dinner at one of the city's best tables.",
            "it": "Un secondo giorno: il bunker più grande, la funivia sul monte Dajti, una passeggiata intorno al lago e cena in uno dei migliori ristoranti.",
            "sq": "Një ditë e dytë: bunkeri më i madh, teleferiku në malin e Dajtit, një shëtitje rreth liqenit dhe darka në një nga tavolinat më të mira të qytetit.",
        },
        "lead": {
            "en": "A bus takes you out to the foot of the mountain, and another brings you back to the Grand Park. Pick a clear day: the cable car is the reason to go.",
            "it": "Un autobus ti porta ai piedi della montagna e un altro ti riporta al Grand Park. Scegli una giornata limpida: la funivia è il motivo per andarci.",
            "sq": "Një autobus të çon te rrëza e malit dhe një tjetër të kthen te Parku i Madh. Zgjidh një ditë të kthjellët: teleferiku është arsyeja për të shkuar.",
        },
        "when": {"en": "A clear, calm day", "it": "Una giornata limpida", "sq": "Një ditë e kthjellët"},
        "stops": [
            ("09:30", "bunkart-1", {
                "en": "Over a hundred rooms dug into the hill for the regime's leaders. Allow a good hour and a half.",
                "it": "Più di cento stanze scavate nella collina per i capi del regime. Calcola almeno un'ora e mezza.",
                "sq": "Mbi njëqind dhoma të gërmuara në kodër për udhëheqësit e regjimit. Llogarit të paktën një orë e gjysmë."}),
            ("11:30", "dajti-ekspres", {
                "en": "Ride up over the forest and have lunch at the top with the whole valley below. It can stop in strong wind.",
                "it": "Sali sopra il bosco e pranza in cima con tutta la valle sotto di te. Può fermarsi con il vento forte.",
                "sq": "Ngjitu mbi pyll dhe ha drekë lart, me gjithë luginën poshtë. Mund të ndalojë kur fryn erë e fortë."}),
            ("15:30", "grand-park", {
                "en": "Back in town, walk around the lake in the late afternoon light.",
                "it": "Tornato in città, fai il giro del lago nella luce del tardo pomeriggio.",
                "sq": "Kthehu në qytet dhe bëj xhiron e liqenit me dritën e pasdites."}),
            ("18:30", "mullixhiu", {
                "en": "Dinner at the park entrance. The room is small, so book a table before you go.",
                "it": "Cena all'ingresso del parco. La sala è piccola, quindi prenota prima di andare.",
                "sq": "Darka në hyrje të parkut. Salla është e vogël, ndaj rezervo tavolinë para se të shkosh."}),
            ("21:00", "radio-bar", {
                "en": "A short walk into Blloku for an unhurried last drink.",
                "it": "Due passi fino al Blloku per un ultimo drink senza fretta.",
                "sq": "Pak hapa deri në Bllok për një pije të fundit pa nxitim."}),
        ],
    },
    {
        "slug": "rainy-day",
        "hero": "house-of-leaves",
        "title": {"en": "A rainy day", "it": "Una giornata di pioggia", "sq": "Një ditë me shi"},
        "summary": {
            "en": "Museums, a covered lunch and raki in a café full of old radios. Every stop is a few minutes' walk from the last.",
            "it": "Musei, un pranzo al coperto e raki in un caffè pieno di vecchie radio. Ogni tappa è a pochi minuti dalla precedente.",
            "sq": "Muze, drekë nën çati dhe raki në një kafene plot radio të vjetra. Çdo ndalesë është disa minuta larg së mëparshmes.",
        },
        "lead": {
            "en": "When the weather turns, stay indoors and go deep into Albania's history. The longest walk between stops is under ten minutes.",
            "it": "Quando il tempo cambia, resta al chiuso e scopri a fondo la storia dell'Albania. Il tratto più lungo tra due tappe è sotto i dieci minuti.",
            "sq": "Kur prishet koha, rri brenda dhe njih nga afër historinë e Shqipërisë. Ecja më e gjatë mes dy ndalesave është nën dhjetë minuta.",
        },
        "when": {"en": "Tuesday to Sunday", "it": "Da martedì a domenica", "sq": "Nga e marta te e diela"},
        "stops": [
            ("10:00", "national-historical-museum", {
                "en": "The country's story from antiquity to the dictatorship. Give it at least 90 minutes. Closed on Mondays.",
                "it": "La storia del paese dall'antichità alla dittatura. Dedicale almeno 90 minuti. Chiuso il lunedì.",
                "sq": "Historia e vendit nga antikiteti te diktatura. Jepi të paktën 90 minuta. Mbyllur të hënën."}),
            ("12:30", "tirana-castle", {
                "en": "Lunch under cover in the restaurants inside the old walls.",
                "it": "Pranzo al riparo nei ristoranti dentro le vecchie mura.",
                "sq": "Drekë nën strehë në restorantet brenda mureve të vjetra."}),
            ("14:00", "house-of-leaves", {
                "en": "The secret police's surveillance centre, with the microphones and files they used.",
                "it": "Il centro di sorveglianza della polizia segreta, con i microfoni e i fascicoli che usava.",
                "sq": "Qendra e përgjimit të Sigurimit, me mikrofonat dhe dosjet që përdorte."}),
            ("15:30", "national-gallery", {
                "en": "Albanian art from icons to socialist realism. If the rain stops, see the statue garden at the back.",
                "it": "Arte albanese dalle icone al realismo socialista. Se smette di piovere, guarda il giardino delle statue sul retro.",
                "sq": "Arti shqiptar nga ikonat te realizmi socialist. Nëse pushon shiu, shiko kopshtin e statujave prapa."}),
            ("17:00", "komiteti", {
                "en": "Warm up with a raki tasting among old radios and posters.",
                "it": "Riscaldati con una degustazione di raki tra vecchie radio e manifesti.",
                "sq": "Ngrohu me një provë rakish mes radiove dhe posterave të vjetër."}),
        ],
    },
]

# Tekstet e ndërfaqes
UI = {
    "en": {
        "nav": "Itineraries",
        "index_title": "Ready-made itineraries",
        "index_lead": "Routes for a day in Tirana, stop by stop, with the time to get there and the bus when it's too far to walk.",
        "eyebrow": "Itinerary",
        "stops_n": "{n} stops",
        "stops": "Stops",
        "km_walk": "On foot",
        "bus_rides": "Bus rides",
        "best_day": "Best day",
        "walk": "Walk about {m} min",
        "walk_dist": "{d}",
        "directions": "Walking directions",
        "bus": "About {km} km: too far to walk",
        "bus_btn": "Find the bus",
        "start_from": "Start from {name}",
        "time_there": "Time there",
        "hours": "Hours",
        "map": "Map of the route",
        "note": "Times are a suggestion, so move them around as you like. Opening hours can change: check them before you go.",
        "others": "More itineraries",
        "view": "See the itinerary",
        "home_eyebrow": "Plan your day",
        "home_title": "Ready-made itineraries",
        "home_lead": "Not sure where to start? Follow one of our routes, stop by stop.",
        "none": "None",
    },
    "it": {
        "nav": "Itinerari",
        "index_title": "Itinerari pronti",
        "index_lead": "Percorsi per una giornata a Tirana, tappa per tappa, con il tempo per arrivarci e l'autobus quando è troppo lontano a piedi.",
        "eyebrow": "Itinerario",
        "stops_n": "{n} tappe",
        "stops": "Tappe",
        "km_walk": "A piedi",
        "bus_rides": "Corse in autobus",
        "best_day": "Giorno ideale",
        "walk": "Circa {m} min a piedi",
        "walk_dist": "{d}",
        "directions": "Indicazioni a piedi",
        "bus": "Circa {km} km: troppo lontano a piedi",
        "bus_btn": "Trova l'autobus",
        "start_from": "Partenza da {name}",
        "time_there": "Tempo di visita",
        "hours": "Orari",
        "map": "Mappa del percorso",
        "note": "Gli orari sono un suggerimento: spostali come preferisci. Gli orari di apertura possono cambiare, controllali prima di andare.",
        "others": "Altri itinerari",
        "view": "Vedi l'itinerario",
        "home_eyebrow": "Organizza la giornata",
        "home_title": "Itinerari pronti",
        "home_lead": "Non sai da dove cominciare? Segui uno dei nostri percorsi, tappa per tappa.",
        "none": "Nessuna",
    },
    "sq": {
        "nav": "Itinerare",
        "index_title": "Itinerare të gatshme",
        "index_lead": "Rrugë për një ditë në Tiranë, ndalesë pas ndalese, me kohën që të duhet për të shkuar dhe autobusin kur është shumë larg për të ecur.",
        "eyebrow": "Itinerar",
        "stops_n": "{n} ndalesa",
        "stops": "Ndalesa",
        "km_walk": "Në këmbë",
        "bus_rides": "Me autobus",
        "best_day": "Dita më e mirë",
        "walk": "Rreth {m} min në këmbë",
        "walk_dist": "{d}",
        "directions": "Si të shkosh në këmbë",
        "bus": "Rreth {km} km: shumë larg për të ecur",
        "bus_btn": "Gjej autobusin",
        "start_from": "Nisu nga {name}",
        "time_there": "Koha aty",
        "hours": "Orari",
        "map": "Harta e rrugës",
        "note": "Oraret janë sugjerim, ndaj ndryshoji si të duash. Oraret e hapjes mund të ndryshojnë: kontrolloji para se të shkosh.",
        "others": "Itinerare të tjera",
        "view": "Shiko itinerarin",
        "home_eyebrow": "Planifiko ditën",
        "home_title": "Itinerare të gatshme",
        "home_lead": "Nuk di nga t'ia fillosh? Ndiq një nga rrugët tona, ndalesë pas ndalese.",
        "none": "Asnjë",
    },
}
