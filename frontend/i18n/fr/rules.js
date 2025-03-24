export default {
  colorRules: {
    colorRequired: 'La couleur est obligatoire'
  },
  labelNameRules: {
    labelRequired: "Le nom de l'étiquette est obligatoire",
    labelLessThan100Chars: "Le nom de l'étiquette doit comporter moins de 100 caractères",
    duplicated: 'Cette étiquette (label) est déja utilisé.'
  },
  keyNameRules: {
    duplicated: 'La clé est déja utilisé.'
  },
  userNameRules: {
    userNameRequired: "Le nom d'utilisateur est requis",
    userNameLessThan30Chars: "Le nom d'utilisateur doit comporter moins de 30 caractères",
    minLength: 'Le nom d\'utilisateur doit comporter au moins 3 caractères'
  },
  roleRules: {
    roleRequired: 'Le rôle est obligatoire'
  },
  projectName: {
    required: 'Le nom du projet est requis',
    maxLength: 'Le nom du projet doit comporter moins de 100 caractères'
  },
  description: {
    required: 'Une description est requise'
  },
  fileFormatRules: {
    fileFormatRequired: 'Le format de fichier est requis'
  },
  emailRules: {
    required: 'L\'e-mail est requis',
    format: 'L\'e-mail doit être valide'
  },
  uploadFileRules: {
    fileRequired: 'Le fichier est obligatoire',
    fileLessThan1MB: 'La taille du fichier doit être inférieure à 100 MB'
  },
  passwordRules: {
    passwordRequired: 'Le mot de passe est obligatoire',
    passwordLessThan30Chars: 'Le mot de passe doit comporter moins de 30 caractères',
    minLength: 'Le mot de passe doit comporter au moins 8 caractères',
    match: 'Les mots de passe doivent correspondre'
  }
}
