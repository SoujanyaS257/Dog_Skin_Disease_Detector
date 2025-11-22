"""
remedies.py
Contains the knowledge base for dog skin diseases, including:
- Home Remedies
- Over-the-Counter (OTC) Medicines
- Dietary Suggestions
"""

# We store the data directly here to avoid JSON file loading errors
REMEDIES_DB = {
    "dermatitis": {
        "title": "🔥 Dermatitis (General Skin Inflammation)",
        "description": "Inflammation of the skin, often caused by allergies, fleas, or contact irritants.",
        "remedies": [
            "Apply a cold compress to soothe red, inflamed areas.",
            "Bathe your dog with an Oatmeal-based shampoo (soothing).",
            "Use a cone (E-collar) to prevent licking and further irritation.",
            "Wash all dog bedding in hot water to remove allergens."
        ],
        "medicines": [
            "**Topical Spray:** Hydrocortisone spray (for itching).",
            "**Shampoo:** Chlorhexidine gluconate shampoo (cleans infection).",
            "**Supplements:** Benadryl (Diphenhydramine) - *Consult vet for dosage (usually 1mg per lb)*."
        ],
        "diet": [
            "**Hypoallergenic Diet:** Switch to a 'novel protein' like Rabbit, Duck, or Salmon.",
            "**Avoid:** Chicken, Beef, and Wheat (common allergens).",
            "**Add:** Omega-3 Fish Oil supplements to reduce inflammation."
        ],
        "disclaimer": "Dermatitis has many causes. If skin does not improve in 48 hours, see a vet."
    },

    "fungal_infection": {
        "title": "🍄 Fungal Infection (Yeast/Malassezia)",
        "description": "Caused by an overgrowth of yeast, usually in ears, paws, or skin folds.",
        "remedies": [
            "Keep skin folds and paws completely dry.",
            "Rinse affected areas with a 50/50 mix of Apple Cider Vinegar and Water.",
            "Use an antifungal wet wipe on paws after walks."
        ],
        "medicines": [
            "**Shampoo:** Ketoconazole or Miconazole shampoo (Antifungal).",
            "**Topical:** Clotrimazole cream (often sold for athlete's foot - safe for dogs in small amounts).",
            "**Ear Cleaner:** Zymox Enzymatic Ear Solution (if ears are affected)."
        ],
        "diet": [
            "**Low Sugar/Carb Diet:** Yeast feeds on sugar. Avoid grain-heavy kibble.",
            "**Probiotics:** Add dog-specific probiotics to balance gut health.",
            "**Add:** Coconut oil (has natural antifungal properties) in small amounts."
        ],
        "disclaimer": "Yeast infections often smell 'musty'. Persistent infections indicate an underlying allergy."
    },

    "ringworm": {
        "title": "⭕ Ringworm (Dermatophytosis)",
        "description": "A contagious fungal infection (not a worm) causing circular bald patches.",
        "remedies": [
            "**Isolate the dog:** This is contagious to humans and other pets.",
            "Disinfect the home with diluted bleach (1:10 ratio) on hard surfaces.",
            "Wear gloves when touching the affected area."
        ],
        "medicines": [
            "**Topical:** Miconazole cream or spray applied twice daily.",
            "**Bath:** Lime Sulfur Dip (smells like rotten eggs but is highly effective).",
            "**Spray:** Chlorhexidine antifungal spray."
        ],
        "diet": [
            "**High Quality Protein:** Helps repair skin and hair faster.",
            "**Vitamin E:** Supports skin healing.",
            "**Zinc:** Essential for healthy fur regrowth."
        ],
        "disclaimer": "If lesions spread or you develop red rings on your skin, see a doctor immediately."
    },

    "demodicosis": {
        "title": "🕷️ Demodicosis (Demodectic Mange)",
        "description": "Caused by mites living in hair follicles. Often seen in puppies or dogs with weak immune systems.",
        "remedies": [
            "Reduce stress for the dog (stress lowers immunity, allowing mites to thrive).",
            "Wash bedding daily.",
            "Ensure the dog is up to date on deworming."
        ],
        "medicines": [
            "**Shampoo:** Benzoyl Peroxide shampoo (flushes out follicles).",
            "**Spot-on Treatment:** Bravecto or NexGard (Require Vet Prescription) are the *best* cure.",
            "**Topical:** Goodwinol ointment (for small spots)."
        ],
        "diet": [
            "**Immune Boost:** Add antioxidants (blueberries, spinach) to food.",
            "**Omega-3s:** Fish oil is critical for skin barrier repair.",
            "**Raw/Fresh Food:** Can help boost natural immunity compared to processed kibble."
        ],
        "disclaimer": "Demodex is an immune issue. Never use motor oil (old myth)! It is toxic."
    },

    "hypersensitive": {
        "title": "🤧 Hypersensitivity (Allergic Reaction)",
        "description": "An acute reaction to food, insect bites, or pollen.",
        "remedies": [
            "Wipe paws and body with a damp cloth after going outside (removes pollen).",
            "Use a cool water bath (no soap) to soothe itching.",
            "Check for fleas—one bite can cause a massive reaction."
        ],
        "medicines": [
            "**Antihistamine:** Benadryl (Diphenhydramine) - *Ask vet for dose*.",
            "**Spray:** Vetericyn anti-itch spray.",
            "**Shampoo:** Hypoallergenic or Aloe Vera shampoo."
        ],
        "diet": [
            "**Elimination Diet:** Feed only one protein source (e.g., Lamb) for 8 weeks.",
            "**Avoid:** Artificial colors and preservatives in treats.",
            "**Hydration:** Ensure plenty of fresh water."
        ],
        "disclaimer": "If facial swelling occurs or breathing is difficult, this is an emergency. Go to a vet."
    },

    "healthy": {
        "title": "✅ Healthy Skin",
        "description": "No obvious disease detected.",
        "remedies": ["Continue regular grooming and brushing.", "Maintain current hygiene routine."],
        "medicines": ["Monthly flea/tick prevention is recommended."],
        "diet": ["Maintain a balanced diet appropriate for the dog's age/breed."],
        "disclaimer": "Regular checkups are still important!"
    },
    
    "default": {
        "title": "❓ Unidentified Condition",
        "description": "The model is unsure. It looks like a skin issue, but specific classification is low confidence.",
        "remedies": ["Keep the area clean and dry.", "Prevent licking with a cone.", "Monitor for spreading."],
        "medicines": ["Consult a vet before applying medication."],
        "diet": ["Ensure fresh water and balanced food."],
        "disclaimer": "Please visit a veterinarian for a proper diagnosis."
    }
}

def get_remedy(disease_name):
    """
    Returns the remedy information for a given disease name.
    """
    # Normalize key: remove underscores, make lowercase
    # e.g. "Fungal_Infection" -> "fungal_infection"
    key = disease_name.lower().replace(" ", "_")
    
    # Fuzzy matching for common terms
    if "fungal" in key: key = "fungal_infection"
    if "mange" in key: key = "demodicosis"
    if "allergy" in key or "hypersens" in key: key = "hypersensitive"
    if "dermatitis" in key: key = "dermatitis"
    if "ringworm" in key: key = "ringworm"
    
    # Return specific remedy or default if not found
    return REMEDIES_DB.get(key, REMEDIES_DB['default'])