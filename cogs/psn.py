import discord
from discord import app_commands
from discord.ext import commands
from psnawp_api import PSNAWP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Config PSN
NPSO_TOKEN = "jHmgyNwYsdmX7Hyqqy9HN4QTxwGVUI3kM4O7ksLKH0lm9dr7Cz6VCKxeVl81phSH"
psnawp = PSNAWP(NPSO_TOKEN)

country_map = {
    "France": "🇫🇷 France", "Sweden": "🇸🇪 Suède", "Germany": "🇩🇪 Allemagne",
    "Spain": "🇪🇸 Espagne", "Italy": "🇮🇹 Italie", "United Kingdom": "🇬🇧 Royaume-Uni",
    "United States": "🇺🇸 États-Unis", "Canada": "🇨🇦 Canada", "Japan": "🇯🇵 Japon",
    "Australia": "🇦🇺 Australie", "Netherlands": "🇳🇱 Pays-Bas", "Belgium": "🇧🇪 Belgique",
    "Portugal": "🇵🇹 Portugal", "Brazil": "🇧🇷 Brésil", "Mexico": "🇲🇽 Mexique",
    "Switzerland": "🇨🇭 Suisse", "Russia": "🇷🇺 Russie", "Poland": "🇵🇱 Pologne",
    "Norway": "🇳🇴 Norvège", "Finland": "🇫🇮 Finlande",
}

def get_selenium_avatar(online_id: str) -> str:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--mute-audio")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-hang-monitor")
    options.add_argument("--disable-prompt-on-repost")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--single-process")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.page_load_strategy = 'eager'

    chrome_prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.images": 1
    }
    options.experimental_options["prefs"] = chrome_prefs

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(f"https://profile.playstation.com/share/{online_id}")
        wait = WebDriverWait(driver, 5)
        img_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div[1]/span[2]/span/div/span/img'
        element = wait.until(EC.visibility_of_element_located((By.XPATH, img_xpath)))
        is_loaded = driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0", element)
        return element.get_attribute("src") if is_loaded else "http://static-resource.np.community.playstation.net/avatar_xl/default/Defaultavatar_xl.png"
    except Exception:
        return "http://static-resource.np.community.playstation.net/avatar_xl/default/Defaultavatar_xl.png"
    finally:
        driver.quit()

class Psn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="psn", description="Affiche les infos publiques d’un profil PSN")
    @app_commands.describe(pseudo="Pseudo PSN à inspecter")
    async def psn(self, interaction: discord.Interaction, pseudo: str):
        await interaction.response.defer()
        try:
            user = psnawp.user(online_id=pseudo)
            profile = user.profile()

            account_id = user.account_id
            online_id = user.online_id
            about_me = profile.get("aboutMe", "").strip() or "Aucune bio"

            languages = profile.get("languages") or profile.get("languagesUsed") or []
            langue = languages[0] if languages else "Non disponible"
            ps_plus = "Actif" if profile.get("isPlus") else "Non actif"
            ps_verified = "Oui" if profile.get("isOfficiallyVerified") else "Non"

            region_obj = user.get_region()
            region = country_map.get(region_obj.name, region_obj.name) if region_obj else "Inconnue"

            avatar_url = get_selenium_avatar(online_id)
            profile_banner = f"https://image.api.playstation.com/profile/images/acct/prod/{account_id}/profile.JPEG"

            # Trophées
            try:
                summary = user.trophy_summary()
                earned = summary.earned_trophies
                trophy_level = summary.trophy_level
                total_trophies = earned.bronze + earned.silver + earned.gold + earned.platinum
                trophies = (
                    f"<:bronze:1396977760999833684>  Bronze\n      {earned.bronze}\n"
                    f"<:argent:1396977821485629602>  Argent\n      {earned.silver}\n"
                    f"<:or:1396977699662205018>  Or\n      {earned.gold}\n"
                    f"<:platine:1396977650907615352>  Platine\n      {earned.platinum}"
                )
            except:
                trophy_level = "Privé"
                trophies = "Privés"
                total_trophies = "Privé"

            # Nombre de jeux
            try:
                total_games = len(list(user.trophy_titles()))
            except:
                total_games = "Privé"

            # Embed
            embed = discord.Embed(title="Profil PSN", color=0x0094FF)
            embed.set_thumbnail(url=avatar_url)
            embed.set_image(url=profile_banner)

            if online_id.lower() != pseudo.lower():
                embed.add_field(name="Ancien PSN", value=pseudo, inline=False)
                embed.add_field(name="Nouveau PSN", value=online_id, inline=False)
            else:
                embed.add_field(name="PSN", value=online_id, inline=False)

            embed.add_field(name="Account ID", value=account_id, inline=False)
            embed.add_field(name="Certifié", value=ps_verified, inline=False)
            embed.add_field(name="Pays", value=region, inline=True)
            embed.add_field(name="Langue", value=langue, inline=True)
            embed.add_field(name="PlayStation Plus", value=ps_plus, inline=True)
            embed.add_field(name="Trophées", value=trophies, inline=False)
            embed.add_field(name="Niveau Trophée", value=str(trophy_level), inline=True)
            embed.add_field(name="🏆 Total Trophées", value=str(total_trophies), inline=True)
            embed.add_field(name="Nombre de jeux", value=str(total_games), inline=True)
            embed.add_field(name="À propos", value=about_me, inline=False)

            view = discord.ui.View()
            view.add_item(discord.ui.Button(
                label="🔗 Voir le profil PSN",
                url=f"https://profile.playstation.com/share/{online_id}",
                style=discord.ButtonStyle.link
            ))

            await interaction.followup.send(embed=embed, view=view)

        except Exception as e:
            await interaction.followup.send(f"Erreur lors de la récupération du profil : {e}")

async def setup(bot):
    await bot.add_cog(Psn(bot))
