import json
import urllib.request

# URL original de TDTChannels
URL_EPG = "https://www.tdtchannels.com/epg/TV.json"

# Canals que volem filtrar
TARGET_CHANNELS = {
    "Xarxa_TAC12.TV",
    "Xarxa_LleidaTV.TV",
    "Xarxa_Canal_Reus_TV.TV"
}

def main():
    req = urllib.request.Request(
        URL_EPG, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    # Suposant que l'estructura del JSON té una llista de canals
    filtered_channels = []
    
    # Si l'estructura és un directori/dict o llista
    if isinstance(data, list):
        filtered_channels = [c for c in data if c.get('id') in TARGET_CHANNELS or c.get('name') in TARGET_CHANNELS]
    elif isinstance(data, dict):
        for key, val in data.items():
            if key in TARGET_CHANNELS:
                filtered_channels.append(val)

    # Desa el resultat filtrat
    with open("epg.json", "w", encoding="utf-8") as f:
        json.dump(filtered_channels, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
