"""Interface text."""

STRINGS = {
    "en": {
        "html_lang": "en-US",
        "contents": "Contents",
        "download_pdf": "Download the PDF",
        "edit_section": "Suggest an edit to this section on GitHub",
        "repo": "The primer on GitHub",
        "light_mode": "Light mode",
        "dark_mode": "Dark mode",
        "switch_theme": "Switch color theme",
        "show_sections": "Show sections of",
        "link_to_section": "Link to this section",
        "view_on_scryfall": "View on Scryfall",
        "close": "Close",
        "hero_caption": "Phyrexian Dreadnought, art by {artist}",
        "show_answer": "Show the answer",
        "license": "Text © 2026 Mario Longobardi, licensed under {cc}: share and adapt it freely, with credit. The license covers the primer's own writing, not the card images or card text.",
        "credit": "Card images from {scryfall}. Magic: The Gathering card names, text and images are © Wizards of the Coast. This primer is unofficial Fan Content permitted under the Fan Content Policy, not approved or endorsed by Wizards.",
        "main_deck": "Main deck",
        "sideboard": "Sideboard",
        "out": "Out",
        "in": "In",
        "map_headers": ("Matchup", "Out", "In"),
        "banner": "Confidential — for your eyes only. A preview draft of the primer: please don't share or distribute it.",
        "banner_print": "Confidential preview — for your eyes only",
    },
}


def strings(lang: str = "en") -> dict:
    return STRINGS[lang]
