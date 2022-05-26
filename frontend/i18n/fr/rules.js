export default {
  colorRules: {
    colorRequired: 'La couleur est obligatoire'
  },
  labelNameRules: {
    labelRequired: "Le nom de l'étiquette est obligatoire",
    labelLessThan100Chars: "Le nom de l'étiquette doit comporter moins de 100 caractères"
  },
  userNameRules: {
    userNameRequired: "Le nom d'utilisateur est requis",
    userNameLessThan30Chars: "Le nom d'utilisateur doit comporter moins de 30 caractères"
  },
  roleRules: {
    roleRequired: 'Rôle est obligatoire'
  },
  projectNameRules: {
    projectNameRequired: 'Le nom du projet est requis',
    projectNameLessThan30Chars: 'Le nom du projet doit comporter moins de 30 caractères'
  },
  descriptionRules: {
    descriptionRequired: 'Une description est requise',
    descriptionLessThan30Chars: 'La description doit comporter moins de 100 caractères'
  },
  projectTypeRules: {
    projectTypeRequired: 'Le type de projet est requis'
  },
  fileFormatRules: {
    fileFormatRequired: 'Le format de fichier est requis'
  },
  uploadFileRules: {
    fileRequired: 'Le fichier est obligatoire',
    fileLessThan1MB: 'La taille du fichier doit être inférieure à 1MB'
  },
  passwordRules: {
    passwordRequired: 'Le mot de passe est obligatoire',
    passwordLessThan30Chars: 'Le mot de passe doit comporter moins de 30 caractères'
  }
}
