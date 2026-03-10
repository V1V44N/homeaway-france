(function () {
  const STORAGE_KEY = 'homeaway_lang'

  function getInitialLang() {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) return saved
    const browser = navigator.language || navigator.userLanguage || 'fr'
    return browser.startsWith('fr') ? 'fr' : 'en'
  }

  let currentLang = getInitialLang()

  function applyLang(lang) {
    currentLang = lang
    localStorage.setItem(STORAGE_KEY, lang)

    document.querySelectorAll('[data-fr][data-en]').forEach(el => {
      el.textContent = el.dataset[lang]
    })
    document.querySelectorAll('[data-fr-placeholder][data-en-placeholder]').forEach(el => {
      el.placeholder = lang === 'fr' ? el.dataset.frPlaceholder : el.dataset.enPlaceholder
    })

    const btn = document.getElementById('langToggleBtn')
    if (btn) {
      btn.querySelector('.lang-active').textContent   = lang === 'fr' ? 'FR' : 'EN'
      btn.querySelector('.lang-inactive').textContent = lang === 'fr' ? 'EN' : 'FR'
    }

    document.documentElement.lang = lang
  }

  function injectLangToggle(selector) {
    // Try the given selector first, then common fallbacks
    const candidates = [selector, '.nav-links', '.nav-right', '.header-controls', 'nav', 'header'].filter(Boolean)
    let target = null
    for (const sel of candidates) {
      target = document.querySelector(sel)
      if (target) break
    }
    if (!target) {
      console.warn('HomeAwayLang: could not find nav container')
      return
    }

    // Don't inject twice
    if (document.getElementById('langToggleBtn')) return

    const btn = document.createElement('button')
    btn.id = 'langToggleBtn'
    btn.setAttribute('title', 'Switch language / Changer la langue')
    btn.style.cssText = [
      'display:inline-flex', 'align-items:center', 'gap:5px',
      'background:var(--card,#1a1714)', 'border:1px solid var(--border,#2a2420)',
      'border-radius:8px', 'padding:0.45rem 0.8rem', 'cursor:pointer',
      'font-family:Outfit,sans-serif', 'font-size:0.75rem', 'font-weight:600',
      'color:var(--muted,#7a6a5a)', 'transition:border-color 0.15s,color 0.15s',
      'flex-shrink:0', 'white-space:nowrap',
    ].join(';')

    btn.innerHTML = `
      <span style="font-size:0.9rem;line-height:1">🌐</span>
      <span class="lang-active" style="color:var(--accent,#d4763b)">FR</span>
      <span style="color:var(--border,#3a3028);font-weight:300">|</span>
      <span class="lang-inactive" style="opacity:0.5">EN</span>
    `

    btn.addEventListener('mouseenter', () => { btn.style.borderColor = 'var(--accent,#d4763b)'; btn.style.color = 'var(--text,#f0e8dc)' })
    btn.addEventListener('mouseleave', () => { btn.style.borderColor = 'var(--border,#2a2420)'; btn.style.color = 'var(--muted,#7a6a5a)' })
    btn.addEventListener('click', () => applyLang(currentLang === 'fr' ? 'en' : 'fr'))

    target.appendChild(btn)
    applyLang(currentLang)
  }

  window.HomeAwayLang = { applyLang, injectLangToggle, getCurrent: () => currentLang }

  // Auto-apply translations on load even before injectLangToggle is called
  document.addEventListener('DOMContentLoaded', () => applyLang(currentLang))
})()