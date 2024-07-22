import discord
from discord.ext import commands
import requests
import json
import io
import os
import subprocess
import tempfile
from faker import Faker
import matplotlib.pyplot as plt

# Konfigurasi API keys dan token
DISCORD_TOKEN = 'your_discord_token_here'
YOUR_OPENWEATHER_API_KEY = '4b7d62092df37b1438ac0f53469dfffe'
YOUR_OPENAI_API_KEY = 'sk-None-9OeepaBhogdFaOR5JhAmT3BlbkFJGtGXaAdqfv2SgnGagUT8'
SHODAN_API_KEY = 'vo9xPekc8ZkPTpG2tTonN50wCkEvgsuP'
PIPL_API_KEY = 'your_pipl_api_key'
VIRUSTOTAL_API_KEY = '8bc7604ef2a7cd931aad82a18fc989acaefbf2942c4312798c61290dffd49e6e'
NEWSAPI_KEY = '80da55ff49204423a7fa3c1b76961f37'
GOOGLE_MAPS_API_KEY = 'AIzaSyCLnvPDqUKiDcMqDsxgXtni_mWx_cPMFqA'
MOZ_API_KEY = 'HjjCTQtTJBC0IS4qjL9S7YAtNKnHBIwykykkEln58rHWg4SDmCEUtCa417uGxarY'
HIBP_API_KEY = 'your_hibp_api_key'

# File untuk menyimpan status toggle dan peringatan
TOGGLE_FILE = 'toggle_status.json'
WARNING_FILE = 'warnings.json'

# Memuat status toggle dari file
def load_toggles():
    if os.path.exists(TOGGLE_FILE):
        with open(TOGGLE_FILE, 'r') as file:
            return json.load(file)
    return {}

# Menyimpan status toggle ke file
def save_toggles(toggles):
    with open(TOGGLE_FILE, 'w') as file:
        json.dump(toggles, file, indent=4)

# Memuat data peringatan dari file
def load_warnings():
    if os.path.exists(WARNING_FILE):
        with open(WARNING_FILE, 'r') as file:
            return json.load(file)
    return {}

# Menyimpan data peringatan ke file
def save_warnings(warnings):
    with open(WARNING_FILE, 'w') as file:
        json.dump(warnings, file, indent=4)

# Status toggle untuk fitur
toggles = load_toggles()
warnings = load_warnings()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Bot telah siap. Logged in as {bot.user.name}')

@bot.command(name='toggle')
@commands.has_permissions(administrator=True)
async def toggle_feature(ctx, feature: str):
    """Aktifkan atau nonaktifkan fitur."""
    valid_features = ['sendemail', 'traceip', 'rcescanner', 'traceroute', 'reverseip', 'exifdata',
                      'tempemail', 'checkmail', 'whois', 'status', 'weather', 'chat', 'domaininfo',
                      'socialmedia', 'nameinfo', 'analyzet', 'news', 'map', 'checkda', 'breach',
                      'plotdata', 'dalfox', 'fakedata', 'fakexy', 'warn']
    feature = feature.lower()

    if feature not in valid_features:
        await ctx.send('Fitur tidak valid. Fitur yang valid: ' + ', '.join(valid_features))
        return

    if feature in toggles:
        del toggles[feature]
        status = 'nonaktif'
    else:
        toggles[feature] = True
        status = 'aktif'

    save_toggles(toggles)
    await ctx.send(f'Fitur "{feature}" telah {status}.')

def is_feature_active(feature):
    return feature in toggles

@bot.command(name='warn')
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, reason: str = 'Tidak ada alasan'):
    if not is_feature_active('warn'):
        await ctx.send('Fitur ini tidak aktif.')
        return

    member_id = str(member.id)
    if member_id in warnings:
        warnings[member_id]['count'] += 1
    else:
        warnings[member_id] = {'count': 1, 'last_warning': reason}

    save_warnings(warnings)
    await ctx.send(f'{member.mention} telah diperingatkan. Alasan: {reason}. Total peringatan: {warnings[member_id]["count"]}')

    if warnings[member_id]['count'] >= 3:
        await ctx.send(f'{member.mention} telah mencapai batas peringatan. Pertimbangkan tindakan lebih lanjut.')

@bot.command(name='sendemail')
async def send_email(ctx, email: str, *, message: str):
    if not is_feature_active('sendemail'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika pengiriman email di sini
    await ctx.send(f'Email dikirim ke {email} dengan pesan: {message}')

@bot.command(name='traceip')
async def trace_ip(ctx, ip_address: str):
    if not is_feature_active('traceip'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika pelacakan IP di sini
    await ctx.send(f'Informasi IP untuk {ip_address}')

@bot.command(name='rcescanner')
async def rce_scanner(ctx, url: str):
    if not is_feature_active('rcescanner'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika pemindaian RCE di sini
    await ctx.send(f'Pemindaian RCE untuk URL {url}')

@bot.command(name='traceroute')
async def traceroute(ctx, ip_address: str):
    if not is_feature_active('traceroute'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika traceroute di sini
    await ctx.send(f'Rute traceroute untuk IP {ip_address}')

@bot.command(name='reverseip')
async def reverse_ip(ctx, ip_address: str):
    if not is_feature_active('reverseip'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika pencarian IP terbalik di sini
    await ctx.send(f'Informasi IP terbalik untuk {ip_address}')

@bot.command(name='exifdata')
async def exif_data(ctx, image_url: str):
    if not is_feature_active('exifdata'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika pengambilan data EXIF di sini
    await ctx.send(f'Data EXIF untuk gambar {image_url}')

@bot.command(name='tempemail')
async def temp_email(ctx):
    if not is_feature_active('tempemail'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika email sementara di sini
    await ctx.send('Email sementara dibuat.')

@bot.command(name='checkmail')
async def check_mail(ctx, email: str):
    if not is_feature_active('checkmail'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika pemeriksaan email di sini
    await ctx.send(f'Informasi untuk email {email}')

@bot.command(name='whois')
async def whois(ctx, domain: str):
    if not is_feature_active('whois'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika whois di sini
    await ctx.send(f'Informasi WHOIS untuk domain {domain}')

@bot.command(name='status')
async def status(ctx):
    if not is_feature_active('status'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika status di sini
    await ctx.send('Status sistem saat ini.')

@bot.command(name='weather')
async def weather(ctx, *, location: str):
    if not is_feature_active('weather'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={YOUR_OPENWEATHER_API_KEY}')
        data = response.json()
        await ctx.send(f'Cuaca di {location}: {json.dumps(data, indent=2)}')
    except Exception as e:
        await ctx.send(f'Gagal mendapatkan informasi cuaca. Error: {str(e)}')

@bot.command(name='chat')
async def chat(ctx, *, prompt: str):
    if not is_feature_active('chat'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.post('https://api.openai.com/v1/engines/davinci/completions', headers={
            'Authorization': f'Bearer {YOUR_OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }, json={
            'prompt': prompt,
            'max_tokens': 50
        })
        data = response.json()
        await ctx.send(f'Jawaban: {data["choices"][0]["text"]}')
    except Exception as e:
        await ctx.send(f'Gagal menghubungi API OpenAI. Error: {str(e)}')

@bot.command(name='domaininfo')
async def domain_info(ctx, domain: str):
    if not is_feature_active('domaininfo'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.get(f'https://api.shodan.io/dns/resolve?hostname={domain}&key={SHODAN_API_KEY}')
        data = response.json()
        await ctx.send(f'Informasi Domain {domain}: {json.dumps(data, indent=2)}')
    except Exception as e:
        await ctx.send(f'Gagal mendapatkan informasi domain. Error: {str(e)}')

@bot.command(name='socialmedia')
async def social_media(ctx, username: str):
    if not is_feature_active('socialmedia'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika pencarian media sosial di sini
    await ctx.send(f'Informasi media sosial untuk {username}')

@bot.command(name='nameinfo')
async def name_info(ctx, name: str):
    if not is_feature_active('nameinfo'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika pencarian informasi nama di sini
    await ctx.send(f'Informasi untuk nama {name}')

@bot.command(name='analyzet')
async def analyze_t(ctx, url: str):
    if not is_feature_active('analyzet'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika analisis T di sini
    await ctx.send(f'Analisis T untuk URL {url}')

@bot.command(name='news')
async def news(ctx, *, query: str):
    if not is_feature_active('news'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.get(f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}')
        data = response.json()
        await ctx.send(f'Berita tentang {query}: {json.dumps(data, indent=2)}')
    except Exception as e:
        await ctx.send(f'Gagal mendapatkan berita. Error: {str(e)}')

@bot.command(name='map')
async def map_info(ctx, *, location: str):
    if not is_feature_active('map'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.get(f'https://maps.googleapis.com/maps/api/staticmap?center={location}&zoom=13&size=600x300&key={GOOGLE_MAPS_API_KEY}')
        with open('map.png', 'wb') as f:
            f.write(response.content)
        with open('map.png', 'rb') as f:
            await ctx.send(file=discord.File(f, 'map.png'))
    except Exception as e:
        await ctx.send(f'Gagal mendapatkan peta. Error: {str(e)}')

@bot.command(name='checkda')
async def check_da(ctx, domain: str):
    if not is_feature_active('checkda'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.get(f'https://moz.com/api/v2/url_metrics?url={domain}&access_token={MOZ_API_KEY}')
        data = response.json()
        await ctx.send(f'Informasi DA untuk domain {domain}: {json.dumps(data, indent=2)}')
    except Exception as e:
        await ctx.send(f'Gagal mendapatkan informasi DA. Error: {str(e)}')

@bot.command(name='breach')
async def breach(ctx, email: str):
    if not is_feature_active('breach'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}', headers={
            'User-Agent': 'DiscordBot',
            'Authorization': f'Bearer {HIBP_API_KEY}'
        })
        data = response.json()
        await ctx.send(f'Pelanggaran untuk email {email}: {json.dumps(data, indent=2)}')
    except Exception as e:
        await ctx.send(f'Gagal mendapatkan informasi pelanggaran. Error: {str(e)}')

@bot.command(name='plotdata')
async def plot_data(ctx, x_values: str, y_values: str):
    if not is_feature_active('plotdata'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        x = list(map(float, x_values.split(',')))
        y = list(map(float, y_values.split(',')))
        plt.figure()
        plt.plot(x, y)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Plot Data')
        plt.savefig('plot.png')
        with open('plot.png', 'rb') as f:
            await ctx.send(file=discord.File(f, 'plot.png'))
    except Exception as e:
        await ctx.send(f'Gagal memplot data. Error: {str(e)}')

@bot.command(name='dalfox')
async def dalfox(ctx, url: str):
    if not is_feature_active('dalfox'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    # Implementasikan logika Dalfox di sini
    await ctx.send(f'Analisis Dalfox untuk URL {url}')

@bot.command(name='fakedata')
async def fake_data(ctx):
    if not is_feature_active('fakedata'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    fake = Faker()
    data = {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email()
    }
    await ctx.send(f'Data Palsu: {json.dumps(data, indent=2)}')

@bot.command(name='fakexy')
async def fake_xy(ctx):
    if not is_feature_active('fakexy'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    fake = Faker()
    data = {
        'latitude': fake.latitude(),
        'longitude': fake.longitude()
    }
    await ctx.send(f'Koordinat Palsu: {json.dumps(data, indent=2)}')

@bot.command(name='exiftool')
async def exif_tool(ctx, image_url: str):
    if not is_feature_active('exiftool'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.get(image_url)
        image_data = io.BytesIO(response.content)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(image_data.read())
            temp_file_path = temp_file.name

        process = subprocess.run(['exiftool', temp_file_path], capture_output=True, text=True)
        os.remove(temp_file_path)
        await ctx.send(f'Data EXIF: {process.stdout}')
    except Exception as e:
        await ctx.send(f'Gagal mendapatkan data EXIF. Error: {str(e)}')

@bot.command(name='tempmail')
async def temp_mail(ctx):
    if not is_feature_active('tempmail'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.get('https://temp-mail.org/en/api/v1/')
        data = response.json()
        await ctx.send(f'Email sementara: {data.get("email")}')
    except Exception as e:
        await ctx.send(f'Gagal mendapatkan email sementara. Error: {str(e)}')

@bot.command(name='weather')
async def weather(ctx, *, location: str):
    if not is_feature_active('weather'):
        await ctx.send('Fitur ini tidak aktif.')
        return
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={YOUR_OPENWEATHER_API_KEY}')
        data = response.json()
        await ctx.send(f'Cuaca di {location}: {json.dumps(data, indent=2)}')
    except Exception as e:
        await ctx.send(f'Gagal mendapatkan informasi cuaca. Error: {str(e)}')

bot.run(DISCORD_TOKEN)
