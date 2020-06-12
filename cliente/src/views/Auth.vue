<template>
    <v-content>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
                dense
              >
                <v-toolbar-title>{{ showSignup ? 'Cadastro' : 'Login'}}</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    v-if="showSignup"
                    label="Nome"
                    type="text"
                    v-model="user.name"
                  />
                  <v-text-field
                    label="E-mail"
                    type="email"
                    v-model="user.email"
                  />
                  <v-text-field
                    label="Senha"
                    type="password"
                    v-model="user.password"
                  />
                  <v-text-field
                    v-if="showSignup"
                    label="Confirme a senha"
                    type="password"
                    v-model="user.confirmPassword"
                  />
                </v-form>
              </v-card-text>
              <v-card-actions>
                <a href @click.prevent="showSignup = !showSignup">
                <span v-if="showSignup">Já tem cadastro? Acesse o Login!</span>
                <span v-else>Não tem cadastro? Registre-se aqui</span>
              </a>
                <v-spacer />
                <v-btn
                  v-if="showSignup"
                  @click="signup"
                  color="primary">Registrar</v-btn>
                <v-btn
                  v-else
                  @click="signin"
                  color="primary">Entrar</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Auth',
  props: {
    source: String
  },
  data () {
    return {
      showSignup: false,
      user: {},
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
      ]
    }
  },
  methods: {
    ...mapActions(['attemptLogin', 'registerUser']),
    signin () {
      this.attemptLogin(this.user)
        .then(() => this.$router.push({ path: '/' }))
        .catch(e => console.log('erro', e))
    },
    signup () {
      this.registerUser(this.user)
        .then(res => {
          console.log('res', res)
          this.user = {}
          this.showSignup = false
        })
        .catch(e => console.log('erro', e))
    }
  }
}
</script>
