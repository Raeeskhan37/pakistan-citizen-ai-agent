from groq import Groq
from groq import RateLimitError

import streamlit as st

from ai.prompts import (
    build_system_prompt,
    build_user_prompt,
)

from config.settings import GROQ_MODEL


# ============================================================
# GROQ CLIENT
# ============================================================

def get_client():

    return Groq(
        api_key=st.secrets["GROQ_API_KEY"],
        timeout=45.0,
    )


# ============================================================
# SAUDI WORK VISA DETECTION
# ============================================================

def is_saudi_work_visa_vaccination_question(
    question,
    department,
):

    if department != "Vaccination for Travelling Abroad":
        return False

    q = (
        question or ""
    ).lower()

    saudi_terms = [
        "saudi",
        "saudia",
        "saudi arabia",
        "سعودی",
    ]

    work_terms = [
        "work visa",
        "employment visa",
        "employment",
        "work permit",
        "worker",
        "working",
        "job visa",
        "iqama",
        "job",
        "ملازمت",
        "ورک ویزا",
        "اقامہ",
    ]

    vaccination_terms = [
        "vaccine",
        "vaccination",
        "vaccinated",
        "immunization",
        "immunisation",
        "ویکسین",
        "ویکسینیشن",
    ]

    return (
        any(
            term in q
            for term in saudi_terms
        )
        and
        any(
            term in q
            for term in work_terms
        )
        and
        any(
            term in q
            for term in vaccination_terms
        )
    )


# ============================================================
# SAUDI GUARDRAIL
# ============================================================

def add_work_visa_guardrail(
    system_prompt,
):

    guardrail = """
CRITICAL EVIDENCE RULE — ORDINARY SAUDI WORK VISA

If the user's question concerns an ordinary Saudi
employment/work visa, do not treat it as Hajj or Umrah.

Do not state that a specific vaccine is mandatory unless
the supplied CURRENT official evidence explicitly proves
that requirement.

Do not convert "can get vaccinated" into "must be vaccinated".

Do not transfer Hajj or Umrah requirements to ordinary
employment visas.

Answer only from the supplied official evidence.
"""

    return (
        system_prompt
        + "\n\n"
        + guardrail
    )


# ============================================================
# BIRTH CERTIFICATE FALLBACK
# ============================================================

def build_birth_fallback(
    question,
    evidence,
    language,
):

    q = (
        question or ""
    ).lower()

    # --------------------------------------------------------
    # SINDH
    # --------------------------------------------------------

    if "sindh" in q:

        if language in ("Urdu", "اردو"):

            return """
### سندھ

سندھ میں پیدائش کی رجسٹریشن متعلقہ لوکل گورنمنٹ /
یونین کونسل کے نظام کے ذریعے کی جاتی ہے۔

حکومت سندھ نے پیدائش، وفات، شادی اور طلاق کی
آن لائن رجسٹریشن کے لیے صوبائی CRMS نظام بھی
متعارف کرایا ہے۔

درخواست دینے سے پہلے متعلقہ یونین کونسل یا
سرکاری سندھ CRMS نظام سے موجودہ طریقہ کار کی
تصدیق کریں۔
"""

        return """
### Sindh

Birth registration in Sindh is handled through the
relevant local-government / Union Council system.

The Government of Sindh has also announced online
registration of birth, death, marriage and divorce
through the provincial CRMS system.

Confirm the current procedure with the relevant
Union Council or official Sindh CRMS service before
applying.
"""

    # --------------------------------------------------------
    # BALOCHISTAN
    # --------------------------------------------------------

    if "balochistan" in q:

        if language in ("Urdu", "اردو"):

            return """
### بلوچستان

بلوچستان میں پیدائش کی رجسٹریشن متعلقہ لوکل
کونسل / یونین کونسل کے ذریعے کی جاتی ہے۔

بلوچستان لوکل گورنمنٹ اینڈ رورل ڈویلپمنٹ
ڈیپارٹمنٹ پیدائش کے سرٹیفکیٹ کی سرکاری سروس
فراہم کرتا ہے۔

CRMS / PakID کے ذریعے آن لائن رجسٹریشن کی
سہولت بھی سرکاری طور پر بیان کی گئی ہے۔

درخواست دینے سے پہلے متعلقہ لوکل کونسل یا
سرکاری CRMS سروس سے موجودہ طریقہ کار کی
تصدیق کریں۔
"""

        return """
### Balochistan

Birth registration in Balochistan is handled through
the relevant Local Council / Union Council.

The Balochistan Local Government & Rural Development
Department provides an official Birth Certificate
service.

The department has also announced online registration
through CRMS/PakID.

Confirm the current procedure with the relevant Local
Council or official CRMS service before applying.
"""

    # --------------------------------------------------------
    # KP
    # --------------------------------------------------------

    if (
        "kp" in q
        or "kpk" in q
        or "khyber pakhtunkhwa" in q
    ):

        if language in ("Urdu", "اردو"):

            return """
### خیبر پختونخوا

پیدائش کی رجسٹریشن متعلقہ ویلج کونسل یا
نیبرہڈ کونسل کے ذریعے کی جاتی ہے۔

سرکاری KP رہنمائی کے مطابق Form-A، والدین یا
سرپرست کے CNIC/پاسپورٹ کی تصدیق شدہ کاپی اور
دستیاب ہونے کی صورت میں ہسپتال کا برتھ
سرٹیفکیٹ، ویکسینیشن کارڈ یا اسکول سرٹیفکیٹ
درکار ہو سکتا ہے۔
"""

        return """
### Khyber Pakhtunkhwa

Birth registration is handled through the relevant
Village Council or Neighbourhood Council.

Official KP guidance lists Form-A, an attested CNIC
or passport copy of the parent(s)/guardian, and,
where available, a health-facility birth certificate,
immunization card or school certificate.
"""

    # --------------------------------------------------------
    # PUNJAB / LAHORE
    # --------------------------------------------------------

    if (
        "lahore" in q
        or "punjab" in q
    ):

        if language in ("Urdu", "اردو"):

            return """
### پنجاب

پنجاب، بشمول لاہور، میں پیدائش کی رجسٹریشن
متعلقہ یونین کونسل کے ذریعے کی جاتی ہے۔

سرکاری پنجاب رہنمائی کے مطابق والدین کے CNIC
کی نقول، پیدائش کا ثبوت اور مقررہ یونین کونسل
فارم درکار ہوتا ہے۔

معمول کی اور تاخیر سے ہونے والی رجسٹریشن کے
لیے مختلف طریقہ کار اور مدت مقرر ہے۔
"""

        return """
### Punjab

In Punjab, including Lahore, birth registration is
handled through the relevant Union Council.

Official Punjab guidance lists parents' CNIC copies,
proof of birth and the prescribed Union Council form.

Normal and late registration have different
procedures and processing periods.
"""

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    if language in ("Urdu", "اردو"):

        return """
پاکستان میں نئے پیدائش سرٹیفکیٹ کا طریقہ صوبے
اور علاقے کے مطابق مختلف ہو سکتا ہے۔

سول پیدائش کی رجسٹریشن عام طور پر متعلقہ یونین
کونسل، لوکل کونسل، میونسپل کمیٹی یا دوسرے
متعلقہ مقامی حکام کے ذریعے ہوتی ہے۔

NADRA کا CRC / B-Form سول پیدائش سرٹیفکیٹ سے
الگ دستاویز ہے۔

درخواست دینے سے پہلے اپنے علاقے کی متعلقہ
مقامی حکومت سے موجودہ طریقہ کار، مطلوبہ
دستاویزات، فیس اور آن لائن سہولت کی تصدیق کریں۔
"""

    return """
In Pakistan, the procedure for obtaining a new birth
certificate varies by province and territory.

Civil birth registration is generally handled through
the relevant Union Council, Local Council, Municipal
Committee or other local-government authority.

A NADRA CRC/B-Form is a separate identity document
and should not be treated as a replacement for the
civil birth certificate.

Confirm the current procedure, documents, fees and
online options with the relevant local authority.
"""


# ============================================================
# DRIVING LICENCE FALLBACK
# ============================================================

def build_driving_fallback(
    question,
    evidence,
    language,
):

    q = (
        question or ""
    ).strip().lower()

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    if "htv" in q or "heavy transport vehicle" in q:
        category = "HTV (Heavy Transport Vehicle)"

    elif "ltv" in q or "light transport vehicle" in q:
        category = "LTV (Light Transport Vehicle)"

    elif (
        "motor car" in q
        or "motorcar" in q
        or "car licence" in q
        or "car license" in q
        or "car/jeep" in q
    ):
        category = "Motor Car / Car / Jeep"

    elif (
        "motorcycle" in q
        or "motor cycle" in q
        or "bike" in q
    ):
        category = "Motorcycle"

    elif (
        "psv" in q
        or "public service vehicle" in q
    ):
        category = "PSV (Public Service Vehicle)"

    elif (
        "learner" in q
        or "learner permit" in q
        or "learning licence" in q
        or "learning license" in q
    ):
        category = "Learner Driving Licence"

    else:
        category = "Driving Licence"

    # --------------------------------------------------------
    # JURISDICTION DETECTION
    # --------------------------------------------------------

    specific_jurisdiction = None

    if "punjab" in q or "lahore" in q:
        specific_jurisdiction = "Punjab"

    elif "sindh" in q or "karachi" in q:
        specific_jurisdiction = "Sindh"

    elif (
        "khyber pakhtunkhwa" in q
        or "kpk" in q
        or "kp" in q
        or "peshawar" in q
    ):
        specific_jurisdiction = (
            "Khyber Pakhtunkhwa"
        )

    elif (
        "balochistan" in q
        or "quetta" in q
    ):
        specific_jurisdiction = "Balochistan"

    elif "islamabad" in q:
        specific_jurisdiction = (
            "Islamabad Capital Territory"
        )

    elif (
        "ajk" in q
        or "azad kashmir" in q
        or "muzaffarabad" in q
    ):
        specific_jurisdiction = (
            "Azad Jammu and Kashmir"
        )

    elif (
        "gilgit-baltistan" in q
        or "gilgit baltistan" in q
        or "gilgit" in q
        or "skardu" in q
    ):
        specific_jurisdiction = (
            "Gilgit-Baltistan"
        )

    # --------------------------------------------------------
    # URDU — SPECIFIC JURISDICTION
    # --------------------------------------------------------

    if language in ("Urdu", "اردو"):

        if specific_jurisdiction == "Punjab":

            return f"""
### پنجاب

**کیٹیگری:** {category}

پنجاب میں ڈرائیونگ لائسنس کی سرکاری آن لائن
سروس DLIMS 2.0 کے ذریعے دستیاب ہے۔

نئے لائسنس کے لیے سرکاری نظام میں اکاؤنٹ بنانا،
درخواست فارم مکمل کرنا، PSID بنانا، فیس ادا کرنا
اور DLIMS کی ہدایات کے مطابق پراسیسنگ مکمل کرنا
شامل ہے۔

درست فیس اور مخصوص دستاویزات منتخب کیٹیگری کے
مطابق سرکاری DLIMS سے چیک کریں۔
"""

        if specific_jurisdiction == "Sindh":

            return f"""
### سندھ

**کیٹیگری:** {category}

سندھ میں ڈرائیونگ لائسنس کی سرکاری سروس
Driving License Sindh (DLS) کے ذریعے دستیاب ہے۔

سرکاری طریقہ کار میں آن لائن رجسٹریشن، DLS
فرنٹ ڈیسک پر حاضری، اسکریننگ، میڈیکل، فیس
ادائیگی اور متعلقہ ٹیسٹ شامل ہو سکتے ہیں۔

روڈ ٹیسٹ اور دیگر مراحل منتخب لائسنس کی
کیٹیگری کے مطابق لاگو ہوتے ہیں۔
"""

        if specific_jurisdiction == "Khyber Pakhtunkhwa":

            return f"""
### خیبر پختونخوا

**کیٹیگری:** {category}

KP میں ڈرائیونگ لائسنس کے لیے Dastak سرکاری
ڈیجیٹل روٹ کے طور پر استعمال ہوتا ہے جہاں
متعلقہ سروس دستیاب ہو۔

سرکاری KP ٹرانسپورٹ لائسنسنگ نظام میں Learner،
LTV، HTV اور International Driving Licence
سروسز شامل ہیں۔

درخواست کے مراحل میں پروفائل، شناختی تصدیق،
ضروری دستاویزات، تصدیق، فیس اور لائسنس
پراسیسنگ شامل ہو سکتی ہے۔

مخصوص کیٹیگری کے موجودہ مراحل Dastak اور
KP Transport Department سے چیک کریں۔
"""

        if specific_jurisdiction == "Balochistan":

            if "quetta" in q:

                return f"""
        ### Quetta, Balochistan

        **Requested category:** {category}

        Balochistan Police operates Police Mobile Khidmat
        Markaz (PKM) facilities in Quetta.

        For a new Motor Car licence, the official Balochistan
        Police information establishes the following process:

        **1. Obtain the learner permit**

        The official PKM service states that a learner driving
        licence can be obtained from Police Mobile Khidmat
        Markaz.

        For Motor Car:
        - Minimum learner age: 18 years
        - Original CNIC and one copy
        - Traffic Rules & Regulations Code Book
        - Medical Certificate for applicants aged 50 or above
        - Learner permit validity: 6 months
        - Published learner fee: Rs. 60 Post Office ticket
        - Published turnaround: about 15 minutes

        **2. Complete the learner period**

        The official PKM endorsement requirements specify an
        original learner permit of at least six weeks.

        **3. Follow the regular-licence / endorsement process**

        The official PKM information lists the following for
        endorsement:

        - Medical Certificate copy
        - CNIC copy
        - Two attested fresh photographs
        - Original learner permit of at least six weeks
        - Driving tickets according to the applicable schedule

        **Important:**

        The official PKM website does not publish a complete
        step-by-step regular Motor Car licence procedure on
        the same page. Therefore, the agent must not invent
        additional tests, fees or processing steps.

        For the current Quetta procedure, use the official
        Balochistan Police Police Mobile Khidmat Markaz /
        Traffic Police service.

        **Official source:**
        Balochistan Police — Police Mobile Khidmat Markaz
        https://pkm.balochistanpolice.gov.pk/
"""

    return f"""
### Balochistan

**Requested category:** {category}

Balochistan Police provides driving-licence services
through Police Mobile Khidmat Markaz (PKM).

Officially documented services include:

- Learner Driving Licence
- Driving Licence Renewal
- International Driving Licence
- Duplicate Driving Licence
- Endorsement of a Licence

For a new regular {category}, the official evidence
available to the agent does not publish every step of
the complete regular-licence procedure.

Therefore, the agent should provide only the documented
requirements and direct the citizen to the official
Balochistan Police PKM for the current regular-licence
procedure.
"""

    if specific_jurisdiction == "Islamabad Capital Territory":

        return f"""
### اسلام آباد کیپیٹل ٹیریٹری

**کیٹیگری:** {category}

اسلام آباد ٹریفک پولیس کی سرکاری ITP-DLIMS
آن لائن سروس میں New Driving Licence، Learner
Permit، Driving Tests، Renewal، Duplicate اور
International Driving Permit کی سہولیات شامل ہیں۔

مخصوص فیس، دستاویزات اور ٹیسٹ منتخب کیٹیگری
کے مطابق موجودہ ITP-DLIMS سے چیک کریں۔
"""

        if specific_jurisdiction == "Azad Jammu and Kashmir":

            return f"""
### آزاد جموں و کشمیر

**کیٹیگری:** {category}

AJK Traffic Police کا سرکاری پورٹل لائسنس
پروسیجر، تصدیق، درخواست ٹریکنگ، فارم، میڈیکل
فارم، فیس چالان اور متعلقہ لائسنسنگ معلومات
فراہم کرتا ہے۔

درخواست کے لیے سرکاری AJK Traffic Police
طریقہ کار اور متعلقہ فارم استعمال کریں۔
"""

        if specific_jurisdiction == "Gilgit-Baltistan":

            return f"""
### گلگت بلتستان

**کیٹیگری:** {category}

Gilgit-Baltistan DLMIS سرکاری Regular Driving
Licence، Renewal، Duplicate اور International
Driving Licence سروسز فراہم کرتا ہے۔

Regular Licence Form میں Motorcycle، Motor Car،
LTV، HTV اور دیگر گاڑیوں کی کیٹیگریز شامل ہیں۔

مخصوص دستاویزات اور فیس موجودہ DLMIS سے چیک کریں۔
"""

    # --------------------------------------------------------
    # ENGLISH — SPECIFIC JURISDICTION
    # --------------------------------------------------------

    if specific_jurisdiction == "Punjab":

        return f"""
### Punjab

**Requested category:** {category}

The official Punjab DLIMS 2.0 provides driving
licence services.

For a new licence, the official online process
includes creating an account, completing the
application, generating the PSID, making payment
and following the DLIMS processing instructions.

The exact fee and document requirements depend on
the selected licence category and should be checked
on the current official DLIMS portal.
"""

    if specific_jurisdiction == "Sindh":

        return f"""
### Sindh

**Requested category:** {category}

The official Driving License Sindh (DLS) system
provides driving licence services.

The computerized licence procedure includes online
registration, appearance at the DLS front desk,
screening/registration, medical examination, fee
payment and the applicable written/oral and road
tests.

The exact requirements depend on the selected
licence category.
"""

    if specific_jurisdiction == "Khyber Pakhtunkhwa":

        return f"""
### Khyber Pakhtunkhwa

**Requested category:** {category}

The official KP transport licensing workflow uses
the Dastak App as a digital route for driving
licence services where the relevant service is
available.

The official KP transport licensing system covers
Learner, LTV, HTV and International Driving
Licence services.

The digital workflow may include applicant profile,
CNIC/NADRA verification, required documents,
verification/approval, payment and licence
processing.

The exact steps can vary according to the selected
category and current service availability.
"""

    if specific_jurisdiction == "Balochistan":

        return f"""
### Balochistan

**Requested category:** {category}

Official Balochistan Police evidence confirms
driving-licence services through Police Mobile
Khidmat Markaz (PKM).

The published services include learner licence,
renewal, international licence, duplicate licence
and endorsement.

For a new regular {category}, the official evidence
retrieved does not establish the complete regular
licence procedure. Therefore, additional steps are
not being assumed.

The current procedure should be confirmed with the
official Balochistan PKM.
"""

    if specific_jurisdiction == "Islamabad Capital Territory":

        return f"""
### Islamabad Capital Territory

**Requested category:** {category}

Islamabad Traffic Police provides official driving
licence services through ITP-DLIMS.

The official services include new driving licence,
learner permit, driving tests, renewal, duplicate
licence and international driving permit.

Specific documents, fees and test requirements
should be checked against the current ITP-DLIMS
requirements for the selected category.
"""

    if specific_jurisdiction == "Azad Jammu and Kashmir":

        return f"""
### Azad Jammu and Kashmir

**Requested category:** {category}

The official Traffic Police AJ&K portal provides
licence procedures, application tracking, licence
office information, application forms, medical
forms, fee challans, licence fee information and
test-related material.

Applicants should follow the official AJK Traffic
Police procedure for the selected category.
"""

    if specific_jurisdiction == "Gilgit-Baltistan":

        return f"""
### Gilgit-Baltistan

**Requested category:** {category}

The official Gilgit-Baltistan DLMIS provides
regular driving licence, renewal, duplicate and
international driving licence services.

The official regular licence form includes
Motorcycle, Motor Car, LTV, HTV and other vehicle
categories.

Check the current DLMIS for the exact documents,
fees and processing requirements.
"""

    # --------------------------------------------------------
    # ALL SEVEN JURISDICTIONS
    # --------------------------------------------------------

    if language in ("Urdu", "اردو"):

        return f"""
# پاکستان میں {category} حاصل کرنے کا طریقہ

ذیل میں دستیاب سرکاری شواہد کے مطابق ساتوں
صوبوں/علاقوں کی معلومات الگ الگ دی گئی ہیں۔

### 1. پنجاب

Punjab DLIMS 2.0 کے ذریعے ڈرائیونگ لائسنس کی
آن لائن سروس دستیاب ہے۔ نئے لائسنس کے لیے
اکاؤنٹ، درخواست، PSID، فیس اور سرکاری پراسیسنگ
مراحل شامل ہیں۔

### 2. سندھ

Driving License Sindh (DLS) کے ذریعے آن لائن
رجسٹریشن، فرنٹ ڈیسک، اسکریننگ، میڈیکل، فیس
اور متعلقہ ٹیسٹ کا عمل موجود ہے۔

### 3. خیبر پختونخوا

Dastak سرکاری ڈیجیٹل روٹ کے طور پر استعمال ہوتا
ہے جہاں متعلقہ ڈرائیونگ لائسنس سروس دستیاب ہو۔
KP نظام میں Learner، LTV، HTV اور International
Driving Licence شامل ہیں۔

### 4. بلوچستان

Police Mobile Khidmat Markaz ڈرائیونگ لائسنس
سے متعلق سرکاری سروسز فراہم کرتا ہے۔ دستیاب
شواہد میں Learner، Renewal، International،
Duplicate اور Endorsement شامل ہیں۔

نئے Regular لائسنس کے مکمل مراحل کے بارے میں
اضافی معلومات فرض نہیں کی جا رہی۔

### 5. اسلام آباد کیپیٹل ٹیریٹری

ITP-DLIMS کے ذریعے New Licence، Learner Permit،
Driving Tests، Renewal، Duplicate اور International
Driving Permit سروسز دستیاب ہیں۔

### 6. آزاد جموں و کشمیر

AJK Traffic Police کا سرکاری پورٹل لائسنس
پروسیجر، فارم، میڈیکل فارم، فیس اور ٹیسٹ سے
متعلق معلومات فراہم کرتا ہے۔

### 7. گلگت بلتستان

GB DLMIS کے ذریعے Regular Licence، Renewal،
Duplicate اور International Licence سروسز
دستیاب ہیں۔ Regular form میں مختلف گاڑیوں کی
کیٹیگریز شامل ہیں۔

**اہم:** ایک صوبے کی فیس، عمر، دستاویز یا طریقہ
دوسرے صوبے پر لاگو نہیں کیا جانا چاہیے۔
"""

    return f"""
# Getting a {category} in Pakistan

The following information is organized separately
for the seven Pakistani jurisdictions using the
official evidence retrieved.

### 1. Punjab

Punjab DLIMS 2.0 provides official driving licence
services. The new-licence online process includes
account creation, application, PSID generation,
payment and the official processing steps.

### 2. Sindh

Driving License Sindh (DLS) provides online
registration followed by the applicable front-desk,
screening, medical, payment and testing stages.

### 3. Khyber Pakhtunkhwa

Dastak is an official digital route for KP transport
driving-licence services where the relevant service
is available. The KP system covers Learner, LTV,
HTV and International Driving Licence services.

### 4. Balochistan

Balochistan Police's Police Mobile Khidmat Markaz
provides official driving-licence services including
learner, renewal, international, duplicate and
endorsement services.

The retrieved official evidence does not establish
the complete regular-licence procedure for every
category, so additional steps are not assumed.

### 5. Islamabad Capital Territory

ITP-DLIMS provides official services including new
driving licence, learner permit, driving tests,
renewal, duplicate licence and international
driving permit.

### 6. Azad Jammu and Kashmir

The official Traffic Police AJ&K portal provides
licence procedures, application forms, medical forms,
fee challans, licence information and test-related
material.

### 7. Gilgit-Baltistan

GB DLMIS provides regular driving licence, renewal,
duplicate and international licence services.
The regular licence form includes categories such
as Motorcycle, Motor Car, LTV and HTV.

**Important:** Requirements, fees, age limits,
documents and tests must not be transferred from
one jurisdiction to another.
"""


# ============================================================
# MAIN ANSWER GENERATOR
# ============================================================

def generate_answer(
    question,
    department,
    evidence,
    language,
):

        # --------------------------------------------------------
    # DRIVING LICENCE
    #
    # For an unspecified jurisdiction, use the deterministic
    # seven-jurisdiction answer. This prevents Groq's token
    # limit from cutting the answer after Punjab/KP.
    # --------------------------------------------------------

    if department == "Driving Licence":

        q_lower = (
            question or ""
        ).strip().lower()

        has_specific_jurisdiction = any(
            term in q_lower
            for term in [
                "punjab",
                "lahore",
                "sindh",
                "karachi",
                "khyber pakhtunkhwa",
                "kpk",
                "kp",
                "peshawar",
                "balochistan",
                "quetta",
                "islamabad",
                "ajk",
                "azad kashmir",
                "muzaffarabad",
                "gilgit-baltistan",
                "gilgit baltistan",
                "gilgit",
                "skardu",
            ]
        )

        # If no jurisdiction was specified, ALWAYS use the
        # complete seven-jurisdiction fallback. Do not send
        # this long answer through the LLM.
        if not has_specific_jurisdiction:

            return build_driving_fallback(
                question=question,
                evidence=evidence,
                language=language,
            )

    client = get_client()

    system_prompt = build_system_prompt(
        department=department,
        language=language,
    )

    if is_saudi_work_visa_vaccination_question(
        question=question,
        department=department,
    ):

        system_prompt = add_work_visa_guardrail(
            system_prompt
        )

    # --------------------------------------------------------
    # Evidence limit
    # --------------------------------------------------------

    max_evidence_chars = 30000

    if len(evidence) > max_evidence_chars:

        evidence = (
            evidence[:max_evidence_chars]
            + "\n\n[Evidence was limited for answer-generation "
              "efficiency. Use the jurisdiction-specific evidence "
              "already provided above and do not invent missing details.]"
        )

    user_prompt = build_user_prompt(
        question=question,
        department=department,
        evidence=evidence,
        language=language,
    )

    # --------------------------------------------------------
    # Generate AI answer
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.1,
            max_tokens=1200,
        )

        answer = (
            response.choices[0]
            .message.content
        )

        # ----------------------------------------------------
        # Successful AI answer
        # ----------------------------------------------------

        if answer:

            return answer.strip()

        # ----------------------------------------------------
        # EMPTY AI RESPONSE
        # ----------------------------------------------------

        if department == "Driving Licence":

            return build_driving_fallback(
                question=question,
                evidence=evidence,
                language=language,
            )

        if (
            department
            == "Union Council / Local Government"
            and any(
                term in (
                    question or ""
                ).lower()
                for term in [
                    "birth",
                    "birth certificate",
                    "birth registration",
                    "newborn",
                    "پیدائش",
                ]
            )
        ):

            return build_birth_fallback(
                question,
                evidence,
                language,
            )

        return (
            "The official government sources were found, "
            "but the AI returned an empty answer. "
            "Please try the question again."
        )

    # ========================================================
    # RATE LIMIT
    # ========================================================

    except RateLimitError:

        if department == "Driving Licence":

            return build_driving_fallback(
                question=question,
                evidence=evidence,
                language=language,
            )

        if (
            department
            == "Union Council / Local Government"
            and any(
                term in (
                    question or ""
                ).lower()
                for term in [
                    "birth",
                    "birth certificate",
                    "birth registration",
                    "newborn",
                    "پیدائش",
                ]
            )
        ):

            return build_birth_fallback(
                question,
                evidence,
                language,
            )

        return (
            "The AI answer service has temporarily "
            "reached its usage limit. The official "
            "government sources were found. Please "
            "try again later."
        )

    # ========================================================
    # ANY OTHER AI ERROR
    # ========================================================

    except Exception as exc:

        error_text = str(
            exc
        ).lower()

        # ----------------------------------------------------
        # DRIVING LICENCE FALLBACK
        # ----------------------------------------------------

        if department == "Driving Licence":

            return build_driving_fallback(
                question=question,
                evidence=evidence,
                language=language,
            )

        # ----------------------------------------------------
        # BIRTH CERTIFICATE FALLBACK
        # ----------------------------------------------------

        if (
            department
            == "Union Council / Local Government"
            and any(
                term in (
                    question or ""
                ).lower()
                for term in [
                    "birth",
                    "birth certificate",
                    "birth registration",
                    "newborn",
                    "پیدائش",
                ]
            )
        ):

            return build_birth_fallback(
                question,
                evidence,
                language,
            )

        # ----------------------------------------------------
        # TIMEOUT
        # ----------------------------------------------------

        if (
            "timeout" in error_text
            or "timed out" in error_text
        ):

            return (
                "The AI request took too long to complete. "
                "The official government sources were found. "
                "Please try the question again."
            )

        return (
            "The AI answer could not be generated at this "
            "time. The official government sources were "
            "found. Please try the question again."
        )
