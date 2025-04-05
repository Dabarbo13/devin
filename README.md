# devinBuild a full-stack, production-ready web application with the following integrated systems:

1. Clinical Trial Management (CTMS)

Study setup with phases, arms, visits, documents, and protocol versions

Participant enrollment, eligibility tracking, visit scheduling, adverse event logging

Investigator and coordinator access control

Site-level activity logs, deviation tracking, compliance monitoring


2. Biological Donation & Inventory Management

Donor onboarding and screening (includes physical exams, lab entry, eligibility rules)

Donation scheduling (e.g., leukapheresis, whole blood, PBMCs, etc.)

Inventory tracking by sample type, volume, expiration, storage location

Automated labeling (QR/barcode), chain of custody logs, storage unit mapping


3. Recruiting Platform

Public-facing sign-up form for donors and study participants

Demographic & eligibility filters (age, BMI, HLA type, medication flags, etc.)

Messaging system for call logs, texts, email, and status tags

Referral bonuses, social media tracking, study qualification logic


4. Sponsor & Researcher Portals

Sponsors can create/view/edit trial protocols and track recruitment in real time

Researchers (buyers) can request custom sample collections

Order tracking for status: planned > collecting > shipping > received

Real-time dashboards with KPIs: sample yield, donor flow, site activity


5. Web Store for Research Material

Product listing: sample type, volume, donor attributes (age, sex, HLA, health status)

Cart, checkout, and payment integration (Stripe or ACH preferred)

Purchase history, invoices, and tracking numbers

API access for approved institutional buyers


6. Tech Stack & Requirements

Frontend: React + Tailwind

Backend: Django + PostgreSQL

REST and GraphQL APIs

Celery for async jobs, Redis for task queue

Role-based permissions (donor, recruiter, admin, sponsor, researcher)

Full test suite, Swagger API docs, Dockerized for deployment

Optional: Mobile-optimized frontend or PWA wrapper


Generate modular code organized by features, with clear folders for models, views, serializers, tests, and routes. Include migration files, environment configs, seed data, and CI/CD pipeline scripts.

THE NUMBER ONE MOST IMPORTANT RULE: Please keep track of your token count, if you estimate that an artifact will not be able to be completed, pause and ask me to tell you to continue. If an artifact will need to be broken into separate prompts. Chose the most logical stopping place that will allow you to pick back up
