export default {
  colorRules: {
    colorRequired: 'Farbe wird benötigt'
  },
  labelNameRules: {
    labelRequired: 'Labelname wird benötigt',
    labelLessThan100Chars: 'Labelname muss kürzer als 100 Zeichen sein'
  },
  userNameRules: {
    userNameRequired: 'Benutzername wird benötigt',
    userNameLessThan30Chars: 'Benutzername muss kürzer als 30 Zeichen sein',
    minLength: 'Benutzername muss mindestens 3 Zeichen lang sein'
  },
  roleRules: {
    roleRequired: 'Rolle wird benötigt'
  },
  projectName: {
    required: 'Projektname wird benötigt',
    maxLength: 'Projektname muss kürzer als 100 Zeichen sein'
  },
  description: {
    required: 'Beschreibung wird benötigt'
  },
  fileFormatRules: {
    fileFormatRequired: 'Dateiformat wird benötigt'
  },
  emailRules: {
    required: 'E-Mail wird benötigt',
    format: 'E-Mail muss gültig sein'
  },
  uploadFileRules: {
    fileRequired: 'Datei(en) werden benötigt',
    fileLessThan1MB: 'Dateigröße muss kleiner als 100 MB sein!'
  },
  passwordRules: {
    passwordRequired: 'Passwort wird benötigt',
    passwordLessThan30Chars: 'Passwort muss kürzer als 30 Zeichen sein',
    minLength: 'Passwort muss mindestens 8 Zeichen lang sein',
    match: 'Passwörter müssen übereinstimmen',
  }
}
