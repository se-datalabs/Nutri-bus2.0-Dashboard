import json
import random

def generate_demo_sessions():
    with open('dashboard_district_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    random.seed(42)  # Deterministic seed for consistent reproducible data

    venue_types = [
        'Community Kraal Shade',
        'Borehole & Water Point Area',
        'Trading Centre Shade',
        'Market Place Gathering Ground',
        'Village Council Tree',
        'Sub-county Boma Shade',
        'Parish Chapel Compound',
        'Manyatta Gathering Centre',
        'Health Centre Outreach Shade',
        'Boma Community Ground'
    ]

    facilitators = [
        'VHT Team',
        'VHT Team',
        'VHT Team',
        'Lead Coordinator',
        'Field Nutritionist & VHT'
    ]

    all_demos = []
    demo_id_counter = 1

    # Campaign dates in September 2026
    base_dates = [f'2026-09-{d:02d}' for d in range(8, 26)]

    for dist_name, dist_info in db.items():
        schools = dist_info.get('schools_list', [])
        for sch_idx, sch in enumerate(schools):
            sch_name = sch['name']
            subcounty = sch.get('subcounty', dist_name)
            
            for sess_no in range(1, 11):
                sess_id = f'DEMO-{demo_id_counter:03d}'
                demo_id_counter += 1
                
                # Venue
                venue_type = venue_types[(sess_no - 1) % len(venue_types)]
                clean_sch = sch_name.replace(' P/S', '').replace(' PRIMARY SCHOOL', '').strip().title()
                site_name = f"{clean_sch} {venue_type}"
                
                # Date
                date_val = base_dates[(sch_idx * 2 + sess_no) % len(base_dates)]
                
                # Facilitator
                fac = facilitators[(sch_idx + sess_no) % len(facilitators)]
                
                # Decide if compliant or flagged (approx 18% flagged < 80)
                is_flagged = random.random() < 0.18
                
                if is_flagged:
                    # Total between 58 and 78
                    total = random.randint(58, 78)
                    caregivers = int(total * random.uniform(0.50, 0.58))
                    elders = int(total * random.uniform(0.10, 0.15))
                    children = total - caregivers - elders
                    pwd = random.randint(1, 4)
                    status = '🚩 Flagged (<80)'
                else:
                    # Total between 80 and 115
                    total = random.randint(80, 115)
                    caregivers = int(total * random.uniform(0.50, 0.58))
                    elders = int(total * random.uniform(0.12, 0.18))
                    children = total - caregivers - elders
                    pwd = random.randint(3, 7)
                    status = '✅ Compliant (≥80)'
                    
                demo_obj = {
                    'id': sess_id,
                    'session_no': sess_no,
                    'district': dist_name,
                    'subcounty': subcounty,
                    'school': sch_name,
                    'site': site_name,
                    'date': date_val,
                    'facilitator': fac,
                    'caregivers': caregivers,
                    'elders': elders,
                    'children': children,
                    'pwd': pwd,
                    'total': total,
                    'flagged': is_flagged,
                    'status': status
                }
                all_demos.append(demo_obj)

    with open('dashboard_demo_sessions_640.json', 'w', encoding='utf-8') as out_f:
        json.dump(all_demos, out_f, indent=2)

    print(f"Successfully generated {len(all_demos)} demo sessions into dashboard_demo_sessions_640.json")

if __name__ == '__main__':
    generate_demo_sessions()
