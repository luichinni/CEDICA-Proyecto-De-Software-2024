from wtforms.widgets import FileInput

class CustomFileInput(FileInput):
    def __call__(self, field, **kwargs):
        return f'''
        <div class="file has-name is-boxed is-primary">
            <label class="file-label">
                <input {self.html_params(name=field.name, **kwargs)} class="file-input" type="file" onchange="updateFileName(this)"/>
                <span class="file-cta">
                  <span class="file-icon">
                    <i class="fas fa-upload"></i>
                  </span>
                  <span class="file-label"> Elegir archivo... </span>
                </span>
                <span class="file-name" id="{field.id}_filename"> Sin archivo seleccionado </span>
            </label>
        </div>
        <script>
          function updateFileName(input) {{
            var fileNameSpan = document.getElementById('{field.id}_filename');
            if (input.files && input.files[0]) {{
              fileNameSpan.textContent = input.files[0].name;
            }} else {{
              fileNameSpan.textContent = 'Sin archivo seleccionado';
            }}
          }}
        </script>
        '''
