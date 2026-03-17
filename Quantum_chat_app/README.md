# ⚜️ SANDESH: Quantum-Secure Communication ⚜️

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb)

> **"Defeating the 'Harvest Now, Decrypt Later' threat through Sub-atomic Encryption Laws."**

SANDESH is a proof-of-concept, real-time, end-to-end encrypted messaging platform. It simulates the **BB84 Quantum Key Distribution (QKD)** protocol to provide absolute cryptographic security, ensuring that any attempt at network eavesdropping instantly collapses the communication channel.

---

## 🚀 The Arsenal (Key Features)

* **⚛️ BB84 Protocol Simulation (Intrusion Detection):** Employs the laws of quantum mechanics (Heisenberg's Uncertainty Principle). If an eavesdropper (Eve) intercepts the channel, the quantum state collapses, instantly alerting the users and destroying the compromised key.
* **🛡️ Defense-in-Depth Architecture:** Combines global WSS (WebSocket Secure) tunneling via Ngrok/Pinggy with heavy AES/Custom payload encryption.
* **🥷 Cryptographic Camouflage (Metadata Shielding):** Defeats Traffic Analysis. All network packets are padded to a constant length (Constant-Length Padding). Dummy traffic is dropped entirely at the application layer to prevent database bloat.
* **Vault of Silence (Zero-Knowledge DB):** Integrates with MongoDB. The backend acts strictly as a blind relay—storing only sealed ciphertext. The server never holds the decryption keys.
* **⚡ Real-Time Full-Duplex Sync:** Built on FastAPI WebSockets and a state-persistent Streamlit reactive UI for zero-latency communication.

---

## 🏗️ Technical Architecture

1. **Frontend:** Streamlit (Reactive UI, Session State Management)
2. **Backend Engine:** FastAPI (WebSocket Routers, Async I/O)
3. **Quantum Layer:** Custom Python implementation of BB84 basis generation and error-rate checking.
4. **Database:** MongoDB (Motor/PyMongo)
5. **Reverse Proxy:** Ngrok & Pinggy for global deployment.

---

## ⚙️ Local Setup & Deployment

Want to host your own Quantum Chamber? Follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/anandpiyush121-goat/SANDESH-Quantum-Secure.git
cd SANDESH-Quantum-Secure
