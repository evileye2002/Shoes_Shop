function initDatepicker(id, options = null) {
  const $elm = document.getElementById(id);

  if (!$elm) return;

  if (!options) {
    options = {
      autohide: true,
      format: "dd-mm-yyyy",
      orientation: "top",
      // clearBtn: true,
      // todayBtn: true,
      // todayBtnMode: 1,
      weekStart: 1,
      language: "vi",
    };
  }
  new Datepicker($elm, options);
}
