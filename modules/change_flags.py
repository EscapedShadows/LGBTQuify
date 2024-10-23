from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

class FlagChanger():
    def __init__(self, flags: dict, settings):
        self.flags = flags
        self.settings = settings
    
    def select_flags(self):
        self.num_flags = inquirer.number(
            message="How many flags do you want to combine?",
            min_allowed=1,
            max_allowed=4,
            validate=EmptyInputValidator(),
            default=1
        ).execute()

        choices = [{"name": value, "value": key} for key, value in self.flags.items()]

        flags = inquirer.fuzzy(
            message="Select your Flags",
            choices=choices,
            multiselect=True,
            validate=lambda result: len(result) == int(self.num_flags),
            invalid_message=f"Please select {self.num_flags} flags",
            max_height="70%"
        ).execute()

        self.settings.set_setting({"key": "selectedFlags", "value": flags})

        return flags