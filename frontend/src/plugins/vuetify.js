import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

import {
  VApp,
  VMain,
  VContainer,
  VNavigationDrawer,
  VList,
  VListItem,
  VListItemTitle,
  VIcon,
  VDivider,
  VBtn,
  VCard,
  VDataTable,
  VDialog,
  VForm,
  VTextField,
  VTextarea,
  VAutocomplete,
  VChip,
  VRow,
  VCol
} from 'vuetify/components'

export default createVuetify({
  components: {
    VApp,
    VMain,
    VContainer,
    VNavigationDrawer,
    VList,
    VListItem,
    VListItemTitle,
    VIcon,
    VDivider,
    VBtn,
    VCard,
    VDataTable,
    VDialog,
    VForm,
    VTextField,
    VTextarea,
    VAutocomplete,
    VChip,
    VRow,
    VCol
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})
