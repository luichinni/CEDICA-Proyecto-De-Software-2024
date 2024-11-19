
class CustomInput:
    def __init__(self, type, icon, placeholder = None):
        self.type = type
        self.icon = icon
        self.placeholder = placeholder if placeholder else type


    def __call__(self, field, **kwargs):
        return f"""
            <div class="field">
                <p class="control has-icons-left has-icons-right">
                    <input id="{field.id}" name="{field.name}" class="input" type="{self.type}" placeholder="{self.placeholder}">
                    <span class="icon is-small is-left">
                        <span class="icon">
                            <img src="{self.icon}" alt="Input icon" width="20" height="20">
                        </span>
                    </span>
                </p>
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