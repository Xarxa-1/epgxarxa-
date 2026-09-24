import gzip
import urllib.request
import xml.etree.ElementTree as ET

# Font oficial de l'EPG en XML de TDTChannels
URL_XML_GZ = "https://www.tdtchannels.com/epg/TV.xml.gz"

# IDs dels canals que volem filtrar
TARGET_CHANNELS = {
    "Xarxa_TAC12.TV",
    "Xarxa_LleidaTV.TV",
    "Xarxa_Canal_Reus_TV.TV",
    "Xarxa_Penedes_TV.TV",
    "Xarxa_TV_Costa_Brava.TV",
    "BTV.TV"
}

def main():
    req = urllib.request.Request(
        URL_XML_GZ,
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    print("Descarregant i descomprimint l'EPG XML...")
    with urllib.request.urlopen(req) as response:
        with gzip.GzipFile(fileobj=response) as gz:
            tree = ET.parse(gz)

    root = tree.getroot()

    # Eliminem els canals que no pertanyen a la nostra selecció
    for channel in root.findall('channel'):
        channel_id = channel.get('id')
        if channel_id not in TARGET_CHANNELS:
            root.remove(channel)

    # Eliminem els programes de la parrilla que no siguin dels nostres canals
    for programme in root.findall('programme'):
        channel_id = programme.get('channel')
        if channel_id not in TARGET_CHANNELS:
            root.remove(programme)

    # Desem el resultat en un nou fitxer XML
    print("Guardant epg.xml filtrat...")
    tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    main()
