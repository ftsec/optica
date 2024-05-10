import os
te_bearer_token = os.getenv("THOUSAND_EYES_BEARER_TOKEN")  # can retrieve this from the thousand eyes users and roles tab..
base_url = "https://api.thousandeyes.com/v6"
request_timeout = 30  # in seconds
log_level = "INFO"
aids = [2074313, 2074315]