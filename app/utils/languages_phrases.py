"""
languages_phrases.py
--------------------
Módulo que contiene los idiomas soportados por la aplicación
y ejemplos de frases para practicar pronunciación y comprensión.

Estructura:
- LANGUAGE_OPTIONS: Diccionario con los nombres visibles de los idiomas y sus códigos estándar.
- EXAMPLE_PHRASES: Diccionario con listas de frases de ejemplo por idioma.

"""

LANGUAGE_OPTIONS = {
    "Inglés (US)": "en-US",
    "Español (ES)": "es-ES",
    "Francés (FR)": "fr-FR",
    "Alemán (DE)": "de-DE",
    "Italiano (IT)": "it-IT"
}

EXAMPLE_PHRASES = {
    "en-US": [
        "The quick brown fox jumps over the lazy dog",
        "Hello world, how are you today?",
        "Practice makes perfect in language learning",
        "Can you please repeat that more slowly?",
        "It's a beautiful day to learn something new",
        "She sells seashells by the seashore",
        "I thought I saw a shadow in the corner",
        "Let’s grab a coffee and talk about the project",
        "Tomorrow will be better if we start today",
        "Please call me when you get home safely"
    ],
    "es-ES": [
        "El rápido zorro marrón salta sobre el perro perezoso",
        "Hola mundo, ¿cómo estás hoy?",
        "La práctica hace al maestro en el aprendizaje de idiomas",
        "¿Podrías repetirlo más despacio, por favor?",
        "Es un hermoso día para aprender algo nuevo",
        "Tres tristes tigres tragan trigo en un trigal",
        "No dejes para mañana lo que puedas hacer hoy",
        "Me gustaría un café con leche y una tostada, por favor",
        "El conocimiento es poder cuando se comparte",
        "Nos vemos pronto, cuídate mucho"
    ],
    "fr-FR": [
        "Le rapide renard brun saute par-dessus le chien paresseux",
        "Bonjour le monde, comment vas-tu aujourd'hui?",
        "La pratique rend parfait dans l'apprentissage des langues",
        "Pouvez-vous répéter plus lentement, s’il vous plaît?",
        "C’est une belle journée pour apprendre quelque chose de nouveau",
        "Un petit café pour bien commencer la journée",
        "Il ne faut jamais remettre à demain ce qu’on peut faire aujourd’hui",
        "Je voudrais un croissant et un jus d’orange, s’il vous plaît",
        "Parler plusieurs langues ouvre de nombreuses portes",
        "Merci beaucoup pour votre aide, c’était très gentil"
    ],
    "de-DE": [
        "Der schnelle braune Fuchs springt über den faulen Hund",
        "Hallo Welt, wie geht es dir heute?",
        "Übung macht den Meister beim Sprachenlernen",
        "Können Sie das bitte etwas langsamer wiederholen?",
        "Heute ist ein wunderschöner Tag zum Lernen",
        "Fischers Fritz fischt frische Fische",
        "Morgenstund hat Gold im Mund",
        "Ich hätte gern einen Kaffee ohne Zucker, bitte",
        "Wissen ist Macht, wenn man es teilt",
        "Danke für deine Hilfe, ich schätze das wirklich"
    ],
    "it-IT": [
        "La veloce volpe marrone salta sopra il cane pigro",
        "Ciao mondo, come stai oggi?",
        "La pratica rende perfetti nell'apprendimento delle lingue",
        "Puoi ripetere più lentamente, per favore?",
        "È una bella giornata per imparare qualcosa di nuovo",
        "Trentatré trentini entrarono a Trento tutti e trentatré trotterellando",
        "Non rimandare a domani ciò che puoi fare oggi",
        "Vorrei un cappuccino e una brioche, per favore",
        "Chi parla più lingue vede più mondi",
        "Grazie mille per il tuo aiuto, sei molto gentile"
    ]
}
