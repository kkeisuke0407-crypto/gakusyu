(function () {
  var button = document.getElementById('measurement-optout');
  if (!button) return;
  function refresh() {
    var off = localStorage.getItem('sou_measurement_optout') === '1';
    button.textContent = off ? 'このブラウザで計測を再開する' : 'このブラウザで計測を停止する';
    document.getElementById('measurement-status').textContent = off ? '現在、このブラウザの計測は停止しています。' : '現在、このブラウザの計測は有効です。';
  }
  try {
    refresh();
    button.addEventListener('click', function () {
      localStorage.setItem('sou_measurement_optout', localStorage.getItem('sou_measurement_optout') === '1' ? '0' : '1');
      refresh();
    });
  } catch (_) { button.hidden = true; }
})();
