# 🇵🇰 Pakistan Citizen AI Agent

## پاکستان سٹیزن AI ایجنٹ

An AI-powered government services information assistant
designed to help Pakistani citizens find current information
about government services.

## Departments

1. NADRA
2. Passport
3. Union Council / Local Government
4. Driving Licence
5. Arms Licence
6. Police Clearance
7. Protector for Visa
8. Vaccination for Travelling Abroad
9. Domicile

## Architecture

User Question
→ Department Detection
→ Web Research
→ Official Source Filtering
→ Verification
→ Groq AI
→ Answer + Sources

## Important

The AI should not rely only on its training knowledge.

The application searches current online information and
prioritizes official government sources.

If reliable information cannot be found, the application
should tell the citizen that the information could not be
verified instead of inventing an answer.

## AI

Groq API.

## Search

DDGS independent web search.

## Deployment

Streamlit Community Cloud.

## Secret

GROQ_API_KEY

Never commit API keys to GitHub.

## Developer

Developed by Raees Khan
