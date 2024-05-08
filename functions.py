

voices_list = [
    "1. English US - Female",
    "2. English US - Male 1",
    "3. English US - Male 2",
    "4. English US - Male 3",
    "5. English US - Male 4",
    "6. English UK - Male 1",
    "7. English UK - Male 2",
    "8. English AU - Female",
    "9. English AU - Male",
    "10. French - Male 1",
    "11. French - Male 2",
    "12. German - Female",
    "13. German - Male",
    "14. Spanish - Male",
    "15. Spanish MX - Male 1",
    "16. Spanish MX - Male 2",
    "17. Spanish MX - Female 1",
    "18. Spanish MX - Female 2",
    "19. Spanish MX - Female 3",
    "20. Spanish MX - Optimus Prime (Transformers)",
    "21. Portuguese BR - Female 2",
    "22. Portuguese BR - Female 3",
    "23. Portuguese BR - Male",
    "24. Indonesian - Female",
    "25. Japanese - Female 1",
    "26. Japanese - Female 2",
    "27. Japanese - Female 3",
    "28. Japanese - Male",
    "29. Korean - Male 1",
    "30. Korean - Male 2",
    "31. Korean - Female",
    "32. Characters - Ghostface (Scream)",
    "33. Characters - Chewbacca (Star Wars)",
    "34. Characters - C3PO (Star Wars)",
    "35. Characters - Stitch (Lilo & Stitch)",
    "36. Characters - Stormtrooper (Star Wars)",
    "37. Characters - Rocket (Guardians of the Galaxy)",
    "38. Singing - Alto",
    "39. Singing - Tenor",
    "40. Singing - Sunshine Soon",
    "41. Singing - Warmy Breeze",
    "42. Singing - Glorious",
    "43. Singing - It Goes Up",
    "44. Singing - Chipmunk",
    "45. Singing - Dramatic"
]

voices_map = {
    str(i + 1): voice_id for i, voice_id in enumerate([
        "en_us_001", "en_us_006", "en_us_007", "en_us_009", "en_us_010",
        "en_uk_001", "en_uk_003", "en_au_001", "en_au_002", "fr_001",
        "fr_002", "de_001", "de_002", "es_002", "es_mx_002", "es_male_m3",
        "es_female_f6", "es_female_fp1", "es_mx_female_supermom",
        "es_mx_male_transformer", "br_003", "br_004", "br_005", "id_001",
        "jp_001", "jp_003", "jp_005", "jp_006", "kr_002", "kr_004", "kr_003",
        "en_us_ghostface", "en_us_chewbacca", "en_us_c3po", "en_us_stitch",
        "en_us_stormtrooper", "en_us_rocket", "en_female_f08_salut_damour",
        "en_male_m03_lobby", "en_male_m03_sunshine_soon",
        "en_female_f08_warmy_breeze", "en_female_ht_f08_glorious",
        "en_male_sing_funny_it_goes_up", "en_male_m2_xhxs_m03_silly",
        "en_female_ht_f08_wonderful_world"
    ])
}

def check_service_availability():
    try:
        response = requests.get(f"{ENDPOINT}/api/status")
        data = response.json()
        return response.status_code == 200 and data.get('data') and data['data'].get('available')
    except requests.exceptions.RequestException as e:
        print(f"Error querying API status: {e}")
        return False

def generate_audio(text, voice):
    try:
        response = requests.post(f"{ENDPOINT}/api/generation", json={"text": text, "voice": voice})
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                # Decode base64-encoded audio data
                return base64.b64decode(data['data'])
            else:
                print(f"Generation failed: {data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"Failed to generate audio: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error generating audio: {e}")
        return None
