from collections import defaultdict
from random import choice

from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget
from unidecode import unidecode

from games.bingo import BingoGrid
from games.motus import MotusGrid
from games.teams import MotusTeam
from glcore.application import Application, MediaPlayer

DICTIONARY: dict[int, set[str]] = defaultdict(
    set,
    {
        5: {
            "paris",
            "motus",
            "lapin",
            "pomme",
            "biere",
            "coder",
            "sport",
            "badge",
            "cloud",
            "mysql",
            "linux",
            "sympa",
            "funky",
            "chill",
            "covid",
            "pixel",
        },
        6: {
            "python",
            "rennes",
            "nantes",
            "docker",
            "gitlab",
            "zinzin",
            "jungle",
            "zouave",
            "marmot",
            "soleil",
            "banane",
            "canard",
            "tresor",
            "oignon",
            "projet",
            "pastis",
        },
        7: {
            "quarkus",
            "serveur",
            "sardine",
            "biscuit",
            "voiture",
            "erratum",
            "galette",
            "sourire",
            "exemple",
            "licorne",
            "webhook",
            "console",
            "clavier",
            "placard",
            "serrure",
            "galaxie",
        },
        8: {
            "frontend",
            "pipeline",
            "fretille",
            "musicien",
            "chocolat",
            "conduire",
            "paquebot",
            "intranet",
            "internet",
            "portable",
            "logiciel",
            "festival",
            "bretagne",
            "saucisse",
            "folichon",
            "rigolade",
        },
        9: {
            "framework",
            "grotesque",
            "spikeeday",
            "froussard",
            "telephone",
            "brouillon",
            "promotion",
            "momomotus",
            "confiance",
            "afterwork",
            "optimiste",
            "equilibre",
            "vacancier",
            "delicieux",
            "curiosite",
            "captivant",
        },
    },
)

# mots = [
#     "pomme", "chien", "ordinateur", "soleil", "montagne", "plage", "piano",
#     "voiture", "fraise", "etoile", "basket", "television", "livre", "foret",
#     "girafe", "banane", "ciel", "elephant", "guitare", "hopital", "jardin",
#     "kiwi", "lampe", "mer", "nuage", "orange", "parapluie", "quiche", "restaurant",
#     "souris", "table", "velo", "wagon", "xylophone", "yogourt", "zebre",
#     "amour", "bonheur", "chocolat", "danse", "eau", "famille", "gateau",
#     "hiver", "ile", "jouet", "kangourou", "lune", "miel", "nuit",
#     "oiseau", "puzzle", "quartier", "rose", "sourire", "tapis", "univers",
#     "voyage", "weekend", "xenophobe", "yaourt", "zen", "cactus", "delicieux",
#     "energie", "feuille", "genereux", "hibou", "internet", "jazz", "kiosque",
#     "lycee", "magnifique", "noir", "opera", "piscine", "quizz", "radiateur",
#     "samedi", "tambour", "ultrason", "velours", "whisky", "xylographe", "yoga",
#     "zephyr", "arcenciel", "boussole", "chamallow", "desert", "escalier", "frisson",
#     "galaxie", "horizon", "infini", "jumelles", "kayak", "labyrinthe", "metaphore",
#     "nenuphar", "obscurite", "papillon", "quasar", "retro", "sphere", "tourbillon",
#     "ultimatum", "velociraptor", "wok", "xylophoniste", "yacht", "ziggourat",
#     "abandon", "abattre", "aberration", "abreuvoir", "absence", "absolu", "abuser",
#     "accepter", "acclamer", "accrocher", "accuser", "achat", "acier", "acoustique",
#     "acquérir", "acteur", "actif", "adaptable", "addition", "adieu", "admettre",
#     "adorer", "adresser", "aduler", "affaire", "affiche", "affreux", "âge",
#     "agir", "agréable", "ahurir", "aider", "aiguille", "ailleurs", "aimable",
#     "ajouter", "alarme", "album", "alcool", "alerte", "algèbre", "aligner",
#     "aliment", "aller", "allumer", "alors", "alpaga", "amateur", "ambiance",
#     "améliorer", "amertume", "amidon", "amour", "ampleur", "amusant", "analogie",
#     "analyse", "ancien", "angle", "animal", "année", "annoncer", "apercevoir",
#     "apparence", "applaudir", "appoint", "apprendre", "approcher", "argument", "arôme",
#     "arracher", "arriver", "article", "aspect", "asseoir", "assister", "assurer",
#     "astre", "atelier", "atome", "atrocité", "attacher", "attendre", "aubaine",
#     "aucun", "audace", "aurore", "automne", "autruche", "avaler", "avancer",
#     "avenir", "averse", "avis", "avoir", "avouer", "avril", "axiome",
#     "badge", "bagage", "baignade", "baisser", "balader", "balayer", "baleine",
#     "bambou", "banal", "barbecue", "barge", "baril", "barrer", "bassine",
#     "batir", "battre", "beauté", "bébé", "bécane", "belote", "benevole",
#     "berceau", "besoin", "béton", "beurre", "biais", "biceps", "bidule",
#     "bilan", "bille", "binôme", "biologie", "biopsie", "biscuit", "bistouri",
#     "bitume", "bizarre", "blâmer", "blé", "blessure", "blinder", "blocage",
#     "blond", "bloquer", "blouse", "bobine", "bocage", "boire", "boiter",
#     "bolide", "bonheur", "bonjour", "bonus", "bordure", "bosse", "boucle",
#     "bouée", "bouger", "boulot", "bourgeon", "bousculer", "boutique", "boxeur",
#     "branche", "bras", "brave", "briller", "brin", "briser", "brochure",
#     "broder", "bronze", "brosse", "bruit", "brûler", "brume", "bulle",
#     "bureau", "burin", "buste", "buter", "buvable", "buzzer", "câble",
#     "caché", "cadeau", "cagoule", "caisse", "calcul", "calepin", "cambriolage",
#     "camion", "canal", "canard", "canif", "capable", "capot", "carabine",
#     "carbone", "caresser", "caribou", "carnage", "carotte", "carreau", "cartable",
#     "casier", "casque", "casserole", "causer", "cavité", "ceinture", "cela",
#     "cendrier", "censure", "cerise", "cerner", "cerveau", "cesser", "chagrin",
#     "chaise", "chaleur", "champion", "chance", "chapitre", "charnière", "chasse",
#     "chaudron", "chaussure", "chercher", "cheveu", "chiffre", "chignon", "chimère",
#     "chiot", "chlore", "choc", "choisir", "chose", "chouette", "chrome",
#     "chute", "cibler", "cidre", "ciel", "cigare", "cimetière", "cingler",
#     "cire", "cirque", "citerne", "citron", "civil", "clairon", "clameur",
#     "clan", "clavier", "cliché", "climat", "cliquetis", "cloner", "cloche",
#     "clôture", "clown", "cocon", "coiffer", "cojoindre", "colère", "colline",
#     "colmater", "colon", "combat", "comédie", "comité", "commencer", "comparer",
#     "complet", "compris", "comte", "concours", "condamner", "confiance", "confort",
#     "congé", "conclure", "conduire", "confier", "congeler", "conifère", "connaître",
#     "conquérir", "consulter", "contenir", "convaincre", "copier", "coquille", "corail",
#     "corbeau", "corde", "corne", "corps", "correct", "coton", "couche",
#     "coude", "coudre", "cougar", "couleur", "couper", "courage", "courbe",
#     "courir", "court", "couteau", "couvrir", "crabe", "crainte", "crampon",
#     "crane", "cravate", "créature", "crédit", "crème", "crépir", "creuser",
#     "crier", "crime", "crin", "crise", "crochet", "croisière", "croquer",
#     "cruauté", "cube", "culot", "culture", "cumulus", "cupide", "curatif",
#     "cure", "curseur", "cyber", "cycle", "cylindre", "cynique", "dame",
#     "danger", "danse", "dard", "date", "davantage", "debout", "décéder",
#     "déchirer", "décider", "déclarer", "décrire", "déduire", "défendre", "dégager",
#     "déjeuner", "délice", "demain", "demander", "demeurer", "dément", "démission",
#     "démontrer", "départ", "dépenser", "déplorer", "déposer", "déranger", "dernier",
#     "dérober", "désastre", "descendre", "désert", "déshabiller", "désigner", "déssiner",
#     "destin", "détacher", "détour", "détruire", "dette", "deuil", "devenir",
#     "deviner", "devoir", "diable", "dialogue", "diamant", "dicter", "dieu",
#     "différer", "diffuser", "digérer", "digne", "diluer", "dimanche", "diminuer",
#     "dîner", "diplôme", "dire", "diriger", "discuter", "disposer", "distance",
#     "divertir", "diviser", "dobler", "document", "dogme", "doigt", "dominer",
#     "donner", "doré", "dos", "douane", "doubler", "douceur", "douter",
#     "doyen", "dragon", "draper", "dresser", "droit", "dur", "durcir",
#     "durer", "eau", "éblouir", "écarlate", "écart", "échapper", "échelle",
#     "éclair", "éclipse", "école", "écouter", "écraser", "écrire", "éditer",
#     "éducation", "effacer", "effet", "effrayer", "égaliser", "égarer", "éjecter",
#     "élaborer", "élargir", "électrique", "élégant", "éléphant", "élever", "élixir",
#     "elle", "éloigner", "élu", "emballer", "embellir", "embouteillage", "embrasser",
#     "émeraude", "émotion", "émouvoir", "empêcher", "employer", "emporter", "encadrer",
#     "enchère", "enclave", "encombre", "encore", "endive", "endormir", "endroit",
#     "énergie", "enfance", "enfer", "enfler", "enfoncer", "enfreindre", "enfuir",
#     "engager", "engloutir", "engrais", "enjamber", "enjeu", "enlever", "ennemi",
#     "ennuyeux", "énorme", "enquêter", "enrichir", "ensemble", "entamer", "entendre",
#     "entier", "entonner", "entraîner", "entreprendre", "envelopper", "envie", "envoyer",
#     "épaisseur", "éparpiller", "épée", "épelucher", "épicer", "épier", "épilogue",
#     "épine", "époque", "épreuve", "éprouver", "épuiser", "équateur", "équiper",
#     "équivalent", "équivoque", "ériger", "erreur", "éruption", "escalader", "esclave",
#     "espèce", "espoir", "esquisse", "essayer", "essence", "essieu", "essor",
#     "estomac", "estrade", "étage", "étagère", "étaler", "état", "éteindre",
#     "étendre", "éternel", "éthique", "étirer", "étoile", "étonner", "étouffer",
#     "étroit", "évacuer", "évader", "évaluer", "évasion", "éveiller", "éviter",
#     "exact", "examiner", "exaucer", "excéder", "exclure", "excuse", "exécuter",
#     "exemple", "exercer", "exiger", "exil", "exister", "expirer", "expliquer",
#     "exploiter", "explorer", "exporter", "exprimer", "exquis", "extase", "externe",
#     "extrême", "exulter", "fabriquer", "face", "facette", "facile", "facture",
#     "faible", "falaise", "falloir", "fameux", "famille", "farce", "fatal",
#     "fatigue", "faune", "favori", "faxer", "fébrile", "féconder", "féculent",
#     "fédérer", "félin", "femme", "fendre", "féroce", "ferveur", "festin",
#     "fêter", "feuille", "feutre", "fiable", "fibre", "fiction", "fichu",
#     "fidèle", "figer", "figure", "filet", "filmer", "filou", "filtrer",
#     "fin", "finalement", "finir", "fiole", "firme", "fixer", "flairer",
#     "flamme", "fléau", "flegme", "fleur", "flocon", "flore", "fluctuer",
#     "fluide", "fluvial", "folie", "fonction", "fondre", "faible", "forcer",
#     "forêt", "forge", "forme", "fort", "fosse", "fou", "foudre",
#     "fouet", "fouine", "foule", "four", "foyer", "fraction", "fracture",
#     "fragile", "frais", "framboise", "frapper", "frayeur", "frémir", "fréquence",
#     "friction", "frisson", "frivole", "froisser", "fructueux", "fruit", "fugue",
#     "fuir", "fuite", "fumer", "fureur", "furieux", "fusée", "fuser",
#     "fusil", "futur", "gagner", "galerie", "gambader", "garage", "garde",
#     "gardien", "garnir", "gaz", "gazon", "geler", "générer", "géant",
#     "gélatine", "geler", "gémir", "génial", "génie", "genou", "gentil",
#     "genre", "géologie", "geste", "gibier", "gicler", "gilet", "girafe",
#     "givre", "glace", "glisser", "globe", "gloire", "gluant", "glycine",
#     "gobelet", "golf", "gorge", "gosier", "goutte", "grâce", "grain",
#     "gramme", "grand", "gras", "gratter", "gravier", "grelot", "grenade",
#     "griffe", "griller", "grimper", "grogner", "gronder", "gros", "grotte",
#     "groupe", "grue", "guépard", "guerre", "guetter", "guide", "guider",
#     "guimauve", "guirlande", "guitare", "gymnaste", "gypse", "habiter", "hache",
#     "halte", "hameau", "hangar", "hanter", "haras", "haricot", "harpe",
#     "hasard", "haut", "hélicoptère", "hérisson", "hermine", "héro", "hésiter",
#     "heureux", "hibou", "hier", "histoire", "hiver", "hochet", "homme",
#     "honnête", "honoré", "horde", "horizon", "horloge", "hormone", "hortensia",
#     "hôtel", "houle", "houlette", "houppe", "hourra", "huître", "humble",
#     "humide", "humour", "hurler", "hurrah", "hutte", "hydromel", "hydrater",
#     "idée", "ignorer", "igre", "iguane", "illicite", "illégal", "illusion",
#     "image", "imaginer", "imiter", "immense", "immobile", "immortalité", "impératif",
#     "imploser", "importer", "imposer", "imprimer", "incarner", "incendie", "incident",
#     "incliner", "inconnu", "incruster", "indiquer", "indice", "inducteur", "inférer",
#     "infliger", "informer", "ingénieur", "inhaler", "inhiber", "initer", "injecter",
#     "injustice", "innocent", "inoculer", "inonder", "inscrire", "insister", "inspecter",
#     "inspirer", "installer", "instruire", "insulter", "intégrer", "intéresser", "interne",
#     "intimer", "intoxiquer", "intrigue", "inventer", "inviter", "invoquer", "iode",
#     "iris", "issue", "ivresse", "jaguar", "jaillir", "jalousie", "jambe",
#     "jargon", "jardin", "jauge", "jaunir", "jeter", "jeton", "jeudi",
#     "jeune", "joie", "joindre", "jouer", "jour", "jubiler", "juger",
#     "jumeler", "jungle", "junior", "jupon", "jurer", "juron", "jury",
#     "kaki", "kangourou", "karaté", "kayak", "kenyan", "ketchup", "kilo",
#     "kiwi", "koala", "labourer", "labyrinthe", "lac", "lacet", "laine",
#     "laisser", "lambeau", "lamelle", "lampe", "lanceur", "langage", "lanterne",
#     "lapin", "large", "larme", "laver", "laxatif", "lèche", "lecture",
#     "légal", "léger", "légume", "lent", "leçon", "lézard", "liane",
#     "libérer", "libre", "licorne", "liège", "lier", "lire", "lisser",
#     "liste", "litre", "livre", "lobe", "local", "logique", "loin",
#     "loisir", "long", "lopin", "louer", "lourd", "louve", "loyal",
#     "lubie", "lucide", "lueur", "lugubre", "luisant", "lumière", "lundi",
#     "lune", "lupin", "lutin", "lutte", "luxe", "lynx", "lyrique",
#     "macaron", "machine", "magenta", "magique", "magnifique", "maigre", "main",
#     "maintien", "maison", "majesté", "malade", "malheur", "malin", "manche",
#     "manger", "manier", "manquer", "marche", "mardi", "marge", "mariage",
#     "marquer", "masque", "masse", "masure", "matelas", "matière", "maudit",
#     "mauvais", "meilleur", "mélanger", "membre", "même", "mépriser", "merci",
#     "mère", "merle", "mesure", "métal", "météore", "méthode", "métier",
#     "mettre", "meuble", "meunier", "meute", "midi", "miel", "miette",
#     "mieux", "milieu", "mille", "mime", "mince", "mineur", "mini",
#     "minute", "miracle", "miroir", "misère", "missile", "mixte", "mobile",
#     "mode", "moelleux", "mois", "moment", "monde", "monnaie", "monsieur",
#     "monter", "moquer", "morceau", "mordre", "morose", "morsure", "mortel",
#     "morue", "motif", "mouche", "moulin", "mourir", "mousse", "mouton",
#     "mouvement", "moyen", "muet", "muir", "muguet", "multiplier", "munir",
#     "mûr", "muraille", "mûrir", "muscle", "muse", "mushroom", "musique",
#     "mût", "mutuel", "myriade", "mystère", "mythique", "nageur", "nappe",
#     "narine", "narrer", "natal", "natif", "naître", "naître", "nature",
#     "naval", "navigateur", "navire", "neige", "nerf", "nerveux", "nettoyer",
#     "neuf", "neutraliser", "neutron", "neveu", "niche", "nicher", "nier",
#     "niveau", "noblesse", "noce", "noir", "noisette", "nomade", "nombre",
#     "nommer", "nonchalant", "nordique", "norme", "noter", "notre", "nouer",
#     "nougat", "nourrir", "nous", "nouveau", "novice", "noyau", "noyer",
#     "nuage", "nuancer", "nuire", "nuit", "nul", "nuque", "nuptial",
#     "nuque", "oasis", "objet", "obtenir", "obus", "occasion", "occuper",
#     "océan", "octobre", "odeur", "odorat", "œil", "œuf", "offenser",
#     "officier", "offrir", "ogre", "oiseau", "ombre", "onctueux", "onduler",
#     "onirique", "onze", "opérer", "opposer", "opulente", "orange", "orbite",
#     "ordinaire", "orifice", "origine", "oser", "osmose", "ossature", "otage",
#     "oubliez", "ouest", "ours", "outil", "outrage", "ouvert", "ouvrir",
#     "oxygène", "ozone", "pacha", "pacifier", "pacte", "pagayer", "page",
#     "paille", "pain", "paire", "paix", "palace", "palissade", "palmier",
#     "palpiter", "panache", "pancarte", "panda", "panique", "panneau", "panorama",
#     "pantalon", "papier", "papillon", "papoter", "parade", "parc", "pardonner",
#     "pareil", "parfum", "parler", "parmi", "parole", "partir", "parvenir",
#     "passer", "pastèque", "patauger", "patinage", "patrie", "patron", "pause",
#     "pauvre", "paver", "payer", "paysage", "peau", "pêche", "pécher",
#     "pédiatre", "pédaler", "peigner", "peinture", "pelage", "pelé", "pelouse",
#     "pénalité", "pencher", "pendule", "pénétrer", "pénible", "pension", "pentagone",
#     "pepper", "percé", "percer", "perdu", "péril", "période", "perle",
#     "permis", "perplexe", "perruche", "persil", "personne", "perte", "peser",
#     "pesticide", "petit", "pétrole", "peur", "pharaon", "phobie", "phoque",
#     "photon", "phrase", "physique", "piano", "pierre", "pile", "pilote",
#     "piment", "pincer", "pinceau", "pingouin", "pins", "pion", "piquer",
#     "pirate", "pire", "pirogue", "piscine", "piston", "pivot", "pizza",
#     "placer", "plage", "plaire", "plan", "plaque", "plastron", "plateau",
#     "plein", "pleurer", "pliage", "plomb", "plonger", "plot", "pluie",
#     "plume", "plumet", "plus", "plutôt", "pneu", "poche", "podium",
#     "poème", "poète", "poids", "poing", "poire", "poison", "poitrine",
#     "polaire", "pôle", "police", "polir", "pollen", "pomme", "pompier",
#     "poncer", "pondre", "pont", "population", "porc", "port", "poser",
#     "position", "possible", "poste", "potage", "potin", "poubelle", "pouce",
#     "poudre", "poulet", "poupée", "pour", "pousser", "poutre", "pouvoir",
#     "prairie", "pratique", "précieux", "prédire", "préfixe", "préjugé", "prélude",
#     "prénom", "présence", "prétexte", "prévoir", "prier", "principe", "privé",
#     "prix", "prochain", "proclamer", "procès", "professeur", "proie", "projeter",
#     "promener", "prononcer", "propre", "prospectus", "protéger", "prouver", "proverbe",
#     "prudence", "prune", "public", "puce", "puiser", "pull", "pulpe",
#     "pulse", "puma", "punir", "purifier", "puzzle", "pyjama", "pyramide",
#     "quand", "quantité", "quartier", "quasi", "quête", "question", "qui",
#     "quinze", "quitter", "quoi", "rabais", "raboter", "racine", "raconter",
#     "radar", "rafale", "rage", "ragot", "raideur", "raisin", "rajeunir",
#     "ramasser", "rancard", "rang", "rapace", "rapide", "rasage", "raser",
#     "rasoir", "rassurer", "rater", "ratio", "rature", "ravage", "ravir",
#     "rayer", "réaction", "réagir", "réaliser", "réanimer", "rebond", "recette",
#     "recevoir", "recherche", "record", "reculer", "récurer", "redevenir", "redouter",
#     "refuser", "regarder", "régime", "région", "regretter", "rein", "rejeter",
#     "rejoindre", "relation", "relever", "religion", "remarquer", "remède", "remise",
#     "remonter", "remplir", "remuer", "rencontre", "rendre", "renier", "renoncer",
#     "rentrer", "renverser", "reposer", "reproche", "requin", "réserver", "résine",
#     "résoudre", "respecter", "rester", "retard", "retenir", "retirer", "retour",
#     "retrouver", "réussir", "revenir", "revoir", "revue", "rhume", "ricaner",
#     "riche", "rideau", "ridicule", "rien", "rigide", "rigoler", "rincer",
#     "rire", "risquer", "rituel", "rivière", "robe", "robot", "robuste",
#     "rocade", "roche", "rodeur", "rogner", "rognon", "rond", "ronfler",
#     "ronger", "roquet", "rosir", "rotation", "rouge", "rouler", "rouleau",
#     "route", "ruban", "rubis", "ruche", "rude", "ruelle", "ruiner",
#     "ruisseau", "ruser", "rustre", "sable", "sabot", "sabre", "sac",
#     "sachet", "sacoche", "safari", "sage", "sain", "saisir", "salade",
#     "salé", "salir", "salon", "saluer", "samedi", "sanction", "sang",
#     "sanguine", "sanitaire", "saper", "sarcasme", "sardine", "saturer", "saugrenu",
#     "saumon", "saut", "sauver", "savoir", "science", "scinder", "scolaire",
#     "score", "scruter", "sculpter", "séance", "sécher", "secouer", "sécréter",
#     "séduire", "seigneur", "sein", "séjour", "sélectif", "selon", "semaine",
#     "sembler", "semer", "semestre", "sensuel", "sentir", "séparer", "serrure",
#     "sertir", "servir", "seuil", "seulement", "short", "sien", "sieste",
#     "siffler", "sigle", "signal", "silence", "silicium", "silo", "simple",
#     "singe", "sinon", "sinus", "siphon", "sirop", "site", "situer",
#     "skier", "slice", "social", "société", "soda", "soigner", "soir",
#     "soixante", "soja", "solaire", "soldat", "soleil", "solide", "solo",
#     "sombrer", "somme", "sommet", "somnoler", "sonde", "songer", "sonner",
#     "sorcier", "sortir", "sosie", "sottise", "souci", "soudain", "souffrir",
#     "souhaiter", "soulever", "soumettre", "soupe", "sourd", "soustraire", "soutenir",
#     "souvent", "soyeux", "spectacle", "sport", "stade", "stagiaire", "stand",
#     "stanchez", "star", "station", "sternum", "stimuler", "stipuler", "stop",
#     "store", "style", "suave", "subir", "sucre", "suer", "suffire",
#     "suggérer", "suivre", "sujet", "sulfite", "supérieur", "supplier", "supporter",
#     "surprendre", "surtout", "surveiller", "tache", "taille", "taire", "talon",
#     "tambour", "tamiser", "tanguer", "tanin", "tant", "taper", "tapis",
#     "tard", "tarte", "tasse", "taureau", "taux", "taverne", "taxer",
#     "taxi", "tellement", "témoin", "tempête", "temple", "tenace", "tendre",
#     "tenir", "tenter", "terme", "terre", "test", "texte", "thé",
#     "théâtre", "thème", "tiare", "tibia", "tic", "tien", "tige",
#     "tipi", "tirer", "tissu", "titre", "toast", "toge", "toile",
#     "toiser", "toit", "tomber", "tome", "tonne", "tonte", "toque",
#     "tordre", "torse", "tortue", "totem", "toucher", "toujours", "tour",
#     "tousser", "tout", "toux", "trace", "traduire", "train", "trancher",
#     "travail", "trésor", "tribu", "tricher", "trier", "trio", "tripe",
#     "triste", "troc", "trois", "tromper", "tronc", "trop", "trouer",
#     "trouver", "tube", "tuile", "turbo", "tutu", "tuyau", "type",
#     "tyran", "ubiquité", "ulcère", "ultrason", "unanime", "unir", "unité",
#     "universalité", "université", "urne", "usage", "usine", "usure", "utile",
#     "utopie", "vache", "vague", "vaillant", "vaincre", "valeur", "valider",
#     "valise", "vallon", "valve", "vampire", "vase", "vaste", "veau",
#     "vécu", "vecteur", "végétal", "véhicule", "veiller", "veine", "velours",
#     "velu", "vendre", "venir", "vent", "venue", "verbe", "verdict",
#     "vérifier", "vers", "vertige", "verve", "veste", "vétérinaire", "veulerie",
#     "vider", "vie", "vierge", "vieux", "vif", "vigne", "vigueur",
#     "vilain", "village", "vinaigre", "vindicte", "vinyle", "violon", "vipe",
#     "virage", "virgule", "virtuel", "virus", "visage", "viser", "vision",
#     "visqueux", "visuel", "vital", "vitesse", "vitraux", "vivant", "vivider",
#     "vivre", "vocal", "vodka", "vogue", "voici", "voile", "voir",
#     "voisin", "voiture", "volaille", "volcan", "voler", "voltiger", "volume",
#     "voter", "votre", "vouloir", "vous", "voyage", "voyager", "voyelle",
#     "vrai", "vue", "vulgaire", "wagon", "wagon", "zèbre", "zèle",
#     "zénith", "zeste", "zinc", "zone", "zoom"
# ]


# for m in mots:
#     if len(m) >= 5:
#         DICTIONARY[len(m)].add(m)


class MotusEngine(Application):
    """The Motus game engine class."""

    MAX_ATTEMPTS = 6

    def __init__(self, n):
        self.i = 0  # current attempt
        self.j = 0  # current letter
        self.k = 0  # current team
        self.n = n  # number of teams
        self.length_key = None
        self.is_playing = False

        super().__init__()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)

        if not self.is_playing:
            self.setup_word()
            self.is_playing = True
            return

        if event.isAutoRepeat() and not event.key() == Qt.Key.Key_Backspace:
            return

        if event.text().isalpha():
            if self.j < len(self.secret_word):
                self.grid.motus[self.i][self.j].active = False
                self.grid.motus[self.i][self.j].text = unidecode(event.text()).upper()
                self.grid.motus[self.i][self.j].repaint()
                self.j += 1

                if self.j < len(self.secret_word):
                    self.grid.motus[self.i][self.j].active = True
                    self.grid.motus[self.i][self.j].repaint()

        elif event.key() == Qt.Key.Key_Backspace:
            if self.j > 0:
                if self.j != len(self.secret_word):
                    self.grid.motus[self.i][self.j].active = False
                    self.grid.motus[self.i][self.j].repaint()

                self.j -= 1
                self.grid.motus[self.i][self.j].active = True
                self.grid.motus[self.i][self.j].text = self.secret_word[self.j] if self.grid.corrects[self.j] else "."
                self.grid.motus[self.i][self.j].repaint()

        elif event.key() == Qt.Key.Key_Return:
            if self.j < len(self.secret_word):
                self.grid.motus[self.i][self.j].active = False
                self.grid.motus[self.i][self.j].repaint()

            guess = "".join(label.text if i < self.j else " " for i, label in enumerate(self.grid.motus[self.i]))

            self.grid.update_line(self.i, self.j, self.secret_word, guess)

            match_found = self.j == len(self.secret_word) and guess == self.secret_word

            if match_found or self.i == self.MAX_ATTEMPTS - 1:
                if match_found:
                    MediaPlayer.play("victory")
                    self.grid.shine(self.i)
                    QThread.msleep(100)
                    self.teams[self.k].score += (self.MAX_ATTEMPTS - self.i) * 10
                    self.teams[self.k].draw_balls()
                else:
                    MediaPlayer.play("loose")
                    self.grid.update_line(self.i, self.j, self.secret_word)

                QThread.msleep(3000)

                self.teams[self.k].active = False
                self.teams[self.k].repaint()
                self.k = (self.k + 1) % self.n
                self.setup_word()
            else:
                self.i += 1
                self.j = 0
                self.grid.setup_line(self.i, self.secret_word)

    def init(self, container: QWidget):
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        container.setLayout(main_layout)

        left_bar = QVBoxLayout()
        left_bar.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.bingo_grids = QStackedWidget(container)
        self.bingo_grids.setFixedHeight(int(container.width() * 0.25))
        left_bar.addWidget(self.bingo_grids)

        teams_layout = QVBoxLayout()
        teams_layout.setContentsMargins(0, 0, 10, 0)
        teams_layout.setSpacing(10)
        self.teams = []
        for i in range(self.n):
            self.bingo_grids.addWidget(BingoGrid(i, container))
            self.teams.append(MotusTeam(i, self.bingo_grids))
            teams_layout.addWidget(self.teams[i])
        left_bar.addLayout(teams_layout)
        main_layout.addLayout(left_bar)

        self.grid = MotusGrid(container)
        self.grid.setFixedHeight(container.height())
        self.grid.setFixedWidth(int(container.width() * 0.75))
        main_layout.addWidget(self.grid)

    def setup_word(self):
        self.teams[self.k].active = True
        self.teams[self.k].repaint()

        self.i, self.j = 0, 0
        if self.k == 0:
            self.change_wlength()
        self.secret_word = self.get_secret_word()
        self.grid.setup(self.MAX_ATTEMPTS, len(self.secret_word))
        self.grid.setup_line(0, self.secret_word)
        self.bingo_grids.setCurrentIndex(self.k)

        if not self.bingo_grids.currentWidget().remaining_balls:
            self.bingo_grids.currentWidget().init_grid_animation()

    def change_wlength(self):
        self.length_key = choice(list(k for k, v in DICTIONARY.items() if len(v) >= self.n))

    def get_secret_word(self) -> str:
        word = choice(list(DICTIONARY[self.length_key]))
        DICTIONARY[self.length_key].remove(word)

        return unidecode(word).upper()
