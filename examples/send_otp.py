"""
Example: Sending OTP using MSG91 OTP API
"""

import os

from msg91 import Client

# Initialize client with your auth key
auth_key = os.getenv("MSG91_AUTH_KEY", "your_auth_key")
client = Client(auth_key)

# Example 1: Send basic OTP
print("Example 1: Send basic OTP")
try:
    response = client.otp.send(
        mobile="919XXXXXXXXX"  # Replace with actual mobile number
    )
    print(f"OTP sent successfully: {response}")
    session_id = response.get("message")
    print(f"Session ID: {session_id}")
except Exception as e:
    print(f"Error sending OTP: {e}")

print("\n" + "=" * 50 + "\n")

# Example 2: Send OTP with custom message
print("Example 2: Send OTP with custom message")
try:
    response = client.otp.send(
        mobile="919XXXXXXXXX",
        message="Your login verification code is ##OTP##. Valid for 5 minutes.",
        sender="MYAPP",
        otp_expiry=5,  # 5 minutes
        otp_length=6,  # 6 digit OTP
    )
    print(f"Custom OTP sent: {response}")
except Exception as e:
    print(f"Error sending custom OTP: {e}")

print("\n" + "=" * 50 + "\n")

# Example 3: Verify OTP
print("Example 3: Verify OTP")
try:
    # Replace with actual OTP received by user
    otp_to_verify = "123456"

    response = client.otp.verify(mobile="919XXXXXXXXX", otp=otp_to_verify)
    print(f"OTP verification result: {response}")

    if response.get("type") == "success":
        print("OTP verified successfully!")
    else:
        print("OTP verification failed!")

except Exception as e:
    print(f"Error verifying OTP: {e}")

print("\n" + "=" * 50 + "\n")

# Example 4: Resend OTP via text
print("Example 4: Resend OTP via text")
try:
    response = client.otp.resend(mobile="919XXXXXXXXX", retrytype="text")
    print(f"OTP resent via text: {response}")
except Exception as e:
    print(f"Error resending OTP: {e}")

print("\n" + "=" * 50 + "\n")

# Example 5: Resend OTP via voice
print("Example 5: Resend OTP via voice")
try:
    response = client.otp.resend(mobile="919XXXXXXXXX", retrytype="voice")
    print(f"OTP resent via voice: {response}")
except Exception as e:
    print(f"Error resending OTP via voice: {e}")

print("\n" + "=" * 50 + "\n")

# Example 6: Complete OTP flow
print("Example 6: Complete OTP authentication flow")
try:
    mobile = "919XXXXXXXXX"

    # Step 1: Send OTP
    print("Step 1: Sending OTP...")
    send_response = client.otp.send(
        mobile=mobile,
        message="Your verification code is ##OTP##",
        otp_length=4,
        otp_expiry=10,  # 10 minutes
    )

    if send_response.get("type") == "success":
        print(f"✓ OTP sent successfully. Session ID: {send_response.get('message')}")

        # In real application, user would enter the OTP they received
        # For demo purposes, we'll show the verification step
        print("\nStep 2: User enters OTP (simulation)")
        print("In real app: user_otp = input('Enter OTP: ')")

        # Step 3: Verify OTP (replace with actual OTP)
        # user_otp = "1234"  # This would come from user input
        # verify_response = client.otp.verify(mobile=mobile, otp=user_otp)
        # print(f"✓ Verification result: {verify_response}")

        print("\nStep 3: If user didn't receive OTP, resend it")
        resend_response = client.otp.resend(mobile=mobile, retrytype="text")
        print(f"✓ OTP resent: {resend_response}")

    else:
        print(f"✗ Failed to send OTP: {send_response}")

except Exception as e:
    print(f"Error in OTP flow: {e}")

print("\n" + "=" * 50 + "\n")
print("OTP examples completed!")
print("\nNote: Replace '919XXXXXXXXX' with actual mobile numbers for testing.")
print("Make sure to set MSG91_AUTH_KEY environment variable with your API key.")
