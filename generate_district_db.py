import json
import os

# Load official 64 schools database
with open("official_64_schools.json", "r", encoding="utf-8") as sf:
    official_schools = json.load(sf)

# Complete district-level dataset with date-stamped records for reactive filtering
district_data = {
    "Abim": {
        "dates": ["2026-09-08", "2026-09-15", "2026-09-22"],
        "schools": 1, "target_schools": 9, "demos": 8, "target_demos": 90,
        "learners": 820, "target_learners": 14190, "target_enrolled": 17111, "caregivers": 22, "target_caregivers": 7200,
        "teachers_vhts": 22, "pwd_reach": 34,
        "teachers_male": 4, "teachers_female": 4, "headteachers": 1, "patrons": 2,
        "vhts_male": 7, "vhts_female": 7, "vhts_pwd_male": 3, "vhts_pwd_female": 2,
        "exit_interviews": {
            "Teacher 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls", "Fair plate sharing"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will show mothers in our PTA meeting how to add dried cowpea flour to school porridge."},
            "Teacher 2": {"sex": "Male", "lessons": ["Fair plate sharing", "Improved cooking methods", "Hotline 0800"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will ensure boys carry water jerricans in the morning so girls do not come late for math."},
            "Teacher 3": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Nutri Clubs & Hotline"], "action": "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "words": "I committed to running the NutriClub every Tuesday afternoon."},
            "VHT 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls", "Fair plate sharing"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will visit 5 households every week to verify they add wild eboo to morning porridge."},
            "VHT 2": {"sex": "Male", "lessons": ["Chore rebalancing for girls", "Improved cooking methods"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will speak with the village elders to release young girls from early livestock herding."},
            "VHT 3": {"sex": "Male", "lessons": ["Rebalancing morning water/wood chores so girls stay in school", "Establishing Nutri Clubs, Nutri-Moments, or using WFP 0800 Hotline"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will organize village kraal meetings to ensure fathers assign morning borehole chores to boys, and share the 0800 toll-free number."}
        },
        "v1": {"active": 1, "days": {"Tue": 1, "Thu": 1}, "plan": 1, "charts": 260, "tollfree": 1, "att_m": 180, "att_f": 170},
        "v2": {"hc_lower_m": 115, "hc_lower_f": 110, "hc_mid_m": 110, "hc_mid_f": 105, "hc_up_m": 95, "hc_up_f": 90, "teachers_m": 4, "teachers_f": 4, "comm_m": 7, "comm_f": 16, "pwd_m": 10, "pwd_f": 9},
        "v3": {"charts_issued": 260, "charts_returned": 228, "joint_comp": 204, "feedback_tried": 184, "feedback_help": 32, "feedback_not": 12, "barriers": {"Firewood": 10, "Water": 8, "Ingredients": 6, "Chores": 4, "Disagreement": 2}, "stoves_verified": 1},
        "demos_metrics": {"caregivers": 22, "fathers": 8, "boys": 34, "girls": 38, "pwd_m": 3, "pwd_f": 2, "handson": 7, "passive": 1, "fuelsaving": 7, "barriers": {"Money": 8, "Water": 6, "Missing items": 4, "Firewood": 3, "Chores": 1}, "commitments": {"Will try": 18, "Need VHT": 3, "Not possible": 1}}
    },
    "Amudat": {
        "dates": ["2026-09-07", "2026-09-14", "2026-09-21"],
        "schools": 1, "target_schools": 5, "demos": 7, "target_demos": 50,
        "learners": 760, "target_learners": 3600, "target_enrolled": 6655, "caregivers": 20, "target_caregivers": 4000,
        "teachers_vhts": 20, "pwd_reach": 31,
        "teachers_male": 4, "teachers_female": 3, "headteachers": 1, "patrons": 2,
        "vhts_male": 6, "vhts_female": 7, "vhts_pwd_male": 3, "vhts_pwd_female": 2,
        "exit_interviews": {
            "Teacher 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will make sure pupils understand that wild green vegetables give strength to study."},
            "Teacher 2": {"sex": "Male", "lessons": ["Chore rebalancing for girls", "Improved cooking methods"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "Boys must fetch water from the borehole so that their sisters are not late and whipped."},
            "Teacher 3": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Fair plate sharing", "Hotline 0800"], "action": "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "words": "I will inspect our school kitchen to ensure the cook covers the porridge pot."},
            "VHT 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Fair plate sharing"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will demonstrate crushing roasted sesame into morning porridge for weaning infants."},
            "VHT 2": {"sex": "Male", "lessons": ["Improved cooking methods", "Chore rebalancing for girls"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will encourage pastoral fathers to let boys take shifts at the water point."},
            "VHT 3": {"sex": "Female", "lessons": ["Preparing/enriching WFP Metu porridge with local wild greens/staples", "Rebalancing morning water/wood chores so girls stay in school"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will train mothers in Karita on crushing cowpeas and drying seasonal greens for porridge."}
        },
        "v1": {"active": 1, "days": {"Thu": 1, "Fri": 1}, "plan": 1, "charts": 240, "tollfree": 1, "att_m": 170, "att_f": 160},
        "v2": {"hc_lower_m": 105, "hc_lower_f": 100, "hc_mid_m": 100, "hc_mid_f": 95, "hc_up_m": 90, "hc_up_f": 85, "teachers_m": 4, "teachers_f": 3, "comm_m": 6, "comm_f": 15, "pwd_m": 9, "pwd_f": 8},
        "v3": {"charts_issued": 240, "charts_returned": 204, "joint_comp": 182, "feedback_tried": 165, "feedback_help": 28, "feedback_not": 11, "barriers": {"Firewood": 9, "Water": 7, "Ingredients": 5, "Chores": 4, "Disagreement": 2}, "stoves_verified": 1},
        "demos_metrics": {"caregivers": 20, "fathers": 7, "boys": 31, "girls": 35, "pwd_m": 2, "pwd_f": 2, "handson": 6, "passive": 1, "fuelsaving": 6, "barriers": {"Money": 7, "Water": 5, "Missing items": 3, "Firewood": 3, "Chores": 1}, "commitments": {"Will try": 16, "Need VHT": 3, "Not possible": 1}}
    },
    "Kaabong": {
        "dates": ["2026-09-09", "2026-09-16", "2026-09-24"],
        "schools": 1, "target_schools": 13, "demos": 8, "target_demos": 130,
        "learners": 890, "target_learners": 16378, "target_enrolled": 25225, "caregivers": 24, "target_caregivers": 10400,
        "teachers_vhts": 24, "pwd_reach": 36,
        "teachers_male": 5, "teachers_female": 4, "headteachers": 1, "patrons": 2,
        "vhts_male": 7, "vhts_female": 8, "vhts_pwd_male": 3, "vhts_pwd_female": 3,
        "exit_interviews": {
            "Teacher 1": {"sex": "Male", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls", "Fair plate sharing"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will register attendance every morning at 7:45 AM and follow up on late girls."},
            "Teacher 2": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Nutri Clubs & Hotline"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "We have established a school vegetable garden to supply cowpeas for NutriClub demos."},
            "Teacher 3": {"sex": "Male", "lessons": ["Improved cooking methods", "Chore rebalancing for girls"], "action": "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "words": "I will train pupils on fuel-efficient cooking and putting lids on pots."},
            "VHT 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Fair plate sharing", "Hotline 0800"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will teach young mothers to forage safe eboo and sun-dry it for the dry season."},
            "VHT 2": {"sex": "Male", "lessons": ["Chore rebalancing for girls", "Fair plate sharing"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "Elder men must be reminded that daughters also need rest and full bellies to grow."},
            "VHT 3": {"sex": "Male", "lessons": ["Rebalancing morning water/wood chores so girls stay in school", "Fair and equal plate sharing between boys and girls at home", "Using improved cooking methods to consume less firewood"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will mobilize household heads across Kalapata so young girls are not pulled out of class for firewood collection."}
        },
        "v1": {"active": 1, "days": {"Tue": 1, "Thu": 1}, "plan": 1, "charts": 290, "tollfree": 1, "att_m": 195, "att_f": 185},
        "v2": {"hc_lower_m": 125, "hc_lower_f": 120, "hc_mid_m": 120, "hc_mid_f": 115, "hc_up_m": 105, "hc_up_f": 100, "teachers_m": 5, "teachers_f": 4, "comm_m": 8, "comm_f": 18, "pwd_m": 11, "pwd_f": 10},
        "v3": {"charts_issued": 290, "charts_returned": 252, "joint_comp": 224, "feedback_tried": 204, "feedback_help": 35, "feedback_not": 13, "barriers": {"Firewood": 11, "Water": 9, "Ingredients": 7, "Chores": 4, "Disagreement": 2}, "stoves_verified": 1},
        "demos_metrics": {"caregivers": 24, "fathers": 9, "boys": 38, "girls": 42, "pwd_m": 3, "pwd_f": 3, "handson": 7, "passive": 1, "fuelsaving": 7, "barriers": {"Money": 9, "Water": 6, "Missing items": 4, "Firewood": 3, "Chores": 2}, "commitments": {"Will try": 20, "Need VHT": 3, "Not possible": 1}}
    },
    "Kotido": {
        "dates": ["2026-09-10", "2026-09-17"],
        "schools": 0, "target_schools": 12, "demos": 5, "target_demos": 120,
        "learners": 480, "target_learners": 17211, "target_enrolled": 27441, "caregivers": 15, "target_caregivers": 9600,
        "teachers_vhts": 14, "pwd_reach": 22,
        "teachers_male": 0, "teachers_female": 0, "headteachers": 0, "patrons": 0,
        "vhts_male": 7, "vhts_female": 7, "vhts_pwd_male": 2, "vhts_pwd_female": 2,
        "exit_interviews": {
            "Teacher 1": {"sex": "Female", "lessons": ["Preparing/enriching WFP Metu porridge with local wild greens/staples", "Chore rebalancing for girls"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will educate parents during assembly on adding dry cowpea leaf flour to child porridge."},
            "Teacher 2": {"sex": "Male", "lessons": ["Chore rebalancing for girls", "Improved cooking methods"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "Boys must participate in morning chores so their sisters can arrive before classes commence."},
            "Teacher 3": {"sex": "Female", "lessons": ["Fair plate sharing", "Hotline 0800"], "action": "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "words": "We are organizing our NutriClub to practice energy-efficient stove operations."},
            "VHT 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "Community demonstration site mobilized for porridge enrichment."},
            "VHT 2": {"sex": "Male", "lessons": ["Improved cooking methods", "Chore rebalancing for girls"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "Chore sharing promoted in catchment villages."},
            "VHT 3": {"sex": "Female", "lessons": ["Preparing/enriching WFP Metu porridge with local wild greens/staples", "Using improved cooking methods to consume less firewood"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will conduct home visits to demonstrate fuel-saving covered cooking pots."}
        },
        "v1": {"active": 0, "days": {}, "plan": 0, "charts": 0, "tollfree": 0, "att_m": 0, "att_f": 0},
        "v2": {"hc_lower_m": 0, "hc_lower_f": 0, "hc_mid_m": 0, "hc_mid_f": 0, "hc_up_m": 0, "hc_up_f": 0, "teachers_m": 0, "teachers_f": 0, "comm_m": 0, "comm_f": 0, "pwd_m": 0, "pwd_f": 0},
        "v3": {"charts_issued": 0, "charts_returned": 0, "joint_comp": 0, "feedback_tried": 0, "feedback_help": 0, "feedback_not": 0, "barriers": {}, "stoves_verified": 0},
        "demos_metrics": {"caregivers": 15, "fathers": 5, "boys": 21, "girls": 24, "pwd_m": 2, "pwd_f": 2, "handson": 5, "passive": 0, "fuelsaving": 5, "barriers": {"Money": 5, "Water": 4, "Missing items": 2, "Firewood": 2, "Chores": 1}, "commitments": {"Will try": 13, "Need VHT": 2, "Not possible": 0}}
    },
    "Moroto": {
        "dates": ["2026-09-06", "2026-09-13", "2026-09-22"],
        "schools": 1, "target_schools": 5, "demos": 9, "target_demos": 50,
        "learners": 950, "target_learners": 5545, "target_enrolled": 9956, "caregivers": 28, "target_caregivers": 4000,
        "teachers_vhts": 25, "pwd_reach": 42,
        "teachers_male": 5, "teachers_female": 4, "headteachers": 1, "patrons": 2,
        "vhts_male": 8, "vhts_female": 8, "vhts_pwd_male": 4, "vhts_pwd_female": 3,
        "exit_interviews": {
            "Teacher 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls", "Fair plate sharing"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will mobilize boys in my class to share water fetching so sisters are not locked out."},
            "Teacher 2": {"sex": "Male", "lessons": ["Fair plate sharing", "Improved cooking methods", "Hotline 0800"], "action": "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "words": "I will personally check that the cook maintains the firewood-saving stove daily."},
            "Teacher 3": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Nutri Clubs & Hotline"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will conduct porridge tasting during our Friday NutriClub assembly."},
            "VHT 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Fair plate sharing"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will teach caregivers in Manyattas how to grind dried wild greens into baby food."},
            "VHT 2": {"sex": "Male", "lessons": ["Chore rebalancing for girls", "Improved cooking methods"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will address kraal leaders on the benefits of girls attending classes punctually."},
            "VHT 3": {"sex": "Male", "lessons": ["Rebalancing morning water/wood chores so girls stay in school", "Fair and equal plate sharing between boys and girls at home", "Establishing Nutri Clubs, Nutri-Moments, or using WFP 0800 Hotline"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will work with traditional leaders in Nadunget to rebalance morning water chores and promote the 0800 toll-free line."}
        },
        "v1": {"active": 1, "days": {"Tue": 1, "Thu": 1, "Fri": 1}, "plan": 1, "charts": 310, "tollfree": 1, "att_m": 210, "att_f": 200},
        "v2": {"hc_lower_m": 135, "hc_lower_f": 130, "hc_mid_m": 130, "hc_mid_f": 125, "hc_up_m": 115, "hc_up_f": 110, "teachers_m": 5, "teachers_f": 4, "comm_m": 9, "comm_f": 20, "pwd_m": 13, "pwd_f": 12},
        "v3": {"charts_issued": 310, "charts_returned": 272, "joint_comp": 242, "feedback_tried": 220, "feedback_help": 38, "feedback_not": 14, "barriers": {"Firewood": 12, "Water": 10, "Ingredients": 7, "Chores": 5, "Disagreement": 2}, "stoves_verified": 1},
        "demos_metrics": {"caregivers": 28, "fathers": 10, "boys": 42, "girls": 46, "pwd_m": 4, "pwd_f": 3, "handson": 8, "passive": 1, "fuelsaving": 8, "barriers": {"Money": 10, "Water": 7, "Missing items": 5, "Firewood": 3, "Chores": 2}, "commitments": {"Will try": 23, "Need VHT": 4, "Not possible": 1}}
    },
    "Nabilatuk": {
        "dates": ["2026-09-08", "2026-09-17", "2026-09-25"],
        "schools": 1, "target_schools": 5, "demos": 9, "target_demos": 50,
        "learners": 810, "target_learners": 5510, "target_enrolled": 9569, "caregivers": 24, "target_caregivers": 4000,
        "teachers_vhts": 22, "pwd_reach": 35,
        "teachers_male": 4, "teachers_female": 4, "headteachers": 1, "patrons": 2,
        "vhts_male": 7, "vhts_female": 7, "vhts_pwd_male": 3, "vhts_pwd_female": 3,
        "exit_interviews": {
            "Teacher 1": {"sex": "Male", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "Boys volunteered in front of assembly to do morning sweeping and water chores."},
            "Teacher 2": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Fair plate sharing"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will encourage parents to bring greens to school on porridge cooking days."},
            "Teacher 3": {"sex": "Male", "lessons": ["Improved cooking methods", "Hotline 0800"], "action": "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "words": "We posted the toll-free board on the main office door for anyone with questions."},
            "VHT 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Fair plate sharing"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "We will show mothers how to enrich Metu rations with locally grown cowpea leaves."},
            "VHT 2": {"sex": "Male", "lessons": ["Chore rebalancing for girls", "Improved cooking methods"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "We have agreed that the youngest child must receive the first warm cup of porridge."},
            "VHT 3": {"sex": "Female", "lessons": ["Preparing/enriching WFP Metu porridge with local wild greens/staples", "Fair and equal plate sharing between boys and girls at home"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will verify in community gatherings that the youngest child is served their nutritious cup of porridge first."}
        },
        "v1": {"active": 1, "days": {"Tue": 1, "Thu": 1}, "plan": 1, "charts": 270, "tollfree": 1, "att_m": 185, "att_f": 175},
        "v2": {"hc_lower_m": 115, "hc_lower_f": 110, "hc_mid_m": 110, "hc_mid_f": 105, "hc_up_m": 100, "hc_up_f": 95, "teachers_m": 4, "teachers_f": 4, "comm_m": 7, "comm_f": 17, "pwd_m": 11, "pwd_f": 10},
        "v3": {"charts_issued": 270, "charts_returned": 234, "joint_comp": 208, "feedback_tried": 190, "feedback_help": 32, "feedback_not": 12, "barriers": {"Firewood": 10, "Water": 8, "Ingredients": 6, "Chores": 4, "Disagreement": 2}, "stoves_verified": 1},
        "demos_metrics": {"caregivers": 24, "fathers": 9, "boys": 35, "girls": 39, "pwd_m": 3, "pwd_f": 3, "handson": 8, "passive": 1, "fuelsaving": 8, "barriers": {"Money": 8, "Water": 6, "Missing items": 4, "Firewood": 3, "Chores": 2}, "commitments": {"Will try": 20, "Need VHT": 3, "Not possible": 1}}
    },
    "Nakapiripirit": {
        "dates": ["2026-09-05", "2026-09-12", "2026-09-20"],
        "schools": 1, "target_schools": 5, "demos": 8, "target_demos": 50,
        "learners": 730, "target_learners": 6061, "target_enrolled": 8749, "caregivers": 18, "target_caregivers": 4000,
        "teachers_vhts": 20, "pwd_reach": 28,
        "teachers_male": 4, "teachers_female": 3, "headteachers": 1, "patrons": 2,
        "vhts_male": 6, "vhts_female": 7, "vhts_pwd_male": 2, "vhts_pwd_female": 2,
        "exit_interviews": {
            "Teacher 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "Pupils were excited to learn about adding greens to porridge without changing color."},
            "Teacher 2": {"sex": "Male", "lessons": ["Chore rebalancing for girls", "Improved cooking methods"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will monitor girl attendance in morning class and visit homes of latecomers."},
            "Teacher 3": {"sex": "Female", "lessons": ["Fair plate sharing", "Hotline 0800"], "action": "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "words": "NutriClub meets every Thursday to practice porridge preparation."},
            "VHT 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Fair plate sharing"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I demonstrated drying eboo under shade so vitamins are not destroyed by direct sun."},
            "VHT 2": {"sex": "Male", "lessons": ["Improved cooking methods", "Chore rebalancing for girls"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "Elder council confirmed support for balanced chore division between boys and girls."},
            "VHT 3": {"sex": "Male", "lessons": ["Rebalancing morning water/wood chores so girls stay in school", "Using improved cooking methods to consume less firewood"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will engage elder councils in Lemusui so sons fetch morning water, allowing girls to reach school before 8:00 AM."}
        },
        "v1": {"active": 1, "days": {"Thu": 1, "Fri": 1}, "plan": 1, "charts": 230, "tollfree": 1, "att_m": 160, "att_f": 150},
        "v2": {"hc_lower_m": 105, "hc_lower_f": 100, "hc_mid_m": 100, "hc_mid_f": 95, "hc_up_m": 90, "hc_up_f": 85, "teachers_m": 4, "teachers_f": 3, "comm_m": 6, "comm_f": 15, "pwd_m": 9, "pwd_f": 8},
        "v3": {"charts_issued": 230, "charts_returned": 196, "joint_comp": 174, "feedback_tried": 160, "feedback_help": 26, "feedback_not": 10, "barriers": {"Firewood": 9, "Water": 7, "Ingredients": 5, "Chores": 3, "Disagreement": 1}, "stoves_verified": 1},
        "demos_metrics": {"caregivers": 18, "fathers": 6, "boys": 30, "girls": 33, "pwd_m": 2, "pwd_f": 2, "handson": 7, "passive": 1, "fuelsaving": 7, "barriers": {"Money": 7, "Water": 5, "Missing items": 3, "Firewood": 2, "Chores": 1}, "commitments": {"Will try": 15, "Need VHT": 2, "Not possible": 1}}
    },
    "Napak": {
        "dates": ["2026-09-11", "2026-09-18"],
        "schools": 0, "target_schools": 5, "demos": 3, "target_demos": 50,
        "learners": 210, "target_learners": 4942, "target_enrolled": 6459, "caregivers": 8, "target_caregivers": 4000,
        "teachers_vhts": 8, "pwd_reach": 11,
        "teachers_male": 0, "teachers_female": 0, "headteachers": 0, "patrons": 0,
        "vhts_male": 4, "vhts_female": 4, "vhts_pwd_male": 1, "vhts_pwd_female": 1,
        "exit_interviews": {
            "Teacher 1": {"sex": "Male", "lessons": ["Preparing/enriching WFP Metu porridge with local wild greens/staples", "Chore rebalancing for girls"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will show mothers in our school meetings how to enrich rations with wild greens."},
            "Teacher 2": {"sex": "Female", "lessons": ["Fair plate sharing", "Hotline 0800"], "action": "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "words": "We will display the WFP toll-free hotline board clearly on the staffroom veranda."},
            "Teacher 3": {"sex": "Male", "lessons": ["Chore rebalancing for girls", "Improved cooking methods"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will follow up on boys fetching water so sisters arrive in class on time."},
            "VHT 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "Community demonstration site mobilized for porridge enrichment."},
            "VHT 2": {"sex": "Male", "lessons": ["Improved cooking methods", "Chore rebalancing for girls"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "Chore sharing promoted in catchment villages."},
            "VHT 3": {"sex": "Female", "lessons": ["Preparing/enriching WFP Metu porridge with local wild greens/staples", "Establishing Nutri Clubs, Nutri-Moments, or using WFP 0800 Hotline"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will support VHT community cooking sessions with wild greens and encourage community feedback via 0800."}
        },
        "v1": {"active": 0, "days": {}, "plan": 0, "charts": 0, "tollfree": 0, "att_m": 0, "att_f": 0},
        "v2": {"hc_lower_m": 0, "hc_lower_f": 0, "hc_mid_m": 0, "hc_mid_f": 0, "hc_up_m": 0, "hc_up_f": 0, "teachers_m": 0, "teachers_f": 0, "comm_m": 0, "comm_f": 0, "pwd_m": 0, "pwd_f": 0},
        "v3": {"charts_issued": 0, "charts_returned": 0, "joint_comp": 0, "feedback_tried": 0, "feedback_help": 0, "feedback_not": 0, "barriers": {}, "stoves_verified": 0},
        "demos_metrics": {"caregivers": 8, "fathers": 3, "boys": 12, "girls": 14, "pwd_m": 1, "pwd_f": 1, "handson": 3, "passive": 0, "fuelsaving": 3, "barriers": {"Money": 3, "Water": 2, "Missing items": 1, "Firewood": 1, "Chores": 0}, "commitments": {"Will try": 7, "Need VHT": 1, "Not possible": 0}}
    },
    "Karenga": {
        "dates": ["2026-09-12", "2026-09-19"],
        "schools": 0, "target_schools": 5, "demos": 3, "target_demos": 50,
        "learners": 190, "target_learners": 7438, "target_enrolled": 9521, "caregivers": 6, "target_caregivers": 4000,
        "teachers_vhts": 8, "pwd_reach": 9,
        "teachers_male": 0, "teachers_female": 0, "headteachers": 0, "patrons": 0,
        "vhts_male": 4, "vhts_female": 4, "vhts_pwd_male": 1, "vhts_pwd_female": 1,
        "exit_interviews": {
            "Teacher 1": {"sex": "Female", "lessons": ["Preparing/enriching WFP Metu porridge with local wild greens/staples", "Chore rebalancing for girls"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "I will lead our school NutriClub in identifying safe local wild greens for porridge."},
            "Teacher 2": {"sex": "Male", "lessons": ["Chore rebalancing for girls", "Improved cooking methods"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will encourage boys to relieve sisters from morning firewood tasks."},
            "Teacher 3": {"sex": "Female", "lessons": ["Fair plate sharing", "Hotline 0800"], "action": "Adopt firewood-saving practices in school kitchen / establish Nutri Club", "words": "We will ensure cooks cover cooking pots tightly to conserve school firewood."},
            "VHT 1": {"sex": "Female", "lessons": ["Metu porridge with wild greens", "Chore rebalancing for girls"], "action": "Enrich school/home porridge with obtainable local greens or cowpeas", "words": "Community demonstration site mobilized for porridge enrichment."},
            "VHT 2": {"sex": "Male", "lessons": ["Improved cooking methods", "Chore rebalancing for girls"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "Chore sharing promoted in catchment villages."},
            "VHT 3": {"sex": "Male", "lessons": ["Rebalancing morning water/wood chores so girls stay in school", "Fair and equal plate sharing between boys and girls at home"], "action": "Mobilize boys/fathers to share water/wood chores so girls arrive on time", "words": "I will mobilize boys in Kocholo to fetch domestic firewood and water so girls remain in class."}
        },
        "v1": {"active": 0, "days": {}, "plan": 0, "charts": 0, "tollfree": 0, "att_m": 0, "att_f": 0},
        "v2": {"hc_lower_m": 0, "hc_lower_f": 0, "hc_mid_m": 0, "hc_mid_f": 0, "hc_up_m": 0, "hc_up_f": 0, "teachers_m": 0, "teachers_f": 0, "comm_m": 0, "comm_f": 0, "pwd_m": 0, "pwd_f": 0},
        "v3": {"charts_issued": 0, "charts_returned": 0, "joint_comp": 0, "feedback_tried": 0, "feedback_help": 0, "feedback_not": 0, "barriers": {}, "stoves_verified": 0},
        "demos_metrics": {"caregivers": 6, "fathers": 2, "boys": 11, "girls": 13, "pwd_m": 1, "pwd_f": 1, "handson": 3, "passive": 0, "fuelsaving": 3, "barriers": {"Money": 2, "Water": 2, "Missing items": 1, "Firewood": 1, "Chores": 0}, "commitments": {"Will try": 5, "Need VHT": 1, "Not possible": 0}}
    }
}

# Attach official schools list per district
for dName in district_data:
    district_schools = [s for s in official_schools if s.get("district", "").strip().lower() == dName.lower()]
    district_data[dName]["schools_list"] = district_schools

with open("dashboard_district_db.json", "w", encoding="utf-8") as f:
    json.dump(district_data, f, indent=2)

print(f"Saved dashboard_district_db.json successfully with {len(district_data)} districts and attached official schools.")
