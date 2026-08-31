(function () {
  var grid = document.getElementById('project-grid');
  var countEl = document.getElementById('project-count');
  if (!grid || !countEl) return;

  var cards = Array.prototype.slice.call(grid.children);
  var total = cards.length;
  var buttons = Array.prototype.slice.call(document.querySelectorAll('#project-filters .filter-btn'));

  function apply(filter) {
    var shown = 0;
    cards.forEach(function (card) {
      var techs = (card.getAttribute('data-tech') || '').toLowerCase().split(',');
      var match = filter === 'all' || techs.indexOf(filter) !== -1;
      card.hidden = !match;
      if (match) shown++;
    });
    var label = total === 1 ? ' project' : ' projects';
    countEl.textContent = filter === 'all'
      ? total + label
      : 'Showing ' + shown + ' of ' + total + label;
  }

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      buttons.forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      apply(btn.getAttribute('data-filter'));
    });
  });
})();