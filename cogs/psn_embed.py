import discord


def get_custom_embed(name: str) -> discord.Embed:
    """
    Retourne un Embed personnalisé pour certains pseudos spéciaux,
    en suivant le style général des embeds PSN (thumbnail, image, champs, footer).
    """
    # Cartes de style
    color_map = {
        "V": 0x0094FF,
        "ZR": 0x0094FF,
        "OL": 0x0094FF,
        "ms": 0x0094FF,
        "qcp": 0x0094FF,
        "bet": 0x0094FF,
        "L17": 0x0094FF,
        "SS_": 0x0094FF,
    }

    title_map = {
        "V": "Profile PSN",
        "OL": "Profile PSN",
        "ZR": "Profile PSN",
        "ms": "Profile PSN",
        "qcp": "Profile PSN",
        "bet": "Profile PSN",
        "L17": "Profile PSN",
        "SS_": "Profile PSN",
    }

    desc_map = {
        "V": "PSN :\n V",
        "OL": "PSN :\n OL",
        "ZR": "PSN :\n ZR",
        "ms": "PSN :\n ms",
        "qcp": "PSN :\n qcp",
        "bet": "PSN :\n bet",
        "L17": "PSN :\n L17",
        "SS_": "PSN :\n SS_",
    }


    # Création de l'embed
    embed = discord.Embed(
        title=title_map.get(name, f"Profil {name}"),
        description=desc_map.get(name, "Profil personnalisé."),
        color=color_map.get(name, 0x2ECC71)
    )
    # Thumbnail et bannière pour respecter le style
    # Champs spécifiques
    if name == "V":
        embed.add_field(name="Status", value="Privé", inline=True)
        embed.add_field(name="Account ID <:aid:1397760504457465879>", value="-", inline=True)
        embed.add_field(name="Pays 🌍", value="Russie 🇷🇺", inline=True)
        embed.add_field(name="Langue", value="RU", inline=True)
        embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value="Non Actif", inline=True)
        embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value="Privé", inline=True)
        embed.add_field(name="Niveau de Trophées <:leveltrph:1397758392033869924>", value="Privé", inline=True)
        embed.add_field(name="Total de Trophées <:trph:1397758357464416369>", value="Privé", inline=True)
        embed.add_field(name="Nombre de jeux", value="Privé", inline=True)
        embed.add_field(name="Amis <:amis:1397758314036596897>", value="Privé", inline=True)
        embed.add_field(name="Date de création", value="2017", inline=True)
        embed.set_image(url="https://image.api.playstation.com/profile/images/acct/prod/1872489449964855051/profile.JPEG")
    elif name == "OL":
        embed.add_field(name="Status", value="Privé", inline=True)
        embed.add_field(name="Account ID <:aid:1397760504457465879>", value="-", inline=True)
        embed.add_field(name="Pays 🌍", value="Corée du sud", inline=True)
        embed.add_field(name="Langue", value="KR", inline=True)
        embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value="Non Actif", inline=True)
        embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value="Privé", inline=True)
        embed.add_field(name="Niveau de Trophées <:leveltrph:1397758392033869924>", value="Privé", inline=True)
        embed.add_field(name="Total de Trophées <:trph:1397758357464416369>", value="Privé", inline=True)
        embed.add_field(name="Nombre de jeux", value="Privé", inline=True)
        embed.add_field(name="Amis <:amis:1397758314036596897>", value="Privé", inline=True)
        embed.add_field(name="Date de création", value="2017", inline=True)
    elif name == "ZR":
        embed.add_field(name="Status", value="Privé", inline=True)
        embed.add_field(name="Account ID <:aid:1397760504457465879>", value="-", inline=True)
        embed.add_field(name="Pays 🌍", value="France", inline=True)
        embed.add_field(name="Langue", value="FR", inline=True)
        embed.add_field(name="About me", value="@uxhk aka zerty", inline=True)
        embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value="Non Actif", inline=True)
        embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value="Privé", inline=True)
        embed.add_field(name="Niveau de Trophées <:leveltrph:1397758392033869924>", value="Privé", inline=True)
        embed.add_field(name="Total de Trophées <:trph:1397758357464416369>", value="Privé", inline=True)
        embed.add_field(name="Nombre de jeux", value="Privé", inline=True)
        embed.add_field(name="Amis <:amis:1397758314036596897>", value="Privé", inline=True)
        embed.add_field(name="Date de création", value="2017", inline=True)
    elif name == "ms":
        embed.add_field(name="Status", value="Privé", inline=True)
        embed.add_field(name="Account ID <:aid:1397760504457465879>", value="-", inline=True)
        embed.add_field(name="Pays 🌍", value="Japon 🇯🇵", inline=True)
        embed.add_field(name="Langue", value="JP", inline=True)
        embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value="Non Actif", inline=True)
        embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value="Privé", inline=True)
        embed.add_field(name="Niveau de Trophées <:leveltrph:1397758392033869924>", value="Privé", inline=True)
        embed.add_field(name="Total de Trophées <:trph:1397758357464416369>", value="Privé", inline=True)
        embed.add_field(name="Nombre de jeux", value="Privé", inline=True)
        embed.add_field(name="Amis <:amis:1397758314036596897>", value="Privé", inline=True)
        embed.add_field(name="Dernière session de jeu", value="2017", inline=True)
        embed.add_field(name="Date de création", value="2017", inline=True)
    elif name == "qcp":
        embed.add_field(name="Status", value="Privé", inline=True)
        embed.add_field(name="Account ID <:aid:1397760504457465879>", value="-", inline=True)
        embed.add_field(name="Pays 🌍", value="?", inline=True)
        embed.add_field(name="Langue", value="?", inline=True)
        embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value="Non Actif", inline=True)
        embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value="Privé", inline=True)
        embed.add_field(name="Niveau de Trophées <:leveltrph:1397758392033869924>", value="Privé", inline=True)
        embed.add_field(name="Total de Trophées <:trph:1397758357464416369>", value="Privé", inline=True)
        embed.add_field(name="Nombre de jeux", value="Privé", inline=True)
        embed.add_field(name="Amis <:amis:1397758314036596897>", value="Privé", inline=True)
        embed.add_field(name="Date de création", value="2017", inline=True)
    elif name == "bet":
        embed.add_field(name="Status", value="Privé", inline=True)
        embed.add_field(name="Account ID <:aid:1397760504457465879>", value="-", inline=True)
        embed.add_field(name="Pays 🌍", value="?", inline=True)
        embed.add_field(name="Langue", value="?", inline=True)
        embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value="Non Actif", inline=True)
        embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value="Privé", inline=True)
        embed.add_field(name="Niveau de Trophées <:leveltrph:1397758392033869924>", value="Privé", inline=True)
        embed.add_field(name="Total de Trophées <:trph:1397758357464416369>", value="Privé", inline=True)
        embed.add_field(name="Nombre de jeux", value="Privé", inline=True)
        embed.add_field(name="Amis <:amis:1397758314036596897>", value="Privé", inline=True)
        embed.add_field(name="Date de création", value="2017", inline=True)
    elif name == "L17":
        embed.add_field(name="Status", value="Privé", inline=True)
        embed.add_field(name="Account ID <:aid:1397760504457465879>", value="-", inline=True)
        embed.add_field(name="Pays 🌍", value="?", inline=True)
        embed.add_field(name="Langue", value="?", inline=True)
        embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value="Non Actif", inline=True)
        embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value="Privé", inline=True)
        embed.add_field(name="Niveau de Trophées <:leveltrph:1397758392033869924>", value="Privé", inline=True)
        embed.add_field(name="Total de Trophées <:trph:1397758357464416369>", value="Privé", inline=True)
        embed.add_field(name="Nombre de jeux", value="Privé", inline=True)
        embed.add_field(name="Amis <:amis:1397758314036596897>", value="Privé", inline=True)
        embed.add_field(name="Date de création", value="2017", inline=True)
    elif name == "SS_":
        embed.add_field(name="Status", value="Privé", inline=True)
        embed.add_field(name="Account ID <:aid:1397760504457465879>", value="2530784296730065801", inline=True)
        embed.add_field(name="Pays 🌍", value="États-Unis 🇺🇸", inline=True)
        embed.add_field(name="Langue", value="US", inline=True)
        embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value="Non Actif", inline=True)
        embed.add_field(name="Trophées <:alltrph:1397759469542314095>", value="Privé", inline=True)
        embed.add_field(name="Niveau de Trophées <:leveltrph:1397758392033869924>", value="Privé", inline=True)
        embed.add_field(name="Total de Trophées <:trph:1397758357464416369>", value="Privé", inline=True)
        embed.add_field(name="Nombre de jeux", value="Privé", inline=True)
        embed.add_field(name="Amis <:amis:1397758314036596897>", value="3", inline=True)
        embed.add_field(name="Date de création", value="2006 <:2k6:1397618209061994606>", inline=True)
        embed.add_field(name="A propros", value="Gucci Demon.", inline=True)
        embed.set_thumbnail(url="https://psn-rsc.prod.dl.playstation.net/psn-rsc/avatar/UT0016/CUSA06833_00-AV00000000000001_72E7CFC37BB24D706E60_xl.png")

    # Footer unifié
    embed.set_footer(text="Profil PSN")
    return embed

async def setup(bot):
    # Permet de charger ce module sans cog spécifique
    pass

