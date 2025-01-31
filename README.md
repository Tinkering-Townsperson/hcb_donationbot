# hcb-donationbot

 Discord bot that integrates with the HCB API to see donations to an org (only works in DMs)!

## Usage

Send this message to the bot:

```txt
!donations {hcb_id} {hours_interval}
```

Replace the following parameters:

- **hcb_id** (STRING, OPTIONAL, DEFAULT="hq"): id of organisation (hq, org_WKu8v9, etc.)
- **hours_interval** (INT, OPTIONAL, DEFAULT=24): how many hours back to filter (last 24 hours, etc.)
