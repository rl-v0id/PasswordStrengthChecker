import streamlit as st
import re
import math
from collections import Counter
import string

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
                            element.innerHTML.includes('keyboard_arrow')) {
                            
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

# Comprehensive common passwords and dictionary words database
COMMON_PASSWORDS = {
    # Numeric sequences
    '123456', '123456789', '12345678', '1234567890', '12345', '1234567',
    '654321', '987654321', '0123456789', '1111111111', '2222222222',
    '1234554321', '123321', '111111', '000000', '666666', '777777',
    
    # Basic words with numbers
    'password', 'password123', 'password1', 'password12', 'password1234',
    'admin', 'admin123', 'admin1', 'administrator', 'root', 'root123',
    'user', 'user123', 'guest', 'guest123', 'test', 'test123',
    
    # Keyboard patterns
    'qwerty', 'qwerty123', 'qwertyuiop', 'asdfgh', 'asdfghjkl', 'zxcvbn',
    'qazwsx', 'qaz123', 'wsx123', 'zaq123', 'xsw123', 'cde123',
    'qwe123', 'asd123', 'zxc123', 'qweasd', 'qweasdzxc',
    
    # Common words
    'welcome', 'welcome123', 'hello', 'hello123', 'world', 'world123',
    'login', 'login123', 'access', 'access123', 'enter', 'enter123',
    'computer', 'computer123', 'internet', 'internet123', 'system',
    
    # Names and dates
    'john', 'john123', 'mary', 'mary123', 'mike', 'mike123', 'sarah',
    'david', 'chris', 'alex', 'jessica', 'michael', 'jennifer',
    '2023', '2024', '2025', '1990', '1995', '2000', '2010',
    
    # Sports and common interests
    'football', 'soccer', 'basketball', 'baseball', 'tennis', 'golf',
    'music', 'movie', 'game', 'love', 'money', 'secret', 'master',
    
    # Simple substitutions
     'p@ssw0rd', 'p@ssword', 'passw0rd', '123qwe', 'qwe123asd',
    'abc123def', '1q2w3e4r', '1q2w3e', 'a1b2c3', 'abc123',
    
    # Company/brand names
    'google', 'facebook', 'apple', 'microsoft', 'amazon', 'twitter',
    'instagram', 'youtube', 'netflix', 'spotify', 'github',
    
    # Weak patterns
    'letmein', 'trustno1', 'dragon', 'baseball', 'monkey', 'sunshine',
    'princess', 'cookie', 'summer', 'flower', 'shadow', 'superman',
    'jesus', 'ninja', 'mustang', 'charlie', 'tigger', 'freedom',
    'jordan', 'hunter', 'killer', 'soccer', 'batman', 'master',
    'whatever', 'nothing', 'nobody', 'anyone', 'someone', 'everyone',
    
    # International variants
    'senha123', 'senha', 'mot2passe', 'contraseña', 'passwort',
    'heslo', 'lösenord', 'salasana', 'wachtwoord'
}

COMMON_WORDS = {
    # Basic system words
    'password', 'admin', 'administrator', 'user', 'username', 'login',
    'welcome', 'guest', 'test', 'testing', 'demo', 'example', 'sample',
    'default', 'change', 'temp', 'temporary', 'new', 'old', 'backup',
    
    # Technology terms
    'computer', 'laptop', 'desktop', 'server', 'database', 'system',
    'network', 'internet', 'website', 'email', 'domain', 'host',
    'cloud', 'data', 'file', 'folder', 'document', 'program',
    
    # Personal information
    'name', 'birth', 'birthday', 'anniversary', 'phone', 'address',
    'street', 'city', 'state', 'country', 'home', 'work', 'office',
    'school', 'college', 'university', 'company', 'business',
    
    # Common names
    'john', 'mary', 'james', 'patricia', 'robert', 'jennifer', 'michael',
    'linda', 'william', 'elizabeth', 'david', 'barbara', 'richard',
    'susan', 'joseph', 'jessica', 'thomas', 'sarah', 'christopher',
    'karen', 'daniel', 'nancy', 'matthew', 'lisa', 'anthony', 'betty',
    
    # Family relations
    'mother', 'father', 'sister', 'brother', 'daughter', 'son',
    'wife', 'husband', 'mom', 'dad', 'mama', 'papa', 'family',
    
    # Colors
    'black', 'white', 'red', 'blue', 'green', 'yellow', 'orange',
    'purple', 'pink', 'brown', 'gray', 'grey', 'silver', 'gold',
    
    # Animals
    'cat', 'dog', 'bird', 'fish', 'horse', 'cow', 'pig', 'sheep',
    'lion', 'tiger', 'bear', 'wolf', 'fox', 'rabbit', 'mouse',
    'elephant', 'monkey', 'snake', 'spider', 'butterfly',
    
    # Nature
    'sun', 'moon', 'star', 'earth', 'water', 'fire', 'wind', 'rain',
    'snow', 'tree', 'flower', 'grass', 'mountain', 'river', 'ocean',
    'beach', 'forest', 'desert', 'island', 'valley',
    
    # Time and dates
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
    'sunday', 'january', 'february', 'march', 'april', 'may', 'june',
    'july', 'august', 'september', 'october', 'november', 'december',
    'morning', 'afternoon', 'evening', 'night', 'today', 'tomorrow',
    'yesterday', 'week', 'month', 'year', 'hour', 'minute', 'second',
    
    # Emotions and states
    'happy', 'sad', 'angry', 'love', 'hate', 'good', 'bad', 'nice',
    'great', 'awesome', 'cool', 'hot', 'cold', 'warm', 'fresh',
    'clean', 'dirty', 'new', 'old', 'young', 'strong', 'weak',
    
    # Common verbs
    'make', 'take', 'come', 'give', 'think', 'know', 'want', 'need',
    'find', 'help', 'work', 'play', 'live', 'move', 'open', 'close',
    'start', 'stop', 'begin', 'end', 'create', 'delete', 'save',
    
    # Objects
    'house', 'car', 'phone', 'book', 'table', 'chair', 'door', 'window',
    'key', 'money', 'food', 'drink', 'coffee', 'tea', 'beer', 'wine',
    'music', 'movie', 'game', 'sport', 'ball', 'shoe', 'shirt',
    
    # Countries and cities
    'america', 'england', 'france', 'germany', 'italy', 'spain',
    'china', 'japan', 'india', 'canada', 'australia', 'brazil',
    'london', 'paris', 'berlin', 'madrid', 'rome', 'tokyo', 'beijing'
}

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
    
    # Avoid dictionary words (-10 points)
    password_lower = password.lower()
    for word in COMMON_WORDS:
        if word in password_lower:
            score -= 10
            issues.append("Avoid common dictionary words")
            break
    
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

# Main app
def main():
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
                <span style="font-size: 4rem; margin-right: 0.5rem; filter: drop-shadow(0 0 15px rgba(79,172,254,0.6));">�️</span>
                Password Strength Checker
            </h1>
            <p class="sub-title">Test your password strength and get suggestions for improvement</p>
        </div>
    </div>
    """.replace("�️", "🔐"), unsafe_allow_html=True)
    
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
            # Analyze password
            score, strength_label, issues, color = analyze_password_strength(password)
            entropy = calculate_entropy(password)
            
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
        
        col_gen1, col_gen2 = st.columns(2)
        with col_gen1:
            include_symbols = st.checkbox("Include Symbols (!@#$%^&*)", value=True)
            include_numbers = st.checkbox("Include Numbers (0-9)", value=True)
        with col_gen2:
            include_upper = st.checkbox("Include Uppercase (A-Z)", value=True)
            include_lower = st.checkbox("Include Lowercase (a-z)", value=True)
        
        if st.button("🎲 Generate Secure Password", 
                    help="Generate a cryptographically secure password with your preferences"):
            import secrets
            import random
            
            # Build character set based on user preferences
            char_set = ""
            password_chars = []
            
            if include_lower:
                char_set += string.ascii_lowercase
                password_chars.append(secrets.choice(string.ascii_lowercase))
            if include_upper:
                char_set += string.ascii_uppercase
                password_chars.append(secrets.choice(string.ascii_uppercase))
            if include_numbers:
                char_set += string.digits
                password_chars.append(secrets.choice(string.digits))
            if include_symbols:
                symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
                char_set += symbols
                password_chars.append(secrets.choice(symbols))
            
            if not char_set:
                st.error("⚠️ Please select at least one character type!")
            else:
                # Fill remaining length with random chars from selected set
                remaining_length = password_length - len(password_chars)
                for _ in range(remaining_length):
                    password_chars.append(secrets.choice(char_set))
                
                # Shuffle the password
                random.shuffle(password_chars)
                generated_password = ''.join(password_chars)
                
                # Display generated password with copy functionality
                st.markdown("""
                <div style="background: #2d3748; padding: 1rem; border-radius: 10px; 
                           border: 2px dashed #4a5568; margin: 1rem 0;">
                    <p style="margin: 0; font-weight: bold; color: #e2e8f0;">Generated Password:</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.code(generated_password, language=None)
                
                # Analyze the generated password
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
                <p style="margin-bottom: 0; font-size: 1em; color: #2d3748; font-weight: 500;">All analysis happens locally in your browser. Your passwords never leave your device.</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.95); border: 2px solid #4299e1; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(66, 153, 225, 0.2);">
                <h5 style="color: #2b6cb0; margin-top: 0; font-weight: 700;">⚡ Real-time</h5>
                <p style="margin-bottom: 0; font-size: 1em; color: #2d3748; font-weight: 500;">Instant feedback as you type helps you create stronger passwords immediately.</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.95); border: 2px solid #9f7aea; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(159, 122, 234, 0.2);">
                <h5 style="color: #553c9a; margin-top: 0; font-weight: 700;">🎯 Comprehensive</h5>
                <p style="margin-bottom: 0; font-size: 1em; color: #2d3748; font-weight: 500;">Checks against 500+ common passwords and uses advanced pattern detection.</p>
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
    main()