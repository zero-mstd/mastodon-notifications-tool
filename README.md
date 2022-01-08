# Mastodon Notifications Tool

This is a tool for exporting and viewing Mastodon’s notifications. It uses the offical API to get notifications in json, and can be viewed, sorted, filtered, or searched in a browser with the power of [List.js](https://listjs.com/).

Warning: This tool should be used for learning (or lottery) purpose only, because it doesn’t make any sense to indulge in notifications, such as favourite, reblog, follow, etc.

## Usage

```bash
git clone https://github.com/zero-mstd/mastodon-notifications-tool.git

cd mastodon-notifications-tool

firefox view.html
# You can open the `example.json` for a quickly glance.

vim export.py
# You should edit line 8 and line 10 first.
#
#   a. <your_access_token_here> (line 8)
#           You can get your access token by: Settings -> Development ->
#       NEW APPLICATION -> fill in an application name -> SUBMIT -> click your
#       application name -> you will see your access token.
#
#   b. <your_domain_here> (line 10)
#           Replace it with the domain address of the instance you are using.

python export.py
# Use the exporting tool to fetch all the notifications.

# If you run out your rate limits, which is 300 requests in 5 minutes per IP by
#    default, see, https://docs.joinmastodon.org/api/rate-limits/,
#    you can execute the following command to continue:
python export.py --continue

# If you got new notifications since last time you export,
#    you can execute the following command to update new data:
python export.py --update
```
