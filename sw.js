/* Service worker: makes the app installable and usable offline.
   Bump CACHE when you want every phone to drop old cached files. */
const CACHE = 'bangla-vocab-v1';
const ASSETS = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/maskable-512.png', 'icons/apple-touch-icon.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function staleWhileRevalidate(req) {
  return caches.match(req).then((hit) => {
    const net = fetch(req).then((res) => {
      if (res && (res.ok || res.type === 'opaque')) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); }
      return res;
    }).catch(() => hit);
    return hit || net;
  });
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Page loads: network first (so a new push shows up), cache when offline or slow.
  if (req.mode === 'navigate') {
    e.respondWith(
      Promise.race([
        fetch(req).then((res) => { const copy = res.clone(); caches.open(CACHE).then((c) => c.put('index.html', copy)); return res; }),
        new Promise((_, rej) => setTimeout(rej, 4000)),
      ]).catch(() => caches.match('index.html').then((r) => r || caches.match('./')))
    );
    return;
  }
  // Own files and the Firebase SDK: serve from cache, refresh in the background.
  if (url.origin === self.location.origin || (url.hostname === 'www.gstatic.com' && url.pathname.startsWith('/firebasejs/'))) {
    e.respondWith(staleWhileRevalidate(req));
  }
  // Everything else (Firestore, Google sign-in, fonts) goes straight to the network.
});
