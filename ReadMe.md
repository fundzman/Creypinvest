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
- All mail (allauth confirmations, alerts, contact form) goes through Anymail’s Resend backend. Helpers in `creyp/utils.py` send in a background thread when `DEBUG=False`.

## Static & Media Storage (Cloudflare R2)

Static files and user uploads live in a Cloudflare R2 bucket, accessed through R2’s S3-compatible API with `django-storages`, and served from `cdn.creypinvest.com`.

- Set environment variables in `.env`:
  - `USE_R2=True` (anything else serves files from local disk)
  - `R2_ACCOUNT_ID=YOUR_CLOUDFLARE_ACCOUNT_ID`
  - `R2_ACCESS_KEY_ID=YOUR_R2_TOKEN_ACCESS_KEY_ID`
  - `R2_SECRET_ACCESS_KEY=YOUR_R2_TOKEN_SECRET`
  - `R2_BUCKET_NAME=YOUR_BUCKET_NAME`
  - `R2_REGION=auto`
  - `R2_CDN_DOMAIN=cdn.creypinvest.com` (optional, this is the default)
- In the Cloudflare dashboard:
  1. Create the R2 bucket and an R2 API token with **Object Read & Write** on it.
  2. Under the bucket’s **Settings → Custom Domains**, connect `cdn.creypinvest.com`.
  3. Add a CORS policy allowing `GET` from `https://creypinvest.com` (needed for fonts loaded from the CDN).
- After deploying, upload static files once (and again whenever `static/` changes):
  - `python manage.py collectstatic --noinput`
- Upload the default avatar so `Profile.image` doesn’t 404:
  - `media-root/profile-image-placeholder.png` → `media/profile-image-placeholder.png` in the bucket
