/* Яндекс Метрика для всех страниц сайта.
   Впишите номер счётчика вместо null, например: window.YM_ID = 12345678;
   Пока номера нет, Метрика не загружается и ничего не отправляется. */
window.YM_ID = null;

(function () {
  var id = window.YM_ID;
  if (!id) return;
  (function (m, e, t, r, i, k, a) {
    m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
    m[i].l = 1 * new Date();
    for (var j = 0; j < document.scripts.length; j++) { if (document.scripts[j].src === r) { return; } }
    k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a);
  })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
  window.ym(id, 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: true });
})();

/* Отправить цель: ymGoal('finish', {score: 7}). Без номера счётчика ничего не делает. */
window.ymGoal = function (name, params) {
  try { if (window.YM_ID && window.ym) window.ym(window.YM_ID, 'reachGoal', name, params); } catch (e) {}
};
