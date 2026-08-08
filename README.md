# Cart Rescue

### Intelligent Cart Abandonment Prediction & Recovery System

Cart Rescue is an intelligent e-commerce platform that predicts cart abandonment in real time by analyzing customer behavior during their shopping journey. The system provides abandonment risk predictions, explains the factors influencing the prediction, and recommends the most appropriate recovery action to improve customer conversion.

Developed as part of **AI Build 2026 – Track 2: Cart Rescue**.

---

# Overview

Cart abandonment is a common challenge faced by e-commerce platforms. Customers may leave before completing their purchase due to payment failures, long checkout processes, delivery concerns, or price comparisons.

Cart Rescue continuously monitors customer sessions, analyzes behavioral patterns using machine learning, predicts abandonment risk, and recommends the most suitable action instead of applying the same strategy to every customer.

The platform supports two user roles:
- **Customer** – Shop, add to cart, checkout, and make payments
- **Super Admin** – Monitor live sessions, review high-risk sessions, accept/ignore AI recommendations, and trigger recovery actions via SMS/Call

---

# Features

## Customer Portal
- Customer Registration & Login
- Home Page with Featured Products
- Product Listing (Shop Page)
- Flash Sale & AI Personalized Recommendations
- Add to Cart with Quantity Selector
- Shopping Cart (Increase / Decrease quantity)
- Checkout & Payment Processing
- Real-time Session & Event Tracking

## AI Prediction Engine
- Real-Time Session Monitoring
- Customer Behavior Event Tracking
- Feature Extraction from session events
- Abandonment Risk Prediction (XGBoost)
- Risk Score & Risk Level Generation
- Scenario Detection (Payment Failure, Checkout Hesitation, Price Sensitivity, etc.)
- Intelligent Action Recommendation

## Super Admin Dashboard
- Dashboard Overview (Live Sessions, High Risk, Total Sessions, Customers)
- Live Customer Sessions (Active / Inactive status)
- High Risk Sessions
- Session Details with AI Recommendation
- Accept / Ignore recommended action
- Action History
- Analytics (Risk Breakdown, Scenario Distribution, Action Stats)
- Trigger recovery via **Twilio SMS / Phone Call**

---

# System Workflow

```text
Customer Login / Guest Session
            │
            ▼
      Browse Products
            │
            ▼
       View Product
            │
            ▼
       Add to Cart
            │
            ▼
        Checkout
            │
            ▼
     Payment Attempt
            │
            ▼
  Store Session Events (MongoDB)
            │
            ▼
 Machine Learning Prediction
   (Features → Risk → Scenario)
            │
            ▼
      Risk Score + Scenario
            │
            ▼
     Decision Agent
            │
            ▼
  Recommended Action
            │
            ▼
 Super Admin Reviews Session
            │
     ┌──────┴──────┐
     ▼             ▼
  Accept         Ignore
     │
     ▼
Twilio SMS / Call
     │
     ▼
Dashboard + Action History Updated
```

---

# Technology Stack

## Frontend

React.js (Vite)
React Router
Axios
Lucide React (Icons)
Custom CSS

## Backend

Python
Flask
Flask-CORS
REST APIs

## Database

MongoDB Atlas

## Machine Learning

XGBoost
Scikit-learn
Pandas
NumPy

---

# Project Structure

Cart_Rescue/
│
├── backend/
│   ├── routes/
│   │   ├── admin_routes.py         
│   │   ├── auth_routes.py           
│   │   ├── event_routes.py          
│   │   ├── product_routes.py        
│   │   └── session_routes.py        
│   │
│   ├── app.py                      
│   ├── config.py                    
│   ├── database.py                  
│   ├── decision_service.py         
│   ├── session_manager.py           
│   ├── twilio_service.py            
│   ├── create_admin.py              
│   ├── fix_admin.py                 
│   ├── test_api.py                 
│   ├── requirements.txt
│   └── .env                       
│
├── frontend/
│   ├── public/
│   │
│   ├── src/
│   │   ├── assets/
│   │   │
│   │   ├── components/
│   │   │   ├── AddToCartButton.jsx  
│   │   │   ├── Categories.jsx
│   │   │   ├── FeaturedProducts.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── Newsletter.jsx
│   │   │   └── Testimonials.jsx
│   │   │
│   │   ├── context/
│   │   │   └── SessionContext.jsx  
│   │   │
│   │   ├── pages/
│   │   │   ├── admin/
│   │   │   │   ├── AdminLayout.jsx
│   │   │   │   ├── AdminDashboard.jsx
│   │   │   │   ├── LiveSessions.jsx
│   │   │   │   ├── HighRiskSessions.jsx
│   │   │   │   ├── SessionDetail.jsx     
│   │   │   │   ├── ActionHistory.jsx
│   │   │   │   ├── Analytics.jsx
│   │   │   │   └── Admin.css
│   │   │   │
│   │   │   ├── Cart.jsx             
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Shop.jsx
│   │   │   ├── Auth.css
│   │   │   └── Cart.css
│   │   │
│   │   ├── App.jsx                
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── ml/
│   ├── datasets/                  
│   ├── realtime/
│   │   ├── realtime_features.py    
│   │   ├── risk_scorer.py           
│   │   ├── scenario_detector.py    
│   │   └── action_engine.py         
│   │
│   ├── saved_models/
│   │   └── xgboost.pkl              
│   │
│   ├── feature_engineering.py
│   ├── preprocessing.py
│   ├── xgboost_model.py
│   └── ...
│
├── .gitignore
└── README.md

---

---

## User Roles


Role                       Access
Customer                   Home, Shop, Cart, Checkout, Payment, Login, RegisterSuper AdminFull Admin Dashboard + ability to visit Shop
Super Admin                Credentials


## Default Super Admin Credentials
textEmail   : admin@cartrescue.ai
Password: Admin@123


---

# Machine Learning

## Pipeline

Session Events
      ↓
Feature Generation
      ↓
XGBoost Risk Scorer
      ↓
Scenario Detector
      ↓
Action Engine
      ↓
Final Decision (Risk + Scenario + Recommended Action)


### Features Used

- Number of Events
- Product Views
- Add to Cart Count
- Checkout Started
- Payment Attempts / Failures
- Cart Value
- Average & Max Price

### Prediction Output

- Risk Score
- Predicted Reason
- Recommended Action

### Risk Levels

- HIGH
- MEDIUM
- LOW

### Detected Scenarios

- Payment Failure
- Checkout Hesitation
- Price Sensitivity
- Shipping Friction
- Form Friction
- Cart Abandonment Risk
- Browsing


---

# Decision Agent

Possible recommendations include:

- Do Nothing
- Send Reminder
- Retry Payment
- Offer Discount Coupon
- Offer Free Shipping
- Customer Support Assistance

NO_ACTION
SEND_CART_REMINDER
SHOW_EXIT_INTENT_POPUP
SHOW_LIMITED_TIME_DISCOUNT
OFFER_FREE_SHIPPING
OFFER_COD_OR_ALTERNATE_PAYMENT
SHOW_TRUST_BADGES_AND_REVIEWS
SHOW_PERSONALIZED_RECOMMENDATION

When Super Admin Accepts an action, the system can trigger:
Twilio SMS

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/Hackathon1.git
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

# Team

Developed by

- P. Nithish
- Tallapaneni Sri Dhruti
- Akhilakoppolu

---

Thank you for taking the time to review our project.
