# Frappe-Wix Integration

A custom Frappe app that automatically creates and updates Wix products when Items are created or modified in Frappe.

## Features

- ✅ **Automatic Product Creation**: Creates Wix products when Frappe Items are created
- ✅ **Real-time Updates**: Updates Wix products when Frappe Items are modified
- ✅ **Field Mapping**: Maps Frappe Item fields to appropriate Wix Product fields
- ✅ **Error Handling**: Comprehensive error handling and logging
- ✅ **Configurable**: Easy to enable/disable and customize

## Wix Site Integration

**Target Site**: kokofresh  
**Site ID**: `a57521a4-3ecd-40b8-852c-462f2af558d2`

## Field Mapping

| Frappe Item Field | Wix Product Field | Description |
|-------------------|-------------------|-------------|
| `item_name` | `product.name` | Product name |
| `item_code` | `product.variantsInfo.variants[0].sku` | Product SKU |
| `description` | `product.plainDescription` | Product description (HTML) |
| `standard_rate` | `product.variantsInfo.variants[0].price.actualPrice.amount` | Product price |
| `weight_per_unit` | `product.variantsInfo.variants[0].physicalProperties.weight` | Product weight |
| `brand` | `product.brand.name` | Product brand |

## Installation

### 1. Install the App

```bash
# Navigate to your Frappe bench directory
cd /path/to/your/frappe-bench

# Clone the repository
git clone https://github.com/macrobian88/frappe-wix-integration.git apps/wix_integration

# Install the app
bench --site your-site-name install-app wix_integration
```

### 2. Configure Wix Authentication

You need to set up Wix authentication in your Site Config:

1. Go to **Setup > Site Config**
2. Add these fields:
   - `wix_auth_token`: Your Wix API authentication token
   - `enable_wix_integration`: Set to `1` to enable the integration

### 3. Add Custom Field to Item DocType

To store the Wix Product ID, add a custom field:

1. Go to **Customize > Customize Form**
2. Select **Item** DocType
3. Add a new field:
   - **Field Type**: Data
   - **Field Name**: `custom_wix_product_id`
   - **Label**: Wix Product ID
   - **Read Only**: Yes

## Getting Wix Authentication Token

To get your Wix authentication token:

1. **Create a Wix App** (if you haven't already):
   - Go to [Wix Developers](https://dev.wix.com/)
   - Create a new app or use existing one
   - Get your App ID and App Secret

2. **OAuth Flow** (Recommended):
   - Implement OAuth flow to get user consent
   - Store the access token securely

3. **API Key** (For development):
   - You can use Wix API keys for testing
   - Not recommended for production

## Usage

### Automatic Sync

Once configured, the integration works automatically:

1. **Create Item**: When you create a new Item in Frappe, it automatically creates a product in Wix
2. **Update Item**: When you update an Item, it updates the corresponding Wix product
3. **Error Handling**: Any errors are logged and displayed to the user

### Manual Testing

To test the integration:

1. Create a new Item with:
   - Item Name: "Test Product"
   - Item Code: "TEST-001"
   - Description: "This is a test product"
   - Standard Rate: 100.00
   - Maintain Stock: Yes

2. Check the **Error Log** for any issues
3. Verify the product was created in your Wix store
4. The `custom_wix_product_id` field should be populated

## Configuration Options

### Site Config Settings

| Setting | Description | Required |
|---------|-------------|----------|
| `wix_auth_token` | Wix API authentication token | Yes |
| `enable_wix_integration` | Enable/disable the integration (1/0) | Yes |
| `wix_site_id` | Override default Wix site ID | No |

### Customization

To customize the field mapping, edit `wix_integration/wix_integration/utils/wix_api.py` and modify the `format_product_data` function.

## Troubleshooting

### Common Issues

1. **"Wix authentication token not configured"**
   - Set the `wix_auth_token` in Site Config

2. **"Failed to sync item to Wix"**
   - Check Error Log for detailed error messages
   - Verify your Wix authentication token is valid
   - Ensure Wix app has proper permissions

3. **Products not syncing**
   - Verify `enable_wix_integration` is set to `1`
   - Check that the item is a stock item
   - Ensure it's not a variant or template

### Debug Logging

The app logs detailed information. Check:
- **Error Log** in Frappe
- Server console output
- Frappe logs directory

## API Endpoints Used

- **Create Product**: `POST https://www.wixapis.com/stores/v3/products`
- **Update Product**: `PATCH https://www.wixapis.com/stores/v3/products/{productId}`

## Security Considerations

1. **Store tokens securely**: Never commit authentication tokens to version control
2. **Use HTTPS**: All API calls use HTTPS
3. **Validate data**: Input validation is performed before API calls
4. **Error handling**: Sensitive information is not exposed in error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Error Logs
3. Create an issue on GitHub

---

**Happy syncing! 🚀**
