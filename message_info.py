# Edit this file with your authentication and message details

# PW API Key
key = ""

# PW Login Credentials
email = ""
password = ""

# your alliance ID
alliance_id = ""


# Use [[ruler]] and [[nation]] in subject/body to have the bot enter in the recipients leader or nation name
# subject should not exceed 50 characters

# Recruitment Message Details
recruiter_subject = ""
recruiter_body = """ """

# Applicant Message Details
applicant_subject = ""
applicant_body = """ """


# DO NOT EDIT the following
recruitment_message = {'subject': recruiter_subject, 'body': recruiter_body}
applicant_message = {'subject': applicant_subject, 'body': applicant_body}
login_payload = {
                'email': email,
                'password': password,
                'loginform': 'login'
}
