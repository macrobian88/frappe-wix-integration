import frappe
import requests
import json
from typing import Dict, Optional, Any

class WixAPI:
    """Wix API integration class"""
    
    def __init__(self):
        self.base_url = "https://www.wixapis.com"
        self.site_id = "a57521a4-3ecd-40b8-852c-462f2af558d2"  # kokofresh site
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def get_auth_token(self) -> str:
        """Get authentication token from site config or generate one"""
        # In a real implementation, you would get this from Wix OAuth or API keys
        # For this demo, we'll use a placeholder
        token = frappe.db.get_single_value("Site Config", "wix_auth_token")
        if not token:
            frappe.throw("Wix authentication token not configured. Please set 'wix_auth_token' in Site Config.")
        return token
    
    def create_product(self, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a product in Wix"""
        try:
            auth_token = self.get_auth_token()
            self.headers["Authorization"] = f"Bearer {auth_token}"
            
            url = f"{self.base_url}/stores/v3/products"
            
            response = requests.post(
                url=url,
                headers=self.headers,
                json=product_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                frappe.log_error(
                    f"Wix API Error: {response.status_code} - {response.text}",
                    "Wix Product Creation Failed"
                )
                return None
                
        except Exception as e:
            frappe.log_error(
                f"Error creating Wix product: {str(e)}",
                "Wix API Exception"
            )
            return None
    
    def update_product(self, product_id: str, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a product in Wix"""
        try:
            auth_token = self.get_auth_token()
            self.headers["Authorization"] = f"Bearer {auth_token}"
            
            url = f"{self.base_url}/stores/v3/products/{product_id}"
            
            response = requests.patch(
                url=url,
                headers=self.headers,
                json=product_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                frappe.log_error(
                    f"Wix API Error: {response.status_code} - {response.text}",
                    "Wix Product Update Failed"
                )
                return None
                
        except Exception as e:
            frappe.log_error(
                f"Error updating Wix product: {str(e)}",
                "Wix API Exception"
            )
            return None

def format_product_data(item_doc) -> Dict[str, Any]:
    """Format Frappe Item data for Wix Product API"""
    
    # Get price from item
    price = str(item_doc.standard_rate or "0.00")
    
    # Create basic product structure
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
        product_data["product"]["plainDescription"] = item_doc.description
    
    # Add SKU if available
    if item_doc.item_code:
        product_data["product"]["variantsInfo"]["variants"][0]["sku"] = item_doc.item_code
    
    # Add weight if available
    if item_doc.weight_per_unit:
        product_data["product"]["variantsInfo"]["variants"][0]["physicalProperties"]["weight"] = float(item_doc.weight_per_unit)
    
    # Add brand if available
    if item_doc.brand:
        product_data["product"]["brand"] = {
            "name": item_doc.brand
        }
    
    return product_data
