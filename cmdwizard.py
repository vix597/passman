class CmdWizardStep:
    def __init__(self, 
        prompt,
        help_msg=None, 
        required=False, 
        default=None, 
        value_type="str", 
        validator=None
    ):
        self.prompt = prompt
        self.help_msg = help_msg
        self.value = None
        self.required = required
        self.default=default
        self.value_type = value_type
        self.validator = validator
        if self.required:
            self.prompt = "*"+self.prompt
        
    def run(self):
        while not self.value:
            if self.default:
                display = self.prompt+" ["+self.default+"]: "
            else:
                display = self.prompt+": "
                
            self.value = input(display)
            if self.value.lower() in ("h","help","?") and self.help_msg:
                print(self.help_msg)
                self.value = None
            elif len(self.value) == 0:
                if self.required:
                    if self.default:
                        self.value = self.default
                    else:
                        print("This value is required. Try again.")
                        self.value = None
                        
            if not self.validate(self.value):
                print("Invalid value of "+self.value+". Try again.")
                self.value = None
    
    def validate(self, value):
        if self.validator:
            return self.validator(value)
            
        if self.value_type == "int":
            try:
                int(value)
            except ValueError:
                return False
        elif self.value_type == "bool":
            if value.lower() not in ("true","false","t","f","0","1","yes","y","n","no"):
                return False
        return True
        
class CmdWizard:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.steps = {}
        
    def add_step(self, 
        name, 
        prompt, 
        help_msg=None, 
        required=False, 
        default=None, 
        value_type="str", 
        validator=None
    ):   
        self.steps[name] = CmdWizardStep(prompt, help_msg, required, default, value_type, validator)
        
    def run(self):
        print("==="+self.name+"===")
        if self.description:
            print(self.description)
            print("Required options begin with a '*'")
            print("="*(6+len(self.name)))
        
        for step in self.steps.values():
            step.run()