const CACHE = 'scripture-studio-v1';
const OFFLINE_URLS = ['/'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => {
      return cache.addAll(OFFLINE_URLS);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      return (
        cached ||
        fetch(event.request)
          .then((resp) => {
            const copy = resp.clone();
            caches.open(CACHE).then((cache) => cache.put(event.request, copy));
            return resp;
          })
          .catch(() => caches.match('/'))
      );
    })
  );
});
