<template>
  <section class="section">
    <div class="container">
      <!-- Caja con sombra y borde redondeado -->
      <div class="box">
        <h2 class="title is-3 has-text-centered">Contacto</h2>
        <p class="subtitle has-text-centered">¡Nos encantaría saber de ti!</p>
        
        <!-- Formulario de contacto -->
        <form>
          <div class="field">
            <label class="label">Nombre</label>
            <div class="control">
              <input class="input" type="text" placeholder="Tu nombre" />
            </div>
          </div>

          <div class="field">
            <label class="label">Email</label>
            <div class="control">
              <input class="input" type="email" placeholder="tuemail@ejemplo.com" />
            </div>
          </div>

          <div class="field">
            <label class="label">Mensaje</label>
            <div class="control">
              <textarea class="textarea" placeholder="Escribe tu mensaje aquí"></textarea>
            </div>
          </div>

          <div class="field is-grouped is-justify-content-center">
            <div class="control">
              <button class="button is-link">Enviar</button>
            </div>
            <div class="control">
              <button class="button is-light" type="reset">Cancelar</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>
