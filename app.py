import streamlit as st
import re
import math
from collections import Counter
import string
import requests
import base64
import os
import sys
import getpass
import secrets
import random
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Configure page settings
st.set_page_config(
    page_title="Password Strength Checker",
    page_icon="🔒",
    layout="wide"
)

# Enhanced styling with beautiful gradient background
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main background with light animated gradient */
    .stApp {
        background: linear-gradient(-45deg, #e8f5e8, #e3f2fd, #fce4ec, #fff3e0, #f3e5f5, #e0f2f1);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
    }
    
    /* Gradient animation */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Content container with high contrast */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        padding: 2rem;
        margin: 1rem auto;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        max-width: 1200px;
    }
    
    /* Light floating elements background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(76, 175, 80, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Enhanced typography with high contrast */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        color: #1a202c !important;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(255, 255, 255, 0.8);
    }
    
    p, span, div {
        font-family: 'Inter', sans-serif !important;
        color: #2d3748 !important;
        font-weight: 500;
    }
    
    /* Dark text in expander sections for better readability */
    .stExpander [data-testid="stMarkdownContainer"] p,
    .stExpander [data-testid="stMarkdownContainer"] span,
    .stExpander [data-testid="stMarkdownContainer"] div,
    .stExpander [data-testid="stMarkdownContainer"] strong {
        color: #1a202c !important;
        font-weight: 600;
    }
    
    /* Override Streamlit's color inheritance */
    .element-container [data-testid="stMarkdownContainer"] p,
    .element-container [data-testid="stMarkdownContainer"] span,
    .element-container [data-testid="stMarkdownContainer"] div {
        color: inherit !important;
    }
    
    /* High contrast input styling */
    .stTextInput > div > div > input {
        background: white !important;
        border: 3px solid #4facfe;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 16px;
        font-weight: 500;
        color: #1a202c !important;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00f2fe;
        box-shadow: 0 0 0 4px rgba(0, 242, 254, 0.2);
        background: white !important;
        outline: none;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
        font-family: 'Inter', sans-serif;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* High contrast metric containers */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(79, 172, 254, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #1a202c !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        color: #4a5568 !important;
        font-weight: 600 !important;
    }
    
    /* Enhanced progress bar */
    .stProgress > div > div > div {
        border-radius: 10px;
        background: linear-gradient(90deg, #ff4757, #ffa502, #2ed573);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Light expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(79, 172, 254, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(5px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide material icons and unwanted text */
    .material-icons-text,
    span[class*="material-icons"],
    .streamlit-expanderHeader .e1fqkh3o0,
    .streamlit-expanderHeader .e1fqkh3o1,
    .streamlit-expanderHeader .e1fqkh3o2,
    .streamlit-expanderHeader .e1fqkh3o3,
    .css-1cpxqw2 {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        font-size: 0 !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
    }
    
    /* Hide any span that might contain keyboard arrow text */
    .streamlit-expanderHeader span[data-baseweb] {
        display: none !important;
    }
    
    /* Aggressive hiding of expander icons */
    .streamlit-expanderHeader > div > div:last-child {
        display: none !important;
    }
    
    /* Hide all potential icon containers in expanders */
    .streamlit-expanderHeader [class*="css-"],
    .streamlit-expanderHeader [data-testid*="stMarkdown"] ~ *,
    .streamlit-expanderHeader span:not([class*="stMarkdown"]) {
        display: none !important;
        font-size: 0 !important;
        opacity: 0 !important;
        visibility: hidden !important;
    }
    
    /* More aggressive targeting of Streamlit expander icons */
    .streamlit-expanderHeader svg,
    .streamlit-expanderHeader [data-testid="expanderToggle"],
    .streamlit-expanderHeader button,
    .streamlit-expanderHeader [role="button"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* ABSOLUTE NUCLEAR OPTION - Target the exact problematic text */
    * {
        text-rendering: optimizeSpeed !important;
    }
    
    *:not([data-testid="stMarkdownContainer"]):not([data-testid="stMarkdownContainer"] *):not(.stMarkdown):not(.stMarkdown *):not(h1):not(h2):not(h3):not(h4):not(h5):not(h6):not(p):not(span):not(strong):not(em):not(code):not(pre):not(ul):not(ol):not(li):not(div[data-testid="stMarkdownContainer"]):not(div[data-testid="stMarkdownContainer"] *) {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Hide any text that could be keyboard_arrow */
    *::before, *::after {
        content: none !important;
    }
    
    [data-testid="stExpander"] *:not([data-testid="stMarkdownContainer"]):not([data-testid="stMarkdownContainer"] *):not(h1):not(h2):not(h3):not(h4):not(h5):not(h6):not(p):not(span[data-testid="stMarkdownContainer"]):not(strong):not(em):not(code):not(pre):not(ul):not(ol):not(li):not(.stMarkdown):not(.stMarkdown *):not(div[data-testid="stMarkdownContainer"]):not(div[data-testid="stMarkdownContainer"] *) {
        color: transparent !important;
        font-size: 0px !important;
        line-height: 0 !important;
        height: 0px !important;
        width: 0px !important;
        max-height: 0px !important;
        max-width: 0px !important;
        overflow: hidden !important;
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        text-indent: -9999px !important;
    }
    
    /* Specifically target the problematic element from screenshot */
    [data-testid="stExpander"] div:not([data-testid="stMarkdownContainer"]):not(.stMarkdown) {
        font-size: 0 !important;
        line-height: 0 !important;
        color: transparent !important;
        display: none !important;
    }
    
    /* Hide any element that might contain keyboard_arrow text */
    [class*="css-"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    [class*="css-"]:not([data-testid="stMarkdownContainer"]) {
        color: transparent !important;
        font-size: 0 !important;
    }
    
    /* Target specific Streamlit classes that might show icons as text */
    .css-1cpxqw2,
    .css-16huue1,
    .css-1d391kg,
    .css-10trblm {
        font-size: 0 !important;
        color: transparent !important;
        display: none !important;
    }
    
    /* Light sidebar */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 2px solid rgba(79, 172, 254, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* High contrast code blocks */
    .stCode {
        background: rgba(26, 32, 44, 0.95) !important;
        border-radius: 10px;
        border: 2px solid rgba(79, 172, 254, 0.3);
        backdrop-filter: blur(5px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .stCode code {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    /* Enhanced tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid rgba(79, 172, 254, 0.3);
        backdrop-filter: blur(5px);
        color: #1a202c !important;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4facfe, #00f2fe) !important;
        color: white !important;
        font-weight: 700;
        box-shadow: 0 4px 20px rgba(79, 172, 254, 0.4);
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    /* Checkboxes and sliders */
    .stCheckbox > label {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8, #6a42a0);
    }
    
    /* Subtle animations */
    .element-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* High contrast alert boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(79, 172, 254, 0.4);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    .stAlert [data-testid="stMarkdownContainer"] {
        color: #1a202c !important;
        font-weight: 500;
    }
    
    /* Success alerts */
    .stSuccess {
        border-color: rgba(46, 213, 115, 0.6) !important;
        background: rgba(212, 243, 223, 0.95) !important;
    }
    
    /* Error alerts */
    .stError {
        border-color: rgba(255, 71, 87, 0.6) !important;
        background: rgba(254, 226, 226, 0.95) !important;
    }
    
    /* Warning alerts */
    .stWarning {
        border-color: rgba(255, 165, 2, 0.6) !important;
        background: rgba(255, 243, 205, 0.95) !important;
    }
    
    /* Force all 4 checkboxes in one horizontal line with MASSIVE spacing */
    div[data-testid="column"] {
        flex: 1 1 25% !important;
        max-width: none !important;
        min-width: 300px !important;
        margin-right: 150px !important;
        padding-right: 60px !important;
        padding-left: 40px !important;
        overflow: visible !important;
    }
    
    div[data-testid="column"]:last-child {
        margin-right: 0 !important;
        padding-right: 0 !important;
    }
    
    /* Ensure container doesn't wrap */
    .stColumn {
        display: flex !important;
        flex-direction: column !important;
        flex-shrink: 0 !important;
    }
    
    /* Fix checkbox text display */
    .stCheckbox {
        margin-bottom: 8px !important;
        white-space: nowrap !important;
        flex-shrink: 0 !important;
    }
    
    .stCheckbox > label {
        font-size: 0.9em !important;
        padding: 6px 8px !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        overflow: visible !important;
        display: flex !important;
        align-items: center !important;
        flex-direction: row !important;
        text-overflow: ellipsis !important;
    }
    
    .stCheckbox > label > div {
        white-space: nowrap !important;
        word-wrap: normal !important;
        overflow: visible !important;
    }
    
    /* Ensure the main container stays horizontal */
    .element-container .stColumn {
        display: inline-block !important;
        width: auto !important;
        vertical-align: top !important;
    }
</style>

<script>
    // IMMEDIATE NUCLEAR TEXT REPLACEMENT
    (function() {
        // Function to aggressively remove keyboard arrow text
        function nukeKeyboardText() {
            // Replace all instances of keyboard_arrow text in the entire document
            const bodyHTML = document.body.innerHTML;
            if (bodyHTML.includes('keyboard_arrow')) {
                document.body.innerHTML = bodyHTML
                    .replace(/keyboard_arrow_right/gi, '')
                    .replace(/keyboard_arrow_down/gi, '')
                    .replace(/keyboard_arrow_up/gi, '')
                    .replace(/keyboard_arrow_left/gi, '')
                    .replace(/keyboard_arrow/gi, '');
            }
        }
        
        // Run immediately
        nukeKeyboardText();
        
        // Run on DOM ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', nukeKeyboardText);
        }
        
        // Hide any existing keyboard arrow text immediately with CSS
        const style = document.createElement('style');
        style.innerHTML = `
            * {
                font-family: 'Inter', sans-serif !important;
            }
            body *:not([data-testid*="stMarkdown"]):not([data-testid="stMarkdownContainer"]):not([data-testid="stMarkdownContainer"] *):not(.stMarkdown):not(.stMarkdown *):not(h1):not(h2):not(h3):not(h4):not(h5):not(h6):not(p):not(span[data-testid*="stMarkdown"]):not(strong):not(em):not(code):not(pre):not(ul):not(ol):not(li) {
                color: transparent !important;
                font-size: 0 !important;
                visibility: hidden !important;
                display: none !important;
            }
            .streamlit-expanderHeader * {
                display: none !important;
                visibility: hidden !important;
            }
            .streamlit-expanderHeader {
                overflow: hidden !important;
            }
            [data-testid="stExpander"] > div > div:last-child {
                display: none !important;
            }
        `;
        document.head.appendChild(style);
        
        // Continuous text replacement
        setInterval(nukeKeyboardText, 10);
    })();

    // Aggressive function to remove keyboard_arrow_right text
    function hideKeyboardArrowText() {
        // Target all possible selectors where the text might appear
        const selectors = [
            '*',
            '[data-testid*="element"]',
            '.streamlit-expanderHeader *',
            '.stExpander *',
            '.css-1cpxqw2',
            '.e1fqkh3o0',
            '.e1fqkh3o1',
            '.e1fqkh3o2',
            '.e1fqkh3o3',
            'span',
            'div'
        ];
        
        selectors.forEach(selector => {
            try {
                const elements = document.querySelectorAll(selector);
                elements.forEach(element => {
                    if (element && element.textContent) {
                        const text = element.textContent.trim();
                        if (text.includes('keyboard_arrow') || 
                            text === 'keyboard_arrow_right' || 
                            text === 'keyboard_arrow_down' ||
                            text === 'keyboard_arrow_up' ||
                            text === 'keyboard_arrow_left' ||
                            text === 'keyboard_arrow' || element.innerHTML.includes('keyboard_arrow')) {
                            
                            // Multiple approaches to hide the element
                            element.style.cssText = 'display: none !important; visibility: hidden !important; opacity: 0 !important; font-size: 0 !important; height: 0 !important; width: 0 !important; overflow: hidden !important;';
                            element.textContent = '';
                            element.innerHTML = '';
                            
                            // Try to remove the element completely
                            if (element.parentNode) {
                                element.parentNode.removeChild(element);
                            }
                        }
                    }
                });
            } catch (e) {
                // Ignore selector errors
            }
        });
        
        // Also hide any material-icons or similar classes
        const materialIcons = document.querySelectorAll('[class*="material"], [class*="icon"], [data-testid*="icon"]');
        materialIcons.forEach(element => {
            if (element.textContent && 
                (element.textContent.includes('keyboard_arrow') || 
                 element.textContent.includes('expand') ||
                 element.textContent.includes('chevron'))) {
                element.style.display = 'none !important';
                element.remove();
            }
        });
        
        // Additional cleanup for any text nodes containing keyboard_arrow
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        const textNodesToRemove = [];
        let node;
        while (node = walker.nextNode()) {
            if (node.nodeValue && node.nodeValue.includes('keyboard_arrow')) {
                textNodesToRemove.push(node);
            }
        }
        
        textNodesToRemove.forEach(textNode => {
            if (textNode.parentNode) {
                textNode.parentNode.removeChild(textNode);
            }
        });
    }
    
    // Run immediately and repeatedly
    hideKeyboardArrowText();
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', hideKeyboardArrowText);
    } else {
        hideKeyboardArrowText();
    }
    
    // Run very frequently to catch all dynamic content
    setInterval(hideKeyboardArrowText, 100);
    
    // Also run on window load
    window.addEventListener('load', hideKeyboardArrowText);
    
    // Enhanced MutationObserver
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            let shouldRun = false;
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' || mutation.type === 'characterData') {
                    shouldRun = true;
                }
            });
            if (shouldRun) {
                setTimeout(hideKeyboardArrowText, 10);
            }
        });
        
        // Start observing the entire document
        observer.observe(document.documentElement, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true
        });
    }
</script>
""", unsafe_allow_html=True)

import os

# Load common passwords from list.txt (40k+ most used passwords)
COMMON_PASSWORDS = set()
list_path = os.path.join(os.path.dirname(__file__), "list.txt")
try:
    with open(list_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            pwd = line.strip().lower()
            if pwd:
                COMMON_PASSWORDS.add(pwd)
except Exception as e:
    st.warning(f"Could not load common password list: {e}")

# --- Master Password Management ---
def get_master_password_file():
    """Get the master password hash file path"""
    project_dir = os.path.dirname(__file__)
    history_dir = os.path.join(project_dir, "user_data")
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    return os.path.join(history_dir, "master.hash")

def get_salt_file():
    """Get the salt file path"""
    project_dir = os.path.dirname(__file__)
    history_dir = os.path.join(project_dir, "user_data")
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    return os.path.join(history_dir, "salt.key")

def create_master_password():
    """Create a new master password"""
    print("\n🔐 Setting up Master Password")
    print("=" * 50)
    print("This master password will encrypt your password history.")
    print("⚠️  Important: If you forget this password, your history will be lost!")
    print("=" * 50)
    
    while True:
        password1 = getpass.getpass("Enter new master password: ")
        if len(password1) < 8:
            print("❌ Master password must be at least 8 characters long!")
            continue
        
        password2 = getpass.getpass("Confirm master password: ")
        if password1 != password2:
            print("❌ Passwords don't match! Try again.")
            continue
            
        # Generate salt and hash
        salt = os.urandom(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        password_hash = kdf.derive(password1.encode())
        
        # Save salt and hash
        with open(get_salt_file(), "wb") as f:
            f.write(salt)
        with open(get_master_password_file(), "wb") as f:
            f.write(password_hash)
        
        print("✅ Master password created successfully!")
        return True

def verify_master_password():
    """Verify the master password"""
    if not os.path.exists(get_master_password_file()) or not os.path.exists(get_salt_file()):
        return create_master_password()
    
    print("\n🔐 Master Password Required")
    print("=" * 30)
    
    # Load salt and stored hash
    with open(get_salt_file(), "rb") as f:
        salt = f.read()
    with open(get_master_password_file(), "rb") as f:
        stored_hash = f.read()
    
    max_attempts = 3
    for attempt in range(max_attempts):
        password = getpass.getpass(f"Enter master password (attempt {attempt + 1}/{max_attempts}): ")
        
        # Derive key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        try:
            password_hash = kdf.derive(password.encode())
            if password_hash == stored_hash:
                print("✅ Master password verified!")
                return True
        except:
            pass
        
        if attempt < max_attempts - 1:
            print("❌ Incorrect password. Try again.")
        else:
            print("❌ Too many failed attempts. Exiting...")
    
    return False

def change_master_password():
    """Change the master password"""
    if not verify_master_password():
        return False
    
    print("\n🔄 Changing Master Password")
    print("=" * 30)
    
    # Get new password
    while True:
        new_password1 = getpass.getpass("Enter new master password: ")
        if len(new_password1) < 8:
            print("❌ Master password must be at least 8 characters long!")
            continue
        
        new_password2 = getpass.getpass("Confirm new master password: ")
        if new_password1 != new_password2:
            print("❌ Passwords don't match! Try again.")
            continue
        break
    
    # Generate new salt and hash
    salt = os.urandom(32)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    password_hash = kdf.derive(new_password1.encode())
    
    # Save new salt and hash
    with open(get_salt_file(), "wb") as f:
        f.write(salt)
    with open(get_master_password_file(), "wb") as f:
        f.write(password_hash)
    
    print("✅ Master password changed successfully!")
    return True

def get_encryption_key_from_master_password(master_password):
    """Derive encryption key from master password"""
    # Load salt
    salt_file = get_salt_file()
    if not os.path.exists(salt_file):
        raise FileNotFoundError("Salt file not found. Master password may not be set up properly.")
    
    with open(salt_file, "rb") as f:
        salt = f.read()
    
    # Derive key for Fernet encryption
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

# --- History feature removed by user request ---

def calculate_entropy(password):
    """Calculate password entropy"""
    if not password:
        return 0
    
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'[0-9]', password):
        charset_size += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        charset_size += 32
    
    entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0
    return round(entropy, 2)

def check_repeating_patterns(password):
    """Check for repeating characters and simple patterns"""
    issues = []
    
    # Check for consecutive repeating characters
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            issues.append("Contains 3+ consecutive repeating characters")
            break
    
    # Check for simple sequences
    sequences = ['123', '234', '345', '456', '567', '678', '789', 'abc', 'bcd', 'cde']
    for seq in sequences:
        if seq in password.lower():
            issues.append("Contains simple sequences (123, abc, etc.)")
            break
    
    # Check for keyboard patterns
    keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '1234', 'qwer']
    for pattern in keyboard_patterns:
        if pattern in password.lower():
            issues.append("Contains keyboard patterns")
            break
            
    return issues

def analyze_password_strength(password):
    """Analyze password strength and return score with details"""
    if not password:
        return 0, "No password entered", [], ""
    
    score = 0
    feedback = []
    issues = []
    
    # Length check (0-25 points)
    length = len(password)
    if length >= 12:
        score += 25
    elif length >= 8:
        score += 15
    elif length >= 6:
        score += 10
    else:
        issues.append("Password too short (minimum 8 characters)")
    
    # Character variety (0-40 points total)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>\-_+=\[\]\\\/~`]', password))
    
    char_variety = sum([has_lower, has_upper, has_digit, has_special])
    score += char_variety * 10
    
    if not has_lower:
        issues.append("Add lowercase letters")
    if not has_upper:
        issues.append("Add uppercase letters")
    if not has_digit:
        issues.append("Add numbers")
    if not has_special:
        issues.append("Add special characters (!@#$%^&*)")
    
    # Avoid common passwords (-20 points)
    if password.lower() in COMMON_PASSWORDS:
        score -= 20
        issues.append("Avoid common passwords")
    

    
    # Check for patterns (-10 points)
    pattern_issues = check_repeating_patterns(password)
    if pattern_issues:
        score -= 10
        issues.extend(pattern_issues)
    
    # Bonus for length > 12 (0-15 points)
    if length > 12:
        score += min(15, (length - 12) * 2)
    
    # Ensure score is within bounds
    score = max(0, min(100, score))
    
    # Determine strength label
    if score >= 80:
        strength_label = "Very Strong"
        color = "#00ff00"
    elif score >= 60:
        strength_label = "Strong"
        color = "#90ee90"
    elif score >= 40:
        strength_label = "Moderate"
        color = "#ffa500"
    elif score >= 20:
        strength_label = "Weak"
        color = "#ff6347"
    else:
        strength_label = "Very Weak"
        color = "#ff0000"
    
    return score, strength_label, issues, color

def generate_suggestions(issues):
    """Generate specific suggestions based on identified issues"""
    suggestions = []
    
    if "Password too short (minimum 8 characters)" in issues:
        suggestions.append("• Use at least 8 characters (12+ recommended)")
    if "Add lowercase letters" in issues:
        suggestions.append("• Include lowercase letters (a-z)")
    if "Add uppercase letters" in issues:
        suggestions.append("• Include uppercase letters (A-Z)")
    if "Add numbers" in issues:
        suggestions.append("• Include numbers (0-9)")
    if "Add special characters (!@#$%^&*)" in issues:
        suggestions.append("• Include special characters (!@#$%^&*)")
    if "Avoid common passwords" in issues:
        suggestions.append("• Avoid commonly used passwords")
    if "Avoid common dictionary words" in issues:
        suggestions.append("• Avoid dictionary words")
    if any("repeating" in issue.lower() for issue in issues):
        suggestions.append("• Avoid repeating characters")
    if any("sequence" in issue.lower() for issue in issues):
        suggestions.append("• Avoid simple sequences (123, abc)")
    if any("keyboard" in issue.lower() for issue in issues):
        suggestions.append("• Avoid keyboard patterns (qwerty)")
    
    if not suggestions:
        suggestions.append("• Your password looks good! Consider making it even longer for extra security.")
    
    return suggestions

def create_strength_meter(score, color, strength_label):
    """Create an enhanced visual strength meter with animations"""
    # Gradient colors based on strength
    gradient_colors = {
        "Very Weak": "linear-gradient(45deg, #ff4444, #cc0000)",
        "Weak": "linear-gradient(45deg, #ff6b35, #f7931e)", 
        "Moderate": "linear-gradient(45deg, #ffa500, #ff8c00)",
        "Strong": "linear-gradient(45deg, #32cd32, #228b22)",
        "Very Strong": "linear-gradient(45deg, #00ff00, #008000)"
    }
    
    gradient = gradient_colors.get(strength_label, color)
    
    # Enhanced progress bar with glow effect and animation
    progress_html = f"""
    <div style="background: linear-gradient(90deg, #e8e8e8, #f5f5f5); 
                border-radius: 15px; height: 40px; margin: 15px 0; 
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
                position: relative; overflow: hidden;">
        <div style="background: {gradient}; 
                   height: 40px; width: {score}%; 
                   border-radius: 15px; 
                   transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
                   display: flex; align-items: center; justify-content: center;
                   position: relative;
                   box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
            <span style="color: white; font-weight: bold; font-size: 16px;
                         text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                         z-index: 2; position: relative;">
                {score}%
            </span>
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                       background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                       animation: shimmer 2s infinite;"></div>
        </div>
    </div>
    
    <style>
    @keyframes shimmer {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}
    </style>
    """
    return progress_html

# --- Streamlit Session Setup (called from run.py) ---
def setup_streamlit_session():
    """Setup Streamlit session with master password"""
    # Get master password for the session
    print("\n🔐 Please enter your master password for this session:")
    master_password = getpass.getpass("Master password: ")
    
    # Verify the password
    with open(get_salt_file(), "rb") as f:
        salt = f.read()
    with open(get_master_password_file(), "rb") as f:
        stored_hash = f.read()
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    try:
        password_hash = kdf.derive(master_password.encode())
        if password_hash != stored_hash:
            print("❌ Incorrect master password!")
            return False
    except:
        print("❌ Incorrect master password!")
        return False
    
    # Store master password in environment variable for Streamlit session
    os.environ['MASTER_PASSWORD'] = master_password
    return True

# Main app
def main():
    # Initialize master password in session state
    if 'master_password' not in st.session_state:
        master_password = os.environ.get('MASTER_PASSWORD')
        if not master_password:
            st.error("🔒 **Master password not found!**")
            st.markdown("""
            ### 📋 How to fix this:
            
            **The Password Strength Checker must be started from the command line launcher.**
            
            #### ✅ Correct way to start the application:
            1. 📁 Navigate to the project folder
            2. 🐍 Run: `python run.py`  
            3. 🔑 Choose option **2** (Use the tool)
            4. 🔐 Enter your master password when prompted
            
            #### ❌ Don't run directly:
            - Don't run `python app.py` directly
            - Don't run `streamlit run app.py` directly
            - Always use the `run.py` launcher
            
            ---
            
            **💡 The launcher handles master password verification and secure session setup.**
            """)
            st.stop()
        st.session_state.master_password = master_password
    
    # Enhanced header with animated banner
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f23 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(0, 255, 0, 0.2);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(
            ellipse at center,
            rgba(0, 255, 0, 0.05) 0%,
            transparent 70%
        );
        z-index: 1;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
    }
    
    .main-title {
        text-align: center;
        margin: 0;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3.5rem;
        letter-spacing: 3px;
        background: linear-gradient(
            45deg,
            #00ff00,
            #00ccff,
            #ffffff,
            #00ccff,
            #00ff00
        );
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
        position: relative;
    }
    
    .sub-title {
        color: rgba(255,255,255,0.9);
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-size: 1.3em;
        font-family: 'Poppins', sans-serif;
        font-weight: 300;
    }
    
    @keyframes headerGlow {
        0% { box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        100% { box-shadow: 0 15px 40px rgba(102,126,234,0.4); }
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -300% 0;
        }
        50% {
            background-position: 300% 0;
        }
        100% {
            background-position: -300% 0;
        }
    }
    

    
    @keyframes borderGlow {
        0% { 
            border-color: #4facfe;
            box-shadow: 
                0 8px 32px rgba(79, 172, 254, 0.3),
                0 0 0 1px rgba(79, 172, 254, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        100% { 
            border-color: #00f2fe;
            box-shadow: 
                0 8px 32px rgba(79, 172, 254, 0.5),
                0 0 20px rgba(0, 242, 254, 0.4),
                0 0 40px rgba(79, 172, 254, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }
    }
    
    @keyframes borderGlowStrong {
        0% { 
            border-color: #4facfe;
            box-shadow: 
                0 8px 32px rgba(79, 172, 254, 0.4),
                0 0 0 1px rgba(79, 172, 254, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }
        100% { 
            border-color: #00f2fe;
            box-shadow: 
                0 12px 40px rgba(79, 172, 254, 0.6),
                0 0 30px rgba(0, 242, 254, 0.5),
                0 0 60px rgba(79, 172, 254, 0.3),
                0 0 80px rgba(0, 242, 254, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }
    }
    </style>
    
    <div class="main-header">
        <div class="header-content">
            <h1 class="main-title">
                <span style="font-size: 4rem; margin-right: 0.5rem; filter: drop-shadow(0 0 15px rgba(79,172,254,0.6));">🗑️</span>
                Password Strength Checker
            </h1>
            <p class="sub-title">Test your password strength and get suggestions for improvement</p>
        </div>
    </div>
    """.replace("🔡️", "🔐"), unsafe_allow_html=True)
    
    # Enhanced instructions with icons
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.98); 
                padding: 2rem; border-radius: 20px; margin: 1rem 0;
                border: 3px solid #4facfe; 
                box-shadow: 
                    0 8px 32px rgba(79, 172, 254, 0.3),
                    0 0 0 1px rgba(79, 172, 254, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                animation: borderGlow 3s ease-in-out infinite alternate;">
        <h3 style="margin-top: 0; color: #1a202c; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.5rem;">
            📋 How to use this tool:
        </h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;">
            <div style="display: flex; align-items: center; margin: 0.8rem 0; padding: 1rem; 
                        background: rgba(79, 172, 254, 0.08); border-radius: 12px; border-left: 4px solid #4facfe;">
                <span style="font-size: 2rem; margin-right: 1rem;">1️⃣</span>
                <span style="color: #1a202c; font-weight: 600; font-size: 1.1rem;">Enter your password in the secure field below</span>
            </div>
            <div style="display: flex; align-items: center; margin: 0.8rem 0; padding: 1rem; 
                        background: rgba(79, 172, 254, 0.08); border-radius: 12px; border-left: 4px solid #4facfe;">
                <span style="font-size: 2rem; margin-right: 1rem;">2️⃣</span>
                <span style="color: #1a202c; font-weight: 600; font-size: 1.1rem;">View real-time strength analysis</span>
            </div>
            <div style="display: flex; align-items: center; margin: 0.8rem 0; padding: 1rem; 
                        background: rgba(79, 172, 254, 0.08); border-radius: 12px; border-left: 4px solid #4facfe;">
                <span style="font-size: 2rem; margin-right: 1rem;">3️⃣</span>
                <span style="color: #1a202c; font-weight: 600; font-size: 1.1rem;">Follow suggestions to improve your password</span>
            </div>
            <div style="display: flex; align-items: center; margin: 0.8rem 0; padding: 1rem; 
                        background: rgba(46, 213, 115, 0.1); border-radius: 12px; border-left: 4px solid #2ed573;">
                <span style="font-size: 2rem; margin-right: 1rem;">🎯</span>
                <span style="color: #1a202c; font-weight: 600; font-size: 1.1rem;">Aim for a <strong style="color: #2ed573;">"Strong"</strong> or <strong style="color: #2ed573;">"Very Strong"</strong> rating</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced password input section
        st.markdown('<div class="password-section">', unsafe_allow_html=True)
        st.markdown("""
        <h3 style="margin-top: 0; color: #333; font-family: 'Poppins', sans-serif;">
            🔐 Password Analysis
        </h3>
        """, unsafe_allow_html=True)
        
        password = st.text_input(
            "Enter your password:",
            type="password",
            help="🔒 Your password is analyzed locally and never sent to any server",
            key="password_input",
            placeholder="Type your password here..."
        )
        
        if password:
            # Show analysis progress with verbose feedback
            with st.spinner('🔍 Analyzing password...'):
                import time
                time.sleep(0.5)  # Brief pause for user feedback
                
            st.success("✅ Password analyzed successfully!")
            
            # Verbose feedback about what's happening
            with st.expander("📋 Analysis Details", expanded=False):
                st.write("**🔍 What we're checking:**")
                st.write("• Password length and complexity")
                st.write("• Character variety (uppercase, lowercase, numbers, symbols)")
                st.write("• Common password patterns and sequences")
                st.write("• Dictionary word detection")
                st.write("• Entropy calculation for randomness")
                
                st.write("**🔒 Security & Privacy:**")
                st.write("• All analysis happens locally on your device")
                st.write("• No passwords are saved or stored anywhere")
                st.write("• No data sent to external servers")
            
            # Analyze password
            score, strength_label, issues, color = analyze_password_strength(password)
            entropy = calculate_entropy(password)
            
            # Analysis completed
            st.info("✅ Password analysis completed!")
            
            # Display enhanced strength meter
            st.markdown("### 📊 Password Strength Analysis")
            st.markdown(create_strength_meter(score, color, strength_label), unsafe_allow_html=True)
            
            # Enhanced metrics display with better styling
            st.markdown("""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                       gap: 1rem; margin: 1rem 0;">
            """, unsafe_allow_html=True)
            
            col_score, col_entropy, col_length = st.columns(3)
            with col_score:
                delta_color = "normal" if score >= 60 else "inverse"
                st.metric("🎯 Strength", f"{strength_label}", f"{score}/100", delta_color=delta_color)
            with col_entropy:
                entropy_label = "High" if entropy > 40 else "Medium" if entropy > 25 else "Low"
                st.metric("🧮 Entropy", f"{entropy} bits", f"{entropy_label}", 
                         help="Higher entropy means more unpredictable")
            with col_length:
                length_status = "Good" if len(password) >= 12 else "OK" if len(password) >= 8 else "Short"
                st.metric("📏 Length", f"{len(password)} chars", f"{length_status}", 
                         help="Longer passwords are generally stronger")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Enhanced suggestions section
            if issues:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #dc3545, #e74c3c); 
                           padding: 1.5rem; border-radius: 15px; margin: 1rem 0;
                           border: 2px solid rgba(255, 255, 255, 0.3);
                           box-shadow: 0 8px 32px rgba(220, 53, 69, 0.3);
                           backdrop-filter: blur(10px);">
                    <h3 style="margin-top: 0; color: #ffffff; font-family: 'Inter', sans-serif;
                              text-shadow: 0 2px 4px rgba(0,0,0,0.3); font-weight: 600;">
                        🔧 Suggestions for Improvement
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                suggestions = generate_suggestions(issues)
                for i, suggestion in enumerate(suggestions):
                    st.markdown(f"""
                    <div style="background: rgba(220, 53, 69, 0.9); padding: 0.8rem; margin: 0.5rem 0; 
                               border-radius: 10px; border-left: 3px solid #ffffff;
                               border: 1px solid rgba(255, 255, 255, 0.3);
                               box-shadow: 0 4px 12px rgba(220, 53, 69, 0.2); color: #ffffff;
                               backdrop-filter: blur(5px);">
                        <span style="color: #ffffff; font-weight: 500;">{suggestion}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #22543d, #2f855a); 
                           padding: 1.5rem; border-radius: 15px; margin: 1rem 0;
                           border-left: 5px solid #9ae6b4; text-align: center;">
                    <h3 style="margin: 0; color: #c6f6d5; font-family: 'Poppins', sans-serif;">
                        🎉 Excellent! Your password meets all security criteria!
                    </h3>
                    <p style="margin: 0.5rem 0 0 0; color: #c6f6d5;">
                        Your password is strong and secure. Great job! 💪
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close password-section
    
    # History feature removed by user request
    with col2:
        # Enhanced tips section
        st.markdown('<div class="tips-section">', unsafe_allow_html=True)
        st.markdown("""
        <h3 style="margin-top: 0; color: #495057; font-family: 'Poppins', sans-serif;">
            💡 Password Security Guide
        </h3>
        """, unsafe_allow_html=True)
        
        with st.expander("✅ Good Password Examples", expanded=False):
            st.markdown("""
            <div style="background: #1a472a; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: #e8f5e8;">
                <p style="color: #a8e6a3;"><strong>🌟 Excellent passwords:</strong></p>
                <ul style="margin-bottom: 0; color: #e8f5e8;">
                    <li><code style="background: #2d5a3d; color: #a8e6a3; padding: 2px 4px; border-radius: 3px;">MyDog$Name2024!</code> - Personal + Special chars + Numbers</li>
                    <li><code style="background: #2d5a3d; color: #a8e6a3; padding: 2px 4px; border-radius: 3px;">Coffee&Code123#</code> - Interests + Symbols + Length</li>
                    <li><code style="background: #2d5a3d; color: #a8e6a3; padding: 2px 4px; border-radius: 3px;">Tr@vel2Paris$2024</code> - Dreams + Substitutions + Year</li>
                    <li><code style="background: #2d5a3d; color: #a8e6a3; padding: 2px 4px; border-radius: 3px;">MusicLover!2024#Rock</code> - Passion + Complexity</li>
                    <li><code style="background: #2d5a3d; color: #a8e6a3; padding: 2px 4px; border-radius: 3px;">Sunrise@Beach7am!</code> - Scene + Time + Symbols</li>
                </ul>
            </div>
            
            <div style="background: #1a365d; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: #bee3f8;">
                <p style="color: #90cdf4;"><strong>🔑 What makes them strong:</strong></p>
                <ul style="margin-bottom: 0; color: #bee3f8;">
                    <li>✓ Mixed case letters (A-z)</li>
                    <li>✓ Numbers and symbols (!@#$)</li>
                    <li>✓ Personal but not obvious info</li>
                    <li>✓ 12+ characters long</li>
                    <li>✓ Memorable stories or phrases</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("❌ Avoid These Patterns", expanded=False):
            st.markdown("""
            <div style="background: #742a2a; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: #fbb6ce;">
                <p style="color: #f8b4cb;"><strong>🚫 Weak password examples:</strong></p>
                <ul style="margin-bottom: 0; color: #fbb6ce;">
                    <li><code style="background: #5a2121; color: #f8b4cb; padding: 2px 4px; border-radius: 3px;">password123</code> - Dictionary word + simple numbers</li>
                    <li><code style="background: #5a2121; color: #f8b4cb; padding: 2px 4px; border-radius: 3px;">123456789</code> - Sequential numbers</li>
                    <li><code style="background: #5a2121; color: #f8b4cb; padding: 2px 4px; border-radius: 3px;">qwerty</code> - Keyboard pattern</li>
                    <li><code style="background: #5a2121; color: #f8b4cb; padding: 2px 4px; border-radius: 3px;">admin</code> - Common system word</li>
                    <li><code style="background: #5a2121; color: #f8b4cb; padding: 2px 4px; border-radius: 3px;">yourname1990</code> - Personal info + birth year</li>
                    <li><code style="background: #5a2121; color: #f8b4cb; padding: 2px 4px; border-radius: 3px;">welcome</code> - Common greeting</li>
                    <li><code style="background: #5a2121; color: #f8b4cb; padding: 2px 4px; border-radius: 3px;">letmein</code> - Obvious phrase</li>
                </ul>
            </div>
            
            <div style="background: #744444; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: #fec5c5;">
                <p style="color: #fed7d7;"><strong>⚠️ Why they're dangerous:</strong></p>
                <ul style="margin-bottom: 0; color: #fec5c5;">
                    <li>🎯 Easy to guess by hackers</li>
                    <li>📋 Found in common password lists</li>
                    <li>🔍 Predictable patterns</li>
                    <li>📏 Too short for modern security</li>
                    <li>👤 Based on public personal info</li>
                    <li>⌨️ Simple keyboard sequences</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("🛡️ Security Best Practices", expanded=True):
            st.markdown("""
            <div style="background: rgba(45, 55, 72, 0.9) !important; 
                       padding: 1.5rem; border-radius: 15px; margin: 0.5rem 0; 
                       border: 2px solid rgba(255, 255, 255, 0.3);
                       backdrop-filter: blur(10px);
                       box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);">
                <p style="color: #ffffff !important; font-size: 1.2em; margin-bottom: 1rem; font-weight: bold !important;"><strong style="color: #ffffff !important;">🔐 Essential Security Habits:</strong></p>
                <div style="display: grid; gap: 0.8rem; color: #ffffff !important;">
                    <div style="display: flex; align-items: center; padding: 0.5rem; background: rgba(255, 255, 255, 0.1); border-radius: 8px;">
                        <span style="margin-right: 0.8rem; font-size: 1.2em; color: #ffffff !important;">🔑</span>
                        <span style="font-weight: 500; color: #ffffff !important;">Use <strong style="color: #90cdf4 !important;">unique passwords</strong> for each account</span>
                    </div>
                    <div style="display: flex; align-items: center; padding: 0.5rem; background: rgba(255, 255, 255, 0.1); border-radius: 8px;">
                        <span style="margin-right: 0.8rem; font-size: 1.2em; color: #ffffff !important;">📱</span>
                        <span style="font-weight: 500; color: #ffffff !important;">Enable <strong style="color: #90cdf4 !important;">two-factor authentication (2FA)</strong></span>
                    </div>
                    <div style="display: flex; align-items: center; padding: 0.5rem; background: rgba(255, 255, 255, 0.1); border-radius: 8px;">
                        <span style="margin-right: 0.8rem; font-size: 1.2em; color: #ffffff !important;">🗂️</span>
                        <span style="font-weight: 500; color: #ffffff !important;">Use a <strong style="color: #90cdf4 !important;">password manager</strong> (LastPass, Bitwarden)</span>
                    </div>
                    <div style="display: flex; align-items: center; padding: 0.5rem; background: rgba(255, 255, 255, 0.1); border-radius: 8px;">
                        <span style="margin-right: 0.8rem; font-size: 1.2em; color: #ffffff !important;">🔄</span>
                        <span style="font-weight: 500; color: #ffffff !important;">Change passwords if <strong style="color: #90cdf4 !important;">compromised</strong></span>
                    </div>
                    <div style="display: flex; align-items: center; padding: 0.5rem; background: rgba(255, 255, 255, 0.1); border-radius: 8px;">
                        <span style="margin-right: 0.8rem; font-size: 1.2em; color: #ffffff !important;">🤫</span>
                        <span style="font-weight: 500; color: #ffffff !important;"><strong style="color: #90cdf4 !important;">Never share</strong> passwords with anyone</span>
                    </div>
                    <div style="display: flex; align-items: center; padding: 0.5rem; background: rgba(255, 255, 255, 0.1); border-radius: 8px;">
                        <span style="margin-right: 0.8rem; font-size: 1.2em; color: #ffffff !important;">📝</span>
                        <span style="font-weight: 500; color: #ffffff !important;">Avoid <strong style="color: #90cdf4 !important;">writing them down</strong> in plain text</span>
                    </div>
                    <div style="display: flex; align-items: center; padding: 0.5rem; background: rgba(255, 255, 255, 0.1); border-radius: 8px;">
                        <span style="margin-right: 0.8rem; font-size: 1.2em; color: #ffffff !important;">⏰</span>
                        <span style="font-weight: 500; color: #ffffff !important;">Update passwords <strong style="color: #90cdf4 !important;">regularly</strong> for sensitive accounts</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced password generator section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2, #f093fb); 
                   padding: 1.5rem; border-radius: 15px; margin: 1rem 0;
                   border: 2px solid rgba(255, 255, 255, 0.3);
                   box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
                   backdrop-filter: blur(10px);">
            <h3 style="margin-top: 0; color: #ffffff; font-family: 'Inter', sans-serif; 
                      text-shadow: 0 2px 4px rgba(0,0,0,0.3); font-weight: 600;">
                🔄 Secure Password Generator
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Password length selector
        password_length = st.slider("Password Length", min_value=8, max_value=32, value=16, 
                                  help="Longer passwords are more secure")
        
        # Initialize session state for toggle switches
        if 'symbols_active' not in st.session_state:
            st.session_state.symbols_active = True
        if 'numbers_active' not in st.session_state:
            st.session_state.numbers_active = True
        if 'upper_active' not in st.session_state:
            st.session_state.upper_active = True
        if 'lower_active' not in st.session_state:
            st.session_state.lower_active = True
        
        # Create spacer for separation
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        # Direct button layout without container
        
        # Each button stacked vertically - simple and clean!
        



        
        # FIXED - Commented out problematic code:
        # with col4:
        if True:  # Changed from 'with col4:' to fix error
            # Removed unnecessary toggle - using buttons below
            # Original line: lower_toggle = st.toggle("� Lowercase (a-z)", value=st.session_state.lower_active, key="lower_toggle")
            pass  # All functionality moved to buttons below
        
        # Container removed - buttons now display directly
        
        if st.button("🔣 Symbols (!@#$%^&*)", 
                    key="symbols_btn",
                    type="primary" if st.session_state.symbols_active else "secondary",
                    use_container_width=True):
            st.session_state.symbols_active = not st.session_state.symbols_active
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("🔢 Numbers (0-9)", 
                    key="numbers_btn",
                    type="primary" if st.session_state.numbers_active else "secondary",
                    use_container_width=True):
            st.session_state.numbers_active = not st.session_state.numbers_active
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("🔠 Uppercase (A-Z)", 
                    key="upper_btn",
                    type="primary" if st.session_state.upper_active else "secondary",
                    use_container_width=True):
            st.session_state.upper_active = not st.session_state.upper_active
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("🔡 Lowercase (a-z)", 
                    key="lower_btn",
                    type="primary" if st.session_state.lower_active else "secondary",
                    use_container_width=True):
            st.session_state.lower_active = not st.session_state.lower_active
        
        # Custom styling for vertical buttons
        st.markdown("""
        <style>
        .stButton > button {
            height: 60px !important;
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 15px !important;
            color: white !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
            background: rgba(255, 255, 255, 0.15) !important;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.85), rgba(118, 75, 162, 0.85)) !important;
            border-color: rgba(102, 126, 234, 0.7) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.95), rgba(118, 75, 162, 0.95)) !important;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Get the values for password generation
        include_symbols = st.session_state.symbols_active
        include_numbers = st.session_state.numbers_active
        include_upper = st.session_state.upper_active
        include_lower = st.session_state.lower_active
        
        # Display last generated password if exists
        if 'generated_password' in st.session_state and st.session_state.generated_password:
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.1); 
                       backdrop-filter: blur(20px);
                       border: 1px solid rgba(255, 255, 255, 0.2);
                       padding: 1.5rem; border-radius: 20px; 
                       margin: 1rem 0;
                       box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25),
                                   0 0 0 1px rgba(255, 255, 255, 0.1),
                                   inset 0 1px 0 rgba(255, 255, 255, 0.2);">
                <p style="margin: 0; font-weight: bold; color: white; text-align: center; 
                          font-size: 1.1rem; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">💡 Last Generated Password:</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([4, 1])
            with col1:
                # Display password with beautiful acrylic styling
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.15); 
                           backdrop-filter: blur(25px);
                           border: 1px solid rgba(255, 255, 255, 0.25);
                           padding: 20px; border-radius: 15px; 
                           margin: 10px 0;
                           box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3),
                                       0 0 0 1px rgba(255, 255, 255, 0.1),
                                       inset 0 1px 0 rgba(255, 255, 255, 0.3);
                           font-family: 'Courier New', monospace; font-size: 18px; 
                           color: white; font-weight: bold; text-align: center;
                           letter-spacing: 2px; word-break: break-all;
                           text-shadow: 0 2px 4px rgba(0,0,0,0.4);">
                    {st.session_state.generated_password}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", help="Clear", key="clear_password"):
                    del st.session_state.generated_password
                    st.rerun()
        
        if st.button("🎲 Generate Secure Password", 
                    help="Generate a cryptographically secure password with your preferences"):
            import secrets
            import random
            import time
            
            # Let's walk through the password generation process step by step
            with st.spinner('🎯 Setting up your character preferences...'):
                time.sleep(0.3)

                # Start with an empty character set and build it up based on user choices
                char_set = ""
                password_chars = []  # We'll make sure to include at least one of each selected type
                selected_types = []  # For feedback to the user

                if include_lower:
                    char_set += string.ascii_lowercase
                    password_chars.append(secrets.choice(string.ascii_lowercase))  # Always add one lowercase
                    selected_types.append("lowercase letters")
                if include_upper:
                    char_set += string.ascii_uppercase
                    password_chars.append(secrets.choice(string.ascii_uppercase))  # Always add one uppercase
                    selected_types.append("uppercase letters")
                if include_numbers:
                    char_set += string.digits
                    password_chars.append(secrets.choice(string.digits))  # Always add one number
                    selected_types.append("numbers")
                if include_symbols:
                    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
                    char_set += symbols
                    password_chars.append(secrets.choice(symbols))  # Always add one symbol
                    selected_types.append("symbols")

            # Let the user know what types are being used and the length
            st.info(f"📝 Using character types: {', '.join(selected_types)}")
            st.info(f"📏 Generating password with {password_length} characters")

            if not char_set:
                st.error("⚠️ Please select at least one character type!")
            else:
                # Now fill in the rest of the password with random choices from the full set
                with st.spinner('🎲 Generating random characters for your password...'):
                    time.sleep(0.4)

                    # Fill up to the desired length
                    remaining_length = password_length - len(password_chars)
                    for _ in range(remaining_length):
                        password_chars.append(secrets.choice(char_set))

                # Shuffle so the required characters aren't always at the start
                with st.spinner('🔀 Shuffling everything for extra randomness...'):
                    time.sleep(0.3)
                    random.shuffle(password_chars)
                generated_password = ''.join(password_chars)

                # Save the result so it can be shown to the user
                st.session_state['generated_password'] = generated_password

                # Show the password in a nice acrylic-styled box
                st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.12); 
                           backdrop-filter: blur(25px);
                           border: 1px solid rgba(255, 255, 255, 0.3);
                           padding: 1.5rem; border-radius: 20px; 
                           margin: 1rem 0;
                           box-shadow: 0 8px 32px rgba(102, 126, 234, 0.35),
                                       0 0 0 1px rgba(255, 255, 255, 0.15),
                                       inset 0 1px 0 rgba(255, 255, 255, 0.25);">
                    <p style="margin: 0; font-weight: bold; color: white; text-align: center; 
                              font-size: 1.2rem; text-shadow: 0 2px 4px rgba(0,0,0,0.4);">🎉 Your Generated Password:</p>
                </div>
                """, unsafe_allow_html=True)

                st.success("✅ Password Generated Successfully!")

                # Show the password itself in a prominent way
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.18); 
                           backdrop-filter: blur(30px);
                           border: 1px solid rgba(255, 255, 255, 0.35);
                           padding: 25px; border-radius: 18px; 
                           margin: 20px 0;
                           box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4),
                                       0 0 0 1px rgba(255, 255, 255, 0.2),
                                       inset 0 2px 0 rgba(255, 255, 255, 0.3);
                           font-family: 'Courier New', monospace; font-size: 22px; 
                           color: white; font-weight: bold; text-align: center;
                           letter-spacing: 3px; word-break: break-all;
                           text-shadow: 0 2px 6px rgba(0,0,0,0.5);
                           position: relative;
                           overflow: hidden;">
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;
                               background: linear-gradient(45deg, 
                                   rgba(102, 126, 234, 0.1) 0%, 
                                   rgba(118, 75, 162, 0.1) 50%, 
                                   rgba(102, 126, 234, 0.1) 100%);
                               pointer-events: none;"></div>
                    <div style="position: relative; z-index: 1;">
                        {generated_password}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Quickly analyze the generated password and show the result
                gen_score, gen_strength, _, _ = analyze_password_strength(generated_password)

                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22543d, #2f855a); 
                           padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <p style="margin: 0; text-align: center; color: #c6f6d5;">
                        <strong>Generated Password Strength: {gen_strength} ({gen_score}/100)</strong><br>
                        💡 Copy this password and test it in the analyzer above!
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close tips-section
    
    # Enhanced Footer
    st.markdown("""
    <div style="margin-top: 3rem; padding: 2.5rem; 
               background: rgba(255, 255, 255, 0.98); 
               border-radius: 20px; text-align: center; 
               border: 3px solid #4facfe;
               box-shadow: 
                   0 8px 32px rgba(79, 172, 254, 0.4),
                   0 0 0 1px rgba(79, 172, 254, 0.3),
                   inset 0 1px 0 rgba(255, 255, 255, 0.2);
               animation: borderGlowStrong 2.5s ease-in-out infinite alternate;">
        <h4 style="color: #1a202c; margin-bottom: 1.5rem; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 1.5rem;">
            🔐 About This Tool
        </h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                   gap: 1.5rem; margin: 1rem 0;">
            <div style="background: rgba(255, 255, 255, 0.95); border: 2px solid #48bb78; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(72, 187, 120, 0.2);">
                <h5 style="color: #22543d; margin-top: 0; font-weight: 700;">🔒 Privacy First</h5>
                <p style="margin-bottom: 0; font-size: 1em; color: #2d3748; font-weight: 500;">All analysis happens locally. No passwords are saved or stored. Nothing leaves your device.</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.95); border: 2px solid #4299e1; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(66, 153, 225, 0.2);">
                <h5 style="color: #2b6cb0; margin-top: 0; font-weight: 700;">⚡ Real-time</h5>
                <p style="margin-bottom: 0; font-size: 1em; color: #2d3748; font-weight: 500;">Instant feedback as you type helps you create stronger passwords immediately.</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.95); border: 2px solid #9f7aea; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(159, 122, 234, 0.2);">
                <h5 style="color: #553c9a; margin-top: 0; font-weight: 700;">🎯 Comprehensive</h5>
                <p style="margin-bottom: 0; font-size: 1em; color: #2d3748; font-weight: 500;">Checks against 40,000+ common passwords and uses advanced pattern detection.</p>
            </div>
        </div>
        <hr style="margin: 2rem 0; border: none; height: 2px; background: linear-gradient(90deg, transparent, #4facfe, transparent);">
        <p style="margin: 0 0 1rem 0; color: #2d3748; font-size: 1em; font-weight: 500; text-align: center;">
            Remember: Use unique passwords for each account and enable 2FA when possible
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple text-based signature
    st.markdown("---")
    st.markdown("### 💗 Built with love by **RL**")
    st.markdown("*Crafted with passion for cybersecurity and user privacy*")
    
    st.markdown("### 🌟 Support Future Development")
    st.markdown("If this tool helped you create stronger passwords, consider supporting more projects like this!")
    
    # Create columns for buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("☕ Buy Me a Coffee", use_container_width=True):
            st.success("Thank you for your support!")
    
    with col2:
        st.markdown("""
        <a href="https://github.com/rl-v0id/PasswordStrengthChecker" target="_blank" style="text-decoration: none;">
            <div style="
                background: linear-gradient(135deg, #ffd700, #ffed4a);
                color: #1a202c;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                text-align: center;
                font-weight: 600;
                border: 2px solid transparent;
                transition: all 0.3s ease;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: block;
                margin: 0;
                width: 100%;
                box-sizing: border-box;
            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(255,215,0,0.3)';" 
               onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';">
                ⭐ Star on GitHub
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <a href="https://github.com/rl-v0id" target="_blank" style="text-decoration: none;">
            <div style="
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                text-align: center;
                font-weight: 600;
                border: 2px solid transparent;
                transition: all 0.3s ease;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: block;
                margin: 0;
                width: 100%;
                box-sizing: border-box;
            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(102,126,234,0.3)';" 
               onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';">
                🚀 Follow for Updates
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("*\"Security should be accessible to everyone, not just the privileged few.\" - RL*")

if __name__ == "__main__":
    # Always run the main Streamlit app
    main()