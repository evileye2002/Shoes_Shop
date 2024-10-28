function intInputRatings() {
  const inputRatings = document.querySelectorAll("[data-input-rating]");

  inputRatings.forEach(function (elm) {
    elm.addEventListener("click", function (e) {
      const farther = e.target.farthestViewportElement;

      if (!farther) return;

      if (farther.matches("[data-rating-star]")) {
        const ratingPoint = Number(farther.getAttribute("data-rating-point"));
        const label = elm.querySelector("[data-rating-label]");
        const ratingValue = elm.querySelector("[data-rating-value]");
        const ratingStars = elm.querySelectorAll("[data-rating-star]");

        label.textContent = ratingPoint;
        ratingValue.value = ratingPoint;

        ratingStars.forEach(function (star) {
          const currRatingPoint = Number(
            star.getAttribute("data-rating-point")
          );

          star.classList.toggle("text-gray-300", currRatingPoint > ratingPoint);
          star.classList.toggle(
            "text-yellow-300",
            currRatingPoint <= ratingPoint
          );
        });
      }
    });
  });
}

intInputRatings();
