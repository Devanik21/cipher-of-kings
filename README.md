# Cipher Of Kings

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square) ![Stars](https://img.shields.io/github/stars/Devanik21/cipher-of-kings?style=flat-square&color=yellow) ![Forks](https://img.shields.io/github/forks/Devanik21/cipher-of-kings?style=flat-square&color=blue) ![Author](https://img.shields.io/badge/Author-Devanik21-black?style=flat-square&logo=github) ![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> A cryptographic puzzle adventure — decode historical and modern ciphers, solve layered ARG-style challenges, and learn the mathematics of secrecy.

---

**Topics:** `classical-ciphers` · `caesar-cipher` · `deep-learning` · `game` · `information-theory` · `puzzle` · `python` · `security` · `vigenere-cipher` · `historical-cryptography`

## Overview

Cipher of Kings is an interactive cryptographic puzzle platform that combines historical storytelling
with rigorous cryptanalysis education. Players progress through a narrative spanning five eras of
cryptographic history — Ancient (Caesar, Atbash, Polybius), Renaissance (Vigenère, Beaufort, Playfair),
Industrial (Enigma, SIGABA), Modern Symmetric (AES, DES), and Public Key (RSA, Elliptic Curve) —
solving progressively more complex cipher challenges to advance the plot.

Each cipher challenge is presented in a story context: a coded message intercepted from a historical
figure, a wartime communication that must be decoded before an enemy advances, or a modern encrypted
transmission. The puzzle mechanic requires understanding the cipher's mathematical structure to find
the solution — not brute-force guessing. Frequency analysis tools, index of coincidence calculators,
and Kasiski examination utilities are provided as in-game instruments that teach cryptanalysis while
solving the puzzle.

Beyond the narrative puzzles, the platform includes a cryptographic laboratory for free-form
experimentation: encrypt and decrypt arbitrary text with any supported cipher, visualise the
substitution and permutation operations step by step, compare ciphertext entropy across algorithms,
and explore how cipher parameters (key length, number of rounds) affect security properties.

---

## Motivation

Cryptography is the mathematical foundation of all digital privacy and security, yet its history is
one of the most compelling intellectual stories in human civilisation — from Caesar's battlefield
dispatches to the Enigma battles of World War II to the public key revolution that enabled the internet.
Cipher of Kings was built to make that history and those mathematics genuinely engaging through
interactive puzzle play, not passive reading.

---

## Architecture

```
Narrative Engine (story state machine)
        │
  Puzzle Layer (cipher challenge per chapter)
  ├── Cipher implementation (encrypt/decrypt)
  ├── Cryptanalysis tools (freq analysis, IC)
  └── Hint system (progressive reveals)
        │
  Progress system (chapter unlock, leaderboard)
        │
  Cryptographic Laboratory (free exploration mode)
        │
  Streamlit / Pygame frontend
```

---

## Features

### Five-Era Narrative Campaign
25-chapter story spanning Ancient Greece to modern public key cryptography, with each era unlocking new cipher types and more complex analytical challenges.

### Historical Cipher Implementations
Fully functional implementations of 15+ classical ciphers: Caesar, ROT13, Atbash, Vigenère, Beaufort, Playfair, Four-Square, Polybius, ADFGX, Rail Fence, Enigma (simplified), and more.

### Cryptanalysis Toolkit
Frequency analysis charts (letter frequency histogram), Index of Coincidence calculator, Kasiski examination for Vigenère period detection, and chi-squared goodness-of-fit test for key length estimation.

### Step-by-Step Cipher Visualisation
Animated visualisation of encryption operations: Caesar wheel rotation, Vigenère tableau lookup, Playfair square construction — making the mathematical operations concrete and learnable.

### Modern Cryptography Module
Educational implementations (not production-safe) of DES, AES (ECB/CBC/CTR), RSA key generation and encryption, and elliptic curve Diffie-Hellman for the advanced chapters.

### Progressive Hint System
Three-tier hint system per puzzle: conceptual hint (cipher type identification), technical hint (key structure), and solution path (step-by-step guide) — each level costs accumulated in-game points.

### Cryptographic Laboratory
Free-form workbench for encrypting and decrypting text with any supported cipher, comparing ciphertext statistics, and exploring how key changes affect output.

### Leaderboard and Achievements
Time-to-solve tracking, achievement badges for completing chapters without hints, and an optional online leaderboard for competitive play.

---

## Tech Stack

| Library / Tool | Role | Why This Choice |
|---|---|---|
| **Python (cryptography)** | Cipher implementations | Classical and modern cipher algorithms |
| **Streamlit** | Game UI | Puzzle interface, cipher laboratory, progress tracking |
| **PyCryptodome** | Modern crypto | AES, RSA implementations for advanced chapters |
| **Matplotlib / Plotly** | Cryptanalysis vis | Letter frequency histograms, IC curves |
| **SQLite** | Game state | Player progress, hint usage, achievement storage |
| **NumPy** | Mathematical ops | Modular arithmetic, matrix operations for Playfair |

---

## Getting Started

### Prerequisites

- Python 3.9+ (or Node.js 18+ for TypeScript/JavaScript projects)
- A virtual environment manager (`venv`, `conda`, or equivalent)
- API keys as listed in the Configuration section

### Installation

```bash
git clone https://github.com/Devanik21/cipher-of-kings.git
cd cipher-of-kings
python -m venv venv && source venv/bin/activate
pip install streamlit pycryptodome matplotlib plotly numpy pandas
streamlit run app.py
```

---

## Usage

```bash
# Start the game
streamlit run app.py

# Cryptanalysis standalone tools
python analyse.py --text 'KHOOR ZRUOG' --method frequency
python kasiski.py --ciphertext 'LXFOPVEFRNHR...' --min_key 3 --max_key 20

# Encrypt/decrypt a message
python cipher.py --cipher vigenere --key SECRET --encrypt 'HELLO WORLD'
python cipher.py --cipher vigenere --key SECRET --decrypt 'ZINCS PGVNU'
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `PLAYER_DB` | `game_data.sqlite` | SQLite database for player progress |
| `HINT_COST` | `10` | Points deducted per hint used |
| `LEADERBOARD_ENABLED` | `False` | Enable online leaderboard (requires server) |
| `START_CHAPTER` | `1` | Starting chapter (1–25) |

> Copy `.env.example` to `.env` and populate required values before running.

---

## Project Structure

```
cipher-of-kings/
├── README.md
├── requirements.txt
├── app.py
└── ...
```

---

## Roadmap

- [ ] ARG (Alternate Reality Game) mode: real-world cipher challenges embedded in QR codes, images, and web pages
- [ ] Collaborative multiplayer mode: team of 2–4 players solving layered multi-cipher challenges together
- [ ] Cipher design mode: create and share custom cipher challenges with the community
- [ ] Post-quantum cryptography chapter: lattice-based and hash-based signature schemes
- [ ] Mobile app with camera-based cipher scanning for physical object integration

---

## Contributing

Contributions, issues, and suggestions are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-idea`
3. Commit your changes: `git commit -m 'feat: add your idea'`
4. Push to your branch: `git push origin feature/your-idea`
5. Open a Pull Request with a clear description

Please follow conventional commit messages and add documentation for new features.

---

## Notes

Modern cryptographic implementations in this project are educational and intentionally simplified. They are NOT safe for production security use. Never use educational crypto code for real encryption of sensitive data — use well-audited libraries like libsodium or the Python cryptography package instead.

---

## Author

**Devanik Debnath**  
B.Tech, Electronics & Communication Engineering  
National Institute of Technology Agartala

[![GitHub](https://img.shields.io/badge/GitHub-Devanik21-black?style=flat-square&logo=github)](https://github.com/Devanik21)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-devanik-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/devanik/)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with curiosity, depth, and care — because good projects deserve good documentation.*
