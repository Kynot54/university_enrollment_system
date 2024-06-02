formation="\
    users-primary=1,\
    users-secondary=1,\
    users-tertiary=1,\
    enrollment=3,\
    notifications=1,\
    krakend=1,\
    amazon-dynamodb-local=1,\
    email_consumer=2,\
    webhook_consumer=2,\
    smtp-email-server=1\
"

foreman start --formation "$formation"