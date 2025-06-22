import random
from datetime import datetime, timedelta

# --- Imports from our application ---
# These imports work because seed.py, database.py, and models.py
# are all in the same 'backend' directory.
from database import SessionLocal, engine
from models import Hiring, BusinessSummary, Base

# --- CONFIGURATION ---
# The database file is implicitly defined by our main application's database.py
# No need to redefine DATABASE_URL here.

# --- Business Rules and Ranges ---
BUSINESSES = {
    "Energy": 30000, "FMCG": 200000, "Tech": 100000, "Media": 5000
}
FUNCTIONS = {
    "Sales": 0.30, "Marketing": 0.15, "HR": 0.10, "Finance": 0.10,
    "Procurement": 0.10, "Legal": 0.05, "Others": 0.20
}
KPI_RANGES = {
    "Tech": {
        "Sales": {"time_to_fill": (60, 110), "cost_per_hire": (50000, 85000)},
        "Marketing": {"time_to_fill": (75, 120), "cost_per_hire": (55000, 90000)},
        "Others": {"time_to_fill": (70, 130), "cost_per_hire": (40000, 70000)},
        "Legal": {"time_to_fill": (100, 180),"cost_per_hire": (80000, 150000)},
    }, "FMCG": {
        "Sales": {"time_to_fill": (45, 80),  "cost_per_hire": (35000, 60000)},
        "Marketing": {"time_to_fill": (60, 95),  "cost_per_hire": (40000, 70000)},
    }, "Energy": {
        "Legal": {"time_to_fill": (110, 190),"cost_per_hire": (90000, 160000)},
    }, "default": {"default": {"time_to_fill": (70, 130), "cost_per_hire": (30000, 70000)}}
}
BUSINESS_SOURCE_MIX = {
    "Tech": { "default": {"Referral": 0.50, "Agency": 0.30, "Portal": 0.15, "Internal": 0.05} },
    "FMCG": { "default": {"Portal": 0.50, "Campus": 0.20, "Agency": 0.15, "Referral": 0.10} },
    "default": { "default": {"Portal": 0.50, "Agency": 0.20, "Referral": 0.15, "Internal": 0.05} }
}
ROLE_TITLES = {
    "Sales": ["Account Executive", "Sales Development Rep", "Regional Sales Manager"],
    "Marketing": ["Digital Marketing Specialist", "Content Strategist", "Brand Manager"],
    "HR": ["HR Business Partner", "Talent Acquisition Specialist", "HR Generalist"],
    "Finance": ["Financial Analyst", "Accountant", "Controller"],
    "Procurement": ["Procurement Officer", "Category Manager", "Sourcing Specialist"],
    "Legal": ["Corporate Counsel", "Paralegal", "Compliance Officer"],
    "Others": ["Data Scientist", "Software Engineer", "Product Manager", "DevOps Engineer"]
}
BUSINESS_PERSONALITY = {
    "Tech": {"ijp_prob": 0.75, "build_prob": 0.65, "diversity_prob": 0.35},
    "FMCG": {"ijp_prob": 0.95, "build_prob": 0.40, "diversity_prob": 0.25},
    "Energy": {"ijp_prob": 0.85, "build_prob": 0.55, "diversity_prob": 0.20},
    "Media": {"ijp_prob": 0.90, "build_prob": 0.50, "diversity_prob": 0.30},
}

# --- Helper Functions ---
def choose_source(business, function):
    business_mix = BUSINESS_SOURCE_MIX.get(business, BUSINESS_SOURCE_MIX["default"])
    sources = business_mix.get(function, business_mix.get("default", {}))
    r = random.random()
    cumulative = 0
    for source, prob in sources.items():
        cumulative += prob
        if r <= cumulative: return source
    return list(sources.keys())[-1] if sources else "Unknown"

def generate_seasonal_date(start_date, end_date):
    total_days = (end_date - start_date).days
    day_offset = random.randint(0, total_days)
    return start_date + timedelta(days=day_offset)

# --- Main Seeding Function ---
def seed_database():
    # We now get the database session from our imported SessionLocal factory
    db = SessionLocal()
    print("Database session started.")
    try:
        print("Clearing existing data...")
        db.query(Hiring).delete()
        db.query(BusinessSummary).delete()
        db.commit()

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)
        total_days_in_year = (end_date - start_date).days

        hirings_to_add = []
        summaries_to_add = []
        outlier_injection_done = False

        print("Generating new data with trends, outliers, and correct summaries...")

        for business, headcount in BUSINESSES.items():
            business_total = headcount
            business_available = int(business_total * random.uniform(0.85, 0.95))
            business_gap = business_total - business_available
            overall_summary = BusinessSummary(
                business_group=business, function='Overall', total_headcount=business_total,
                available_headcount=business_available, gap=business_gap
            )
            summaries_to_add.append(overall_summary)

            total_hires = int(headcount * random.uniform(0.08, 0.12))
            print(f"\n--- Processing: {business} - Simulating {total_hires:,} Hires ---")

            personality = BUSINESS_PERSONALITY.get(business, list(BUSINESS_PERSONALITY.values())[0])

            running_total, running_available, running_gap = 0, 0, 0
            func_items = list(FUNCTIONS.items())

            for i, (function, weight) in enumerate(func_items):
                if i < len(func_items) - 1:
                    func_total = int(business_total * weight)
                    func_available = int(business_available * weight)
                    func_gap = int(business_gap * weight)
                else:
                    func_total = business_total - running_total
                    func_available = business_available - running_available
                    func_gap = business_gap - running_gap

                func_summary = BusinessSummary(
                    business_group=business, function=function, total_headcount=func_total,
                    available_headcount=func_available, gap=func_gap
                )
                summaries_to_add.append(func_summary)

                running_total += func_total
                running_available += func_available
                running_gap += func_gap

                hires_for_function = int(total_hires * weight)
                if hires_for_function == 0: continue

                kpi_config = KPI_RANGES.get(business, {}).get(function, KPI_RANGES["default"]["default"])

                for _ in range(hires_for_function):
                    hire_date = generate_seasonal_date(start_date, end_date)
                    cost_per_hire = random.randint(*kpi_config["cost_per_hire"])
                    time_to_fill = random.randint(*kpi_config["time_to_fill"])

                    if business == "Tech":
                        days_into_year = (hire_date - start_date).days
                        trend_factor = 1 + (days_into_year / total_days_in_year) * 0.5
                        time_to_fill = int(time_to_fill * trend_factor)

                    if business == "Energy" and function == "Legal" and not outlier_injection_done:
                        cost_per_hire *= 3
                        outlier_injection_done = True

                    role_title = random.choice(ROLE_TITLES.get(function, ["General Staff"]))

                    new_hire = Hiring(
                        business_group=business, function=function, role_title=role_title,
                        hire_date=hire_date, cost_per_hire=cost_per_hire, time_to_fill=time_to_fill,
                        ijp_adherence=(random.random() < personality["ijp_prob"]),
                        build_buy_ratio="Build" if (random.random() < personality["build_prob"]) else "Buy",
                        diversity_ratio=(random.random() < personality["diversity_prob"]),
                        source=choose_source(business, function)
                    )
                    hirings_to_add.append(new_hire)

        print("\nAdding generated data to the session...")
        db.add_all(summaries_to_add)
        db.add_all(hirings_to_add)
        db.commit()
        print("Data committed to the database successfully.")
        print(f"\n✅ Seeded {len(hirings_to_add)} hiring records and {len(summaries_to_add)} summary records.")

    except Exception as e:
        print(f"\n[!] An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    print("Running database seeder...")
    # This ensures the tables are created before we try to add data to them.
    # It uses the Base and engine we imported from our application's modules.
    print("Ensuring tables exist...")
    Base.metadata.create_all(bind=engine)
    seed_database()