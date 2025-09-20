import re
import pandas as pd
from datetime import datetime
from app.data.parameters import *
from app.utils.logger import warn


class Normalizer:
    def __init__(self, progress_manager):
        self.progress_manager = progress_manager


    def normalize_vehicle_data(self, vehicle) -> dict:
        """Clean and standardize a single vehicle's data."""

        url = vehicle.get('url', '')

        return {
            'url': url,
            'image': vehicle.get('image', '').strip(),
            'title': vehicle.get('title', '').strip(),
            PRICE: self.clean_numbers(vehicle.get(PRICE, '')),
            MILEAGE: self.clean_numbers(vehicle.get(MILEAGE, '')),
            YEAR: self.clean_year(vehicle.get(YEAR, '')),
            ENGINE_CAPACITY: self.clean_numbers(vehicle.get(ENGINE_CAPACITY, '')),
            MAKE: self.clean_make_model(vehicle.get(MAKE, '')),
            TRANSMISSION: self.clean_transmission(vehicle.get(TRANSMISSION, ''), url),
            FUEL_TYPE: self.clean_fuel_type(vehicle.get(FUEL_TYPE, ''), url),
            MODEL: self.clean_make_model(vehicle.get(MODEL, '')),
            CATEGORY: self.clean_category(vehicle.get(CATEGORY, ''))
        }


    @staticmethod
    def clean_numbers(value) -> int | None:
        """Remove symbols, commas, and convert to integer by truncating decimal."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return int(float(value))

        # Remove all non-digit characters, except periods surrounded by digits
        value_str = str(value).strip()
        value_str = re.sub(r'(?<!\d)\.(?!\d)', '', value_str)
        value_str = re.sub(r'[^\d.]', '', value_str)

        try:
            return int(float(value_str))
        except ValueError:
            return None


    def clean_year(self, year) -> int | None:
        """Ensure YEAR is a valid 4-digit year."""
        base_year = 1900
        cleaned_year = self.clean_numbers(year)

        if cleaned_year is None:
            return None
        try:
            if base_year <= cleaned_year <= datetime.now().year:
                return cleaned_year
        except (ValueError, TypeError):
            return None


    def clean_transmission(self, transmission, url) -> str | None:
        """Normalize transmission case and values."""
        if not transmission:
            return None

        transmission_str = str(transmission).strip().lower()

        if 'auto' in transmission_str:
            return 'automatic'
        elif 'manual' in transmission_str:
            return 'manual'
        else:
            self.progress_manager.log({
                'action': 'Normalize',
                'message': f'Not Supported transmission: {transmission_str}',
                'url': url
            })
            return None


    def clean_fuel_type(self, fuel_type, url) -> str | None:
        """Normalize fuel type case and values."""
        if not fuel_type:
            return None

        fuel_str = str(fuel_type).strip().lower()
        valid_fuels = ['petrol', 'diesel', 'electric', 'hybrid']

        if fuel_str in valid_fuels:
            return fuel_str
        else:
            self.progress_manager.log({
                'action': 'Normalize',
                'message': f'Not Supported fuel type: {fuel_type}',
                'url': url
            })
            return None

    @staticmethod
    def clean_make_model(value) -> str | None:
        """Normalize make and model case and values."""
        if isinstance(value, str):
            value = value.replace('-', ' ')   # Replace dashes with spaces
            value = value.replace('.', '')    # Remove periods
            value = value.title()                         # Title Case
            value = ' '.join(value.split())               # Remove extra spaces
            return value if value else None
        else:
            return None


    @staticmethod
    def clean_category(category: str) -> str | None:
        """Normalize vehicle categories across websites."""
        if not category:
            return None

        # Special handling for patpat car categories
        if category.lower().startswith('car'):
            return "car"

        mapping = {
            "cars": "car",
            "Cars": "car",
            "vans": "van",
            "Vans": "van",
            "Van": "van",
            "suvs": "suv",
            "pickups": "suv",
            "SUV": "suv",
            "motorcycles": "motorcycle",
            "Motorbikes": "motorcycle",
            "Bike": "motorcycle",
            "buses": "bus",
            "Buses": "bus",
            "Bus": "bus",
            "lorries": "lorry",
            "crew-cabs": "lorry",
            "Lorries & Trucks": "lorry",
            "Truck": "lorry",
            "three-wheels": "three_wheeler",
            "Three Wheelers": "three_wheeler",
            "Three wheeler": "three_wheeler",
            "tractors": "tractor",
            "Tractors": "tractor",
            "Land": "tractor",
            "heavy-duties": "heavy_duty",
            "Heavy Duty": "heavy_duty",
            "Heavy": "heavy_duty",
            "others": "other"
        }

        if category in mapping:
            return mapping[category]

        return None


    def null_cleanup(self, vehicles: list) -> list[dict]:
        """
        Handle null values in vehicle dataset:
          1. Drop records missing essential fields (PRICE, YEAR, MAKE).
          3. Fill remaining optional fields with placeholders
             to avoid leaving nulls in the dataset.
        """

        essential_fields = [PRICE, YEAR, MAKE]

        # Convert vehicles list into DataFrame for easier processing
        df = pd.DataFrame(vehicles)

        # Keep only rows where essential fields are not null
        df_cleaned = df.dropna(subset=essential_fields).copy()

        # Identify and log dropped rows
        dropped_rows = df.loc[~df.index.isin(df_cleaned.index)]
        if not dropped_rows.empty:
            count = 0
            for _, row in dropped_rows.iterrows():
                count += 1
                missing = [field for field in essential_fields if pd.isna(row[field])]
                url = row.get("url", "N/A")
                self.progress_manager.log({'action': 'Dropped', 'message': f'Missing {missing[0]}', 'url': url})
            self.progress_manager.add_dropped(count)

        # Count nulls before filling
        null_counts = df_cleaned.isnull().sum()

        # Fill optional fields with placeholders instead of null
        df_cleaned[MILEAGE] = df_cleaned[MILEAGE].fillna(-1)
        df_cleaned[ENGINE_CAPACITY] = df_cleaned[ENGINE_CAPACITY].fillna(-1)
        df_cleaned[FUEL_TYPE] = df_cleaned[FUEL_TYPE].fillna('N/A')
        df_cleaned[MODEL] = df_cleaned[MODEL].fillna('N/A')
        df_cleaned[TRANSMISSION] = df_cleaned[TRANSMISSION].fillna('N/A')
        df_cleaned[CATEGORY] = df_cleaned[CATEGORY].fillna('other')

        # Log how many placeholders were filled
        for field in [MILEAGE, ENGINE_CAPACITY, FUEL_TYPE, MODEL, TRANSMISSION, CATEGORY]:
            if null_counts.get(field, 0) > 0:
                placeholder = '-1' if field in [MILEAGE, ENGINE_CAPACITY] else 'N/A'
                if field == CATEGORY:
                    placeholder = 'other'
                warn(f"Filled {null_counts[field]} nulls in '{field}' with '{placeholder}'")
                self.progress_manager.add_modified(int(null_counts[field]))

        # Convert cleaned DataFrame back to list of dicts
        return df_cleaned.to_dict(orient="records")


map1 = {
  "Alfa Romeo": {
    "Car": "Car"
  },
  "Aston Martin": {
    "Db9": "Db9"
  },
  "Audi": {
    "A3": "A3",
    "Q2": "Q2",
    "A1": "A1",
    "A4": "A4",
    "Q7": "Q7",
    "A5": "A5",
    "A6": "A6",
    "Q5": "Q5",
    "Q3": "Q3",
    "Q4": "Q4",
    "Rs4": "Rs4"
  },
  "Austin": {
    "Mini": "Mini"
  },
  "Baic": {
    "X55": "X55",
    "X25": "X25"
  },
  "Bajaj": {
    "Qute": "Qute"
  },
  "Bentley": {
    "Flying Spur": "Flying Spur"
  },
  "Bmw": {
    "2 Series": "5 Series",
    "3 Series": "5 Series",
    "5 Series": "5 Series",
    "6 Series": "5 Series",
    "7 Series": "5 Series",
    "X Series": "X Series",
    "I Series": "I Series",
    "M Series": "M Series",
    "E Series": "E Series",
    "740Le": "740Le",
    "Activehybrid 7": "Activehybrid 7",
    "225Xe": "225Xe",
    "X1": "X1",
    "I3": "I3",
    "Mini Cooper": "Mini Cooper"
  },
  "Byd": {
    "Sealion 6": "Sealion 6",
    "Dolphin": "Dolphin",
    "Att03": "Att03",
    "Seal": "Seal"
  },
  "Chery": {
    "Qq": "Qq",
    "Tiggo": "Tiggo",
    "Yoyo": "Yoyo",
    "Fulwin": "Fulwin",
    "J2": "J2",
    "Q22": "Q22"
  },
  "Chevrolet": {
    "Cruze": "Cruze",
    "Aveo": "Aveo",
    "Car": "Car",
    "Beat": "Beat",
    "Optra": "Optra"
  },
  "Daewoo": {
    "Nubira": "Nubira",
    "Lanos": "Lanos",
    "Espero Cd": "Espero Cd",
    "Matiz": "Matiz",
    "Cielo": "Cielo"
  },
  "Daihatsu": {
    "Mira": "Mira",
    "Taft": "Taft",
    "Hijet": "Hijet",
    "Boon": "Boon",
    "Thor": "Thor",
    "Rocky": "Rocky",
    "Atrai": "Atrai",
    "Tanto": "Tanto",
    "Terios": "Terios",
    "Move": "Move",
    "Car": "Car",
    "Charade": "Charade",
    "Copen": "Copen",
    "Cuore": "Cuore",
    "Hijet Cargo": "Hijet Cargo",
    "F55": "F55"
  },
  "Datsun": {
    "Redi Go": "Redi Go",
    "Sunny": "Sunny",
    "Car": "Car"
  },
  "Dfsk": {
    "Glory": "Glory",
    "I Auto": "I Auto",
    "580": "580",
    "V27": "V27",
    "330": "330"
  },
  "Fiat": {
    "1100": "1100",
    "Panda": "Panda"
  },
  "Ford": {
    "Ranger": "Ranger",
    "Raptor": "Raptor",
    "Laser": "Laser",
    "Focus": "Focus",
    "Mustang": "Mustang",
    "Fiesta": "Fiesta",
    "Ecosport": "Ecosport",
    "Everest": "Everest",
    "Telstar": "Telstar",
    "Car": "Car",
    "Festiva": "Festiva"
  },
  "Geely": {
    "Panda": "Panda",
    "Ck08": "Ck08"
  },
  "Honda": {
    "Vezel": "Vezel",
    "Fit": "Fit",
    "Civic": "Civic",
    "Grace": "Grace",
    "City": "City",
    "Cr V": "Cr V",
    "Insight": "Insight",
    "N Box": "N Box",
    "Accord": "Accord",
    "Aria": "Aria",
    "N Wgn": "N Wgn",
    "Shuttle": "Shuttle",
    "Airwave": "Airwave",
    "Jade": "Jade",
    "Avancier": "Avancier",
    "Dba": "Dba",
    "Hr V": "Hr V",
    "Crossroad": "Crossroad",
    "Integra": "Integra",
    "S660": "S660",
    "Spike": "Spike",
    "Zr V": "Zr V",
    "Acty": "Acty",
    "Chr": "Chr",
    "Custom": "Custom",
    "Freed": "Freed"
  },
  "Hyundai": {
    "Accent": "Accent",
    "Tucson": "Tucson",
    "Tucsone": "Tucson",
    "Santa Fe": "Santa Fe",
    "Sonata": "Sonata",
    "Eon": "Eon",
    "Elantra": "Elantra",
    "Getz": "Getz",
    "H 100": "H 100",
    "Matrix": "Matrix",
    "Grand I10": "Grand I10",
    "Coupe": "Coupe",
    "Santro": "Santro",
    "Car": "Car",
    "Kona": "Kona",
    "Creta": "Creta",
    "Venue": "Venue",
    "Indigo": "Indigo"
  },
  "Isuzu": {
    "Fargo": "Fargo",
    "Double Cab": "Double Cab",
    "Mu X": "Mu X",
    "Trooper": "Trooper",
    "Jeep": "Jeep",
    "Gemini": "Gemini"
  },
  "Jac": {
    "T9": "T9"
  },
  "Jaguar": {
    "X Type": "X Type",
    "F Pace": "F Pace",
    "Xf": "Xf"
  },
  "Jeep": {
    "Renegade Limited": "Renegade Limited"
  },
  "Jetour": {
    "X70": "X70"
  },
  "Kia": {
    "Sorento": "Sorento",
    "Rio": "Rio",
    "Sportage": "Sportage",
    "Picanto": "Picanto",
    "Stonic": "Stonic",
    "Mentor": "Mentor",
    "Sephia": "Sephia",
    "Clarus": "Clarus",
    "Carens": "Carens",
    "Soul": "Soul",
    "Cerato": "Cerato",
    "Pride": "Pride",
    "Niro": "Niro",
    "Spectra": "Spectra"
  },
  "Land Rover": {
    "Land Rover": "Range Rover",
    "Range Rover": "Range Rover",
    "Defender": "Defender",
    "Discovery": "Discovery",
    "Freelander": "Freelander",
    "Evoque": "Evoque"
  },
  "Lexus": {
    "Rx Series": "Rx Series",
    "Lx": "Lx"
  },
  "Mahindra": {
    "Kuv": "Kuv",
    "Jeep": "Jeep"
  },
  "Maruti": {
    "Car": "Car"
  },
  "Maserati": {
    "Quattroporte": "Quattroporte"
  },
  "Mazda": {
    "Familia": "Familia",
    "Flair": "Flair",
    "Bongo": "Bongo",
    "Demio": "Demio",
    "Axela": "Axela",
    "Rx8": "Rx8",
    "Scrum": "Scrum",
    "6": "6",
    "323": "323",
    "3": "3",
    "Butterfly": "Butterfly",
    "Tribute": "Tribute",
    "Carol": "Carol",
    "B Series": "B Series",
    "Brawny": "Brawny",
    "Ad Wagon": "Ad Wagon",
    "626": "626",
    "Car": "Car",
    "Cx 5": "Cx 5",
    "Vanette": "Vanette",
    "Astina": "Astina"
  },
  "Mercedes Benz": {
    "C Class": "C Class",
    "E Class": "E Class",
    "Cla": "Cla",
    "S Class": "S Class",
    "A Class": "A Class",
    "Gle Class": "Gle Class",
    "220": "220",
    "Glb Class": "Glb Class",
    "Car": "Car",
    "Glc Class": "Glc Class",
    "Gla Class": "Gla Class",
    "G Class": "G Class",
    "B Class": "B Class",
    "W Class": "W Class",
    "Mb 140D": "Mb 140D"
  },
  "Mg": {
    "Zs": "Zs",
    "Mg4 X Icon Ev": "Mg4 X Icon Ev",
    "6": "6"
  },
  "Micro": {
    "Panda": "Panda",
    "Panda Cross": "Panda",
    "Trend": "Trend",
    "Kyron": "Kyron",
    "Mx7": "Mx7",
    "Actyon": "Actyon",
    "Mpv": "Mpv",
    "Tivoli": "Tivoli",
    "Baic": "Baic",
    "Ssangyong": "Ssangyong",
    "Emgrand 7": "Emgrand 7",
    "Ec 7": "Ec 7",
    "Rexton": "Rexton",
    "Geely Ck": "Geely Ck",
    "Almaz": "Almaz",
    "Korando": "Korando"
  },
  "Mini": {
    "Cooper": "Cooper"
  },
  "Mitsubishi": {
    "Lancer": "Lancer",
    "Montero": "Montero",
    "Ek": "Ek",
    "Outlander": "Outlander",
    "Minica": "Minicab",
    "Minicab": "Minicab",
    "Pajero": "Pajero",
    "Pajero Io": "Pajero",
    "L200": "L200",
    "Delica": "Delica",
    "Montero Sport": "Montero Sport",
    "Eclipse": "Eclipse",
    "Jeep": "Jeep",
    "Galant": "Galant",
    "L300": "L300",
    "Xpander": "Xpander",
    "Xpander Cross": "Xpander",
    "Car": "Car",
    "Van": "Van",
    "Mini Cab": "Mini Cab",
    "Colt": "Colt",
    "Triton": "Triton",
    "Intercooler": "Intercooler",
    "Asx": "Asx",
    "4Dr5": "4Dr5",
    "Mini": "Mini",
    "Town Box": "Town Box",
    "I Miev": "I Miev",
    "Rvr": "Rvr",
    "Strada": "Strada",
    "L400": "L400",
    "Carisma": "Carisma",
    "Verada": "Verada",
    "C 11": "C 11"
  },
  "Nissan": {
    "Caravan": "Caravan",
    "Sunny": "Sunny",
    "Fb 13": "Fb 15",
    "Fb 14": "Fb 15",
    "Fb 15": "Fb 15",
    "Vanette": "Vanette",
    "X Trail": "X Trail",
    "March": "March",
    "Clipper": "Clipper",
    "Dayz": "Dayz",
    "Bluebird": "Bluebird",
    "Leaf": "Leaf",
    "Tiida": "Tiida",
    "Almera": "Almera",
    "B11": "B11",
    "B12": "B11",
    "B13": "B11",
    "N 16": "N 16",
    "N 17": "N 16",
    "Ad Wagon": "Ad Wagon",
    "Pulsar": "Pulsar",
    "Cefiro": "Cefiro",
    "Navara": "Navara",
    "Nv100": "Nv100",
    "Presea": "Presea",
    "Exsunny": "Exsunny",
    "Roox": "Roox",
    "B211": "B211",
    "Qashqai": "Qashqai",
    "Primera": "Primera",
    "Wingroad": "Wingroad",
    "Nv200": "Nv200",
    "B310": "B310",
    "Datsun": "Datsun",
    "Cilper": "Cilper",
    "Largo": "Largo",
    "Serena": "Serena",
    "E25": "E25",
    "Y10": "Y10",
    "Nv350": "Nv350",
    "Teana": "Teana",
    "Patrol": "Patrol",
    "Note": "Note",
    "D22": "D22",
    "Cedric": "Cedric",
    "Pino": "Pino",
    "Cube": "Cube",
    "Car": "Car",
    "Sylphy": "Sylphy",
    "Lucino": "Lucino",
    "Juke": "Juke",
    "Laurel": "Laurel",
    "Hiace": "Hiace",
    "Avenir": "Avenir",
    "Skyline": "Skyline",
    "Double Cab": "Double Cab",
    "Hb 12": "Hb 12",
    "Elgrand": "Elgrand",
    "Highway Star": "Highway Star",
    "Homy": "Homy",
    "Magnite": "Magnite",
    "Xterra": "Xterra"
  },
  "Perodua": {
    "Viva": "Viva",
    "Elite": "Elite",
    "Axia": "Axia",
    "Kelisa": "Kelisa",
    "Kenari": "Kenari",
    "Bezza": "Bezza",
    "Kancil": "Kancil"
  },
  "Peugeot": {
    "3008": "3008",
    "5008": "5008",
    "307": "307",
    "406": "406",
    "2008": "2008",
    "407": "407",
    "208": "208",
    "206": "206",
    "504": "504",
    "508": "508",
    "505Sr": "505Sr"
  },
  "Porsche": {
    "718 Boxster": "718 Boxster"
  },
  "Proton": {
    "Wira": "Wira",
    "Saga": "Saga",
    "Savvy": "Savvy"
  },
  "Renault": {
    "Kwid": "Kwid",
    "Megane": "Megane"
  },
  "Rover": {
    "Range Rover": "Range Rover"
  },
  "Ssangyong": {
    "Rexton": "Rexton",
    "Tivoli": "Tivoli",
    "Kyron": "Kyron",
    "Korando": "Korando"
  },
  "Subaru": {
    "Sambar": "Sambar",
    "Xv": "Xv",
    "Car": "Car",
    "Chiffon": "Chiffon",
    "Forester": "Forester"
  },
  "Suzuki": {
    "Wagon R": "Wagon R",
    "Alto": "Alto",
    "Every": "Every",
    "Spacia": "Spacia",
    "Maruti": "Maruti",
    "Swift": "Swift",
    "Celerio": "Celerio",
    "Hustler": "Hustler",
    "A Star": "A Star",
    "Baleno": "Baleno",
    "Estilo": "Estilo",
    "Zen": "Zen",
    "Liana": "Liana",
    "S Cross": "S Cross",
    "Vitara": "Vitara",
    "Escudo": "Escudo",
    "Xbee": "Xbee",
    "Cultus": "Cultus",
    "Ignis": "Ignis",
    "Grand Vitara": "Grand Vitara",
    "Sx": "Sx",
    "S Presso": "S Presso",
    "Esteem": "Esteem",
    "Omini": "Omini",
    "Omni": "Omni",
    "Bandit": "Bandit",
    "Van": "Van",
    "Ritz": "Ritz",
    "Ertiga": "Ertiga",
    "Aerio": "Aerio",
    "Mr Wagon": "Mr Wagon",
    "Clipper": "Clipper",
    "Car": "Car",
    "Carry": "Carry",
    "Lapin": "Lapin",
    "Ciaz": "Ciaz"
  },
  "Tata": {
    "Nano": "Nano",
    "Indica": "Indica",
    "Indigo": "Indigo"
  },
  "Tesla": {
    "Model Y": "Model Y",
    "Model 3": "Model 3"
  },
  "Toyota": {
    "4Runner": "Hiace",
    "Ae 111": "Hiace",
    "Ae100": "Hiace",
    "Allion": "Hiace",
    "Alphard": "Hiace",
    "Altezza": "Hiace",
    "Aqua": "Hiace",
    "Auris": "Hiace",
    "Avanza": "Hiace",
    "Axia": "Hiace",
    "Axio": "Hiace",
    "Belta": "Hiace",
    "Caldina": "Hiace",
    "Cami": "Hiace",
    "Camry": "Hiace",
    "Carina": "Hiace",
    "Chr": "Hiace",
    "Commuter": "Hiace",
    "Corolla": "Hiace",
    "Corona": "Hiace",
    "Corsa": "Hiace",
    "Cr27": "Hiace",
    "Crown": "Hiace",
    "Cynos": "Hiace",
    "Duet": "Hiace",
    "Dx Wagon": "Hiace",
    "Emperor": "Hiace",
    "Esquire": "Hiace",
    "Fieder": "Hiace",
    "Fit": "Hiace",
    "Fortuner": "Hiace",
    "Glanza V": "Hiace",
    "Grand Hiace": "Hiace",
    "Harrier": "Hiace",
    "Hiace": "Hiace",
    "Hilux": "Hiace",
    "Ist": "Hiace",
    "Ke72": "Hiace",
    "Kr42": "Hiace",
    "Land Cruiser": "Hiace",
    "Land Cruiser Prado": "Hiace",
    "Lexus": "Hiace",
    "Lh113": "Hiace",
    "Lh30B": "Hiace",
    "Lh40": "Hiace",
    "Liteace": "Hiace",
    "Lotto": "Hiace",
    "Lucida": "Hiace",
    "Marino": "Hiace",
    "Mark Ii": "Hiace",
    "Mark X": "Hiace",
    "Noah": "Hiace",
    "Passo": "Hiace",
    "Pixis": "Hiace",
    "Platz": "Hiace",
    "Premio": "Hiace",
    "Prius": "Hiace",
    "Raize": "Hiace",
    "Raum": "Hiace",
    "Rav4": "Hiace",
    "Regius": "Hiace",
    "Rocco B5": "Hiace",
    "Roomy": "Hiace",
    "Rush": "Hiace",
    "Sai": "Hiace",
    "Sienta": "Hiace",
    "Soluna": "Hiace",
    "Spacio": "Hiace",
    "Sprinter": "Hiace",
    "Starlet": "Hiace",
    "Super Gl": "Hiace",
    "Surf": "Hiace",
    "Tercel": "Hiace",
    "Townace": "Hiace",
    "Toyoace": "Hiace",
    "Van": "Hiace",
    "Vanguard": "Hiace",
    "Vellfire": "Hiace",
    "Verossa": "Hiace",
    "Vios": "Hiace",
    "Vista": "Hiace",
    "Vitz": "Hiace",
    "Voxy": "Hiace",
    "Wigo": "Hiace",
    "Yaris": "Hiace",
    "Yaris Cross": "Hiace"
  },
  "Universal": {
    "Rino": "Rino"
  },
  "Volkswagen": {
    "1300": "1300",
    "Golf": "Golf",
    "Beetle": "Beetle",
    "Jetta": "Jetta",
    "Passat": "Passat",
    "Transporter": "Transporter"
  },
  "Volvo": {
    "S40": "S40"
  },
  "Willys": {
    "Jeep": "Jeep"
  },
  "Zotye": {
    "Z100": "Z100",
    "Nomad": "Nomad"
  }
}