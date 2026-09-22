from config.departments import DEPARTMENTS


URDU_DEPARTMENT_TERMS = {

    "NADRA": [
        "نادرا",
        "شناختی کارڈ",
        "شناختی",
        "ب فارم",
        "ب فارم",
        "نیکوپ",
        "پو ک",
        "فیملی رجسٹریشن",
        "خاندانی رجسٹریشن",
    ],

    "Passport": [
        "پاسپورٹ",
        "پاسپورٹ بنوانا",
        "پاسپورٹ تجدید",
        "پاسپورٹ رینیو",
        "پاسپورٹ فیس",
        "پاسپورٹ کی تجدید",
        "نیا پاسپورٹ",
        "پاسپورٹ درخواست",
    ],

    "Union Council / Local Government": [
        "یونین کونسل",
        "پیدائش سرٹیفکیٹ",
        "پیدائش کا سرٹیفکیٹ",
        "پیدائش کا اندراج",
        "برتھ سرٹیفکیٹ",
        "وفات کا سرٹیفکیٹ",
        "موت کا سرٹیفکیٹ",
        "موت کا اندراج",
        "شادی کا سرٹیفکیٹ",
        "شادی کا اندراج",
        "نکاح رجسٹریشن",
        "طلاق کا سرٹیفکیٹ",
        "مقامی حکومت",
        "مقامی کونسل",
        "میونسپل کمیٹی",
    ],

    "Driving Licence": [
        "ڈرائیونگ لائسنس",
        "ڈرائیونگ لائسنس",
        "لرنر",
        "لرنر لائسنس",
        "لرنر پرمٹ",
        "لائسنس تجدید",
        "ڈرائیونگ ٹیسٹ",
        "ٹریفک پولیس",
    ],

    "Arms Licence": [
        "اسلحہ لائسنس",
        "اسلحہ",
        "ہتھیار",
        "گن لائسنس",
        "بندوق لائسنس",
        "اسلحہ پرمٹ",
    ],

    "Police Clearance": [
        "پولیس کلیئرنس",
        "پولیس کریکٹر سرٹیفکیٹ",
        "کریکٹر سرٹیفکیٹ",
        "پولیس تصدیق",
        "پولیس سرٹیفکیٹ",
        "پولیس کلیئرنس سرٹیفکیٹ",
    ],

    "Protector for Visa": [
        "پروٹیکٹر",
        "پروٹیکٹر آف ایمیگرنٹس",
        "بیرون ملک ملازمت",
        "ایمیگریشن",
        "امیگریشن",
        "ویزا پروٹیکٹر",
        "پروٹیکٹر اسٹیمپ",
        "اوورسیز ملازمت",
    ],

    "Vaccination for Travelling Abroad": [
        "ویکسین",
        "ویکسینیشن",
        "ویکسینیشن سرٹیفکیٹ",
        "سفر",
        "بیرون ملک ویکسین",
        "بیرون ملک سفر",
        "یلو فیور",
        "میننجائٹس",
        "حج ویکسین",
        "عمرہ ویکسین",
    ],

    "Domicile": [
        "ڈومیسائل",
        "ڈومیسائل سرٹیفکیٹ",
        "مستقل رہائش",
        "مستقل رہائش کا سرٹیفکیٹ",
        "رہائشی سرٹیفکیٹ",
        "ضلع ڈومیسائل",
    ],
}


def detect_department(
    question,
    selected_department="Automatic",
):
    if selected_department != "Automatic":
        return selected_department

    if not question:
        return "General Government Services"

    question_lower = question.lower()

    scores = {
        department: 0
        for department in DEPARTMENTS
    }

    for department, data in DEPARTMENTS.items():

        for keyword in data.get(
            "keywords",
            [],
        ):

            if keyword.lower() in question_lower:
                scores[department] += 2

        for keyword in URDU_DEPARTMENT_TERMS.get(
            department,
            [],
        ):

            if keyword in question:
                scores[department] += 3

    best_department = max(
        scores,
        key=scores.get,
    )

    if scores[best_department] == 0:
        return "General Government Services"

    return best_department
