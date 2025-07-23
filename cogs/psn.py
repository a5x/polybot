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
import json
import os

# Config PSN
NPSO_TOKEN = "jHmgyNwYsdmX7Hyqqy9HN4QTxwGVUI3kM4O7ksLKH0lm9dr7Cz6VCKxeVl81phSH"
psnawp = PSNAWP(NPSO_TOKEN)

# Mapping pays
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
        is_loaded = driver.execute_script(
            "return arguments[0].complete && arguments[0].naturalWidth > 0", element
        )
        return element.get_attribute("src") if is_loaded else \
               "http://static-resource.np.community.playstation.net/avatar_xl/default/Defaultavatar_xl.png"
    except Exception:
        return "http://static-resource.np.community.playstation.net/avatar_xl/default/Defaultavatar_xl.png"
    finally:
        driver.quit()

class ProfileView(discord.ui.View):
    def __init__(self, online_id: str):
        super().__init__(timeout=None)
        self.online_id = online_id

        # Bouton lien pour voir le profil PSN
        self.add_item(discord.ui.Button(
            label="🔗 Partager le profil PSN",
            url=f"https://profile.playstation.com/share/{online_id}",
            style=discord.ButtonStyle.link
        ))

        # Bouton lien pour partager le profil PSN
        self.add_item(discord.ui.Button(
            label="📤 Voir le Profil PSN",
            url=f"https://profile.playstation.com/{online_id}",
            style=discord.ButtonStyle.link
        ))

class Psn(commands.Cog):
    COUNTS_FILE = "data/psn_counts.json"
    DB_FILE = "data/psn_db.json"

    def __init__(self, bot):
        self.bot = bot
        # Charger compteur
        if os.path.exists(self.COUNTS_FILE):
            with open(self.COUNTS_FILE, "r", encoding="utf-8") as f:
                self.counts = json.load(f)
        else:
            self.counts = {}

        # Charger mini-database des dates de création
        try:
            if os.path.exists(self.DB_FILE):
                with open(self.DB_FILE, "r", encoding="utf-8") as f:
                    raw_db = json.load(f)
                    # Normaliser les clés en lowercase pour la recherche
                    self.psn_db = {k.lower(): v for k, v in raw_db.items()}
            else:
                self.psn_db = {}
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"[⚠️] Impossible de charger {self.DB_FILE} : {e}")
            self.psn_db = {}
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"[⚠️] Impossible de charger {self.DB_FILE} : {e}")
            self.psn_db = {}

            self.psn_db = {}

    def save_counts(self):
        with open(self.COUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.counts, f, ensure_ascii=False, indent=2)

    @app_commands.command(name="psn", description="Affiche les infos publiques d’un profil PSN")
    @app_commands.describe(pseudo="Pseudo PSN à inspecter")
    async def psn(self, interaction: discord.Interaction, pseudo: str):
        await interaction.response.defer()

        # Incrémente le compteur
        key = pseudo.lower()
        self.counts[key] = self.counts.get(key, 0) + 1
        self.save_counts()
        check_count = self.counts[key]

        try:
            user = psnawp.user(online_id=pseudo)
            profile = user.profile()

            account_id = user.account_id
            online_id = user.online_id
            about_me = profile.get("aboutMe", "").strip() or "Aucune bio"

            # Gestion de la langue
            languages = profile.get("languages") or profile.get("languagesUsed") or []
            langue = languages[0].split('-')[-1].upper() if languages else "Non disponible"

            # PS Plus et vérifié
            ps_plus = "Actif" if profile.get("isPlus") else "Non actif"
            ps_verified = profile.get("isOfficiallyVerified", False)
            display_name = f"{online_id} <:certif:1397614299039399936>" if ps_verified else online_id

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
                    f"<:bronze:1396977760999833684> Bronze : {earned.bronze}\n"
                    f"<:argent:1396977821485629602> Argent : {earned.silver}\n"
                    f"<:or:1396977699662205018> Or : {earned.gold}\n"
                    f"<:platine:1396977650907615352> Platine : {earned.platinum}"
                )
            except:
                trophy_level = "Privé"
                trophies = "Privés"
                total_trophies = "Privé"

            try:
                total_games = len(list(user.trophy_titles()))
            except:
                total_games = "Privé"

                        # Récupérer date de création depuis la DB
            creation_display = None
            creation_value = self.psn_db.get(key)
            if creation_value:
                # On affiche directement la chaîne (ex. "2022 <:emoji:ID>")
                creation_display = creation_value

            # Construction de l'embed
            embed = discord.Embed(title="Profil PSN", color=0x0094FF)
            embed.set_thumbnail(url=avatar_url)
            embed.set_image(url=profile_banner)

            embed.add_field(name="PSN", value=(f"{display_name}"), inline=False)
            embed.add_field(name="Account ID", value=account_id, inline=False)
            embed.add_field(name="Certifié", value="Oui" if ps_verified else "Non", inline=False)
            embed.add_field(name="Pays", value=region, inline=True)
            embed.add_field(name="Langue", value=langue, inline=True)
            embed.add_field(name="PlayStation Plus <:psplus:1397614330601799873>", value=ps_plus, inline=True)
            embed.add_field(name="Trophées", value=trophies, inline=False)
            embed.add_field(name="Niveau Trophée", value=str(trophy_level), inline=True)
            embed.add_field(name="🏆 Total Trophées", value=str(total_trophies), inline=True)
            embed.add_field(name="Nombre de jeux", value=str(total_games), inline=True)
            if creation_display:
                embed.add_field(name="Date de création", value=creation_display, inline=False)
            embed.add_field(name="À propos", value=about_me, inline=False)

            # Footer avec compteur
            suffix = "check" if check_count == 1 else "checks"
            embed.set_footer(text=f"Le nombre de {suffix} est {check_count} pour ce psn")

            # Envoi
            view = ProfileView(online_id)
            await interaction.followup.send(embed=embed, view=view)

        except Exception as e:
            await interaction.followup.send(f"Erreur lors de la récupération du profil : {e}")

async def setup(bot):
    await bot.add_cog(Psn(bot))
