# Frappe App Structure Fix

The issue was that we had duplicate `hooks.py` and `modules.txt` files in both:
1. Root app directory: `wix_integration/` (WRONG - these should be deleted)
2. Inner module directory: `wix_integration/wix_integration/` (CORRECT - these should remain)

For a valid Frappe app, the structure should be:

```
wix_integration/                    # Root app directory
├── __init__.py                     # Contains version info only
├── install.py                      # Installation scripts (optional)
├── requirements.txt                # Python dependencies (in project root)
└── wix_integration/               # Inner module directory
    ├── __init__.py                # Contains version info
    ├── hooks.py                   # App configuration and hooks (ONLY HERE)
    ├── modules.txt                # Module list (ONLY HERE)
    ├── patches.txt                # Database patches (ONLY HERE)
    ├── config/
    │   ├── __init__.py
    │   └── desktop.py
    ├── doctype/
    │   └── __init__.py
    └── utils/
        ├── __init__.py
        ├── wix_api.py
        ├── item_hooks.py
        └── wix_mcp_integration.py
```

The files `wix_integration/hooks.py` and `wix_integration/modules.txt` need to be deleted.
Only the files in `wix_integration/wix_integration/` should contain the app configuration.
