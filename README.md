# Biobank Platform

A full-stack, production-ready web application with the following integrated systems:

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

## Development Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+
- Redis (for Celery)

### Backend Setup
1. Clone the repository
   ```
   git clone https://github.com/Dabarbo13/devin.git
   cd devin/backend
   ```

2. Set up Python environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install poetry
   poetry install
   ```

3. Configure environment variables
   ```
   cp .env.example .env
   # Edit .env with your specific configuration
   ```

4. Run migrations
   ```
   python manage.py migrate
   ```

5. Start development server
   ```
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to frontend directory
   ```
   cd ../frontend
   ```

2. Install dependencies
   ```
   npm install
   ```

3. Start development server
   ```
   npm run dev
   ```

### API Documentation
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

### Authentication
- JWT authentication is implemented for API endpoints
- Obtain tokens at: http://localhost:8000/api/token/
- Refresh tokens at: http://localhost:8000/api/token/refresh/
- Verify tokens at: http://localhost:8000/api/token/verify/
