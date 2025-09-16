# 🚀 Frappe-Wix Integration

## ✅ **CLEAN APP STRUCTURE - FIXED**

This is the corrected version with proper Frappe app structure.

### 📁 Correct File Structure:

```
wix_integration/
├── __init__.py                    # App version
├── install.py                     # Installation script
└── wix_integration/               # Inner app directory
    ├── __init__.py               # Package init  
    ├── hooks.py                  # ✅ Frappe hooks (CORRECT LOCATION)
    ├── patches.txt               # ✅ Patches file (CORRECT LOCATION)
    ├── modules.txt               # ✅ Modules list (CORRECT LOCATION)
    ├── config/
    │   ├── __init__.py
    │   └── desktop.py
    └── utils/
        ├── __init__.py
        ├── wix_api.py
        ├── wix_mcp_integration.py  
        └── item_hooks.py
```

## 🚀 Installation

```bash
# Clone this repository
git clone -b fix-app-structure https://github.com/macrobian88/frappe-wix-integration.git apps/wix_integration

# Install the app
bench --site your-site install-app wix_integration
```

The structure has been completely cleaned up and should now work correctly!
