import json
p = "data/publication.json"
d = json.load(open(p))
d["sources"].append({
    "id": "fsis-thermometers",
    "title": "USDA FSIS Food Thermometers (calibration: ice-water and boiling-water methods)",
    "url": "https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/food-thermometers",
    "checked_on": "2026-11-19",
    "scope": "Re-read 19 Nov 2026 (session 787a3aab): Calibration section — ice-water method (fill a large glass with ice cubes, add drinking water, stir well, immerse the stem a minimum of 2 inches touching neither the sides nor the bottom, wait a minimum of 30 seconds, check without removing the stem; should read 32 degrees F; adjust per manufacturer instructions) and boiling-water method (at least 2 inches, at least 30 seconds, 212 degrees F at sea level, altitude caveat). Also: most thermometers give an accurate reading within 2 to 4 degrees F when placed correctly; place in the thickest part away from bone, fat or gristle; follow manufacturer instructions for insertion depth. Page last updated Mar 21, 2025.",
})
d["guides"].append({
    "slug": "thermometer-ice-water-check",
    "title": "Is your thermometer still telling the truth? The ice-water check",
    "short_title": "The 30-second ice-water check.",
    "dek": "Before you trust a reading, check the tool against ice water. USDA's method in plain steps — and what to do if it reads off.",
    "category": "Meat thermometers",
    "category_slug": "meat-thermometers",
    "type": "The accuracy check",
    "art": "thermometer",
    "published": "2026-11-19",
    "products": ["SHOP-04", "SHOP-05"],
    "takeaway": "A thermometer is only as useful as its last check. Ice water should read 32°F; if yours does not, follow the manufacturer's instructions to adjust it — or replace it — before you cook to a number.",
    "sections": [
        {
            "heading": "Why check the tool before you trust the reading.",
            "paragraphs": [
                "USDA's Food Safety and Inspection Service puts it plainly: most food thermometers will give an accurate reading within 2 to 4 degrees F — but only if the thermometer is placed in the proper location of the food. Calibration, in FSIS's words, is the process of checking the accuracy of a food thermometer. It is a check on the tool, done before the tool is asked to judge the food.",
                "That order matters. A probe in the thickest part of the food, away from bone, fat or gristle, still reports through a sensing device that can drift. The ice-water check tests the device against a known reference — melting ice and water — instead of asking you to trust the display because it looks precise.",
            ],
            "source_ids": ["fsis-thermometers"],
        },
        {
            "heading": "The ice-water check, step by step.",
            "paragraphs": [
                "FSIS calls the ice-water method best for most thermometers. Fill a large glass with ice cubes, add drinking water and stir well. Immerse the thermometer stem a minimum of 2 inches into the mixture, touching neither the sides nor the bottom of the glass. Wait a minimum of 30 seconds and check the reading without removing the stem from the water. It should read 32 degrees F; if it does, the thermometer is calibrated.",
            ],
            "checklist": [
                "Ice cubes plus drinking water in a large glass, stirred well.",
                "Stem at least 2 inches in — touching neither side nor bottom.",
                "Wait at least 30 seconds; read without removing the stem.",
                "Should read 32°F. If not, adjust according to the manufacturer's instructions (some thermometers have a calibration nut or dial).",
                "If the thermometer does not allow manual calibration, FSIS's boiling-water guidance says you may need to replace it.",
            ],
            "source_ids": ["fsis-thermometers"],
        },
        {
            "heading": "What the check does not tell you.",
            "paragraphs": [
                "The ice-water check verifies the tool at one reference point. It does not verify where a probe should go in a whole bird, how a wireless probe reports across a long roast, or whether any figure in a listing title — a response time, a tolerance, a certification mention — was measured the way you would measure it. Those stay open questions, listed below, until the exact model's own instructions are in front of you.",
                "It also does not replace the temperature target. When the tool passes its check, the number you cook toward still comes from the published safe-minimum chart for that food — poultry 165°F, ground meat 160°F, steaks and roasts 145°F with a 3-minute rest — not from a feature list. Check the tool, then check the food against the chart.",
            ],
            "source_ids": ["SHOP-04", "SHOP-05", "food-safety", "fsis-thermometers"],
        },
    ],
    "unknowns": [
        "Whether either listed thermometer model can be calibrated, and how — that is in each model's own instructions, not verified here.",
        "The insertion depth each listed model's instructions require for an accurate reading.",
        "The accuracy of either listed thermometer — no accuracy measurement is held on this site.",
    ],
    "related": ["where-does-the-probe-go", "thermometer-numbers-on-the-label", "instant-read-or-wireless-thermometer"],
})
d["indexable_pages"].append("guides/thermometer-ice-water-check.html")
open(p, "w").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
print("guides:", len(d["guides"]), "sources:", len(d["sources"]), "indexable:", len(d["indexable_pages"]))
