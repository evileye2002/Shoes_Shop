const DEFAULT_OPTIONS = {
  minValue: 0,
  maxValue: 99,
  onIncrement: () => {},
  onDecrement: () => {},
};

function initCartItemInputCounter(inputID, incrementID, decrementID, options) {
  const $targetEl = document.getElementById(inputID);
  const final_options = {
    ...options,
    onIncrement: () => {
      $targetEl.dispatchEvent(new Event("change"));
    },
    onDecrement: () => {
      $targetEl.dispatchEvent(new Event("change"));
    },
  };
  initCustomInputCounter(inputID, incrementID, decrementID, final_options);
}

function initCustomInputCounter(
  inputID,
  incrementID,
  decrementID,
  options = null
) {
  const $targetEl = document.getElementById(inputID);
  const $incrementEl = document.getElementById(incrementID);
  const $decrementEl = document.getElementById(decrementID);

  const final_options = {
    ...DEFAULT_OPTIONS,
    ...(options ? options : {}),
  };

  const instanceOptions = {
    id: inputID,
    override: options ? options.override : true,
  };

  new InputCounter(
    $targetEl,
    $incrementEl,
    $decrementEl,
    final_options,
    instanceOptions
  );

  // console.log(inputCounter);
}
