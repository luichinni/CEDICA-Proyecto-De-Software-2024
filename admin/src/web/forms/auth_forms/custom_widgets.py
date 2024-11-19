
class CustomInput:
    def __init__(self, type, icon, placeholder = None):
        self.type = type
        self.icon = icon
        self.placeholder = placeholder if placeholder else type


    def __call__(self, field, **kwargs):
        return f"""
            <div id="{field.id}-div" class="field has-addons">
                <div class="control">
                    <button class="button is-white" name="{field.name}" id="{field.id}-icon" type="button">
                        <span class="icon">
                            <img src="{self.icon}" alt="Input icon" width="20" height="20">
                        </span>
                    </button>
                </div>
                <div class="control is-expanded">
                    <input id="{field.id}" class="input is-fullwidth" name="{field.name}" type="{self.type}" placeholder="{self.placeholder}">
                </div>
            </div>
        """

class CustomSubmit:
    def __init__(self, label):
        self.label = label

    def __call__(self, field, **kwargs):
        return f"""
        </br>
        <div class="container">
            <div class="buttons is-centered">
                <button type="submit" name="{field.name}" id="{field.id}" class="button is-success is-medium">
                    <span>{self.label}</span>
                </button>
            </div>
        </div>
        """