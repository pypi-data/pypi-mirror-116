def __init__(hub):
    # This enables acct profiles that begin with "aws" for aws_auto modules
    hub.exec.aws_auto.ACCT = ["aws"]
