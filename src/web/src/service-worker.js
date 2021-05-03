importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.1.5/workbox-sw.js');

const dynamicCache = 'dynamic';
self.__precacheManifest = [].concat(self.__precahceManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});

self.addEventListener('activate', evt => {
    evt.waitUntil(
        caches.keys().then(keys => {
            // If the key cache isn't the new version, delete it
            return Promise.all(keys
                .filter(key => key !== staticCache && key !== dynamicCache)
                .map(key => caches.delete(key))
            )
        })
    )
});

self.addEventListener('message', evt => {
  if (evt.data && evt.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', evt => {
  // Cache Then Network Strategy
  evt.respondWith(
    caches.open('dynamicCache').then(cache => {
      return fetch(evt.request).then(response => {
        cache.put(evt.request, response.clone());
        limitCacheSize(dynamicCache, 15);
        return response;
      })
    // Cache First Strat  
    // caches.open(evt.request).then(cacheRes => {
    //   return cacheRes || fetch(evt.request).then(fetchRes => {
    //     return caches.open(dynamicCacheName).then(cache => {
    //       cache.put(evt.request.url, fetchRes.clone());
    //       // check cached items size
    //       limitCacheSize(dynamicCacheName, 15);
    //       return fetchRes;
    //     })
    //   });
    }).catch(() => {
      if(evt.request.url.indexOf('.html') > -1){
        return caches.match('/fallback.html');
      } 
    })
  );
});