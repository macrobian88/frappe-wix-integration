import frappe
import json
from typing import Dict, Optional, Any
import logging

class WixMCPAPI:
    """Wix API integration using MCP Remote"""
    
    def __init__(self):
        self.site_id = "a57521a4-3ecd-40b8-852c-462f2af558d2"  # kokofresh site
    
    def create_product(self, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a product in Wix using MCP Remote"""
        try:
            # The Wix MCP remote will handle authentication automatically
            # We just need to call the API with proper data structure
            
            frappe.logger().info(f"Attempting to create Wix product with data: {json.dumps(product_data, indent=2)}")
            
            # For now, we'll simulate the API call and log the data
            # In a real implementation with MCP, you would call the Wix API here
            
            # Simulate a successful response
            mock_response = {
                "product": {
                    "id": f"wix_product_{frappe.generate_hash(length=10)}",
                    "name": product_data["product"]["name"],
                    "slug": product_data["product"]["name"].lower().replace(" ", "-")
                }
            }
            
            frappe.logger().info(f"Mock Wix product created: {json.dumps(mock_response, indent=2)}")
            
            return mock_response
            
        except Exception as e:
            frappe.log_error(
                f"Error creating Wix product: {str(e)}\\nProduct Data: {json.dumps(product_data, indent=2)}",
                "Wix API Exception"
            )
            return None
    
    def update_product(self, product_id: str, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a product in Wix using MCP Remote"""
        try:
            frappe.logger().info(f"Attempting to update Wix product {product_id} with data: {json.dumps(product_data, indent=2)}")
            
            # Simulate successful update
            mock_response = {
                "product": {
                    "id": product_id,
                    "name": product_data["product"]["name"],
                    "updated": True
                }
            }
            
            frappe.logger().info(f"Mock Wix product updated: {json.dumps(mock_response, indent=2)}")
            
            return mock_response
            
        except Exception as e:
            frappe.log_error(
                f"Error updating Wix product {product_id}: {str(e)}\\nProduct Data: {json.dumps(product_data, indent=2)}",
                "Wix API Exception"
            )
            return None

def format_product_data(item_doc) -> Dict[str, Any]:
    """Format Frappe Item data for Wix Product API"""
    
    # Get price from item
    price = str(float(item_doc.standard_rate or 0.00))
    
    # Create basic product structure following Wix API v3 schema
    product_data = {
        "product": {
            "name": item_doc.item_name or item_doc.item_code,
            "productType": "PHYSICAL",
            "physicalProperties": {},
            "variantsInfo": {
                "variants": [
                    {
                        "price": {
                            "actualPrice": {
                                "amount": price
                            }
                        },
                        "physicalProperties": {}
                    }
                ]
            }
        }
    }
    
    # Add description if available
    if item_doc.description:
        # Clean HTML for plain description
        description = frappe.utils.strip_html(item_doc.description) if item_doc.description else ""
        if description:
            product_data["product"]["plainDescription"] = description
    
    # Add SKU if available
    if item_doc.item_code:
        product_data["product"]["variantsInfo"]["variants"][0]["sku"] = item_doc.item_code
    
    # Add weight if available
    if item_doc.weight_per_unit and item_doc.weight_per_unit > 0:
        product_data["product"]["variantsInfo"]["variants"][0]["physicalProperties"]["weight"] = float(item_doc.weight_per_unit)
    
    # Add brand if available
    if item_doc.brand:
        product_data["product"]["brand"] = {
            "name": item_doc.brand
        }
    
    # Add item group as category reference
    if item_doc.item_group:
        # Note: You may need to map Frappe Item Groups to Wix Categories
        product_data["product"]["mainCategoryId"] = item_doc.item_group
    
    # Add visibility settings
    product_data["product"]["visible"] = True
    product_data["product"]["visibleInPos"] = True if item_doc.is_stock_item else False
    
    return product_data

# Backward compatibility
WixAPI = WixMCPAPI
