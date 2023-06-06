import os

import re

import asyncio

import random

import string

from datetime import datetime

import aiohttp

import requests

import secrets

import emoji

from telethon import TelegramClient, events, types, functions

from telethon.tl.types import InputMediaPhoto

import requests

# Ingresar tus credenciales de API de Telegram

api_id = TU API ID

api_hash = 'TUAPIHASH'

phone_number = 'TUNUMERO'

# Crear una instancia de TelegramClient

client = TelegramClient('TUUSERNAME', api_id, api_hash)

used_extras = []

used_identifiers = []

def get_card_category(bin):

    if bin.startswith('4'):

        return 'VISA'

    elif bin.startswith(('51', '52', '53', '54', '55')):

        return 'MASTERCARD'

    elif bin.startswith(('34', '37')):

        return 'AMEX'

    elif bin.startswith('6'):

        return 'DISCOVERY'

    else:

        return 'UNKNOWN'

async def extract_live_cc(message):

    if message and message.text:

        ccn_types = ['𝑨𝑷𝑷𝑹𝑶𝑽𝑬𝑫', 'Approved']  # Agrega aquí los tipos de texto adicionales que deseas extraer

        cc_matches = []  # Lista para almacenar las tarjetas de crédito encontradas

        for ccn_type in ccn_types:

            if len(cc_matches) >= 3:

                break  # Si se encuentran 3 tarjetas de crédito, se detiene la búsqueda

            if ccn_type in message.text:

                cc_matches.extend(re.findall(r'\d{16}\|\d{2,4}\|\d{2,4}\|\d{3}', message.text))

        for cc_match in cc_matches:

            cc = cc_match

            year_match = re.search(r'\|(\d{4})\|', cc)

            month_match = re.search(r'\|(\d{2})\|', cc)

            if year_match and month_match:

                try:

                    expiry_date = datetime.strptime(f'{year_match.group(1)}-{month_match.group(1)}-01', '%Y-%m-%d')

                    formatted_expiry_date = expiry_date.strftime('%m|%Y')

                    cvv = 'rnd'

                    bin = cc[:6]

                    extra = f'<code>{cc[:12]}xxxx|{formatted_expiry_date}|{cvv}</code>'

                    if extra in used_extras:

                        # Establece una condición de salida para evitar la recursión infinita

                        return

                    used_extras.append(extra)

                    bank, country, country_code, card_type, card_brand, category = await get_cc_info(bin)

                    country_flag = COUNTRY_EMOJIS.get(country_code, '')

                    card_category = get_card_category(bin)

                    info = f'{card_category} - {card_type} - {category}'

                    cc_message = f'╔═════════════════════════╗\n' \

                                 f'║   { "𝗞𝗔𝗚𝗨𝗬𝗔".center(25, " ") }𝗦𝗖𝗥𝗔𝗣𝗣𝗘𝗥\n' \

                                 f'╠═════════════════════════╣\n' \

                                 f'║ ♚ 𝗕𝗜𝗡 ➤ <code>{bin}</code>\n' \

                                 f'║ ♚ 𝗘𝗫𝗧𝗥𝗔 ➤ {extra}\n' \

                                 f'║ ♚ 𝗖𝗖 ➤ <code>{cc}</code> \n' \

                                 f'╠═════════════════════════╣\n' \

                                 f'║ ♚ 𝗕𝗔𝗡𝗞 ➤ <code>{bank}</code>\n' \

                                 f'║ ♚ 𝗖𝗢𝗨𝗡𝗧𝗥𝗬 ➤ <code>{country} {country_flag}</code>\n' \

                                 f'║ ♚ 𝗜𝗡𝗙𝗢 ➤ <code>{info}</code>\n' \

                                 f'╠═════════════════════════╣\n' \

                                 f'║ 𝗦𝗖𝗥𝗔𝗣𝗣𝗘𝗥 𝗕𝗬 ➤ <a href="https://t.me/L230309">Yamada</a>\n' \

                                 f'╚═════════════════════════╝'

                    target_chat = 'CANALDONDELLEGARAN'

                    gif_path = 'AQUIELGIFQUETENGAENTUPC'  # Reemplaza con la ruta real del archivo GIF

                    gif = await client.upload_file(gif_path)

                    await client.send_message(target_chat, cc_message, file=gif, parse_mode='HTML')

                    await asyncio.sleep(80)  # Espera de 80 segundos

                except Exception as e:

                    print(f'Error: {e}')

                    return

async def get_cc_info(bin):

    url = f"https://binlist.io/lookup/{bin}"

    headers = {"Accept-Version": "3"}

    async with aiohttp.ClientSession() as session:

        async with session.get(url, headers=headers) as resp:

            data = await resp.json()

            bank = data.get("bank", {}).get("name", "")

            country = data.get("country", {}).get("name", "")

            scheme = data.get("scheme", "")

            card_type = data.get("type", "")

            card_brand = data.get("brand", "")

            category = data.get("category", "")  # Nivel de la tarjeta

            

            print("Category:", category)

            

            country_code = data.get("country", {}).get("alpha2", "")

            return bank, country, country_code, card_type, card_brand, category

COUNTRY_EMOJIS = {

    'AR': '🇦🇷',

    'BO': '🇧🇴',

    'BR': '🇧🇷',

    'CL': '🇨🇱',

    'CO': '🇨🇴',

    'CR': '🇨🇷',

    'CU': '🇨🇺',

    'DO': '🇩🇴',

    'EC': '🇪🇨',

    'GT': '🇬🇹',

    'HN': '🇭🇳',

    'MX': '🇲🇽',

    'NI': '🇳🇮',

    'PA': '🇵🇦',

    'PY': '🇵🇾',

    'PE': '🇵🇪',

    'PR': '🇵🇷',

    'UY': '🇺🇾',

    'VE': '🇻🇪',

    'US': '🇺🇸',

    'MX': '🇲🇽',

    'CA': '🇨🇦',

    'AU': '🇦🇺',

    'AL': '🇦🇱',

    'AD': '🇦🇩',

    'AT': '🇦🇹',

    'BY': '🇧🇾',

    'BE': '🇧🇪',

    'BA': '🇧🇦',

    'BG': '🇧🇬',

    'HR': '🇭🇷',

    'CY': '🇨🇾',

    'CZ': '🇨🇿',

    'DK': '🇩🇰',

    'EE': '🇪🇪',

    'FI': '🇫🇮',

    'FR': '🇫🇷',

    'DE': '🇩🇪',

    'GR': '🇬🇷',

    'HU': '🇭🇺',

    'IS': '🇮🇸',

    'IE': '🇮🇪',

    'IT': '🇮🇹',

    'CN': '🇨🇳',

    'SV': '🇸🇻',

    'VN': '🇻🇳',

    'KZ': '🇰🇿',

    'XK': '🇽🇰',

    'LV': '🇱🇻',

    'LI': '🇱🇮',

    'LT': '🇱🇹',

    'LU': '🇱🇺',

    'MK': '🇲🇰',

    'MT': '🇲🇹',

    'MD': '🇲🇩',

    'MC': '🇲🇨',

    'ME': '🇲🇪',

    'NL': '🇳🇱',

    'NO': '🇳🇴',

    'PL': '🇵🇱',

    'PT': '🇵🇹',

    'RO': '🇷🇴',

    'RU': '🇷🇺',

    'SM': '🇸🇲',

    'RS': '🇷🇸',

    'SK': '🇸🇰',

    'SI': '🇸🇮',

    'ES': '🇪🇸',

    'SE': '🇸🇪',

    'CH': '🇨🇭',

    'UA': '🇺🇦',

    'GB': '🇬🇧',

    'VA': '🇻🇦',

    'IL': '🇮🇱',

    'IN': '🇮🇳',

    'ID': '🇮🇩',

    'MY': '🇲🇾',

    'JP': '🇯🇵',

    'TW': '🇹🇼',

    'ZA': '🇿🇦',

    'TZ': '🇹🇿',

    'SA': '🇸🇦',

    'PH': '🇵🇭',

    'OM': '🇴🇲',

    'EG': '🇪🇬',

    'TR': '🇹🇷',

    'HK': '🇭🇰',

    'KY': '🇰🇾',

    'BS': '🇧🇸',

    'BH': '🇧🇭',

    'KE': '🇰🇪',

    'AG': '🇦🇬',

    'AI': '🇦🇮',

    'AO': '🇦🇴',

    'AW': '🇦🇼',

    'BF': '🇧🇫',

    'BI': '🇧🇮',

    'BJ': '🇧🇯',

    'PK': '🇵🇰',

    'BZ': '🇧🇿',

    'CD': '🇨🇩',

    'CF': '🇨🇫',

    'CG': '🇨🇬',

    'CI': '🇨🇮',

    'DJ': '🇩🇯',

    'DM': '🇩🇲',

    'GQ': '🇬🇶',

    'ER': '🇪🇷',

    'FJ': '🇫🇯',

    'GA': '🇬🇦',

    'GD': '🇬🇩',

    'GM': '🇬🇲',

    'GN': '🇬🇳',

    'GW': '🇬🇼',

    'GY': '🇬🇾',

    'HT': '🇭🇹',

    'JM': '🇯🇲',

    'KI': '🇰🇮',

    'KM': '🇰🇲',

    'KN': '🇰🇳',

    'KP': '🇰🇵',

    'KW': '🇰🇼',

    'LA': '🇱🇦',

    'LB': '🇱🇧',

    'LC': '🇱🇨',

    'LR': '🇱🇷',

    'LS': '🇱🇸',

    'LY': '🇱🇾',

    'MG': '🇲🇬',

    'MW': '🇲🇼',

    'ML': '🇲🇱',

    'MR': '🇲🇷',

    'MU': '🇲🇺',

    'MV': '🇲🇻',

    'MW': '🇲🇼',

    'MZ': '🇲🇿',

    'NA': '🇳🇦',

    'NE': '🇳🇪',

    'NG': '🇳🇬',

    'NR': '🇳🇷',

    'NU': '🇳🇺',

    'PG': '🇵🇬',

    'RW': '🇷🇼',

    'SB': '🇸🇧',

    'SC': '🇸🇨',

    'SL': '🇸🇱',

    'SN': '🇸🇳',

    'SO': '🇸🇴',

    'SR': '🇸🇷',

    'SS': '🇸🇸',

    'ST': '🇸🇹',

    'SY': '🇸🇾',

    'TD': '🇹🇩',

    'NZ': '🇳🇿',

    'AF': '🇦🇫', 

    'AO': '🇦🇴', 

    'AM': '🇦🇲', 

    'AZ': '🇦🇿', 

    'BD': '🇧🇩', 

    'BT': '🇧🇹', 

    'KH': '🇰🇭', 

    'CM': '🇨🇲', 

    'CV': '🇨🇻', 

    'CI': '🇨🇮', 

    'DJ': '🇩🇯', 

    'GQ': '🇬🇶', 

    'ER': '🇪🇷', 

    'ET': '🇪🇹', 

    'FJ': '🇫🇯', 

    'GM': '🇬🇲', 

    'GE': '🇬🇪', 

    'GN': '🇬🇳', 

    'GW': '🇬🇼', 

    'HT': '🇭🇹', 

    'IR': '🇮🇷', 

    'IQ': '🇮🇶', 

    'JM': '🇯🇲', 

    'JO': '🇯🇴', 

    'KG': '🇰🇬', 

    'KI': '🇰🇮', 

    'KP': '🇰🇵', 

    'KW': '🇰🇼', 

    'LA': '🇱🇦', 

    'LB': '🇱🇧', 

    'LS': '🇱🇸', 

    'LR': '🇱🇷', 

    'LY': '🇱🇾', 

    'MG': '🇲🇬', 

    'MW': '🇲🇼', 

    'MV': '🇲🇻', 

    'ML': '🇲🇱', 

    'MR': '🇲🇷', 

    'MU': '🇲🇺', 

    'FM': '🇫🇲', 

    'MD': '🇲🇩', 

    'MN': '🇲🇳', 

    'ME': '🇲🇪', 

    'MA': '🇲🇦', 

    'MZ': '🇲🇿', 

    'MM': '🇲🇲', 

    'SG': '🇸🇬',

    'TH': '🇹🇭',

    'AE': '🇦🇪'

}

import asyncio

async def scrape_live_cc(chat):

    try:

        entity = await client.get_entity(chat)

        if entity.username:

            print(f'Scraping LIVE CCs from @{entity.username}...')

        else:

            print(f'Scraping LIVE CCs from {entity.title}...')

    except ValueError:

        print(f'Invalid chat: {chat}')

        return

    except Exception as e:

        print(f'Error: {e}')

        return

    async for message in client.iter_messages(entity):

        await extract_live_cc(message)

async def main():

    await client.start()

    source_chats = ['https://t.me/OficialScorpionsGrupo', 'https://t.me/alterchkchat', 'https://t.me/+rl8ChsLqzBdkNTYx']

    for chat in source_chats:

        await scrape_live_cc(chat)

        # Cambiar al siguiente enlace después de completar el scraping del chat actual

        await asyncio.sleep(75)

    # cierra la sesión de TelegramClient

    await client.disconnect()

asyncio.run(main())
