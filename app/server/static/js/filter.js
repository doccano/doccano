export default function simpleShortcut(shortcut) {
  let simplified = shortcut === null ? '' : shortcut;
  simplified = simplified.replace('ctrl', 'C');
  simplified = simplified.replace('shift', 'S');
  simplified = simplified.split(' ').join('-');
  return simplified;
}
