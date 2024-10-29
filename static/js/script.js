htmx.on("updateModals", (e) => {
  const event = e.detail;

  if (event.close) {
    event.close.forEach((id) => {
      closeModal(id);
    });
  }

  if (event.open) {
    event.open.forEach((id) => {
      openModal(id);
    });
  }
});

htmx.on("htmx:confirm", (e) => {
  e.preventDefault();

  const question = e.detail.question;

  if (!question) {
    e.detail.issueRequest(true);
    return;
  }

  const modalCloseID = e.target.getAttribute("modal-close-id");
  if (modalCloseID) {
    closeModal(modalCloseID);
  }

  document.getElementById("question-label").textContent = question;
  openModal("confirm-delete-modal");

  const $btnConfirm = document.getElementById("btn-confirm");
  $btnConfirm.onclick = function (event) {
    e.detail.issueRequest(true);
    closeModal("confirm-delete-modal");
  };
});

function closeModal(id) {
  const $elm = document.getElementById(id);
  if ($elm) {
    const modal = new Modal($elm);
    modal.hide();
  }
}

function openModal(id) {
  const $elm = document.getElementById(id);
  if ($elm) {
    const modal = new Modal($elm);
    modal.show();
  }
}

function previewAvatar(e) {
  const file = e.target.files[0];
  const acceptedTypes = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
  ];

  if (file && acceptedTypes.includes(file.type)) {
    const reader = new FileReader();

    reader.onload = function (event) {
      const $preview = document.getElementById("avatar-preview");

      $preview.src = event.target.result;
    };

    reader.readAsDataURL(file);
  }
}

function enableButton(id) {
  const $btn = document.getElementById(id);

  if ($btn && $btn.disabled == true) {
    $btn.disabled = false;
  }
}

function updateRangeNumberInput(e, ortherID) {
  const orther = document.getElementById(ortherID);
  orther.value = e.target.value;
}
