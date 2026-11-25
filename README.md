# Inventory Analysis 🥬
### Enterprise AI Supermarket Expiry & Wastage Prediction Platform

Inventory Analysis is a commercial-grade, full-stack supermarket intelligence platform designed to eliminate food waste, detect perishable expiry risks, and maximize supermarket profitability through predictive machine learning and dynamic pricing markdowns.

---

## 🌟 Key Architecture & Capabilities

1. **Frontend**: Next.js 14 (React), TypeScript, Tailwind CSS, Recharts, Lucide React.
2. **Collapsible Hamburger Navigation**: Clean, full-width SaaS dashboard with a smooth slide-out left drawer (☰ icon) that is completely hidden by default.
3. **Database & ORM**: PostgreSQL-ready Prisma ORM with SQLite default (`dev.db`) for immediate zero-config local execution.
4. **Machine Learning Microservice**: Python FastAPI service exposing the trained Scikit-learn **Random Forest Classifier** (`95.6% F1-score`, `100 estimators`) on `http://127.0.0.1:8000`.
5. **AI Calling Assistant**: Conversational inventory assistant powered by Groq SDK with Web Speech voice recognition and speech synthesis (multilingual support for Hindi, English, Spanish, etc.).
6. **Dynamic Pricing Engine**: Automated markdown recommendations (10% to 40%), combo bundles, and supplier return warnings based on days to expiry vs daily sales velocity.
7. **What-If Sandbox Simulator**: Interactive slider-based scenario testing for supermarket store managers.
8. **Compliance & Auditing**: Downloadable CSV and JSON reports, printable audit sheets with manager sign-off.

---

## 🗂️ Application Modules

- **Dashboard (`/`)**: Real-time KPIs (Total SKUs, At-Risk Items, Expiring Soon, Potential Savings, Food Waste Reduction), Recharts risk distributions, weekly velocity projections, and alert resolution.
- **Inventory Management (`/inventory`)**: Search, filter by category & risk level, sort, bulk deletion, manual SKU addition/editing, and CSV import/export.
- **AI Expiry Prediction (`/predictions`)**: Batch Random Forest inference with wastage percentage, unsold quantity projections, and financial loss exposure.
- **Dynamic Pricing Advisor (`/pricing`)**: Algorithmic markdown simulator and cross-category breakfast & produce combo bundles.
- **Single Item Simulator (`/simulator`)**: Real-time slider playground testing stock, sales rates, and shelf-life buffers.
- **AI Calling Assistant (`/chat`)**: Voice-call simulation and text chat grounded in real live supermarket inventory.
- **Model Insights (`/model-insights`)**: 95.6% Accuracy, Confusion Matrix, and Gini Feature Importance breakdown.
- **Analytics & Reports (`/reports`)**: Printable executive audit sheets, CSV export, and JSON data streams.
- **Settings (`/settings`)**: Store preferences, currency symbol, risk threshold calibration, and system health status.

---

## 🚀 Quick Start Guide

### 1. Start the FastAPI Machine Learning Microservice
```powershell
py -3.13 -m uvicorn ml_service.main:app --port 8000 --reload
```
*Health Check: `http://127.0.0.1:8000/health`*

### 2. Start the Inventory Analysis Next.js Web Application
```powershell
npm run start
# Or for live development:
npm run dev
```
*Access in your browser at `http://localhost:3000`*

---

## ⚙️ Environment Variables (`.env`)

```env
DATABASE_URL="file:./dev.db"
GROQ_API_KEY="your_groq_api_key_here"
GROQ_MODEL="llama-3.3-70b-versatile"
ML_SERVICE_URL="http://127.0.0.1:8000"
NEXT_PUBLIC_APP_NAME="Inventory Analysis"
PORT=3000
```
