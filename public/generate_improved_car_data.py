# generate_improved_car_data_v2.py
# Paste and run with: python3 generate_improved_car_data_v2.py
import csv
import random

# --- 1. Vehicle List and Accurate Brand Mapping ---
# Note: EV models are explicitly named for accurate fuel mapping.
vehicles = [
    "Swift", "Baleno", "Alto K10", "Wagon R", "Brezza", "Ertiga", "Grand Vitara", "Celerio",
    "Nexon", "Punch", "Harrier", "Safari", "Tiago", "Altroz", "Tiago.ev", "Nexon.ev", # Tata EVs
    "Scorpio-N", "XUV700", "Thar", "Bolero", "XUV300", "XUV400.ev", # Mahindra EV
    "Creta", "i20", "Venue", "Verna", "Exter", "Grand i10 Nios", "Tucson", "IONIQ 5", # Hyundai EV
    "Seltos", "Sonet", "Carens", "Carnival", "EV6", # Kia EV
    "Innova Crysta", "Innova HyCross", "Fortuner", "Glanza", "Urban Cruiser Hyryder", "Camry Hybrid",
    "City", "Amaze", "Elevate", "WR-V",
    "Kwid", "Triber", "Kiger",
    "C-Class", "E-Class", "S-Class", "GLC", "GLE", "EQS", # Mercedes EV
    "3 Series", "5 Series", "X3", "X5", "i4", "i7", "M2", # BMW EVs
    "A4", "A6", "Q3", "Q5", "e-tron GT", # Audi EV
    "XC60", "S90", "C40 Recharge", # Volvo EV
    "Virtus", "Taigun", "Tiguan",
    "Slavia", "Kushaq", "Octavia", "Superb",
    "Hector", "Astor", "ZS EV", "Comet EV", # MG EVs
    "C3", "C3 Aircross", "C5 Aircross",
    "Magnite", "Kicks",
    "Compass", "Meridian", "Wrangler",
    "F-Pace", "I-Pace" # Jaguar EV
]

brand_map = {
    "Maruti Suzuki": ["Swift", "Baleno", "Alto K10", "Wagon R", "Brezza", "Ertiga", "Grand Vitara", "Celerio"],
    "Tata Motors": ["Nexon", "Punch", "Harrier", "Safari", "Tiago", "Altroz", "Tiago.ev", "Nexon.ev"],
    "Mahindra": ["Scorpio-N", "XUV700", "Thar", "Bolero", "XUV300", "XUV400.ev"],
    "Hyundai": ["Creta", "i20", "Venue", "Verna", "Exter", "Grand i10 Nios", "Tucson", "IONIQ 5"],
    "Kia": ["Seltos", "Sonet", "Carens", "Carnival", "EV6"],
    "Toyota": ["Innova Crysta", "Innova HyCross", "Fortuner", "Glanza", "Urban Cruiser Hyryder", "Camry Hybrid"],
    "Honda": ["City", "Amaze", "Elevate", "WR-V"],
    "Renault": ["Kwid", "Triber", "Kiger"],
    "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "EQS"],
    "BMW": ["3 Series", "5 Series", "X3", "X5", "i4", "i7", "M2"],
    "Audi": ["A4", "A6", "Q3", "Q5", "e-tron GT"],
    "Volvo": ["XC60", "S90", "C40 Recharge"],
    "Volkswagen": ["Virtus", "Taigun", "Tiguan"],
    "Škoda": ["Slavia", "Kushaq", "Octavia", "Superb"],
    "MG": ["Hector", "Astor", "ZS EV", "Comet EV"],
    "Citroën": ["C3", "C3 Aircross", "C5 Aircross"],
    "Nissan": ["Magnite", "Kicks"],
    "Jeep": ["Compass", "Meridian", "Wrangler"],
    "Jaguar": ["F-Pace", "I-Pace"]
}

def find_brand(car):
    for brand, lst in brand_map.items():
        if car in lst:
            return brand
    return "Other"

# --- 2. Body Type and Seating Assignment ---
hatchbacks = {"Swift", "Baleno", "Alto K10", "Wagon R", "Celerio", "i20", "Grand i10 Nios", "Kwid", "Altroz", "Tiago", "Comet EV", "C3", "Glanza"}
sedans = {"City", "Verna", "Amaze", "Virtus", "Slavia", "Octavia", "Superb", "A4", "A6", "3 Series", "5 Series", "S90", "C-Class", "E-Class", "S-Class"}
sub_compact_suvs = {"Brezza", "Nexon", "Punch", "Venue", "Sonet", "Kiger", "Magnite", "Exter", "XUV300"}
mpvs = {"Ertiga", "Triber", "Carens", "Carnival", "Innova Crysta", "Innova HyCross"}
coupes = {"M2"}
premium_sedans_evs = {"i4", "i7", "EQS", "e-tron GT"}

def assign_body_and_seats(car):
    if car in hatchbacks:
        return "Hatchback", 5
    elif car in sedans:
        return "Sedan", 5
    elif car in sub_compact_suvs:
        return "Compact SUV", 5
    elif car in mpvs:
        return "MPV", random.choice([6, 7]) # Many are 7, some are 6
    elif car == "Fortuner":
        return "SUV", 7
    elif car in ("Scorpio-N", "XUV700", "Safari", "Meridian", "C5 Aircross", "GLE", "X5", "Q7", "GLC", "X3", "Q5", "XC60"):
        return "SUV", random.choice([5, 7])
    elif car in ("Thar", "Wrangler"):
        return "Off-Road SUV", 4
    elif car in ("EV6", "IONIQ 5", "Camry Hybrid"):
        return "Crossover", 5
    else: # Default to SUV for the rest (Harrier, Tucson, Compass, etc.)
        return "SUV", 5

# --- 3. Fuel Type and Efficiency Assignment ---
# Define specific fuel maps for popular models based on real options
specific_fuel_map = {
    "Alto K10": ["Petrol", "Petrol/CNG"],
    "Wagon R": ["Petrol", "Petrol/CNG"],
    "Swift": ["Petrol", "Petrol/CNG"],
    "Ertiga": ["Petrol", "Petrol/CNG"],
    "Tiago": ["Petrol", "Petrol/CNG"],
    "Exter": ["Petrol", "Petrol/CNG"],
    "Grand i10 Nios": ["Petrol", "Petrol/CNG"],
    "Nexon": ["Petrol", "Diesel"],
    "Harrier": ["Diesel"],
    "Fortuner": ["Petrol", "Diesel"],
    "Innova Crysta": ["Diesel"],
    "City": ["Petrol"],
    "Camry Hybrid": ["Petrol Hybrid"],
    "Grand Vitara": ["Petrol", "Petrol Mild Hybrid", "Petrol Strong Hybrid"],
    "Urban Cruiser Hyryder": ["Petrol", "Petrol Mild Hybrid", "Petrol Strong Hybrid"],
    "Innova HyCross": ["Petrol", "Petrol Strong Hybrid"],
    # All explicit EVs
    "Tiago.ev": ["EV"], "Nexon.ev": ["EV"], "XUV400.ev": ["EV"], "IONIQ 5": ["EV"], "EV6": ["EV"],
    "EQS": ["EV"], "i4": ["EV"], "i7": ["EV"], "e-tron GT": ["EV"], "C40 Recharge": ["EV"],
    "ZS EV": ["EV"], "Comet EV": ["EV"], "I-Pace": ["EV"]
}

def assign_fuel_and_fe(car, body):
    fuel_options = specific_fuel_map.get(car)

    if fuel_options:
        fuel = random.choice(fuel_options)
    else:
        # Default choices based on common practice
        if body in ("Hatchback", "Compact SUV"):
            fuel = random.choice(["Petrol", "Petrol/Diesel"])
        elif body in ("Sedan", "Crossover"):
            fuel = random.choice(["Petrol", "Petrol/Diesel", "Petrol Hybrid"])
        else: # SUV, MPV, Off-Road SUV
            fuel = random.choice(["Petrol", "Diesel"])

    if "EV" in fuel:
        kmpl = ""
    elif "Hybrid" in fuel:
        # High efficiency for hybrids
        kmpl = round(random.uniform(18, 28), 1)
    elif "Diesel" in fuel:
        # Better than petrol for diesel
        kmpl = round(random.uniform(14, 22), 1)
    else: # Petrol / CNG
        if "CNG" in fuel:
            kmpl = round(random.uniform(25, 35), 1) # High value for CNG (km/kg)
        elif body == "Hatchback":
            kmpl = round(random.uniform(18, 25), 1)
        else:
            kmpl = round(random.uniform(12, 18), 1)

    return fuel, kmpl

# --- 4. Price and Attribute Assignment ---
premium_brands = {"Mercedes-Benz", "BMW", "Audi", "Volvo", "Jaguar"}
mid_brands = {"Kia", "Hyundai", "Toyota", "Mahindra", "Volkswagen", "Škoda", "MG", "Jeep"}
mass_brands = {"Maruti Suzuki", "Tata Motors", "Renault", "Nissan", "Citroën"}

def random_between(a, b):
    return random.randint(a, b)

rows = []
for car in vehicles:
    brand = find_brand(car)
    body, seats = assign_body_and_seats(car)
    fuel, fe_value = assign_fuel_and_fe(car, body)

    # Dimensions based on body type (more realistic ranges)
    if body == "Hatchback":
        length = random_between(3400, 3990)
        width = random_between(1600, 1750)
        height = random_between(1480, 1600)
    elif body == "Sedan":
        length = random_between(4400, 5200) # Covers mid to luxury
        width = random_between(1700, 1950)
        height = random_between(1400, 1550)
    elif body == "Compact SUV":
        length = random_between(3900, 4200)
        width = random_between(1700, 1800)
        height = random_between(1600, 1750)
    elif body == "MPV":
        length = random_between(4400, 5000)
        width = random_between(1750, 1900)
        height = random_between(1750, 1900)
    else: # SUV, Crossover, Off-Road SUV (General)
        length = random_between(4300, 5000)
        width = random_between(1780, 2000)
        height = random_between(1600, 1900)

    # Price ranges (in Lakhs INR, Ex-showroom)
    if brand in premium_brands:
        min_price = random_between(45, 90)
        max_price = random_between(95, 250)
    elif brand in mid_brands:
        min_price = random_between(9, 18)
        max_price = random_between(22, 60)
    elif brand in mass_brands:
        min_price = random_between(4, 9)
        max_price = random_between(10, 20)
    else:
        min_price = random_between(6, 15)
        max_price = random_between(18, 60)

    # Ensure max is always greater than min
    if min_price >= max_price:
        max_price = min_price + random_between(3, 40)

    # Other sensible values
    sales = random_between(500, 30000) # Simple volume proxy
    ground_clearance = random_between(150, 240)
    maintenance = random_between(2, 9) # 1 low - 10 high; lower is cheaper
    safety = random.choice([3, 4, 5]) # Use common global NCAP ratings

    # Adjust safety rating for known safe/unsafe models (e.g., Tata, Mahindra usually high; some Maruti/Renault usually average)
    high_safety = ("Nexon", "Punch", "Altroz", "XUV700", "Scorpio-N", "Nexon.ev")
    if car in high_safety:
        safety = random.choice([4, 5])
    elif brand in premium_brands:
        safety = 5
    elif car in ("Kwid", "Alto K10", "Swift"):
         safety = random.choice([3, 4])


    rows.append([
        car,
        brand,
        sales,
        length,
        width,
        height,
        ground_clearance,
        fe_value,
        max_price,
        min_price,
        maintenance,
        safety,
        body,
        fuel,
        seats
    ])

# --- 5. Write CSV File ---
header = ["VehicleName", "Brand name", "Sales", "Length", "Width", "Height", "GroundClearance", "FuelEfficiency", "PriceMostExpensiveVariant", "PriceCheapestVariant", "MaintenanceCost", "SafetyRating", "BodyType", "FuelType", "Seats"]
out_file = "improved_car_data_v2.csv"
with open(out_file, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("Wrote:", out_file)
print("Example (first 8 rows):")
for r in rows[:8]:
    print(r)