# --- THE PLANET-SPECIFIC NAKSHATRA ENGINE ---
def get_holistic_medicine(planet_name, sign, nakshatra_name):
    """
    Retrieves the specific 'Medicine' based on the Planet + Nakshatra combination.
    This ensures Mars in Ashwini feels different than Sun in Ashwini.
    """
    
    # --- MARS DATASET ---
    mars_medicine = {
        "Ashwini": {
            "astrology": "The 'Swift Lightning.' Mars here is impulsive and moves faster than the mind. It creates 'head-heat' and sudden bursts of energy.",
            "yoga": "Savasana with an Eye Pillow — To force the 'Internal Charioteer' to stop and rest the eyes.",
            "ayurveda": "Cranial Pressure. Use Brahmi oil on the scalp to prevent 'Mars-brain' (migraines/irritability)."
        },
        "Bharani": {
            "astrology": "The 'Volcano in the Vessel.' Mars here is under extreme pressure to transform. It represents the 'Fire of Birth' and deep survival.",
            "yoga": "Baddha Konasana (Bound Angle) — To release the deep 'Apana' (downward) energy stored in the pelvic floor.",
            "ayurveda": "Pelvic Inflammation. Cool the 'Yoni/Linga' energy. Drink Aloe Vera juice to soothe internal heat."
        },
        "Krittika": {
            "astrology": "The 'Commander’s Blade.' This is the sharpest Mars. It provides the power to 'cut' through obstacles but can become critical.",
            "yoga": "Utkatasana (Chair Pose) — To channel the fire into the thighs and stabilize the 'Agnihotra'.",
            "ayurveda": "Blood Purifier. Mars here 'boils' the blood. Use Neem or Turmeric to clear toxins (Ama)."
        },
        # ... (You would continue adding the rest of your Mars descriptions here)
    }

    # --- DEFAULT/GENERIC DATASET (For other planets until you provide them) ---
    generic_medicine = {
        "Ashwini": {"astrology": "The Healer's Star.", "yoga": "Warrior III", "ayurveda": "Brahmi Oil"},
        # ...
    }

    # Selection Logic
    if planet_name == "Mars":
        return mars_medicine.get(nakshatra_name, generic_medicine.get(nakshatra_name))
    else:
        return generic_medicine.get(nakshatra_name, {"astrology": "Wisdom ripening...", "yoga": "N/A", "ayurveda": "N/A"})

# --- UPDATED DATA RETRIEVAL IN THE APP ---
# When the app loops through the planets, it now calls this:
# medicine = get_holistic_medicine(p['name'], p['sign'], p['nakshatra'])
