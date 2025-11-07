import discord
from discord import app_commands
from discord.ext import commands
from psnawp_api import PSNAWP
from .psn_embed import get_custom_embed
import json
import os
import datetime  # Pour le calcul des durées et dates
import base64

# ——————— CONFIGURATION PSN ———————
NPSO_TOKEN = os.getenv("PSN_NPSSO", "Y6MCvTg1GCZG7ISqfFVEcE6wv4s4ehprACZgX2oeff6a2PoJ5lGhpSzrAHgw7bDc")
psnawp    = PSNAWP(NPSO_TOKEN)

# ——————— NOMS SPÉCIAUX POUR EMBED CUSTOM ———————
SPECIAL_NAMES = {"V", "SS_", "OL", "ms", "qcp", "bet", "L17", "ZR"}

# ——————— MAPPING DES PAYS ———————
country_map = {
    "Afghanistan":        "Afghanistan 🇦🇫",
    "Albania":            "Albanie 🇦🇱",
    "Algeria":            "Algérie 🇩🇿",
    "Andorra":            "Andorre 🇦🇩",
    "Angola":             "Angola 🇦🇴",
    "Antigua and Barbuda":"Antigua-et-Barbuda 🇦🇬",
    "Argentina":          "Argentine 🇦🇷",
    "Armenia":            "Arménie 🇦🇲",
    "Australia":          "Australie 🇦🇺",
    "Austria":            "Autriche 🇦🇹",
    "Azerbaijan":         "Azerbaïdjan 🇦🇿",
    "Bahamas":            "Bahamas 🇧🇸",
    "Bahrain":            "Bahreïn 🇧🇭",
    "Bangladesh":         "Bangladesh 🇧🇩",
    "Barbados":           "Barbade 🇧🇧",
    "Belarus":            "Biélorussie 🇧🇾",
    "Belgium":            "Belgique 🇧🇪",
    "Belize":             "Belize 🇧🇿",
    "Benin":              "Bénin 🇧🇯",
    "Bhutan":             "Bhoutan 🇧🇹",
    "Bolivia":            "Bolivie 🇧🇴",
    "Bosnia and Herzegovina":"Bosnie-Herzégovine 🇧🇦",
    "Botswana":           "Botswana 🇧🇼",
    "Brazil":             "Brésil 🇧🇷",
    "Brunei":             "Brunei 🇧🇳",
    "Bulgaria":           "Bulgarie 🇧🇬",
    "Burkina Faso":       "Burkina Faso 🇧🇫",
    "Burundi":            "Burundi 🇧🇮",
    "Cabo Verde":         "Cap-Vert 🇨🇻",
    "Cambodia":           "Cambodge 🇰🇭",
    "Cameroon":           "Cameroun 🇨🇲",
    "Canada":             "Canada 🇨🇦",
    "Central African Republic":"République centrafricaine 🇨🇫",
    "Chad":               "Tchad 🇹🇩",
    "Chile":              "Chili 🇨🇱",
    "China":              "Chine 🇨🇳",
    "Colombia":           "Colombie 🇨🇴",
    "Comoros":            "Comores 🇰🇲",
    "Congo, Republic of the":"Congo (République) 🇨🇬",
    "Congo, Democratic Republic of the":"Congo (RDC) 🇨🇩",
    "Costa Rica":         "Costa Rica 🇨🇷",
    "Côte d’Ivoire":      "Côte d’Ivoire 🇨🇮",
    "Croatia":            "Croatie 🇭🇷",
    "Cuba":               "Cuba 🇨🇺",
    "Cyprus":             "Chypre 🇨🇾",
    "Czechia":            "Tchéquie 🇨🇿",
    "Denmark":            "Danemark 🇩🇰",
    "Djibouti":           "Djibouti 🇩🇯",
    "Dominica":           "Dominique 🇩🇲",
    "Dominican Republic": "République dominicaine 🇩🇴",
    "Ecuador":            "Équateur 🇪🇨",
    "Egypt":              "Égypte 🇪🇬",
    "El Salvador":        "Salvador 🇸🇻",
    "Equatorial Guinea":  "Guinée équatoriale 🇬🇶",
    "Eritrea":            "Érythrée 🇪🇷",
    "Estonia":            "Estonie 🇪🇪",
    "Eswatini":           "Eswatini 🇸🇿",
    "Ethiopia":           "Éthiopie 🇪🇹",
    "Fiji":               "Fidji 🇫🇯",
    "Finland":            "Finlande 🇫🇮",
    "France":             "France 🇫🇷",
    "Gabon":              "Gabon 🇬🇦",
    "Gambia":             "Gambie 🇬🇲",
    "Georgia":            "Géorgie 🇬🇪",
    "Germany":            "Allemagne 🇩🇪",
    "Ghana":              "Ghana 🇬🇭",
    "Greece":             "Grèce 🇬🇷",
    "Grenada":            "Grenade 🇬🇩",
    "Guatemala":          "Guatemala 🇬🇹",
    "Guinea":             "Guinée 🇬🇳",
    "Guinea-Bissau":      "Guinée-Bissau 🇬🇼",
    "Guyana":             "Guyana 🇬🇾",
    "Haiti":              "Haïti 🇭🇹",
    "Honduras":           "Honduras 🇭🇳",
    "Hungary":            "Hongrie 🇭🇺",
    "Iceland":            "Islande 🇮🇸",
    "India":              "Inde 🇮🇳",
    "Indonesia":          "Indonésie 🇮🇩",
    "Iran":               "Iran 🇮🇷",
    "Iraq":               "Irak 🇮🇶",
    "Ireland":            "Irlande 🇮🇪",
    "Israel":             "Israël 🇮🇱",
    "Italy":              "Italie 🇮🇹",
    "Jamaica":            "Jamaïque 🇯🇲",
    "Japan":              "Japon 🇯🇵",
    "Jordan":             "Jordanie 🇯🇴",
    "Kazakhstan":         "Kazakhstan 🇰🇿",
    "Kenya":              "Kenya 🇰🇪",
    "Kiribati":           "Kiribati 🇰🇮",
    "Korea, Republic of (South Korea)": "Corée du Sud 🇰🇷",
    "Korea, Republic of":             "Corée du Sud 🇰🇷",
    "South Korea":                    "Corée du Sud 🇰🇷",
    "Republic of Korea":              "Corée du Sud 🇰🇷",
    "Hong Kong":      "Hong Kong 🇭🇰",
    "Hong Kong SAR":  "Hong Kong 🇭🇰",
    "Kosovo":             "Kosovo 🇽🇰",
    "Kuwait":             "Koweït 🇰🇼",
    "Kyrgyzstan":         "Kirghizistan 🇰🇬",
    "Laos":               "Laos 🇱🇦",
    "Latvia":             "Lettonie 🇱🇻",
    "Lebanon":            "Liban 🇱🇧",
    "Lesotho":            "Lesotho 🇱🇸",
    "Liberia":            "Libéria 🇱🇷",
    "Libya":              "Libye 🇱🇾",
    "Liechtenstein":      "Liechtenstein 🇱🇮",
    "Lithuania":          "Lituanie 🇱🇹",
    "Luxembourg":         "Luxembourg 🇱🇺",
    "Madagascar":         "Madagascar 🇲🇬",
    "Malawi":             "Malawi 🇲🇼",
    "Malaysia":           "Malaisie 🇲🇾",
    "Maldives":           "Maldives 🇲🇻",
    "Mali":               "Mali 🇲🇱",
    "Malta":              "Malte 🇲🇹",
    "Marshall Islands":   "Îles Marshall 🇲🇭",
    "Mauritania":         "Mauritanie 🇲🇷",
    "Mauritius":          "Maurice 🇲🇺",
    "Mexico":             "Mexique 🇲🇽",
    "Micronesia":         "Micronésie 🇫🇲",
    "Moldova":            "Moldavie 🇲🇩",
    "Monaco":             "Monaco 🇲🇨",
    "Mongolia":           "Mongolie 🇲🇳",
    "Montenegro":         "Monténégro 🇲🇪",
    "Morocco":            "Maroc 🇲🇦",
    "Mozambique":         "Mozambique 🇲🇿",
    "Myanmar":            "Myanmar 🇲🇲",
    "Namibia":            "Namibie 🇳🇦",
    "Nauru":              "Nauru 🇳🇷",
    "Nepal":              "Népal 🇳🇵",
    "Netherlands":        "Pays-Bas 🇳🇱",
    "New Zealand":        "Nouvelle-Zélande 🇳🇿",
    "Nicaragua":          "Nicaragua 🇳🇮",
    "Niger":              "Niger 🇳🇪",
    "Nigeria":            "Nigeria 🇳🇬",
    "North Macedonia":    "Macédoine du Nord 🇲🇰",
    "Norway":             "Norvège 🇳🇴",
    "Oman":               "Oman 🇴🇲",
    "Pakistan":           "Pakistan 🇵🇰",
    "Palau":              "Palaos 🇵🇼",
    "Panama":             "Panama 🇵🇦",
    "Papua New Guinea":   "Papouasie-Nouvelle-Guinée 🇵🇬",
    "Paraguay":           "Paraguay 🇵🇾",
    "Peru":               "Pérou 🇵🇪",
    "Philippines":        "Philippines 🇵🇭",
    "Poland":             "Pologne 🇵🇱",
    "Portugal":           "Portugal 🇵🇹",
    "Qatar":              "Qatar 🇶🇦",
    "Romania":            "Roumanie 🇷🇴",
    "Russian Federation":"Russie 🇷🇺",
    "Rwanda":             "Rwanda 🇷🇼",
    "Saint Kitts and Nevis":"Saint-Christophe-et-Niévès 🇰🇳",
    "Saint Lucia":        "Sainte-Lucie 🇱🇨",
    "Saint Vincent and the Grenadines":"Saint-Vincent-et-les-Grenadines 🇻🇨",
    "Samoa":              "Samoa 🇼🇸",
    "San Marino":         "Saint-Marin 🇸🇲",
    "São Tomé and Príncipe":"São Tomé-et-Príncipe 🇸🇹",
    "Saudi Arabia":       "Arabie saoudite 🇸🇦",
    "Senegal":            "Sénégal 🇸🇳",
    "Serbia":             "Serbie 🇷🇸",
    "Seychelles":         "Seychelles 🇸🇨",
    "Sierra Leone":       "Sierra Leone 🇸🇱",
    "Singapore":          "Singapour 🇸🇬",
    "Slovakia":           "Slovaquie 🇸🇰",
    "Slovenia":           "Slovénie 🇸🇮",
    "Solomon Islands":    "Îles Salomon 🇸🇧",
    "Somalia":            "Somalie 🇸🇴",
    "South Africa":       "Afrique du Sud 🇿🇦",
    "South Sudan":        "Soudan du Sud 🇸🇸",
    "Spain":              "Espagne 🇪🇸",
    "Sri Lanka":          "Sri Lanka 🇱🇰",
    "Sudan":              "Soudan 🇸🇩",
    "Suriname":           "Suriname 🇸🇷",
    "Sweden":             "Suède 🇸🇪",
    "Switzerland":        "Suisse 🇨🇭",
    "Syria":              "Syrie 🇸🇾",
    "Taiwan": "Taïwan 🇹🇼",
    "Taiwan, Province of China": "Taïwan 🇹🇼",
    "Taiwan Province of China": "Taïwan 🇹🇼",
    "Chinese Taipei": "Taïwan 🇹🇼",
    "TW": "Taïwan 🇹🇼",
    "zh-TW": "Taïwan 🇹🇼",
    "Tajikistan":         "Tadjikistan 🇹🇯",
    "Tanzania":           "Tanzanie 🇹🇿",
    "Thailand":           "Thaïlande 🇹🇭",
    "Timor-Leste":        "Timor oriental 🇹🇱",
    "Togo":               "Togo 🇹🇬",
    "Tonga":              "Tonga 🇹🇴",
    "Trinidad and Tobago":"Trinité-et-Tobago 🇹🇹",
    "Tunisia":            "Tunisie 🇹🇳",
    "Turkey":             "Turquie 🇹🇷",
    "Turkmenistan":       "Turkménistan 🇹🇲",
    "Tuvalu":             "Tuvalu 🇹🇻",
    "Uganda":             "Ouganda 🇺🇬",
    "Ukraine":            "Ukraine 🇺🇦",
    "United Arab Emirates":"Émirats arabes unis 🇦🇪",
    "United Kingdom":     "Royaume-Uni 🇬🇧",
    "United States":      "États-Unis 🇺🇸",
    "Uruguay":            "Uruguay 🇺🇾",
    "Uzbekistan":         "Ouzbékistan 🇺🇿",
    "Vanuatu":            "Vanuatu 🇻🇺",
    "Vatican City":       "Cité du Vatican 🇻🇦",
    "Venezuela":          "Venezuela 🇻🇪",
    "Vietnam":            "Vietnam 🇻🇳",
    "Yemen":              "Yémen 🇾🇪",
    "Zambia":             "Zambie 🇿🇲",
    "Zimbabwe":           "Zimbabwe 🇿🇼",
}

def fetch_avatar_xl(user):
    """
    Récupère l'URL de l'avatar XL : modern -> legacy -> URL par défaut.
    """
    try:
        avatars_modern = {e['size']: e['url'] for e in user.profile().get('avatars', [])}
        if 'xl' in avatars_modern:
            return avatars_modern['xl']
    except PSNAWPException:
        pass

    try:
        legacy = user.get_profile_legacy()
        avatars_legacy = {e['size']: e['avatarUrl'] for e in legacy.get('profile', {}).get('avatarUrls', [])}
        if 'xl' in avatars_legacy:
            return avatars_legacy['xl']
    except PSNAWPException:
        pass

    return 'http://static-resource.np.community.playstation.net/avatar_xl/default/Defaultavatar_xl.png'

class ProfileView(discord.ui.View):
    """Vue Discord avec boutons pour le profil PSN."""
    def __init__(self, online_id: str):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(
            label="🔗 Partager le profil PSN",
            url=f"https://profile.playstation.com/share/{online_id}",
            style=discord.ButtonStyle.link
        ))
        self.add_item(discord.ui.Button(
            label="📤 Voir le Profil PSN",
            url=f"https://profile.playstation.com/{online_id}",
            style=discord.ButtonStyle.link
        ))

class Psn(commands.Cog):
    COUNTS_FILE = "data/psn_counts.json"
    DB_FILE     = "data/psn_db.json"

    def __init__(self, bot):
        self.bot = bot
        self.counts = json.load(open(self.COUNTS_FILE, "r", encoding="utf-8")) if os.path.exists(self.COUNTS_FILE) else {}
        try:
            raw = json.load(open(self.DB_FILE, "r", encoding="utf-8"))
            self.psn_db = {k.lower(): v for k, v in raw.items()}
        except Exception:
            self.psn_db = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game("Polyvaland ! s/O 667")
        )

    def save_counts(self):
        json.dump(self.counts, open(self.COUNTS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    @app_commands.command(name="psn", description="Affiche les infos publiques d’un profil PSN ou embed custom pour certains noms")
    @app_commands.describe(pseudo="Pseudo PSN à inspecter")
    async def psn(self, interaction: discord.Interaction, pseudo: str):
        # Embed custom pour pseudos spéciaux
        if pseudo in SPECIAL_NAMES:
            embed = get_custom_embed(pseudo)
            return await interaction.response.send_message(embed=embed)

        await interaction.response.defer()
        key = pseudo.lower()
        self.counts[key] = self.counts.get(key, 0) + 1
        self.save_counts()
        check_count = self.counts[key]

        try:
            user    = psnawp.user(online_id=pseudo)
            profile = user.profile()

            # Présence, statut et plateforme
            try:
                basic = user.get_presence()["basicPresence"]
                st = basic["primaryPlatformInfo"]["onlineStatus"]
                plat = basic["primaryPlatformInfo"]["platform"]
                online_status = "En ligne" if st == "online" else "Hors ligne"
                status_str = f"{online_status} ({plat})" if st == "online" else online_status
            except Exception:
                basic = None
                status_str = "Privé"

            # Récupération des infos de base
            account_id   = user.account_id
            current_id   = user.online_id
            about_me     = profile.get("aboutMe", "").strip() or "Aucune bio"
            langs        = profile.get("languages") or profile.get("languagesUsed") or []
            langue       = langs[0].split('-')[-1].upper() if langs else "Non disponible"
            ps_plus      = "Actif" if profile.get("isPlus") else "Non actif"
            verified     = profile.get("isOfficiallyVerified", False)
            display_name = f"{current_id} <:certif:1397614299039399936>" if verified else current_id
            region       = country_map.get(user.get_region().name, "Inconnue") if user.get_region() else "Inconnue"
            avatar_url   = fetch_avatar_xl(user)
            banner_url   = f"https://image.api.playstation.com/profile/images/acct/prod/{account_id}/profile.JPEG"

            # Conversion en HEX et Chiaki
            hex_aid    = hex(int(account_id))[2:]
            aid_bytes  = int(account_id).to_bytes(8, 'big')
            chiaki_aid = base64.b64encode(aid_bytes).decode()

            # Construction de l'embed principal
            embed = discord.Embed(title="Profil PSN", color=0x0094FF)
            embed.set_thumbnail(url=avatar_url)
            embed.set_image(url=banner_url)

            if pseudo.lower() != current_id.lower():
                embed.add_field(name="Ancien PSN", value=pseudo, inline=False)
            embed.add_field(name="PSN Actuel", value=display_name, inline=False)
            embed.add_field(name="Statut", value=status_str, inline=True)
            embed.add_field(name="Account ID <:aid:1397760504457465879>", value=account_id, inline=True)
            embed.add_field(name="HEX ID", value=f"`{hex_aid}`", inline=True)
            embed.add_field(name="Chiaki ID", value=f"`{chiaki_aid}`", inline=True)
            embed.add_field(name="Pays 🌍", value=region, inline=True)
            embed.add_field(name="Langue", value=langue, inline=True)
            embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value=ps_plus, inline=True)

            # Jeu en cours
            if basic:
                games_info = basic.get("gameTitleInfoList", [])
                if games_info:
                    jeux = []
                    for g in games_info:
                        nom = g.get("titleName")
                        stat = g.get("gameStatus")
                        if nom:
                            if stat and stat != nom:
                                jeux.append(f"{nom} ({stat})")
                            else:
                                jeux.append(nom)
                    if jeux:
                        embed.add_field(name="Jeu en cours <:jeu:1397760534530625677>", value="\n".join(jeux), inline=False)

            # Trophées
            try:
                summary = user.trophy_summary()
                e = summary.earned_trophies
                lvl = summary.trophy_level
                total = e.bronze + e.silver + e.gold + e.platinum
                trop = (
                    f"<:bronze:1396977760999833684> Bronze : {e.bronze}\n"
                    f"<:argent:1396977821485629602> Argent : {e.silver}\n"
                    f"<:or:1396977699662205018> Or : {e.gold}\n"
                    f"<:platine:1396977650907615352> Platine : {e.platinum}"
                )
                embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value=trop, inline=False)
                embed.add_field(name="Niveau Trophée <:leveltrph:1397758392033869924>", value=str(lvl), inline=True)
                embed.add_field(name="Total Trophées <:trph:1397758357464416369>", value=str(total), inline=True)
                embed.add_field(name="Nombre de jeux 🎮", value=str(len(list(user.trophy_titles()))), inline=True)
            except Exception:
                embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value="Privés", inline=False)
                embed.add_field(name="Niveau Trophée <:leveltrph:1397758392033869924>", value="Privé", inline=True)
                embed.add_field(name="Total Trophées <:trph:1397758357464416369>", value="Privé", inline=True)
                embed.add_field(name="Nombre de jeux", value="Privé", inline=True)

            # Amis
            try:
                stats = user.friendship()
                count = stats.get("friendsCount", 0)
                amis_val = str(count) if count >= 0 else "Privé"
                embed.add_field(name="Amis <:amis:1397758314036596897>", value=amis_val, inline=True)
            except Exception:
                embed.add_field(name="Amis <:amis:1397758314036596897>", value="Privé", inline=True)

            # Stats de jeu
            try:
                stats_list = list(user.title_stats())
                if stats_list:
                    first_dates = [s.first_played_date_time for s in stats_list if s.first_played_date_time]
                    last_dates = [s.last_played_date_time for s in stats_list if s.last_played_date_time]
                    total_dur = sum((s.play_duration for s in stats_list if s.play_duration), datetime.timedelta())
                    if first_dates:
                        embed.add_field(name="Première partie", value=min(first_dates).strftime("%Y-%m-%d"), inline=True)
                    if last_dates:
                        embed.add_field(name="Dernière partie", value=max(last_dates).strftime("%Y-%m-%d"), inline=True)
                    hours = int(total_dur.total_seconds() // 3600)
                    minutes = int((total_dur.total_seconds() % 3600) // 60)
                    embed.add_field(name="Temps total de jeu", value=f"{hours}h{minutes}m", inline=True)
            except Exception:
                pass

            # Date de création custom
            if key in self.psn_db:
                embed.add_field(name="Date de création", value=self.psn_db[key], inline=False)

            embed.add_field(name="À propos", value=about_me, inline=False)
            embed.set_footer(text=f"Nombre de {'checks' if check_count==1 else 'checks'} : {check_count}")

            view = ProfileView(current_id)
            await interaction.followup.send(embed=embed, view=view)

        except Exception as e:
            await interaction.followup.send(f"Erreur lors de la récupération du profil : {e}")

async def setup(bot):
    await bot.add_cog(Psn(bot))


