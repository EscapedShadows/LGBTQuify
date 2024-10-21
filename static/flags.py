flags = {
    "rainbow_flag": "LGBTQ+ Community (Rainbow Flag)",
    "progress": "Progress Pride Flag",
    "philadelphia": "Philadelphia Pride Flag",
    "transgender": "Transgender",
    "nonbinary": "Non-Binary",
    "genderqueer": "Genderqueer",
    "genderfluid": "Genderfluid",
    "agender": "Agender",
    "bigender": "Bigender",
    "demiboy": "Demiboy",
    "demigirl": "Demigirl",
    "neutrois": "Neutrois",
    "intergender": "Intergender",
    "androgynous": "Androgynous",
    "polygender": "Polygender",
    "pangender": "Pangender",
    "intersex": "Intersex",
    "two_spirit": "Two-Spirit",
    "asexual": "Asexual",
    "aromantic": "Aromantic",
    "bisexual": "Bisexual",
    "pansexual": "Pansexual",
    "lesbian": "Lesbian",
    "sapphic": "Sapphic",
    "gay": "Gay",
    "omnisexual": "Omnisexual",
    "polysexual": "Polysexual",
    "skoliosexual": "Skoliosexual",
    "graysexual": "Graysexual",
    "demisexual": "Demisexual",
    "lithsexual": "Lithsexual",
    "demiromantic": "Demiromantic",
    "grayromantic": "Grayromantic",
    "lithromantic": "Lithromantic",
    "polyamorous": "Polyamorous",
    "queerplatonic": "Queerplatonic",
    "aplatonic": "Aplatonic",
    "sapiosexual": "Sapiosexual",
    "objectumsexual": "Objectumsexual",
    "fictosexual": "Fictosexual",
    "autosexual": "Autosexual",
    "autoromantic": "Autoromantic",
    "aesthetic_attraction": "Aesthetic Attraction",
    "bear": "Bear",
    "leather": "Leather",
    "puppy_play": "Puppy Play",
    "lipstick_lesbian": "Lipstick Lesbian",
    "butch_lesbian": "Butch Lesbian",
    "stone_butch": "Stone Butch",
    "soft_butch": "Soft Butch",
    "drag": "Drag",
    "kink": "Kink",
    "twink": "Twink",
    "otter": "Otter",
    "abrosexual": "Abrosexual",
    "abromantic": "Abromantic",
    "genderflux": "Genderflux",
    "aceflux": "Aceflux",
    "aroflux": "Aroflux"
}

community_flags = {"name": "Community Flags"}
gender_identity_flags = {"name": "Gender Identity Flags"}
sexual_orientation_flags = {"name": "Sexual Orientation Flags"}
romantic_orientation_flags = {"name": "Romantic Orientation Flags"}
relationship_dynamics_flags = {"name": "Relationship Dynamics & Other Attraction Flags"}
community_cultural_flags = {"name": "Community and Cultural Flags"}
fluid_spectrum_flags = {"name": "Fluid and Spectrum Flags"}

flags_dicts = {
    "community_flags": community_flags,
    "gender_identity_flags": gender_identity_flags,
    "sexual_orientation_flags": sexual_orientation_flags,
    "romantic_orientation_flags": romantic_orientation_flags,
    "relationship_dynamics_flags": relationship_dynamics_flags,
    "community_cultural_flags": community_cultural_flags,
    "fluid_spectrum_flags": fluid_spectrum_flags
}

flags_mapping = {
    "community_flags": list(flags.keys())[:3],
    "gender_identity_flags": list(flags.keys())[4:18],
    "sexual_orientation_flags": list(flags.keys())[19:31],
    "romantic_orientation_flags": list(flags.keys())[32:35],
    "relationship_dynamics_flags": list(flags.keys())[36:44],
    "community_cultural_flags": list(flags.keys())[45:55],
    "fluid_spectrum_flags": list(flags.keys())[56:60]
}

for category, keys in flags_mapping.items():
    for key in keys:
        flags_dicts[category][key] = flags[key]
