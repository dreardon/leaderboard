var mixer = mixitup('.container-fluid', {
    animation: {
        duration: 300
    }
});

mixitup('#mix-wrapper', {
  load: {
    sort: 'order:asc'
  },
  animation: {
    effects: 'fade rotateZ(-180deg)',
    duration: 700
  },
  classNames: {
    elementSort: 'sort-btn'
  },
  selectors: {
    target: '.mix-target'
  }
});
