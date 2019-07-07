import 'element-matches';
import 'custom-event-polyfill';

let ShortKey = {}
let mapFunctions = {}
let objAvoided = []
let elementAvoided = []
let keyPressed = false

const parseValue = (value) => {
  value = typeof value === 'string' ? JSON.parse(value.replace(/\'/gi, '"')) : value
  if (value instanceof Array) {
    return {'': value};
  }
  return value
}

const bindValue = (value, el, binding, vnode) => {
  const push = binding.modifiers.push === true
  const avoid = binding.modifiers.avoid === true
  const focus = !binding.modifiers.focus === true
  const once = binding.modifiers.once === true
  if (avoid) {
    objAvoided = objAvoided.filter((itm) => {
      return !itm === el;
    })
    objAvoided.push(el)
  } else {
    mappingFunctions({b: value, push, once, focus, el: vnode.elm})
  }
}

const unbindValue = (value, el) => {
  for (let key in value) {
    const k = ShortKey.encodeKey(value[key])
    const idxElm = mapFunctions[k].el.indexOf(el)
    if (mapFunctions[k].el.length > 1 && idxElm > -1) {
      mapFunctions[k].el.splice(idxElm, 1)
    } else {
      delete mapFunctions[k]
    }
  }
}

ShortKey.install = (Vue, options) => {
  elementAvoided = [...(options && options.prevent ? options.prevent : [])]
  Vue.directive('shortkey', {
    bind: (el, binding, vnode) => {
      // Mapping the commands
      const value = parseValue(binding.value)
      bindValue(value, el, binding, vnode)
    },
    update: (el, binding, vnode) => {
      const oldValue = parseValue(binding.oldValue)
      unbindValue(oldValue, el)

      const newValue = parseValue(binding.value)
      bindValue(newValue, el, binding, vnode)
    },
    unbind: (el, binding) => {
      const value = parseValue(binding.value)
      unbindValue(value, el)
    }
  })
}

ShortKey.decodeKey = (pKey) => createShortcutIndex(pKey)
ShortKey.encodeKey = (pKey) => {
  const shortKey = {}
  shortKey.shiftKey = pKey.includes('shift')
  shortKey.ctrlKey = pKey.includes('ctrl')
  shortKey.metaKey = pKey.includes('meta')
  shortKey.altKey = pKey.includes('alt')
  let indexedKeys = createShortcutIndex(shortKey)
  const vKey = pKey.filter((item) => !['shift', 'ctrl', 'meta', 'alt'].includes(item))
  indexedKeys += vKey.join('')
  return indexedKeys
}

const createShortcutIndex = (pKey) => {
  let k = ''
  if (pKey.key === 'Shift' || pKey.shiftKey) { k += 'shift' }
  if (pKey.key === 'Control' || pKey.ctrlKey) { k += 'ctrl' }
  if (pKey.key === 'Meta'|| pKey.metaKey) { k += 'meta' }
  if (pKey.key === 'Alt' || pKey.altKey) { k += 'alt' }
  if (pKey.key === 'ArrowUp') { k += 'arrowup' }
  if (pKey.key === 'ArrowLeft') { k += 'arrowleft' }
  if (pKey.key === 'ArrowRight') { k += 'arrowright' }
  if (pKey.key === 'ArrowDown') { k += 'arrowdown' }
  if (pKey.key === 'AltGraph') { k += 'altgraph' }
  if (pKey.key === 'Escape') { k += 'esc' }
  if (pKey.key === 'Enter') { k += 'enter' }
  if (pKey.key === 'Tab') { k += 'tab' }
  if (pKey.key === ' ') { k += 'space' }
  if (pKey.key === 'PageUp') { k += 'pageup' }
  if (pKey.key === 'PageDown') { k += 'pagedown' }
  if (pKey.key === 'Home') { k += 'home' }
  if (pKey.key === 'End') { k += 'end' }
  if (pKey.key === 'Delete') { k += 'del' }
  if (pKey.key === 'Backspace') { k += 'backspace' }
  if (pKey.key === 'Insert') { k += 'insert' }
  if (pKey.key === 'NumLock') { k += 'numlock' }
  if (pKey.key === 'CapsLock') { k += 'capslock' }
  if (pKey.key === 'Pause') { k += 'pause' }
  if (pKey.key === 'ContextMenu') { k += 'contextmenu' }
  if (pKey.key === 'ScrollLock') { k += 'scrolllock' }
  if (pKey.key === 'BrowserHome') { k += 'browserhome' }
  if (pKey.key === 'MediaSelect') { k += 'mediaselect' }
  if ((pKey.key && pKey.key !== ' ' && pKey.key.length === 1) || /F\d{1,2}|\//g.test(pKey.key)) k += pKey.key.toLowerCase()
  return k
}

const dispatchShortkeyEvent = (pKey) => {
  const e = new CustomEvent('shortkey', { bubbles: false })
  if (mapFunctions[pKey].key) e.srcKey = mapFunctions[pKey].key
  const elm = mapFunctions[pKey].el
  elm[elm.length - 1].dispatchEvent(e)
}

const dispatchShortkeyDownEvent = (pKey) => {
    const e = new CustomEvent('shortkeydown', { bubbles: false })
    if (mapFunctions[pKey].key) e.srcKey = mapFunctions[pKey].key
    const elm = mapFunctions[pKey].el
    elm[elm.length - 1].dispatchEvent(e)
  }

ShortKey.keyDown = (pKey) => {
  if ((!mapFunctions[pKey].once && !mapFunctions[pKey].push) || (mapFunctions[pKey].push && !keyPressed)) {
    dispatchShortkeyEvent(pKey)
  }
}

if (process && process.env && process.env.NODE_ENV !== 'test') {
  ;(function () {
    document.addEventListener('keydown', (pKey) => {
      const decodedKey = ShortKey.decodeKey(pKey)
      // Check avoidable elements
      if (availableElement(decodedKey)) {
        pKey.preventDefault()
        pKey.stopPropagation()
        if (mapFunctions[decodedKey].focus) {
          ShortKey.keyDown(decodedKey)
          dispatchShortkeyDownEvent(decodedKey)
          keyPressed = true
        } else if (!keyPressed) {
          const elm = mapFunctions[decodedKey].el
          elm[elm.length - 1].focus()
          keyPressed = true
        }
      }
    }, true)

    document.addEventListener('keyup', (pKey) => {
      const decodedKey = ShortKey.decodeKey(pKey)
      if (availableElement(decodedKey)) {
        pKey.preventDefault()
        pKey.stopPropagation()
        if (mapFunctions[decodedKey].once || mapFunctions[decodedKey].push) {
          dispatchShortkeyEvent(decodedKey);
        }
      }
      keyPressed = false
    }, true)
  })()
}

const mappingFunctions = ({b, push, once, focus, el}) => {
  for (let key in b) {
    const k = ShortKey.encodeKey(b[key])
    const elm = mapFunctions[k] && mapFunctions[k].el ? mapFunctions[k].el : []
    elm.push(el)
    mapFunctions[k] = {
      push,
      once,
      focus,
      key,
      el: elm
    }
  }
}

const availableElement = (decodedKey) => {
  const objectIsAvoided = !!objAvoided.find(r => r === document.activeElement)
  const filterAvoided = !!(elementAvoided.find(selector => document.activeElement && document.activeElement.matches(selector)))
  return !!mapFunctions[decodedKey] && !(objectIsAvoided || filterAvoided)
}

if (typeof module != 'undefined' && module.exports) {
  module.exports = ShortKey;
} else if (typeof define == 'function' && define.amd) {
  define( function () { return ShortKey; } );
} else {
  window.ShortKey = ShortKey;
}

export default ShortKey