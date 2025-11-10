# Creypinvest, Inc __[ Open Source Project ]__

This is a Bitcoin Broker Site Created By __Divine Ikhuoria Ebehiremen__

## Programing Languages Used

- Python [_Django_] [Mostly Used]
- Cascading StyleSheet [_SCSS_]
- HTML5
- JAVASCRIPT [_ECMAScript_]

## Road Map

- __Login System__
  - Signup Page
  - Login Page
  - Password Reset
  - Change Password
  - Allowing More Than One Email Own By A User

- ### Emailing System __[_Made Faster With Email Threading_]__

  - Email Confirmation
  - New Device Login
  - Transactions Notification

- __Dashboard Area__
  - Home _[redirect to base page]_
  - User Wallet __[_Toggle Balance To Show USD Balance In BTC_]__
  - Referral System
  - User Profile Section
  - Payment Section
  - Help _[redirect to contact us page]_
  - Logout

#### Other Features

- Current Bitcoin Price Will Be Used
- Admin Side
  - Strong Authentication
- Added Extra Security Layer By Automatically Changing The ___Hash_ Model__ Of A Transaction With Same Hash As Before Like A _BlockChain_

## NOTE

- Getting User __IP Address__ For The New Device Detection!

Made With ❤ By __Divine Ikhuoria__ aka Divuzki

## Email Configuration (Resend)

- Install dependencies: `django-anymail` is already included in `requirements.txt`.
- Set environment variables in `.env`:
  - `RESEND_API_KEY=YOUR_RESEND_API_KEY`
  - `DEFAULT_FROM_EMAIL=you@your-verified-domain.com`
- Verify your sending domain in Resend and ensure `DEFAULT_FROM_EMAIL` matches your verified domain.
- The app uses Django’s `send_mail` with Anymail’s Resend backend; no code changes are required where emails are sent.
