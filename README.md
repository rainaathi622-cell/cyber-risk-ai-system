# Cyber Risk AI System

## Problem Statement
AI-powered continuous cybersecurity risk assessment system that monitors 
organizational assets, scores vulnerabilities using CVE data, and recommends 
where to allocate security budget for maximum risk reduction.

## Tech Stack
- Frontend: React.js + TypeScript + Tailwind CSS + Recharts
- Backend: Python FastAPI
- Database: PostgreSQL (via Supabase)
- Authentication: JWT (python-jose, passlib/bcrypt)
- Data Source: NVD CVE API

## Features
- Real-time asset and vulnerability tracking
- AI-driven risk scoring (context-aware: CVSS + criticality + exposure + patch status)
- Budget-optimized fix recommendations (greedy algorithm)
- Interactive dashboard with charts, filtering, and critical alerts
- JWT authentication with protected routes
- Responsive design (mobile/tablet/desktop)
- Resilient database connections with automatic retry logic

## Progress

### Complete ✅ (Days 1-23)
- Full backend: FastAPI, PostgreSQL, real CVE data integration
- Risk scoring engine with explainable formula
- Budget optimization engine
- React frontend: Dashboard, Assets, Budget, Login - all connected to real data
- JWT authentication with protected routes and logout
- Responsive design across all pages
- Critical risk alert banners
- Test data cleaned up, system reviewed

### Up Next - Continuous Monitoring & Testing 🚧
- Scheduled auto-refresh of CVE data and risk scores
- End-to-end testing and edge case handling
- Deployment preparation

## Status
🚧 Under Development - Day 23 of 40