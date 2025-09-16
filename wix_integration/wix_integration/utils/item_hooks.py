import frappe
from .wix_api import WixAPI, format_product_data

def create_wix_product(doc, method):
    """Hook function called after Item creation"""
    try:
        # Check if Wix integration is enabled
        if not frappe.db.get_single_value("Site Config", "enable_wix_integration"):
            return
        
        # Skip if this is a variant or template
        if doc.variant_of or doc.has_variants:
            frappe.logger().info(f"Skipping Wix sync for item {doc.item_code} - variant or template")
            return
        
        # Skip if not a stock item or if it's a service
        if not doc.is_stock_item:
            frappe.logger().info(f"Skipping Wix sync for item {doc.item_code} - not a stock item")
            return
        
        # Initialize Wix API
        wix_api = WixAPI()
        
        # Format product data
        product_data = format_product_data(doc)
        
        frappe.logger().info(f"Creating Wix product for item: {doc.item_code}")
        
        # Create product in Wix
        wix_response = wix_api.create_product(product_data)
        
        if wix_response and wix_response.get("product"):
            wix_product_id = wix_response["product"].get("id")
            
            # Store Wix product ID in Item document
            frappe.db.set_value("Item", doc.name, "custom_wix_product_id", wix_product_id)
            frappe.db.commit()
            
            frappe.logger().info(
                f"Successfully created Wix product {wix_product_id} for item {doc.item_code}"
            )
            
            # Show success message to user
            frappe.msgprint(
                f"Item '{doc.item_code}' successfully synced to Wix as product ID: {wix_product_id}",
                title="Wix Sync Success"
            )
        else:
            frappe.logger().error(f"Failed to create Wix product for item {doc.item_code}")
            frappe.msgprint(
                f"Failed to sync item '{doc.item_code}' to Wix. Check Error Log for details.",
                title="Wix Sync Failed",
                indicator="red"
            )
    
    except Exception as e:
        frappe.log_error(
            f"Error in create_wix_product hook for item {doc.item_code}: {str(e)}",
            "Wix Integration Error"
        )
        frappe.msgprint(
            f"Error syncing item '{doc.item_code}' to Wix: {str(e)}",
            title="Wix Sync Error",
            indicator="red"
        )

def update_wix_product(doc, method):
    """Hook function called after Item update"""
    try:
        # Check if Wix integration is enabled
        if not frappe.db.get_single_value("Site Config", "enable_wix_integration"):
            return
        
        # Check if item has a Wix product ID
        wix_product_id = doc.get("custom_wix_product_id")
        if not wix_product_id:
            frappe.logger().info(f"Item {doc.item_code} has no Wix product ID - skipping update")
            return
        
        # Skip if this is a variant or template
        if doc.variant_of or doc.has_variants:
            return
        
        # Initialize Wix API
        wix_api = WixAPI()
        
        # Format product data
        product_data = format_product_data(doc)
        
        frappe.logger().info(f"Updating Wix product {wix_product_id} for item: {doc.item_code}")
        
        # Update product in Wix
        wix_response = wix_api.update_product(wix_product_id, product_data)
        
        if wix_response:
            frappe.logger().info(
                f"Successfully updated Wix product {wix_product_id} for item {doc.item_code}"
            )
        else:
            frappe.logger().error(f"Failed to update Wix product for item {doc.item_code}")
    
    except Exception as e:
        frappe.log_error(
            f"Error in update_wix_product hook for item {doc.item_code}: {str(e)}",
            "Wix Integration Error"
        )
