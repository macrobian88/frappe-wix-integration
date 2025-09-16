from . import __version__ as app_version

app_name = "wix_integration"
app_title = "Wix Integration"
app_publisher = "Custom"
app_description = "Integrate Frappe Items with Wix Products"
app_email = "admin@example.com"
app_license = "MIT"

# Document Events
doc_events = {
    "Item": {
        "after_insert": "wix_integration.wix_integration.utils.wix_api.create_wix_product",
        "on_update": "wix_integration.wix_integration.utils.wix_api.update_wix_product"
    }
}

# Required apps
required_apps = ["frappe"]

# Installation
after_install = "wix_integration.install.after_install"
