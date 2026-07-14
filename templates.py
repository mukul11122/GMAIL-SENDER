def get_stock_email_template(custom_message=None):
    custom_message_section = ""
    if custom_message:
        custom_message_section = f'''
        <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px;">
            <p style="margin: 0; color: #856404; font-size: 14px;"><strong>{custom_message}</strong></p>
        </div>
        '''
    
    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
        
        <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 40px 30px; text-align: center;">
            <div style="font-size: 50px; margin-bottom: 15px;">📦</div>
            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700;">
                <strong>NEW STOCK HAS ARRIVED!</strong>
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 15px 0 0 0; font-size: 16px;">
                <strong>Fresh inventory now available for your business</strong>
            </p>
        </div>
        
        <div style="padding: 35px 30px;">
            <p style="color: #333; font-size: 16px; line-height: 1.7; margin: 0;">
                <strong>Dear Sir,</strong>
            </p>
            
            <p style="color: #555; font-size: 15px; line-height: 1.8; margin: 20px 0;">
                <strong style="font-size: 16px;">Kindly find attached Stock details and send your Orders.</strong>
            </p>
            
            <p style="color: #333; font-size: 15px; line-height: 1.8; margin: 15px 0;">
                <strong style="background-color: #fff3cd; padding: 3px 8px; border-radius: 3px;">Many new and short items included in the list and marked.</strong>
            </p>
            
            {custom_message_section}
            
            <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin: 25px 0; border: 2px solid #1e3c72;">
                <h3 style="color: #1e3c72; font-size: 16px; margin: 0 0 12px 0; font-weight: 700;">
                    📋 <strong>STOCK DETAILS ATTACHED</strong>
                </h3>
                <p style="color: #666; font-size: 14px; line-height: 1.6; margin: 0;">
                    <strong>Please find the complete stock list attached to this email.</strong><br>
                    The attachment contains <strong>all product details, quantities, and pricing information.</strong>
                </p>
            </div>
            
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; padding: 25px; margin: 25px 0; text-align: center;">
                <h2 style="color: #ffffff; margin: 0 0 15px 0; font-size: 18px; font-weight: 700;">
                    <strong>WHY ORDER NOW?</strong>
                </h2>
                <div style="display: inline-block; text-align: left;">
                    <p style="color: rgba(255,255,255,0.95); margin: 8px 0; font-size: 14px;">
                        <strong>✅ Fresh stock ready for immediate dispatch</strong>
                    </p>
                    <p style="color: rgba(255,255,255,0.95); margin: 8px 0; font-size: 14px;">
                        <strong>✅ Limited quantities available</strong>
                    </p>
                    <p style="color: rgba(255,255,255,0.95); margin: 8px 0; font-size: 14px;">
                        <strong>✅ Competitive wholesale pricing</strong>
                    </p>
                    <p style="color: rgba(255,255,255,0.95); margin: 8px 0; font-size: 14px;">
                        <strong>✅ Fast delivery to your location</strong>
                    </p>
                </div>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="#" style="display: inline-block; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: #ffffff; padding: 18px 45px; text-decoration: none; border-radius: 30px; font-size: 17px; font-weight: 700; box-shadow: 0 4px 15px rgba(40,167,69,0.3);">
                    <strong>🛒 PLACE YOUR ORDER NOW</strong>
                </a>
            </div>
            
            <div style="background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 15px 20px; margin: 25px 0; border-radius: 4px;">
                <p style="color: #856404; font-size: 15px; margin: 0; line-height: 1.6;">
                    <strong>⚡ HURRY!</strong> Stocks are limited and will be allocated on a 
                    <strong style="text-decoration: underline;">first-come, first-served basis.</strong> 
                    <strong>Place your order TODAY to secure your supply!</strong>
                </p>
            </div>
            
            <div style="border-top: 2px dashed #e0e0e0; padding-top: 20px; margin-top: 30px;">
                <p style="color: #555; font-size: 14px; margin: 0 0 10px 0;">
                    <strong>Need help or have questions?</strong>
                </p>
                <p style="color: #888; font-size: 13px; margin: 0;">
                    <strong>Simply reply to this email or contact our sales team directly.</strong><br>
                    We're here to assist you!
                </p>
            </div>
            
            <p style="color: #666; font-size: 14px; margin-top: 30px;">
                <strong>Best regards,</strong><br>
                <strong style="color: #1e3c72; font-size: 16px;">Sales Team</strong>
            </p>
        </div>
        
        <div style="background-color: #1e3c72; padding: 20px 30px; text-align: center;">
            <p style="color: rgba(255,255,255,0.9); font-size: 12px; margin: 0;">
                This email was sent to <strong>{{{{email}}}}</strong><br>
                <strong>© 2026 All Rights Reserved</strong>
            </p>
        </div>
        
    </div>
</body>
</html>
    '''


def get_stock_email_template_table(stock_data_raw=None, custom_message=None):
    return get_stock_email_template(custom_message)
