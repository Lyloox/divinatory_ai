import json
import random
from collections import Counter
from divinatory_ai.utils import bcolors

interpretations_fp = '../data/tarot_interpretations.json'
WAIT_BETWEEN_DRAWS = True

suits_set = {"wands", "cups", "swords", "coins"}

with open(interpretations_fp, 'r') as f:
    interpretations = json.load(f)
    interpretations = interpretations['tarot_interpretations']


def get_color(suit):
    if suit == 'major':
        return bcolors.CVIOLET2
    if suit == 'wands':
        return bcolors.CBLUE
    if suit == 'cups':
        return bcolors.CRED
    if suit == 'swords':
        return bcolors.OKCYAN
    if suit == 'coins':
        return bcolors.CYELLOW
    return bcolors.CGREYBG


def analyze_spread(suits_counter):
    dominance_threshold = sum(suits_counter.values()) // 2
    suits_top = suits_counter.most_common(1)[0]
    if suits_top[1] > dominance_threshold:
        # This suit is dominant
        suit = suits_top[0]
        print(get_color(suit) + suit.capitalize() + bcolors.ENDC +
              " are dominant: ", end='')
        if suit == 'wands':
            print("fiery energy; conflicting goals; hyperactivity; "
                  "emphasis on action")
        if suit == 'cups':
            print("emotionalism; emphasis on collaboration and feelings; "
                  "introspection")
        if suit == 'swords':
            print("emphasis on logic; paralysis by analysis; over-thinking")
        if suit == 'coins':
            print("practical concerns; emphasis on cost, value, health, "
                  "and body")

    suits_absents = suits_set.difference(suits_counter.keys())
    if len(suits_absents) == 1:
        suit = list(suits_absents)[0]
        print(get_color(suit) + suit.capitalize() + bcolors.ENDC +
              " suit is absent: ", end='')
        if suit == 'wands':
            print("Difficulty making things happen or action with no "
                  "real goal in mind")
        if suit == 'cups':
            print("clinical detachment; action with no thought of "
                  "impact; coldness")
        if suit == 'swords':
            print("lack of communication; impulsive action; "
                  "irrationality; confusion")
        if suit == 'coins':
            print("impracticality; no eye on the bottom line; "
                  "unhealthy choices")


def draw_keywords_for(*subjects, n_meanings=3):
    # Draw the expected number of cards
    nb_subjects = len(subjects)
    rate_reversed_cards = 1 / 4 if nb_subjects > 2 else 0
    cards = random.choices(interpretations, k=nb_subjects)

    # Print each card
    suits_counter = Counter()
    for subject, card in zip(subjects, cards):
        if card['suit'] != 'major':
            suits_counter.update([card['suit']])

        # Process text to display
        reversed = random.random() < rate_reversed_cards
        card_name = ' '.join([w.capitalize() for w in card['name'].split()])
        keywords = ' '.join(card['keywords'])
        meanings = card['meanings']['shadow' if reversed else 'light']
        if len(meanings) > n_meanings:
            meanings = random.choices(meanings, k=3)
        meanings = '\r\n'.join(meanings)

        print(f"{subject}\r\n" +
              get_color(card['suit']) +
              f"* {card_name}" + (" REVERSED" if reversed else "") +
              bcolors.ENDC +
              f" – {keywords}\r\n{meanings}")

        if WAIT_BETWEEN_DRAWS:
            input()

    # Analyze elementals
    analyze_spread(suits_counter)


def draw_fortune_telling_for(*subjects):
    nb_subjects = len(subjects)
    cards = random.choices(interpretations, k=nb_subjects)
    for subject, card in zip(subjects, cards):
        print(f"{subject}: " if subject else ""
        f"{' '.join([w.capitalize() for w in card['name'].split()])} – "
        f"{random.choice(card['fortune_telling'])}")


def get_spreads_dict():
    """
    Source for ideas: http://www.madebymark.com/wp-content/uploads/2015/11/A-Guide-to-Tarot-Card-Reading-Text-Only.txt
    :return:
    """
    spreads = dict()
    spreads.update({"Yes / No":
                        (lambda x: "Yes" if random.random() > 5 else "No", 42)})
    subjects = ["The first one tells you what led to this situation",
                "The second is what is actually going on",
                "The last is the actual result"]
    spreads.update({"Actual situation – Past, Present, Future":
                        (draw_keywords_for, subjects)})
    subjects = [""]
    spreads.update({"How or what can I do? What do I need to know today?":
                        (draw_fortune_telling_for, subjects)})
    subjects = ["The first represents why something should be done",
                "The second represents why something shouldn't be done"]
    spreads.update({"Pro / Con, should I?":
                        (draw_keywords_for, subjects)})
    subjects = ["Top card represent one perspective of your problem",
                "This represent represents another perspective",
                "This a first step you can take to transform it into a "
                "win-win situation",
                "And this is a second one"]
    spreads.update({"Conflict resolution – Crossroads Spread":
                        (draw_keywords_for, subjects)})
    subjects = ["The Situation – What is going on?",
                "The Foundation – The person or influence that perpetuates "
                "the situation",
                "The Past – How the foundation has shaped past events",
                "The Catalyst – Represents potentiel for change, shake things "
                "up, or redirect the flow of events",
                "The Result – the outcome, what you can expect with the "
                "Catalyst"]
    spreads.update({"Situation resolution – Minor Cross":
                        (draw_keywords_for, subjects)})
    subjects = ["Once Upon a Time – the situation in the beginning, before "
                "complications. \nPotential original goals or expectations.",
                "The Incident – how an action taken, a person met, or decision "
                "made changes the course of events",
                "Initial Response – your first most basic, impulsive response "
                "to the Incident",
                "Insight – something you must know in order to act with wisdom",
                "Resolution – The way out of the forest"]
    spreads.update({"Interpersonal issues – Story Spread":
                        (draw_keywords_for, subjects)})
    subjects = ["What Covers you – you and your situation",
                "What Crosses you – indicates an influence now coming into "
                "play",
                "What Crowns you – your hopes and goals",
                "What is beneath you – the issue at the root of your question",
                "What is before – an influence that will soon have impact",
                "What is behind – your history",
                "You – your feelings about your situation.\n"
                "Can clarifies what the problem really is",
                "Your House – the mood of those closest to you\n"
                "Can also be The Option – offer a plan of action instead",
                "Your Fears – illuminate your deepest concerns\n"
                "Reveals what will happen if you do nothing",
                "The Outcome – what will ultimately happen\n"
                "Or could happen if you take the Option"]
    spreads.update({"Question your whole situation – Celtic Cross":
                        (draw_keywords_for, subjects)})
    subjects = ["First step you have to take to be successful",
                "Second one",
                "Ultimate one"]
    spreads.update({"Three steps to success":
                        (draw_keywords_for, subjects)})
    return spreads
