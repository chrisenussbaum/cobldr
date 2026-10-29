# Waitlist → Google Sheet

`waitlist.gs` receives signups from the form on `index.html` and adds each one as a row in a Google Sheet.

## Setup

1. Create a new Google Sheet (e.g. "cobldr waitlist").
2. In the Sheet, open **Extensions → Apps Script**.
3. Delete the starter code, paste in all of `waitlist.gs`, and click **Save**.
4. Click **Deploy → New deployment**, click the gear next to "Select type" and choose **Web app**.
   - **Execute as:** Me
   - **Who has access:** Anyone
5. Click **Deploy**, then **Authorize access** and allow it with your Google account.
   (Google may warn the app isn't verified: click **Advanced → Go to … (unsafe)**. It's your own script.)
6. Copy the **Web app URL** (ends in `/exec`) and set it as `ENDPOINT` in `index.html`.

## Updating the script

After editing the code, use **Deploy → Manage deployments → ✏️ → Version: New version → Deploy**
so the URL stays the same. "New deployment" creates a new URL.
