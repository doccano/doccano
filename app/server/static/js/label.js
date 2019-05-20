import Vue from 'vue';
import HTTP from './http';
import simpleShortcut from './filter';

Vue.filter('simpleShortcut', simpleShortcut);

const isLetter = (l) => {
  const pattern = 'abcdefghijklmnopqrstuvwxyz'
  if (pattern.indexOf(l.toLowerCase()) !== -1) {
    return true
  }
  return false
}

const colorPalette = [
  '#209cee',
  '#f44336',
  '#e91e63',
  '#9c27b0',
  '#3f51b5',
  '#2196f3',
  '#03a9f4',
  '#00bcd4',
  '#009688',
  '#4caf50',
  '#8bc34a',
  '#cddc39',
  '#ffeb3b',
  '#ffc107',
  '#ff9800',
  '#ff5722',
  '#795548',
  '#9e9e9e'
]

const vm = new Vue({
  el: '#mail-app',
  delimiters: ['[[', ']]'],
  data: {
    labels: [],
    labelText: '',
    labelComment: '',
    selectedKey: '',
    checkedKey: [],
    shortcutKey: '',
    backgroundColor: '#209cee',
    textColor: '#ffffff',
    labelId: null
  },

  computed: {
    /**
      * combineKeys: Combine selectedKey and checkedKey to get shortcutKey
      * saveKeys: Save null to database if shortcutKey is empty string
      */
    combineKeys: function () {
      this.shortcutKey = '';

      // If checkedKey exits, add it to shortcutKey
      if (this.checkedKey.length > 0) {
        this.checkedKey.sort();
        this.shortcutKey = this.checkedKey.join(' ');

        // If selectedKey exist, add it to shortcutKey
        if (this.selectedKey.length !== 0) {
          this.shortcutKey = this.shortcutKey + ' ' + this.selectedKey;
        }
      }

      // If only selectedKey exist, assign to shortcutKey
      if (this.shortcutKey.length === 0 && this.selectedKey.length !== 0) {
        this.shortcutKey = this.selectedKey;
      }
      return this.shortcutKey;
    },

    saveKeys: function () {
      this.shortcutKey = this.combineKeys;
      if (this.shortcutKey === '') {
        return null;
      }
      return this.shortcutKey;
    },
  },
  
  methods: {
    addLabel() {
      const payload = {
        text: this.labelText,
        shortcut: this.saveKeys,
        background_color: this.backgroundColor,
        text_color: this.textColor,
        comment: this.labelComment,
      };
      HTTP.post('labels/', payload).then((response) => {
        this.labels.push(response.data);
        this.reset();
      });
    },

    saveLabel() {
      const payload = {
        text: this.labelText,
        shortcut: this.saveKeys,
        background_color: this.backgroundColor,
        text_color: this.textColor,
        comment: this.labelComment
      };
      HTTP.put(`labels/${this.labelId}`, payload).then((response) => {
        Vue.set(this.labels, this.labels.findIndex((l) => l.id === response.data.id), response.data)
      });
    },

    setLabel(label) {
      this.reset()
      this.labelText = label.text
      this.backgroundColor = label.background_color
      this.textColor = label.text_color
      this.labelComment = label.comment
      this.labelId = label.id

      if (label.shortcut) {
        const splited = label.shortcut.split(' ')
        if (splited.length === 1) {
          this.selectedKey = label.shortcut
        } else {
          this.selectedKey = splited[splited.length - 1]

          for (let i = 0; i < splited.length -1; ++i) {
            this.checkedKey.push(splited[i])
          }
        }
      }
    },

    removeLabel(label) {
      const labelId = label.id;
      HTTP.delete(`labels/${labelId}`).then((response) => {
        const index = this.labels.indexOf(label);
        this.labels.splice(index, 1);
      });
    },

    reset() {
      this.labelText = '';
      this.labelComment = '';
      this.selectedKey = '';
      this.checkedKey = [];
      this.shortcutKey = '';
      this.backgroundColor = this.findLabelColor();
      this.textColor = '#ffffff';
      this.labelId = null
    },

    isSuitableShortcut(char) {
      let ret = true
      if (isLetter(char)) {
        this.labels.forEach((label) => {
          const shortcut = label.shortcut
          if (shortcut) {
            const splittedShortcut = shortcut.split(' ')
            const letter = splittedShortcut[splittedShortcut.length - 1]
            if (letter === char) {
              ret = false
            }
          }
        })
      } else {
        ret = false
      }
      return ret
    },
    findSuitableShortcut(lt) {
      const words = lt.split(' ')
      let maxWordLength = 0
      words.forEach((w) => {
        if (w.length > maxWordLength) {
          maxWordLength = w.length
        }
      })
      for (let i = 0; i < maxWordLength; ++i) {
        for (let k = 0; k < words.length; ++k) {
          if (i < words[k].length) {
            const char = words[k].charAt(i).toLowerCase()
            if (this.isSuitableShortcut(char)) {
              return char
            }
          }
        }
      }
      
      return null
    },
    findLabelColor() {
      let lastColorIndex = -1;
      for (let i = this.labels.length - 1; i >= 0; --i) {
        const label = this.labels[i]
        const idx = colorPalette.indexOf(label.background_color)
        if (idx !== -1 && idx > lastColorIndex) {
          lastColorIndex = idx
        }
      }
      if (lastColorIndex + 1 < colorPalette.length) {
        return colorPalette[lastColorIndex + 1]; 
      } else {
        return colorPalette[0]
      } 
    },
    setShortcut() {
      if (this.labelText && this.labelText.length) {
        const sc = this.findSuitableShortcut(this.labelText)
        if (sc) {
          this.selectedKey = sc
        }
      } else if ((!this.labelText || !this.labelText.length) && this.selectedKey) {
        this.selectedKey = ''
      }
    }
  },
  created() {
    HTTP.get('labels').then((response) => {
      this.labels = response.data;
      this.backgroundColor = this.findLabelColor()
    });
  }
});
