function initCartItemInputCounter(inputID, incrementID, decrementID) {
  const $targetEl = document.getElementById(inputID);
  const $incrementEl = document.getElementById(incrementID);
  const $decrementEl = document.getElementById(decrementID);

  const options = {
    minValue: 0,
    maxValue: 99,
    onIncrement: () => {
      //   console.log("input field value has been incremented");
      $targetEl.dispatchEvent(new Event("change"));
    },
    onDecrement: () => {
      //   console.log("input field value has been decremented");
      $targetEl.dispatchEvent(new Event("change"));
    },
  };

  const instanceOptions = {
    id: inputID,
    override: true,
  };

  new InputCounter(
    $targetEl,
    $incrementEl,
    $decrementEl,
    options,
    instanceOptions
  );
}
