# 🚀 Frappe-Wix Integration: Complete Setup Guide

## 📋 Quick Start

This repository contains a complete Frappe custom app that automatically syncs Items from Frappe to Products in Wix. 

### 🎯 Target Integration
- **Wix Site**: kokofresh
- **Site ID**: `a57521a4-3ecd-40b8-852c-462f2af558d2`
- **Catalog Version**: Auto-detected (V1 or V3 support)

## ⚡ Installation

### 1. Clone and Install

```bash
# Navigate to your Frappe bench directory
cd /path/to/your/frappe-bench

# Clone the repository
git clone https://github.com/macrobian88/frappe-wix-integration.git apps/wix_integration

# Install the app
bench --site your-site-name install-app wix_integration

# Restart the bench
bench restart
```

### 2. Configure Authentication

#### Get Wix API Credentials:
1. Go to [Wix Developers](https://dev.wix.com/)
2. Create or select your app
3. Get OAuth token or API key
4. Note down your app permissions

#### Set up in Frappe:
1. Go to **Setup > Site Config**
2. Click **Add Row** and set:
   - **Key**: `wix_auth_token`
   - **Value**: Your Wix API token
3. Add another row:
   - **Key**: `enable_wix_integration` 
   - **Value**: `1`

### 3. Test the Integration

Create a new Item:
1. Go to **Stock > Item > New**
2. Fill in:
   - **Item Code**: `TEST-SYNC-001`
   - **Item Name**: `Test Sync Product`
   - **Item Group**: Any existing group
   - **Stock UOM**: `Nos`
   - **Standard Rate**: `99.99`
   - **Description**: `This is a test product for Wix sync`
   - **Maintain Stock**: ✅ Yes

3. **Save** the item
4. Check for success message: "Item synced to Wix"
5. Check the **Wix Product ID** field is populated

## 🔧 Field Mapping

| Frappe Item | Wix Product | Notes |
|-------------|-------------|-------|
| `item_name` | Product Name | Primary display name |
| `item_code` | SKU | Unique identifier |
| `description` | Description | HTML stripped for plain text |
| `standard_rate` | Price | Converted to string format |
| `weight_per_unit` | Weight | Physical properties |
| `brand` | Brand | If available |
| `valuation_rate` | Cost | For profit calculations |

## 🛠️ Architecture

```
Frappe Item Creation
       ↓
Document Hook (after_insert)
       ↓
Format Product Data
       ↓
Call Wix API (Catalog V1/V3)
       ↓
Store Wix Product ID
       ↓
Show Success/Error Message
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "Wix authentication token not configured"
**Solution**: Set `wix_auth_token` in Site Config

#### 2. "Failed to sync item to Wix"
**Solutions**:
- Check Error Log for detailed messages
- Verify Wix token is valid and has required permissions
- Ensure item is a stock item (not service)

#### 3. "Products not syncing"
**Check**:
- `enable_wix_integration` is set to `1`
- Item is not a variant or template
- Item has `is_stock_item` checked

#### 4. "Catalog version error"
The app auto-detects catalog version. If you get version errors:
- Check your Wix site's catalog version
- Update the API endpoints in the integration

### 🔧 Debug Mode

Enable detailed logging:
1. Go to **Error Log**
2. Look for entries with title "Wix Integration"
3. Check server console for real-time logs

## 📝 Customization

### Modify Field Mapping

Edit `wix_integration/wix_integration/utils/wix_api.py`:

```python
def format_product_data(item_doc):
    # Add your custom field mappings here
    product_data = {
        "product": {
            "name": item_doc.your_custom_field,  # Custom mapping
            # ... rest of the mapping
        }
    }
    return product_data
```

### Add Custom Logic

Edit `wix_integration/wix_integration/utils/item_hooks.py`:

```python
def create_wix_product(doc, method):
    # Add custom conditions
    if doc.custom_field == "special_value":
        # Custom logic here
        pass
    
    # ... rest of the hook
```

## 🔐 Security Best Practices

1. **Never commit tokens**: Use Site Config, not code
2. **Use HTTPS**: All API calls are encrypted
3. **Validate input**: Data is sanitized before API calls
4. **Error handling**: Sensitive data not exposed in logs

## 📈 Advanced Features

### Batch Sync
```python
# Custom script to sync all items
from wix_integration.wix_integration.utils.item_hooks import create_wix_product

items = frappe.get_all("Item", {"is_stock_item": 1})
for item_name in items:
    item = frappe.get_doc("Item", item_name.name)
    create_wix_product(item, "manual")
```

### Webhook Integration
Add webhook endpoints to sync back from Wix:

```python
@frappe.whitelist(allow_guest=True)
def wix_webhook(data):
    # Handle Wix -> Frappe sync
    pass
```

## 📞 Support

### Getting Help
1. **Documentation**: Check this README
2. **Error Logs**: Review Frappe Error Log
3. **GitHub Issues**: Create issues for bugs
4. **Community**: Ask in Frappe forums

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests if applicable  
4. Submit pull request

## 📄 License

MIT License - Feel free to use and modify!

---

## 🎉 Success!

If you've followed this guide, you should now have:

✅ **Automatic product creation** in Wix when Items are created in Frappe  
✅ **Field mapping** between Frappe and Wix  
✅ **Error handling** and logging  
✅ **Configurable integration** you can enable/disable  

**Happy syncing!** 🚀

---

### 📊 Integration Stats

- **Repository**: https://github.com/macrobian88/frappe-wix-integration
- **Version**: 1.0.0
- **Frappe Compatible**: v13+ 
- **Python**: 3.8+
- **Dependencies**: frappe, requests

**Made with ❤️ for seamless e-commerce integration**
