export function simpleShortcut(shortcut) {
  let simplified = shortcut == null ? '' : shortcut;
  simplified = simplified.replace('ctrl', 'C');
  simplified = simplified.replace('shift', 'S');
  simplified = simplified.split(' ').join('-');
  return simplified;
}

export function title(value) {
  const string = (value || '').toString();
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export function daysAgo(dateStr) {
  const updatedAt = new Date(dateStr);
  const currentTm = new Date();

  // difference between days(ms)
  const msDiff = currentTm.getTime() - updatedAt.getTime();

  // convert daysDiff(ms) to daysDiff(day)
  const daysDiff = Math.floor(msDiff / (1000 * 60 * 60 * 24));

  return daysDiff === 1
    ? `${daysDiff} day ago`
    : `${daysDiff} days ago`;
}
