const ICONS = {
  success: {
    color: "text-green-500 bg-green-100 dark:bg-green-800 dark:text-green-200",
    svg: `<path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z" />`,
    srLabel: "Check icon",
  },
  error: {
    color: "text-red-500 bg-red-100 dark:bg-red-800 dark:text-red-200",
    svg: `<path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z" />`,
    srLabel: "Error icon",
  },
  warning: {
    color:
      "text-orange-500 bg-orange-100 dark:bg-orange-800 dark:text-orange-200",
    svg: `<path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z" />`,
    srLabel: "Warning icon",
  },
  info: {
    color: "text-blue-500 bg-blue-100 dark:bg-blue-800 dark:text-blue-200",
    svg: `<path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.147 15.085a7.159 7.159 0 0 1-6.189 3.307A6.713 6.713 0 0 1 3.1 15.444c-2.679-4.513.287-8.737.888-9.548A4.373 4.373 0 0 0 5 1.608c1.287.953 6.445 3.218 5.537 10.5 1.5-1.122 2.706-3.01 2.853-6.14 1.433 1.049 3.993 5.395 1.757 9.117Z"/>`,
    svgSize: "size-4",
    svgFill: "none",
    srLabel: "Info icon",
  },
};

const TOAST_TEMPLATE = (type, message) => {
  const { color, svg, svgSize, svgFill, srLabel } = ICONS[type];

  return `
    <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 rounded-lg ${color}">
      <svg class="${
        svgSize ? svgSize : "size-5"
      }" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="${
    svgFill ? svgFill : "currentColor"
  }" viewBox="0 0 20 20">
        ${svg}
      </svg>
      <span class="sr-only">${srLabel}</span>
    </div>
    <div class="ms-3 text-sm font-normal">${message}</div>
    <button onclick="dismissToast(event)" type="button" class="ms-2 sm:ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700" aria-label="Close">
      <span class="sr-only">Close</span>
      <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
      </svg>
    </button>
  `;
};
// const toastsContainer = document.getElementById("toasts-container");
const BASE_TOAST_CLASSES =
  "animate-fade-in toast flex items-center w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow-sm border dark:text-gray-400 dark:bg-gray-800";

htmx.on("messages", (e) => {
  const messages = e.detail.value;

  messages.forEach((m) => {
    const $toast = document.createElement("div");
    createToast($toast, m.tags, m.message);
  });
});

function autoRemoveToast($toast) {
  const dismiss = new Dismiss($toast);
  setTimeout(() => {
    dismiss.hide();
    setTimeout(() => {
      $toast.remove();
    }, 400);
  }, 5000);
}

function createToast($toast, tags, message) {
  $toast.className = BASE_TOAST_CLASSES;
  $toast.setAttribute("role", "alert");
  $toast.innerHTML = TOAST_TEMPLATE(tags, message);
  toastsContainer.appendChild($toast);
  autoRemoveToast($toast);
}

function dismissToast(e) {
  const $toast = e.target.closest(".toast");

  if ($toast) {
    const dismiss = new Dismiss($toast);
    dismiss.hide();
    setTimeout(() => {
      $toast.remove();
    }, 400);
  }
}
