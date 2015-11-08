from cmdwizard import CmdWizard

generate_password_wizard = CmdWizard(
    name="Generate a password",
    description="Steps through the generation of a password"
)
generate_password_wizard.add_step(
    name="password.size",  
    prompt="Select a password size",
    help_msg="Specify the number of characters for the password to be generated.",
    required=True,
    default=15,
    value_type="int"
)
generate_password_wizard.add_step(
    name="password.disallow.chars",
    prompt="Specify the characters that are not allowed in the password",
    help_msg='This should be a list of characters with no seperation (i.e. "*`~[]{}\/")'
)
generate_password_wizard.add_step(
    name="password.case.rule",
    prompt="Specify the number of upper case characters",
    help_msg="Leaving this 0 allows for any number of upper case characters",
    default=0,
    value_type="int",
    required=True
)
generate_password_wizard.add_step(
    name="password.copy",
    prompt="Copy the password to the clipboard?",
    help_msg="If not, the password will be echoed to the screen, otherwiswe it will just be copied.",
    required=True,
    value_type="bool",
    default="Yes"
)

account_wizard = CmdWizard(
    name="Account Wizard",
    description="Adds or updates an account in the PassMan database."
)
account_wizard.add_step(
    name="name",
    prompt="Enter the account name",
    help_msg="This name will be used as the unique identifier in the database for later access/update",
    required=True
)
account_wizard.add_step(
    name="username",
    prompt="Enter the username for the new account",
    help_msg="This is the username associated with the new account being added to PassMan.",
    required=True
)
account_wizard.add_step(
    name="description",
    prompt="Enter a description for the new account",
    help_msg="This field is optional. It is intended for informational puposes."
)
account_wizard.add_step(
    name="url",
    prompt="Enter the login URL for the new account",
    help_msg="This field is option. It is intended to be the URL where the username and password should be entered."
)