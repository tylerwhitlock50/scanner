// plugins/vuetify.js
import { createVuetify } from 'vuetify';
import 'vuetify/styles'; // Import Vuetify's styles
import { aliases, mdi } from 'vuetify/iconsets/mdi'; // Material Design Icons (optional)

export default createVuetify({
  icons: {
    defaultSet: 'mdi', // Use Material Design Icons
    aliases,
    sets: {
      mdi,
    },
  },
});

