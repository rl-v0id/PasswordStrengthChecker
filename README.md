# 🔒 Password Strength Checker

## Introduction

Welcome to the **Password Strength Checker**, a powerful and user-friendly tool designed to help you evaluate and improve the security of your passwords. Built with Streamlit, this application provides real-time feedback, actionable suggestions, and a secure password generator to ensure your online accounts remain safe from unauthorized access.

Whether you're creating a new password or testing an existing one, this tool offers:
- **Real-time analysis** of password strength against **40,000+ common passwords**.
- **Entropy calculation** to measure unpredictability and randomness.
- **Visual strength meter** with color-coded feedback and animations.
- **Actionable tips** and specific suggestions to enhance password security.
- **Secure password generation** with fully customizable character sets.
- **Encrypted local history** to track your password security improvements over time.

---

## 🚀 Features

### Core Functionality
- **Real-time Analysis**: Password strength updates instantly as you type with verbose feedback.
- **Comprehensive Scoring**: Advanced 0-100 point scoring system with detailed breakdown and explanations.
- **Visual Feedback**: Animated color-coded strength meter with glassmorphism design and progress animations.
- **Actionable Suggestions**: AI-powered specific recommendations to improve password security.
- **Secure Generator**: Cryptographically secure password generation with full customization options.
- **Privacy-First**: All analysis happens locally - your passwords never leave your device.

### Security Checks
- ✅ **Length Analysis**: Minimum 8 characters, bonus for 12+.
- ✅ **Character Variety**: Uppercase, lowercase, numbers, special characters.
- ✅ **Pattern Detection**: Identifies repeating characters and simple sequences.
- ✅ **Dictionary Words**: Checks against **40,000+ most common passwords** from comprehensive wordlists.
- ✅ **Entropy Calculation**: Measures password unpredictability using advanced algorithms.
- ✅ **Keyboard Patterns**: Detects common patterns like "qwerty" or "123456".
- ✅ **Advanced Analysis**: Sophisticated pattern matching and security vulnerability detection.

### 🗄️ Password Database
This tool includes a comprehensive database of **40,000+ most commonly used passwords** sourced from:
- Major data breaches and leaked password databases
- Common password patterns and variations
- Dictionary words and their common substitutions
- Sequential patterns and keyboard layouts
- Industry-standard security wordlists

The database is stored in `list.txt` and is regularly updated to include new common password patterns discovered in security research.

### 🎨 User Interface
- **Modern Glassmorphism Design**: Beautiful acrylic glass effects with backdrop blur
- **Animated Progress Bars**: Smooth animations and visual feedback
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Dark/Light Compatibility**: Optimized for all viewing preferences
- **Accessibility**: Full keyboard navigation and screen reader support

---

## 🔐 Password Strength History (Encrypted & Local)

### Security Features
- **Dual Storage Format**: Stores both encrypted passwords (for optional viewing) and SHA-256 hashes for security.
- **Fernet Encryption**: Uses industry-standard Fernet symmetric encryption from the `cryptography` library.
- **Local-Only Storage**: All data is saved locally in your home directory - never transmitted anywhere.
- **Key Management**: Automatically generates and manages encryption keys securely.
- **Privacy Controls**: View/hide actual passwords with individual toggle controls for each entry.

### What's Stored
- ✅ Encrypted password (can be decrypted and viewed locally)
- ✅ SHA-256 hash (for security verification)
- ✅ Password strength score (0-100)
- ✅ Strength category (Very Weak to Very Strong)
- ✅ Analysis timestamp

### Usage
- Click **"📋 Show My Password History"** to view your encrypted password history.
- Use the **👁️ eye icon** next to each entry to reveal/hide the actual password.
- Export your history to a text file for backup purposes.
- Clear all history with the **🗑️ Clear History** button (requires confirmation).

**Security Note:** All encryption/decryption happens locally. Your passwords are never sent to any external servers.

---

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/rl-v0id/PasswordStrengthChecker.git
   cd PasswordStrengthChecker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python run.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

---

## ⚙️ Technical Specifications

### Built With
- **Frontend**: Streamlit with custom HTML/CSS and JavaScript
- **Backend**: Python 3.7+ with advanced security libraries
- **Encryption**: Fernet (cryptography library) for secure local storage
- **Styling**: Custom glassmorphism CSS with backdrop-filter effects
- **Password Analysis**: Multi-layered security algorithms

### Dependencies
- `streamlit` - Web application framework
- `cryptography` - Fernet encryption for secure password storage
- `hashlib` - SHA-256 hashing for password verification
- `secrets` - Cryptographically secure random number generation
- `string` - Character set management for password generation
- `os` - File system operations for local storage
- `random` - Password shuffling and randomization

### Performance
- **Real-time Analysis**: Sub-100ms password analysis response time
- **Database Lookup**: Optimized O(1) lookup against 40,000+ password database
- **Memory Efficient**: Minimal RAM usage with efficient data structures
- **Local Processing**: No network requests ensure instant feedback

---

## 📋 Usage

### Password Analysis
1. **Enter Your Password**: Type your password in the secure input field (hidden from view).
2. **Real-time Feedback**: Watch the strength meter update instantly with verbose explanations.
3. **Review Analysis**: Check detailed breakdown including:
   - Password strength score (0-100)
   - Entropy calculation (in bits)
   - Character length and variety
   - Specific security recommendations
4. **View History**: Access your encrypted password history to track improvements.

### Password Generation
1. **Set Preferences**: Choose character types (uppercase, lowercase, numbers, symbols).
2. **Adjust Length**: Select password length (8-32 characters).
3. **Generate**: Click "🎲 Generate Secure Password" for cryptographically secure passwords.
4. **Test Generated Password**: Copy and analyze your new password in the strength checker.

### Security Best Practices
- Use the built-in suggestions to improve weak passwords
- Aim for "Strong" or "Very Strong" ratings
- Enable different character types for maximum security
- Use unique passwords for each account
- Consider using a password manager for storage

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this tool, please fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## 🛡️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

For any inquiries or feedback, feel free to reach out:
- **Email**: rlcenzo777@gmail.com
- **GitHub**: [rl-v0id](https://github.com/your-username)

---

🌟 **Star this repository if you found it helpful!**
