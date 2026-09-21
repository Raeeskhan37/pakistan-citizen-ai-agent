from config.departments import DEPARTMENTS


URDU_DEPARTMENT_TERMS = {
    "NADRA": [
        "نادرا",
        "شناختی کارڈ",
        "شناختی",
        "ب فارم",
        "نیکوپ",
        "پو ک",
    ],

    "Passport": [
        "پاسپورٹ",
        "پاسپورٹ بنوانا",
        "پاسپورٹ تجدید",
        "پاسپورٹ رینیو",
        "پاسپورٹ فیس",
        "پاسپورٹ کی تجدید",
        "نیا پاسپورٹ",
    ],

    "Union Council / Local Government": [
        "یونین کونسل",
        "پیدائش سرٹیفکیٹ",
        "موت کا سرٹیفکیٹ",
        "شادی کا سرٹیفکیٹ",
        "طلاق",
        "مقامی حکومت",
    ],

    "Driving Licence": [
        "ڈرائیونگ لائسنس",
        "ڈرائیونگ لائسنس",
        "لرنر",
        "لائسنس تجدید",
        "ٹریفک لائسنس",
    ],

    "Arms Licence": [
        "اسلحہ لائسنس",
        "اسلحہ",
        "ہتھیار",
        "گن لائسنس",
    ],

    "Police Clearance": [
        "پولیس کلیئرنس",
        "پولیس کریکٹر سرٹیفکیٹ",
        "کریکٹر سرٹیفکیٹ",
        "پولیس تصدیق",
    ],

    "Protector for Visa": [
        "پروٹیکٹر",
        "پروٹیکٹر آف ایمیگرنٹس",
        "بیرون ملک ملازمت",
        "ایمیگریشن",
        "ویزا پروٹیکٹر",
    ],

    "Vaccination for Travelling Abroad": [
        "ویکسین",
        "ویکسینیشن",
        "سفر",
        "بیرون ملک ویکسین",
        "یلو فیور",
        "میننجائٹس",
    ],

    "Domicile": [
        "ڈومیسائل",
        "ڈومیسائل سرٹیفکیٹ",
        "مستقل رہائش",
        "رہائشی سرٹیفکیٹ",
    ],
}


def detect_department(question, selected_department="Automatic"):

    if selected_department != "Automatic":
        return selected_department

    question_lower = question.lower()

    scores = {}

    for department, data in DEPARTMENTS.items():

        score = 0

        # English keywords
        for keyword in data["keywords"]:
            if keyword.lower() in question_lower:
                score += 2

        # Urdu keywords
        for keyword in URDU_DEPARTMENT_TERMS.get(department, []):
            if keyword in question:
                score += 3

        scores[department] = score

    best_department = max(
        scores,
        key=scores.get
    )

    if scores[best_department] == 0:
        return "General Government Services"

    return best_department
