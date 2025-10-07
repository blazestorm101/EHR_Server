# 🚀 ESP32 Monitor Server

A robust Flask-based server for monitoring ESP32 devices, handling button presses, emergency messages, and providing a RESTful API for Android applications.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supported-blue.svg)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46a2f1.svg)

## 📖 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [ESP32 Integration](#-esp32-integration)
- [Mobile App](#-mobile-app)
- [Development](#-development)
- [Contributing](#-contributing)

## ✨ Features

### 🔐 Authentication & Security
- **JWT-based authentication** with secure token management
- **User registration & login** with password hashing
- **Protected API endpoints** with role-based access

### 📱 ESP32 Integration
- **Real-time data ingestion** from ESP32 devices
- **Button press tracking** with timestamps and locations
- **Emergency message handling** with severity levels
- **Device management** for multiple ESP32 devices

### 📊 Monitoring & Analytics
- **Live dashboard** with real-time statistics
- **Historical data** tracking and analysis
- **Emergency alert system** with acknowledgment
- **Device status monitoring**

### 🚀 Deployment & Scalability
- **Cloud-ready** architecture for Render deployment
- **PostgreSQL database** for production scalability
- **RESTful API design** for easy integration
- **CORS enabled** for cross-origin requests

## 🏗️ Architecture

```mermaid
graph TB
    A[ESP32 Devices] --> B[Flask Server]
    C[Android App] --> B
    B --> D[PostgreSQL Database]
    B --> E[Render Cloud]
    
    subgraph "ESP32 Monitor Server"
        B --> F[Auth System]
        B --> G[API Routes]
        B --> H[Data Models]
    end