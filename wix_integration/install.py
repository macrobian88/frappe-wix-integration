import frappe

def after_install():
    """Run after installing the app"""
    try:
        # Create custom field for Wix Product ID
        create_custom_field_for_wix_product_id()
        
        # Set default configuration
        setup_default_configuration()
        
        frappe.db.commit()
        
        print("\n" + "="*60)
        print("🎉 Wix Integration app installed successfully!")
        print("="*60)
        print("📋 Next Steps:")
        print("1. Go to Setup > Site Config")
        print("2. Add 'wix_auth_token' with your Wix API token")
        print("3. Add 'enable_wix_integration' and set to 1")
        print("4. Create a test Item to verify the integration")
        print("="*60)
        print("🏪 Target Wix Site: kokofresh")
        print("🆔 Site ID: a57521a4-3ecd-40b8-852c-462f2af558d2")
        print("="*60 + "\n")
        
    except Exception as e:
        frappe.log_error(f"Error in after_install: {str(e)}", "Wix Integration Installation Error")
        print(f"❌ Installation completed with errors: {str(e)}")
        print("Check Error Log for details.")

def create_custom_field_for_wix_product_id():
    """Create custom field to store Wix Product ID in Item DocType"""
    try:
        # Check if field already exists
        if frappe.db.exists("Custom Field", {"dt": "Item", "fieldname": "custom_wix_product_id"}):
            print("✅ Custom field 'custom_wix_product_id' already exists")
            return
        
        # Create custom field
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Item",
            "label": "Wix Product ID",
            "fieldname": "custom_wix_product_id",
            "fieldtype": "Data",
            "read_only": 1,
            "no_copy": 1,
            "print_hide": 1,
            "report_hide": 1,
            "description": "Automatically populated when item is synced to Wix",
            "insert_after": "item_code"
        })
        
        custom_field.insert(ignore_permissions=True)
        print("✅ Created custom field 'custom_wix_product_id' in Item DocType")
        
    except Exception as e:
        print(f"⚠️  Error creating custom field: {str(e)}")
        frappe.log_error(f"Error creating custom field: {str(e)}", "Wix Integration Setup Error")

def setup_default_configuration():
    """Set up default configuration values"""
    try:
        # Get Site Config
        site_config = frappe.get_doc("Site Config", "Site Config")
        
        # Set default values if not already set
        if not site_config.get("enable_wix_integration"):
            site_config.set("enable_wix_integration", "0")  # Disabled by default
            print("✅ Set 'enable_wix_integration' to 0 (disabled by default)")
        
        if not site_config.get("wix_site_id"):
            site_config.set("wix_site_id", "a57521a4-3ecd-40b8-852c-462f2af558d2")
            print("✅ Set default Wix Site ID for kokofresh")
        
        site_config.save(ignore_permissions=True)
        
    except Exception as e:
        print(f"⚠️  Error setting up configuration: {str(e)}")
        frappe.log_error(f"Error setting up configuration: {str(e)}", "Wix Integration Setup Error")
