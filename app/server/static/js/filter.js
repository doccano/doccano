export default function simpleShortcut(shortcut) {
  if (shortcut === null) {
    shortcut = '';
  } else {
    shortcut = shortcut.replace('ctrl', 'C');
    shortcut = shortcut.replace('shift', 'S');
    shortcut = shortcut.split(' ').join('-');
  }
  return shortcut;
}
